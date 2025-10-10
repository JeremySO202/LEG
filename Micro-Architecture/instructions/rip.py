#branch menor igual
class Rip:
    def __init__(self, _registro1, _registro2, _offset, _procesador):
        self.registro1 = _registro1
        self.registro2 = _registro2
        self.offset = _offset
        self.procesador = _procesador
        self.ejecucion = [self.decode, self.execute, self.memory, self.writeback]
        self.branch_taken = False
        self.prediction_made = False
        
    def reset(self):
        self.ejecucion = [self.decode, self.execute, self.memory, self.writeback]
        self.branch_taken = False
        self.prediction_made = False
   
    def decode(self):
        self.procesador.regRF.data = [None] * 2
        self.procesador.regRF.data[0] = self.procesador.RF.registros[self.registro1]
        self.procesador.regRF.data[1] = self.procesador.RF.registros[self.registro2]
        print(f"Valores leídos: {self.procesador.regRF.data}")
   
    def execute(self):
       
        valor1 = self.procesador.regRF.data[0]
        valor2 = self.procesador.regRF.data[1]
       
        self.procesador.regALU.data = self.procesador.ALU.operar(valor1, valor2, 1)
       
        self.branch_taken = (self.procesador.regALU.data <= 0)
       
        instruction_id = id(self)
        predicted_taken = self.procesador.branch_predictor.predict(instruction_id)
       
        if predicted_taken != self.branch_taken:
            print(f"misprediction")
            print(f"Predicción: {predicted_taken}, Real: {self.branch_taken}")
           
            if not predicted_taken and self.branch_taken:
                print(f"Aplicando salto tardío y limpiando pipeline")
                self.procesador.PC += self.offset - 2
                self.procesador.clear_pipeline()
           
            elif predicted_taken and not self.branch_taken:
                self.procesador.PC -= self.offset
                self.procesador.clear_pipeline()
        else:
            print(f"Predicción correcta")
       
        self.procesador.branch_predictor.update(instruction_id, self.branch_taken)
   
    def memory(self):
        print(f"Sin operación de memoria para rip")
        pass
   
    def writeback(self):
        print(f"Sin writeback para rip")
        pass
   
    def ejecutar(self):
        if self.ejecucion:
            fase = self.ejecucion.pop(0)
            fase()
        else:
            print("No hay más fases para ejecutar en rip")