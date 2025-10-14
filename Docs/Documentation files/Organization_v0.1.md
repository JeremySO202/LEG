## Organización / Microarquitectura

### Visión general
El procesador simulado implementa un **pipeline de 5 etapas** (**FETCH → DECODE → EXECUTE → MEMORY → WRITEBACK**) con **forwarding**, **stalls** para dependencias de carga y **predicción de saltos**. La organización se modela en software con:
- **Memoria de instrucciones (IM)**: lista de objetos-instrucción creada por `Inst_Decoder` (`instr_decoder.py`).
- **Banco de registros (RF)**: `archivoRegistros` (`components/register_file.py`).
- **ALU / Unidades funcionales**: `ALU` (`components/alu.py`) y operaciones especiales usadas por las clases de instrucción.
- **Memoria de datos (DM)**: `memoriaDatos` (`components/data_memory.py`).
- **Bóveda / Root of Trust (VAULT)**: `vault` (`components/vault.py`) con puerto dedicado (no direccionable por MEM). Incluye control de acceso mediante autenticación con la instrucción AUT (tipo A).
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
      EXHUB[EX Stage Hub]
      ALU_OP[ALU Ops<br/>SMA, RTA, MUL, Y, O, OEX]
      IMM_OP[Immediate Ops<br/>SMAI, RTAI, MULI, ROTI, etc.]
      BRANCH_OP[Branch Ops<br/>RIG]
      MIX_OP[Security Ops<br/>MIX - VAULT Access]
      AUTH_OP[Authentication<br/>AUT - Password Verify]
      EXHUB --> ALU_OP
      EXHUB --> IMM_OP
      EXHUB --> BRANCH_OP
      EXHUB --> MIX_OP
      EXHUB --> AUTH_OP
      ALU_OP --> EXHUB
      IMM_OP --> EXHUB
      BRANCH_OP --> EXHUB
      MIX_OP --> EXHUB
      AUTH_OP --> EXHUB
    end
    
    %% Pipeline Register EX/MEM
    regALU[regALU<br/>Pipeline Register]
    
    %% MEM Stage
    subgraph MEM_Stage["MEM: Memory Access"]
      MEM[Memory Ops<br/>CRG, GRD - Data Memory]
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
    RF[General-Purpose Registers<br/>archivoRegistros<br/>L0..L15 — 64-bit each<br/>Total: 16 registers]
  end
  
  %% Security Vault
  subgraph Security["Security Vault"]
    VAULT[VAULT Component<br/>vault<br/>K0..K3 - Private Keys<br/>H0..H3 - Hash State]
  end
  
  %% Control Units
  subgraph Control["Control & Hazard Management"]
    direction TB
    HC[HazardControl<br/>Data Forwarding<br/>Stall Detection]
    BP[BranchPredictor<br/>Prediction & Mispredict]
    DECODER[Inst_Decoder<br/>Binary → Instr Objects]
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
  regRF --> EXHUB
  EXHUB --> regALU
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
  AUTH_OP <--> VAULT
  
  %% ALU Connection
  EXHUB <--> ALU_UNIT
  
  %% Control Connections
  DECODER --> ID
  HC -.->|Forwarding| EXHUB
  HC -.->|Stall Control| regRF
  BP -.->|Prediction| BRANCH_OP
  BRANCH_OP -.->|Outcome| BP
  
  %% Forwarding Paths
  regALU -.->|EX→EX| EXHUB
  regDM -.->|MEM→EX| EXHUB
  WB -.->|WB→EX| EXHUB
  
  %% PC Update
  BRANCH_OP -.->|Branch Target| PC
  
  %% Legend
  subgraph Legend["Instruction Categories"]
    R_TYPE[R-Type<br/>NOP, SMA, RTA, MUL, Y, O, OEX, MOV]
    I_TYPE[I-Type<br/>SMAI, RTAI, MULI, ROTD, ROTI, NO, ROL, MODP, MULA]
    B_TYPE[B-Type<br/>RIG]
    H_TYPE[H-Type<br/>MIX]
    M_TYPE[M-Type<br/>CRG, GRD]
    V_TYPE[V-Type<br/>GRDK, GRDH]
    A_TYPE[A-Type<br/>AUT - Authentication]
  end



