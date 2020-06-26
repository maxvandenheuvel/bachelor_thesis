import data_structs as ds
import copy
import utils as ut
import main as mn
# First make a copy of the given rule base and then return the sorted rule base "name"_copy


class Order:
    def __init__(self, rule_list):
        self.rule_list = rule_list

    def order_rules(self, argument=""):
        if isinstance(argument, list):
            self.sort_with_given_index(argument)
        else:
            method = getattr(self, argument, lambda: "highest is bottom")
            return method()

    def top_is_highest(self):
        self.rule_list = self.rule_list[::-1]
        return "Top has highest priority"

    def long_is_highest(self):
        self.rule_list.sort(key=ut.length_rule)
        return "Longest has highest priority"

    def short_is_highest(self):
        self.rule_list.sort(reverse=True, key=ut.length_rule)
        return "Shortest has highest priority"

    def sort_with_given_index(self, argument):
        print("i")
        temp_list = copy.copy(self.rule_list)
        new_rule_list = []
        pop_count, index = 0, 0
        for i in argument:
            print(i)
            if i > len(self.rule_list) - 1:
                return 0
            print("index", index)
            index = i - pop_count
            if index < 0:
                index = 0
            print("index:", index)
            print("popcount:", pop_count)
            new_rule_list.append(temp_list.pop(index))
            pop_count += 1
        self.rule_list = new_rule_list + temp_list
        mn.print_rule_list(new_rule_list)
        return "Priority determined by given index"


class SpecificGeneral:
    def __init__(self, rule_list):
        self.rule_list = rule_list


class Node:
    def __init__(self, literal):
        self.literal = literal
        self.edges = []

    def assign_edges(self, weight, other):
        self.edges.append((weight, other))

    def clear_edges(self):
        self.edges = []

    def determine_weight(self, formula, weight=1):
        left_and = False
        if isinstance(formula, ds.Literal):
            self.assign_edges(1/weight, formula)
        else:
            if formula.operator == ds.Operator.AND:
                weight += 1
                temp = formula
                while temp.right_is_subformula():
                    temp = temp.terms[1]
                    if temp.operator == ds.Operator.AND:
                        weight += 1
                    else:
                        break
            if formula.left_is_subformula():
                if formula.terms[0].operator == ds.Operator.AND:
                    left_and = True
                self.determine_weight(formula.terms[0], weight)
            else:
                self.assign_edges(1/weight, formula.terms[0])
            if formula.right_is_subformula():
                self.determine_weight(formula.terms[1], weight)
            else:
                if left_and and formula.operator == ds.Operator.AND:
                    weight += 1
                self.assign_edges(1/weight, formula.terms[1])


# def create_edges(rule)
#     node = Node(rule.conclusion)
#     if formula.left_is_subformula():
#         pass
#     else:
#
#     if formula.right_is_subformula():
#         pass
#     Weights or subsumption

# # Be able to check if a formula us subsumed by another formula
# def check_subsumed(formula, other):
#     if other.left_is_subformula():
#         check_subsumed(formula, other.terms[0])
#     elif not ut.check_factor_in_formula(other.terms[0], formula):
#         return 0
#     else:
#         if other.right_is_subformula():
#             check_subsumed(formula, other.terms[1])
#         elif not ut.check_factor_in_formula(other.terms[1])
#             return 0