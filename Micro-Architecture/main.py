from instructions.rig import BranchEqual
from instructions.crg import LoadWord
from instructions.grd import StoreWord
from instructions.sma import Sma
from instructions.smai import Smai
from instructions.rta import Rta
from instructions.rtai import Rtai
from instructions.y import Y
from instructions.o import O
from instructions.mov import Mov
from instructions.mul import Mul
from instructions.muli import Muli
from instructions.mix import Mix

from instr_decoder import Inst_Decoder

from processor_fh import ProcesadorFullHazard


import sys

if __name__ == "__main__":
    # Leer intervalo desde argumentos de la línea de comandos (si no, usar 1 por defecto)
    interval = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
    procesador = ProcesadorFullHazard(interval=interval)

    procesador.RF.registros[0] = 7
    procesador.RF.registros[1] = 7
    procesador.RF.registros[9] = 5
    procesador.RF.registros[10] = 10
    procesador.DM.datos[9] = 20

    """
    assembled_code = [
    "00000000000000000000000000000000", # NOP
    "00000000000000001100100000010001", # SMA L1 L2 L3
    "00000000001111111101010000100100", # SMAI L4 L5 255
    "00000000000000100001110000110110", # RTA L6 L7 L8
    "00000000000000101110100001011001", # MUL L9 L10 L11
    "00000000000110010011010001101100", # MULI L12 L13 100
    "00000000000000000011110001111110", # Y L14 L15 L0
    "00000000000000001100100010000001", # O L1 L2 L3
    "00000000000000011001010010010100", # OEX L4 L5 L6
    "00000000000011001010000010100111", # ROTD L7 L8 50
    "00000000000001100110100010111001", # ROTI L9 L10 25
    "00000000000000110111000011001011", # NO L11 L12 L13
    "00000000000000000011110011011110"]  # MOV L14 L15 L0

    decoder = Inst_Decoder()
    decoder.load_code(assembled_code, procesador)"""
    
    procesador.cargarInstrucciones(Sma(2, 0, 1, procesador))
    procesador.cargarInstrucciones(LoadWord(5, 2, 1, procesador))
    procesador.cargarInstrucciones(Smai(3, 9, 1, procesador))
    
    #procesador.cargarInstrucciones(StoreWord(9, 0, 1, procesador))
    #procesador.cargarInstrucciones(Sma(3, 9, 0, procesador))
    #procesador.cargarInstrucciones(Mov(5, 1, procesador))

    procesador.iniciarEjecucion()