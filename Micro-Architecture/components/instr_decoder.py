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
        
    def __init__(self, _processor):
        self.processor = _processor
        self.R_instructions = {
            "000001": "Sma",
            "000011": "Rta",
            "000101": "Mul",
            "000111": "Y",
            "001000": "O",
            "001001": "OEX",
            "001100": "No",
            "001101": "Mov"
        }

        self.I_instructions = {
            "000001": "Smai",
            "000100": "Rtai",
            "000110": "Muli",
            "001010": "Rotd",
            "001011": "Roti",
            "001110": "Rol",
            "001111": "Modp",
            "010001": "Mula"
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
        
    def get_opcode(self, instruction):
        opcode = instruction[9:4]
        for inst_type, dic in self.instructions.items():
            if opcode in dic:
                print(f"El valor {opcode} está en el diccionario {inst_type}.")
                break
        else:
            print(f"El valor {opcode} no se encuentra en ningún diccionario.")
