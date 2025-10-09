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
    'RTAI': ["000100", "R"],
    'MUL': ["000101", "R"],
    'MULI': ["000110", "I"],
    'Y': ["000111", "R"],
    'O': ["001000", "R"],
    'OEX': ["001001", "R"],
    'ROTD': ["001010", "I"],
    'ROTI': ["001011", "I"],
    'NO': ["001100", "R"],
    'MOV': ["001101", "R"]

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

    if instruction_parameter[1] == 'R':
        
        if data[0] == 'NOP':
            return "0"*32
        
        elif data[0] == 'SMA':
            if len(data) != 4:
                raise ValueError("Invalid number of parameters for SMA instruction: "+ line)
            if data[1] in regs and data[2] in regs and data[3] in regs:
                opcode = instruction_parameter[0]
                rd = regs[data[1]]
                rs1 = regs[data[2]]
                rs2 = regs[data[3]]
                return "0"*14 + rs2 + rs1 + opcode + rd
            else:
                raise ValueError("Invalid register in SMA instruction: "+ line)
        
        elif data[0] == 'RTA':
            if len(data) != 4:
                raise ValueError("Invalid number of parameters for RTA instruction: "+ line)
            if data[1] in regs and data[2] in regs and data[3] in regs:
                opcode = instruction_parameter[0]
                rd = regs[data[1]]
                rs1 = regs[data[2]]
                rs2 = regs[data[3]]
                return "0"*14 + rs2 + rs1 + opcode + rd
            else:
                raise ValueError("Invalid register in RTA instruction: "+ line)
        
        elif data[0] == 'RTAI':
            if len(data) != 4:
                raise ValueError("Invalid number of parameters for RTAI instruction: "+ line)
            if data[1] in regs and data[2] in regs and data[3] in regs:
                opcode = instruction_parameter[0]
                rd = regs[data[1]]
                rs1 = regs[data[2]]
                rs2 = regs[data[3]]
                return "0"*14 + rs2 + rs1 + opcode + rd
            else:
                raise ValueError("Invalid register in RTAI instruction: "+ line)
        
        elif data[0] == 'MUL':
            if len(data) != 4:
                raise ValueError("Invalid number of parameters for MUL instruction: "+ line)
            if data[1] in regs and data[2] in regs and data[3] in regs:
                opcode = instruction_parameter[0]
                rd = regs[data[1]]
                rs1 = regs[data[2]]
                rs2 = regs[data[3]]
                return "0"*14 + rs2 + rs1 + opcode + rd
            else:
                raise ValueError("Invalid register in MUL instruction: "+ line)
        
        elif data[0] == 'Y':
            if len(data) != 4:
                raise ValueError("Invalid number of parameters for Y instruction: "+ line)
            if data[1] in regs and data[2] in regs and data[3] in regs:
                opcode = instruction_parameter[0]
                rd = regs[data[1]]
                rs1 = regs[data[2]]
                rs2 = regs[data[3]]
                return "0"*14 + rs2 + rs1 + opcode + rd
            else:
                raise ValueError("Invalid register in Y instruction: "+ line)
        
        elif data[0] == 'O':
            if len(data) != 4:
                raise ValueError("Invalid number of parameters for O instruction: "+ line)
            if data[1] in regs and data[2] in regs and data[3] in regs:
                opcode = instruction_parameter[0]
                rd = regs[data[1]]
                rs1 = regs[data[2]]
                rs2 = regs[data[3]]
                return "0"*14 + rs2 + rs1 + opcode + rd
            else:
                raise ValueError("Invalid register in O instruction: "+ line)
        
        elif data[0] == 'OEX':
            if len(data) != 4:
                raise ValueError("Invalid number of parameters for OEX instruction: "+ line)
            if data[1] in regs and data[2] in regs and data[3] in regs:
                opcode = instruction_parameter[0]
                rd = regs[data[1]]
                rs1 = regs[data[2]]
                rs2 = regs[data[3]]
                return "0"*14 + rs2 + rs1 + opcode + rd
            else:
                raise ValueError("Invalid register in OEX instruction: "+ line)
        
        elif data[0] == 'NO':
            if len(data) != 4:
                raise ValueError("Invalid number of parameters for NO instruction: "+ line)
            if data[1] in regs and data[2] in regs and data[3] in regs:
                opcode = instruction_parameter[0]
                rd = regs[data[1]]
                rs1 = regs[data[2]]
                rs2 = regs[data[3]]
                return "0"*14 + rs2 + rs1 + opcode + rd
            else:
                raise ValueError("Invalid register in NO instruction: "+ line)
        
        elif data[0] == 'MOV':
            if len(data) != 4:
                raise ValueError("Invalid number of parameters for MOV instruction: "+ line)
            if data[1] in regs and data[2] in regs and data[3] in regs:
                opcode = instruction_parameter[0]
                rd = regs[data[1]]
                rs1 = regs[data[2]]
                rs2 = regs[data[3]]
                return "0"*14 + rs2 + rs1 + opcode + rd
            else:
                raise ValueError("Invalid register in MOV instruction: "+ line)
        
        else:
            raise ValueError("Unknown R-type instruction: "+ data[0])
               
    if instruction_parameter[1] == 'I':
        
        if data[0] == 'SMAI':
            if len(data) != 4:
                raise ValueError("Invalid number of parameters for SMAI instruction: "+ line)
            if data[1] in regs and data[2] in regs and data[3].isdigit():
                opcode = instruction_parameter[0]
                rd = regs[data[1]]
                rs1 = regs[data[2]]
                imm = format(int(data[3]), '018b')
                return imm + rs1 + opcode + rd
            else:
                raise ValueError("Invalid register or immediate value in SMAI instruction: "+ line)
        
        elif data[0] == 'MULI':
            if len(data) != 4:
                raise ValueError("Invalid number of parameters for MULI instruction: "+ line)
            if data[1] in regs and data[2] in regs and data[3].isdigit():
                opcode = instruction_parameter[0]
                rd = regs[data[1]]
                rs1 = regs[data[2]]
                imm = format(int(data[3]), '018b')
                return imm + rs1 + opcode + rd
            else:
                raise ValueError("Invalid register or immediate value in MULI instruction: "+ line)
        
        elif data[0] == 'ROTD':
            if len(data) != 4:
                raise ValueError("Invalid number of parameters for ROTD instruction: "+ line)
            if data[1] in regs and data[2] in regs and data[3].isdigit():
                opcode = instruction_parameter[0]
                rd = regs[data[1]]
                rs1 = regs[data[2]]
                imm = format(int(data[3]), '018b')
                return imm + rs1 + opcode + rd
            else:
                raise ValueError("Invalid register or immediate value in ROTD instruction: "+ line)
        
        elif data[0] == 'ROTI':
            if len(data) != 4:
                raise ValueError("Invalid number of parameters for ROTI instruction: "+ line)
            if data[1] in regs and data[2] in regs and data[3].isdigit():
                opcode = instruction_parameter[0]
                rd = regs[data[1]]
                rs1 = regs[data[2]]
                imm = format(int(data[3]), '018b')
                return imm + rs1 + opcode + rd
            else:
                raise ValueError("Invalid register or immediate value in ROTI instruction: "+ line)
        
        else:
            raise ValueError("Unknown I-type instruction: "+ data[0])

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
