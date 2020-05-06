# Generated from Hello.g4 by ANTLR 4.7.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys

def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\f")
        buf.write("E\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\3\2")
        buf.write("\6\2\20\n\2\r\2\16\2\21\3\2\3\2\3\3\3\3\3\3\3\3\3\3\3")
        buf.write("\4\3\4\3\4\3\4\3\4\3\4\5\4!\n\4\3\4\3\4\3\4\7\4&\n\4\f")
        buf.write("\4\16\4)\13\4\3\5\3\5\3\5\3\5\3\5\3\5\5\5\61\n\5\3\5\3")
        buf.write("\5\3\5\3\5\3\5\3\5\7\59\n\5\f\5\16\5<\13\5\3\6\3\6\3\6")
        buf.write("\5\6A\n\6\3\7\3\7\3\7\2\4\6\b\b\2\4\6\b\n\f\2\2\2E\2\17")
        buf.write("\3\2\2\2\4\25\3\2\2\2\6 \3\2\2\2\b\60\3\2\2\2\n@\3\2\2")
        buf.write("\2\fB\3\2\2\2\16\20\5\4\3\2\17\16\3\2\2\2\20\21\3\2\2")
        buf.write("\2\21\17\3\2\2\2\21\22\3\2\2\2\22\23\3\2\2\2\23\24\7\2")
        buf.write("\2\3\24\3\3\2\2\2\25\26\5\6\4\2\26\27\7\5\2\2\27\30\5")
        buf.write("\b\5\2\30\31\5\f\7\2\31\5\3\2\2\2\32\33\b\4\1\2\33\34")
        buf.write("\7\7\2\2\34\35\5\6\4\2\35\36\7\b\2\2\36!\3\2\2\2\37!\5")
        buf.write("\n\6\2 \32\3\2\2\2 \37\3\2\2\2!\'\3\2\2\2\"#\f\4\2\2#")
        buf.write("$\7\3\2\2$&\5\6\4\5%\"\3\2\2\2&)\3\2\2\2\'%\3\2\2\2\'")
        buf.write("(\3\2\2\2(\7\3\2\2\2)\'\3\2\2\2*+\b\5\1\2+,\7\7\2\2,-")
        buf.write("\5\b\5\2-.\7\b\2\2.\61\3\2\2\2/\61\5\n\6\2\60*\3\2\2\2")
        buf.write("\60/\3\2\2\2\61:\3\2\2\2\62\63\f\5\2\2\63\64\7\3\2\2\64")
        buf.write("9\5\b\5\6\65\66\f\4\2\2\66\67\7\4\2\2\679\5\b\5\58\62")
        buf.write("\3\2\2\28\65\3\2\2\29<\3\2\2\2:8\3\2\2\2:;\3\2\2\2;\t")
        buf.write("\3\2\2\2<:\3\2\2\2=>\7\6\2\2>A\7\n\2\2?A\7\n\2\2@=\3\2")
        buf.write("\2\2@?\3\2\2\2A\13\3\2\2\2BC\7\t\2\2C\r\3\2\2\2\t\21 ")
        buf.write("\'\608:@")
        return buf.getvalue()


