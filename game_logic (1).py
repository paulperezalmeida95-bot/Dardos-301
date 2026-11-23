"""Lógica central y reglas de Dardos 301."""
from dataclasses import dataclass


@dataclass
class Game:
    """Partida 301 para dos participantes; este objeto administra el estado."""
    players: tuple[str, str] = ("Jugador 1", "Jugador 2")
    scores: list[int] | None = None
    current: int = 0
    darts_this_turn: int = 0
    status: str = "en_curso"
    winner: str | None = None
    last_message: str = "Partida iniciada."
    turn_start_score: int | None = None

    def __post_init__(self):
        if len(self.players) != 2 or any(not str(name).strip() for name in self.players):
            raise ValueError("La partida requiere exactamente dos nombres válidos.")
        if self.scores is None:
            self.scores = [301, 301]
        if len(self.scores) != 2 or any(not isinstance(score, int) or score < 0 for score in self.scores):
            raise ValueError("El marcador debe contener dos puntajes enteros no negativos.")
        if self.current not in (0, 1):
            raise ValueError("Índice de jugador inválido.")
        if self.turn_start_score is None:
            self.turn_start_score = self.scores[self.current]

    def play(self, points: int) -> dict:
        """Procesa un tiro entre 0 y 60; bust restaura el puntaje al inicio del turno."""
        if self.status != "en_curso":
            raise ValueError("La partida ya terminó.")
        if isinstance(points, bool) or not isinstance(points, int) or not 0 <= points <= 60:
            raise ValueError("Los puntos deben ser un entero entre 0 y 60.")

        player = self.current
        after = self.scores[player] - points
        self.darts_this_turn += 1

        if after < 0 or after == 1:
            self.scores[player] = self.turn_start_score
            self.last_message = f"{self.players[player]}: bust; conserva {self.turn_start_score} puntos."
            self._next_player()
        elif after == 0:
            self.scores[player] = 0
            self.status = "finalizada"
            self.winner = self.players[player]
            self.last_message = f"¡{self.winner} gana la partida!"
        else:
            self.scores[player] = after
            self.last_message = f"{self.players[player]} anota {points}; le quedan {after}."
            if self.darts_this_turn == 3:
                self._next_player()

        return self.to_dict()

    def _next_player(self):
        self.current = 1 - self.current
        self.darts_this_turn = 0
        self.turn_start_score = self.scores[self.current]

    def to_dict(self) -> dict:
        """Devuelve una copia serializable del estado actual."""
        return {
            "players": list(self.players), "scores": list(self.scores),
            "current": self.current, "current_player": self.players[self.current],
            "darts_this_turn": self.darts_this_turn, "status": self.status,
            "winner": self.winner, "last_message": self.last_message,
        }
