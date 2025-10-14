class ALU:
    def __init__(self):
        # Máscara para limitar resultados a 64 bits
        self.MASK_64BIT = 0xFFFFFFFFFFFFFFFF

    def _limit_64bit(self, value):
        """Limita un valor a 64 bits usando máscara."""
        return value & self.MASK_64BIT

    def operar(self, A, B, op, C=0):
        # Asegurar que los operandos estén dentro de 64 bits
        A = self._limit_64bit(A)
        B = self._limit_64bit(B)
        C = self._limit_64bit(C)
        
        if op == 0:
            return self._limit_64bit(A + B)
        elif op == 1:
            return self._limit_64bit(A - B)
        elif op == 2:
            return self._limit_64bit(A & B)
        elif op == 3:
            return self._limit_64bit(A | B)
        elif op == 4:
            return self._limit_64bit(A * B)  # Multiplicación
        elif op == 5:
            # Desplazamiento a la izquierda lógico (limitado a 63 bits de desplazamiento)
            B = B & 0x3F  # Limitar desplazamiento a 0-63
            return self._limit_64bit(A << B)
        elif op == 6:
            # Desplazamiento a la derecha lógico (limitado a 63 bits de desplazamiento)
            B = B & 0x3F  # Limitar desplazamiento a 0-63
            return self._limit_64bit(A >> B)
        elif op == 7:
            return self._limit_64bit(A ^ B)  # XOR
        elif op == 8:
            return self._limit_64bit(~A)  # NOT
        elif op == 9:
            if B == 0:
                raise ValueError("División por cero en operación módulo")
            return self._limit_64bit(A % B)
        elif op == 10:
            # Mix no lineal: (A & B) | (~A & C)
            return self._limit_64bit((A & B) | (~A & C))
        elif op == 11:
            # Multiplicación áurea
            mul = A * 0x9e3779b97f4a7c15
            return self._limit_64bit(mul)
        elif op == 12:
            # Rotación a la izquierda
            B = B & 0x3F  # Limitar rotación a 0-63
            return self._limit_64bit((A << B) | (A >> (64 - B)))
        elif op == 13:
            return 1 if A == B else 0  # Comparación de igualdad
        else:
            raise ValueError("Operación no reconocida")