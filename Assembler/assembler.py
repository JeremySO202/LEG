import sys

def read_file(file_path):
    with open(file_path, 'r') as archivo:
        lineas = [linea.strip() for linea in archivo]
    return lineas

def write_file(file_path, lines):
    with open(file_path, 'w') as archivo:
        for linea in lines:
            archivo.write(linea + '\n')

opcodes = {
    'NOP': ["000000", "R"],
    'SMA': ["000001", "R"],
    'SMAI': ["000010", "I"],
    'RTA': ["000011", "R"],
    'RTAI': ["000100", "I"],
    'MUL': ["000101", "R"],
    'MULI': ["000110", "I"],
    'Y': ["000111", "R"],
    'O': ["001000", "R"],
    'OEX': ["001001", "R"],
    'ROTD': ["001010", "I"],
    'ROTI': ["001011", "I"],
    'NO': ["001100", "I"],
    'MOV': ["001101", "R"],
    'ROL': ["001110", "I"],
    'MODP': ["001111", "I"],
    'MIX': ["010000", "H"],
    "MULA": ["010001", "I"],
    "CRG": ["010010", "M"],
    "GRD": ["010011", "M"],
    'RIG': ["010100", "B"],
    'RIM': ["010101", "B"],
    'RIP': ["010110", "B"],
    'RIN': ["010111", "B"],
 #Falta agregar las instrucciones de vault
}

regs = {
    'L0': "0000",
    'L1': "0001",
    'L2': "0010",
    'L3': "0011",
    'L4': "0100",
    'L5': "0101",
    'L6': "0110",
    'L7': "0111",
    'L8': "1000",
    'L9': "1001",
    'L10': "1010",
    'L11': "1011",
    'L12': "1100",
    'L13': "1101",
    'L14': "1110",
    'L15': "1111"
}

vault = {
    'H0': "0000",
    'H1': "0001",
    'H2': "0010",
    'H3': "0011",
    'K0': "0100",
    'K1': "0101",
    'K2': "0110",
    'K3': "0111",
}

