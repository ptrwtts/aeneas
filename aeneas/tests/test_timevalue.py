#!/usr/bin/env python
# coding=utf-8

import unittest
import numpy

from aeneas.timevalue import Decimal
from aeneas.timevalue import TimeValue

class TestTimeValue(unittest.TestCase):

    def check(self, value, expected=None):
        self.assertTrue(isinstance(value, TimeValue))
        if expected is not None:
            self.assertEqual(value, expected)

    def check_numpy(self, value, expected=None):
        #print(type(value))
        #print(type(value[0]))
        self.assertTrue(isinstance(value[0], TimeValue))
        self.assertTrue((value == expected).all())

    def test_create_from_float(self):
        tv1 = TimeValue(1.234)
        self.check(tv1)

    def test_create_from_string(self):
        tv1 = TimeValue("1.234")
        self.check(tv1)

    def test_repr(self):
        tv1 = TimeValue("1.234")
        self.assertEqual(tv1.__repr__(), "TimeValue('1.234')")

    def test_add(self):
        tv1 = TimeValue("1.100")
        tv2 = TimeValue("2.200")
        tv3 = TimeValue("3.300")
        self.check(tv1 + tv2, tv3)
        self.check(tv2 + tv1, tv3)
        d = Decimal("2.200")
        self.check(tv1 + d, tv3)
        self.check(d + tv1, tv3)

    def test_div(self):
        tv1 = TimeValue("1.100")
        tv2 = TimeValue("2.200")
        tv3 = TimeValue("0.500")
        self.check(tv1 / tv2, tv3)
        d = Decimal("2.200")
        self.check(tv1 / d, tv3)

    def test_floordiv(self):
        tv1 = TimeValue("1.100")
        tv2 = TimeValue("2.200")
        tv3 = TimeValue("0.000")
        self.check(tv1 // tv2, tv3)
        d = Decimal("2.200")
        self.check(tv1 // d, tv3)

    def test_mod(self):
        tv1 = TimeValue("1.100")
        tv2 = TimeValue("2.200")
        tv3 = TimeValue("0.000")
        self.check(tv2 % tv1, tv3)
        d = Decimal("1.100")
        self.check(tv2 % d, tv3)

    def test_mul(self):
        tv1 = TimeValue("1.100")
        tv2 = TimeValue("2.200")
        tv3 = TimeValue("2.420")
        self.check(tv1 * tv2, tv3)
        self.check(tv2 * tv1, tv3)
        d = Decimal("2.200")
        self.check(tv1 * d, tv3)

    def test_sub(self):
        tv1 = TimeValue("1.100")
        tv2 = TimeValue("2.200")
        tv3 = TimeValue("-1.100")
        tv4 = TimeValue("1.100")
        self.check(tv1 - tv2, tv3)
        self.check(tv2 - tv1, tv4)
        d = Decimal("2.200")
        self.check(tv1 - d, tv3)

    def test_truediv(self):
        tv1 = TimeValue("1")
        tv2 = TimeValue("2")
        tv3 = TimeValue("0.5")
        self.check(tv1 / tv2, tv3)
        d = Decimal("2")
        self.check(tv1 / d, tv3)

    def test_op_float(self):
        tv1 = TimeValue("1.100")
        tv2 = 2.200
        tv3 = TimeValue("3.300")
        with self.assertRaises(TypeError):
            self.check(tv1 + tv2, tv3)
        with self.assertRaises(TypeError):
            self.check(tv1 / tv2, tv3)
        with self.assertRaises(TypeError):
            self.check(tv1 // tv2, tv3)
        with self.assertRaises(TypeError):
            self.check(tv1 * tv2, tv3)
        with self.assertRaises(TypeError):
            self.check(tv1 - tv2, tv3)

    def test_numpy_int(self):
        tv1 = TimeValue("1.000")
        n1 = numpy.array([0, 1, 2], dtype=int)
        n2 = numpy.array([TimeValue("1.000"),TimeValue("2.000"),TimeValue("3.000")], dtype=TimeValue)
        n3 = numpy.array([TimeValue("0.000"),TimeValue("1.000"),TimeValue("2.000")], dtype=TimeValue)
        self.check_numpy(n1 + tv1, n2)
        self.check_numpy(n1 * tv1, n3)

    def test_numpy_float(self):
        tv1 = TimeValue("1.000")
        n1 = numpy.array([0.0, 1.0, 2.0], dtype=float)
        n2 = numpy.array([TimeValue("1.000"),TimeValue("2.000"),TimeValue("3.000")], dtype=TimeValue)
        n3 = numpy.array([TimeValue("0.000"),TimeValue("1.000"),TimeValue("2.000")], dtype=TimeValue)
        with self.assertRaises(TypeError):
            self.check_numpy(n1 + tv1, n2)
        with self.assertRaises(TypeError):
            self.check_numpy(n1 * tv1, n3)

    def test_numpy_tv(self):
        tv1 = TimeValue("1.000")
        n1 = numpy.array([TimeValue("0.000"),TimeValue("1.000"),TimeValue("2.000")], dtype=TimeValue)
        n2 = numpy.array([TimeValue("1.000"),TimeValue("2.000"),TimeValue("3.000")], dtype=TimeValue)
        n3 = numpy.array([TimeValue("0.000"),TimeValue("1.000"),TimeValue("2.000")], dtype=TimeValue)
        self.check_numpy(n1 + tv1, n2)
        self.check_numpy(n1 * tv1, n3)

    def test_numpy_decimal(self):
        tv1 = TimeValue("1.000")
        n1 = numpy.array([Decimal("0.000"),Decimal("1.000"),Decimal("2.000")], dtype=Decimal)
        n2 = numpy.array([TimeValue("1.000"),TimeValue("2.000"),TimeValue("3.000")], dtype=TimeValue)
        n3 = numpy.array([TimeValue("0.000"),TimeValue("1.000"),TimeValue("2.000")], dtype=TimeValue)
        self.check_numpy(n1 + tv1, n2)
        self.check_numpy(n1 * tv1, n3)



if __name__ == '__main__':
    unittest.main()



