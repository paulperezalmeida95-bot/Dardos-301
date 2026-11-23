"""Modo local de Dardos 301 para dos jugadores."""
from game_logic import Game


def mostrar(game: Game) -> None:
    state = game.to_dict()
    print("\n" + "=" * 44)
    print("DARDOS 301 — MODO LOCAL")
    for name, score in zip(state["players"], state["scores"]):
        marker = "  <-- turno" if name == state["current_player"] else ""
        print(f"{name}: {score}{marker}")
    print(state["last_message"])
    print("=" * 44)


def main() -> None:
    names = []
    for index in (1, 2):
        name = input(f"Nombre del jugador {index} [Jugador {index}]: ").strip()
        names.append(name or f"Jugador {index}")
    game = Game(players=tuple(names))
    while game.status == "en_curso":
        mostrar(game)
        try:
            points = int(input(f"Puntos del tiro de {game.players[game.current]} (0–60): "))
            game.play(points)
        except ValueError as error:
            print(f"Entrada inválida: {error}")
    mostrar(game)
    print(f"Ganador: {game.winner}")


if __name__ == "__main__":
    main()
