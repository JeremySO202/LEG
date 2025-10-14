# Decisiones de Diseño y Modelado del Software

## 1) Resumen de decisiones (alto nivel)
- **Formato de instrucción**: 32 bits; **datapath**: 64 bits.
- **Registros**: 16 generales `L0..L15` (64-bit).  
- **Bóveda (Root of Trust)**: `K0..K3` (llaves 64-bit) y `H0..H3`≡(A,B,C,D). No direccionable; acceso **solo** por instrucciones tipo H.
- **Memoria**: instrucciones en palabras de 32b; datos en palabras de 64b. Acceso vía `CRG/GRD` con `base + imm16 (two’s complement)`.
- **Inmediatos**: soportados (p.ej., `SMAI`, `MULI`, `ROL rd, rs, imm`). Sign-extend a 64b en la ALU.
- **Saltos**: `RIG` (branch if equal), política estática **not-taken**; resolución en EX.
- **Unidades funcionales**: ALU64, Data Memory, Instruction Memory, Register File, Register, Vault.
- **Seguridad**: la bóveda no se copia a registros ni a memoria; solo se usa como **fuente** en instrucciones H-type.
- **Endianness**: el modelo opera a nivel de **palabra**; para serialización externa usamos convención **big-endian** sin impacto en la ejecución interna.

---

## 2) Modelado del software
**Objetivo**: simular la ISA y la microarquitectura para ejecutar programas ensamblados (32b/inst) y observar ciclos, estado del pipeline y resultados de las operaciones.

El modelado del software en LEG se centra en representar de manera precisa el comportamiento de la ISA y la microarquitectura, permitiendo la ejecución de programas ensamblados y la validación de su funcionamiento. Esto incluye la simulación de las etapas del pipeline, el manejo de riesgos (hazards), y la interacción con los componentes principales del procesador.

---

### Componentes principales del modelo

1. **Assembler (`assembler.py`)**:
   - Convierte código ensamblador en binario (32 bits por instrucción).
   - Valida el tipo de instrucción (R/I/M/B/H), los registros utilizados y los rangos de los inmediatos.
   - Genera un archivo binario que puede ser cargado en la memoria de instrucciones del procesador.

2. **Instruction Decoder (`Inst_Decoder`)**:
   - Decodifica cada palabra de 32 bits en una instrucción concreta.
   - Extrae los campos de la instrucción (`opcode`, `rd`, `rs*`, `imm`) y marca fuentes provenientes de la bóveda (si aplica).
   - Clasifica las instrucciones según su tipo (R, I, M, B, H) para su ejecución en las etapas correspondientes del pipeline.

3. **Procesador (`ProcesadorFullHazard`)**:
   - Implementa un pipeline de 5 etapas: **IF–ID–EX–MEM–WB**.
   - Maneja riesgos de datos mediante forwarding (EX/MEM → ID) y stalls (pausas) cuando es necesario.
   - Incluye predicción de saltos y resolución en la etapa EX.
   - Proporciona un contador de ciclos y muestras en pantalla para depuración.
---

### Unidades funcionales
El modelo incluye los siguientes componentes principales, cada uno simulado como una unidad funcional independiente:

1. **ALU (Arithmetic Logic Unit)**:
   - Realiza operaciones aritméticas, lógicas y de rotación.
   - Instrucciones soportadas: `SMA`, `SMAI`, `Y`, `O`, `ROL`, `MUL`, `MULI`, `MULA`.

2. **Data Memory (`data_memory.py`)**:
   - Simula la memoria de datos del procesador.
   - Permite operaciones de carga (`CRG`) y almacenamiento (`GRD`) basadas en direccionamiento `base + imm16`.
   - Garantiza alineación natural para accesos de 64 bits.

3. **Instruction Memory (`instr_memory.py`)**:
   - Simula la memoria de instrucciones.
   - Almacena las palabras de 32 bits que representan las instrucciones del programa ensamblado.
   - Se carga desde un archivo generado por el ensamblador.

