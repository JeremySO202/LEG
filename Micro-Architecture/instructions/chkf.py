#Comparar firma  CHKF rd, rs1, rs2 (registro destino, la calculada, la extraida del doc)
# Compara 1 solo bloque desde registro

class Chkf:
    def __init__(self, _destino, _registro1, _registro2, _bovedareg1, _bovedareg2, _procesador):
        self.destino = _destino
        self.registro1 = _registro1
        self.registro2 = _registro2
        self.bovedareg1 = _bovedareg1
        self.bovedareg2 = _bovedareg2 
        self.procesador = _procesador
        self.ejecucion = [self.decode, self.execute, self.memory, self.writeback]
    
    def decode(self):
        print(f"Leyendo registros R{self.registro1} y R{self.registro2}")
        self.procesador.regRF.data = [None] * 2
        self.procesador.regRF.data[0] = self.procesador.RF.registros[self.registro1]
        self.procesador.regRF.data[1] = self.procesador.RF.registros[self.registro2]
        print(f"Valores leídos: {self.procesador.regRF.data}")
    
    def execute(self):
        print(f"Comparando firma")
        if self.bovedareg1 or self.bovedareg2:
            print("Usando registros de boveda")
            tempA = self.procesador.vault.get_secure_reg(self.registro1) if self.bovedareg1 else self.procesador.RF.registros[self.registro1]
            tempB = self.procesador.vault.get_secure_reg(self.registro2) if self.bovedareg2 else self.procesador.RF.registros[self.registro2]
            self.procesador.regALU.data = self.procesador.ALU.operar(tempA, tempB, 13)
        else:
            self.procesador.regALU.data = self.procesador.ALU.operar(self.procesador.regRF.data[0], self.procesador.regRF.data[1], 13)
        print(f"Resultado ALU: {self.procesador.regALU.data}")
    
    def memory(self):
        print(f"Sin operación de memoria para Chkf")
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
            print("No hay más fases para ejecutar en Chkf.")
