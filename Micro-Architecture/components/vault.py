class vault:
    def __init__(self):
        # Registros seguros de la bóveda: 0-3 son llaves (K), 4-7 son hashes (H)
        self.secure_regs = [10]*8  # cada uno de 64 bits
        
        # Contraseña numérica para autenticación mediante instrucción AUT
        self.master_password = 12345
        
        # Estado de autenticación (se activa mediante instrucción AUT)
        self.secure_user = False
    
    def is_authenticated(self):
        """Verifica si el usuario está autenticado."""
        return self.secure_user

    def write_secure_reg(self, index, valor):
        """Escritura en registros de la bóveda (requiere autenticación)."""
        if self.secure_user:
            if 0 <= index < 8:
                self.secure_regs[index] = valor
                return True
        return False

    def get_secure_reg(self, index):
        """Lectura de registros de la bóveda (requiere autenticación)."""
        if self.secure_user:
            if 0 <= index < 8:
                print(f"Accediendo a registro seguro K{index} con valor {self.secure_regs[index]}")
                return self.secure_regs[index]
        return 0
    
    def get_password(self):
        """Obtiene la contraseña maestra (solo para comparación interna)."""
        return self.master_password
    
    def write_authorization(self, result):
        """Actualiza el estado de autenticación (usado por instrucción AUT)."""
        self.secure_user = result
        
    def unathorize(self):
        """Desautoriza el acceso a la bóveda."""
        self.secure_user = False

