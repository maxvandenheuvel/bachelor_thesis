from antlr4 import *

from HelloLexer import HelloLexer
from HelloParser import HelloParser
from HelloListener import HelloListener
from antlr4.tree.Tree import TerminalNodeImpl
from data_structs import DataStructs as ds


class HelloLoader(HelloListener):
    def __init__(self):
        self.decorations = {}  # Decorate the tree
        self.rule_list = []  # End products

    def exitProg(self, ctx):
        pass

    def exitExpr(self, ctx):
        conclusion = self.decorations[ctx.conclusion()]
        premise = self.decorations[ctx.premise()]
        rule = ds.Rule(conclusion, premise)
        self.decorations[ctx] = rule
        self.rule_list.append(rule)
        pass

    def exitConclusion(self, ctx):
        if ctx.literal():
            literal = self.decorations[ctx.literal()]
            self.decorations[ctx] = literal
        elif ctx.lc:
            self.decorations[ctx] = self.decorations[ctx.premise()[0]]
        else:
            left = self.decorations[ctx.conclusion()[0]]
            right = self.decorations[ctx.conclusion()[1]]
            terms = [left, right]
            formula_bool = [isinstance(left, ds.Formula), isinstance(right, ds.Formula)]
            self.decorations[ctx] = ds.Formula(terms, ds.Operator().AND, formula_bool)
        pass

    def exitPremise(self, ctx):
        if ctx.literal():
            literal = self.decorations[ctx.literal()]
            self.decorations[ctx] = literal
        elif ctx.lp:
            self.decorations[ctx] = self.decorations[ctx.premise()[0]]
        else:
            if ctx.AND():
                operator = ds.Operator().AND
            else:
                operator = ds.Operator().OR
            left = self.decorations[ctx.premise()[0]]
            right = self.decorations[ctx.premise()[1]]
            terms = [left, right]  # left/right of operator
            formula_bool = [isinstance(left, ds.Formula), isinstance(right, ds.Formula)]  # Lets us know if term is a formula
            self.decorations[ctx] = ds.Formula(terms, operator, formula_bool)
        pass

    def exitLiteral(self, ctx):
        neg = False
        if ctx.NEG():
            neg = True
        literal = ds.Literal(ctx.ID().getText(), neg)
        self.decorations[ctx] = literal
        # print(ctx.getText())

    def exitEnd(self, ctx):
        pass


def parse_string(code):
    return parse(InputStream(code))


def parse_file(filename):
    with open(filename, 'r') as myfile:
        code = myfile.read()
    return parse_string(code)


def print_tree(tree, rule_names, indent = 0):
    if tree.getText() == "<EOF>":
        return
    elif isinstance(tree, TerminalNodeImpl):
        print("{0}{1}".format("  " * indent, tree.getText()))
    else:
        print("{0}{1}:".format("  " * indent, rule_names[tree.getRuleIndex()]))
        for child in tree.children:
            print_tree(child, rule_names, indent + 1)


def parse(input_stream):
    lexer = HelloLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = HelloParser(stream)
    tree = parser.prog()
    loader = HelloLoader()
    walker = ParseTreeWalker()
    walker.walk(loader, tree)

    return loader.rule_list
    # printRule(loader.rule_list)
    # print_tree(tree, parser.ruleNames)

# Rule -> Formulas -> Literals (neg/pos)


# Returns a struct of the negation of the given formula
def negateForm(formula):
    neg_form = formula
    if isinstance(neg_form, ds.Formula):
        form_bool = neg_form.formula_bool
        terms = neg_form.terms
        if form_bool[0]:
            negateForm(neg_form.terms[0])
        if form_bool[1]:
            negateForm(neg_form.terms[1])
        else:
            negateLit(terms[0])
            negateLit(terms[1])
        if neg_form.operator == "and":
            neg_form.operator = "or"
        else:
            neg_form.operator = "and"
    else:
        negateLit(neg_form)
    return neg_form


# Negates the given literal
def negateLit(literal):
    if literal.neg:
        literal.neg = False
    else:
        literal.neg = True
    return


# Prints (for now) formula depth first,
def printData(formula):
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
                left = getLiteral(formula.terms[0])
                right = getLiteral(formula.terms[1])
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
                print(getLiteral(formula), end='')
                if len(to_visit) == 1:
                    op = save_operator.pop()
                    print(" " + op + " ", end='')
                if to_visit:
                    formula = to_visit.pop()
                else:
                    print("")
                    break


# Transforms a literal in the right format
def getLiteral(term):
    atom = term.atom
    neg = term.neg
    if neg:
        minus = "-"
    else:
        minus = ""
    return minus + atom


def comp_lit(literal1, literal2):
    if literal1.atom == literal2.atom:
        if literal1.neg == literal2.neg:
            return True
    return False


# Recursive comparison of two formulas, Returns True if equal, False otherwise.
def comp_form(form1, form2):
    success = False
    if isinstance(form1, ds.Formula) and isinstance(form2, ds.Formula):
        form_bool1 = form1.formula_bool
        form_bool2 = form2.formula_bool
        if form_bool1 == form_bool2:
            if form1.operator == form2.operator:
                if form_bool1[0]:  # Left terms are formulas
                    if comp_form(form1.terms[0], form2.terms[0]):
                        pass
                else:
                    success = comp_lit(form1.terms[0], form2.terms[0])

                if form_bool1[1]:  # Right terms are formulas
                    if comp_form(form1.terms[1], form2.terms[1]):
                        pass
                else:
                    success = comp_lit(form1.terms[1], form2.terms[1])

    elif isinstance(form1, ds.Literal) and isinstance(form2, ds.Literal):
        success = comp_lit(form1, form2)
    return success


# def pb_to_cb(rule_list):
#     ri = rule_list.pop()
#     ri_conc = ri.conclusion
#     neg_ri_conc = negateForm(ri_conc)
#
#     for rj in rule_list[::-1]:  # from ri-1 to r1
#         rj_conc = rj.conclusion
#         if comp_form(rj_conc, neg_ri_conc):
#     #         rj.premise = rj.premise and negateForm(ri.premise)
#     #         Implement a way to add formulas to existing formulas
#     pb_to_cb(rule_list) # Recursively convert


if __name__ == '__main__':
    rule_list = parse_string("p and c and c <- l and (c or d)."
                             "p and d <- l and (c or d).")
    # negateForm(rule_list[0].premise)
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
