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

    procesador.cargarInstrucciones(StoreWord(9, 0, 1, procesador))
    procesador.cargarInstrucciones(Sma(3, 9, 0, procesador))
    procesador.cargarInstrucciones(Mov(5, 1, procesador))

    procesador.iniciarEjecucion()