from HelloParser import HelloParser

def same_conc_list(rule_list):
    rule_list = rule_list[::-1]
    rule_dict = make_rule_dict(rule_list)
    for rule in rule_list:
        if rule == rule_list[-1]:
            break
        for next_rule in rule_list[rule_list.index(rule) + 1:]:
            if rule.conclusion().getText() == next_rule.conclusion().getText():
                rule_dict[next_rule].append(rule.premise())
    return rule_dict


def make_rule_dict(rule_list):
    dict = {}
    for rule in rule_list:
        dict[rule] = []
    return dict


def opposite_conc_list(rule_list):
    rule_list = rule_list[::-1]
    rule_dict = make_rule_dict(rule_list)
    for rule in rule_list:
        if rule == rule_list[-1]:
            break
        for next_rule in rule_list[rule_list.index(rule) + 1:]:
            if rule.conclusion().getText() == "-" + next_rule.conclusion().getText()\
               or "-" + rule.conclusion().getText() == next_rule.conclusion().getText():
                rule_dict[next_rule].append(rule.premise())
    return rule_dict


class Combine(object):
    def __init__(self):
        self.start = None

    def combine_rule(self, rule_list, decorations):  # Opposite
        op_dict = opposite_conc_list(rule_list, decorations)
        print_dict(op_dict)
        for rule in rule_list:
            opposites = op_dict.get(rule)
            for i in rule.children[:-1]:    # Printing the rule
                if i == rule.children[-2]:
                    print(i.getText(), end='')
                else:
                    print(i.getText() + " ", end='')
            for op in opposites:    # Printing the opposites
                if isinstance(op.children[0], HelloParser.NegIDContext):
                    print(" and " + op.children[0].ID().getText(), end='')
                else:
                    print(" and -" + op.getText(), end='')
            print(rule.children[-1].getText())

def print_dict(rule_dict):
    for i in rule_dict:
        print("key", i.getText())
        for op in rule_dict.get(i):
            print("value", op.getText())
        print("new")
