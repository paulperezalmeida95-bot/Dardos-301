"""Servidor TCP autoritativo de Dardos 301. Uso: python3 server.py [puerto]."""
import json
import socket
import sys
from game_logic import Game

HOST = "0.0.0.0"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 5050


def send_json(connection, data):
    connection.sendall((json.dumps(data, ensure_ascii=False) + "\n").encode("utf-8"))


def receive_json(reader):
    line = reader.readline()
    if not line:
        raise ConnectionError("El cliente se desconectó.")
    return json.loads(line)


def main():
    game = Game()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((HOST, PORT))
        listener.listen(1)
        print(f"Servidor escuchando en {HOST}:{PORT}; esperando al Jugador 2…")
        connection, address = listener.accept()
        with connection:
            print(f"Cliente conectado desde {address[0]}")
            with connection.makefile("r", encoding="utf-8") as reader:
                send_json(connection, {"tipo": "estado", "state": game.to_dict()})
                try:
                    while game.status == "en_curso":
                        if game.current == 0:
                            print(f"\nTu turno (Jugador 1). Marcador: {game.scores}")
                            raw = input("Puntos del tiro (0–60): ").strip()
                            try:
                                points = int(raw)
                                game.play(points)
                            except ValueError as error:
                                print(f"Entrada inválida: {error}")
                                continue
                            send_json(connection, {"tipo": "estado", "state": game.to_dict()})
                        else:
                            print("Esperando la jugada del Jugador 2…")
                            message = receive_json(reader)
                            if message.get("tipo") != "jugada":
                                send_json(connection, {"tipo": "error", "mensaje": "Se esperaba una jugada."})
                                continue
                            try:
                                game.play(message.get("puntos"))
                                send_json(connection, {"tipo": "estado", "state": game.to_dict()})
                            except ValueError as error:
                                send_json(connection, {"tipo": "error", "mensaje": str(error), "state": game.to_dict()})
                    print(game.last_message)
                except (ConnectionError, OSError, json.JSONDecodeError) as error:
                    print(f"Conexión terminada: {error}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nServidor cerrado.")
