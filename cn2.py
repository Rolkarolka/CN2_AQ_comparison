import copy
import numpy as np


class CN2:
    def __init__(self, dataset, min_significance=0.4, max_size_star=3):
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

    def get_covered(self, cpx, classified_examples):
        return [example for example in classified_examples if
                all([example["attributes"][attr[0]] == attr[1] for attr in cpx])]

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

    def evaluate(self, test_dataset):
        classified_examples = copy.deepcopy(test_dataset)
        confusion_values = self._get_confusion_values(self._get_confusion_matrix(classified_examples))
        accuracy = self._get_accuracy(confusion_values)
        precision = self._get_macro_avg_precision(confusion_values)
        recall = self._get_macro_avg_recall(confusion_values)
        f1 = self._get_f1_score(confusion_values)
        return accuracy, precision, recall, f1

    def _get_accuracy(self, confusion_values):
        accuracy = 0
        for _, v in confusion_values.items():
            accuracy += (v["tp"] + v["tn"]) / (v["tp"] + v["tn"] + v["fp"] + v["fn"])
        return accuracy / len(self.classes)

    def _get_macro_avg_precision(self, confusion_values):
        precision = 0
        for _, v in confusion_values.items():
            precision += v["tp"]/(v["tp"]+v["fp"])
        return precision / len(self.classes)

    def _get_macro_avg_recall(self, confusion_values):
        recall = 0
        for _, v in confusion_values.items():
            recall += v["tp"]/(v["tp"]+v["fn"])
        return recall / len(self.classes)

    def _get_confusion_matrix(self, classified_examples):
        confusion_matrix = {key: {cls: 0 for cls in self.classes} for key in self.classes}
        for rule, (common_class, _) in self.rules:
            covered_examples = self.get_covered(rule, classified_examples)
            for example in covered_examples:
                confusion_matrix[example["class"]][common_class] += 1
            classified_examples = [element for element in classified_examples if element not in covered_examples]
        return confusion_matrix

    def _get_confusion_values(self, confusion_matrix):
        confusion_values = {key: {} for key in self.classes}
        for cls in self.classes:
            confusion_values[cls]["tp"] = confusion_matrix[cls][cls]
            confusion_values[cls]["tn"] = sum(
                [sum([confusion_matrix[c][x] for x in self.classes if x != cls]) for c in self.classes if c != cls])
            confusion_values[cls]["fp"] = sum([confusion_matrix[c][cls] for c in self.classes if c != cls])
            confusion_values[cls]["fn"] = sum([confusion_matrix[cls][c] for c in self.classes if c != cls])
        return confusion_values

    def _get_f1_score(self, confusion_values):
        f1_score = 0
        for _, v in confusion_values.items():
            precision = round(v["tp"]/(v["tp"]+v["fp"]), 2)
            recall = round(v["tp"]/(v["tp"]+v["fn"]), 2)
            f1_score += (2 * precision * recall) / (recall + precision)
        return f1_score / len(self.classes)
