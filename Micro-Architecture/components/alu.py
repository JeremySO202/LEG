class ALU:
    def __init__(self):
        pass

    def operar(self, A, B, op, C=0):
        if op == 0:
            return A + B
        elif op == 1:
            return A - B
        elif op == 2:
            return A & B
        elif op == 3:
            return A | B
        elif op == 4:
            return A * B # Multiplicación
        elif op == 5:
            return A << B # Desplazamiento a la izquierda lógico
            #deberia limitarse a 32 bits?
        elif op == 6:
            return A >> B # Desplazamiento a la derecha lógico
        elif op == 7:
            return A ^ B # XOR
        elif op == 8:
            return ~A # NOT
        elif op == 9:
            return A % B
        elif op == 10:
            return (A & B) | (~A & C);
        elif op == 11:
            mul = A * 0x9e3779b97f4a7c15
            mul &= 0xFFFFFFFFFFFFFFFF 
            return mul
        else:
            raise ValueError("Operación no reconocida")