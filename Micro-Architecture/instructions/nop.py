#nop- no operation

class Nop:
    def __init__(self, _procesador):
        self.procesador = _procesador
        self.ejecucion = [self.decode, self.execute, self.memory, self.writeback]
        
    def reset(self):
        self.ejecucion = [self.decode, self.execute, self.memory, self.writeback]
    
    def decode(self):
        print(f"Leyendo valores 0 y 0")
        self.procesador.regRF.data = [None] * 2
        self.procesador.regRF.data[0] = 0
        self.procesador.regRF.data[1] = 0
        print(f"Valores leídos: {self.procesador.regRF.data}")
    
    def execute(self):
        print(f"Sin operación de execute para Nop")
    
    def memory(self):
        print(f"Sin operación de memoria para Nop")
    
    def writeback(self):
        print(f"Sin operación de memoria para Nop")
       
    def ejecutar(self):
        if self.ejecucion:
            fase = self.ejecucion.pop(0)
            fase()
        else:
            print("No hay más fases para ejecutar en Nop.")
