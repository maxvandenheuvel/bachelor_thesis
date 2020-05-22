from antlr4 import *
from antlr4.tree.Tree import TerminalNodeImpl

import data_structs as ds
import parser
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


# Prints (for now) formula depth first,
def print_data(formula):
    to_visit = []
    save_operator = []
    while True:
        if isinstance(formula, ds.Formula):
            form_bool = formula.formula_bool
            if form_bool[0]:  # Left term is a formula
                to_visit.append(formula.terms[1])
                save_operator.append(formula.operator)
                formula = formula.terms[0]
            elif form_bool[1]:  # Right term is a formula
                to_visit.append(formula.terms[0])
                save_operator.append(formula.operator)
                formula = formula.terms[1]
            else:
                left = get_literal(formula.terms[0])
                right = get_literal(formula.terms[1])
                print(left + " " + formula.operator + " " + right, end='')
                if to_visit:
                    op = save_operator.pop()
                    print(" " + op + " ", end='')
                    formula = to_visit.pop()
                else:
                    print("")
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
                    print("")
                    break


# Transforms a literal in the right format
def get_literal(term):
    atom = term.atom
    neg = term.neg
    if neg:
        minus = "-"
    else:
        minus = ""
    return minus + atom

# def icb_ti_ftcb(rule_list):

# def ftcb_to_icb(rule_list):

# def icb_to_pb(rule_list):
#     Quince-McCluskey


if __name__ == '__main__':
    rule_list = parser.parse_string("p <- l and (c or d)."
                                    "p <- l and (c or d).")
    ds.pb_to_icb(rule_list)
    # negate_form(rule_list[0].premise)
    # rule1 = rule_list[0]
    # rule2 = rule_list[1]
    # prem1 = rule1.premise
    # prem2 = rule2.premise
    # conc1 = rule1.conclusion
    # conc2 = rule2.conclusion
    # # if comp_form(conc1, conc2):
    # #     print("conc kek")
    # if comp_form(prem1, prem2):
    #     print("prem kek")
    # # printData(conclusion)
    # printData(prem1)
    # printData(prem2)
