from antlr4 import *

from HelloLexer import HelloLexer
from HelloParser import HelloParser
from HelloListener import HelloListener
from antlr4.tree.Tree import TerminalNodeImpl
from check import *


class HelloLoader(HelloListener):
    def __init__(self):
        self.decorations = {}  # Decorate the tree
        self.rule_list = []  # End products
        self.opposite_conc_list = []
        self.same_conc_list = []
        self.lastExpr = None
        self.conc_dict = []

    def exitProg(self, ctx):
        Combine.combine_rule(self, self.rule_list, self.decorations)
        pass

    def exitExpr(self, ctx):
        self.rule_list.append(ctx)
        pass

    def exitConclusion(self, ctx):
        pass

    def exitPremise(self, ctx):
        pass

    # For later implementation of "or" in conclusion
    # def exitAndlit(self, ctx):
    #     # print(ctx.getText())
    #     pass
    #
    # def exitOrlit(self, ctx):
    #     pass

    def exitNegID(self, ctx):
        self.decorations[ctx] = False
        pass

    def exitGenID(self, ctx):
        self.decorations[ctx] = True
        pass

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
    print_tree(tree, parser.ruleNames)


if __name__ == '__main__':
    parse_string("p <- a and c."
                 "-p <- -b.")
