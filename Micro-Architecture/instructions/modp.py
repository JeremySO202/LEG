#multiplicacion immediate

class Modp:
    def __init__(self, _destino, _registro1, _boveda, _procesador):
        self.destino = _destino
        self.registro1 = _registro1
        self.prime = 0xFFFFFFFB 
        self.boveda = _boveda
        self.procesador = _procesador
        self.ejecucion = [self.decode, self.execute, self.memory, self.writeback]
        
    def reset(self):
        self.ejecucion = [self.decode, self.execute, self.memory, self.writeback]
    
    def decode(self):
        print(f"Leyendo registro R{self.registro1}")
        self.procesador.regRF.data = self.procesador.RF.registros[self.registro1]
        print(f"Valor leído: {self.procesador.regRF.data}")
    
    def execute(self):
        print(f"Aplicando modulo de registro e inmediato ({self.prime})")
        if self.procesador.regRF.data is None:
            raise ValueError(f"el Reg {self.registro1} es None y no puede dividirse.")
        if self.boveda:
            print("Usando registro de boveda")
            tempA = self.procesador.vault.get_secure_reg(self.registro1)
            self.procesador.regALU.data = self.procesador.ALU.operar(tempA, self.prime, 9)
        else:
            self.procesador.regALU.data = self.procesador.ALU.operar(
                self.procesador.regRF.data, self.prime, 9)
        print(f"Modulo - ALU: {self.procesador.regALU.data}")
    
    def memory(self):
        print(f"Sin operación de memoria para Modp")
        self.procesador.regDM.data = self.procesador.regALU.data
    
    def writeback(self):
        print(f"Escribiendo resultado en R{self.destino}")
        self.procesador.RF.registros[self.destino] = self.procesador.regDM.data
        print(f"R{self.destino} = {self.procesador.RF.registros[self.destino]}")
    
    def ejecutar(self):
        if self.ejecucion:
            fase = self.ejecucion.pop(0)
            fase()
        else:
            print("No hay más fases para ejecutar en Modp.")