from TagmaLexer import TagmaLexer
from TagmaParser import TagmaParser
from TagmaLoader import TagmaLoader


def parse_string(code):
    return parse(InputStream(code))


def parse_file(filename):
    with open(filename, 'r') as myfile:
        code = myfile.read()
    return parse_string(code)


def parse(input_stream):
    lexer = TagmaLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = TagmaParser(stream)
    tree = parser.prog()
    loader = TagmaLoader()
    walker = ParseTreeWalker()
    walker.walk(loader, tree)
    # printRule(loader.rule_list)
    # print_tree(tree, parser.ruleNames)
    return loader.rule_list
