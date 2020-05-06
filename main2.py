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
            terms = [self.decorations[ctx.conclusion()[0]], self.decorations[ctx.conclusion()[1]]]
            self.decorations[ctx] = ds.Formula(terms, ds.Operator().OR)
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
            terms = [self.decorations[ctx.premise()[0]], self.decorations[ctx.premise()[1]]]
            self.decorations[ctx] = ds.Formula(terms, operator)
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


# def printRule(rule_list):
#     for rule in rule_list:
#         print(rule)
#         conc = rule.conclusion()
#         prem = rule.premise()
#         while isinstance(conc, ds.Formula):
#             print(conc.terms)
#         # while not isinstance(rule.conclusion, ds.Literal):
#         #
#         #     print(rule.conclusion + "<-")


def parse(input_stream):
    lexer = HelloLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = HelloParser(stream)
    tree = parser.prog()
    loader = HelloLoader()
    walker = ParseTreeWalker()
    walker.walk(loader, tree)
    # print(loader.rule_list)
    # printRule(loader.rule_list)
    # print_tree(tree, parser.ruleNames)


if __name__ == '__main__':
    parse_string("p <- (a or c) and b."
                 "c and d <- a."
                 "b <- s or d.")
