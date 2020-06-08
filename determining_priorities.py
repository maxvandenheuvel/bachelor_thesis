import data_structs as ds


class Order:
    def __init__(self, rule_list):
        self.rule_list = rule_list

    def order_rules(self, argument):
        method = getattr(self, argument, lambda: "highest_is_bottom")
        return method()

    def top_is_highest(self):
        self.rule_list = self.rule_list[::-1]

    def long_is_highest(self):
        return self.rule_list.sort(reverse=True, key=length_rule)

    def short_is_highest(self):
        return self.rule_list.sort(key=length_rule)


class SpecificGeneral:
    def __init__(self, rule_list):
        self.rule_list = rule_list


def length_rule(rule):
    premise = rule.premise
    return length_formula(premise)


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
