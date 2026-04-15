import unittest
from rpn import evaluar_rpn, RPNError


class TestRPN(unittest.TestCase):

    # -------------------------
    # CASOS BASICOS
    # -------------------------
    def test_basicos(self):
        self.assertEqual(evaluar_rpn("3 4 +"), 7)
        self.assertEqual(evaluar_rpn("5 1 2 + 4 * + 3 -"), 14)

    def test_reales(self):
        self.assertAlmostEqual(evaluar_rpn("2.5 2 *"), 5.0)

    def test_division(self):
        self.assertEqual(evaluar_rpn("6 2 /"), 3)

    # -------------------------
    # CONSTANTES
    # -------------------------
    def test_constantes(self):
        self.assertAlmostEqual(evaluar_rpn("p"), 3.141592, places=5)
        self.assertAlmostEqual(evaluar_rpn("e"), 2.71828, places=5)
        self.assertAlmostEqual(evaluar_rpn("j"), 1.61803, places=5)

    # -------------------------
    # PILA
    # -------------------------
    def test_pila(self):
        self.assertEqual(evaluar_rpn("3 dup *"), 9)
        self.assertEqual(evaluar_rpn("5 2 swap /"), 0.4)

    def test_drop(self):
        self.assertEqual(evaluar_rpn("3 4 drop"), 3)

    def test_clear(self):
        self.assertEqual(evaluar_rpn("3 4 clear 5"), 5)

    # -------------------------
    # FUNCIONES
    # -------------------------
    def test_funciones(self):
        self.assertEqual(evaluar_rpn("9 sqrt"), 3)
        self.assertEqual(evaluar_rpn("2 3 yx"), 8)

    def test_funciones_unarias(self):
        self.assertEqual(evaluar_rpn("10 log"), 1)
        self.assertAlmostEqual(evaluar_rpn("2.718281828 ln"), 1, places=5)
        self.assertAlmostEqual(evaluar_rpn("1 ex"), 2.71828, places=5)
        self.assertEqual(evaluar_rpn("2 10x"), 100)
        self.assertEqual(evaluar_rpn("2 1/x"), 0.5)
        self.assertEqual(evaluar_rpn("5 chs"), -5)

    # -------------------------
    # ERRORES
    # -------------------------
    def test_errores_basicos(self):
        with self.assertRaises(RPNError):
            evaluar_rpn("3 +")  # pila insuficiente

        with self.assertRaises(RPNError):
            evaluar_rpn("3 0 /")  # división por cero

        with self.assertRaises(RPNError):
            evaluar_rpn("a")  # token inválido

        with self.assertRaises(RPNError):
            evaluar_rpn("1 2")  # sobran elementos

        with self.assertRaises(RPNError):
            evaluar_rpn("-1 sqrt")  # raíz negativa

    def test_errores_funciones(self):
        with self.assertRaises(RPNError):
            evaluar_rpn("0 log")  # log inválido

        with self.assertRaises(RPNError):
            evaluar_rpn("0 ln")  # ln inválido

        with self.assertRaises(RPNError):
            evaluar_rpn("0 1/x")  # división por cero

    def test_errores_pila(self):
        with self.assertRaises(RPNError):
            evaluar_rpn("dup")

        with self.assertRaises(RPNError):
            evaluar_rpn("swap")

        with self.assertRaises(RPNError):
            evaluar_rpn("drop")

    def test_clear_invalido(self):
        with self.assertRaises(RPNError):
            evaluar_rpn("clear")  # queda pila vacía

    def test_expresion_vacia(self):
        with self.assertRaises(RPNError):
            evaluar_rpn("")


if __name__ == "__main__":
    unittest.main()