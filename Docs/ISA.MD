# LEG    <small>REFERENCE DATA CARD

//TODO: hay que agregarle el calling a los otros registros
Hay que hacer el del vault
Hay que agregar informaicón adicional como de que es big endian
que los registros son de cierto tamaño y demás info importante
se puede poner en una tabla y ponerla ahí abajo
Hay que agregar la parte del excel para que se vea más lindo
¿Si lo hacemos en overleaf tal vez queda más lindo, no se puede? -> hacerlo si hay tiempo 

### ARITHMETIC INSTRUCTIONS 


| MNEMONIC, NAME | OP-CODE|  FORMAT | OPERATION 
|---|---|---|---|
| NOP | 000000 | 1 | no-op 
| SMA - <small>suma | 000001 | R |  rd ← rs1 + rs2 
| SMAI - <small>suma inmediato| 000010 | I |  rd ← rs1 + imm  
| RTA - <small>resta| 000011 | R | rd ← rs1 - rs2 
| RTAI - <small>resta inmediato | 000100 |  I | rd ← rs1 - imm 
| MUL - <small>multiplicación | 000101 |  R |  rd ← rs1 * rs2 
| MULI - <small>multiplicación inmediato | 000110 | I | rd ← rs1 * imm 
| Y - <small>and | 000111 | R | rd ← rs1 & rs2 
| O - <small>or | 001000 |  R | rd ← rs1 or rs2 
| OEX - <small>xor | 001001 |  R | rd ← rs1 ^ rs2 
| ROTD - <small>rota derecha| 001010 | I |  rd ← rotr64(rs, imm) 
| ROTI - <small>rota izquierda| 001011 |  I | rd ← rotl64(rs, imm) 
| NO - <small>bitwise not| 001100 |  R | rd ← ~rs 
| MOV - <small>mover | 001101 | R | rd ← rs1 



### HASH INSTRUCTIONS

| MNEMONIC, NAME | OP-CODE|  FORMAT | OPERATION 
|---|---|---|---|
| ROL - <small>nombre | 001110 | I |  rd ← (rs1 << imm) or (rs1 >> (64 - imm))
| MODP - <small>nombre | 001111 | I | rd ← rs1 mod 0xFFFFFFFB 
| MIX - <small>nombre | 010000 | R |  rd ← (ra & rb) or (~ra & rc)  
| MULA - <small>nombre | 010001 | I | rd ← (ra & rb) or (~ra & rc)  



### MEMORY ACCESS/ DATA HANDLING INSTRUCTIONS

| MNEMONIC, NAME | OP-CODE|  FORMAT | OPERATION 
|---|---|---|---|
| CRG - <small>nombre | 010010 | M |  rd ← M64[base+offs]
| GRD - <small>nombre | 010011 | M | M64[base+offs] ← rs



### VAULT INTERACTION INSTRUCTIONS

| MNEMONIC, NAME | OP-CODE|  FORMAT | OPERATION 
|---|---|---|---|



### BRANCH/JUMP INSTRUCTIONS

| MNEMONIC, NAME | OP-CODE|  FORMAT | OPERATION 
|---|---|---|---|
| RIG - <small>nombre | 010100 | B |  if(rs1==rs2) pc+=off
| RIM - <small>nombre | 010101 | B | if(rs1>=rs2) pc+=off
| RIP - <small>nombre | 010110 | B |  if(rs1<=rs2) pc+=off 
| RIN - <small>nombre | 010111 | B | rd←pc+4; pc+=off


<hr style="margin:0; border:3px solid white;">


### CORE INSTRUCTION FORMATS
|TYPE| 31-11|11-4|3-5|2-4|1-5|
|---|---|---|---|---|---|
| R: |X(13) | RS2(4) | RS1(4) | OPC(6) | RD(4)
| B: |OFFSET(18) | RS2(4) | OPC(6) | RS1(4)
| M: |OFFSET(18) | BASE(4) | OPC(6) | RS/RD(4)
| I: |IMM(18) | RS1(4) | OPC(6) | RD(4)
| V: |

<hr style="margin:0; border:3px solid white;">
 
### REGISTER NAME, CALLING, USE

| NAME   | CALLING | USE                                              |
|----------| -----|--------------------------------------------------|
| L0       | | Argumento / Valor de retorno / Variable temporal |
| L1-L2    || Argumento / Variable temporal                    |
| L3-L7    || Variables preservadas                            |
| L8-L11 |(P0-P3) | Variable temporal                          |
| L12 |(SP) | Puntero a la pila de memoria                     |
| L13 |(LR) | Puntero de link / Dirección de retorno           |
| L14 |(PC) | Contador de programa                             |
| L15 |(Zero) | Número cero     |


<hr style="margin:0; border:3px solid white;">


### ADDITIONAL INFORMATION 

AGREGAR ACÁ LO DEL BIG ENDIAN
Y DEMÁS INFORMACIÓN QUE sea necesaria

