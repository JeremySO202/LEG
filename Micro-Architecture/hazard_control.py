from instructions.sma import Sma
from instructions.rta import Rta
from instructions.y import Y
from instructions.o import O
from instructions.mul import Mul
from instructions.smai import Smai
from instructions.rig import BranchEqual
from instructions.crg import LoadWord
from instructions.grd import StoreWord
from instructions.mix import Mix

class HazardControl:
    
    def __init__(self, procesador):
        self.procesador = procesador

    def handle_misprediction(self, instruction):
        print("Predicción incorrecta detectada. Penalización aplicada.")
        self.procesador.clear_pipeline()
        self.procesador.PC -= instruction.offset + 1

    def try_check(self, current_instruction):

        if not isinstance(current_instruction, (Sma, Rta, O, Y, Mul, Smai, BranchEqual, Mix)):
            print("No se aplica forwarding: instrucción no es de un tipo soportado.")
            return False

        if isinstance(current_instruction, (Sma, Rta, O, Y, Mul, BranchEqual)):
            if current_instruction.procesador.regRF.data is None:
                current_instruction.procesador.regRF.data = [None, None]
        elif isinstance(current_instruction, Mix):
            if current_instruction.procesador.regRF.data is None:
                current_instruction.procesador.regRF.data = [None, None, None]
        
        elif isinstance(current_instruction, Smai):
            pass

        alu_inst = self.procesador.regALU.instruccion

        if self.procesador.regALU.instruccion:
            if isinstance(current_instruction, (Sma, Rta, O, Y, Mul, BranchEqual)):
                if hasattr(alu_inst, 'destino') and alu_inst.destino == current_instruction.registro1:
                    current_instruction.procesador.Check = self.procesador.regALU.data
                    current_instruction.procesador.forw_reg = 1
                    print(f"Hazard detectado: R{alu_inst.destino} -> registro1 (R{current_instruction.registro1})")
                    return True

                if hasattr(alu_inst, 'destino') and alu_inst.destino == current_instruction.registro2:
                    current_instruction.procesador.Check = self.procesador.regALU.data
                    current_instruction.procesador.forw_reg = 2
                    print(f"Hazard detectado: R{alu_inst.destino} -> registro2 (R{current_instruction.registro2})")
                    return True

            elif isinstance(current_instruction, Smai):
                if hasattr(alu_inst, 'destino') and alu_inst.destino == current_instruction.registro1:
                    current_instruction.procesador.Check = self.procesador.regALU.data
                    current_instruction.procesador.forw_reg = 1
                    print(f"Hazard detectado: R{alu_inst.destino} -> registro1 (R{current_instruction.registro1})")
                    return True
                
            elif isinstance(current_instruction, Mix):
                if hasattr(alu_inst, 'destino') and alu_inst.destino == current_instruction.registro1:
                    current_instruction.procesador.Check = self.procesador.regALU.data
                    current_instruction.procesador.forw_reg = 1
                    print(f"Hazard detectado: R{alu_inst.destino} -> registro1 (R{current_instruction.registro1})")
                    return True

                if hasattr(alu_inst, 'destino') and alu_inst.destino == current_instruction.registro2:
                    current_instruction.procesador.Check = self.procesador.regALU.data
                    current_instruction.procesador.forw_reg = 2
                    print(f"Hazard detectado: R{alu_inst.destino} -> registro2 (R{current_instruction.registro2})")
                    return True
                
                if hasattr(alu_inst, 'destino') and alu_inst.destino == current_instruction.registro3:
                    current_instruction.procesador.Check = self.procesador.regALU.data
                    current_instruction.procesador.forw_reg = 3
                    print(f"Hazard detectado: R{alu_inst.destino} -> registro3 (R{current_instruction.registro3})")
                    return True

        print("No hubo necesidad de aplicar forwarding para esta instrucción.")
        return False
    
   



    def second_check(self, current_instruction):
      
        if self.procesador.regALU.instruccion:
            alu_inst = self.procesador.regALU.instruccion

            # Para instrucciones tipo R
            if isinstance(current_instruction, (Sma, Rta, O, Y, Mul)):
                # caso1: RAW para el primer registro
                if hasattr(alu_inst, 'destino') and alu_inst.destino == current_instruction.registro1:
                    current_instruction.procesador.regIM.data[0] = self.procesador.regALU.data
                    forwarding_applied = True
                    print(f"Forwarding desde ALU a DECODE para registro {current_instruction.registro1}.")

                # caso2: RAW para el segundo registro
                if hasattr(alu_inst, 'destino') and alu_inst.destino == current_instruction.registro2:
                    current_instruction.procesador.regIM.data[1] = self.procesador.regALU.data
                    forwarding_applied = True
                    print(f"Forwarding desde ALU a DECODE para registro {current_instruction.registro2}.")

            # Para instrucciones tipo I
            elif isinstance(current_instruction, Smai):
                if hasattr(alu_inst, 'destino') and alu_inst.destino == current_instruction.registro1:
                    current_instruction.procesador.regIM.data = self.procesador.regALU.data
                    forwarding_applied = True
                    print(f"Forwarding desde ALU a DECODE para registro {current_instruction.registro1}.")

        # Mensaje si no hubo forwarding
        if not forwarding_applied:
            print("No hubo necesidad de aplicar forwarding para esta instrucción.")

    def forward_from_execute(self, destino, resultado):
        """Envía el resultado de ALU al registro correspondiente."""
    
        # Actualiza el valor en el archivo de registros
        self.procesador.RF.registros[destino] = resultado

        # Si no hay instrucción en DECODE, no es necesario imprimir mensajes adicionales
        if not self.procesador.regRF.instruccion:
            return

        # Bandera para detectar si hubo forwarding
        forwarding_applied = False

        # Si hay instrucciones esperando este valor, lo forwardea a ellas
        inst = self.procesador.regRF.instruccion
        
        # Para instrucciones tipo R
        if isinstance(inst, (Sma, Rta, O, Y, Mul)):
            if inst.registro1 == destino and self.procesador.regRF.data[0] is None:
                print(f"Forwarding R{destino} a registro1 en DECODE.")
                self.procesador.regRF.data[0] = resultado
                forwarding_applied = True
            if inst.registro2 == destino and self.procesador.regRF.data[1] is None:
                print(f"Forwarding R{destino} a registro2 en DECODE.")
                self.procesador.regRF.data[1] = resultado
                forwarding_applied = True

        # Para instrucciones tipo I
        elif isinstance(inst, Smai):
            if inst.registro1 == destino and self.procesador.regRF.data is None:
                print(f"Forwarding R{destino} a registro1 en DECODE.")
                self.procesador.regRF.data = resultado
                forwarding_applied = True
                
        elif isinstance(inst, Mix):
            if inst.registro1 == destino and self.procesador.regRF.data[0] is None:
                print(f"Forwarding R{destino} a registro1 en DECODE.")
                self.procesador.regRF.data[0] = resultado
                forwarding_applied = True
            if inst.registro2 == destino and self.procesador.regRF.data[1] is None:
                print(f"Forwarding R{destino} a registro2 en DECODE.")
                self.procesador.regRF.data[1] = resultado
                forwarding_applied = True
            if inst.registro3 == destino and self.procesador.regRF.data[2] is None:
                print(f"Forwarding R{destino} a registro3 en DECODE.")
                self.procesador.regRF.data[2] = resultado
                forwarding_applied = True

        # Mensaje si no hubo necesidad de aplicar forwarding
        if not forwarding_applied:
            print(f"No hubo necesidad de aplicar forwarding desde EXECUTE para el destino R{destino}.")


class BranchPredictor:
    def __init__(self, default_prediction=False):
        """
        Inicializa el BranchPredictor con una política predeterminada.
        default_prediction: True para 'salto tomado', False para 'no tomado'.
        """
        self.history = {}
        self.default_prediction = default_prediction

    def predict(self, instruction_id):
        """Devuelve la predicción para una instrucción específica."""
        return self.history.get(instruction_id, self.default_prediction)

    def update(self, instruction_id, actual_outcome):
        """Actualiza el historial dinámico basado en el resultado real."""
        self.history[instruction_id] = actual_outcome
        print(f"Historial actualizado para instrucción {instruction_id}: {actual_outcome}")

    def reset(self):
        """Resetea el historial dinámico."""
        self.history = {}