class HelloParser ( Parser ):

    grammarFileName = "Hello.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'and'", "'or'", "'<-'", "'-'", "'('", 
                     "')'", "'.'" ]

    symbolicNames = [ "<INVALID>", "AND", "OR", "IMPLIES", "NEG", "LBRA", 
                      "RBRA", "DOT", "ID", "WS", "ANY" ]

    RULE_prog = 0
    RULE_expr = 1
    RULE_conclusion = 2
    RULE_premise = 3
    RULE_literal = 4
    RULE_end = 5

    ruleNames =  [ "prog", "expr", "conclusion", "premise", "literal", "end" ]

    EOF = Token.EOF
    AND=1
    OR=2
    IMPLIES=3
    NEG=4
    LBRA=5
    RBRA=6
    DOT=7
    ID=8
    WS=9
    ANY=10

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None



    class ProgContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(HelloParser.EOF, 0)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(HelloParser.ExprContext)
            else:
                return self.getTypedRuleContext(HelloParser.ExprContext,i)


        def getRuleIndex(self):
            return HelloParser.RULE_prog

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProg" ):
                listener.enterProg(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProg" ):
                listener.exitProg(self)




    def prog(self):

        localctx = HelloParser.ProgContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_prog)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 13 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 12
                self.expr()
                self.state = 15 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << HelloParser.NEG) | (1 << HelloParser.LBRA) | (1 << HelloParser.ID))) != 0)):
                    break

            self.state = 17
            self.match(HelloParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ExprContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def conclusion(self):
            return self.getTypedRuleContext(HelloParser.ConclusionContext,0)


        def IMPLIES(self):
            return self.getToken(HelloParser.IMPLIES, 0)

        def premise(self):
            return self.getTypedRuleContext(HelloParser.PremiseContext,0)


        def end(self):
            return self.getTypedRuleContext(HelloParser.EndContext,0)


        def getRuleIndex(self):
            return HelloParser.RULE_expr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpr" ):
                listener.enterExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpr" ):
                listener.exitExpr(self)




    def expr(self):

        localctx = HelloParser.ExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_expr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 19
            self.conclusion(0)
            self.state = 20
            self.match(HelloParser.IMPLIES)
            self.state = 21
            self.premise(0)
            self.state = 22
            self.end()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ConclusionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.lc = None # Token
            self.rc = None # Token

        def conclusion(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(HelloParser.ConclusionContext)
            else:
                return self.getTypedRuleContext(HelloParser.ConclusionContext,i)


        def LBRA(self):
            return self.getToken(HelloParser.LBRA, 0)

        def RBRA(self):
            return self.getToken(HelloParser.RBRA, 0)

        def literal(self):
            return self.getTypedRuleContext(HelloParser.LiteralContext,0)


        def AND(self):
            return self.getToken(HelloParser.AND, 0)

        def getRuleIndex(self):
            return HelloParser.RULE_conclusion

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConclusion" ):
                listener.enterConclusion(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConclusion" ):
                listener.exitConclusion(self)



    def conclusion(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = HelloParser.ConclusionContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 4
        self.enterRecursionRule(localctx, 4, self.RULE_conclusion, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 30
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [HelloParser.LBRA]:
                self.state = 25
                localctx.lc = self.match(HelloParser.LBRA)
                self.state = 26
                self.conclusion(0)
                self.state = 27
                localctx.rc = self.match(HelloParser.RBRA)
                pass
            elif token in [HelloParser.NEG, HelloParser.ID]:
                self.state = 29
                self.literal()
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 37
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,2,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = HelloParser.ConclusionContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_conclusion)
                    self.state = 32
                    if not self.precpred(self._ctx, 2):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                    self.state = 33
                    self.match(HelloParser.AND)
                    self.state = 34
                    self.conclusion(3) 
                self.state = 39
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx

    class PremiseContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.lp = None # Token
            self.rp = None # Token

        def premise(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(HelloParser.PremiseContext)
            else:
                return self.getTypedRuleContext(HelloParser.PremiseContext,i)


        def LBRA(self):
            return self.getToken(HelloParser.LBRA, 0)

        def RBRA(self):
            return self.getToken(HelloParser.RBRA, 0)

        def literal(self):
            return self.getTypedRuleContext(HelloParser.LiteralContext,0)


        def AND(self):
            return self.getToken(HelloParser.AND, 0)

        def OR(self):
            return self.getToken(HelloParser.OR, 0)

        def getRuleIndex(self):
            return HelloParser.RULE_premise

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPremise" ):
                listener.enterPremise(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPremise" ):
                listener.exitPremise(self)



    def premise(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = HelloParser.PremiseContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 6
        self.enterRecursionRule(localctx, 6, self.RULE_premise, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 46
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [HelloParser.LBRA]:
                self.state = 41
                localctx.lp = self.match(HelloParser.LBRA)
                self.state = 42
                self.premise(0)
                self.state = 43
                localctx.rp = self.match(HelloParser.RBRA)
                pass
            elif token in [HelloParser.NEG, HelloParser.ID]:
                self.state = 45
                self.literal()
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 56
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,5,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 54
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
                    if la_ == 1:
                        localctx = HelloParser.PremiseContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_premise)
                        self.state = 48
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 49
                        self.match(HelloParser.AND)
                        self.state = 50
                        self.premise(4)
                        pass

                    elif la_ == 2:
                        localctx = HelloParser.PremiseContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_premise)
                        self.state = 51
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 52
                        self.match(HelloParser.OR)
                        self.state = 53
                        self.premise(3)
                        pass

             
                self.state = 58
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,5,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx

    class LiteralContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NEG(self):
            return self.getToken(HelloParser.NEG, 0)

        def ID(self):
            return self.getToken(HelloParser.ID, 0)

        def getRuleIndex(self):
            return HelloParser.RULE_literal

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLiteral" ):
                listener.enterLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLiteral" ):
                listener.exitLiteral(self)




    def literal(self):

        localctx = HelloParser.LiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_literal)
        try:
            self.state = 62
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [HelloParser.NEG]:
                self.enterOuterAlt(localctx, 1)
                self.state = 59
                self.match(HelloParser.NEG)
                self.state = 60
                self.match(HelloParser.ID)
                pass
            elif token in [HelloParser.ID]:
                self.enterOuterAlt(localctx, 2)
                self.state = 61
                self.match(HelloParser.ID)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class EndContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DOT(self):
            return self.getToken(HelloParser.DOT, 0)

        def getRuleIndex(self):
            return HelloParser.RULE_end

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEnd" ):
                listener.enterEnd(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEnd" ):
                listener.exitEnd(self)




    def end(self):

        localctx = HelloParser.EndContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_end)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 64
            self.match(HelloParser.DOT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[2] = self.conclusion_sempred
        self._predicates[3] = self.premise_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def conclusion_sempred(self, localctx:ConclusionContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 2)
         

    def premise_sempred(self, localctx:PremiseContext, predIndex:int):
            if predIndex == 1:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 2)
         




