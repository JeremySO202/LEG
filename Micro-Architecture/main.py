from instructions.rig import BranchEqual
from instructions.crg import LoadWord
from instructions.grd import StoreWord
from instructions.sma import Sma
from instructions.smai import Smai
from instructions.rta import Rta
from instructions.rtai import Rtai
from instructions.y import Y
from instructions.o import Or
from instructions.mov import Mov
from instructions.mul import MUL
from instructions.muli import Muli
from instructions.mix import Mix

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


    #procesador.cargarInstrucciones(StoreWord(0,-4,4,procesador))
    #procesador.cargarInstrucciones(StoreWord(1,-3,4,procesador))
    
    procesador.cargarInstrucciones(Sma(2, 0, 1, procesador))  # R2 = R0 + R1
    procesador.cargarInstrucciones(Rtai(3, 2, 1, procesador)) # R3 = R2 - R1
    procesador.cargarInstrucciones(Mix(11,1,9,3, procesador)) # R11 = (R1 & R9) | (~R1 & R0)         

    procesador.iniciarEjecucion()