def extract_bytes(line):
    """Extracts bytes from a given line of assembly code."""

    line = line.upper()
    print("Processing line:", line)


    data = line.split(" ")
    
    data = [item for item in data if item != '']

    if data[0] in opcodes:
        instruction_parameter = opcodes[data[0]]
    else:
        raise ValueError("Unknown mnemonic: "+ data[0])

    opcode = instruction_parameter[0]

    if instruction_parameter[1] == 'R':
        
        if data[0] == 'NOP':
            return "0"*32
        
        if len(data) != 4:
            raise ValueError("Invalid number of parameters for R-type instruction: "+ line)
        
        # Check for vault register usage
        if data[1] in vault:
            raise ValueError("Invalid use of vault register in R-type instruction: "+ line)
        elif data[1] in regs:
            rd = regs[data[1]]
        else:
            raise ValueError("Unknown destination register: "+ data[1])
            
        if data[2] in vault:
            rs1= vault[data[2]]
            vrs1 = "1"  # Indicate rs1 is a vault register
        elif data[2] in regs:
            rs1 = regs[data[2]]
            vrs1 = "0"  # Indicate rs1 is a general-purpose register
        else:
            raise ValueError("Unknown source register 1: "+ data[2])
        if data[3] in vault:
            rs2= vault[data[3]]
            vrs2 = "1"  # Indicate rs2 is a vault register
        elif data[3] in regs:
            rs2 = regs[data[3]]
            vrs2 = "0"  # Indicate rs2 is a general-purpose register
        else:
            raise ValueError("Unknown source register 2: "+ data[3])

        return vrs1 + vrs2 + "0"*12 + rs2 + rs1 + opcode + rd
    
    if instruction_parameter[1] == 'B':
        
           
        
        if len(data) != 4:
            raise ValueError("Invalid number of parameters for B-type instruction: "+ line)
        
        if data[1] in regs:
            rd = regs[data[1]]
        else:
            raise ValueError("Unknown destination register: "+ data[1])
        
        if data[2] in regs:
            rs = regs[data[2]]
        else:
            raise ValueError("Unknown source register: "+ data[2])
        
        if not data[3].lstrip('-').isdigit():
            raise ValueError("Immediate value must be an integer: "+ data[3])
        if not -65536 <= int(data[3]) <= 65535:
            raise ValueError("Immediate value out of range (-65536 to 65535): "+ data[3])
        
         # Convert immediate to 16-bit two's complement binary
        if int(data[3]) < 0:
            imm = format((1 << 16) + int(data[3]), '016b')
        else:
            imm = format(int(data[3]), '016b')
        return "00"+imm + rs + opcode + rd
        
    if instruction_parameter[1] == 'M':
        
        if len(data) != 4:
            raise ValueError("Invalid number of parameters for M-type instruction: "+ line)
        
        if data[1] in regs:
            rd = regs[data[1]]
        else:
            raise ValueError("Unknown destination/source register: "+ data[1])
        
        if data[2] in regs:
            rs = regs[data[2]]
        else:
            raise ValueError("Unknown base register: "+ data[2])
        
        if not data[3].lstrip('-').isdigit():
            raise ValueError("Immediate value must be an integer: "+ data[3])
        if not -65536 <= int(data[3]) <= 65535:
            raise ValueError("Immediate value out of range (-65536 to 65535): "+ data[3])
        
         # Convert immediate to 16-bit two's complement binary
        if int(data[3]) < 0:
            imm = format((1 << 16) + int(data[3]), '016b')
        else:
            imm = format(int(data[3]), '016b')
        return "00"+imm + rs + opcode + rd
    if instruction_parameter[1] == 'I':
        
        if data[0] == 'NO':
            if len(data) != 3:
                raise ValueError("Invalid number of parameters for NO instruction: "+ line)
            
            if data[1] in regs:
                rd = regs[data[1]]
            else:
                raise ValueError("Unknown destination register: "+ data[1])
            if data[2] in vault:
                rs = vault[data[2]]
            elif data[2] in regs:
                rs = regs[data[2]]
            else:
                raise ValueError("Unknown source register: "+ data[2])
            
            return "00"+"0"*16 + rs + opcode + rd
        
        if len(data) != 4:
            raise ValueError("Invalid number of parameters for I-type instruction: "+ line)
        
        if data[1] in vault:
            raise ValueError("Invalid use of vault register in I-type instruction: "+ line)
        elif data[1] in regs:
            rd = regs[data[1]]
        else:
            raise ValueError("Unknown destination register: "+ data[1])

        if data[2] in vault:
            rs = vault[data[2]]
            vrs = "1"  # Indicate rs is a vault register
        elif data[2] in regs:
            rs = regs[data[2]]
            vrs = "0"  # Indicate rs is a general-purpose register
        else:
            raise ValueError("Unknown source register: "+ data[2])
        
        if not data[3].lstrip('-').isdigit():
            raise ValueError("Immediate value must be an integer: "+ data[3])
        if not -65536 <= int(data[3]) <= 65535:
            raise ValueError("Immediate value out of range (-65536 to 65535): "+ data[3])
        
         # Convert immediate to 17-bit two's complement binary
        if int(data[3]) < 0:
            imm = format((1 << 17) + int(data[3]), '017b')
        else:
            imm = format(int(data[3]), '017b')
        return vrs+imm + rs + opcode + rd
    
    if instruction_parameter[1] == 'H':

        if len(data) != 5:
            raise ValueError("Invalid number of parameters for H-type instruction: "+ line)
        
        if data[1] in vault:
            raise ValueError("Invalid use of vault register in H-type instruction: "+ line)
        elif data[1] in regs:
            rd = regs[data[1]]
        else:
            raise ValueError("Unknown destination register: "+ data[1])
        
        if data[2] in vault and data[3] in vault and data[4] in vault:
            rs1 = vault[data[2]]
            rs2 = vault[data[3]]
            rs3 = vault[data[4]]
            vrs = "1"
        elif data[2] in regs and data[3] in regs and data[4] in regs:
            rs1 = regs[data[2]]
            rs2 = regs[data[3]]
            rs3 = regs[data[4]]
            vrs = "0"
        else:
            raise ValueError("All source registers must be of the same type (either all vault or all general-purpose): "+ line)
        
        return vrs + "0"*9 + rs3 + rs2 + rs1 + opcode + rd

def assembler(file_path, output_file):
    """Main function to assemble the code from the given file path."""
    lines = read_file(file_path)    

    binary_lines = []

    for line in lines:
        binary_line = extract_bytes(line)
        binary_lines.append(binary_line)

    write_file(output_file, binary_lines)
    print(f"Assembly completed. Output written to {output_file}")
    return binary_lines

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python assembler.py <assembly_file> <output_file>")
        sys.exit(1)

    assembly_file = sys.argv[1]
    output_file = sys.argv[2]

    print("Assembler started...")
    binary_lines = assembler(assembly_file, output_file)
