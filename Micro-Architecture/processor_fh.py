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



class ProcesadorFullHazard:
    def __init__(self, interval=1):
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

    def iniciarEjecucion(self):
        needs_forwarding = False
        second_hazard = False
        start_time = time.time()
        execute = True
        
        while execute:
            self.total_cycles += 1

            execute = False
            # WRITEBACK
            print("----------------------")
            print(f"Etapa WRITEBACK {self.PC-4} ")
            if self.regDM.instruccion is not None:
                execute = True
                print(f"{self.regDM.instruccion}")
                self.regDM.instruccion.ejecutar()
                self.pipeline_locations[4] = "Instrucción escribiendo"
                self.regDM.clear()
                self.writeback_instruction_index = None
                self.instructions_completed += 1
            else:
                print("No hay instrucción en esta etapa")
                self.pipeline_locations[4] = ""

            # MEMORY
            print("----------------------")
            print(f"Etapa MEMORY {self.PC-3} ")
            if self.regALU.instruccion is not None:
                execute = True
                self.regALU.instruccion.ejecutar()
                self.pipeline_locations[3] = "Instrucción en memoria"
                self.regDM.instruccion = self.regALU.instruccion
                self.writeback_instruction_index = self.memory_instruction_index
                self.regALU.clear()
                self.memory_instruction_index = None
            else:
                print("No hay instrucción en esta etapa")
                self.pipeline_locations[3] = ""

            # EXECUTE
            print("----------------------")
            print(f"Etapa EXECUTE {self.PC-2}")
            if self.regRF.instruccion is not None and not isinstance(self.regRF.instruccion, Nop):
                execute = True
                if needs_forwarding:
                    print(f"Recibiendo forwarding en EXECUTE")
                    print(f"Valor a recibir: {self.Check}")
                
                    # Para instrucciones de dos registros 
                    if isinstance(self.regRF.instruccion, (Sma, Rta, Mul, Y, O, Oex, Rig, Rip, Rim)):
                        if self.forw_reg == 1:
                            self.regRF.data[0] = self.Check
                        elif self.forw_reg == 2:
                            print(f"Forwarding al registro2")
                            self.regRF.data[1] = self.Check
                        
                        print(f"Después del forwarding: {self.regRF.data}")

                    
                    #Para instrucciones con inmediatos
                    elif isinstance(self.regRF.instruccion, (Smai, Rtai, Muli, Roti, Rotd, No, Rol, Modp, Mula, Crg)):
                        if self.forw_reg == 1:
                            self.regRF.data = self.Check
                            print(f"Después del forwarding: {self.regRF.data}")
                            
                    elif isinstance(self.regRF.instruccion, Mix):
                        # Aplicar el forwarding al registro correspondiente
                        if self.forw_reg == 1:
                            print(f"Forwarding al registro1")
                            self.regRF.data[0] = self.Check
                        elif self.forw_reg == 2:
                            print(f"Forwarding al registro2")
                            self.regRF.data[1] = self.Check
                        elif self.forw_reg == 3:
                            print(f"Forwarding al registro3")
                            self.regRF.data[2] = self.Check
                        
                        print(f"Después del forwarding: {self.regRF.data}")
                    
                    needs_forwarding = False

                #revisar las cosas de memoria

                if second_hazard:
                    print(f"Recibiendo forwarding de MEM")
                    print(f"Valor a recibir: {self.second_check}")
                    # Para instrucciones de dos registros
                    if isinstance(self.regRF.instruccion, (Sma, Rta, Mul, Y, O, Oex, Rig, Rip, Rim)):
                        if self.regRF.data is None:
                            self.regRF.data = [None, None]    
                        if self.forw_reg2 == 1:
                            self.regRF.data[0] = self.second_check
                        elif self.forw_reg2 == 2:
                            print(f"Forwarding al registro2")
                            print(f"Valor antes del forwarding: {self.regRF.data}")
                            print(f"Valor a recibir: {self.second_check}")
                            self.regRF.data[1] = self.second_check
                            
                            print(f"Después del forwarding: {self.regRF.data}")
                        
                        #Para instrucciones con inmediatos
                        elif isinstance(self.regRF.instruccion, (Smai, Rtai, Muli, Roti, Rotd, No, Rol, Modp, Mula)):
                            if self.regRF.data is None:
                                self.regRF.data = None
                            if self.forw_reg2 == 1:
                                self.regRF.data = self.second_check
                                print(f"Después del forwarding: {self.regRF.data}")
                                
                        elif isinstance(self.regRF.instruccion, Mix):
                            if self.forw_reg2 == 1:
                                print(f"Forwarding al registro1")
                                self.regRF.data[0] = self.second_check
                            elif self.forw_reg2 == 2:
                                print(f"Forwarding al registro2")
                                self.regRF.data[1] = self.second_check
                            elif self.forw_reg2 == 3:
                                print(f"Forwarding al registro3")
                                self.regRF.data[2] = self.second_check
                            
                            print(f"Después del forwarding: {self.regRF.data}")
                    second_hazard = False

                self.regRF.instruccion.ejecutar()
                
                self.pipeline_locations[2] = "Instrucción ejecutando"
                self.regALU.instruccion = self.regRF.instruccion
                self.memory_instruction_index = self.execute_instruction_index
                self.regRF.clear()
                self.execute_instruction_index = None
            else:
                print("No hay instrucción en esta etapa")
                self.pipeline_locations[2] = ""

            # DECODE
            print("----------------------")
            print(f"Etapa DECODE {self.PC-1} {self.regIM.instruccion.__class__.__name__}")
            if self.regIM.instruccion is not None:
                execute = True

                #para los branches 
                if isinstance(self.regIM.instruccion, (Rig, Rip, Rim)):
                    instruction_id = id(self.regIM.instruccion)
                    predicted_taken = self.branch_predictor.predict(instruction_id)
                    print(f"[Branch detectado - Predicción: {predicted_taken}")
                    
                    if predicted_taken:
                        print(f"[Tomando salto: PC += {self.regIM.instruccion.offset}")
                        self.PC += self.regIM.instruccion.offset
                
                #forwarding de execute
                if isinstance(self.regIM.instruccion, (Sma, Rta, Mul, Y, O, Oex, Rig, Rip, Rim, Smai, Rtai, Muli, Roti, Rotd, No, Rol, Modp, Mula, Mix, Crg)):
                    if self.hazard_control.exex_fw(self.regIM.instruccion):
                        print("Se detectó un hazard EX- Forwarding necesario")
                        
                        needs_forwarding = True
                    else:
                        print("No se detectó un hazard de EX")
                        needs_forwarding = False

                #revisa el forwarding de mem a execute
                if isinstance(self.regIM.instruccion, (Sma, Rta, Mul, Y, O, Oex, Rig, Rip, Rim, Smai, Rtai, Muli, Roti, Rotd, No, Rol, Modp, Mula, Mix)):
                    if self.hazard_control.memreg_forw(self.regIM.instruccion):
                        print("Se detectó un hazard de MEM - Forwarding necesario")
                        print(f"{self.second_check}")
                        
                        second_hazard = True
                    else:
                        print("No se detectó un hazard de MEM")
                        second_hazard = False
                    
                    
                # Verifica si debe insertar NOP (burbuja)
                if isinstance(self.regALU.instruccion, Crg) and (needs_forwarding or second_hazard):
                    print("Inserción de NOP por dependencia con Crg")

                    # Retroceder el PC para volver a ejecutar la instrucción que estaba en decode
                    self.PC -= 1

                    # Insertar NOP en la etapa de Decode actual
                    self.regRF.clear()
                    self.regIM.instruccion = Nop(self)
                    self.regRF.instruccion = self.regIM.instruccion

                    # No avanzar esta instrucción al pipeline todavía
                    time.sleep(0.1)

                else:
                    # Continuar flujo normal del decode
                    if isinstance(self.regIM.instruccion, (Sma, Rta, Mul, Y, O, Oex, Rig, Rip, Rim)):
                        if self.regRF.data is None:
                            self.regRF.data = [None, None]
                    elif isinstance(self.regIM.instruccion, (Smai, Rtai, Muli, Roti, Rotd, No, Rol, Modp, Mula)):
                        if self.regRF.data is None:
                            self.regRF.data = None
                    elif isinstance(self.regIM.instruccion, Mix):
                        if self.regRF.data is None:
                            self.regRF.data = [None, None, None]

                self.pipeline_locations[1] = f"Instrucción {self.PC - 1}"
                self.regIM.instruccion.ejecutar()
                #en estas 2 lineas debe de estar el error
                self.regRF.instruccion = self.regIM.instruccion
                self.execute_instruction_index = self.decode_instruction_index
                if isinstance(self.regIM.instruccion,  Rig):
                    print(f"{self.regRF.data}")
                    print(f"{self.regIM.data}")
                
                self.regIM.clear()
                self.decode_instruction_index = None

            else:
                print("No hay instrucción en esta etapa")
                self.pipeline_locations[1] = ""

            # FETCH
            print("----------------------")
            print(f"Etapa FETCH {self.PC}")

            if self.PC < len(self.IM.instrucciones):
                # NUEVA LÓGICA: Verificar si la instrucción a hacer fetch está en MEMORY o WRITEBACK
                if self.memory_instruction_index == self.PC or self.writeback_instruction_index == self.PC:
                    print(f"⚠️ STALL DETECTADO: La instrucción {self.PC} aún está en el pipeline (MEMORY o WRITEBACK)")
                    print(f"   Memory index: {self.memory_instruction_index}, Writeback index: {self.writeback_instruction_index}")
                    print(f"   Insertando NOP y retrocediendo PC")
                    
                    # Insertar NOP en lugar de hacer fetch
                    self.regIM.instruccion = Nop(self)
                    self.regIM.instruccion.reset()
                    self.decode_instruction_index = None
                    
                    # NO incrementar PC, queremos volver a intentar hacer fetch de esta instrucción
                    self.PC = self.PC  # Mantener PC igual
                    
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

            print("___________________________________________")
            print("_________________FIN CICLO_________________")

            # Calcular métricas de desempeño
            elapsed_time = self.time
            if elapsed_time > 0:
                cpi = self.total_cycles / max(1, self.instructions_completed)
                ipc = self.instructions_completed / max(1, self.total_cycles)
                clock_rate = self.total_cycles / (elapsed_time * 1e9)
            else:
                cpi, ipc, clock_rate = 0, 0, 0

            print(f"Total Cycles: {self.total_cycles}, Instructions Completed: {self.instructions_completed}, Elapsed Time: {elapsed_time}, Clock Rate: {clock_rate:.2e} GHz")
            print("___________________________________________")
            self.time += 20

            time.sleep(self.interval)

    def manejar_branch(self, branch_instruction):
        branch_instruction.ejecutar()

        actual_taken = self.regALU.data == 0
        print(f"Resultado real del salto: {actual_taken}")

        instruction_id = id(branch_instruction)
        predicted_taken = self.branch_predictor.predict(instruction_id)

        if predicted_taken != actual_taken:
            self.hazard_control.handle_misprediction(branch_instruction)

        self.branch_predictor.update(instruction_id, actual_taken)