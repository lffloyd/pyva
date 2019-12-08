class MIPSGenerator:

    def generate_code(self, abstract_syntax_tree):
        return abstract_syntax_tree['production'].cgen(abstract_syntax_tree['production'])