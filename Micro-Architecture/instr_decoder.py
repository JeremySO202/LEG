from instructions.rig import BranchEqual
from instructions.crg import LoadWord
from instructions.grd import StoreWord
from instructions.sma import Sma
from instructions.smai import Smai
from instructions.rta import Rta
from instructions.rtai import Rtai
from instructions.y import Y
from instructions.o import O
from instructions.mov import Mov
from instructions.mul import Mul
from instructions.muli import Muli
from instructions.mix import Mix
from instructions.oex import Oex
from instructions.rotd import Rotd
from instructions.roti import Roti
from instructions.no import No
from instructions.nop import Nop

class Inst_Decoder:
    
    """ CORE INSTRUCTION FORMATS
        |TYPE| 31-22|21-18|17-14|13-10|9-4|3-0|
        |---|---|---|---|---|---|---|
        | R ||X(14) | RS2(4) | RS1(4) | OPC(6) | RD(4)
        | B |||OFFSET(18)  |RS2(4) | OPC(6) | RS1(4)
        | M |||OFFSET(18)  |BASE(4) | OPC(6) | RS/RD(4)
        | I |||IMM(18)  |RS1(4) | OPC(6) | RD(4)
        | H |X(10) | RS3(4) | RS2(4) | RS1(4) | OPC(6) | RD(4)
        | V | """
        
    def __init__(self):
        #self.processor = _processor
        self.R_instructions = {
            "000000": "Nop",
            "000001": "Sma",
            "000011": "Rta",
            "000101": "Mul",
            "000111": "Y",
            "001000": "O",
            "001001": "Oex",
            "001100": "No"
        }

        self.I_instructions = {
            "000010": "Smai",
            "000100": "Rtai",
            "000110": "Muli",
            "001010": "Rotd",
            "001011": "Roti",
            "001110": "Rol",
            "001111": "Modp",
            "010001": "Mula",
            "001101": "Mov"
        }

        self.B_instructions = {
            "010100": "Rig",
            "010101": "Rim",
            "010110": "Rip",
            "010111": "Rin"
        }

        self.H_instructions = {
            "010000": "Mix",
            "001110": "Rol",
            "001111": "Modp",
            "010001": "Mula"
        }

        self.V_instructions = {}

        self.M_instructions = {
            "010010": "Crg",
            "010011": "Grd"
        }
        
        self.instructions  = {
            "R": self.R_instructions,
            "I": self.I_instructions,
            "B": self.B_instructions,
            "H": self.H_instructions,
            "V": self.V_instructions,
            "M": self.M_instructions
        }
        
    def load_code(self, assembled_code, processor):
        for line in assembled_code:
            instruction = self.get_instruction(line, processor)
            if instruction:
                processor.cargarInstrucciones(instruction)
        return 0
        
    def get_instruction(self, code_line, processor):
        mnemonic, instruction_type = self.get_mnemonic_and_type(code_line) 
        if mnemonic is None:
            print(f"[ERROR] Opcode desconocido en línea: {code_line}")
            return None

        # Obtener la clase correspondiente (si existe)
        if mnemonic not in globals():
            print(f"[ERROR] No existe clase para instrucción '{mnemonic}'")
            return None
        
        cls = globals()[mnemonic]
        
        if instruction_type == "R":          
            #| R ||X(14) | RS2(4) | RS1(4) | OPC(6) | RD(4)
            rs1 = int(code_line[14:18],2)
            rs2 = int(code_line[18:22],2)
            rd = int(code_line[28:32],2)
            if mnemonic == "No":
                print(f"{mnemonic} L{rd}, L{rs1}")
                return cls(rd, rs1, processor)
            elif mnemonic == "Nop":
                print(f"{mnemonic}")
                return cls(processor)
            else:
                print(f"{mnemonic} L{rd}, L{rs1}, L{rs2}")
                return cls(rd, rs1, rs2, processor)
        elif instruction_type == "I":
            #| I |||IMM(18)  |RS1(4) | OPC(6) | RD(4)
            imm = int(code_line[1:18],2)
            rs1 = int(code_line[18:22],2)
            rd = int(code_line[28:32],2)
            if mnemonic == "Mov":
                print(f"{mnemonic} L{rd} #{imm}")
                return cls(rd, imm, processor)
            elif mnemonic == "Modp":
                print(f"{mnemonic} L{rd} L{rs1}")
                return cls(rd, rs1, processor)
            else:
                print(f"{mnemonic} L{rd} L{rs1} #{imm}")
                return cls(rd, rs1, imm, processor)
        elif instruction_type == "M":
            #| M |||OFFSET(18)  |BASE(4) | OPC(6) | RS/RD(4)
            offset = int(code_line[1:18],2)
            base = int(code_line[18:22],2)
            rd = int(code_line[28:32],2)
            print(f"{mnemonic} L{rd} (L{base} + #{offset})")
            if mnemonic == "Crg":  # Load
                return cls(rd, offset, base, processor)
            else:  # Store
                return cls(base, offset, rd, processor)
            # este necesita revisión
        elif instruction_type == "B":
            #| B |||OFFSET(18)  |RS2(4) | OPC(6) | RS1(4)
            offset = int(code_line[1:18],2)
            rs2 = int(code_line[18:22],2)
            rs1 = int(code_line[28:32],2)
            print(f"{mnemonic} L{rs1} L{rs2} #{offset}")
            return cls(rs1, rs2, offset, processor)
            # este necesita revisión
        elif instruction_type == "H":
           #| H |X(10) | RS3(4) | RS2(4) | RS1(4) | OPC(6) | RD(4)
            rs3 = code_line[10:14]
            rs2 = code_line[14:18]
            rs1 = code_line[18:22]
            rd = code_line[28:32]
            print(f"{mnemonic} L{rd} L{rs1} L{rs2} L{rs3}")
            return cls(rd, rs1, rs2, rs3, processor)
            # este necesita revisión
        return 0
    
    def get_mnemonic_and_type(self, code_line):
        opcode = code_line[22:28]
        for inst_type, dic in self.instructions.items():
            if opcode in dic:
                #print(f"El valor {opcode} está en el diccionario {inst_type} con instrucción '{dic[opcode]}'.")
                return dic[opcode], inst_type
        return None, None
            
            


