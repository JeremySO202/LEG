# Decisiones de Diseño y Modelado del Software

## 1) Resumen de decisiones (alto nivel)
- **Formato de instrucción**: 32 bits; **datapath**: 64 bits.
- **Registros**: 16 generales `L0..L15` (64-bit).  
- **Bóveda (Root of Trust)**: `K0..K3` (llaves 64-bit) y `H0..H3`≡(A,B,C,D). No direccionable; acceso **solo** por instrucciones tipo H.
- **Memoria**: instrucciones en palabras de 32b; datos en palabras de 64b. Acceso vía `CRG/GRD` con `base + imm16 (two’s complement)`.
- **Inmediatos**: soportados (p.ej., `SMAI`, `MULI`, `ROL rd, rs, imm`). Sign-extend a 64b en la ALU.
- **Saltos**: `RIG` (branch if equal), política estática **not-taken**; resolución en EX.
- **Unidades funcionales**: ALU64, MUL64, MIX/HASH (ToyMDMA), LSU (Load/Store), Branch.
- **Seguridad**: la bóveda no se copia a registros ni a memoria; solo se usa como **fuente** en instrucciones H-type.
- **Endianness**: el modelo opera a nivel de **palabra**; para serialización externa usamos convención **big-endian** sin impacto en la ejecución interna.

---

## 2) Modelado del software
**Objetivo**: simular la ISA y la microarquitectura para ejecutar programas ensamblados (32b/inst) y observar ciclos y estado.

### Componentes
- **Assembler (`assembler.py`)**: ASM → binario (32 bits por línea). Valida tipo (R/I/M/B/H), registros y rangos de inmediatos.
- **Instruction Decoder (`Inst_Decoder`)**: convierte cada palabra de 32b en una operación concreta; extrae campos (`opcode`, `rd`, `rs*`, `imm`) y marca **fuentes VAULT**.
- **Procesador (`ProcesadorFullHazard`)**: pipeline **IF–ID–EX–MEM–WB** con control de riesgos (forwarding/stalls), contador de ciclos y trazas opcionales.

### Banco de registros
- `L0..L15` (64b). Escritura solo en WB.  
- **Bóveda**: `K0..K3` y `H0..H3(A,B,C,D)`; **no** tiene puerto de memoria; acceso solo por H-type y jamás como **destino**.

### Unidades funcionales
- **ALU64**: suma/lógico/rotaciones (`SMA`, `SMAI`, `Y`, `O`, `ROL`).
- **MUL64**: `MUL`, `MULI`, `MULA`.
- **MIX/HASH**: `MIX`, `HASHRND`, `SIGN`, `LOADK`, `LOADIV` (puerto dedicado a bóveda).
- **LSU**: `CRG/GRD` (cargas/almacenamientos 64b).
- **Branch**: evalúa `RIG` en EX.

### Memoria
- **Instrucciones**: arreglo lineal de 32b cargado desde `.txt` del assembler.
- **Datos**: arreglo de 64b; direccionamiento **base + imm16** (two’s complement).  
- Sin accesos desalineados en el modelo (asumido alineamiento natural).

### Manejo de instrucciones y ciclo de ejecución
1. **IF**: se lee 1 palabra de 32b.  
2. **ID**: decodifica tipo, lee `L*` y marca fuentes VAULT.  
3. **EX**: ejecuta en ALU/MUL/MIX/HASH/Branch; aplica sign-extend a inmediatos.  
4. **MEM**: `CRG/GRD` a memoria de datos (la bóveda no pasa por MEM).  
5. **WB**: escribe resultado en `L*` (nunca en bóveda).

**Riesgos**  
- **Datos**: forwarding EX/MEM→ID; **stall** tras carga si hay dependencia inmediata.  
- **Control**: not-taken; si falla, se inserta burbuja.  
- **Estructurales**: un acceso de datos por ciclo (LSU).

### Validación mínima
- **Smoke test** con `NOP`.  
- **Programa ToyMDMA**: hashing por bloques de 64b y **firma** con `SIGN`; observar `(A,B,C,D)` y firma final.  
- **Negativos**: líneas no binarias/longitudes ≠ 32 → error controlado de carga.

---

## 3) Justificación breve de diseño
- **32b instrucción + 64b datapath**: equilibrio densidad/rendimiento para carga criptográfica con costo moderado.  
- **Inmediatos cortos** y **sign-extend**: decoder simple y hardware compacto.  
- **Bóveda cerrada**: reduce superficie de ataque; el acceso queda explícito en opcodes H.  
- **Primitivas dedicadas** (`MIX`, `HASHRND`, `SIGN`): menos ciclos totales en hash/firma con incremento moderado de complejidad.
