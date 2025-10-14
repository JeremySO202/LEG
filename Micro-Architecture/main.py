from instr_decoder import Inst_Decoder
from processor_fh import ProcesadorFullHazard

import sys
from pathlib import Path

def load_code_from_file(file_path, processor):
        p = Path(file_path).expanduser()
        if not p.is_file():
            print(f"Error: The file {file_path} does not exist.")
            return False

        lines = []
        with p.open('r', encoding='utf-8') as f:
            for i, raw in enumerate(f, 1):
                s = raw.strip()
                if not s:
                    continue
                if len(s) != 32 or any(c not in '01' for c in s):
                    print(f"Error: Invalid instruction format on line {i}: '{raw.strip()}'")
                    return False
                lines.append(s)
        if not lines:
            print("Error: No valid instructions found in the file.")
            return False
        decoder = Inst_Decoder()
        decoder.load_code(lines, processor)
        return True

def load_file_to_memory(file_path, processor):
    # Carga cualquier archivo en la memoria del procesador en bloques de 64 bits.
    p = Path(file_path).expanduser()
    if not p.is_file():
        print(f"Error: The file {file_path} does not exist.")
        return False

    try:
        # Leer archivo como bytes
        with p.open('rb') as f:
            file_bytes = f.read()
        
        if not file_bytes:
            print("Error: The file is empty.")
            return False
        
        print(f"Loading {len(file_bytes)} bytes from {file_path} into memory...")
        
        # Pedir la key de 64 bits
        while True:
            try:
                key_input = input("Enter a 64-bit key (hex format, e.g., 0x123456789ABCDEF0 or decimal): ").strip()
                
                # Validar formato hexadecimal o decimal
                if key_input.lower().startswith('0x'):
                    key_64bit = int(key_input, 16)
                else:
                    key_64bit = int(key_input)
                
                # Validar que esté dentro del rango de 64 bits
                if not 0 <= key_64bit <= 0xFFFFFFFFFFFFFFFF:
                    print("Error: Key must be within 64-bit range (0 to 0xFFFFFFFFFFFFFFFF)")
                    continue
                
                print(f"Key accepted: 0x{key_64bit:016X}")
                break
                
            except ValueError:
                print("Error: Invalid key format. Please enter a valid number in hex (0x...) or decimal format.")
                continue
        
        # Convertir bytes a bits y agrupar en bloques de 64 bits
        # Memory[0] = tamaño, Memory[1] = key, Memory[2+] = datos del archivo
        memory_address = 2
        
        # Procesar de 8 en 8 bytes (64 bits cada bloque)
        for i in range(0, len(file_bytes), 8):
            # Tomar hasta 8 bytes del archivo
            chunk = file_bytes[i:i+8]
            
            # Si el chunk es menor a 8 bytes, rellenar con ceros
            if len(chunk) < 8:
                chunk = chunk + b'\x00' * (8 - len(chunk))
            
            # Convertir los 8 bytes a un entero de 64 bits (big-endian)
            value_64bit = int.from_bytes(chunk, byteorder='big')
            
            # Cargar en la memoria del procesador
            processor.DM.datos[memory_address] = value_64bit
            
            print(f"Memory[{memory_address}] = 0x{value_64bit:016X}")
            memory_address += 1
        
        # Guardar el tamaño de los datos del archivo en Memory[0]
        file_data_blocks = memory_address - 2
        processor.DM.datos[0] = file_data_blocks
        
        # Guardar la key en Memory[1]
        processor.DM.datos[1] = key_64bit
        
        print(f"Memory layout:")
        print(f"  Memory[0] = {file_data_blocks} (file data blocks)")
        print(f"  Memory[1] = 0x{key_64bit:016X} (64-bit key)")
        print(f"  Memory[2-{memory_address-1}] = file data ({file_data_blocks} blocks)")
        print(f"Successfully loaded file and key into memory.")
        return True
        
    except Exception as e:
        print(f"Error loading file to memory: {e}")
        return False

