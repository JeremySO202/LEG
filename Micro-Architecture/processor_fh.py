import time
from components.alu import ALU
from components.data_memory import memoriaDatos
from components.instr_memory import memoriaInstrucciones
from components.vault import vault
from components.register_file import archivoRegistros
from components.register import Registro
from hazard_control import HazardControl, BranchPredictor
#register-register
from instructions.nop import Nop
from instructions.sma import Sma
from instructions.rta import Rta
from instructions.mul import Mul
from instructions.y import Y
from instructions.o import O
from instructions.oex import Oex
from instructions.chkf import Chkf
#1 register
from instructions.smai import Smai
from instructions.rtai import Rtai
from instructions.muli import Muli
from instructions.rotd import Rotd
from instructions.roti import Roti
from instructions.no import No
from instructions.rol import Rol
from instructions.modp import Modp
from instructions.mula import Mula
from instructions.frm import Frm

#branch
from instructions.rig import Rig
from instructions.rim import Rim
from instructions.rip import Rip

#h-type
from instructions.mix import Mix

#memory
from instructions.crg import Crg
from instructions.grd import Grd

#vault
from instructions.grdh import Grdh
from instructions.grdk import Grdk



class ProcesadorFullHazard:
    # Constantes para tipos de instrucciones
    TWO_REG_INSTRUCTIONS = (Sma, Rta, Mul, Y, O, Oex, Roti, Rotd, Rig, Rip, Rim, Chkf)
    IMMEDIATE_INSTRUCTIONS = (Smai, Rtai, Muli, No, Rol, Modp, Mula, Crg, Grd, Grdh, Grdk, Frm)
    IMMEDIATE_NO_CRG = (Smai, Rtai, Muli, No, Rol, Modp, Mula, Grd, Grdh, Grdk, Frm)
    ALL_HAZARD_INSTRUCTIONS = (Sma, Rta, Mul, Y, O, Oex, Rig, Rip, Rim, Smai, Rtai, Muli, Roti, Rotd, No, Rol, Modp, Mula, Mix, Crg, Grd, Grdh, Grdk, Chkf, Frm)
    
    def __init__(self, interval=1, print_registers=False, step_by_step=False):
        self.PC = 0
        self.Check = ""
        self.forw_reg = 0
        self.second_check = ""
        self.forw_reg2 = 0
        self.IM = memoriaInstrucciones()
        self.regIM = Registro()
        self.RF = archivoRegistros()
        self.regRF = Registro()
        self.ALU = ALU()
        self.regALU = Registro()
        self.DM = memoriaDatos()
        self.regDM = Registro()
        self.hazard_control = HazardControl(self)
        self.branch_predictor = BranchPredictor(default_prediction=True)

        self.time = 1
        self.interval = interval
        self.print_registers = print_registers
        self.step_by_step = step_by_step
        self.total_cycles = 0
        self.instructions_completed = 0
        self.pipeline_locations = ["", "", "", "", ""]
        
        self.vault = vault()
        
        # Para tracking de instrucciones en el pipeline
        self.fetch_instruction_index = None
        self.decode_instruction_index = None
        self.execute_instruction_index = None
        self.memory_instruction_index = None
        self.writeback_instruction_index = None


    def cargarInstrucciones(self, instruccion):
        self.IM.instrucciones.append(instruccion)

    def clear_pipeline(self):
        print("Limpiando pipeline tras el salto.")
        time.sleep(0.1)
        self.regIM.clear()
        self.regRF.clear()
        # Limpiar los índices también
        self.decode_instruction_index = None
        self.execute_instruction_index = None

    def _print_stage_header(self, stage_name, pc_offset):
        # Imprime el encabezado de cada etapa del pipeline
        print("----------------------")
        print(f"Etapa {stage_name} {self.PC + pc_offset}")

    def _print_no_instruction(self, stage_index):
        # Imprime mensaje cuando no hay instrucción en una etapa
        print("No hay instrucción en esta etapa")
        self.pipeline_locations[stage_index] = ""

    def _handle_forwarding_two_registers(self, instruction, forw_value, forw_reg):
        # Maneja forwarding para instrucciones de dos registros
        if forw_reg == 1:
            instruction.regRF.data[0] = forw_value
        elif forw_reg == 2:
            print(f"Forwarding al registro2")
            instruction.regRF.data[1] = forw_value
        print(f"Después del forwarding: {instruction.regRF.data}")

    def _handle_forwarding_immediate(self, instruction, forw_value):
        # Maneja forwarding para instrucciones con inmediatos
        instruction.regRF.data = forw_value
        print(f"Después del forwarding: {instruction.regRF.data}")

    def _handle_forwarding_mix(self, instruction, forw_value, forw_reg):
        # Maneja forwarding para instrucciones Mix
        if forw_reg == 1:
            print(f"Forwarding al registro1")
            instruction.regRF.data[0] = forw_value
        elif forw_reg == 2:
            print(f"Forwarding al registro2")
            instruction.regRF.data[1] = forw_value
        elif forw_reg == 3:
            print(f"Forwarding al registro3")
            instruction.regRF.data[2] = forw_value
        print(f"Después del forwarding: {instruction.regRF.data}")

    def iniciarEjecucion(self):
        needs_forwarding = False
        second_hazard = False
        start_time = time.time()
        execute = True
        max_cycles = 10000  # Límite para los ciclos inficitos
        
        while execute and self.total_cycles < max_cycles:
            self.total_cycles += 1
            execute = False

            # WRITEBACK
            self._print_stage_header("WRITEBACK", -4)
            if self.regDM.instruccion is not None:
                execute = True
                print(f"{self.regDM.instruccion}")
                self.regDM.instruccion.ejecutar()
                self.pipeline_locations[4] = "Instrucción escribiendo"
                self.regDM.clear()
                self.writeback_instruction_index = None
                self.instructions_completed += 1
            else:
                self._print_no_instruction(4)

            # MEMORY
            self._print_stage_header("MEMORY", -3)
            if self.regALU.instruccion is not None:
                execute = True
                self.regALU.instruccion.ejecutar()
                self.pipeline_locations[3] = "Instrucción en memoria"
                self.regDM.instruccion = self.regALU.instruccion
                self.writeback_instruction_index = self.memory_instruction_index
                self.regALU.clear()
                self.memory_instruction_index = None
            else:
                self._print_no_instruction(3)

            # EXECUTE
            self._print_stage_header("EXECUTE", -2)
            if self.regRF.instruccion is not None and not isinstance(self.regRF.instruccion, Nop):
                execute = True
                
                # Aplicar forwarding EX-EX
                if needs_forwarding:
                    print(f"Recibiendo forwarding en EXECUTE - Valor: {self.Check}")
                    
                    
                    if isinstance(self.regRF.instruccion, self.TWO_REG_INSTRUCTIONS):
                        self._handle_forwarding_two_registers(self, self.Check, self.forw_reg)
                    elif isinstance(self.regRF.instruccion, self.IMMEDIATE_INSTRUCTIONS):
                        
                        if self.forw_reg == 1:
                            self._handle_forwarding_immediate(self, self.Check)
                    elif isinstance(self.regRF.instruccion, Mix):
                        self._handle_forwarding_mix(self, self.Check, self.forw_reg)
                    
                    needs_forwarding = False

                # Aplicar forwarding MEM-EX
                if second_hazard:
                    print(f"Recibiendo forwarding de MEM - Valor: {self.second_check}")

                    if isinstance(self.regRF.instruccion, self.TWO_REG_INSTRUCTIONS):
                        if self.regRF.data is None:
                            self.regRF.data = [None, None]
                        self._handle_forwarding_two_registers(self, self.second_check, self.forw_reg2)
                    elif isinstance(self.regRF.instruccion, self.IMMEDIATE_INSTRUCTIONS):
                        if self.regRF.data is None:
                            self.regRF.data = None
                        if self.forw_reg2 == 1:
                            self._handle_forwarding_immediate(self, self.second_check)
                    elif isinstance(self.regRF.instruccion, Mix):
                        self._handle_forwarding_mix(self, self.second_check, self.forw_reg2)
                    
                    second_hazard = False

                self.regRF.instruccion.ejecutar()
                self.pipeline_locations[2] = "Instrucción ejecutando"
                self.regALU.instruccion = self.regRF.instruccion
                self.memory_instruction_index = self.execute_instruction_index
                self.regRF.clear()
                self.execute_instruction_index = None
            else:
                self._print_no_instruction(2)

            # DECODE
            self._print_stage_header("DECODE", -1)
            if self.regIM.instruccion is not None:
                print(f"{self.regIM.instruccion.__class__.__name__}")
                execute = True

                # Detección de hazards EX-EX y MEM-EX para todas las instrucciones que los necesiten
                if isinstance(self.regIM.instruccion, self.ALL_HAZARD_INSTRUCTIONS):
                    # Hazard EX-EX
                    needs_forwarding = self.hazard_control.exex_fw(self.regIM.instruccion)
                    print(f"Hazard EX: {'Detectado - Forwarding necesario' if needs_forwarding else 'No detectado'}")

                    
                    second_hazard = self.hazard_control.memreg_forw(self.regIM.instruccion)
                    print(f"Hazard MEM: {'Detectado - Forwarding necesario' if second_hazard else 'No detectado'}")
                    if second_hazard:
                        print(f"Valor MEM: {self.second_check}")
                
                # Inserción de NOP por dependencia con load (Crg)
                if isinstance(self.regALU.instruccion, Crg) and (needs_forwarding or second_hazard):
                    print("Inserción de NOP por dependencia con Crg")
                    self.PC -= 1
                    self.regRF.clear()
                    self.regIM.instruccion = Nop(self)
                    self.regRF.instruccion = self.regIM.instruccion
                    time.sleep(0.1)
                else:
                    # Inicializar estructura de datos según tipo de instrucción
                    if isinstance(self.regIM.instruccion, self.TWO_REG_INSTRUCTIONS):
                        if self.regRF.data is None:
                            self.regRF.data = [None, None]
                    elif isinstance(self.regIM.instruccion, self.IMMEDIATE_NO_CRG):
                        if self.regRF.data is None:
                            self.regRF.data = None
                    elif isinstance(self.regIM.instruccion, Mix):
                        if self.regRF.data is None:
                            self.regRF.data = [None, None, None]

                # Continuar flujo normal del pipeline
                self.pipeline_locations[1] = f"Instrucción {self.PC - 1}"
                self.regIM.instruccion.ejecutar()
                self.regRF.instruccion = self.regIM.instruccion
                self.execute_instruction_index = self.decode_instruction_index
                
                # Debug específico para Rig
                if isinstance(self.regIM.instruccion, Rig):
                    print(f"RIG Debug - RF data: {self.regRF.data}, IM data: {self.regIM.data}")
                
                self.regIM.clear()
                self.decode_instruction_index = None
            else:
                self._print_no_instruction(1)

            # FETCH
            self._print_stage_header("FETCH", 0)

            if self.PC < len(self.IM.instrucciones):
                # Verificar stalls por instrucciones en pipeline
                if self.memory_instruction_index == self.PC or self.writeback_instruction_index == self.PC:
                    print(f"STALL: Instrucción {self.PC} en pipeline (MEM:{self.memory_instruction_index}, WB:{self.writeback_instruction_index})")
                    print(f"Insertando NOP")
                    
                    self.regIM.instruccion = Nop(self)
                    self.regIM.instruccion.reset()
                    self.decode_instruction_index = None
                    self.pipeline_locations[0] = f"STALL (esperando instrucción {self.PC})"
                    execute = True
                else:
                    # Fetch normal
                    execute = True
                    print(f"Cargando instrucción {self.PC}")
                    self.pipeline_locations[0] = f"Instrucción {self.PC}"
                    self.regIM.instruccion = self.IM.instrucciones[self.PC]
                    self.regIM.instruccion.reset()
                    self.decode_instruction_index = self.PC
                    self.PC += 1
            else:
                print("No hay más instrucciones")
                self.pipeline_locations[0] = ""

            # Fin de ciclo y métricas
            print("___________________________________________")
            print("_________________FIN CICLO_________________")
               
            elapsed_time = self.time
            if elapsed_time > 0:
                clock_rate = self.total_cycles / (elapsed_time * 1e9)
            else:
                clock_rate = 0

            print(f"Ciclo: {self.total_cycles}, Completadas: {self.instructions_completed}, Tiempo: {elapsed_time}, Clock: {clock_rate:.2e} GHz")
            print("___________________________________________")
            self.time += 20
            time.sleep(self.interval)
            
            if self.print_registers:
                print(f"Registros: {self.RF.registros}")
                print(f"Vault: {self.vault.secure_regs}")
                print(f"First 64 memory blocks: {self.DM.datos[:64]}")
                
            if self.step_by_step:
                input("Presiona Enter para continuar al siguiente ciclo...")
        
        # Verificar si se alcanzó el límite de ciclos
        if self.total_cycles >= max_cycles:
            print(f"Se alcanzó el límite máximo de ciclos ({max_cycles})")
            print(f"El programa puede estar en un ciclo infinito o necesita más ciclos para completar.")
            print(f"Instrucciones completadas: {self.instructions_completed}")

    def manejar_branch(self, branch_instruction):
        branch_instruction.ejecutar()

        actual_taken = self.regALU.data == 0
        print(f"Resultado real del salto: {actual_taken}")

        instruction_id = id(branch_instruction)
        predicted_taken = self.branch_predictor.predict(instruction_id)

        if predicted_taken != actual_taken:
            self.hazard_control.handle_misprediction(branch_instruction)

        self.branch_predictor.update(instruction_id, actual_taken)