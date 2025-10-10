#load

class Crg:
    def __init__(self, _destino, _inmediato, _fuente, _procesador):
        self.destino = _destino
        self.inmediato = _inmediato
        self.fuente = _fuente
        self.procesador = _procesador
        self.ejecucion = [self.decode, self.execute, self.memory, self.writeback]
        
    def reset(self):
        self.ejecucion = [self.decode, self.execute, self.memory, self.writeback]

    def decode(self):
        print(f"Leyendo registro base R{self.fuente}")
        self.procesador.regRF.data = self.procesador.RF.registros[self.fuente]
        print(f" Valor del registro base: {self.procesador.regRF.data}")
    
    def execute(self):
        print(f"Calculando dirección: R{self.fuente} + {self.inmediato}")
        self.procesador.regALU.data = self.procesador.ALU.operar(self.procesador.regRF.data, self.inmediato, 0)
        print(f" Dirección calculada: {self.procesador.regALU.data}")
    
    def memory(self):
        print(f"Leyendo de memoria[{self.procesador.regALU.data}]")
        
        if self.procesador.DM.datos[self.procesador.regALU.data] == None:
            print(f"En la dirección {self.procesador.regALU.data} no hay dato almacenado")
            self.procesador.regDM.data = 0
        else:
            self.procesador.regDM.data = self.procesador.DM.datos[self.procesador.regALU.data]
        
        print(f" Dato leído: {self.procesador.regDM.data}")
    
    def writeback(self):
        print(f"Escribiendo en R{self.destino}")
        self.procesador.RF.registros[self.destino] = self.procesador.regDM.data
        print(f"R{self.destino} = {self.procesador.RF.registros[self.destino]}")
    
    def ejecutar(self):
        if self.ejecucion:
            fase = self.ejecucion.pop(0)
            fase()
        else:
            print("No hay más fases para ejecutar en LoadWord.")

    def ejecutahyeg(self):
        if self.ejecucion:
            fase = self.ejecucion.pop(0)
            fase()
        else:
            print("No hay más fases para ejecutar en LoadWord.")
