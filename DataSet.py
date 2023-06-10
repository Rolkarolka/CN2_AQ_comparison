import csv
import copy


class DataSet:
    def __init__(self, csv_path):
        """
        Wczytuje dane z pliku csv_path, którego format powinien wyglądać:
        atr1, atr2, atr3, ..., atrN, klasa
        """
        self.dataSet = []
        with open(csv_path) as csv_file:
            spamreader = csv.reader(csv_file, delimiter=',')
            for row in spamreader:
                attributes = [row[i] for i in range(0, len(row) - 1)]
                self.dataSet.append({"attributes": copy.deepcopy(attributes), "class": row[-1]})

    def get_set_with_known_attributes(self):
        new_dataset = []
        for record in self.dataSet:
            if not ("?" in record["attributes"]):
                new_dataset.append(record)
        self.dataSet = new_dataset

    def __getitem__(self, key):
        return self.dataSet[key]

    def __len__(self):
        return len(self.dataSet)

    def __setitem__(self, key, value):
        self.dataSet[key] = value

    def __str__(self):
        return str(self.dataSet)

    def scale_attributes(self, factor):
        for example in self.dataSet:
            example['attributes'] = example['attributes'] * factor
    
    def scale_examples(self, factor):
        self.dataSet = self.dataSet * factor
