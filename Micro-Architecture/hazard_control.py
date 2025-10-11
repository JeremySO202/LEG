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

#h-type
from instructions.mix import Mix

#memory
from instructions.crg import Crg
from instructions.grd import Grd

class HazardControl:
    
    def __init__(self, procesador):
        self.procesador = procesador
    
    def _initialize_regrf_data(self, current_instruction):
        """Inicializa la estructura de datos regRF según el tipo de instrucción"""
        if isinstance(current_instruction, (Sma, Rta, Mul, Y, O, Oex, Rig, Rip, Rim)):
            if current_instruction.procesador.regRF.data is None:
                current_instruction.procesador.regRF.data = [None, None]
        elif isinstance(current_instruction, Mix):
            if current_instruction.procesador.regRF.data is None:
                current_instruction.procesador.regRF.data = [None, None, None]
    
    def _check_two_register_hazard(self, current_instruction, source_inst, forwarding_data, is_mem_stage=False):
        """Verifica hazards para instrucciones de dos registros"""
        if not hasattr(source_inst, 'destino'):
            return False
            
        # Verificar registro1
        if (source_inst.destino == current_instruction.registro1 and 
            (not hasattr(current_instruction, 'bovedareg1') or current_instruction.bovedareg1 == 0)):
            if is_mem_stage:
                current_instruction.procesador.second_check = forwarding_data
                current_instruction.procesador.forw_reg2 = 1
            else:
                current_instruction.procesador.Check = forwarding_data
                current_instruction.procesador.forw_reg = 1
            print(f"Hazard detectado: R{source_inst.destino} -> registro1 (R{current_instruction.registro1})")
            return True
            
        # Verificar registro2  
        if (source_inst.destino == current_instruction.registro2 and
            (not hasattr(current_instruction, 'bovedareg2') or current_instruction.bovedareg2 == 0)):
            if is_mem_stage:
                current_instruction.procesador.second_check = forwarding_data
                current_instruction.procesador.forw_reg2 = 2
            else:
                current_instruction.procesador.Check = forwarding_data
                current_instruction.procesador.forw_reg = 2
            print(f"Hazard detectado: R{source_inst.destino} -> registro2 (R{current_instruction.registro2})")
            return True
            
        return False
    
    def _check_single_register_hazard(self, current_instruction, source_inst, forwarding_data, is_mem_stage=False):
        """Verifica hazards para instrucciones de un registro"""
        if not hasattr(source_inst, 'destino'):
            return False
            
        if source_inst.destino == current_instruction.registro1 and current_instruction.boveda == 0:
            if is_mem_stage:
                current_instruction.procesador.second_check = forwarding_data
                current_instruction.procesador.forw_reg2 = 1
            else:
                current_instruction.procesador.Check = forwarding_data
                current_instruction.procesador.forw_reg = 1
            print(f"Hazard detectado: R{source_inst.destino} -> registro1 (R{current_instruction.registro1})")
            return True
            
        return False
    
    def _check_mix_hazard(self, current_instruction, source_inst, forwarding_data, is_mem_stage=False):
        """Verifica hazards para instrucciones Mix (3 registros)"""
        if not hasattr(source_inst, 'destino'):
            return False
            
        registers = [
            (current_instruction.registro1, 1, "registro1"),
            (current_instruction.registro2, 2, "registro2"), 
            (current_instruction.registro3, 3, "registro3")
        ]
        
        for reg_num, forw_reg_num, reg_name in registers:
            if source_inst.destino == reg_num and current_instruction.boveda == 0:
                if is_mem_stage:
                    current_instruction.procesador.second_check = forwarding_data
                    current_instruction.procesador.forw_reg2 = forw_reg_num
                else:
                    current_instruction.procesador.Check = forwarding_data
                    current_instruction.procesador.forw_reg = forw_reg_num
                print(f"Hazard detectado: R{source_inst.destino} -> {reg_name} (R{reg_num})")
                return True
                
        return False

    def handle_misprediction(self, instruction):
        """Maneja las mispredictions de branch de forma centralizada"""
        print("Predicción incorrecta detectada. Penalización aplicada.")
        
        if not instruction.prediction_made:
            predicted_taken = self.procesador.branch_predictor.predict(id(instruction))
        else:
            predicted_taken = instruction.prediction_made
        
        if not predicted_taken and instruction.branch_taken:
            print(f"Aplicando salto tardío y limpiando pipeline")
            self.procesador.PC += instruction.offset
            
        elif predicted_taken and not instruction.branch_taken:
            print(f"Cancelando salto especulativo y restaurando PC")
            self.procesador.PC -= instruction.offset + 1
            
        self.procesador.clear_pipeline()

    def exex_fw(self, current_instruction):
        """Detecta y aplica forwarding EX-EX"""
        self._initialize_regrf_data(current_instruction)
        
        alu_inst = self.procesador.regALU.instruccion
        if not alu_inst:
            print("No hubo necesidad de aplicar forwarding de EX para esta instrucción.")
            return False
        
        forwarding_data = self.procesador.regALU.data
        
        # Instrucciones con dos registros fuente
        if isinstance(current_instruction, (Sma, Rta, Mul, Y, O, Oex, Rig, Rip, Rim)):
            return self._check_two_register_hazard(current_instruction, alu_inst, forwarding_data)
            
        # Instrucciones con un registro fuente
        elif isinstance(current_instruction, (Smai, Rtai, Muli, Roti, Rotd, No, Rol, Modp, Mula)):
            return self._check_single_register_hazard(current_instruction, alu_inst, forwarding_data)
            
        # Instrucciones de crg
        elif isinstance(current_instruction, Crg):
            if hasattr(alu_inst, 'destino') and alu_inst.destino == current_instruction.fuente:
                current_instruction.procesador.Check = forwarding_data
                current_instruction.procesador.forw_reg = 1
                print(f"Hazard detectado: L{alu_inst.destino} -> fuente (L{current_instruction.fuente})")
                return True
                
        # Instrucciones con tres registros fuente
        elif isinstance(current_instruction, Mix):
            return self._check_mix_hazard(current_instruction, alu_inst, forwarding_data)

        print("No hubo necesidad de aplicar forwarding de EX para esta instrucción.")
        return False
    

    def memreg_forw(self, current_instruction):
        """Detecta y aplica forwarding MEM-EX"""
        self._initialize_regrf_data(current_instruction)
        
        dm_inst = self.procesador.regDM.instruccion
        if not dm_inst:
            print("No hubo necesidad de aplicar forwarding de MEM para esta instrucción.")
            return False
        
        forwarding_data = self.procesador.regDM.data
        
        # Instrucciones con dos registros fuente
        if isinstance(current_instruction, (Sma, Rta, Mul, Y, O, Oex, Rig, Rip, Rim)):
            return self._check_two_register_hazard(current_instruction, dm_inst, forwarding_data, is_mem_stage=True)
            
        # Instrucciones con un registro fuente
        elif isinstance(current_instruction, (Smai, Rtai, Muli, Roti, Rotd, No, Rol, Modp, Mula)):
            return self._check_single_register_hazard(current_instruction, dm_inst, forwarding_data, is_mem_stage=True)
                
        # Instrucciones con tres registros fuente
        elif isinstance(current_instruction, Mix):
            return self._check_mix_hazard(current_instruction, dm_inst, forwarding_data, is_mem_stage=True)

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