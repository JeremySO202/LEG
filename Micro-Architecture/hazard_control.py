#registro-registro
from instructions.sma import Sma
from instructions.rta import Rta
from instructions.y import Y
from instructions.o import O
from instructions.mul import Mul
from instructions.rol import Rol
from instructions.oex import Oex
#para un inmediato
from instructions.mov import Mov
#para un solo registro
from instructions.no import No
#otras
from instructions.crg import LoadWord
from instructions.rig import RIG  
from instructions.rim import RIM
from instructions.rin import RIN
from instructions.rip import RIP

from instructions.grd import StoreWord
from instructions.mix import Mix
#de inmediatos
from instructions.rtai import Rtai
from instructions.smai import Smai
from instructions.muli import Muli
from instructions.roti import Roti
from instructions.rotd import Rotd

class HazardControl:
    
    def __init__(self, procesador):
        self.procesador = procesador

    def handle_misprediction(self, instruction):
        print("Predicción incorrecta detectada. Penalización aplicada.")
        self.procesador.clear_pipeline()
        self.procesador.PC -= instruction.offset + 1

    def exex_fw(self, current_instruction):
        if not isinstance(current_instruction, (Sma, Rta, O, Y, Oex, Mul, Rol, RIG, RIP, RIM, Smai, Rtai, Muli, No, Rotd, Roti, Mix)):
            print("No se aplica forwarding: instrucción no es de un tipo soportado.")
            return False

        if isinstance(current_instruction, (Sma, Rta, O, Y, Mul, RIG)):
            if current_instruction.procesador.regRF.data is None:
                current_instruction.procesador.regRF.data = [None, None]
        elif isinstance(current_instruction, Mix):
            if current_instruction.procesador.regRF.data is None:
                current_instruction.procesador.regRF.data = [None, None, None]
        
        elif isinstance(current_instruction, (Smai, Rtai, Muli, No, Roti, Rotd)):
            pass

        alu_inst = self.procesador.regALU.instruccion

        if self.procesador.regALU.instruccion:
            if isinstance(current_instruction, (Sma, Rta, O, Y, Oex, Mul, Rol, RIG, RIP, RIM)):
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

            elif isinstance(current_instruction,(Smai, Rtai, Muli, No, Roti, Rotd)):
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

        print("No hubo necesidad de aplicar forwarding de EX para esta instrucción.")
        return False
    

    #revisar el no

    def memreg_forw(self, current_instruction):

        if not isinstance(current_instruction, (Sma, Rta, O, Y, Mul, Smai, RIG, Mix)):
            print("No se aplica forwarding: instrucción no es de un tipo soportado.")
            return False

        if isinstance(current_instruction, (Sma, Rta, O, Y, Mul, RIG)):
            if current_instruction.procesador.regRF.data is None:
                current_instruction.procesador.regRF.data = [None, None]
        elif isinstance(current_instruction, Mix):
            if current_instruction.procesador.regRF.data is None:
                current_instruction.procesador.regRF.data = [None, None, None]
        
        elif isinstance(current_instruction, (Smai, Rtai, Muli)):
            pass

        dm_inst = self.procesador.regDM.instruccion

        if self.procesador.regDM.instruccion:
            if isinstance(current_instruction, (Sma, Rta, O, Y, Mul, RIG)):
                if hasattr(dm_inst, 'destino') and dm_inst.destino == current_instruction.registro1:
                    current_instruction.procesador.second_check = self.procesador.regDM.data
                    current_instruction.procesador.forw_reg2 = 1
                    print(f"Hazard detectado: R{dm_inst.destino} -> registro1 (R{current_instruction.registro1})")
                    return True
                
                if hasattr(dm_inst, 'destino') and dm_inst.destino == current_instruction.registro2:
                    current_instruction.procesador.second_check = self.procesador.regDM.data
                    current_instruction.procesador.forw_reg2 = 2
                    print(f"Hazard detectado: R{dm_inst.destino} -> registro1 (R{current_instruction.registro2})")
                    return True
            
            elif isinstance(current_instruction, (Smai, Rtai, Muli)):
                if hasattr(dm_inst, 'destino') and dm_inst.destino == current_instruction.registro1:
                    current_instruction.procesador.second_check = self.procesador.regDM.data
                    current_instruction.procesador.forw_reg2 = 1
                    print(f"Hazard detectado: R{dm_inst.destino} -> registro1 (R{current_instruction.registro1})")
                    return True
                
            elif isinstance(current_instruction, Mix):
                if hasattr(dm_inst, 'destino') and dm_inst.destino == current_instruction.registro1:
                    current_instruction.procesador.second_check = self.procesador.regDM.data
                    current_instruction.procesador.forw_reg2 = 1
                    print(f"Hazard detectado: R{dm_inst.destino} -> registro1 (R{current_instruction.registro1})")
                    return True
                
                if hasattr(dm_inst, 'destino') and dm_inst.destino == current_instruction.registro2:
                    current_instruction.procesador.second_check = self.procesador.regDM.data
                    current_instruction.procesador.forw_reg2 = 2
                    print(f"Hazard detectado: R{dm_inst.destino} -> registro1 (R{current_instruction.registro2})")
                    return True
                
                if hasattr(dm_inst, 'destino') and dm_inst.destino == current_instruction.registro3:
                    current_instruction.procesador.second_check = self.procesador.regDM.data
                    current_instruction.procesador.forw_reg2 = 3
                    print(f"Hazard detectado: R{dm_inst.destino} -> registro1 (R{current_instruction.registro3})")
                    return True

        print("No hubo necesidad de aplicar forwarding de MEM para esta instrucción.")
        return False


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