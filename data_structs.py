from enum import Enum
import copy


# Class for the operators
class Operator(Enum):
    NOT = 1
    OR = 2
    AND = 3


# Class to make and negate literal objects.
class Literal:
    def __init__(self, atom, neg=False):
        self.atom = atom
        self.neg = neg  # True if the atom is negative.

    # Returns True if two literals have the same atom and negation.
    def __eq__(self, other):
        if self.atom == other.atom:
            if self.neg == other.neg:
                return True
        return False

    # Negates a literal and returns a new literal object.
    def negate_literal(self):
        return Literal(self.atom, not self.neg)

    # Returns True if the given literal is unspecified in the object literal.
    def is_unspecified_literal(self, literal):
        if self.atom == literal.atom:
            return False
        return True


# Class to create, negate and check formula objects.
class Formula:
    def __init__(self, terms, operator):
        self.terms = terms
        self.operator = operator

    # Negates the formula operator and returns a new Operator object.
    def negate_operator(self):
        if self.operator == Operator.AND:
            return Operator.OR
        elif self.operator == Operator.OR:
            return Operator.AND
        else:
            return 0

    # Negates a formula by negating both terms and the operator and returns a new Formula object.
    def negate_formula(self):
        left_term = self.terms[0].negate_literal()
        right_term = self.terms[1].negate_literal()
        operator = self.negate_operator()
        return Formula([left_term, right_term], operator)

    # Returns True if the left term is a formula object.
    def left_is_subformula(self):
        if isinstance(self.terms[0], Formula):
            return True
        return False

    # Returns True if the right term is a formula object.
    def right_is_subformula(self):
        if isinstance(self.terms[1], Formula):
            return True
        return False

    # Checks if the given literal is unspecified in the formula object. Returns True is unspecified, False otherwise.
    def is_unspecified_formula(self, literal):
        unspecified = False
        if isinstance(self, Literal):  # If the object is a literal, check specification of the literal.
            unspecified = self.is_unspecified_literal(literal)
        else:
            if self.left_is_subformula or self.right_is_subformula():  # If the formula has subformulas.
                if self.left_is_subformula():
                    unspecified = self.terms[0].is_unspecified_formula(literal)  # Recursive handle left term.
                else:
                    unspecified = self.terms[0].is_unspecified_literal(literal)
                if unspecified:
                    if self.right_is_subformula():
                        unspecified = self.terms[1].is_unspecified_formula(literal)  # Recursive handle right term.
                    else:
                        unspecified = self.terms[1].is_unspecified_literal(literal)
            else:
                # If both terms are unspecified by the literal, unspecified is True.
                if self.terms[1].is_unspecified_literal(literal) and self.terms[0].is_unspecified_literal(literal):
                    unspecified = True
        return unspecified

    # Returns a list of literals in a new_formula that are unspecified in the object formula.
    def get_unspecified_literals(self, new_formula):
        unspecified_literals = []
        if isinstance(new_formula, Literal):  # If given formula is a literal, add literal to the list if unspecified.
            if Formula.is_unspecified_formula(self, new_formula):
                unspecified_literals.append(new_formula)
        else:
            if new_formula.left_is_subformula():  # Recursive handle left term.
                unspecified_list = Formula.get_unspecified_literals(self, new_formula.terms[0])
                unspecified_literals.extend([i for i in unspecified_list if i not in unspecified_literals])  # Only
                # add non-duplicate literals.
            else:
                if Formula.is_unspecified_formula(self, new_formula.terms[0]):
                    unspecified_literals.append(new_formula.terms[0])
            if new_formula.right_is_subformula():  # Recursive handle right term.
                unspecified_list = Formula.get_unspecified_literals(self, new_formula.terms[1])
                unspecified_literals.extend([i for i in unspecified_list if i not in unspecified_literals])  # Only
                # add non-duplicate literals.
            else:
                if Formula.is_unspecified_formula(self, new_formula.terms[1]):
                    unspecified_literals.append(new_formula.terms[1])
        return unspecified_literals

    # Builds a formula with the OR operator.
    @staticmethod
    def build_or_formula(left_term, right_term):
        if left_term is None or right_term is None:
            return 0
        return Formula([left_term, right_term], Operator.OR)

    # Builds a formula with the AND operator.
    @staticmethod
    def build_and_formula(left_term, right_term):
        if left_term is None or right_term is None:
            return 0
        return Formula([left_term, right_term], Operator.AND)

    # returns a new negated formula object.
    @staticmethod
    def build_not_formula(formula):
        if formula is None:
            return 0
        neg_formula = copy.copy(formula)
        if isinstance(formula, Formula):
            if formula.left_is_subformula() or formula.right_is_subformula():
                if formula.left_is_subformula():
                    neg_formula.terms[0] = Formula.build_not_formula(formula.terms[0])  # Recursive handle left term.
                else:
                    neg_formula.terms[0] = formula.terms[0].negate_literal()
                if formula.right_is_subformula():
                    neg_formula.terms[1] = Formula.build_not_formula(formula.terms[1])  # Recursive handle right term.
                else:
                    neg_formula.terms[1] = formula.terms[1].negate_literal()
                neg_formula.operator = formula.negate_operator()
            elif not formula.right_is_subformula() and not formula.left_is_subformula():  # If the formula has no
                # subformulas just negate the formula.
                neg_formula = formula.negate_formula()
        elif isinstance(formula, Literal):
            neg_formula = formula.negate_literal()
        return neg_formula


