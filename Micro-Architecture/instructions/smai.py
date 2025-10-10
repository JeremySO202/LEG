# suma con inmediato
class Smai:
    def __init__(self, _destino, _registro1, _inmediate, _boveda, _procesador):
        self.destino = _destino
        self.registro1 = _registro1
        self.inmediate = _inmediate
        self.boveda = _boveda
        self.procesador = _procesador
        self.ejecucion = [self.decode, self.execute, self.memory, self.writeback]
    
    def reset(self):
        """Reinicia la lista de ejecución para poder ejecutar la instrucción nuevamente"""
        self.ejecucion = [self.decode, self.execute, self.memory, self.writeback]
    
    def decode(self):
        print(f"Leyendo registro R{self.registro1}")
        self.procesador.regRF.data = self.procesador.RF.registros[self.registro1]
        print(f"Valor leído: {self.procesador.regRF.data}")
    
    def execute(self):
        print(f"Sumando registro + inmediato ({self.inmediate})")
        if self.procesador.regRF.data is None:
            raise ValueError(f"el Reg {self.registro1} es None y no puede sumarse.")
        if self.boveda:
            print("Usando registro de boveda")
            tempA = self.procesador.vault.get_secure_reg(self.registro1)
            self.procesador.regALU.data = self.procesador.ALU.operar(tempA, self.inmediate, 0)
        else:
            # Si regRF.data es una lista, tomar el primer elemento, si no, usar el valor directamente
            if isinstance(self.procesador.regRF.data, list):
                valor = self.procesador.regRF.data[0] if self.procesador.regRF.data else 0
            else:
                valor = self.procesador.regRF.data
            self.procesador.regALU.data = self.procesador.ALU.operar(valor, self.inmediate, 0)
        print(f"Resultado ALU: {self.procesador.regALU.data}")
    
    def memory(self):
        print(f"Sin operación de memoria para SmaI")
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
            print("No hay más fases para ejecutar en Smai.")