def save_file_from_memory(file_path, processor):
    # Guarda el contenido de la memoria del procesador en un archivo en bloques de 64 bits
    p = Path(file_path).expanduser()
    try:
        with p.open('wb') as f:
            # Leer la cantidad de bloques de datos del archivo desde Memory[0]
            file_data_blocks = processor.DM.datos[0] + 4
            key_64bit = processor.DM.datos[1]
            
            print(f"Saving {file_data_blocks } data blocks from memory to {file_path}...")
            print(f"Key used during processing: 0x{key_64bit:016X}")
            
            # Solo guardar los datos del archivo (Memory[2] en adelante)
            for address in range(2, 2 + file_data_blocks):
                value_64bit = processor.DM.datos[address]
                
                # Convertir el entero de 64 bits a 8 bytes (big-endian)
                chunk = value_64bit.to_bytes(8, byteorder='big')
                
                # Escribir los 8 bytes en el archivo
                f.write(chunk)
                
                print(f"Wrote Memory[{address}] = {value_64bit} to file.")
        
        print(f"Successfully saved processed file data to {file_path}.")
        return True
        
    except Exception as e:
        print(f"Error saving file from memory: {e}")
        return False

if __name__ == "__main__":
    # Mostrar ayuda si se solicita
    if "-h" in sys.argv or "--help" in sys.argv:
        print("LEG ISA Processor Simulator")
        print("Usage: python main.py [options] <instructions_file> <input_file> <output_file> [interval]")
        print("\nRequired Arguments:")
        print("  instructions_file  Path to instruction file (.txt) generated by assembler")
        print("  input_file         Path to input data file to load into memory")
        print("  output_file        Path to output file for processed data")
        print("\nOptional Arguments:")
        print("  interval           Execution interval (default: 1.0)")
        print("\nOptions:")
        print("  -S, --step         Step-by-step execution")
        print("  -R, --registers    Print register states")
        print("  -h, --help         Show this help message")
        print("\nMemory Layout:")
        print("  Memory[0]          Number of data blocks")
        print("  Memory[1]          64-bit encryption key (user provided)")
        print("  Memory[2+]         Input file data in 64-bit blocks")
        print("\nExamples:")
        print("  python main.py program.txt input.bin output.bin")
        print("  python main.py program.txt input.bin output.bin 0.5")
        print("  python main.py -R -S program.txt input.bin output.bin")
        sys.exit(0)
    
    # Parse flags and arguments
    step_by_step = "-S" in sys.argv or "--step" in sys.argv
    print_registers = "-R" in sys.argv or "--registers" in sys.argv
    
    
    # Remove flags from argv to get clean arguments
    clean_args = [arg for arg in sys.argv[1:] if not arg.startswith('-')]
    
    # Validate required arguments
    if len(clean_args) < 3:
        print("Error: Missing required arguments")
        sys.exit(1)
    
    # Parse arguments
    instructions_file = clean_args[0]
    input_file = clean_args[1]
    output_file = clean_args[2]
    

    # Parse optional interval (default 1.0)
    interval = 1.0
    if len(clean_args) >= 4:
        try:
            interval = float(clean_args[3])
        except ValueError:
            print(f"Error: Invalid interval value '{clean_args[3]}'. Using default 1.0")
            interval = 1.0
    
    print(f"Loading instructions from: {instructions_file}")
    print(f"Loading input data from: {input_file}")
    print(f"Saving output to: {output_file}")
    print(f"Execution interval: {interval}")
    
    # Create processor
    procesador = ProcesadorFullHazard(interval=interval, print_registers=print_registers, step_by_step=step_by_step)
    
    # Load input data and key into memory
    print("\n=== Loading Input Data and Key ===")
    ok = load_file_to_memory(input_file, procesador)
    if not ok:
        sys.exit(1)
    
    # Load instructions and execute
    print("\n=== Loading Instructions ===")
    ok = load_code_from_file(instructions_file, procesador)
    if not ok:
        sys.exit(1)
    
    print("\n=== Executing Program ===")
    procesador.iniciarEjecucion()
    
    # Save processed data to output file
    print("\n=== Saving Output ===")
    ok = save_file_from_memory(output_file, procesador)
    if not ok:
        sys.exit(1)
        
    print("\n=== Execution Complete ===")
    print(f"Processed data has been saved to {output_file}")