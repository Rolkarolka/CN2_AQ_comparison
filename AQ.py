import random
import copy

from Complex import Complex


class AQ:
    def __init__(self, T, m):
        """
        T - zbiór wszystkich przykładów
        m - liczba najlepszych wybieranych z G kompleksów
        self.R - zbiór przykładów niepokrytych
        self.G - zbiórmaksymalnie ogólnych modeli w H
        self.x_s - ziarno wybrane spośród zbioru przykładów niepokrytych self.R
        self.R_1 - zbiór przykładów ze zbioru przykładów niepokrytych, których klasa jest zgodna z klasą ziarna x_s
        self.R_0 - zbiór przykładów ze zbioru przykładów niepokrytych, których klasa jest niezgodna z klasą ziarna x_s
        """
        self.m = m
        self.R = T
        all_attributes = self._get_all_attributes()
        self.G = [Complex(all_attributes)]
        self.x_s = random.choice(self.R)
        self.R_1, self.r_0 = self._get_subsets(self.R)
        self.bestV = -1
        self.bestComplex = Complex(all_attributes)

    def _get_all_attributes(self):
        """
        Wyznacza wszystkie możliwe wartości atrybutu na potrzeby stworzenia pierwszego kompleksu uniwersalnego
        """
        all_attributes = [set() for _ in range(0, len(self.R[0]["attributes"]))]
        for example in self.R:
            for i in range(0, len(example["attributes"])):
                all_attributes[i].add(copy.deepcopy(example["attributes"][i]))
        return all_attributes

    def _get_subsets(self, R):
        """
        Dzieli zbiór przykładów niepokrytych na dwa podzbiory w zależności od klasy ziarna
        """
        r_0 = []
        r_1 = []
        for example in R:
            if example["class"] == self.x_s["class"]:
                r_1.append(copy.deepcopy(example))
            else:
                r_0.append(copy.deepcopy(example))
        return r_1, r_0

    def process(self):
        """
        Główna pętla algorytmu. Wyznacza najlepszej jakości regułę decyzją w oparciu o dostarczony zbiór danych.
        """
        r_0_g = self._filter_subset(self.r_0)
        while len(r_0_g) != 0:
            x_n = random.choice(r_0_g)
            self._specialization(x_n)
            self._create_max_general_g()
            self.G = self._get_max_quality_complexes(self.m)
            r_0_g = self._filter_subset(self.r_0)
        max_quality_complexes = self._get_max_quality_complexes(1)
        if not max_quality_complexes:
            print("Brak kompleksów w zbiorze")
            return None
        else:
            return max_quality_complexes

    def _filter_subset(self, set):
        """
        Filtruje dany zbiór i zwraca tylko te przykłady, które spełniają co najmniej jeden kompleks ze zbioru G.
        Używany do wyznaczenia zbioru R_0_G, którego długość stanowi kryterium zatrzymania.
        """
        filtred_subset = []
        for example in set:
            for complex in self.G:
                if complex.check(example["attributes"]):
                    filtred_subset.append(example)
                    break
        return filtred_subset

    def _specialization(self, x_n):
        """
        Dla wszystkich k ∈ {k' ∈ G | k' pokrywające x_n}:
            G := G − {k} ∪ specjalizacja(k, x_n, x_s);
        """
        K = []
        for k in self.G:
            if k.check(x_n["attributes"]):
                K.append(k)
        for k in K:
            self.G.remove(k)
            self.G += k.specialize(x_n, self.x_s)

    def _create_max_general_g(self):
        """
        G := G − {k ∈ G | (∃k' ∈ G) k' jest bardziej ogólne od k}
        """
        K_to_remove = set()
        for k in self.G:
            for k_prim in self.G:
                if k != k_prim:
                    if k.is_specialized(k_prim):
                        K_to_remove.add(k)
        for k in K_to_remove:
            self.G.remove(k)

    def _get_error_measures(self, complex, dataset):
        """
        Liczy miary macierzy pomyłek dla podanego kompleksu
        miary to: dokładnosć, precyzja, swoistość oraz czułość.
        """
        P, N = self._get_subsets(dataset)

        tp = 0
        tn = 0
        fp = 0
        fn = 0
        for example in P:
            if complex.check(example["attributes"]):
                tp += 1
            else:
                fn += 1
        for example in N:
            if not complex.check(example["attributes"]):
                tn += 1
            else:
                fp += 1
        accuracy = (tp + tn) / len(dataset)
        if tp + fp == 0:
            precision = None
        else:
            precision = tp / (tp + fp)
        specificity = tn / len(N)
        sensitivity = tp / len(P)
        return accuracy, precision, specificity, sensitivity

    def get_best_complex_with_measures(self, dataset):
        acc, prec, spec, sens = self._get_error_measures(self.bestComplex, dataset)
        print("Dokładność: ", acc)
        print("Precyzja: ", prec)
        print("Swoistość: ", spec)
        print("Czułość: ", sens)
        return acc, prec, spec, sens
    # TODO metryki dla klasyfikacji wieloklasowej

    def _v(self, complex):
        """
        Funkcja jakości - suma pokrytych przykładów o klasie zgodnej z klasą ziarna 
        i suma przykładów niepokrytych o klasie niezgodnej z klasą ziarna
        """
        v = 0
        for example in self.R_1:
            if complex.check(example["attributes"]):
                v += 1
        for example in self.r_0:
            if not complex.check(example["attributes"]):
                v += 1

        if v > self.bestV:
            self.bestV = v
            self.bestComplex = complex
        return v

    def _get_max_quality_complexes(self, m):
        """
        G := Arg^m max_k∈G v_R(1),R(0) (k);
        """
        quality_G = {(complex, self._v(complex)) for complex in self.G}
        G = []
        for _ in range(0, min(m, len(quality_G))):
            max_quality = 0
            max_quality_complex = None
            for complex, quality in quality_G:
                if quality >= max_quality:
                    max_quality = quality
                    max_quality_complex = complex
            G.append(copy.deepcopy(max_quality_complex))
            quality_G.remove((max_quality_complex, max_quality))
        print()
        return G
