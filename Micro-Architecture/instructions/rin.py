#salto incondicional
class Rin:
    def __init__(self, _destino, _offset, _procesador):
        self.destino = _destino
        self.offset = _offset
        self.procesador = _procesador
        self.ejecucion = [self.decode, self.execute, self.memory, self.writeback]
        self.return_address = None
   
    def decode(self):
        self.return_address = self.procesador.PC
        print(f"Dirección de retorno: {self.return_address}")
        
        self.procesador.PC += self.offset
        print(f"PC actualizado a {self.procesador.PC}")
        
        self.procesador.clear_pipeline()
   
    def execute(self):
        self.procesador.regALU.data = self.return_address
        print(f"Dirección de retorno: {self.procesador.regALU.data}")
   
    def memory(self):
        self.procesador.regDM.data = self.procesador.regALU.data
        print(f"Valor: {self.procesador.regDM.data}")
   
    def writeback(self):
        self.procesador.RF.registros[self.destino] = self.procesador.regDM.data
        print(f"R{self.destino} = {self.procesador.RF.registros[self.destino]}")
   
    def ejecutar(self):
        if self.ejecucion:
            fase = self.ejecucion.pop(0)
            fase()
        else:
            print("No hay más fases para ejecutar en rim")