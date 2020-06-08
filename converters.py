import data_structs as ds
import qm_utils as qmu
import copy
import main as mn

# Class used for conversions, returns the converted rule list.
class Program:
    def __init__(self):
        self.rule_list = []

    # Used for the conversion from priority to constraint based, builds the rule list.
    def priority_to_intermediate(self, new_rule):
        if not self.rule_list:  # If rule list is empty, just add the new rule.
            self.rule_list.append(new_rule)
        else:
            merged = False  # Keeps track of merge process.
            for rule in self.rule_list[::-1]:  # Traverse the rule list backwards.
                if new_rule.conclusion == rule.conclusion:  # If the conclusions are the same, build OR formula.
                    rule.premise = ds.Formula.build_or_formula(rule.premise, new_rule.premise)
                    merged = True
                elif new_rule.conclusion == rule.conclusion.negate_literal():  # If conclusions are negations,
                    # build AND with negated premise.
                    new_rule.premise = ds.Formula.build_and_formula(new_rule.premise,
                                                                    ds.Formula.build_not_formula(rule.premise))
                    merged = False
                else:
                    continue
            if not merged:  # Add the rule to the front if not merged.
                self.rule_list.insert(0, new_rule)

    # Used for the conversion from intermediate to full tabular constraint, builds the rule list alphabetical order.
    def intermediate_to_full_tabular(self, new_rule):
        added = False
        for i in range(len(self.rule_list)):  # Loop over rule list and get index.
            if new_rule.conclusion == self.rule_list[i].conclusion.negate_literal():  # If the conclusions are
                # negations.
                rule = self.rule_list.pop(i)
                unspecified_literals_old = ds.Formula.get_unspecified_literals(rule.premise, new_rule.premise)  # Get
                # literals from the new_rule that are unspecified in the old rule.
                unspecified_literals_new = ds.Formula.get_unspecified_literals(new_rule.premise, rule.premise)  # Get
                # literals from the old that are unspecified in the new rule.

                for literal in unspecified_literals_old:  # Loop over unspecified literals and rebuild old rules.
                    new_lit = ds.Literal(literal.atom, literal.neg)
                    new_lit_neg = new_lit.negate_literal()
                    self.rule_list.insert(i, ds.Rule(rule.conclusion,
                                                     ds.Formula.build_sort_and_formula(rule.premise, new_lit_neg)))
                    self.rule_list.insert(i, ds.Rule(rule.conclusion,
                                                     ds.Formula.build_sort_and_formula(rule.premise, new_lit)))

                for literal in unspecified_literals_new:  # Build the new rules and insert.
                    new_lit = ds.Literal(literal.atom, literal.neg)
                    new_lit_neg = new_lit.negate_literal()
                    self.rule_list.insert(i, ds.Rule(new_rule.conclusion,
                                                     ds.Formula.build_sort_and_formula(new_rule.premise, new_lit_neg)))
                    self.rule_list.insert(i, ds.Rule(new_rule.conclusion,
                                                     ds.Formula.build_sort_and_formula(new_rule.premise, new_lit)))
                    added = True
        if not added:
            self.rule_list.insert(0, new_rule)  # Add the new rule to the front of the list.

    @staticmethod
    def full_tabular_to_intermediate(rule_list):
        rule_dict = qmu.qm_dict(rule_list)
        return qmu.apply_qm(rule_dict)

    def intermediate_to_priority(self, rules):
        established_factors = []
        not_evaluated_situations = []
        facts = []
        for ri in rules[::-1]:  # Get highest priority first
            conclusion = ri.conclusion
            factors = get_relevant_factors(rules, conclusion)
            if not established_factors:
                established_factors = []
            if not not_evaluated_situations:
                not_evaluated_situations = relevant_situations(factors)
            rule_base_i = formula_to_full_tabular(ri.premise, factors)  # Rule base filled with premises.
            rule_base_j = []
            for rj in rule_base_i:
                if rj in not_evaluated_situations:
                    new_premise = copy.deepcopy(rj)
                    apply = True
                    for factor in established_factors:
                        if check_factor_in_formula(factor.negate_literal(), rj):
                            apply = False
                            break
                        elif check_factor_in_formula(factor, rj):
                            new_premise = remove_factor_from_formula(factor, new_premise)

                    if apply and new_premise:
                        rule_base_j.append(ds.Rule(conclusion, new_premise))
                    not_evaluated_situations.remove(rj)
            rule_dict = qmu.qm_dict(rule_base_j)  # Apply QM on rule_base_js
            new_rule_base = qmu.apply_qm(rule_dict)
            for rule in new_rule_base:
                facts += factors_premise(rule.premise)
                self.rule_list.insert(0, rule)
            established_factors = extract_factors(not_evaluated_situations, facts)


