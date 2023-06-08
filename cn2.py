import copy
import numpy as np

class CN2:
    def __init__(self, dataset, min_significance=0.4, max_size_star=3):
        self.dataset = dataset
        self.selectors = self._get_all_attributes()
        self.classes = set(example["class"] for example in self.dataset)
        self.min_significance = min_significance
        self.max_size_star = max_size_star

    def get_highest_quality_complex(self):
        rules = []
        classified_examples = copy.deepcopy(self.dataset)
        best_cpx = ()
        while best_cpx is not None:
            best_cpx = self.find_best_complex(classified_examples)
            if best_cpx is not None:
                covered_examples = self.get_covered(best_cpx, classified_examples)
                classified_examples = [element for element in classified_examples if element not in covered_examples]
                common_class = self.get_most_common_class(covered_examples)
                rules += (best_cpx, common_class)
        return rules

    def find_best_complex(self, classified_examples):
        star = {()}
        best_cpx = None
        best_cpx_quality = float('inf')
        while len(star) != 0:
            new_star = self.specialize_star(star)
            star_complex_quality = {}
            for complex in new_star:
                complex_significance = self.count_significance(complex, classified_examples)
                if complex_significance > self.min_significance:
                    complex_quality = self.count_entropy(complex, classified_examples)
                    star_complex_quality[complex] = complex_quality
                    if complex_quality < best_cpx_quality:
                        best_cpx_quality = complex_quality
                        best_cpx = complex
            good_cpxs = sorted(star_complex_quality.items(), key=lambda x: x[1])[:self.max_size_star]
            star = {complex for complex, quality in good_cpxs}
        return best_cpx

    def count_significance(self, complex, classified_examples):
        covered_examples = self.get_covered(complex, classified_examples)
        if covered_examples:
            covered_probs = {key: value/len(covered_examples) for key, value in self.get_covered_classes(covered_examples).items()}
            classified_probs = {key: value/len(classified_examples) for key, value in self.get_covered_classes(classified_examples).items()}
            significance = 0
            for key in self.classes:
                if covered_probs[key] != 0.0:
                    significance += covered_probs[key] * np.log(covered_probs[key]/classified_probs[key])
            return significance * 2
        else:
            return 0

    def count_entropy(self, complex, classified_examples):
        covered_examples = self.get_covered(complex, classified_examples)
        covered_probs = {key: value / len(covered_examples) for key, value in self.get_covered_classes(covered_examples).items()}
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

    def get_covered(self, complex, classified_examples):
        return [example for example in classified_examples if all([example["attributes"][attr[0]] == attr[1] for attr in complex])]

    def specialize_star(self, star):
        new_star = set()
        if star:
            for complex in star:
                # odfitrowanie, żeby nie powstawał kompleks typu [(0, "1"), (0, "2")]
                complex_attr_class = [attr[0] for attr in complex]
                new_attr_selectors = list(filter(lambda attr: not (attr[0] in complex_attr_class), self.selectors))
                for selector in new_attr_selectors:
                    # frozenset sortuje, żeby nie powstawał kompleksy typu [[(0, "1"), (1, "x")],  [(1, "x"), (0, "1")]]
                    new_complex = list(complex) + [selector]
                    new_star.add(frozenset(new_complex))
        else:
            for selector in self.selectors:
                new_star.add(frozenset([selector]))
        return new_star

    def _get_all_attributes(self):
        possible_values = [set() for i in range(len(self.dataset[0]['attributes']))]
        for example in self.dataset:
            for i, attr in enumerate(example["attributes"]):
                possible_values[i].add(attr)

        selectors = []
        for i, attr_values in enumerate(possible_values):
            selectors += [(i, attr_val) for attr_val in attr_values]
        return selectors

    def get_best_complex_with_measures(self, dataset):
        return None, 1, 1, 1, 1

    def get_most_common_class(self, covered_examples):
        covered_classes = self.get_covered_classes(covered_examples)
        most_common = sorted(covered_classes.items(), reverse=True, key=lambda x: x[1])[0]
        return most_common

