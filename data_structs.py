from enum import Enum
import copy


class Operator(Enum):
    NOT = 1
    OR = 2
    AND = 3


class Literal:
    def __init__(self, atom, neg=False):
        self.atom = atom
        self.neg = neg

    def __eq__(self, other):
        if self.atom == other.atom:
            if self.neg == other.neg:
                return True
        return False

    def negate_literal(self):
        return Literal(self.atom, not self.neg)

    def is_unspecified_literal(self, literal):
        if self.atom == literal.atom:
            return False
        return True

class Formula:
    def __init__(self, terms, operator):
        self.terms = terms
        self.operator = operator

    def negate_operator(self):
        if self.operator == Operator.AND:
            return Operator.OR
        elif self.operator == Operator.OR:
            return Operator.AND
        else:
            return 0

    def negate_formula(self):
        left_term = self.terms[0].negate_literal()
        right_term = self.terms[1].negate_literal()
        operator = self.negate_operator()
        return Formula([left_term, right_term], operator)

    def left_is_subformula(self):
        if isinstance(self.terms[0], Formula):
            return True
        return False

    def right_is_subformula(self):
        if isinstance(self.terms[1], Formula):
            return True
        return False

    @staticmethod
    def is_unspecified_formula(formula, literal):
        unspecified = False
        if isinstance(formula, Literal):
            unspecified = formula.is_unspecified_literal(literal)
        else:
            if formula.left_is_subformula or formula.right_is_subformula():
                if formula.left_is_subformula():
                    unspecified = Formula.is_unspecified_formula(formula.terms[0], literal)
                else:
                    unspecified = formula.terms[0].is_unspecified_literal(literal)
                if formula.right_is_subformula():
                    unspecified = Formula.is_unspecified_formula(formula.terms[1], literal)
                else:
                    unspecified = formula.terms[1].is_unspecified_literal(literal)
            else:
                if formula.terms[1].is_unspecified_literal(literal) and formula.terms[0].is_unspecified_literal(literal):
                    unspecified = True
        return unspecified

    @staticmethod
    def build_or_formula(left_term, right_term):
        if left_term is None or right_term is None:
            return 0
        return Formula([left_term, right_term], Operator.OR)

    @staticmethod
    def build_and_formula(left_term, right_term):
        if left_term is None or right_term is None:
            return 0
        return Formula([left_term, right_term], Operator.AND)

    @staticmethod
    def build_not_formula(formula):
        if formula is None:
            return 0
        # neg_formula = Formula()
        neg_formula = copy.copy(formula)
        if isinstance(formula, Formula):
            if formula.left_is_subformula() or formula.right_is_subformula():
                if formula.left_is_subformula():
                    neg_formula.terms[0] = Formula.build_not_formula(formula.terms[0])
                else:
                    neg_formula.terms[0] = formula.terms[0].negate_literal()
                if formula.right_is_subformula():
                    neg_formula.terms[1] = Formula.build_not_formula(formula.terms[1])
                else:
                    neg_formula.terms[1] = formula.terms[1].negate_literal()
                neg_formula.operator = formula.negate_operator()
            elif not formula.right_is_subformula() and not formula.left_is_subformula():
                neg_formula = formula.negate_formula()
        elif isinstance(formula, Literal):
            neg_formula = formula.negate_literal()
        return neg_formula


class Rule:
    def __init__(self, conclusion, premise):
        self.conclusion = conclusion
        self.premise = premise


class Program:
    def __init__(self):
        self.rule_list = []

    # def merge_same_conclusion(self, new_rule):
    #     for rule in self.rule_list:
    #         if new_rule.conclusion == rule.conclusion:
    #             rule.premise = Formula.build_or_formula(rule.premise, new_rule.premise)

    def priority_to_constraint(self, new_rule):
        if not self.rule_list:
            self.rule_list.append(new_rule)
        else:
            merged = False
            for rule in self.rule_list[::-1]:
                # if self.check_for_equal_formulas(new_rule.conclusion, rule.conclusion):
                if new_rule.conclusion == rule.conclusion:
                    rule.premise = Formula.build_or_formula(rule.premise, new_rule.premise)
                    merged = True
                # elif self.check_for_equal_formulas(new_rule.conclusion, Formula.build_not_formula(rule.conclusion)):
                elif new_rule.conclusion == rule.conclusion.negate_literal():
                    new_rule.premise = Formula.build_and_formula(new_rule.premise, Formula.build_not_formula(rule.premise))
                    merged = False
                else:
                    continue
            if not merged:
                self.rule_list.insert(0, new_rule)

    @staticmethod
    def check_unspecified(premise, new_premise):
        rule_list = []
        if new_premise.left_is_subformula:
            rule_list = check_unspecified(premise, new_premise.terms[0])
        else:
            if Formula.is_unspecified_formula(premise, new_premise.terms[0]):
                rule_list.append(Formula.build_and_formula(new_premise.terms[0], premise))
                rule_list.append(Formula.build_and_formula(new_premise.terms[0].negate_literal(), premise))
        if new_premise.right_is_subformula:
            continue
        else:
            if Formula.is_unspecified_formula(premise, new_premise.terms[1]):
                rule_list.append(Formula.build_and_formula(new_premise.terms[1], premise))
                rule_list.append(Formula.build_and_formula(new_premise.terms[1].negate_literal(), premise))

    def constraint_to_full_tabular(self, new_rule):
        self.rule_list.insert(0, new_rule)
        for rule in self.rule_list:
            if new_rule.conclusion == rule.conclusion.negate_literal():
                if isinstance(new_rule.premise, Literal):
                    if rule.premise.is_unspecified_literal(new_rule.premise):




    # Recursive comparison of two formulas, Returns True if equal, False otherwise.
    # WIP If time; abstract order, apply negations, collapse hierarchy.
    # def check_for_equal_formulas(self, new_rule, existing_rule):
    #     success = False
    #     if isinstance(new_rule, Formula) and isinstance(existing_rule, Formula):
    #         if new_rule.operator == existing_rule.operator:
    #             if Formula.has_subformulas(new_rule.terms[0]) and Formula.has_subformulas(existing_rule.terms[0]):
    #                 if self.check_for_equal_formulas(new_rule.terms[0], existing_rule.terms[0]):
    #                     pass
    #             else:
    #                 success = self.check_for_equal_formulas(new_rule.terms[0], existing_rule.terms[0])
    #             if Formula.has_subformulas(new_rule.terms[1]) and Formula.has_subformulas(existing_rule.terms[1]):
    #                 if self.check_for_equal_formulas(new_rule.terms[1], existing_rule.terms[1]):
    #                     pass
    #             else:
    #                 success = existing_rule.terms[1] == new_rule.terms[1]
    #
    #     elif isinstance(new_rule, Literal) and isinstance(existing_rule, Literal):
    #         success = existing_rule == new_rule
    #     return success


def pb_to_icb(rule_list):
    temp_program = Program()
    for ri in rule_list[::-1]:  # from ri to r1
        temp_program.priority_to_constraint(ri)
    return temp_program.rule_list


def icb_to_ftcb(rule_list):
    temp_program = Program()
    for ri in rule_list[::-1]:  # from ri to r1
        temp_program.constraint_to_full_tabular(ri)
    return temp_program.rule_list
