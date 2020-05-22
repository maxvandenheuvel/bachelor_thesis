import unittest
import parser
import data_structs as ds


class TestDataStruct(unittest.TestCase):
    def setUp(self):
        self.aPos = ds.Literal("a", False)
        self.aNeg = ds.Literal("a", True)
        self.bPos = ds.Literal("b", False)
        self.bNeg = ds.Literal("b", True)

        self.literal_pos_neg = [self.aPos, self.bNeg]
        self.literal_neg_pos = [self.aNeg, self.bPos]

        self.or_form_with_literal_terms = ds.Formula.build_or_formula(self.literal_pos_neg)
        self.and_form_with_literal_terms = ds.Formula.build_and_formula(self.literal_neg_pos)
        
    def test_create_literal(self):
        self.assertTrue(self.aNeg.neg)
        self.assertEqual(self.aNeg.atom, "a")

        self.assertTrue(self.bNeg.neg)
        self.assertEqual(self.bNeg.atom, "b")

        self.assertFalse(self.aPos.neg)
        self.assertEqual(self.aPos.atom, "a")

        self.assertFalse(self.bPos.neg)
        self.assertEqual(self.bPos.atom, "b")

    def test_negate_literal(self):
        negate_aPos = ds.Literal.build_not_literal(self.aPos)
        self.assertTrue(negate_aPos.neg)

        negate_aNeg = ds.Literal.build_not_literal(self.aNeg)
        self.assertFalse(negate_aNeg.neg)

    def test_build_or_formula(self):
        self.assertEqual(self.or_form_with_literal_terms.terms, self.literal_pos_neg)
        self.assertEqual(self.or_form_with_literal_terms.operator, ds.Operator.OR)
        self.assertEqual(self.or_form_with_literal_terms.formula_bool, [False, False])

        self.assertIsInstance(self.or_form_with_literal_terms.terms[0], ds.Literal)
        self.assertIsInstance(self.or_form_with_literal_terms.terms[1], ds.Literal)

    def test_build_and_formula(self):
        self.assertEqual(self.and_form_with_literal_terms.terms, self.literal_neg_pos)
        self.assertEqual(self.and_form_with_literal_terms.operator, ds.Operator.AND)
        self.assertEqual(self.and_form_with_literal_terms.formula_bool, [False, False])

        self.assertIsInstance(self.and_form_with_literal_terms.terms[0], ds.Literal)
        self.assertIsInstance(self.and_form_with_literal_terms.terms[1], ds.Literal)

    def test_negate_or_formula(self):
        negate_or = ds.Formula.build_not_formula(self.or_form_with_literal_terms)

        self.assertEqual(negate_or.terms, self.literal_pos_neg)
        self.assertEqual(negate_or.operator, ds.Operator.AND)
        self.assertEqual(negate_or.formula_bool, [False, False])

        self.assertTrue(negate_or.terms[0].neg)
        self.assertFalse(negate_or.terms[1].neg)

    def test_negate_and_formula(self):
        negate_and = ds.Formula.build_not_formula(self.and_form_with_literal_terms)  # aPos or bNeg

        self.assertEqual(negate_and.terms, self.literal_neg_pos)
        self.assertEqual(negate_and.operator, ds.Operator.OR)
        self.assertEqual(negate_and.formula_bool, [False, False])

        self.assertFalse(negate_and.terms[0].neg)
        self.assertTrue(negate_and.terms[1].neg)

    def test_negate_lit_form(self):
        lit_form_terms = [self.aPos, self.or_form_with_literal_terms]
        and_formula_lit_form = ds.Formula.build_and_formula(lit_form_terms)  # aPos and (aPos or bNeg)
        negate_lit_form = ds.Formula.build_not_formula(and_formula_lit_form)  # aNeg or (aNeg and bPos)

        # Tests a formula with left term a literal and right term a formula.
        self.assertIsInstance(negate_lit_form.terms[1], ds.Formula)

        self.assertTrue(negate_lit_form.terms[0].neg)  # Checks first aNeg in; aNeg or (aNeg and bPos)
        self.assertTrue(negate_lit_form.terms[1].terms[0].neg)  # Checks second aNeg in; aNeg or (aNeg and bPos)
        self.assertFalse(negate_lit_form.terms[1].terms[1].neg)  # Checks bPos in; aNeg or (aNeg and bPos)

        self.assertEqual(negate_lit_form.operator, ds.Operator.OR)  # Checks the outer operator
        self.assertEqual(negate_lit_form.terms[1].operator, ds.Operator.AND)  # Checks the inner operator

    def test_negate_form_lit(self):
        form_lit_terms = [self.and_form_with_literal_terms, self.aPos]
        and_formula_form_lit = ds.Formula.build_and_formula(form_lit_terms)  # (aNeg and bPos) and aPos
        negate_form_lit = ds.Formula.build_not_formula(and_formula_form_lit)  # (aPos or bNeg) or aNeg

        # Tests a formula with right term a literal and left term a formula.
        self.assertIsInstance(negate_form_lit.terms[0], ds.Formula)

        self.assertTrue(negate_form_lit.terms[1].neg)  # Checks aNeg in; (aPos or bNeg) or aNeg
        self.assertTrue(negate_form_lit.terms[0].terms[1].neg)  # Checks bPos in; (aPos or bNeg) or aNeg
        self.assertFalse(negate_form_lit.terms[0].terms[0].neg)  # Checks aPos in; (aPos or bNeg) or aNeg

        self.assertEqual(negate_form_lit.operator, ds.Operator.OR)  # Checks for the outer operator
        self.assertEqual(negate_form_lit.terms[0].operator, ds.Operator.OR)  # Checks the inner operator

    def test_negate_form_form(self):
        formula_terms = [self.or_form_with_literal_terms, self.and_form_with_literal_terms]
        and_formula_form = ds.Formula.build_and_formula(formula_terms)  # (aPos or bNeg) and (aNeg and bPos)
        negate_form = ds.Formula.build_not_formula(and_formula_form)  # (aNeg and bPos) or (aPos or bNeg)

        # Tests a formula with both terms a formula.
        self.assertIsInstance(negate_form.terms[0], ds.Formula)  # Checks if the first term is a Formula
        self.assertIsInstance(negate_form.terms[1], ds.Formula)  # Checks if the second term is a Formula

        self.assertTrue(negate_form.terms[0].terms[0].neg)  # Checks aNeg in; (aNeg and bPos) or (aPos or bNeg)
        self.assertTrue(negate_form.terms[1].terms[1].neg)  # Checks bNeg in; (aNeg and bPos) or (aPos or bNeg)
        self.assertFalse(negate_form.terms[1].terms[0].neg)  # Checks aPos in; (aNeg and bPos) or (aPos or bNeg)
        self.assertFalse(negate_form.terms[0].terms[1].neg)  # Checks bPos in; (aNeg and bPos) or (aPos or bNeg)

        self.assertEqual(negate_form.operator, ds.Operator.OR)  # Checks the outer operator
        self.assertEqual(negate_form.terms[0].operator, ds.Operator.AND)  # Checks the left inner operator
        self.assertEqual(negate_form.terms[1].operator, ds.Operator.OR)  # Checks the right inner operator


if __name__ == '__main__':
    unittest.main()
