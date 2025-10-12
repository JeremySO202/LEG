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
    'ROTD': ["001010", "R"],
    'ROTI': ["001011", "R"],
    'NO': ["001100", "I"],
    'MOV': ["001101", "I"],
    'ROL': ["001110", "I"],
    'MODP': ["001111", "I"],
    'MIX': ["010000", "H"],
    "MULA": ["010001", "I"],
    "CRG": ["010010", "M"],
    "GRD": ["010011", "M"],
    'RIG': ["010100", "B"],
    'RIM': ["010101", "B"],
    'RIP': ["010110", "B"],
    'GRDH': ["010111", "V"],
    'GRDK': ["011000", "V"],
    'FRM': ["011001", "I"],
    'CHKF': ["011010", "R"]
    
    
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
    'K3': "0111"
}

def _parse_line(line):
    """Parse assembly line into tokens and get instruction info."""
    # Remove comments (everything after #)
    if '#' in line:
        line = line[:line.index('#')]
    
    # Convert to uppercase and strip whitespace
    line = line.upper().strip()
    print("Processing line:", line)
    
    # Skip empty lines after comment removal
    if not line:
        return None, None, None
    
    data = [item for item in line.split(" ") if item != '']
    
    if not data:
        return None, None, None
    
    if data[0] not in opcodes:
        raise ValueError("Unknown mnemonic: " + data[0])
    
    instruction_parameter = opcodes[data[0]]
    opcode = instruction_parameter[0]
    instr_type = instruction_parameter[1]
    
    return data, opcode, instr_type

def _validate_register(reg, reg_type="register", allow_vault=True):
    """Validate register and return its binary representation and vault flag."""
    if reg in regs:
        return regs[reg], "0"
    elif allow_vault and reg in vault:
        return vault[reg], "1"
    else:
        reg_types = "register" if not allow_vault else "register or vault"
        raise ValueError(f"Unknown {reg_type}: {reg}")

def _validate_immediate_signed(value_str, bits=16):
    """Validate signed immediate value and convert to binary."""
    if not value_str.lstrip('-').isdigit():
        raise ValueError(f"Immediate value must be a signed integer: {value_str}")
    
    value = int(value_str)
    max_val = (1 << (bits - 1)) - 1  # 32767 for 16-bit
    min_val = -(1 << (bits - 1))     # -32768 for 16-bit
    
    if not min_val <= value <= max_val:
        raise ValueError(f"Immediate value out of range ({min_val} to {max_val}): {value_str}")
    
    if value < 0:
        return format((1 << bits) + value, f'0{bits}b')
    else:
        return format(value, f'0{bits}b')

def _validate_immediate_unsigned(value_str, bits=16):
    """Validate unsigned immediate value and convert to binary."""
    if not value_str.isdigit():
        raise ValueError(f"Immediate value must be an unsigned integer: {value_str}")
    
    value = int(value_str)
    max_val = (1 << bits) - 1  # 65535 for 16-bit, 3 for 2-bit
    
    if not 0 <= value <= max_val:
        raise ValueError(f"Immediate value out of range (0 to {max_val}): {value_str}")
    
    return format(value, f'0{bits}b')

def extract_bytes(line):
    """Extracts bytes from a given line of assembly code."""
    data, opcode, instr_type = _parse_line(line)
    
    # Skip empty lines or comment-only lines
    if data is None:
        return None

    if instr_type == 'R':
        if data[0] == 'NOP':
            return "0" * 32
        
        if len(data) != 4:
            raise ValueError("Invalid number of parameters for R-type instruction: " + line)
        
        # Destination register (no vault allowed)
        rd, _ = _validate_register(data[1], "destination register", allow_vault=False)
        
        # Source registers (vault allowed)
        rs1, vrs1 = _validate_register(data[2], "source register 1")
        rs2, vrs2 = _validate_register(data[3], "source register 2")

        return vrs1 + vrs2 + "0" * 12 + rs2 + rs1 + opcode + rd
    
    if instr_type == 'B':
        if len(data) != 4:
            raise ValueError("Invalid number of parameters for B-type instruction: " + line)
        
        # Registers (no vault allowed for B-type)
        rd, _ = _validate_register(data[1], "destination register", allow_vault=False)
        rs, _ = _validate_register(data[2], "source register", allow_vault=False)
        
        # Signed immediate
        imm = _validate_immediate_signed(data[3])
        
        return "00" + imm + rs + opcode + rd
        
    if instr_type == 'M':
        if len(data) != 4:
            raise ValueError("Invalid number of parameters for M-type instruction: " + line)
        
        # Registers (no vault allowed for M-type)
        rd, _ = _validate_register(data[1], "destination/source register", allow_vault=False)
        rs, _ = _validate_register(data[2], "base register", allow_vault=False)
        
        # Signed immediate
        imm = _validate_immediate_signed(data[3])
        
        return "00" + imm + rs + opcode + rd
    
    if instr_type == 'I':
        # Special case: NO instruction
        if data[0] in ('NO', 'MULA', 'MODP'):
            if len(data) != 3:
                raise ValueError("Invalid number of parameters for NO instruction: " + line)
            
            rd, _ = _validate_register(data[1], "destination register", allow_vault=False)
            rs, _ = _validate_register(data[2], "source register")
            
            return "00" + "0" * 16 + rs + opcode + rd

        # Special case: MOV instruction
        if data[0] == 'MOV':
            if len(data) != 3:
                raise ValueError("Invalid number of parameters for MOV instruction: " + line)

            rd, _ = _validate_register(data[1], "destination register", allow_vault=False)
            imm = _validate_immediate_unsigned(data[2])
            
            return "00" + imm + "0000" + opcode + rd
        elif data[0] == 'FRM':
            if len(data) != 4:
                raise ValueError("Invalid number of parameters for FRM instruction: " + line)
            
            rd, _ = _validate_register(data[1], "destination register", allow_vault=False)
            rs, vrs = _validate_register(data[2], "source register")
            index = _validate_immediate_unsigned(data[3], bits=2)
            
            return "0"*16 + index + rs + opcode + rd
        # Regular I-type instructions
        if len(data) != 4:
            raise ValueError("Invalid number of parameters for I-type instruction: " + line)
        
        rd, _ = _validate_register(data[1], "destination register", allow_vault=False)
        rs, vrs = _validate_register(data[2], "source register")
        imm = _validate_immediate_unsigned(data[3])
        
        return vrs + "0" + imm + rs + opcode + rd
    
    if instr_type == 'H':
        if len(data) != 5:
            raise ValueError("Invalid number of parameters for H-type instruction: " + line)
        
        # Destination register (no vault allowed)
        rd, _ = _validate_register(data[1], "destination register", allow_vault=False)
        
        # All source registers must be same type (all vault or all regular)
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
            raise ValueError("All source registers must be of the same type (either all vault or all general-purpose): " + line)
        
        return vrs + "0" * 9 + rs3 + rs2 + rs1 + opcode + rd

    if instr_type == 'V':
        if len(data) != 3:
            raise ValueError("Invalid number of parameters for V-type instruction: " + line)
        
        rs, _ = _validate_register(data[1], "source register", allow_vault=False)
        index_bits = _validate_immediate_unsigned(data[2], bits=2)
        
        return "0" * 20 + index_bits + opcode + rs
    
    raise ValueError(f"Unknown instruction type: {instr_type}")

def assembler(file_path, output_file):
    """Main function to assemble the code from the given file path."""
    lines = read_file(file_path)

    binary_lines = []

    for line in lines:
        binary_line = extract_bytes(line)
        # Only add non-None lines (skip comments and empty lines)
        if binary_line is not None:
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
