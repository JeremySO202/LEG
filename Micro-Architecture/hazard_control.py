#register-register
from instructions.nop import Nop
from instructions.sma import Sma
from instructions.rta import Rta
from instructions.mul import Mul
from instructions.y import Y
from instructions.o import O
from instructions.oex import Oex
from instructions.mov import Mov

#immediate
from instructions.smai import Smai
from instructions.rtai import Rtai
from instructions.muli import Muli
from instructions.rotd import Rotd
from instructions.roti import Roti
from instructions.no import No
from instructions.rol import Rol
from instructions.modp import Modp
from instructions.mula import Mula

#branch
from instructions.rig import Rig
from instructions.rim import Rim
from instructions.rip import Rip
from instructions.rin import Rin

#h-type
from instructions.mix import Mix

#memory
from instructions.crg import Crg
from instructions.grd import Grd

class HazardControl:
    
    def __init__(self, procesador):
        self.procesador = procesador

    def handle_misprediction(self, instruction):
        print("Predicción incorrecta detectada. Penalización aplicada.")
        self.procesador.clear_pipeline()
        self.procesador.PC -= instruction.offset + 2

    def exex_fw(self, current_instruction):
        
        if isinstance(current_instruction, (Sma, Rta, Mul, Y, O, Oex, Rig, Rip, Rim)):
            if current_instruction.procesador.regRF.data is None:
                current_instruction.procesador.regRF.data = [None, None]
        elif isinstance(current_instruction, Mix):
            if current_instruction.procesador.regRF.data is None:
                current_instruction.procesador.regRF.data = [None, None, None]
        
        elif isinstance(current_instruction, (Smai, Rtai, Muli, Smai, Rtai, Muli, Roti, Rotd, No, Rol, Modp, Mula, Crg)):
            pass

        alu_inst = self.procesador.regALU.instruccion

        if self.procesador.regALU.instruccion:
            # Instrucciones con dos registros fuente
            if isinstance(current_instruction, (Sma, Rta, Mul, Y, O, Oex, Rig, Rip, Rim)):
                if hasattr(alu_inst, 'destino') and alu_inst.destino == current_instruction.registro1 and (not hasattr(current_instruction, 'bovedareg1') or current_instruction.bovedareg1 == 0):
                    current_instruction.procesador.Check = self.procesador.regALU.data
                    current_instruction.procesador.forw_reg = 1
                    print(f"Hazard detectado: R{alu_inst.destino} -> registro1 (R{current_instruction.registro1})")
                    return True

                if hasattr(alu_inst, 'destino') and alu_inst.destino == current_instruction.registro2 and (not hasattr(current_instruction, 'bovedareg2') or current_instruction.bovedareg2 == 0):
                    current_instruction.procesador.Check = self.procesador.regALU.data
                    current_instruction.procesador.forw_reg = 2
                    print(f"Hazard detectado: R{alu_inst.destino} -> registro2 (R{current_instruction.registro2})")
                    return True
            # Instrucciones con un registro fuente
            elif isinstance(current_instruction,(Smai, Rtai, Muli, Roti, Rotd, No, Rol, Modp, Mula)):
                if hasattr(alu_inst, 'destino') and alu_inst.destino == current_instruction.registro1 and current_instruction.boveda == 0:
                    current_instruction.procesador.Check = self.procesador.regALU.data
                    current_instruction.procesador.forw_reg = 1
                    print(f"Hazard detectado: R{alu_inst.destino} -> registro1 (R{current_instruction.registro1})")
                    return True
                
             # Instrucciones de crg 
             #Sma R1 R2 R3
             #CRG R4 1 R1
            elif isinstance(current_instruction, Crg):
                if hasattr(alu_inst, 'destino') and alu_inst.destino == current_instruction.fuente:
                    current_instruction.procesador.Check = self.procesador.regALU.data
                    current_instruction.procesador.forw_reg = 1
                    print(f"Hazard detectado: L{alu_inst.destino} -> lfuente (L{current_instruction.fuente})")
                    return True
                
            # Instrucciones con tres registros fuente
            elif isinstance(current_instruction, Mix):
                if hasattr(alu_inst, 'destino') and alu_inst.destino == current_instruction.registro1 and current_instruction.boveda == 0:
                    current_instruction.procesador.Check = self.procesador.regALU.data
                    current_instruction.procesador.forw_reg = 1
                    print(f"Hazard detectado: R{alu_inst.destino} -> registro1 (R{current_instruction.registro1})")
                    return True

                if hasattr(alu_inst, 'destino') and alu_inst.destino == current_instruction.registro2 and current_instruction.boveda == 0:
                    current_instruction.procesador.Check = self.procesador.regALU.data
                    current_instruction.procesador.forw_reg = 2
                    print(f"Hazard detectado: R{alu_inst.destino} -> registro2 (R{current_instruction.registro2})")
                    return True
                
                if hasattr(alu_inst, 'destino') and alu_inst.destino == current_instruction.registro3 and current_instruction.boveda == 0:
                    current_instruction.procesador.Check = self.procesador.regALU.data
                    current_instruction.procesador.forw_reg = 3
                    print(f"Hazard detectado: R{alu_inst.destino} -> registro3 (R{current_instruction.registro3})")
                    return True

        print("No hubo necesidad de aplicar forwarding de EX para esta instrucción.")
        return False
    

    #revisar el no

    def memreg_forw(self, current_instruction):

        if isinstance(current_instruction, (Sma, Rta, Mul, Y, O, Oex, Rig, Rip, Rim)):
            if current_instruction.procesador.regRF.data is None:
                current_instruction.procesador.regRF.data = [None, None]
        elif isinstance(current_instruction, Mix):
            if current_instruction.procesador.regRF.data is None:
                current_instruction.procesador.regRF.data = [None, None, None]
        
        elif isinstance(current_instruction, (Smai, Rtai, Muli, Smai, Rtai, Muli, Roti, Rotd, No, Rol, Modp, Mula)):
            pass

        dm_inst = self.procesador.regDM.instruccion

        if self.procesador.regDM.instruccion:
            # Instrucciones con dos registros fuente
            if isinstance(current_instruction, (Sma, Rta, Mul, Y, O, Oex, Rig, Rip, Rim)):
                if hasattr(dm_inst, 'destino') and dm_inst.destino == current_instruction.registro1 and (not hasattr(current_instruction, 'bovedareg1') or current_instruction.bovedareg1 == 0):
                    current_instruction.procesador.second_check = self.procesador.regDM.data
                    current_instruction.procesador.forw_reg2 = 1
                    print(f"Hazard detectado: R{dm_inst.destino} -> registro1 (R{current_instruction.registro1})")
                    return True

                if hasattr(dm_inst, 'destino') and dm_inst.destino == current_instruction.registro2 and (not hasattr(current_instruction, 'bovedareg2') or current_instruction.bovedareg2 == 0):
                    current_instruction.procesador.second_check = self.procesador.regDM.data
                    current_instruction.procesador.forw_reg2 = 2
                    print(f"Hazard detectado: R{dm_inst.destino} -> registro2 (R{current_instruction.registro2})")
                    return True
            # Instrucciones con un registro fuente
            elif isinstance(current_instruction, (Smai, Rtai, Muli, Roti, Rotd, No, Rol, Modp, Mula)):
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
                    print(f"Hazard detectado: R{dm_inst.destino} -> registro2 (R{current_instruction.registro2})")
                    return True
                
                if hasattr(dm_inst, 'destino') and dm_inst.destino == current_instruction.registro3:
                    current_instruction.procesador.second_check = self.procesador.regDM.data
                    current_instruction.procesador.forw_reg2 = 3
                    print(f"Hazard detectado: R{dm_inst.destino} -> registro3 (R{current_instruction.registro3})")
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