# Class to build Rules with conclusion and premise.
class Rule:
    def __init__(self, conclusion, premise):
        self.conclusion = conclusion
        self.premise = premise


# Class used for conversions, returns the converted rule list.
class Program:
    def __init__(self):
        self.rule_list = []

    # Used for conclusions with operators.
    # def merge_same_conclusion(self, new_rule):
    #     for rule in self.rule_list:
    #         if new_rule.conclusion == rule.conclusion:
    #             rule.premise = Formula.build_or_formula(rule.premise, new_rule.premise)

    # Used for the conversion from priority to constraint based, builds the rule list.
    def priority_to_constraint(self, new_rule):
        if not self.rule_list:  # If rule list is empty, just add the new rule.
            self.rule_list.append(new_rule)
        else:
            merged = False  # Keeps track of merge process.
            for rule in self.rule_list[::-1]:  # Traverse the rule list backwards.
                if new_rule.conclusion == rule.conclusion:  # If the conclusions are the same, build OR formula.
                    rule.premise = Formula.build_or_formula(rule.premise, new_rule.premise)
                    merged = True
                elif new_rule.conclusion == rule.conclusion.negate_literal():  # If conclusions are negations,
                    # build AND with negated premise.
                    new_rule.premise = Formula.build_and_formula(new_rule.premise,
                                                                 Formula.build_not_formula(rule.premise))
                    merged = False
                else:
                    continue
            if not merged:  # Add the rule to the front if not merged.
                self.rule_list.insert(0, new_rule)

    # Used for the conversion from constraint to full tabular constraint, builds the rule list.
    def constraint_to_full_tabular(self, new_rule):
        if not self.rule_list:  # Add new rule if rule list is empty.
            self.rule_list.append(new_rule)
        else:
            for i in range(len(self.rule_list)):  # Loop over rule list and get position integers.
                rule = self.rule_list[i]
                if new_rule.conclusion == rule.conclusion.negate_literal():  # If the conclusions are negations.
                    unspecified_literals = Formula.get_unspecified_literals(rule.premise, new_rule.premise)  # Get
                    # unspecified literals list.
                    for literal in unspecified_literals:  # Loop over unspecified literals and build the new rules.
                        new_lit = Literal(literal.atom, literal.neg)
                        self.rule_list[i] = Rule(rule.conclusion,
                                                 Formula.build_and_formula(new_lit.negate_literal(), rule.premise))
                        self.rule_list.insert(i, Rule(rule.conclusion,
                                                      Formula.build_and_formula(new_lit, rule.premise)))
            self.rule_list.insert(0, new_rule)  # Add the new rule to the front of the list.

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


# Priority based to intermediate constraint based conversion.
def pb_to_icb(rule_list):
    temp_program = Program()
    for ri in rule_list[::-1]:  # from ri to r1
        temp_program.priority_to_constraint(ri)
    return temp_program.rule_list


# Intermediate constraint based to full-tabular constraint based conversion.
def icb_to_ftcb(rule_list):
    temp_program = Program()
    for ri in rule_list[::-1]:  # from ri to r1
        temp_program.constraint_to_full_tabular(ri)
    return temp_program.rule_list
