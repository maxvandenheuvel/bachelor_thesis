from antlr4 import *

from TagmaListener import TagmaListener
import data_structs as ds


class TagmaLoader(TagmaListener):
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
            self.decorations[ctx] = ds.Formula.build_and_formula(terms)
        pass

    def exitPremise(self, ctx):
        if ctx.literal():
            literal = self.decorations[ctx.literal()]
            self.decorations[ctx] = literal
        elif ctx.lp:
            self.decorations[ctx] = self.decorations[ctx.premise()[0]]
        else:
            left = self.decorations[ctx.premise()[0]]
            right = self.decorations[ctx.premise()[1]]
            terms = [left, right]  # left/right of operator
            if ctx.AND():
                self.decorations[ctx] = ds.Formula.build_and_formula(terms)
            else:
                self.decorations[ctx] = ds.Formula.build_or_formula(terms)
        pass

    def exitLiteral(self, ctx):
        neg = False
        if ctx.NEG():
            neg = True
        literal = ds.Literal(ctx.ID().getText(), neg)
        self.decorations[ctx] = literal

    def exitEnd(self, ctx):
        pass
