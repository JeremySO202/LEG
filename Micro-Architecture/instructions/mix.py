#non linear mix
# uint64_t f = (A & B) | (~A & C);
# suma
class Mix:
    def __init__(self, _destino, _registro1, _registro2, _registro3, _boveda, _procesador):
        self.destino = _destino
        self.registro1 = _registro1
        self.registro2 = _registro2
        self.registro3 = _registro3
        self.boveda = _boveda
        self.procesador = _procesador
        self.ejecucion = [self.decode, self.execute, self.memory, self.writeback]
        
    def reset(self):
        self.ejecucion = [self.decode, self.execute, self.memory, self.writeback]
    
    def decode(self):
        print(f"Leyendo registros R{self.registro1}, R{self.registro2} y R{self.registro3}")
        self.procesador.regRF.data = [None] * 3
        self.procesador.regRF.data[0] = self.procesador.RF.registros[self.registro1]
        self.procesador.regRF.data[1] = self.procesador.RF.registros[self.registro2]
        self.procesador.regRF.data[2] = self.procesador.RF.registros[self.registro3]
        print(f"Valores leídos: {self.procesador.regRF.data}")
    
    def execute(self):
        print(f"Mezclando valores")
        if self.boveda:
            print("Usando registros de boveda")
            tempA = self.procesador.vault.get_secure_reg(self.registro1)
            tempB = self.procesador.vault.get_secure_reg(self.registro2)
            tempC = self.procesador.vault.get_secure_reg(self.registro3)
            self.procesador.regALU.data = self.procesador.ALU.operar(A=tempA, B=tempB, op=10, C=tempC)
        else:
            self.procesador.regALU.data = self.procesador.ALU.operar(A=self.procesador.regRF.data[0], B=self.procesador.regRF.data[1], op=10, C=self.procesador.regRF.data[2])
        print(f"Resultado ALU: {self.procesador.regALU.data}")
    
    def memory(self):
        print(f"Sin operación de memoria para Mix")
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
            print("No hay más fases para ejecutar en Sma.")
