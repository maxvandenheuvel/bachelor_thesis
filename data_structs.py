from enum import Enum
import copy


class Operator(Enum):
    NOT = 1
    OR = 2
    AND = 3


class Literal:
    def __init__(self, atom, neg):
        self.atom = atom
        self.neg = neg

    @staticmethod
    def build_not_literal(term):
        if term is None:
            return 0
        neg_term = term
        if neg_term.neg:
            neg_term.neg = False
        else:
            neg_term.neg = True
        return neg_term


class Formula:
    def __init__(self, terms, operator, formula_bool):
        self.terms = terms
        self.operator = operator
        self.formula_bool = formula_bool  # This boolean keeps track whether the terms are formulas themselves.
    
    @staticmethod
    def build_or_formula(terms):
        if terms is None:
            return 0
        formula_bool = [isinstance(terms[0], Formula), isinstance(terms[1], Formula)]
        return Formula(terms, Operator.OR, formula_bool)
    
    @staticmethod
    def build_and_formula(terms):
        if terms is None:
            return 0
        formula_bool = [isinstance(terms[0], Formula), isinstance(terms[1], Formula)]
        return Formula(terms, Operator.AND, formula_bool)
    
    @staticmethod
    def build_not_formula(term):
        if term is None:
            return 0
        neg_term = copy.copy(term)
        if isinstance(term, Formula):
            form_bool = neg_term.formula_bool
            if form_bool[0]:
                neg_term.terms[0] = Formula.build_not_formula(neg_term.terms[0])
            else:
                neg_term.terms[0] = Literal.build_not_literal(neg_term.terms[0])
            if form_bool[1]:
                neg_term.terms[1] = Formula.build_not_formula(neg_term.terms[1])
            else:
                neg_term.terms[1] = Literal.build_not_literal(neg_term.terms[1])
            if neg_term.operator == Operator.AND:
                neg_term.operator = Operator.OR
            else:
                neg_term.operator = Operator.AND
        elif isinstance(term, Literal):
            neg_term = Literal.build_not_literal(term)
        return neg_term


class Rule:
    def __init__(self, conclusion, premise):
        self.conclusion = conclusion
        self.premise = premise

    
class Program:
    def __init__(self):
        self.rule_list = []

    def merge_rule(self, new_rule):
        if not self.rule_list:
            self.rule_list.append(new_rule)
        else:
            merged = False
            for rule in self.rule_list:
                if self.check_for_equal_formulas(new_rule.conclusion, rule.conclusion):
                    rule.premise = Formula.build_or_formula([rule.premise, new_rule.premise])
                    merged = True
                elif self.check_for_equal_formulas(new_rule.conclusion, Formula.build_not_formula(rule.conclusion)):
                    rule.premise = Formula.build_and_formula([rule.premise, Formula.build_not_formula(new_rule.premise)])
                    merged = True
                else:
                    continue
            if not merged:
                self.rule_list.append(new_rule)

    # Recursive comparison of two formulas, Returns True if equal, False otherwise.
    def check_for_equal_formulas(self, new_rule, existing_rule):
        success = False
        if isinstance(new_rule, Formula) and isinstance(existing_rule, Formula):
            form_bool1 = new_rule.formula_bool
            form_bool2 = existing_rule.formula_bool
            if form_bool1 == form_bool2:
                if new_rule.operator == existing_rule.operator:
                    if form_bool1[0]:  # Left terms are formulas
                        if self.check_for_equal_formulas(new_rule.terms[0], existing_rule.terms[0]):
                            pass
                    else:
                        success = self.check_for_equal_formulas(new_rule.terms[0], existing_rule.terms[0])

                    if form_bool1[1]:  # Right terms are formulas
                        if self.check_for_equal_formulas(new_rule.terms[1], existing_rule.terms[1]):
                            pass
                    else:
                        success = self.check_for_equal_literals(new_rule.terms[1], existing_rule.terms[1])

        elif isinstance(new_rule, Literal) and isinstance(existing_rule, Literal):
            success = self.check_for_equal_literals(new_rule, existing_rule)
        return success

    @staticmethod
    def check_for_equal_literals(new_literal, existing_literal):
        if new_literal.atom == existing_literal.atom:
            if new_literal.neg == existing_literal.neg:
                return True
        return False


def pb_to_icb(rule_list):
    temp_program = Program()
    for ri in rule_list[::-1]:  # from ri-1 to r1
        temp_program.merge_rule(ri)
    return temp_program.rule_list
