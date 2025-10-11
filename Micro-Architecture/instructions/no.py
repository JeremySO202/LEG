#not 

class No:
    def __init__(self, _destino, _registro, _boveda, _procesador):
        self.destino = _destino
        self.registro = _registro
        self.boveda = _boveda
        self.procesador = _procesador
        self.ejecucion = [self.decode, self.execute, self.memory, self.writeback]
        
    def reset(self):
        self.ejecucion = [self.decode, self.execute, self.memory, self.writeback]
    
    def _read_register(self):
        """Lee el registro fuente y lo almacena en regRF"""
        self.procesador.regRF.data = self.procesador.RF.registros[self.registro]
    
    def _get_operand_value(self):
        """Obtiene el valor del operando considerando registros de bóveda"""
        if self.boveda:
            return self.procesador.vault.get_secure_reg(self.registro)
        else:
            return self.procesador.regRF.data
    
    def decode(self):
        print(f"Leyendo registro R{self.registro}")
        self._read_register()
        print(f"Valor leído: {self.procesador.regRF.data}")
    
    def execute(self):
        print(f"Aplicando NOT a registro")
        if self.procesador.regRF.data is None:
            raise ValueError(f"el Reg {self.registro} es None y no puede aplicarse NOT.")
        
        if self.boveda:
            print("Usando registro de boveda")
        
        operand_value = self._get_operand_value()
        self.procesador.regALU.data = self.procesador.ALU.operar(operand_value, 0, 7)
        print(f"Resultado ALU: {self.procesador.regALU.data}")
    
    def memory(self):
        print(f"Sin operación de memoria para No")
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
            print("No hay más fases para ejecutar en No.")