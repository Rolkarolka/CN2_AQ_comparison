import copy


class Algorithm:
    def __init__(self):
        self.classes = []
        self.rules = []

    def get_covered(self, cpx, classified_examples):
        return [example for example in classified_examples if
                all([example["attributes"][attr[0]] == attr[1] for attr in cpx])]

    def evaluate(self, test_dataset):
        classified_examples = copy.deepcopy(test_dataset)
        confusion_values = self._get_confusion_values(self._get_confusion_matrix(classified_examples))
        accuracy = self._get_accuracy(confusion_values)
        precision = self._get_macro_avg_precision(confusion_values)
        recall = self._get_macro_avg_recall(confusion_values)
        f1 = self._get_macro_f1_score(precision, recall)
        return accuracy, precision, recall, f1

    def _get_accuracy(self, confusion_values):
        accuracy = 0
        for _, v in confusion_values.items():
            denominator = v["tp"] + v["tn"] + v["fp"] + v["fn"]
            if denominator != 0:
                accuracy += (v["tp"] + v["tn"]) / denominator
        return accuracy / len(self.classes)

    def _get_macro_avg_precision(self, confusion_values):
        precision = 0
        for _, v in confusion_values.items():
            denominator = v["tp"] + v["fp"]
            if denominator != 0:
                precision += v["tp"] / denominator
        return precision / len(self.classes)

    def _get_macro_avg_recall(self, confusion_values):
        recall = 0
        for _, v in confusion_values.items():
            denominator = (v["tp"] + v["fn"])
            if denominator != 0:
                recall += v["tp"] / denominator
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

    def _get_macro_f1_score(self, macro_avg_precision, macro_avg_recall):
        return (2 * macro_avg_precision * macro_avg_recall) / (macro_avg_recall + macro_avg_precision)
