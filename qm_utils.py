import qm
import data_structs as ds


# Takes as input a dictionary build by the qm_dict function and returns a simplified rule list.
def apply_qm(qm_dicts):
    rule_list = []
    quinemc = qm.QuineMcCluskey()
    for key in qm_dicts.keys():  # Loop over all the keys.
        literals = qm_dicts[key][0]  # Get the positional literal string
        value = qm_dicts[key][1:]  # Get the minterms
        simplified = quinemc.simplify(value)  # Returns a set of simplified strings
        rule_list += convert_string_to_datastructure(simplified, literals, key)  # Add new rules objects to the rule_list.
    return rule_list


# Takes a set of strings created by simplifications, literal position of the strings  and the conclusion of the formula.
# Returns a list of Rules based on the simplifications and conclusions.
def convert_string_to_datastructure(set_of_strings, literals, conclusion):
    rule_list = []
    for string in set_of_strings:  # Loop over list of strings with same conclusions.
        literal_list = []
        for i in range(len(literals)):  # Loop over the strings
            if string[i] == '0':
                literal_list.append(ds.Literal(literals[i], True))
            elif string[i] == '1':
                literal_list.append(ds.Literal(literals[i]))
            else:
                continue
        formula = literal_list[0]
        for literal in literal_list[1:]:  # Form the AND formula with the created literals.
            formula = ds.Formula.build_and_formula(formula, literal)
        rule_list.append(ds.Rule(conclusion, formula))
    return rule_list


# Creates and returns a dictionary with conclusions as keys with a list as values.
# First element in each value list are the literals used in the premise followed by the minterms.
def qm_dict(rule_list):
    qm_dict = {}
    for rule in rule_list:
        added = False
        minterm, literals = get_minterm_literals(rule.premise)
        for key in qm_dict.keys():  # Iterate through just the keys.
            if key == rule.conclusion:
                qm_dict[key] += [(int('0b' + minterm, 2))]
                added = True
        if not added:
            qm_dict[rule.conclusion] = [literals, int('0b' + minterm, 2)]
    return qm_dict


# Turns formulas into minterm strings. 1 is positive, 0 is negative.
def get_minterm_literals(formula):
    minterm = ""
    literals = ""
    if isinstance(formula, ds.Literal):
        if formula.neg:
            return '0', formula.atom
        else:
            return '1', formula.atom
    else:
        if formula.left_is_subformula():
            minterm_temp, literals_temp = get_minterm_literals(formula.terms[0])
            minterm += minterm_temp
            literals += literals_temp
        else:
            if formula.terms[0].neg:
                minterm += '0'
            else:
                minterm += '1'
            literals += formula.terms[0].atom
        if formula.right_is_subformula():
            minterm_temp, literals_temp = get_minterm_literals(formula.terms[1])
            minterm += minterm_temp
            literals += literals_temp
        else:
            if formula.terms[1].neg:
                minterm += '0'
            else:
                minterm += '1'
            literals += formula.terms[1].atom
        return minterm, literals
