from TagmaLexer import TagmaLexer
from TagmaParser import TagmaParser
from TagmaLoader import TagmaLoader
import antlr4


def parse_string(code):
    return parse(antlr4.InputStream(code))


def parse_file(filename):
    with open(filename, 'r') as myfile:
        code = myfile.read()
    return parse_string(code)


def parse(input_stream):
    lexer = TagmaLexer(input_stream)
    stream = antlr4.CommonTokenStream(lexer)
    parser = TagmaParser(stream)
    tree = parser.prog()
    loader = TagmaLoader()
    walker = antlr4.ParseTreeWalker()
    walker.walk(loader, tree)
    # printRule(loader.rule_list)
    # print_tree(tree, parser.ruleNames)
    return loader.rule_list
