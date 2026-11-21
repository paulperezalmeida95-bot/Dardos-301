"""Reglas compartidas para Dardos 301."""
from dataclasses import dataclass


@dataclass
class Game:
    """Estado autoritativo de una partida 301 con dos jugadores."""
    players: tuple[str, str] = ("Jugador 1", "Jugador 2")
    scores: list[int] | None = None
    current: int = 0
    darts_this_turn: int = 0
    status: str = "en_curso"
    winner: str | None = None
    last_message: str = "Partida iniciada."
    turn_start_score: int | None = None

    def __post_init__(self):
        if self.scores is None:
            self.scores = [301, 301]
        if self.turn_start_score is None:
            self.turn_start_score = self.scores[self.current]

    def play(self, points: int) -> dict:
        """Aplica un tiro (0–60); bust restaura el puntaje inicial del turno."""
        if self.status != "en_curso":
            raise ValueError("La partida ya terminó.")
        if isinstance(points, bool) or not isinstance(points, int) or not 0 <= points <= 60:
            raise ValueError("Los puntos deben ser un entero entre 0 y 60.")

        player = self.current
        after = self.scores[player] - points
        self.darts_this_turn += 1
        bust = after < 0 or after == 1

        if bust:
            self.scores[player] = self.turn_start_score
            self.last_message = f"{self.players[player]}: bust; conserva {self.turn_start_score} puntos."
            self.current = 1 - player
            self.darts_this_turn = 0
            self.turn_start_score = self.scores[self.current]
        elif after == 0:
            self.scores[player] = 0
            self.status = "finalizada"
            self.winner = self.players[player]
            self.last_message = f"¡{self.winner} gana la partida!"
        else:
            self.scores[player] = after
            self.last_message = f"{self.players[player]} anota {points}; le quedan {after}."
            if self.darts_this_turn == 3:
                self.current = 1 - player
                self.darts_this_turn = 0
                self.turn_start_score = self.scores[self.current]

        return self.to_dict()

    def to_dict(self) -> dict:
        return {
            "players": list(self.players), "scores": list(self.scores),
            "current": self.current, "current_player": self.players[self.current],
            "darts_this_turn": self.darts_this_turn, "status": self.status,
            "winner": self.winner, "last_message": self.last_message,
        }
