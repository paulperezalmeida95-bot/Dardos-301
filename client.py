"""Cliente TCP de Dardos 301. Uso: python3 client.py <IP-servidor> [puerto]."""
import json
import socket
import sys

PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 5050


def send_json(connection, data):
    connection.sendall((json.dumps(data, ensure_ascii=False) + "\n").encode("utf-8"))


def receive_json(reader):
    line = reader.readline()
    if not line:
        raise ConnectionError("El servidor se desconectó.")
    return json.loads(line)


def show_state(state):
    print("\n" + "=" * 40)
    print("DARDOS 301 — MODO LAN")
    for name, score in zip(state["players"], state["scores"]):
        marker = "  <-- turno" if name == state["current_player"] else ""
        print(f"{name}: {score}{marker}")
    print(state["last_message"])
    print("=" * 40)


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 client.py <IP-servidor> [puerto]")
        raise SystemExit(2)
    try:
        with socket.create_connection((sys.argv[1], PORT), timeout=30) as connection:
            connection.settimeout(None)
            with connection.makefile("r", encoding="utf-8") as reader:
                print(f"Conectado a {sys.argv[1]}:{PORT}")
                while True:
                    message = receive_json(reader)
                    if message.get("tipo") == "error":
                        print(f"Jugada rechazada: {message['mensaje']}")
                        state = message.get("state")
                        if state:
                            show_state(state)
                        continue
                    if message.get("tipo") != "estado":
                        print(f"Mensaje no reconocido: {message}")
                        continue
                    state = message["state"]
                    show_state(state)
                    if state["status"] != "en_curso":
                        break
                    if state["current"] == 1:
                        while True:
                            raw = input("Tu tiro, puntos (0–60): ").strip()
                            try:
                                points = int(raw)
                                if not 0 <= points <= 60:
                                    raise ValueError
                                break
                            except ValueError:
                                print("Escribe un entero entre 0 y 60.")
                        send_json(connection, {"tipo": "jugada", "puntos": points})
    except (OSError, ConnectionError, json.JSONDecodeError) as error:
        print(f"No se pudo continuar la partida: {error}")


if __name__ == "__main__":
    main()
