#load

class Crg:
    def __init__(self, _destino, _inmediato, _fuente, _procesador):
        self.destino = _destino
        self.inmediato = _inmediato
        self.fuente = _fuente
        self.procesador = _procesador
        self.ejecucion = [self.decode, self.execute, self.memory, self.writeback]
        
    def reset(self):
        self.ejecucion = [self.decode, self.execute, self.memory, self.writeback]

    def _read_base_register(self):
        """Lee el registro base para calcular la dirección"""
        self.procesador.regRF.data = self.procesador.RF.registros[self.fuente]
    
    def _calculate_address(self):
        """Calcula la dirección de memoria sumando base + offset"""
        return self.procesador.ALU.operar(self.procesador.regRF.data, self.inmediato, 0)
    
    def _read_memory_data(self, address):
        """Lee el dato de la memoria en la dirección especificada"""
        if self.procesador.DM.datos[address] == None:
            print(f"En la dirección {address} no hay dato almacenado")
            return 0
        else:
            return self.procesador.DM.datos[address]

    def decode(self):
        print(f"Leyendo registro base R{self.fuente}")
        self._read_base_register()
        print(f"Valor del registro base: {self.procesador.regRF.data}")
    
    def execute(self):
        print(f"Calculando dirección: R{self.fuente} + {self.inmediato}")
        self.procesador.regALU.data = self._calculate_address()
        print(f"Dirección calculada: {self.procesador.regALU.data}")
    
    def memory(self):
        print(f"Leyendo de memoria[{self.procesador.regALU.data}]")
        self.procesador.regDM.data = self._read_memory_data(self.procesador.regALU.data)
        print(f"Dato leído: {self.procesador.regDM.data}")
    
    def writeback(self):
        print(f"Escribiendo en R{self.destino}")
        self.procesador.RF.registros[self.destino] = self.procesador.regDM.data
        print(f"R{self.destino} = {self.procesador.RF.registros[self.destino]}")
    
    def ejecutar(self):
        if self.ejecucion:
            fase = self.ejecucion.pop(0)
            fase()
        else:
            print("No hay más fases para ejecutar en Crg.")
