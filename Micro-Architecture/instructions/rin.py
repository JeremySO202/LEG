#salto inconicional 

class RIN:
    def __init__(self, _destino, _offset, _procesador):
        self.destino = _destino
        self.offset = _offset
        self.procesador = _procesador

        self.ejecucion = [self.etapa1]

    def etapa1(self):

        self.procesador.RF.registros[self.destino] = self.procesador.PC + 4
        print(f"Guardando {self.procesador.PC + 4} en registro {self.destino}")

        self.procesador.PC += self.offset
        print(f"PC actualizado a {self.procesador.PC}")

        self.procesador.clear_pipeline()

    def ejecutar(self):
        if self.ejecucion:
            fase = self.ejecucion.pop(0)
            fase()
        else:
            print("No hay más fases para ejecutar en Rama Incondicional.")