# Priority based to intermediate constraint based conversion.
def pb_to_icb(rule_list):
    temp_program = Program()
    for ri in rule_list[::-1]:  # from ri to r1
        temp_program.priority_to_intermediate(ri)
    return temp_program.rule_list


# Intermediate constraint based to full-tabular constraint based conversion.
def icb_to_ftcb(rule_list):
    temp_program = Program()
    for ri in rule_list[::-1]:  # from ri to r1
        temp_program.intermediate_to_full_tabular(ri)
    return temp_program.rule_list


def ftcb_to_icb(rule_list):
    temp_program = Program()
    return temp_program.full_tabular_to_intermediate(rule_list)


def icb_to_pb(rule_list):  # Last rule has highest priority (for now)
    temp_program = Program()
    temp_program.intermediate_to_priority(rule_list)
    # print(temp_program.rule_list)
    return temp_program.rule_list


def extract_factors(situations, facts):
    established = []
    for i in range(len(situations)):
        for fact in facts:
            if check_factor_in_formula(fact, situations[i]) and fact not in established:
                established.append(fact)
            elif check_factor_in_formula(fact.negate_literal(), situations[i]) and fact.negate_literal() not in established:
                established.append(fact.negate_literal())
    return established


# Returns the formula object with the given factor removed from the formula. Returns False if formula becomes empty.
def remove_factor_from_formula(factor, formula):
    if isinstance(formula, ds.Literal):
        return False
    if formula.left_is_subformula():
        formula.terms[0] = remove_factor_from_formula(factor, formula.terms[0])
    elif factor == formula.terms[0]:
        return formula.terms[1]
    if formula.right_is_subformula():
        formula.terms[1] = remove_factor_from_formula(factor, formula.terms[1])
    elif factor == formula.terms[1]:
        return formula.terms[0]
    return formula


# Returns True is the given factor is in the formula. False otherwise.
def check_factor_in_formula(factor, formula):
    if isinstance(formula, ds.Literal):
        if factor == formula:
            return True
    else:
        if formula.left_is_subformula():
            if check_factor_in_formula(factor, formula.terms[0]):
                return True
        elif factor == formula.terms[0]:
            return True
        if formula.right_is_subformula():
            if check_factor_in_formula(factor, formula.terms[1]):
                return True
        elif factor == formula.terms[1]:
            return True
    return False


# Returns a list the formula in full tabular form based on the given factors.
def formula_to_full_tabular(formula, factors):
    full_tabular_list = []
    added = False
    for factor in factors:
        if check_factor_in_formula(factor, formula) or check_factor_in_formula(factor.negate_literal(), formula):
            continue
        full_tabular_list.append(ds.Formula.build_sort_and_formula(formula, factor))
        full_tabular_list.append(ds.Formula.build_sort_and_formula(formula, factor.negate_literal()))
        added = True
    if not added:
        full_tabular_list.append(formula)
    return full_tabular_list


# Creates all possible situations based on a factor list. Returns a list of situations (AND formulas)
def relevant_situations(factor_list):
    if not factor_list:
        return False
    situations = [factor_list[0], factor_list[0].negate_literal()]
    for f in factor_list[1:]:
        for i in range(len(situations)):
            situations.append(ds.Formula.build_and_formula(situations[i], f))
            situations[i] = ds.Formula.build_and_formula(situations[i], f.negate_literal())
    return situations


# Returns a list of new factors objects which are relevant to the given conclusion.
def get_relevant_factors(formula_list, conclusion):
    factors = []
    for formula in formula_list:
        if formula.conclusion == conclusion or formula.conclusion == conclusion.negate_literal():
            formula_factors = factors_premise(formula.premise)
            for factor in formula_factors:
                if factor not in factors and factor.negate_literal() not in factors:
                    factors.append(factor)
    return factors


# Returns a list of new literal objects which are all the factors in the given premise.
def factors_premise(premise):
    factors = []
    if isinstance(premise, ds.Literal):
        # factors.append(ds.Literal(premise.atom, premise.neg))
        factors.append(premise)
    else:
        if premise.left_is_subformula():
            factors += factors_premise(premise.terms[0])
        else:
            # factors.append(ds.Literal(premise.terms[0].atom, premise.terms[0].neg))
            factors.append(premise.terms[0])
        if premise.right_is_subformula():
            factors += factors_premise(premise.terms[1])
        else:
            # factors.append(ds.Literal(premise.terms[1].atom, premise.terms[1].neg))
            factors.append(premise.terms[1])
    return factors



