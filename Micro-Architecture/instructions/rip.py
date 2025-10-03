#branch menor igual

class RIP:
    def __init__(self, _registro1, _registro2, _offset, _procesador):
        self.registro1 = _registro1
        self.registro2 = _registro2
        self.offset = _offset
        self.procesador = _procesador

        self.ejecucion = [self.instruccion1, self.instruccion2]

    def instruccion1(self):
        print(f"Obteniendo valores de registros {self.registro1} y {self.registro2}")
        self.procesador.regRF.data = [None] * 2
        self.procesador.regRF.data[0] = self.procesador.RF.registros[self.registro1]
        self.procesador.regRF.data[1] = self.procesador.RF.registros[self.registro2]
        print(f"Valores obtenidos: {self.procesador.regRF.data}")

    def instruccion2(self):
        print("Comparando registros")
        valor1 = self.procesador.regRF.data[0]
        valor2 = self.procesador.regRF.data[1]
        self.procesador.regALU.data = 1 if valor1 <= valor2 else 0

        print(f"Salto tomado: {self.procesador.regALU.data == 1}")

        """Manejo del BranchEqual dentro del procesador."""
        instruction_id = id(self)
        
        predicted_taken = self.procesador.branch_predictor.predict(instruction_id)

        # Obtener la predicción del salto
        if not predicted_taken and self.procesador.regALU.data == 1:
            self.procesador.PC += self.offset - 1
            self.procesador.clear_pipeline()


    def ejecutar(self):
        if self.ejecucion:
            fase = self.ejecucion.pop(0)
            fase()
        else:
            print("No hay más fases para ejecutar en Rama Menor Igual.")