import copy


class Complex:
    def __init__(self, allAttributes):
        self.complex = allAttributes

    def __getitem__(self, key):
        return self.complex[key]

    def __len__(self):
        return len(self.complex)

    def __str__(self):
        return str(self.complex)

    def check(self, attributes_example):
        """
        Sprawdza, czy kompleks pokrywa podane atrybuty.
        """
        for attr_complex, attr_example in zip(self.complex, attributes_example):
            cover_attr = False
            for single_attr_complex in attr_complex:
                if single_attr_complex == attr_example:
                    cover_attr = True
            if not cover_attr:
                return False
        return True

    def specialize(self, x_n, x_s):
        """
        Zwraca listę (zbiór)  maksymalnie ogólnych kompleksów k' takich, że k' jest bardziej szczegółowe
        od self.complex,
        k' nie pokrywa x_n, ale pokrywa x_s
        """
        specialized_complexes = []
        for i in range(0, len(x_n["attributes"])):
            if x_n["attributes"][i] != x_s["attributes"][i]:
                specialized_complex = Complex(copy.deepcopy(self.complex))
                specialized_complex[i].remove(x_n["attributes"][i])
                specialized_complexes.append(copy.deepcopy(specialized_complex))
        return specialized_complexes

    def is_specialized(self, k_prim):
        """
        Sprawdza, czy self.complex jest bardziej szczegółowe od k_prim.
        """
        for i in range(0, len(k_prim)):
            if not self.complex[i].issubset(k_prim[i]):
                return False
        return True
