#Generar firma   FRM rd, rs1, index (Registro destino, registro con hash, indice de la llave) = (A XOR K)

class Frm:
    def __init__(self, _destino, _registro1, _indice, _procesador):
        self.destino = _destino
        self.registro1 = _registro1
        self.indice = _indice
        self.procesador = _procesador
        self.ejecucion = [self.decode, self.execute, self.memory, self.writeback]
        
    def reset(self):
        self.ejecucion = [self.decode, self.execute, self.memory, self.writeback]
    
    def decode(self):
        print(f"Leyendo registros R{self.registro1}")
        self.procesador.regRF.data = None
        self.procesador.regRF.data = self.procesador.RF.registros[self.registro1]
        print(f"Valores leídos: {self.procesador.regRF.data}")
    
    def execute(self):
        print(f"Firmando bloque")
        print(self.procesador.regRF.data)
        self.procesador.regALU.data = self.procesador.ALU.operar(self.procesador.regRF.data, self.procesador.vault.get_secure_reg(self.indice), 7)
        print(f"Resultado ALU: {self.procesador.regALU.data}")
    
    def memory(self):
        print(f"Sin operación de memoria para Frm")
        self.procesador.regDM.data = self.procesador.regALU.data
    
    def writeback(self):
        print(f"Escribiendo resultado en L{self.destino}")
        self.procesador.RF.registros[self.destino] = self.procesador.regDM.data
        print(f"L{self.destino} = {self.procesador.RF.registros[self.destino]}")
       
    def ejecutar(self):
        if self.ejecucion:
            fase = self.ejecucion.pop(0)
            fase()
        else:
            print("No hay más fases para ejecutar en Frm.")
