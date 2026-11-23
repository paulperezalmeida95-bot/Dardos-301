"""Cliente TCP de Dardos 301. Uso: python3 client.py <IP-servidor> [puerto]."""
import json
import socket
import sys

DEFAULT_PORT = 5050


def send_json(connection, data):
    connection.sendall((json.dumps(data, ensure_ascii=False) + "\n").encode("utf-8"))


def receive_json(reader):
    line = reader.readline()
    if not line:
        raise ConnectionError("El servidor cerró la conexión.")
    message = json.loads(line)
    if not isinstance(message, dict):
        raise ValueError("El servidor envió un mensaje con formato inválido.")
    return message


def show_state(state):
    print("\n" + "=" * 40)
    print("DARDOS 301 — MODO LAN")
    for name, score in zip(state["players"], state["scores"]):
        marker = "  <-- turno" if name == state["current_player"] else ""
        print(f"{name}: {score}{marker}")
    print(state["last_message"])
    print("=" * 40)


def ask_points():
    while True:
        raw = input("Tu tiro, puntos (0-60): ").strip()
        try:
            points = int(raw)
            if not 0 <= points <= 60:
                raise ValueError
            return points
        except ValueError:
            print("Ingresa un número entero entre 0 y 60.")


def main():
    if len(sys.argv) not in (2, 3):
        raise SystemExit("Uso: python3 client.py <IP-servidor> [puerto]")
    host = sys.argv[1]
    try:
        port = int(sys.argv[2]) if len(sys.argv) == 3 else DEFAULT_PORT
        if not 1 <= port <= 65535:
            raise ValueError
    except ValueError:
        raise SystemExit("El puerto debe ser un número entre 1 y 65535.")

    try:
        with socket.create_connection((host, port), timeout=10) as connection:
            connection.settimeout(None)
            print(f"Conectado a {host}:{port}")
            with connection.makefile("r", encoding="utf-8") as reader:
                while True:
                    message = receive_json(reader)
                    if message.get("tipo") == "error":
                        print(f"Jugada rechazada: {message.get('mensaje', 'error desconocido')}")
                        if "state" in message:
                            show_state(message["state"])
                        continue
                    if message.get("tipo") != "estado" or "state" not in message:
                        raise ValueError("Mensaje del servidor no reconocido.")
                    state = message["state"]
                    show_state(state)
                    if state["status"] != "en_curso":
                        print(f"Partida finalizada. Ganador: {state['winner']}")
                        break
                    if state["current"] == 1:
                        send_json(connection, {"tipo": "jugada", "puntos": ask_points()})
    except (OSError, ConnectionError, json.JSONDecodeError, ValueError, KeyError) as error:
        print(f"No se pudo continuar la partida: {error}")


if __name__ == "__main__":
    main()
