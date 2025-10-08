class Boveda:
    def init(self):
        self.llaves = [0]*4  # cada una de 64 bits
        self.hashes_iniciales = [0]*4  # A, B, C, D

    def escribir_llave(self, indice, valor):
        if 0 <= indice < 4:
            self.llaves[indice] = valor

    def escribir_hash(self, indice, valor):
        if 0 <= indice < 4:
            self.hashes_iniciales[indice] = valor

    def leer_llave(self, indice):
        return self.llaves[indice]

    def leer_hash(self, indice):
        return self.hashes_iniciales[indice]