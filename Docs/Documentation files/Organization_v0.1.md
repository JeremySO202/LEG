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

### Diagrama de bloques
```mermaid
flowchart TB
  %% Program Counter
  PC[Program Counter<br/>PC]
  
  %% Pipeline Stages with Pipeline Registers
  subgraph Pipeline["5-Stage Pipeline"]
    direction TB
    
    %% IF Stage
    subgraph IF_Stage["IF: Instruction Fetch"]
      IF[Fetch Instruction<br/>IM at PC]
    end
    
    %% Pipeline Register IF/ID
    regIM[regIM<br/>Pipeline Register]
    
    %% ID Stage  
    subgraph ID_Stage["ID: Instruction Decode"]
      ID[Decode & Read RF<br/>Register File Access]
    end
    
    %% Pipeline Register ID/EX
    regRF[regRF<br/>Pipeline Register]
    
    %% EX Stage
    subgraph EX_Stage["EX: Execute"]
      direction LR
      ALU_OP[ALU Operations<br/>SMA, RTA, MUL, Y, O, OEX]
      IMM_OP[Immediate Ops<br/>SMAI, RTAI, MULI, ROTI, etc.]
      BRANCH_OP[Branch Ops<br/>RIG, RIM, RIP, RIN]
      MIX_OP[Security Ops<br/>MIX - VAULT Access]
    end
    
    %% Pipeline Register EX/MEM
    regALU[regALU<br/>Pipeline Register]
    
    %% MEM Stage
    subgraph MEM_Stage["MEM: Memory Access"]
      MEM[Memory Operations<br/>CRG, GRD - Data Memory]
    end
    
    %% Pipeline Register MEM/WB
    regDM[regDM<br/>Pipeline Register]
    
    %% WB Stage
    subgraph WB_Stage["WB: Write Back"]
      WB[Write Back to RF<br/>Result Storage]
    end
  end

  
  %% Memory Subsystem
  subgraph Memories["Memory Subsystem"]
    IM[Instruction Memory<br/>memoriaInstrucciones<br/>32-bit instructions]
    DM[Data Memory<br/>memoriaDatos<br/>64-bit words]
  end
  
  %% Register File
  subgraph RegisterFile["Register File"]
    RF[General Purpose Registers<br/>archivoRegistros<br/>L0 to L15 - 64-bit each<br/>Total: 64 registers]
  end
  
  %% Security Vault
  subgraph Security["Security Vault"]
    VAULT[VAULT Component<br/>vault<br/>K0 to K3: Private Keys<br/>H0 to H3: Hash Values<br/>Secure Authentication]
  end
  
  %% Control Units
  subgraph Control["Control & Hazard Management"]
    direction TB
    HC[HazardControl<br/>Data Forwarding<br/>Stall Detection]
    BP[BranchPredictor<br/>Branch Prediction<br/>Misprediction Handling]
    DECODER[Inst_Decoder<br/>Instruction Decoding<br/>Binary to Objects]
  end
  
  %% ALU and Execution Units
  subgraph ExecutionUnits["Execution Units"]
    ALU_UNIT[ALU Component<br/>Arithmetic & Logic<br/>64-bit Operations]
  end

  
  %% Pipeline Flow
  PC --> IF
  IF --> regIM
  regIM --> ID
  ID --> regRF  
  regRF --> EX_Stage
  EX_Stage --> regALU
  regALU --> MEM
  MEM --> regDM
  regDM --> WB
  
  %% Memory Connections
  IM --> IF
  MEM --> DM
  DM --> MEM
  
  %% Register File Connections
  ID <--> RF
  WB --> RF
  
  %% Vault Security Connection
  MIX_OP <--> VAULT
  
  %% ALU Connection
  EX_Stage --> ALU_UNIT
  ALU_UNIT --> EX_Stage
  
  %% Control Connections
  DECODER --> ID
  HC -.->|Forwarding Paths| EX_Stage
  HC -.->|Stall Control| regRF
  BP -.->|Prediction| BRANCH_OP
  BRANCH_OP -.->|Outcome| BP
  HC -.->|Pipeline Control| Pipeline
  
  %% Forwarding Paths (Data Bypassing)
  regALU -.->|EX-EX Forwarding| EX_Stage
  regDM -.->|MEM-EX Forwarding| EX_Stage
  WB -.->|WB-EX Forwarding| EX_Stage
  
  %% PC Update
  WB -.->|PC Update| PC
  BRANCH_OP -.->|Branch Target| PC
  
  %% Instruction Types Legend
  subgraph Legend["Instruction Categories"]
    R_TYPE[R-Type<br/>NOP, SMA, RTA, MUL, Y, O, OEX, MOV]
    I_TYPE[I-Type<br/>SMAI, RTAI, MULI, ROTD, ROTI, NO, ROL, MODP, MULA]
    B_TYPE[B-Type<br/>RIG, RIM, RIP, RIN]
    H_TYPE[H-Type<br/>MIX]
    M_TYPE[M-Type<br/>CRG, GRD]
  end

