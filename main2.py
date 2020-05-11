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
            self.decorations[ctx] = ds.Formula(terms, ds.Operator().OR, formula_bool)
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


# Prints (for now) data depth first, brackets first ((a and b) and (c and d) does not work yet)

def printData(rule_list):
    for rule in rule_list:
        premise = rule.premise
        conclusion = rule.conclusion
        to_visit = []
        save_operator = []
        while True:
            # print(type(premise))
            if isinstance(premise, ds.Formula):
                form_bool = premise.formula_bool
                if form_bool[0]:  # Left term is a formula
                    to_visit.append(premise.terms[1])
                    save_operator.append(premise.operator)
                    premise = premise.terms[0]
                elif form_bool[1]:  # Right term is a formula
                    to_visit.append(premise.terms[0])
                    save_operator.append(premise.operator)
                    premise = premise.terms[1]
                else:
                    left = getLiteral(premise.terms[0])
                    right = getLiteral(premise.terms[1])
                    print(left + " " + premise.operator + " " + right, end='')
                    if to_visit:
                        op = save_operator.pop()
                        print(" " + op + " ", end='')
                        premise = to_visit.pop()
                    else:
                        print("")
                        break
            else:
                if isinstance(premise, ds.Literal):
                    print(getLiteral(premise), end='')
                    if to_visit:
                        premise = to_visit.pop()
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


if __name__ == '__main__':
    rule_list = parse_string("p <- c and b or (b or d).")
    printData(rule_list)
