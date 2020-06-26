import data_structs as ds


def extractFacts(situations, facts):
    established = []
    for i in range(len(situations)):
        for fact in facts:
            if check_factor_in_formula(fact, situations[i]) and fact not in established:
                established.append(fact)
                situations[i] = remove_factor_from_formula(fact, situations[i])
            elif check_factor_in_formula(fact.negate_literal(),
                                         situations[i]) and fact.negate_literal() not in established:
                established.append(fact.negate_literal())
                situations[i] = remove_factor_from_formula(fact.negate_literal(), situations[i])
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


# Used to determine the length of the premise of the given rule
def length_rule(rule):
    premise = rule.premise
    return length_formula(premise)


# Used to determine the length of a formula, one literal is one length.
def length_formula(formula):
    length = 0
    if isinstance(formula, ds.Literal):
        return length + 1
    elif formula.left_is_subformula():
        length += length_formula(formula.terms[0])
    else:
        length += 1
    if formula.right_is_subformula():
        length += length_formula(formula.terms[1])
    else:
        length += 1
    return length
