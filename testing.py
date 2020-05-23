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

    # def test_negate_or_formula(self):
    #     aPos = ds.Literal("a", False)
    #     bNeg = ds.Literal("b", True)
    #     or_form_literal_terms = ds.Formula.build_or_formula(aPos, bNeg)  # a or -b
    #     negate_or = ds.Formula.build_not_formula(or_form_literal_terms)  # -a and b
    #
    #     self.assertEqual(negate_or.terms[0].atom, ds.Literal("a").atom)
    #     self.assertTrue(negate_or.terms[0].neg)
    #     self.assertEqual(negate_or.terms[1].atom, ds.Literal("b").atom)
    #     self.assertFalse(negate_or.terms[1].neg)
    #
    #     self.assertEqual(negate_or.operator, ds.Operator.AND)
    #
    # def test_negate_and_formula(self):
    #     aPos = ds.Literal("a", False)
    #     bNeg = ds.Literal("b", True)
    #     and_form_literal_terms = ds.Formula.build_and_formula(aPos, bNeg)   # a and -b
    #     negate_and = ds.Formula.build_not_formula(and_form_literal_terms)  # -a or b
    #
    #     self.assertEqual(negate_and.terms[0].atom, ds.Literal("a").atom)
    #     self.assertTrue(negate_and.terms[0].neg)
    #     self.assertEqual(negate_and.terms[1].atom, ds.Literal("b").atom)
    #     self.assertFalse(negate_and.terms[1].neg)
    #
    #     self.assertEqual(negate_and.operator, ds.Operator.OR)

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

    def test_equal_conclusion_merge(self):
        a = ds.Literal("a", False)
        b = ds.Literal("b", False)
        rule_a = ds.Rule(ds.Literal("p", False), a)  # p <- a.
        rule_b = ds.Rule(ds.Literal("p", False), b)  # p <- b.
        program = ds.Program()
        program.merge_rule(rule_a)  # Merged p <- a.
        program.merge_rule(rule_b)  # Merge p <- b.
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



    def test_multiple_conflicting_conc_to_icb(self):
        a = ds.Literal("a", False)
        b = ds.Literal("b", False)
        c = ds.Literal("c", False)
        rule_a = ds.Rule(ds.Literal("p", False), a)  # p <- a.
        rule_b = ds.Rule(ds.Literal("p", True), b)  # -p <- b.
        rule_c = ds.Rule(ds.Literal("p", False), c)  # p <- c.
        combined_abc = ds.pb_to_icb([rule_a, rule_b, rule_c])

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

    #
    # def test_alternating_conflict_conc(self):
    #     a = ds.Literal("a", False)
    #     b = ds.Literal("b", False)
    #     c = ds.Literal("c", False)
    #     d = ds.Literal("d", False)
    #     rule_a = ds.Rule(ds.Literal("p", False), a)  # p <- a.
    #     rule_b = ds.Rule(ds.Literal("p", True), b)  # -p <- b.
    #     rule_c = ds.Rule(ds.Literal("p", False), c)  # p <- c.
    #     rule_d = ds.Rule(ds.Literal("p", True), d)  # -p <- d.
    #
    #     combined_rule = ds.pb_to_icb([rule_a, rule_b, rule_c, rule_d])[0]
    #
    #     # Must become: -p <- ((d and -c) or b) and -a.
    #     self.assertEqual(combined_rule.conclusion.atom, ds.Literal("p").atom)
    #     self.assertIsInstance(combined_rule.conclusion, ds.Literal)
    #     self.assertTrue(combined_rule.conclusion.neg)  # Check if p is negative
    #
    #     self.assertEqual(combined_rule.premise.terms[0].terms[0].terms[0].atom, ds.Literal("d").atom)
    #     self.assertFalse(combined_rule.premise.terms[0].terms[0].terms[0].neg)  # Check if d is positive
    #
    #     self.assertEqual(combined_rule.premise.terms[0].terms[0].terms[1].atom, ds.Literal("c").atom)
    #     self.assertTrue(combined_rule.premise.terms[0].terms[0].terms[1].neg)  # Check if c is negative
    #
    #     self.assertEqual(combined_rule.premise.terms[0].terms[1].atom, ds.Literal("b").atom)
    #     self.assertFalse(combined_rule.premise.terms[0].terms[1].neg)  # Check if b is positive
    #
    #     self.assertEqual(combined_rule.premise.terms[1].atom, ds.Literal("a").atom)
    #     self.assertTrue(combined_rule.premise.terms[1].neg)  # Check if a is negative
    #
    #     self.assertEqual(combined_rule.premise.terms[0].terms[0].operator, ds.Operator.AND)  # Check inner AND
    #     self.assertEqual(combined_rule.premise.terms[0].operator, ds.Operator.OR)  # Check OR
    #     self.assertEqual(combined_rule.premise.operator, ds.Operator.AND)  # Check outer AND
    #
    # def test_different_conflicting_conc(self):
    #     a = ds.Literal("a", False)
    #     b = ds.Literal("b", False)
    #     c = ds.Literal("c", False)
    #     d = ds.Literal("d", False)
    #     rule_a = ds.Rule(ds.Literal("p", False), a)  # p <- a.
    #     rule_b = ds.Rule(ds.Literal("q", False), b)  # q <- b.
    #     rule_c = ds.Rule(ds.Literal("p", True), c)  # -p <- c.
    #     rule_d = ds.Rule(ds.Literal("q", True), d)  # -q <- d.
    #
    #     combined_rule = ds.pb_to_icb([rule_a, rule_b, rule_c, rule_d])
    #
    #     # Must become: -q <- d and -b.
    #     #         and: -p <- c and -a.
    #     self.assertEqual(combined_rule[0].conclusion.atom, ds.Literal("q").atom)
    #     self.assertTrue(combined_rule[0].conclusion.neg)  # Check if q is negative
    #
    #     self.assertEqual(combined_rule[0].premise.terms[0].atom, ds.Literal("d").atom)
    #     self.assertFalse(combined_rule[0].premise.terms[0].neg)  # Check if d is positive
    #
    #     self.assertEqual(combined_rule[0].premise.terms[1].atom, ds.Literal("b").atom)
    #     self.assertTrue(combined_rule[0].premise.terms[1].neg)  # Check if b is negative
    #
    #     self.assertEqual(combined_rule[0].premise.operator, ds.Operator.AND)
    #
    #     self.assertEqual(combined_rule[1].conclusion.atom, ds.Literal("p").atom)
    #     self.assertTrue(combined_rule[1].conclusion.neg)  # Check if p is negative
    #
    #     self.assertEqual(combined_rule[1].premise.terms[0].atom, ds.Literal("c").atom)
    #     self.assertFalse(combined_rule[1].premise.terms[0].neg)  # Check if c is positive
    #
    #     self.assertEqual(combined_rule[1].premise.terms[1].atom, ds.Literal("a").atom)
    #     self.assertTrue(combined_rule[1].premise.terms[1].neg)  # Check if a is negative
    #
    #     self.assertEqual(combined_rule[1].premise.operator, ds.Operator.AND)

    # A test for implementation of AND in the conclusion. (FOR LATER IMPLEMENTATION)
    # def test_pb_to_icb_and_conclusions(self):
    #     p = ds.Literal("p", False)
    #     q = ds.Literal("q", False)
    #     a = ds.Literal("c", False)
    #     b = ds.Literal("d", False)
    #     conc_pq = ds.Formula.build_and_formula(p, q)
    #     conc_qp = ds.Formula.build_and_formula(q, p)
    #     rule_a = ds.Rule(conc_pq, a)  # p and q <- a.
    #     rule_b = ds.Rule(conc_qp, b)  # q and p <- b.
    #
    #     combined_rule = ds.pb_to_icb([rule_a, rule_b])[0]
    #
    #     # Must become: q and p <- b or a.
    #     self.assertEqual(combined_rule.conclusion.terms[0].atom, ds.Literal("q").atom)
    #     self.assertFalse(combined_rule.conclusion.terms[0].neg)  # Check if q is negative
    #     self.assertEqual(combined_rule.conclusion.terms[1].atom, ds.Literal("p").atom)
    #     self.assertFalse(combined_rule.conclusion.terms[1].neg)  # Check if p is negative
    #
    #     self.assertEqual(combined_rule.premise.terms[0].atom, ds.Literal("b").atom)
    #     self.assertFalse(combined_rule.premise.terms[0].neg)  # Check if b is positive
    #
    #     self.assertEqual(combined_rule.premise.terms[1].atom, ds.Literal("a").atom)
    #     self.assertFalse(combined_rule.premise.terms[1].neg)  # Check if a is negative
    #
    #     self.assertEqual(combined_rule.conclusion.operator, ds.Operator.AND)  # Check conclusion AND
    #     self.assertEqual(combined_rule.premise.operator, ds.Operator.AND)  # Check premise AND

    # def
if __name__ == '__main__':
    unittest.main()
