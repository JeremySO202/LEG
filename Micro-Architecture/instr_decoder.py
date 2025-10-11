#register-register
from instructions.nop import Nop
from instructions.sma import Sma
from instructions.rta import Rta
from instructions.mul import Mul
from instructions.y import Y
from instructions.o import O
from instructions.oex import Oex
from instructions.mov import Mov
from instructions.chkf import Chkf

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



class Inst_Decoder:
    
    """ CORE INSTRUCTION FORMATS
            |TYPE| 31 |30| 29-22|21-18|17-14|13-10|9-4|3-0|
            |---|---|---|---|---|---|---|---|---|
            | R | VRS2 |VRS1||X(12) | RS2(4) | RS1(4) | OPC(6) | RD(4)
            | B |X|X|||OFFSET(16)  |RS2(4) | OPC(6) | RS1(4)
            | M |X|X|||OFFSET(16)  |BASE(4) | OPC(6) | RS/RD(4)
            | I | VRS |X|||IMM(16)  |RS(4) | OPC(6) | RD(4)
            | H |VRS||X(9) | RS3(4) | RS2(4) | RS1(4) | OPC(6) | RD(4)
            | V |||||||"""
                
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
            "011010": "Chkf"
            
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
            "001101": "Mov",
            "001100": "No",
            "001110": "Rol",
            "001111": "Modp",
            "010001": "Mula",
            "011001": "Frm"
        }

        self.B_instructions = {
            "010100": "Rig",
            "010101": "Rim",
            "010110": "Rip"
        }

        self.H_instructions = {
            "010000": "Mix"
        }

        

        self.M_instructions = {
            "010010": "Crg",
            "010011": "Grd"
        }
        
        self.V_instructions = {
            "010111": "Grdh",
            "011000": "Grdk"
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
            #| R | VRS2 |VRS1| X(8) | RS2(4) | RS1(4) | OPC(6) | RD(4)|
            vrs2 = int(code_line[31-31:31-30],2) # Bit 31
            vrs1 = int(code_line[31-30:31-29],2) # Bit 30
            rs2 = int(code_line[31-17:31-13],2)  # Bits 17-14
            rs1 = int(code_line[31-13:31-9],2)   # Bits 13-10
            rd = int(code_line[31-3:32],2)       # Bits 3-0
            if mnemonic == "Nop":
                print(f"{mnemonic}")
                return cls(processor)
            elif mnemonic == 'Chkf':
                print(f"{mnemonic} R{rd}, L{rs1}, L{rs2}")
                return cls(rd, rs1, rs2, processor)
            else:

                print(f"{mnemonic} R{rd}, {'V' if vrs1 else 'L'}{rs1}, {'V' if vrs2 else 'L'}{rs2}")
                return cls(rd, rs1, rs2, vrs1, vrs2, processor)
        elif instruction_type == "I":
            #| I | VRS | X | IMM(16)  |RS(4) | OPC(6) | RD(4)|
            vrs = int(code_line[31-31:31-30],2)  # Bit 31
            imm = int(code_line[31-29:31-13],2)  # Bits 29-14 (16 bits)
            if imm >= 2**15:  # Si el bit más significativo es 1, es negativo
                imm -= 2**16  # Convertir a negativo usando complemento a dos
            rs1 = int(code_line[31-13:31-9],2)   # Bits 13-10
            rd = int(code_line[31-3:32],2)       # Bits 3-0
            if mnemonic == "No":
                print(f"{mnemonic} L{rd}, {'V' if vrs else 'L'}{rs1}")
                return cls(rd, rs1, vrs, processor)
            elif mnemonic == "Mov":
                print(f"{mnemonic} L{rd} #{imm}")
                return cls(rd, imm, processor)
            elif mnemonic == "Modp":
                print(f"{mnemonic} L{rd} {'V' if vrs else 'L'}{rs1}")
                return cls(rd, rs1, vrs, processor)
            elif mnemonic == "Mula":
                print(f"{mnemonic} L{rd} {'V' if vrs else 'L'}{rs1}")
                return cls(rd, rs1, vrs, processor)
            elif mnemonic == "Frm":
                imm = int(code_line[31-29:31-13],2)  # Bits 29-14 (16 bits)
                print(f"{mnemonic} R{rd}, R{rs1}, #{imm}")
                return cls(rd, rs1, imm, processor)
            else:
                print(f"{mnemonic} L{rd} {'V' if vrs else 'L'}{rs1} #{imm}")
                return cls(rd, rs1, imm, vrs, processor)
        elif instruction_type == "M":
            #| M |X|X| OFFSET(16)  |BASE(4) | OPC(6) | RS/RD(4)|
            offset = int(code_line[31-29:31-13],2)  # Bits 29-14 (16 bits)
            if offset >= 2**15:  # Si el bit más significativo es 1, es negativo
                offset -= 2**16  # Convertir a negativo usando complemento a dos
            base = int(code_line[31-13:31-9],2)     # Bits 13-10
            rd = int(code_line[31-3:32],2)          # Bits 3-0
            print(f"{mnemonic} L{rd} (L{base} + #{offset})")
            if mnemonic == "Crg":  # Load
                return cls(rd, offset, base, processor)
            else:  # Store
                return cls(base, offset, rd, processor)
            # este necesita revisión
        elif instruction_type == "B":
            #| B |X|X| OFFSET(16)  |RS2(4) | OPC(6) | RS1(4)|
            offset = int(code_line[31-29:31-13],2)  # Bits 29-14 (16 bits)
            if offset >= 2**15:  # Si el bit más significativo es 1, es negativo
                offset -= 2**16  # Convertir a negativo usando complemento a dos
            rs2 = int(code_line[31-13:31-9],2)      # Bits 13-10
            rs1 = int(code_line[31-3:32],2)         # Bits 3-0
            print(f"{mnemonic} L{rs1} L{rs2} #{offset}")
            return cls(rs1, rs2, offset, processor)
            # este necesita revisión
        elif instruction_type == "H":
           #| H |VRS| X(9) | RS3(4) | RS2(4) | RS1(4) | OPC(6) | RD(4)|
            vrs = int(code_line[31-31:31-30],2)   # Bit 31
            rs3 = int(code_line[31-21:31-17],2)   # Bits 21-18
            rs2 = int(code_line[31-17:31-13],2)   # Bits 17-14
            rs1 = int(code_line[31-13:31-9],2)    # Bits 13-10
            rd = int(code_line[31-3:32],2)        # Bits 3-0
            if vrs == 0:
                print(f"{mnemonic} L{rd} L{rs1} L{rs2} L{rs3}")
            else:
                print(f"{mnemonic} R{rd} V{rs1} V{rs2} V{rs3}")
            return cls(rd, rs1, rs2, rs3, vrs, processor)
            # este necesita revisión
        
        elif instruction_type == "V":
           #| V | | | | | X(20) | INDEX(2) | OPC(6) | RS(4) |
            index = int(code_line[31-11:31-9],2)   # Bits 11-10
            rs = int(code_line[31-3:32],2)        # Bits 3-0
            print(f"{mnemonic} R{rs} #{index}")
            return cls(rs, index, processor)
            
        return 0
    
    def get_mnemonic_and_type(self, code_line):
        opcode = code_line[31-9:31-3]  # Bits 9-4 (6 bits)
        for inst_type, dic in self.instructions.items():
            if opcode in dic:
                #print(f"El valor {opcode} está en el diccionario {inst_type} con instrucción '{dic[opcode]}'.")
                return dic[opcode], inst_type
        return None, None
            
            


