class Aut:
    # Aut Rd Rs1 (destino contraseña)
    def __init__(self, _destino, _registro1,  _procesador):
        self.destino = _destino
        self.registro1 = _registro1
        self.procesador = _procesador
        self.ejecucion = [self.decode, self.execute, self.memory, self.writeback]
        
    def reset(self):
        self.ejecucion = [self.decode, self.execute, self.memory, self.writeback]
    
    def decode(self):
        print(f"Leyendo registro R{self.registro1}")
        self.procesador.regRF.data = self.procesador.RF.registros[self.registro1]
        print(f"Valor leído: {self.procesador.regRF.data}")
    
    def execute(self):
        print(f"Verificando contraseña")
        if self.procesador.regRF.data is None:
            raise ValueError(f"el Reg {self.registro1} es None y no puede verificarse.")
        
        print("Usando registro de boveda")
        password = self.procesador.vault.get_password()
        self.procesador.regALU.data = self.procesador.ALU.operar(self.procesador.regRF.data, password, 13)
        print(f"Verificación - ALU: {self.procesador.regALU.data}")
    
    def memory(self):
        print(f"Sin operación de memoria para Aut")
        self.procesador.regDM.data = self.procesador.regALU.data
    
    def writeback(self):
        print(f"Escribiendo resultado en R{self.destino}")
        self.procesador.vault.write_authorization(self.procesador.regDM.data)
        print(f"R{self.destino} = {self.procesador.vault.is_authenticated()}")
    
    def ejecutar(self):
        if self.ejecucion:
            fase = self.ejecucion.pop(0)
            fase()
        else:
            print("No hay más fases para ejecutar en Aut.")
