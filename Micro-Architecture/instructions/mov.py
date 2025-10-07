#mov

class Mov:
    def __init__(self, _destino, _inmediato, _procesador):
        self.destino = _destino
        self.inmediato = _inmediato
        self.procesador = _procesador
        self.ejecucion = [self.decode, self.execute, self.memory, self.writeback]
    
    def decode(self):
        print(f"Preparando inmediato: {self.inmediato}")
        self.procesador.regRF.data = self.inmediato
        print(f" Valor inmediato: {self.procesador.regRF.data}")
    
    def execute(self):
        print(f"Pasando inmediato a través de ALU")
        self.procesador.regALU.data = self.procesador.ALU.operar(self.procesador.regRF.data, 0, 0)
        print(f" Valor en ALU: {self.procesador.regALU.data}")
    
    def memory(self):
        print(f"Pasando valor a etapa de memoria")
        self.procesador.regDM.data = self.procesador.regALU.data
        print(f" Valor: {self.procesador.regDM.data}")
    
    def writeback(self):
        print(f"Escribiendo inmediato en R{self.destino}")
        self.procesador.RF.registros[self.destino] = self.procesador.regDM.data
        print(f"R{self.destino} = {self.procesador.RF.registros[self.destino]}")
    
    def ejecutar(self):
        if self.ejecucion:
            fase = self.ejecucion.pop(0)
            fase()
        else:
            print("No hay más fases para ejecutar en Mov.")






