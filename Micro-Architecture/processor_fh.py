import time
from components.alu import ALU
from components.data_memory import memoriaDatos
from components.instr_memory import memoriaInstrucciones
from components.register_file import archivoRegistros
from components.register import Registro
from instructions.rig import BranchEqual  
from hazard_control import HazardControl, BranchPredictor
from instructions.sma import Add
from instructions.rta import Sub
from instructions.y import And
from instructions.o import Or
from instructions.mul import MUL
from instructions.smai import Addi


class ProcesadorFullHazard:
    def __init__(self, interval=1):
        self.PC = 0
        self.forw_data = ""
        self.forw_reg = 0
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


    def cargarInstrucciones(self, instruccion):
        self.IM.instrucciones.append(instruccion)

    def clear_pipeline(self):
        """Limpia las etapas DECODE y EXECUTE del pipeline tras un salto."""
        print("Limpiando pipeline tras el salto.")
        time.sleep(0.1)
        self.regIM.clear()
        self.regRF.clear()

    def iniciarEjecucion(self):
        needs_forwarding = False
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
                self.regDM.instruccion.ejecutar()
                self.pipeline_locations[4] = "Instrucción escribiendo"
                self.regDM.clear()
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
                self.regALU.clear()
            else:
                print("No hay instrucción en esta etapa")
                self.pipeline_locations[3] = ""

            # EXECUTE
            print("----------------------")
            print(f"Etapa EXECUTE {self.PC-2}")
            if self.regRF.instruccion is not None:
                execute = True
                
                # Aplicar forwarding ANTES de ejecutar si es necesario
                if isinstance(self.regRF.instruccion, (Add, Sub, Or, And, MUL)) and needs_forwarding:
                    print(f"Aplicando forwarding en EXECUTE")
                    print(f"Valor a forwardear: {self.forw_data}")
                    
                    # Asegurarse de que regRF.data existe
                    if self.regRF.data is None:
                        self.regRF.data = [None, None]
                    
                    # Aplicar el forwarding al registro correspondiente
                    if self.forw_reg == 1:
                        print(f"Forwarding al registro1 (índice 0 de regRF.data)")
                        self.regRF.data[0] = self.forw_data
                    elif self.forw_reg == 2:
                        print(f"Forwarding al registro2 (índice 1 de regRF.data)")
                        self.regRF.data[1] = self.forw_data
                    
                    print(f"regRF.data después del forwarding: {self.regRF.data}")
                    needs_forwarding = False  # Reset flag
                    
                elif isinstance(self.regRF.instruccion, (Addi)) and needs_forwarding:
                    print(f"Aplicando forwarding en EXECUTE para Addi")
                    print(f"Valor a forwardear: {self.forw_data}")
                    
                    # Asegurarse de que regRF.data existe
                    if self.regRF.data is None:
                        self.regRF.data = None
                    
                    # Aplicar el forwarding al registro correspondiente
                    if self.forw_reg == 1:
                        print(f"Forwarding al registro1 (regRF.data)")
                        self.regRF.data = self.forw_data
                    
                    print(f"regRF.data después del forwarding: {self.regRF.data}")
                    needs_forwarding = False  # Reset flag
                
                # Ahora ejecutar la instrucción (instruccion2 usará los valores correctos)
                self.regRF.instruccion.ejecutar()

                self.pipeline_locations[2] = "Instrucción ejecutando"
                self.regALU.instruccion = self.regRF.instruccion
                self.regRF.clear()
            else:
                print("No hay instrucción en esta etapa")
                self.pipeline_locations[2] = ""

            # DECODE
            print("----------------------")
            print(f"Etapa DECODE {self.PC-1}")
            if self.regIM.instruccion is not None:
                execute = True
                
                # Detectar si hay hazard y necesitamos forwarding
                if self.hazard_control.reg_forw(self.regIM.instruccion):
                    print("Se detectó un hazard - Forwarding necesario")
                    needs_forwarding = True
                else:
                    print("No se detectó un hazard")
                    needs_forwarding = False

                if isinstance(self.regIM.instruccion, (Add, Sub, Or, And, MUL)):
                    # Instrucciones tipo R: lista de 2 elementos
                    if self.regRF.data is None:
                        self.regRF.data = [None, None]

                elif isinstance(self.regIM.instruccion, Addi):
                    # Instrucciones tipo I: valor escalar
                    if self.regRF.data is None:
                        self.regRF.data = None

                # Ejecutar la instrucción (instruccion1 - lectura de registros)
                self.pipeline_locations[1] = f"Instrucción {self.PC - 1}"
                self.regIM.instruccion.ejecutar()
                self.regRF.instruccion = self.regIM.instruccion
                self.regIM.clear()
            else:
                print("No hay instrucción en esta etapa")
                self.pipeline_locations[1] = ""

            # FETCH
            print("----------------------")
            print(f"Etapa FETCH {self.PC}")
            if self.PC < len(self.IM.instrucciones):
                execute = True
                print(f"Cargando instrucción {self.PC}")
                self.pipeline_locations[0] = f"Instrucción {self.PC}"
                self.regIM.instruccion = self.IM.instrucciones[self.PC]
                print(f"Instrucción cargada: {self.regIM.instruccion.__class__.__name__}")
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
        """Manejo del BranchEqual dentro del procesador."""
        branch_instruction.ejecutar()

        actual_taken = self.regALU.data == 0
        print(f"Resultado real del salto: {actual_taken}")

        instruction_id = id(branch_instruction)
        predicted_taken = self.branch_predictor.predict(instruction_id)

        if predicted_taken != actual_taken:
            self.hazard_control.handle_misprediction(branch_instruction)

        self.branch_predictor.update(instruction_id, actual_taken)