4. **Register File (`register_file.py`)**:
   - Implementa los 16 registros generales (`L0..L15`) de 64 bits.
   - Permite leer y escribir registros en las etapas ID y WB del pipeline.

5. **Register (`register.py`)**:
   - Simula registros temporales utilizados en el pipeline, como `regIM`, `regRF`, `regALU`, y `regDM`.
   - Almacena datos intermedios entre las etapas del pipeline.

6. **Vault (`vault.py`)**:
   - Representa la bóveda de seguridad del procesador.
   - Contiene los registros `K0..K3` (llaves) y `H0..H3` (registros especiales para hash y firma digital).
   - Solo accesible mediante instrucciones tipo H (`MIX`, `HASHRND`, `SIGN`).
   - Garantiza que los datos de la bóveda no se copien a registros generales ni a memoria.

---

### Memoria

- **Memoria de instrucciones**:
  - Arreglo lineal de palabras de 32 bits.
  - Se carga desde un archivo generado por el ensamblador (`.txt`).
- **Memoria de datos**:
  - Arreglo de palabras de 64 bits.
  - Direccionamiento basado en `base + imm16` (complemento a dos).
  - No se permiten accesos desalineados; se asume alineamiento natural.

---

### Ciclo de ejecución
El modelo simula el pipeline del procesador, dividiendo la ejecución en las siguientes etapas:

1. **IF (Instruction Fetch)**:
   - Se lee una palabra de 32 bits desde la memoria de instrucciones.
   - Se incrementa el contador del PC.

2. **ID (Instruction Decode)**:
   - Se decodifica la instrucción y se leen los registros fuente (`L*`).
   - Se marcan fuentes provenientes de la bóveda si aplica.

3. **EX (Execute)**:
   - Se ejecuta la operación en la unidad funcional correspondiente (ALU, MUL, MIX/HASH, Branch).

4. **MEM (Memory Access)**:
   - Se realizan operaciones de carga (`CRG`) o almacenamiento (`GRD`) en la memoria de datos.
   - La bóveda no pasa por esta etapa.

5. **WB (Write Back)**:
   - Se escribe el resultado en los registros generales (`L*`).
   - La bóveda nunca se utiliza como destino.

---

### Manejo de riesgos
1. **Riesgos de datos**:
   - Se resuelven mediante forwarding desde las etapas EX/MEM hacia ID.
   - Si una instrucción de carga tiene una dependencia inmediata, se inserta un stall.

2. **Riesgos de control**:
   - Se utiliza una política de predicción de saltos.
   - Si la predicción falla, se inserta una burbuja en el pipeline.

3. **Riesgos estructurales**:
   - Solo se permite un acceso de datos por ciclo en la LSU.

---

### Validación mínima
El modelo incluye pruebas básicas para validar su funcionamiento:

1. **Smoke test**:
   - Ejecuta un programa con instrucciones `NOP` para verificar el flujo básico del pipeline.

2. **Programa ToyMDMA**:
   - Realiza operaciones de hashing por bloques de 64 bits y firma digital (`SIGN`).
   - Permite observar los valores de los registros especiales `(A, B, C, D)` y la firma final.


---

## 3) Justificación breve de diseño
Las decisiones de diseño y modelado del software en LEG se basan en un equilibrio entre simplicidad, rendimiento y seguridad, adaptándose a los casos de uso previstos. Algunas de las decisiones clave incluyen:

- **32b instrucción + 64b datapath**:
  - Ofrece un equilibrio entre densidad de instrucciones y rendimiento, especialmente para aplicaciones criptográficas.
- **Inmediatos cortos y sign-extend**:
  - Simplifican el decodificador y reducen la complejidad del hardware.
- **Bóveda cerrada**:
  - Garantiza la seguridad al limitar el acceso a las llaves y registros especiales.
- **Primitivas dedicadas**:
  - Instrucciones como `MIX`, `HASHRND` y `SIGN` reducen el número de ciclos necesarios para operaciones de hash y firma digital.
