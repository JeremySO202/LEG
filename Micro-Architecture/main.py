from instructions.rig import BranchEqual
from instructions.crg import LoadWord
from instructions.grd import StoreWord
from instructions.sma import Add
from instructions.smai import Addi
from instructions.rta import Sub
from instructions.rtai import Subi
from instructions.y import And
from instructions.o import Or
from instructions.mov import Mov
from instructions.mul import MUL
from instructions.muli import Muli

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
    
    procesador.cargarInstrucciones(BranchEqual(0,1,2,procesador))
    procesador.cargarInstrucciones(Add(2, 0, 1, procesador))  # R2 = R0 + R1
    procesador.cargarInstrucciones(Add(3, 2, 1, procesador))  # R3 = R2 + R1
    procesador.cargarInstrucciones(Sub(4, 10, 9, procesador))
    procesador.cargarInstrucciones(Add(5,9,10,procesador))
    procesador.cargarInstrucciones(And(5, 1, 4, procesador))
    procesador.cargarInstrucciones(LoadWord(8,3,1,procesador))
    procesador.cargarInstrucciones(Add(5,9,10,procesador))
    procesador.cargarInstrucciones(MUL(5,1,9,procesador))



    procesador.iniciarEjecucion()