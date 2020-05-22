import unittest
import parser
import data_structs as ds


class TestDataStruct(unittest.TestCase):
        
    def test_create_literal(self):
        aPos = ds.Literal("a", False)
        aNeg = ds.Literal("a", True)
        bPos = ds.Literal("b", False)
        bNeg = ds.Literal("b", True)
        
        self.assertTrue(aNeg.neg)
        self.assertEqual(aNeg.atom, "a")

        self.assertTrue(bNeg.neg)
        self.assertEqual(bNeg.atom, "b")

        self.assertFalse(aPos.neg)
        self.assertEqual(aPos.atom, "a")

        self.assertFalse(bPos.neg)
        self.assertEqual(bPos.atom, "b")

    def test_negate_literal(self):
        aPos = ds.Literal("a", False)
        negate_aPos = ds.Literal.build_not_literal(aPos)
        self.assertTrue(negate_aPos.neg)

        aNeg = ds.Literal("a", True)
        negate_aNeg = ds.Literal.build_not_literal(aNeg)
        self.assertFalse(negate_aNeg.neg)

    def test_build_or_formula(self):
        aPos = ds.Literal("a", False)
        bNeg = ds.Literal("b", True)
        or_form_literal_terms = ds.Formula.build_or_formula([aPos, bNeg])
        
        self.assertEqual(or_form_literal_terms.terms, [aPos, bNeg])
        self.assertEqual(or_form_literal_terms.operator, ds.Operator.OR)
        self.assertEqual(or_form_literal_terms.formula_bool, [False, False])

        self.assertIsInstance(or_form_literal_terms.terms[0], ds.Literal)
        self.assertIsInstance(or_form_literal_terms.terms[1], ds.Literal)

    def test_build_and_formula(self):
        aNeg = ds.Literal("a", True)
        bPos = ds.Literal("b", False)
        and_form_literal_terms = ds.Formula.build_and_formula([aNeg, bPos])
        
        self.assertEqual(and_form_literal_terms.terms, [aNeg, bPos])
        self.assertEqual(and_form_literal_terms.operator, ds.Operator.AND)
        self.assertEqual(and_form_literal_terms.formula_bool, [False, False])

        self.assertIsInstance(and_form_literal_terms.terms[0], ds.Literal)
        self.assertIsInstance(and_form_literal_terms.terms[1], ds.Literal)

    def test_negate_or_formula(self):
        aPos = ds.Literal("a", False)
        bNeg = ds.Literal("b", True)
        or_form_literal_terms = ds.Formula.build_or_formula([aPos, bNeg])
        negate_or = ds.Formula.build_not_formula(or_form_literal_terms)

        self.assertEqual(negate_or.terms, [aPos, bNeg])
        self.assertEqual(negate_or.operator, ds.Operator.AND)
        self.assertEqual(negate_or.formula_bool, [False, False])

        self.assertTrue(negate_or.terms[0].neg)
        self.assertFalse(negate_or.terms[1].neg)

    def test_negate_and_formula(self):
        aPos = ds.Literal("a", False)
        bNeg = ds.Literal("b", True)
        and_form_literal_terms = ds.Formula.build_and_formula([aPos, bNeg])   # aPos and bNeg
        negate_and = ds.Formula.build_not_formula(and_form_literal_terms)  # aNeg or bPos

        self.assertEqual(negate_and.terms, [aPos, bNeg])
        self.assertEqual(negate_and.operator, ds.Operator.OR)
        self.assertEqual(negate_and.formula_bool, [False, False])

        self.assertTrue(negate_and.terms[0].neg)  # Checks aNeg in; aNeg or bPos
        self.assertFalse(negate_and.terms[1].neg)  # Checks bPos in; aNeg or bPos

    def test_negate_lit_form(self):
        aPos = ds.Literal("a", False)
        bNeg = ds.Literal("b", True)
        cPos = ds.Literal("c", False)
        or_form_literal_terms = ds.Formula.build_or_formula([aPos, bNeg])
        and_formula_lit_form = ds.Formula.build_and_formula([cPos, or_form_literal_terms])  # cPos and (aPos or bNeg)
        negate_lit_form = ds.Formula.build_not_formula(and_formula_lit_form)  # cNeg or (aNeg and bPos)

        # Tests a formula with left term a literal and right term a formula.
        self.assertIsInstance(negate_lit_form.terms[1], ds.Formula)

        self.assertTrue(negate_lit_form.terms[0].neg)  # Checks cNeg in; cNeg or (aNeg and bPos)
        self.assertTrue(negate_lit_form.terms[1].terms[0].neg)  # Checks aNeg in; cNeg or (aNeg and bPos)
        self.assertFalse(negate_lit_form.terms[1].terms[1].neg)  # Checks bPos in; cNeg or (aNeg and bPos)

        self.assertEqual(negate_lit_form.operator, ds.Operator.OR)  # Checks the outer operator
        self.assertEqual(negate_lit_form.terms[1].operator, ds.Operator.AND)  # Checks the inner operator

    def test_negate_form_lit(self):
        aNeg = ds.Literal("a", True)
        bPos = ds.Literal("b", False)
        cPos = ds.Literal("a", False)
        and_form_literal_terms = ds.Formula.build_and_formula([aNeg, bPos])
        and_formula_form_lit = ds.Formula.build_and_formula([and_form_literal_terms, cPos])  # (aNeg and bPos) and cPos
        negate_form_lit = ds.Formula.build_not_formula(and_formula_form_lit)  # (aPos or bNeg) or cNeg

        # Tests a formula with right term a literal and left term a formula.
        self.assertIsInstance(negate_form_lit.terms[0], ds.Formula)

        self.assertTrue(negate_form_lit.terms[1].neg)  # Checks cNeg in; (aPos or bNeg) or cNeg
        self.assertTrue(negate_form_lit.terms[0].terms[1].neg)  # Checks bPos in; (aPos or bNeg) or cNeg
        self.assertFalse(negate_form_lit.terms[0].terms[0].neg)  # Checks aPos in; (aPos or bNeg) or cNeg

        self.assertEqual(negate_form_lit.operator, ds.Operator.OR)  # Checks for the outer operator
        self.assertEqual(negate_form_lit.terms[0].operator, ds.Operator.OR)  # Checks the inner operator

    def test_negate_form_form(self):
        aPos = ds.Literal("a", False)
        bNeg = ds.Literal("b", True)
        cNeg = ds.Literal("a", True)
        dPos = ds.Literal("d", False)
        or_form_literal = ds.Formula.build_or_formula([aPos, bNeg])
        and_form_literal = ds.Formula.build_and_formula([cNeg, dPos])
        and_formula_form = ds.Formula.build_and_formula([or_form_literal, and_form_literal])  # (aPos or bNeg) and (cNeg and dPos)
        negate_form = ds.Formula.build_not_formula(and_formula_form)  # (aNeg and bPos) or (cPos or dNeg)

        # Tests a formula with both terms a formula.
        self.assertIsInstance(negate_form.terms[0], ds.Formula)  # Checks if the first term is a Formula
        self.assertIsInstance(negate_form.terms[1], ds.Formula)  # Checks if the second term is a Formula

        self.assertTrue(negate_form.terms[0].terms[0].neg)  # Checks aNeg in; (aNeg and bPos) or (cPos or dNeg)
        self.assertFalse(negate_form.terms[0].terms[1].neg)  # Checks bPos in; (aNeg and bPos) or (cPos or dNeg)
        self.assertFalse(negate_form.terms[1].terms[0].neg)  # Checks cPos in; (aNeg and bPos) or (cPos or dNeg)
        self.assertTrue(negate_form.terms[1].terms[1].neg)  # Checks dNeg in; (aNeg and bPos) or (cPos or dNeg)

        self.assertEqual(negate_form.operator, ds.Operator.OR)  # Checks the outer operator
        self.assertEqual(negate_form.terms[0].operator, ds.Operator.AND)  # Checks the left inner operator
        self.assertEqual(negate_form.terms[1].operator, ds.Operator.OR)  # Checks the right inner operator

    def test_for_equal_formulas(self):
        a = ds.Literal("a", False)
        b = ds.Literal("b", False)
        rule_a = ds.Rule(ds.Literal("p", False), a)
        rule_b = ds.Rule(ds.Literal("p", False), b)
        tmp = ds.Program()
        self.assertTrue(tmp.check_for_equal_formulas(rule_a.conclusion, rule_b.conclusion))

    def test_pb_to_icb_same_conc(self):
        a = ds.Literal("a", False)
        b = ds.Literal("b", False)
        rule_a = ds.Rule(ds.Literal("p", False), a)
        rule_b = ds.Rule(ds.Literal("p", False), b)
        combined_rule_list = ds.pb_to_icb([rule_a, rule_b])

        self.assertEqual(combined_rule_list[0].premise.terms[0].atom, "b")
        self.assertEqual(combined_rule_list[0].premise.operator, ds.Operator.OR)
        self.assertEqual(combined_rule_list[0].premise.terms[1].atom, "a")

    def test_pb_to_icb_conflict_conc(self):
        a = ds.Literal("a", False)
        b = ds.Literal("b", False)
        rule_a = ds.Rule(ds.Literal("p", False), a)  # p <- a.
        rule_b = ds.Rule(ds.Literal("p", True), b)  # -p <- b.
        combined_rule_list = ds.pb_to_icb([rule_a, rule_b])

        # Must become -p <- b and -a.
        self.assertEqual(combined_rule_list[0].premise.terms[0].atom, "b")
        self.assertEqual(combined_rule_list[0].premise.operator, ds.Operator.AND)
        self.assertEqual(combined_rule_list[0].premise.terms[1].atom, "a")
        self.assertTrue(combined_rule_list[0].premise.terms[1].neg)
        self.assertEqual(combined_rule_list[0].conclusion.atom, "p")
        self.assertTrue(combined_rule_list[0].conclusion.neg)

    # def test_multiple_conflict_conc(self):
        # a = ds.Literal("a", False)
        # b = ds.Literal("b", False)
        # c = ds.Literal("c", False)
        # d = ds.Literal("d", False)
        # rule_a = ds.Rule(ds.Literal("p", False), a)  # p <- a.
        # rule_b = ds.Rule(ds.Literal("p", True), b)  # -p <- b.
        # rule_c = ds.Rule(ds.Literal("p", False), c)  # p <- c.
        # rule_d = ds.Rule(ds.Literal("m", True), d)  # -p <- d.
        #
        # combined_rule_list = ds.pb_to_icb([rule_d, rule_c, rule_b, rule_a])
        # # Must become: p <- ((a and -b) or c) and -d).
        # print(combined_rule_list[0].conclusion.atom)
        # print(combined_rule_list[0].conclusion.neg)
        # print(combined_rule_list[0].premise.terms[0].terms[0])
        # # self.assertEqual(combined_rule_list[0].premise.terms[0].terms[0].atom, "a")
        # # self.assertEqual(combined_rule_list[0].premise.terms[0].terms[1].atom, "b")
        # # self.assertEqual(combined_rule_list[0].premise.terms[0].operator, ds.Operator.AND)  # Check inner "AND"
        # # self.assertEqual(combined_rule_list[0].premise.terms[1].atom, "c")
        # # self.assertEqual(combined_rule_list[0].premise.terms[0].operator, ds.Operator.OR)  # Check middle "OR"
        # # self.assertEqual(combined_rule_list[0].premise.terms[0].atom, "d")
        # # self.assertEqual(combined_rule_list[0].premise.operator, ds.Operator.AND)  # Check outer "AND"
        #
        # self.assertFalse(combined_rule_list[0].premise.terms[0].terms[0].terms[0].neg)  # Check if a positive
        # self.assertTrue(combined_rule_list[0].premise.terms[0].terms[0].terms[1].neg)  # Check if b negative
        # self.assertFalse(combined_rule_list[0].premise.terms[0].terms[1].neg)  # Check if c positive
        # self.assertTrue(combined_rule_list[0].premise.terms[1].neg)  # Check if d negative


if __name__ == '__main__':
    unittest.main()
