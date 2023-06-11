import copy
import numpy as np

from Algorithm import Algorithm


class CN2(Algorithm):
    def __init__(self, dataset, min_significance=0.4, max_size_star=3):
        super().__init__()
        self.dataset = dataset
        self.selectors = self._get_all_attributes()
        self.classes = set(example["class"] for example in self.dataset)
        self.min_significance = min_significance
        self.max_size_star = max_size_star
        self.rules = self.process()

    def process(self):
        rules = []
        classified_examples = copy.deepcopy(self.dataset)
        best_cpx = ()
        while best_cpx is not None:
            best_cpx = self.find_best_complex(classified_examples)
            if best_cpx is not None:
                covered_examples = self.get_covered(best_cpx, classified_examples)
                classified_examples = [element for element in classified_examples if element not in covered_examples]
                common_class = self.get_most_common_class(covered_examples)
                rules += [(best_cpx, common_class)]
        return rules

    def find_best_complex(self, classified_examples):
        star = {()}
        best_cpx = None
        best_cpx_quality = float('inf')
        while len(star) != 0:
            new_star = self.specialize_star(star)
            star_cpx_quality = {}
            for cpx in new_star:
                cpx_significance = self.count_significance(cpx, classified_examples)
                if cpx_significance > self.min_significance:
                    cpx_quality = self.count_entropy(cpx, classified_examples)
                    star_cpx_quality[cpx] = cpx_quality
                    if cpx_quality < best_cpx_quality:
                        best_cpx_quality = cpx_quality
                        best_cpx = cpx
            good_cpxs = sorted(star_cpx_quality.items(), key=lambda x: x[1])[:self.max_size_star]
            star = {cpx for cpx, quality in good_cpxs}
        return best_cpx

    def count_significance(self, cpx, classified_examples):
        covered_examples = self.get_covered(cpx, classified_examples)
        if covered_examples:
            covered_probs = {key: value / len(covered_examples) for key, value in
                             self.get_covered_classes(covered_examples).items()}
            classified_probs = {key: value / len(classified_examples) for key, value in
                                self.get_covered_classes(classified_examples).items()}
            significance = 0
            for key in self.classes:
                if covered_probs[key] != 0.0:
                    significance += covered_probs[key] * np.log(covered_probs[key] / classified_probs[key])
            return significance * 2
        else:
            return 0

    def count_entropy(self, cpx, classified_examples):
        covered_examples = self.get_covered(cpx, classified_examples)
        covered_probs = {key: value / len(covered_examples) for key, value in
                         self.get_covered_classes(covered_examples).items()}
        entropy = 0
        for key in self.classes:
            if covered_probs[key] != 0.0:
                entropy += covered_probs[key] * np.log2(covered_probs[key])
        return -1 * entropy

    def get_covered_classes(self, covered_examples):
        covered_classes = {cls: 0 for cls in self.classes}
        for example in covered_examples:
            covered_classes[example["class"]] += 1
        return covered_classes

    def specialize_star(self, star):
        new_star = set()
        if star:
            for cpx in star:
                # odfitrowanie, żeby nie powstawał kompleks typu [(0, "1"), (0, "2")]
                cpx_attr_class = [attr[0] for attr in cpx]
                new_attr_selectors = list(filter(lambda attr: not (attr[0] in cpx_attr_class), self.selectors))
                for selector in new_attr_selectors:
                    # frozenset sortuje, żeby nie powstawał kompleksy typu [[(0, "1"), (1, "x")],  [(1, "x"), (0, "1")]]
                    new_cpx = list(cpx) + [selector]
                    new_star.add(frozenset(new_cpx))
        else:
            for selector in self.selectors:
                new_star.add(frozenset([selector]))
        return new_star

    def _get_all_attributes(self):
        # TODO komentarze o funkcjach
        possible_values = [set() for _ in range(len(self.dataset[0]['attributes']))]
        for example in self.dataset:
            for i, attr in enumerate(example["attributes"]):
                possible_values[i].add(attr)

        selectors = []
        for i, attr_values in enumerate(possible_values):
            selectors += [(i, attr_val) for attr_val in attr_values]
        return selectors

    def get_most_common_class(self, covered_examples):
        covered_classes = self.get_covered_classes(covered_examples)
        most_common = sorted(covered_classes.items(), reverse=True, key=lambda x: x[1])[0]
        return most_common

    def get_output(self):
        return self.rules
