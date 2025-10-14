#Guardar llave   GRDK index, rs1

class Grdk:
    def __init__(self, _fuente, _destino, _procesador):
        self.destino = _destino
        self.fuente = _fuente
        self.procesador = _procesador
        self.ejecucion = [self.decode, self.execute, self.memory, self.writeback]
    
    def reset(self):
        self.ejecucion = [self.decode, self.execute, self.memory, self.writeback]
    
    def decode(self):    
        print(f"Leyendo valor a almacenar desde L{self.fuente}")
        self.procesador.regRF.data = [None, None]
        # En RF.data[0] guardamos el valor a almacenar
        self.procesador.regRF.data[0] = self.procesador.RF.registros[self.fuente]
        # En RF.data[1] guardamos el registro base para calcular dirección
        self.procesador.regRF.data[1] = self.destino
        print(f"Valor a almacenar: {self.procesador.regRF.data[0]}")
        
    def execute(self):
        # vault does not require an offset, only direct access allowed
        self.procesador.regALU.data = self.procesador.regRF.data
        print(f"Sin operación de execute para Grdk")
    
    def memory(self):
        print(self.procesador.regALU.data)
        self.procesador.regDM.data = self.procesador.regALU.data
        print(f"Sin operación de memoria para Grdk")
    
    def writeback(self):
        print(f"Escribiendo resultado en V{self.destino} = {self.procesador.regDM.data}")
        self.procesador.vault.write_secure_reg(self.destino, self.procesador.regDM.data)
        print(f"V{self.destino} = {self.procesador.vault.get_secure_reg(self.destino)}")
       
    def ejecutar(self):
        if self.ejecucion:
            fase = self.ejecucion.pop(0)
            fase()
        else:
            print("No hay más fases para ejecutar en Grdk")
