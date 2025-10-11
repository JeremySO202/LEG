## Organización / Microarquitectura

### Visión general
El procesador simulado implementa un **pipeline de 5 etapas** (**FETCH → DECODE → EXECUTE → MEMORY → WRITEBACK**) con **forwarding**, **stalls** para dependencias de carga y **predicción de saltos**. La organización se modela en software con:
- **Memoria de instrucciones (IM)**: lista de objetos-instrucción creada por `Inst_Decoder` (`instr_decoder.py`).
- **Banco de registros (RF)**: `archivoRegistros` (`components/register_file.py`).
- **ALU / Unidades funcionales**: `ALU` (`components/alu.py`) y operaciones especiales usadas por las clases de instrucción.
- **Memoria de datos (DM)**: `memoriaDatos` (`components/data_memory.py`).
- **Bóveda / Root of Trust (VAULT)**: `vault` (`components/vault.py`) con puerto dedicado (no direccionable por MEM).
- **Control de riesgos y branch predictor**: `HazardControl`, `BranchPredictor` (`hazard_control.py`).
- **Registros de pipeline**: `regIM`, `regRF`, `regALU`, `regDM` (instancias de `components/register.Registro`).

### Diagrama de bloques (falta completar)
```mermaid
flowchart LR
  IF[IF: Fetch] --> ID[ID: Decode]
  ID --> EX[EX: ALU / MUL / MIX / Branch]
  EX --> MEM[MEM: Data Mem 64b]
  MEM --> WB[WB: Write Back]

  subgraph Memories
    IM[Instr. Memory (32b/inst)]
    DM[Data Memory (64b word)]
  end
  subgraph Regs
    RF[L0.. (archivoRegistros)]
  end
  subgraph Secure
    VAULT[K0..K3, H0..H3]
  end
  CTRL[HazardControl + BranchPredictor]

  IM -. inst .-> IF
  ID <-- R/W --> RF
  EX <---> RF
  EX <-- secure port --> VAULT
  MEM <--> DM
  ID -. control .- CTRL
  EX -. branch outcome .- CTRL
