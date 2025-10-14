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
    
    def _read_registers(self):
        # Lee los registros fuente y los almacena en regRF
        self.procesador.regRF.data = [None] * 2
        self.procesador.regRF.data[0] = self.procesador.RF.registros[self.registro1]
        self.procesador.regRF.data[1] = self.procesador.RF.registros[self.registro2]
    
    def _evaluate_branch_condition(self, alu_result):
        # Evalúa la condición específica del branch (menor o igual)
        return alu_result <= 0
    
    def _handle_branch_prediction(self):
        # Maneja la predicción y misprediction del branch
        instruction_id = id(self)
        predicted_taken = self.procesador.branch_predictor.predict(instruction_id)
        print(f"Predicción fue: {predicted_taken}")
        
        if predicted_taken != self.branch_taken:
            print(f"misprediction - Predicción: {predicted_taken}, Real: {self.branch_taken}")
            self.procesador.hazard_control.handle_misprediction(self)
        else:
            print(f"Predicción correcta")
        
        self.procesador.branch_predictor.update(instruction_id, self.branch_taken)
   
    def decode(self):
        print(f"Leyendo registros L{self.registro1} y L{self.registro2}")
        self._read_registers()
        print(f"Valores leídos: {self.procesador.regRF.data}")
        
        # Predicción especulativa del branch
        instruction_id = id(self)
        predicted_taken = self.procesador.branch_predictor.predict(instruction_id)
        print(f"[Branch detectado - Predicción: {predicted_taken}]")
        
        if predicted_taken:
            print(f"[Tomando salto especulativo: PC += {self.offset}]")
            self.procesador.PC += self.offset
   
    def execute(self):
        print(f"Comparando valores para branch menor igual")
        valor1 = self.procesador.regRF.data[0]
        valor2 = self.procesador.regRF.data[1]
       
        self.procesador.regALU.data = self.procesador.ALU.operar(valor1, valor2, 1)
        self.branch_taken = self._evaluate_branch_condition(self.procesador.regALU.data)
        
        print(f"Resultado comparación: {valor1} - {valor2} = {self.procesador.regALU.data}")
        print(f"Salto: {self.branch_taken}")
       
        self._handle_branch_prediction()
   
    def memory(self):
        print(f"Sin operación de memoria para Rip")
   
    def writeback(self):
        print(f"Sin writeback para Rip")
   
    def ejecutar(self):
        if self.ejecucion:
            fase = self.ejecucion.pop(0)
            fase()
        else:
            print("No hay más fases para ejecutar en Rip.")