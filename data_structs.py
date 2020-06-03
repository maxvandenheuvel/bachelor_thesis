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
        if self.atom == other.atom and self.neg == other.neg:
            return True
        return False

    # So we can use literals as keys when making a dictionary.
    def __hash__(self):
        return hash((self.atom, self.neg))

    def __gt__(self, other):
        return self.atom > other.atom

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

    # Takes a literal and a formula and returns the formula with the literal inserted in alphabetical order,
    # also returns a literal that still needs to be added.
    @staticmethod
    def sort_and_alphabetical(formula, literal):
        formula_c = copy.deepcopy(formula)  # Create a full copy of the formula
        literal_c = copy.deepcopy(literal)  # Create a full copy of the literal
        if formula_c.left_is_subformula():
            formula_c.terms[0], literal_c = Formula.sort_and_alphabetical(formula_c.terms[0], literal_c)
        else:
            if formula_c.terms[0] > literal_c:  # Check if left term is lower in the alphabet
                temp = formula_c.terms[0]
                formula_c.terms[0] = literal_c
                literal_c = temp
        if formula_c.right_is_subformula():
            formula_c.terms[1], literal_c = Formula.sort_and_alphabetical(formula_c.terms[1], literal_c)
        else:
            if formula_c.terms[1] > literal_c:  # Check if right term is lower in the alphabet
                temp = formula_c.terms[1]
                formula_c.terms[1] = literal_c
                literal_c = temp
        return formula_c, literal_c

    # Adds the given literal to the formula so it is sorted in alphabetical order, only with AND operators.
    @staticmethod
    def build_sort_and_formula(formula, literal):
        if isinstance(formula, Literal):
            if formula > literal:  # Check if formula is lower in the alphabet than literal.
                return Formula.build_and_formula(literal, formula)
            else:
                return Formula.build_and_formula(formula, literal)
        else:  # Sort the formula and return the last literal that needs to be added.
            formula, literal = Formula.sort_and_alphabetical(formula, literal)
            return Formula.build_and_formula(formula, literal)

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
