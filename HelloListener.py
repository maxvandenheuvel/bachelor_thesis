# Generated from Hello.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .HelloParser import HelloParser
else:
    from HelloParser import HelloParser

# This class defines a complete listener for a parse tree produced by HelloParser.
class HelloListener(ParseTreeListener):

    # Enter a parse tree produced by HelloParser#prog.
    def enterProg(self, ctx:HelloParser.ProgContext):
        pass

    # Exit a parse tree produced by HelloParser#prog.
    def exitProg(self, ctx:HelloParser.ProgContext):
        pass


    # Enter a parse tree produced by HelloParser#expr.
    def enterExpr(self, ctx:HelloParser.ExprContext):
        pass

    # Exit a parse tree produced by HelloParser#expr.
    def exitExpr(self, ctx:HelloParser.ExprContext):
        pass


    # Enter a parse tree produced by HelloParser#conclusion.
    def enterConclusion(self, ctx:HelloParser.ConclusionContext):
        pass

    # Exit a parse tree produced by HelloParser#conclusion.
    def exitConclusion(self, ctx:HelloParser.ConclusionContext):
        pass


    # Enter a parse tree produced by HelloParser#premise.
    def enterPremise(self, ctx:HelloParser.PremiseContext):
        pass

    # Exit a parse tree produced by HelloParser#premise.
    def exitPremise(self, ctx:HelloParser.PremiseContext):
        pass


    # Enter a parse tree produced by HelloParser#literal.
    def enterLiteral(self, ctx:HelloParser.LiteralContext):
        pass

    # Exit a parse tree produced by HelloParser#literal.
    def exitLiteral(self, ctx:HelloParser.LiteralContext):
        pass


    # Enter a parse tree produced by HelloParser#end.
    def enterEnd(self, ctx:HelloParser.EndContext):
        pass

    # Exit a parse tree produced by HelloParser#end.
    def exitEnd(self, ctx:HelloParser.EndContext):
        pass


