from antlr4 import *
from antlr4.tree.Tree import TerminalNodeImpl

import data_structs as ds

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


# def comp_lit(literal1, literal2):
#     if literal1.atom == literal2.atom:
#         if literal1.neg == literal2.neg:
#             return True
#     return False


# Recursive comparison of two formulas, Returns True if equal, False otherwise.
# def comp_form(form1, form2):
#     success = False
#     if isinstance(form1, ds.Formula) and isinstance(form2, ds.Formula):
#         form_bool1 = form1.formula_bool
#         form_bool2 = form2.formula_bool
#         if form_bool1 == form_bool2:
#             if form1.operator == form2.operator:
#                 if form_bool1[0]:  # Left terms are formulas
#                     if comp_form(form1.terms[0], form2.terms[0]):
#                         pass
#                 else:
#                     success = comp_lit(form1.terms[0], form2.terms[0])
#
#                 if form_bool1[1]:  # Right terms are formulas
#                     if comp_form(form1.terms[1], form2.terms[1]):
#                         pass
#                 else:
#                     success = comp_lit(form1.terms[1], form2.terms[1])
#
#     elif isinstance(form1, ds.Literal) and isinstance(form2, ds.Literal):
#         success = comp_lit(form1, form2)
#     return success


# def pb_to_icb(rule_list):
#     ri = rule_list.pop()
#     ri_conc = ri.conclusion
#     neg_ri_conc = negate_form(ri_conc)
#
#     for rj in rule_list[::-1]:  # from ri-1 to r1
#         rj_conc = rj.conclusion
#         if comp_form(rj_conc, neg_ri_conc):
#     #         rj.premise = rj.premise and negate_form(ri.premise)
#     #         Implement a way to add formulas to existing formulas
#     pb_to_cb(rule_list) # Recursively convert


# def icb_ti_ftcb(rule_list):

# def ftcb_to_icb(rule_list):

# def icb_to_pb(rule_list):
#     Quince-McCluskey


if __name__ == '__main__':
    rule_list = parse_string("p and c and c <- l and (c or d)."
                             "p and d <- l and (c or d).")
    # negate_form(rule_list[0].premise)
    rule1 = rule_list[0]
    rule2 = rule_list[1]
    prem1 = rule1.premise
    prem2 = rule2.premise
    conc1 = rule1.conclusion
    conc2 = rule2.conclusion
    # if comp_form(conc1, conc2):
    #     print("conc kek")
    if comp_form(prem1, prem2):
        print("prem kek")
    # printData(conclusion)
    printData(prem1)
    printData(prem2)
