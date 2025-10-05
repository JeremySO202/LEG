#branch equal

class BranchEqual:
    def __init__(self, _registro1, _registro2, _offset, _procesador):
        self.registro1 = _registro1
        self.registro2 = _registro2
        self.offset = _offset
        self.procesador = _procesador
        self.ejecucion = [self.decode, self.execute, self.memory, self.writeback]
        self.branch_taken = False 
        self.prediction_made = False
    
    def decode(self):
        print(f"[DECODE] Leyendo registros R{self.registro1} y R{self.registro2}")
        self.procesador.regRF.data = [None] * 2
        self.procesador.regRF.data[0] = self.procesador.RF.registros[self.registro1]
        self.procesador.regRF.data[1] = self.procesador.RF.registros[self.registro2]
        print(f"[DECODE] Valores leídos: {self.procesador.regRF.data}")
    
    def execute(self):
        """Etapa EXECUTE: Compara los registros y resuelve el salto"""
        print(f"[EXECUTE] Comparando registros (resta para BEQ)")
        
        # Realizar la resta en la ALU (operación 1 = resta)
        self.procesador.regALU.data = self.procesador.ALU.operar(self.procesador.regRF.data[0], self.procesador.regRF.data[1], 1)
        
        # Determinar si el salto debe tomarse (si son iguales, resta = 0)
        self.branch_taken = (self.procesador.regALU.data == 0)
        print(f"[EXECUTE] Resultado comparación: {self.procesador.regALU.data}")
        print(f"[EXECUTE] Salto debe tomarse: {self.branch_taken}")
        
        # Obtener predicción
        instruction_id = id(self)
        predicted_taken = self.procesador.branch_predictor.predict(instruction_id)
        print(f"[EXECUTE] Predicción fue: {predicted_taken}")
        
        # Verificar si hubo misprediction
        if predicted_taken != self.branch_taken:
            print(f"[EXECUTE] ⚠️ MISPREDICTION detectada!")
            print(f"[EXECUTE] Predicción: {predicted_taken}, Real: {self.branch_taken}")
            
            # Si se predijo NO tomado pero SÍ se toma
            if not predicted_taken and self.branch_taken:
                print(f"[EXECUTE] Aplicando salto tardío y limpiando pipeline")
                self.procesador.PC += self.offset - 2  # -2 porque ya avanzó 2 ciclos
                self.procesador.clear_pipeline()
            
            # Si se predijo tomado pero NO se toma
            elif predicted_taken and not self.branch_taken:
                print(f"[EXECUTE] Cancelando salto especulativo y restaurando PC")
                # El PC ya se modificó en DECODE cuando se predijo, hay que corregirlo
                self.procesador.PC -= self.offset  # Revertir el salto especulativo
                self.procesador.clear_pipeline()
        else:
            print(f"[EXECUTE] ✓ Predicción correcta")
        
        # Actualizar el predictor con el resultado real
        self.procesador.branch_predictor.update(instruction_id, self.branch_taken)
    
    def memory(self):
        print(f"Sin operación de memoria para BEQ")
        # Los branches no necesitan acceso a memoria
        pass
    
    def writeback(self):
        print(f"Sin writeback para BEQ")
        # Los branches no escriben en registros
        pass
    
    def ejecutar(self):
        if self.ejecucion:
            fase = self.ejecucion.pop(0)
            fase()
        else:
            print("No hay más fases para ejecutar en BranchEqual.")
