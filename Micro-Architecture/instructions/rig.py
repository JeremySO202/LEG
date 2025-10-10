#branch equal

class Rig:
    def __init__(self, _registro1, _registro2, _offset, _procesador):
        self.registro1 = _registro1
        self.registro2 = _registro2
        self.offset = _offset
        self.procesador = _procesador
        self.ejecucion = [self.decode, self.execute, self.memory, self.writeback]
        self.branch_taken = False 
        self.prediction_made = False
    
    def decode(self):
        self.procesador.regRF.data = [None] * 2
        self.procesador.regRF.data[0] = self.procesador.RF.registros[self.registro1]
        self.procesador.regRF.data[1] = self.procesador.RF.registros[self.registro2]
        print(f"valores leídos: {self.procesador.regRF.data}")
    
    def execute(self):
        self.procesador.regALU.data = self.procesador.ALU.operar(self.procesador.regRF.data[0], self.procesador.regRF.data[1], 1)
        self.branch_taken = (self.procesador.regALU.data == 0)
        print(f"comparación: {self.procesador.regALU.data}")
        print(f"Salto: {self.branch_taken}")
        
        instruction_id = id(self)
        predicted_taken = self.procesador.branch_predictor.predict(instruction_id)
        print(f"Predicción fue: {predicted_taken}")
        
        if predicted_taken != self.branch_taken:
            print(f"misprediction")
            print(f"Predicción: {predicted_taken}, Real: {self.branch_taken}")
            
            if not predicted_taken and self.branch_taken:
                print(f"Aplicando salto tardío y limpiando pipeline")
                self.procesador.PC += self.offset - 2  # -2 porque ya avanzó 2 ciclos
                self.procesador.clear_pipeline()
            
            elif predicted_taken and not self.branch_taken:
                print(f"Cancelando salto especulativo y restaurando PC")
                self.procesador.PC -= self.offset
                self.procesador.clear_pipeline()
        else:
            print(f"Predicción correcta")
        
        self.procesador.branch_predictor.update(instruction_id, self.branch_taken)
    
    def memory(self):
        print(f"Sin operación de memoria para rim")
        pass
    
    def writeback(self):
        print(f"Sin writeback para rim")
        pass
    
    def ejecutar(self):
        if self.ejecucion:
            fase = self.ejecucion.pop(0)
            fase()
        else:
            print("No hay más fases para ejecutar en rim")
