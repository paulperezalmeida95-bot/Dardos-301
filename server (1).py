"""Servidor TCP autoritativo. Uso: python3 server.py [puerto]."""
import json
import socket
import sys
from game_logic import Game

HOST = "0.0.0.0"
DEFAULT_PORT = 5050


def send_json(connection, data):
    connection.sendall((json.dumps(data, ensure_ascii=False) + "\n").encode("utf-8"))


def receive_json(reader):
    line = reader.readline()
    if not line:
        raise ConnectionError("El cliente se desconectó.")
    return json.loads(line)


def run_game(connection, game):
    """Bucle alternado: el servidor controla el jugador 1 y el cliente el 2."""
    with connection.makefile("r", encoding="utf-8") as reader:
        send_json(connection, {"tipo": "estado", "state": game.to_dict()})
        while game.status == "en_curso":
            if game.current == 0:
                print(f"\nTurno de {game.players[0]}. Marcador: {game.scores}")
                raw = input("Puntos del tiro (0-60): ").strip()
                try:
                    game.play(int(raw))
                except ValueError as error:
                    print(f"Jugada inválida: {error}")
                    continue
                send_json(connection, {"tipo": "estado", "state": game.to_dict()})
                print(game.last_message)
            else:
                print("Esperando jugada del cliente...")
                message = receive_json(reader)
                if not isinstance(message, dict) or message.get("tipo") != "jugada":
                    send_json(connection, {"tipo": "error", "mensaje": "Mensaje inválido; se esperaba una jugada."})
                    continue
                try:
                    game.play(message.get("puntos"))
                except ValueError as error:
                    send_json(connection, {"tipo": "error", "mensaje": str(error), "state": game.to_dict()})
                    continue
                send_json(connection, {"tipo": "estado", "state": game.to_dict()})
                print(game.last_message)
    return game


def main():
    try:
        port = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT
        if not 1 <= port <= 65535:
            raise ValueError
    except ValueError:
        raise SystemExit("El puerto debe ser un número entre 1 y 65535.")

    game = Game()
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            listener.bind((HOST, port))
            listener.listen(1)
            print(f"Servidor escuchando en {HOST}:{port}; esperando al Jugador 2...")
            connection, address = listener.accept()
            with connection:
                print(f"Cliente conectado desde {address[0]}:{address[1]}")
                run_game(connection, game)
                print(game.last_message)
    except (ConnectionError, OSError, json.JSONDecodeError) as error:
        print(f"Partida interrumpida: {error}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nServidor cerrado por el usuario.")
