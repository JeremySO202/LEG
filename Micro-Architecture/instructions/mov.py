#mov

class Mov:
    def __init__(self, _destino, _inmediato, _procesador):
        self.destino = _destino
        self.inmediato = _inmediato
        self.procesador = _procesador
        self.ejecucion = [self.decode, self.execute, self.memory, self.writeback]
        
    def reset(self):
        self.ejecucion = [self.decode, self.execute, self.memory, self.writeback]
    
    def _load_immediate_value(self):
        # Carga el valor inmediato en regRF
        self.procesador.regRF.data = self.inmediato
    
    def _get_operand_value(self):
        # Obtiene el valor del operando (inmediato)
        return self.procesador.regRF.data
    
    def decode(self):
        print(f"Cargando valor inmediato: {self.inmediato}")
        self._load_immediate_value()
        print(f"Valor inmediato cargado: {self.procesador.regRF.data}")
    
    def execute(self):
        print(f"Moviendo valor inmediato")
        operand_value = self._get_operand_value()
        self.procesador.regALU.data = self.procesador.ALU.operar(operand_value, 0, 0)
        print(f"Valor en ALU: {self.procesador.regALU.data}")
    
    def memory(self):
        print(f"Sin operación de memoria para Mov")
        self.procesador.regDM.data = self.procesador.regALU.data
        print(f"Valor: {self.procesador.regDM.data}")
        
    def writeback(self):
        print(f"Escribiendo valor en L{self.destino}")
        self.procesador.RF.registros[self.destino] = self.procesador.regDM.data
        print(f"L{self.destino} = {self.procesador.RF.registros[self.destino]}")

    def ejecutar(self):
        if self.ejecucion:
            fase = self.ejecucion.pop(0)
            fase()
        else:
            print("No hay más fases para ejecutar en Mov.")






