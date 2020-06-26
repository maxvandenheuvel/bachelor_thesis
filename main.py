# from antlr4 import *
from antlr4.tree.Tree import TerminalNodeImpl

import converters as cv
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


# Prints formula depth first
def print_data(formula):
    if isinstance(formula, ds.Literal):
        print(get_literal(formula), end='')
    else:
        if formula.left_is_subformula():
            print_data(formula.terms[0])
        else:
            print(get_literal(formula.terms[0]) + " " + get_operator(formula.operator) + " ", end='')
        if formula.left_is_subformula() and formula.right_is_subformula():
            print(" " + get_operator(formula.operator) + " ", end='')
        if formula.right_is_subformula():
            print_data(formula.terms[1])
        elif formula.left_is_subformula():
            print(" " + get_operator(formula.operator) + " " + get_literal(formula.terms[1]), end='')
        else:
            print(get_literal(formula.terms[1]), end='')


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
    # rule_list = ps.parse_string("p <- a and -b."
    #                             "-p <- b and c.")
    rule_list = ps.parse_file("testGrammar")
    icb = cv.pb_to_icb(rule_list)
    # ftcb = cv.icb_to_ftcb(rule_list)
    # print_rule_list(icb)
    # icb = cv.ftcb_to_icb(ftcb)
    # pb = cv.icb_to_pb(rule_list)
    # print_rule_list(icb)
    # print()
    print_rule_list(icb)

