# from antlr4 import *
from antlr4.tree.Tree import TerminalNodeImpl

import data_structs as ds
import parser as ps

# Rule -> Formulas -> Literals (neg/pos)


def print_tree(tree, rule_names, indent = 0):
    if tree.getText() == "<EOF>":
        return
    elif isinstance(tree, TerminalNodeImpl):
        print("{0}{1}".format("  " * indent, tree.getText()))
    else:
        print("{0}{1}:".format("  " * indent, rule_names[tree.getRuleIndex()]))
        for child in tree.children:
            print_tree(child, rule_names, indent + 1)


# Prints formula depth first,
def print_data(formula):
    to_visit = []
    save_operator = []
    while True:
        if isinstance(formula, ds.Formula):
            if formula.left_is_subformula():  # Left term is a formula
                to_visit.append(formula.terms[1])
                save_operator.append(get_operator(formula.operator))
                formula = formula.terms[0]
            elif formula.right_is_subformula():  # Right term is a formula
                to_visit.append(formula.terms[0])
                save_operator.append(get_operator(formula.operator))
                formula = formula.terms[1]
            else:
                left = get_literal(formula.terms[0])
                right = get_literal(formula.terms[1])
                print(left + " " + get_operator(formula.operator) + " " + right, end='')
                if to_visit:
                    op = save_operator.pop()
                    print(" " + op + " ", end='')
                    formula = to_visit.pop()
                else:
                    # print("")
                    break
        else:
            if isinstance(formula, ds.Literal):
                print(get_literal(formula), end='')
                if len(to_visit) == 1:
                    op = save_operator.pop()
                    print(" " + op + " ", end='')
                if to_visit:
                    formula = to_visit.pop()
                else:
                    # print("")
                    break


def get_operator(operator):
    if operator == ds.Operator.OR:
        return "or"
    if operator == ds.Operator.AND:
        return "and"


# Transforms a literal in the right format
def get_literal(term):
    atom = term.atom
    neg = term.neg
    if neg:
        minus = "-"
    else:
        minus = ""
    return minus + atom


def print_rule_list(rule_list):
    for rule in rule_list:
        print_data(rule.conclusion)
        print(" <- ", end='')
        print_data(rule.premise)
        print("")


if __name__ == '__main__':
    rule_list = ps.parse_string("p <- a and -b."
                                "-p <- b.")
    # icb = ds.pb_to_icb(rule_list)
    ftcb = ds.icb_to_ftcb(rule_list)  # Still have to implement removing duplicates.
    # print_rule_list(icb)
    print_rule_list(ftcb)
