"""Pruebas de unidad para las reglas de Dardos 301."""
import unittest
from game_logic import Game


class GameLogicTests(unittest.TestCase):
    def test_rechaza_puntos_fuera_de_rango_y_tipos_invalidos(self):
        game = Game()
        for value in (-1, 61, "20", True):
            with self.subTest(value=value), self.assertRaises(ValueError):
                game.play(value)
        self.assertEqual(game.scores, [301, 301])

    def test_cambia_turno_despues_de_tres_dardos(self):
        game = Game()
        game.play(20)
        game.play(20)
        state = game.play(20)
        self.assertEqual(state["scores"], [241, 301])
        self.assertEqual(state["current"], 1)
        self.assertEqual(state["darts_this_turn"], 0)

    def test_bust_restaura_puntaje_del_inicio_del_turno(self):
        game = Game(scores=[101, 301])
        game.play(20)
        game.play(60)
        state = game.play(30)  # 101 - 20 - 60 - 30 sería negativo
        self.assertEqual(state["scores"][0], 101)
        self.assertEqual(state["current"], 1)

    def test_llegar_exactamente_a_cero_determina_ganador(self):
        game = Game(scores=[40, 301])
        state = game.play(40)
        self.assertEqual(state["status"], "finalizada")
        self.assertEqual(state["winner"], "Jugador 1")
        with self.assertRaises(ValueError):
            game.play(1)

    def test_quedar_en_uno_es_bust(self):
        game = Game(scores=[61, 301])
        game.play(20)
        state = game.play(40)  # queda en 1; revierte a 61
        self.assertEqual(state["scores"], [61, 301])
        self.assertEqual(state["current"], 1)


if __name__ == "__main__":
    unittest.main()
