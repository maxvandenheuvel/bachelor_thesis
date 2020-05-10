

class DataStructs:
    def __init__(self):
        self.self = self

    class Operator:
        def __init__(self):
            self.AND = "and"
            self.OR = "or"

    class Literal:
        def __init__(self, atom, neg):
            self.atom = atom
            self.neg = neg

    class Formula:
        def __init__(self, terms, operator, formula_bool):
            self.terms = terms
            self.operator = operator
            self.formula_bool = formula_bool

    class Rule:
        def __init__(self, conclusion, premise):
            self.conclusion = conclusion
            self.premise = premise


obj = DataStructs.Literal("a", False)
