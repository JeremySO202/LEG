#save

class Grd:
    def __init__(self, _fuente, _inmediato, _destino, _procesador):
        self.destino = _destino
        self.inmediato = _inmediato
        self.fuente = _fuente
        self.procesador = _procesador
        self.ejecucion = [self.decode, self.execute, self.memory, self.writeback]
    
    def reset(self):
        """Reinicia la lista de ejecución para poder ejecutar la instrucción nuevamente"""
        self.ejecucion = [self.decode, self.execute, self.memory, self.writeback]
    
    def decode(self):
        print(f"Leyendo valor a almacenar desde R{self.fuente}")
        self.procesador.regRF.data = [None, None]
        # En RF.data[0] guardamos el valor a almacenar
        self.procesador.regRF.data[0] = self.procesador.RF.registros[self.fuente]
        # En RF.data[1] guardamos el registro base para calcular dirección
        self.procesador.regRF.data[1] = self.procesador.RF.registros[self.destino]
        print(f" Valor a almacenar: {self.procesador.regRF.data[0]}")
        print(f" Registro base: {self.procesador.regRF.data[1]}")
    
    def execute(self):
        print(f"Calculando dirección: R{self.destino} + {self.inmediato}")
        # Calculamos la dirección de memoria
        direccion = self.procesador.ALU.operar(self.procesador.regRF.data[1], self.inmediato, 0)
        # Guardamos [dirección, valor_a_almacenar]
        self.procesador.regALU.data = [direccion, self.procesador.regRF.data[0]]
        print(f" Dirección calculada: {self.procesador.regALU.data[0]}")
    
    def memory(self):
        print(f"Almacenando en memoria[{self.procesador.regALU.data[0]}]")
        self.procesador.DM.datos[self.procesador.regALU.data[0]] = self.procesador.regALU.data[1]
        self.procesador.regDM.data = self.procesador.regALU.data[1]
        print(f" Dato almacenado: {self.procesador.regDM.data}")
    
    def writeback(self):
        print(f"StoreWord completado")
    
    def ejecutar(self):
        if self.ejecucion:
            fase = self.ejecucion.pop(0)
            fase()
        else:
            print("No hay más fases para ejecutar en StoreWord.")
