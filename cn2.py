class CN2:
    def __init__(self, dataset, m):
        self.dataset = dataset
        self.m = m
    def process(self, classified_examples):
        rules = []
        best_cpx = None  # TODO
        while best_cpx is None or not classified_examples:
            best_cpx = self.find_best_complex(classified_examples)
            if best_cpx is not None:
                covered_examples = self.get_covered(best_cpx, classified_examples)
                classified_examples -= covered_examples
                common_class = self.find_common_class(covered_examples)
                rules += (best_cpx, common_class)

    def find_best_complex(self, classified_examples):
        return None

    def get_covered(self, best_cpx, classified_examples):
        return []

    def find_common_class(self, covered_examples):
        return None



