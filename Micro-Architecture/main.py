from instructions.mula import Mula
from instructions.rol import Rol
from instructions.frm import Frm
from instructions.mov import Mov
from instructions.grdh import Grdh

from instr_decoder import Inst_Decoder

from processor_fh import ProcesadorFullHazard


import sys

if __name__ == "__main__":
    # Leer intervalo desde argumentos de la línea de comandos (si no, usar 1 por defecto)
    interval = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
    procesador = ProcesadorFullHazard(interval=interval)

    procesador.RF.registros[0] = 7
    procesador.RF.registros[1] = 0x9e3779b97aaa7c19
    procesador.RF.registros[2] = 7
    procesador.RF.registros[3] = 128
    procesador.RF.registros[4] = 0
    procesador.RF.registros[9] = 5
    procesador.RF.registros[10] = 10
    procesador.DM.datos[9] = 20
    # Llave inicial 
    procesador.vault.secure_regs[0] = 0x1009E607F3BCC4D2  
    # Hashes iniciales (64-bit)
    procesador.vault.secure_regs[4] = 0x6A09E667F3BCC908  
    procesador.vault.secure_regs[5] = 0xBB67AE8584CAA73B  
    procesador.vault.secure_regs[6] = 0x3C6EF372FE94F82B  
    procesador.vault.secure_regs[7] = 0xA54FF53A5F1D36F1 
    
    
    #procesador.cargarInstrucciones(Grdh(1, 4, 1, procesador)) # GRDH L1 V4 
    procesador.cargarInstrucciones(Frm(5, 1, 4, 0, 1, procesador)) # FRM L5 v1
    #procesador.cargarInstrucciones(StoreWord(9, 0, 1, procesador))
    #procesador.cargarInstrucciones(Sma(3, 9, 0, procesador))
    #procesador.cargarInstrucciones(Mov(5, 1, procesador))

    procesador.iniciarEjecucion()