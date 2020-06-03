import unittest
import main as mn
import data_structs as ds
import converters as cv
import qm
import qm_utils as qmu

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
        negate_aPos = aPos.negate_literal()
        self.assertTrue(negate_aPos.neg)

        aNeg = ds.Literal("a", True)
        negate_aNeg = aNeg.negate_literal()
        self.assertFalse(negate_aNeg.neg)

    def test_build_or_formula(self):
        aPos = ds.Literal("a", False)
        bNeg = ds.Literal("b", True)
        or_form_literal_terms = ds.Formula.build_or_formula(aPos, bNeg)

        self.assertEqual(or_form_literal_terms.terms, [aPos, bNeg])
        self.assertEqual(or_form_literal_terms.operator, ds.Operator.OR)

        self.assertIsInstance(or_form_literal_terms.terms[0], ds.Literal)
        self.assertIsInstance(or_form_literal_terms.terms[1], ds.Literal)

    def test_build_and_formula(self):
        aNeg = ds.Literal("a", True)
        bPos = ds.Literal("b", False)
        and_form_literal_terms = ds.Formula.build_and_formula(aNeg, bPos)

        self.assertEqual(and_form_literal_terms.terms, [aNeg, bPos])
        self.assertEqual(and_form_literal_terms.operator, ds.Operator.AND)

        self.assertIsInstance(and_form_literal_terms.terms[0], ds.Literal)
        self.assertIsInstance(and_form_literal_terms.terms[1], ds.Literal)

    def test_negate_or_formula(self):
        aPos = ds.Literal("a", False)
        bNeg = ds.Literal("b", True)
        or_form_literal_terms = ds.Formula.build_or_formula(aPos, bNeg)  # a or -b
        negate_or = ds.Formula.build_not_formula(or_form_literal_terms)  # -a and b

        self.assertEqual(negate_or.terms[0].atom, ds.Literal("a").atom)
        self.assertTrue(negate_or.terms[0].neg)
        self.assertEqual(negate_or.terms[1].atom, ds.Literal("b").atom)
        self.assertFalse(negate_or.terms[1].neg)

        self.assertEqual(negate_or.operator, ds.Operator.AND)

    def test_negate_and_formula(self):
        aPos = ds.Literal("a", False)
        bNeg = ds.Literal("b", True)
        and_form_literal_terms = ds.Formula.build_and_formula(aPos, bNeg)   # a and -b
        negate_and = ds.Formula.build_not_formula(and_form_literal_terms)  # -a or b

        self.assertEqual(negate_and.terms[0].atom, ds.Literal("a").atom)
        self.assertTrue(negate_and.terms[0].neg)
        self.assertEqual(negate_and.terms[1].atom, ds.Literal("b").atom)
        self.assertFalse(negate_and.terms[1].neg)

        self.assertEqual(negate_and.operator, ds.Operator.OR)

    def test_negate_lit_form(self):
        aPos = ds.Literal("a", False)
        bNeg = ds.Literal("b", True)
        cPos = ds.Literal("c", False)
        or_form_literal_terms = ds.Formula.build_or_formula(aPos, bNeg)  # a or -b
        and_formula_lit_form = ds.Formula.build_and_formula(cPos, or_form_literal_terms)  # c and (a or -b)
        negate_lit_form = ds.Formula.build_not_formula(and_formula_lit_form)  # -c or (-a and b)

        # Tests a formula with left term a literal and right term a formula.
        self.assertIsInstance(negate_lit_form.terms[1], ds.Formula)

        self.assertTrue(negate_lit_form.terms[0].neg)  # Checks -c in; -c or (-a and b)
        self.assertTrue(negate_lit_form.terms[1].terms[0].neg)  # Checks a in; -c or (-a and b)
        self.assertFalse(negate_lit_form.terms[1].terms[1].neg)  # Checks b in; -c or (-a and b)

        self.assertEqual(negate_lit_form.operator, ds.Operator.OR)  # Checks the outer operator
        self.assertEqual(negate_lit_form.terms[1].operator, ds.Operator.AND)  # Checks the inner operator

    def test_negate_form_lit(self):
        aNeg = ds.Literal("a", True)
        bPos = ds.Literal("b", False)
        cPos = ds.Literal("a", False)
        and_form_literal_terms = ds.Formula.build_and_formula(aNeg, bPos)
        and_formula_form_lit = ds.Formula.build_and_formula(and_form_literal_terms, cPos)  # (-a and b) and c
        negate_form_lit = ds.Formula.build_not_formula(and_formula_form_lit)  # (a or -b) or -c

        # Tests a formula with right term a literal and left term a formula.
        self.assertIsInstance(negate_form_lit.terms[0], ds.Formula)

        self.assertTrue(negate_form_lit.terms[1].neg)  # Checks -b in; (a or -b) or -c
        self.assertTrue(negate_form_lit.terms[0].terms[1].neg)  # Checks -b in; (a or -b) or -c
        self.assertFalse(negate_form_lit.terms[0].terms[0].neg)  # Checks a in; (a or -b) or -c

        self.assertEqual(negate_form_lit.operator, ds.Operator.OR)  # Checks for the outer operator
        self.assertEqual(negate_form_lit.terms[0].operator, ds.Operator.OR)  # Checks the inner operator

    def test_negate_form_form(self):
        aPos = ds.Literal("a", False)
        bNeg = ds.Literal("b", True)
        cNeg = ds.Literal("a", True)
        dPos = ds.Literal("d", False)
        or_form_literal = ds.Formula.build_or_formula(aPos, bNeg)
        and_form_literal = ds.Formula.build_and_formula(cNeg, dPos)
        and_formula_form = ds.Formula.build_and_formula(or_form_literal, and_form_literal)  # (a or -b) and (-c and d)
        negate_form = ds.Formula.build_not_formula(and_formula_form)  # (-a and b) or (c or -d)

        # Tests a formula with both terms a formula.
        self.assertIsInstance(negate_form.terms[0], ds.Formula)  # Checks if the first term is a Formula
        self.assertIsInstance(negate_form.terms[1], ds.Formula)  # Checks if the second term is a Formula

        self.assertTrue(negate_form.terms[0].terms[0].neg)  # Checks -a in; (-a and b) or (c or -d)
        self.assertFalse(negate_form.terms[0].terms[1].neg)  # Checks b in; (-a and b) or (c or -d)
        self.assertFalse(negate_form.terms[1].terms[0].neg)  # Checks c in; (-a and b) or (c or -d)
        self.assertTrue(negate_form.terms[1].terms[1].neg)  # Checks -d in; (-a and b) or (c or -d)

        self.assertEqual(negate_form.operator, ds.Operator.OR)  # Checks the outer operator
        self.assertEqual(negate_form.terms[0].operator, ds.Operator.AND)  # Checks the left inner operator
        self.assertEqual(negate_form.terms[1].operator, ds.Operator.OR)  # Checks the right inner operator

    def test_equal_conclusion_pb_to_icb(self):
        a = ds.Literal("a", False)
        b = ds.Literal("b", False)
        rule_a = ds.Rule(ds.Literal("p", False), a)  # p <- a.
        rule_b = ds.Rule(ds.Literal("p", False), b)  # p <- b.
        program = cv.Program()
        program.priority_to_constraint(rule_a)  # Merged p <- a.
        program.priority_to_constraint(rule_b)  # Merge p <- b.
        new_rule = program.rule_list[0]
        # Should be p <- a or b.
        self.assertEqual(new_rule.conclusion.atom, ds.Literal("p").atom)
        self.assertFalse(new_rule.conclusion.neg)

        self.assertEqual(new_rule.premise.terms[0].atom, ds.Literal("a").atom)
        self.assertFalse(new_rule.premise.terms[0].neg)

        self.assertEqual(new_rule.premise.terms[1].atom, ds.Literal("b").atom)
        self.assertFalse(new_rule.premise.terms[1].neg)

        self.assertEqual(new_rule.premise.operator, ds.Operator.OR)

    def test_pb_to_icb_same_conc(self):
        a = ds.Literal("a", False)
        b = ds.Literal("b", False)
        rule_a = ds.Rule(ds.Literal("p", False), a)
        rule_b = ds.Rule(ds.Literal("p", False), b)
        combined_rule_list = cv.pb_to_icb([rule_a, rule_b])

        self.assertEqual(combined_rule_list[0].premise.terms[0].atom, "b")
        self.assertEqual(combined_rule_list[0].premise.operator, ds.Operator.OR)
        self.assertEqual(combined_rule_list[0].premise.terms[1].atom, "a")

    def test_pb_to_icb_conflict_conc(self):
        a = ds.Literal("a", False)
        b = ds.Literal("b", False)
        rule_a = ds.Rule(ds.Literal("p", False), a)  # p <- a.
        rule_b = ds.Rule(ds.Literal("p", True), b)  # -p <- b.
        combined_rule_list = cv.pb_to_icb([rule_a, rule_b])

        # Must become:  p <- a and -b.  (combined_rule_list[0])
        #         and: -p <- b.         (combined_rule_list[1])
        self.assertEqual(combined_rule_list[1].conclusion.atom, "p")
        self.assertTrue(combined_rule_list[1].conclusion.neg)

        self.assertEqual(combined_rule_list[1].premise.atom, "b")
        self.assertFalse(combined_rule_list[1].premise.neg)

        self.assertEqual(combined_rule_list[0].premise.terms[0].atom, "a")
        self.assertFalse(combined_rule_list[0].premise.terms[0].neg)

        self.assertEqual(combined_rule_list[0].premise.terms[1].atom, "b")
        self.assertTrue(combined_rule_list[0].premise.terms[1].neg)

        self.assertEqual(combined_rule_list[0].premise.operator, ds.Operator.AND)

    def test_alternating_conflicting_conc_to_icb(self):
        a = ds.Literal("a", False)
        b = ds.Literal("b", False)
        c = ds.Literal("c", False)
        rule_a = ds.Rule(ds.Literal("p", False), a)  # p <- a.
        rule_b = ds.Rule(ds.Literal("p", True), b)  # -p <- b.
        rule_c = ds.Rule(ds.Literal("p", False), c)  # p <- c.
        combined_abc = cv.pb_to_icb([rule_a, rule_b, rule_c])

        # Must become: p <- a and -b or c.      (combined_abs[0])
        #            :-p <- b and -c.           (combined_abs[1])
        #            : p <- c or a.             (combined_abs[2])

        self.assertEqual(combined_abc[2].conclusion.atom, ds.Literal("p").atom)
        self.assertFalse(combined_abc[2].conclusion.neg)  # Check if p is positive in; p <- c or a.

        self.assertEqual(combined_abc[2].premise.terms[0].atom, ds.Literal("c").atom)
        self.assertFalse(combined_abc[2].premise.terms[0].neg)  # Check if c is positive in; p <- c or a.

        self.assertEqual(combined_abc[2].premise.terms[1].atom, ds.Literal("a").atom)
        self.assertFalse(combined_abc[2].premise.terms[0].neg)  # Check if a is positive in; p <- c or a.

        self.assertEqual(combined_abc[2].premise.operator, ds.Operator.OR)  # Check OR operator in premise

        self.assertEqual(combined_abc[1].conclusion.atom, ds.Literal("p").atom)
        self.assertTrue(combined_abc[1].conclusion.neg)  # Check if p is negative in; -p <- b and -c.

        self.assertEqual(combined_abc[1].premise.terms[0].atom, ds.Literal("b").atom)
        self.assertFalse(combined_abc[1].premise.terms[0].neg)  # Check if b is positive in; -p <- b and -c.

        self.assertEqual(combined_abc[1].premise.terms[1].atom, ds.Literal("c").atom)
        self.assertTrue(combined_abc[1].premise.terms[1].neg)  # Check if c is negative in; -p <- b and -c.

        self.assertEqual(combined_abc[1].premise.operator, ds.Operator.AND)  # Check AND operator

        self.assertEqual(combined_abc[0].premise.terms[0].atom, ds.Literal("a").atom)
        self.assertFalse(combined_abc[0].premise.terms[0].neg)  # Check if a is positive in; p <- a and (-b or c).

        self.assertEqual(combined_abc[0].premise.operator, ds.Operator.AND)  # Check outer AND operator

        self.assertEqual(combined_abc[0].premise.terms[1].terms[0].atom, ds.Literal("b").atom)
        self.assertTrue(combined_abc[0].premise.terms[1].terms[0].neg)  # Check if b is neg in; p <- a and (-b or c).

        self.assertEqual(combined_abc[0].premise.terms[1].terms[1].atom, ds.Literal("c").atom)
        self.assertFalse(combined_abc[0].premise.terms[1].terms[1].neg)  # Check if c is pos in; p <- a and (-b or c).

        self.assertEqual(combined_abc[0].premise.terms[1].operator, ds.Operator.OR)  # Check inner OR operator

    def test_mutliple_conflict_conc(self):
        a = ds.Literal("a", False)
        b = ds.Literal("b", False)
        c = ds.Literal("c", False)
        d = ds.Literal("d", False)
        rule_a = ds.Rule(ds.Literal("p", False), ds.Formula.build_or_formula(a, c))  # p <- a or c.
        rule_b = ds.Rule(ds.Literal("p", True), ds.Formula.build_or_formula(b, d))  # -p <- b or d.
        combined_rule = cv.pb_to_icb([rule_a, rule_b])

        # Must become:  p <- (a or c) and (-b and -d).
        #            : -p <- b or d.
        self.assertEqual(combined_rule[1].conclusion.atom, ds.Literal("p").atom)
        self.assertTrue(combined_rule[1].conclusion.neg)  # Check if p is negative in; -p <- b or d.

        self.assertEqual(combined_rule[1].premise.terms[0].atom, ds.Literal("b").atom)
        self.assertFalse(combined_rule[1].premise.terms[0].neg)  # Check if b is positive in; -p <- b or d.

        self.assertEqual(combined_rule[1].premise.terms[1].atom, ds.Literal("d").atom)
        self.assertFalse(combined_rule[1].premise.terms[1].neg)  # Check if d is positive in; -p <- b or d.

        self.assertEqual(combined_rule[1].premise.operator, ds.Operator.OR)  # Check OR in; -p <- b or d.

        self.assertEqual(combined_rule[0].conclusion.atom, ds.Literal("p").atom)
        self.assertFalse(combined_rule[0].conclusion.neg)  # Check if p is positive in; p <- (a or c) and (-b and -d).

        self.assertEqual(combined_rule[0].premise.terms[0].terms[0].atom, ds.Literal("a").atom)
        self.assertFalse(
            combined_rule[0].premise.terms[0].terms[0].neg)  # Check if a is positive in; p <- (a or c) and (-b and -d).

        self.assertEqual(combined_rule[0].premise.terms[0].terms[1].atom, ds.Literal("c").atom)
        self.assertFalse(
            combined_rule[0].premise.terms[0].terms[1].neg)  # Check if c is positive in; p <- (a or c) and (-b and -d).

        self.assertEqual(combined_rule[0].premise.terms[0].operator,
                         ds.Operator.OR)  # Check OR in; p <- (a or c) and (-b and -d).

        self.assertEqual(combined_rule[0].premise.terms[1].terms[0].atom, ds.Literal("b").atom)
        self.assertTrue(
            combined_rule[0].premise.terms[1].terms[0].neg)  # Check if b is negative in; p <- (a or c) and (-b and -d).

        self.assertEqual(combined_rule[0].premise.terms[1].terms[1].atom, ds.Literal("d").atom)
        self.assertTrue(
            combined_rule[0].premise.terms[1].terms[1].neg)  # Check if d is negative in; p <- (a or c) and (-b and -d).

        self.assertEqual(combined_rule[0].premise.terms[1].operator,
                         ds.Operator.AND)  # Check innter AND in; p <- (a or c) and (-b and -d).

        self.assertEqual(combined_rule[0].premise.operator, ds.Operator.AND)  # Check outer AND

    def test_is_unspecified_literal(self):
        aP = ds.Literal("a", False)
        aN = ds.Literal("a", True)
        b = ds.Literal("b", False)
        self.assertTrue(aP.is_unspecified_literal(b))
        self.assertFalse(aN.is_unspecified_literal(aP))

    def test_is_unspecified_formula(self):
        aP = ds.Literal("a", False)
        aN = ds.Literal("a", True)
        b = ds.Literal("b", False)
        c = ds.Literal("c", False)
        d = ds.Literal("d", False)

        aP_and_c = ds.Formula.build_and_formula(aP, c)
        aN_and_c = ds.Formula.build_and_formula(aN, c)
        aP_and_c_and_b = ds.Formula.build_and_formula(aP_and_c, b)
        b_and_aP_and_c = ds.Formula.build_and_formula(b, aP_and_c)
        aP_and_c_and_An_and_c = ds.Formula.build_and_formula(aP_and_c, aN_and_c)

        self.assertFalse(aP_and_c.is_unspecified_formula(aN))
        self.assertFalse(aP_and_c.is_unspecified_formula(c))

        self.assertFalse(aN_and_c.is_unspecified_formula(aP))
        self.assertFalse(aN_and_c.is_unspecified_formula(c))

        self.assertFalse(aP_and_c_and_b.is_unspecified_formula(aN))
        self.assertFalse(aP_and_c_and_b.is_unspecified_formula(c))
        self.assertFalse(aP_and_c_and_b.is_unspecified_formula(b))

        self.assertFalse(b_and_aP_and_c.is_unspecified_formula(aN))
        self.assertFalse(b_and_aP_and_c.is_unspecified_formula(b))
        self.assertFalse(b_and_aP_and_c.is_unspecified_formula(c))

        self.assertFalse(aP_and_c_and_An_and_c.is_unspecified_formula(c))
        self.assertFalse(aP_and_c_and_An_and_c.is_unspecified_formula(aN))

        self.assertTrue(aP_and_c.is_unspecified_formula(b))
        self.assertTrue(aN_and_c.is_unspecified_formula(b))
        self.assertTrue(aP_and_c_and_b.is_unspecified_formula(d))
        self.assertTrue(aP_and_c_and_An_and_c.is_unspecified_formula(b))

    def test_get_unspecified_literals(self):
        aP = ds.Literal("a", False)
        aN = ds.Literal("a", True)
        b = ds.Literal("b", False)
        c = ds.Literal("c", False)
        d = ds.Literal("d", False)
        e = ds.Literal("e", False)
        f = ds.Literal("f", False)

        aP_and_c = ds.Formula.build_and_formula(aP, c)
        aN_and_c = ds.Formula.build_and_formula(aN, c)
        d_and_e = ds.Formula.build_and_formula(d, e)
        b_and_aP_and_c = ds.Formula.build_and_formula(b, aP_and_c)
        aP_and_c_and_An_and_c = ds.Formula.build_and_formula(aP_and_c, aN_and_c)
        d_and_e_and_f = ds.Formula.build_and_formula(d_and_e, f)

        self.assertEqual(ds.Formula.get_unspecified_literals(aP, aN), [])
        self.assertEqual(ds.Formula.get_unspecified_literals(aP, aN_and_c), [c])
        self.assertEqual(ds.Formula.get_unspecified_literals(aP, b_and_aP_and_c), [b, c])
        self.assertEqual(ds.Formula.get_unspecified_literals(aP, aP_and_c_and_An_and_c), [c])

        self.assertEqual(ds.Formula.get_unspecified_literals(aP_and_c, aN), [])
        self.assertEqual(ds.Formula.get_unspecified_literals(aP_and_c, aN_and_c), [])
        self.assertEqual(ds.Formula.get_unspecified_literals(aP_and_c, b_and_aP_and_c), [b])
        self.assertEqual(ds.Formula.get_unspecified_literals(aP_and_c, aP_and_c_and_An_and_c), [])

        self.assertEqual(ds.Formula.get_unspecified_literals(b_and_aP_and_c, aN), [])
        self.assertEqual(ds.Formula.get_unspecified_literals(b_and_aP_and_c, aN_and_c), [])
        self.assertEqual(ds.Formula.get_unspecified_literals(b_and_aP_and_c, b_and_aP_and_c), [])
        self.assertEqual(ds.Formula.get_unspecified_literals(b_and_aP_and_c, aP_and_c_and_An_and_c), [])

        self.assertEqual(ds.Formula.get_unspecified_literals(aP_and_c_and_An_and_c, aN), [])
        self.assertEqual(ds.Formula.get_unspecified_literals(aP_and_c_and_An_and_c, aN_and_c), [])
        self.assertEqual(ds.Formula.get_unspecified_literals(aP_and_c_and_An_and_c, b_and_aP_and_c),
                         [ds.Literal("b", False)])
        self.assertEqual(ds.Formula.get_unspecified_literals(aP_and_c_and_An_and_c, aP_and_c_and_An_and_c), [])

        self.assertEqual(ds.Formula.get_unspecified_literals(aP, d), [ds.Literal("d", False)])
        self.assertEqual(ds.Formula.get_unspecified_literals(aP_and_c, d), [ds.Literal("d", False)])
        self.assertEqual(ds.Formula.get_unspecified_literals(b_and_aP_and_c, d), [ds.Literal("d", False)])
        self.assertEqual(ds.Formula.get_unspecified_literals(aP_and_c_and_An_and_c, d), [ds.Literal("d", False)])

        self.assertEqual(ds.Formula.get_unspecified_literals(aP, d_and_e), [ds.Literal("d", False),
                                                                            ds.Literal("e", False)])
        self.assertEqual(ds.Formula.get_unspecified_literals(aP_and_c, d_and_e), [ds.Literal("d", False),
                                                                                  ds.Literal("e", False)])
        self.assertEqual(ds.Formula.get_unspecified_literals(b_and_aP_and_c, d_and_e), [ds.Literal("d", False),
                                                                                        ds.Literal("e", False)])
        self.assertEqual(ds.Formula.get_unspecified_literals(aP_and_c_and_An_and_c, d_and_e), [ds.Literal("d", False),
                                                                                               ds.Literal("e", False)])

        self.assertEqual(ds.Formula.get_unspecified_literals(aP, d_and_e_and_f), [ds.Literal("d", False),
                                                                                  ds.Literal("e", False),
                                                                                  ds.Literal("f", False)])
        self.assertEqual(ds.Formula.get_unspecified_literals(aP_and_c, d_and_e_and_f), [ds.Literal("d", False),
                                                                                        ds.Literal("e", False),
                                                                                        ds.Literal("f", False)])
        self.assertEqual(ds.Formula.get_unspecified_literals(b_and_aP_and_c, d_and_e_and_f), [ds.Literal("d", False),
                                                                                              ds.Literal("e", False),
                                                                                              ds.Literal("f", False)])
        self.assertEqual(ds.Formula.get_unspecified_literals(aP_and_c_and_An_and_c, d_and_e_and_f),
                         [ds.Literal("d", False),
                          ds.Literal("e", False),
                          ds.Literal("f", False)])

    def test_intermediate_to_full_tabular(self):
        a_and_negb = ds.Formula.build_and_formula(ds.Literal("a"), ds.Literal("b", True))
        b = ds.Literal("b")
        rule_a = ds.Rule(ds.Literal("p"), a_and_negb)  # p <- a and -b.
        rule_b = ds.Rule(ds.Literal("p", True), b)  # -p <- b.
        new_rule_base = cv.icb_to_ftcb([rule_a, rule_b])

        # Must become: p <- a and -b.
        #            : -p <- a and b.
        #            : -p <- -a and b.

        # Check p <- a and -b
        self.assertEqual(new_rule_base[0].conclusion.atom, ds.Literal("p").atom)
        self.assertFalse(new_rule_base[0].conclusion.neg)  # Check if p positive in; p <- a and -b.

        self.assertEqual(new_rule_base[0].premise.terms[0].atom, ds.Literal("a").atom)
        self.assertFalse(new_rule_base[0].premise.terms[0].neg)  # Check if a positive in; p <- a and -b.

        self.assertEqual(new_rule_base[0].premise.terms[1].atom, ds.Literal("b").atom)
        self.assertTrue(new_rule_base[0].premise.terms[1].neg)  # Check if b negative in; p <- a and -b.

        self.assertEqual(new_rule_base[0].premise.operator, ds.Operator.AND)  # Check AND in; p <- a and -b.

        # Check -p <- a and b.
        self.assertEqual(new_rule_base[1].conclusion.atom, ds.Literal("p").atom)
        self.assertTrue(new_rule_base[1].conclusion.neg)  # Check if p negative in; -p <- a and b.

        self.assertEqual(new_rule_base[1].premise.terms[0].atom, ds.Literal("a").atom)
        self.assertFalse(new_rule_base[1].premise.terms[0].neg)  # Check if a positive in;  -p <- a and b.

        self.assertEqual(new_rule_base[1].premise.terms[1].atom, ds.Literal("b").atom)
        self.assertFalse(new_rule_base[1].premise.terms[1].neg)  # Check if b positive in;  -p <- a and b.

        self.assertEqual(new_rule_base[1].premise.operator, ds.Operator.AND)  # Check AND in;  -p <- a and b.

        # Check -p <- -a and b.
        self.assertEqual(new_rule_base[2].conclusion.atom, ds.Literal("p").atom)
        self.assertTrue(new_rule_base[2].conclusion.neg)  # Check if p negative in; -p <- -a and b.

        self.assertEqual(new_rule_base[2].premise.terms[0].atom, ds.Literal("a").atom)
        self.assertTrue(new_rule_base[2].premise.terms[0].neg)  # Check if a negative in; -p <- -a and b.

        self.assertEqual(new_rule_base[2].premise.terms[1].atom, ds.Literal("b").atom)
        self.assertFalse(new_rule_base[2].premise.terms[1].neg)  # Check if b positive in; p <- a and -b.

        self.assertEqual(new_rule_base[2].premise.operator, ds.Operator.AND)  # Check AND in; -p <- -a and b.

    def test_sort_and_alphabetical(self):
        d_and_e = ds.Formula.build_and_formula(ds.Literal("d"), ds.Literal("e"))
        a_and_d, e1 = ds.Formula.sort_and_alphabetical(d_and_e, ds.Literal("a"))

        self.assertEqual(a_and_d.terms[0], ds.Literal("a"))
        self.assertEqual(a_and_d.terms[1].atom, ds.Literal("d").atom)
        self.assertEqual(e1, ds.Literal("e"))

        # Test with soring needed.
        a_and_d_and_e1 = ds.Formula.build_and_formula(a_and_d, e1)
        a_and_b_and_d, e2 = ds.Formula.sort_and_alphabetical(a_and_d_and_e1, ds.Literal("b"))
        self.assertEqual(a_and_b_and_d.terms[0].terms[0], ds.Literal("a"))
        self.assertEqual(a_and_b_and_d.terms[0].terms[1], ds.Literal("b"))
        self.assertEqual(a_and_b_and_d.terms[1], ds.Literal("d"))
        self.assertEqual(e2, ds.Literal("e"))

        # Test when no sorting is needed.
        a_and_b_and_d, f = ds.Formula.sort_and_alphabetical(a_and_b_and_d, ds.Literal("f"))
        self.assertEqual(a_and_b_and_d.terms[0].terms[0], ds.Literal("a"))
        self.assertEqual(a_and_b_and_d.terms[0].terms[1], ds.Literal("b"))
        self.assertEqual(a_and_b_and_d.terms[1], ds.Literal("d"))
        self.assertEqual(f, ds.Literal("f"))

    def test_sort_build_and(self):
        a_and_c = ds.Formula.build_and_formula(ds.Literal("a"), ds.Literal("c"))
        a_and_b_and_c = ds.Formula.build_sort_and_formula(a_and_c, ds.Literal("b"))
        self.assertEqual(a_and_b_and_c.terms[0].terms[0], ds.Literal("a"))
        self.assertEqual(a_and_b_and_c.terms[0].terms[1], ds.Literal("b"))
        self.assertEqual(a_and_b_and_c.terms[1], ds.Literal("c"))

    def test_intermediate_to_full_tabular_alphabetical(self):
        a_and_negb = ds.Formula.build_and_formula(ds.Literal("a"), ds.Literal("b", True))
        b_and_c = ds.Formula.build_and_formula(ds.Literal("b"), ds.Literal("c"))

        rule_a = ds.Rule(ds.Literal("p"), a_and_negb)  # p <- a and -b.
        rule_b = ds.Rule(ds.Literal("p", True), b_and_c)  # -p <- b and c.
        new_rule_base = cv.icb_to_ftcb([rule_a, rule_b])

        # Must become: p <- a and -b and c.
        #            : p <- a and -b and -c.
        #            : -p <- a and b and c.
        #            : -p <- -a and b and c.

        # Check p <- a and -b and c.
        self.assertEqual(new_rule_base[0].conclusion, ds.Literal("p"))  # Check p in; p <- a and -b and c.
        self.assertEqual(new_rule_base[0].premise.terms[0].terms[0], ds.Literal("a"))  # Check a in; p <- a and -b and c.
        self.assertEqual(new_rule_base[0].premise.terms[0].terms[1], ds.Literal("b", True))  # Check b in; p <- a and -b and c.
        self.assertEqual(new_rule_base[0].premise.terms[1], ds.Literal("c")) # Check c in; p <- a and -b and c.

        self.assertEqual(new_rule_base[0].premise.terms[0].operator, ds.Operator.AND)  # Check first AND in; p <- a and -b and c.
        self.assertEqual(new_rule_base[0].premise.operator, ds.Operator.AND)  # Check second AND in; p <- a and -b and c.

        # Check p <- a and -b and -c.
        self.assertEqual(new_rule_base[1].conclusion, ds.Literal("p"))  # Check p in; p <- a and -b and -c.
        self.assertEqual(new_rule_base[1].premise.terms[0].terms[0], ds.Literal("a")) # Check a in; p <- a and -b and -c.
        self.assertEqual(new_rule_base[1].premise.terms[0].terms[1], ds.Literal("b", True))  # Check b in; p <- a and -b and -c.
        self.assertEqual(new_rule_base[1].premise.terms[1], ds.Literal("c", True))  # Check c in; p <- a and -b and -c.
        self.assertEqual(new_rule_base[1].premise.terms[0].operator, ds.Operator.AND)  # Check first AND in; p <- -a and -b
        # and -c.
        self.assertEqual(new_rule_base[1].premise.operator, ds.Operator.AND)  # Check second AND in; p <- a
        # and -b and -c.

        # Check -p < a and b and c.
        self.assertEqual(new_rule_base[2].conclusion, ds.Literal("p", True))  # Check p in; -p <- a and b and c.
        self.assertEqual(new_rule_base[2].premise.terms[0].terms[0], ds.Literal("a"))  # Check a in; -p <- a and b and c.
        self.assertEqual(new_rule_base[2].premise.terms[0].terms[1], ds.Literal("b"))  # Check b in;  -p <- a and b and c.
        self.assertEqual(new_rule_base[2].premise.terms[1], ds.Literal("c"))  # Check c in;  -p <- a and b and c.

        self.assertEqual(new_rule_base[2].premise.terms[0].operator, ds.Operator.AND)  # Check first AND in; -p <- a
        # and b and c.
        self.assertEqual(new_rule_base[2].premise.operator, ds.Operator.AND)  # Check second AND in;  -p <-
        # a and b and c.

        # Check -p <- -a and b and c.
        self.assertEqual(new_rule_base[3].conclusion, ds.Literal("p", True))  # Check p in; -p <- -a and b and c.
        self.assertEqual(new_rule_base[3].premise.terms[0].terms[0], ds.Literal("a", True))  # Check a in; -p <- -a
        # and b and c.
        self.assertEqual(new_rule_base[3].premise.terms[0].terms[1], ds.Literal("b"))  # Check b in;  -p <- -a and b
        # and c.
        self.assertEqual(new_rule_base[3].premise.terms[1], ds.Literal("c")) # Check c in;  -p <- -a and b and c.

        self.assertEqual(new_rule_base[3].premise.terms[0].operator, ds.Operator.AND)  # Check first AND in;  -p <-
        # -a and b and c.
        self.assertEqual(new_rule_base[3].premise.operator, ds.Operator.AND)  # Check second AND in;  -p <-
        # -a and b and c.

    def test_get_minterm_literals(self):
        a = ds.Literal("a")
        b = ds.Literal("b")
        c = ds.Literal("c")
        a_and_b = ds.Formula.build_and_formula(a, b)
        na_and_b = ds.Formula.build_and_formula(a.negate_literal(), b)
        a_and_nb = ds.Formula.build_and_formula(a, b.negate_literal())
        na_and_b_and_c = ds.Formula.build_and_formula(na_and_b, c)
        a_and_nb_and_nc = ds.Formula.build_and_formula(a_and_nb, c.negate_literal())

        # Must become: a and -b = '10'
        #            : a and b = '11'
        #            : -a and b = '01'
        #            : -a and b and c = '011'
        #            : a and -b and -c = '100'

        self.assertEqual(qmu.get_minterm_literals(a), ('1', 'a'))
        self.assertEqual(qmu.get_minterm_literals(a.negate_literal()), ('0', 'a'))
        self.assertEqual(qmu.get_minterm_literals(a_and_b), ('11', 'ab'))
        self.assertEqual(qmu.get_minterm_literals(a_and_nb), ('10', 'ab'))
        self.assertEqual(qmu.get_minterm_literals(na_and_b), ('01', 'ab'))
        self.assertEqual(qmu.get_minterm_literals(na_and_b_and_c), ('011', 'abc'))
        self.assertEqual(qmu.get_minterm_literals(a_and_nb_and_nc), ('100', 'abc'))

    def test_transform_rules_to_QM(self):
        a_and_negb = ds.Formula.build_and_formula(ds.Literal("a"), ds.Literal("b", True))

        b_and_c = ds.Formula.build_and_formula(ds.Literal("b"), ds.Literal("c"))
        a_and_b_and_c = ds.Formula.build_and_formula(ds.Literal("a"), b_and_c)
        na_and_b_and_c = ds.Formula.build_and_formula(ds.Literal("a", True), b_and_c)

        rule_a = ds.Rule(ds.Literal("p"), a_and_negb)  # p <- a and -b.
        rule_b = ds.Rule(ds.Literal("p", True), a_and_b_and_c)  # -p <- a and b and c.
        rule_c = ds.Rule(ds.Literal("p", True), na_and_b_and_c)  # -p <- -a and b and c.

        QM_dict = qmu.qm_dict([rule_a, rule_b, rule_c])

        self.assertEqual(QM_dict[ds.Literal("p", False)], ['ab', 2])
        self.assertEqual(QM_dict[ds.Literal("p", True)], ['abc', 7, 3])

    def test_qm(self):
        qm_dict = {ds.Literal("p"): ['abc', 7, 3]}
        value = qm_dict[ds.Literal("p")]
        literals, minterm = value[1], value[1:]
        quineMc = qm.QuineMcCluskey()
        simplified = quineMc.simplify(minterm)
        self.assertEqual(simplified, {'-11'})

    def test_apply_qm(self):
        a_and_nb = ds.Formula.build_and_formula(ds.Literal("a"), ds.Literal("b", True))

        b_and_c = ds.Formula.build_and_formula(ds.Literal("b"), ds.Literal("c"))
        a_and_b_and_c = ds.Formula.build_and_formula(ds.Literal("a"), b_and_c)
        na_and_b_and_c = ds.Formula.build_and_formula(ds.Literal("a", True), b_and_c)

        rule_a = ds.Rule(ds.Literal("p"), a_and_nb)  # p <- a and -b.
        rule_b = ds.Rule(ds.Literal("p", True), a_and_b_and_c)  # -p <- a and b and c.
        rule_c = ds.Rule(ds.Literal("p", True), na_and_b_and_c)  # -p <- -a and b and c.

        QM_dict = qmu.qm_dict([rule_a, rule_b, rule_c])
        rule_list = qmu.apply_qm(QM_dict)

        # Must become: p <- a and -b.
        #             -p <- b and c.

        self.assertEqual(rule_list[0].premise.terms[0], ds.Literal("a"))
        self.assertEqual(rule_list[0].premise.terms[1], ds.Literal("b", True))
        self.assertEqual(rule_list[0].conclusion, ds.Literal("p"))
        self.assertEqual(rule_list[0].premise.operator, ds.Operator.AND)

        self.assertEqual(rule_list[1].premise.terms[0], ds.Literal("b"))
        self.assertEqual(rule_list[1].premise.terms[1], ds.Literal("c"))
        self.assertEqual(rule_list[1].conclusion, ds.Literal("p", True))
        self.assertEqual(rule_list[1].premise.operator, ds.Operator.AND)

if __name__ == '__main__':
    unittest.main()
