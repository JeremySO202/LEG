# Hoja de referencia LEG - Versión 0.1

## Registros  ---> Hay que ver cuantos queremos

| Nombre   | Uso                                              |
|----------|--------------------------------------------------|
| L0       | Argumento / Valor de retorno / Variable temporal |
| L1 - L3  | Argumento / Variable temporal                    |
| L4 - L11 | Variables preservadas                            |
| L12      | Variable temporal                                |
| L13 (SP) | Puntero a la pila de memoria                     |
| L14 (LR) | Puntero de link                                  |
| L15 (PC) | Contador de programa                             |

## Tipos de Instrucciones

### Formatos (32 bits)  ---> Hay que ver cuáles dejamos
- R:  OPC(6) | RD(4) | RS1(4) | RS2(4) | FUN(6) | Z(8)
- I:  OPC(6) | RD(4) | RS1(4) | IMM(18)
- M:  OPC(6) | RD(4) | BASE(4) | OFFS(18)
- B:  OPC(6) | RS1(4) | RS2(4) | OFFS(18)   ; PC-relative
- V:  OPC(6) | SUB(4) | IDX(2) | RD/RS(4) | FUN(4) | Z(12) ; Bóveda/Hash


### Instrucciones aritméticas / lógicas  --> Mnemonicos en español o en inglés?

| Mnemónico | Semántica | Lat. |
|---|---|---|
| NOP | no-op | 1 |
| ADD rd,rs1,rs2 | rd ← rs1 + rs2 | 1 |
| SUB rd,rs1,rs2 | rd ← rs1 - rs2 | 1 |
| AND/OR/XOR rd,rs1,rs2 | bitwise | 1 |
| ROL rd,rs,sh | rotl64(rs, sh[0..63]) | 1 |
| LI rd,imm | rd ← signext(imm) | 1 |
| BEQ rs1,rs2,off | if(rs1==rs2) pc+=off | 1 |
| BNE rs1,rs2,off | if(rs1!=rs2) pc+=off | 1 |
| JAL rd,off | rd←pc+4; pc+=off | 1 |
| RET | pc ← x15 | 1 |

### Instrucciones de Hash (≥3, requeridas)

| Mnemónico | Semántica | Lat. |
|---|---|---|
| MULC_GR rd,rs | rd ← (rs * 0x9e3779b97f4a7c15) & 2^64-1 | 2 |
| MODP_P rd,rs | rd ← rs mod 0xFFFFFFFB | 2 |
| MIX3 rd,ra,rb,rc | rd ← (ra & rb) | (~ra & rc) | 1 |
| XOR4K a,b,c,d,kidx | a←a^K[kidx]; b←b^K[kidx]; c←c^K[kidx]; d←d^K[kidx] | 2 |

### Instrucciones de acceso a memoria / manejo de datos

| Mnemónico | Semántica | Lat. |
|---|---|---|
| LD rd,offs(base) | rd ← M64[base+offs] | 2 |
| ST rs,offs(base) | M64[base+offs] ← rs | 2 |

### Instrucciones de acceso a bóveda

| Mnemónico | Semántica | Nota |
|---|---|---|
| VSETK kidx, imm64 | bóveda.K[kidx] ← imm64 | carga segura |
| VSETIV i, imm64 | bóveda.IV[i] ← imm64 (i∈{0:A..3:D}) | carga segura |
| HINIT i | H[i] ← bóveda.IV[i] (no expone IV) | no GPR |
| HKLOAD rd,rs,kidx | rd ← rs ^ bóveda.K[kidx] | no filtra K en claro |

### Instrucciones de salto / branch

| Mnemónico | Semántica | Nota |
|---|---|---|
| VSETK kidx, imm64 | bóveda.K[kidx] ← imm64 | carga segura |
| VSETIV i, imm64 | bóveda.IV[i] ← imm64 (i∈{0:A..3:D}) | carga segura |
| HINIT i | H[i] ← bóveda.IV[i] (no expone IV) | no GPR |
| HKLOAD rd,rs,kidx | rd ← rs ^ bóveda.K[kidx] | no filtra K en claro |

### Instrucciones de llamada al sistema

No tenemos, porque LEG está orientado a empotrados?

## Encodificación de instrucciones







