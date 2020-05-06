# Generated from Hello.g4 by ANTLR 4.7.2
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\f")
        buf.write("\65\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t")
        buf.write("\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\3\2\3\2\3\2\3\2\3")
        buf.write("\3\3\3\3\3\3\4\3\4\3\4\3\5\3\5\3\6\3\6\3\7\3\7\3\b\3\b")
        buf.write("\3\t\5\t+\n\t\3\n\6\n.\n\n\r\n\16\n/\3\n\3\n\3\13\3\13")
        buf.write("\2\2\f\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25\f\3")
        buf.write("\2\4\4\2C\\c|\5\2\13\f\17\17\"\"\2\65\2\3\3\2\2\2\2\5")
        buf.write("\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2")
        buf.write("\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2\25\3\2\2")
        buf.write("\2\3\27\3\2\2\2\5\33\3\2\2\2\7\36\3\2\2\2\t!\3\2\2\2\13")
        buf.write("#\3\2\2\2\r%\3\2\2\2\17\'\3\2\2\2\21*\3\2\2\2\23-\3\2")
        buf.write("\2\2\25\63\3\2\2\2\27\30\7c\2\2\30\31\7p\2\2\31\32\7f")
        buf.write("\2\2\32\4\3\2\2\2\33\34\7q\2\2\34\35\7t\2\2\35\6\3\2\2")
        buf.write("\2\36\37\7>\2\2\37 \7/\2\2 \b\3\2\2\2!\"\7/\2\2\"\n\3")
        buf.write("\2\2\2#$\7*\2\2$\f\3\2\2\2%&\7+\2\2&\16\3\2\2\2\'(\7\60")
        buf.write("\2\2(\20\3\2\2\2)+\t\2\2\2*)\3\2\2\2+\22\3\2\2\2,.\t\3")
        buf.write("\2\2-,\3\2\2\2./\3\2\2\2/-\3\2\2\2/\60\3\2\2\2\60\61\3")
        buf.write("\2\2\2\61\62\b\n\2\2\62\24\3\2\2\2\63\64\13\2\2\2\64\26")
        buf.write("\3\2\2\2\5\2*/\3\b\2\2")
        return buf.getvalue()


class HelloLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    AND = 1
    OR = 2
    IMPLIES = 3
    NEG = 4
    LBRA = 5
    RBRA = 6
    DOT = 7
    ID = 8
    WS = 9
    ANY = 10

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'and'", "'or'", "'<-'", "'-'", "'('", "')'", "'.'" ]

    symbolicNames = [ "<INVALID>",
            "AND", "OR", "IMPLIES", "NEG", "LBRA", "RBRA", "DOT", "ID", 
            "WS", "ANY" ]

    ruleNames = [ "AND", "OR", "IMPLIES", "NEG", "LBRA", "RBRA", "DOT", 
                  "ID", "WS", "ANY" ]

    grammarFileName = "Hello.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


