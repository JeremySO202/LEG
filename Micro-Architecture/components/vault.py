class vault:
    def __init__(self):
        # Llaves privadas (solo lectura/escritura segura)
        self.secure_regs = [10]*8  # cada una de 64 bits 0 a 3 son llaves, 4 a 7 son hashes
        
        # Contraseña hardcoded para el login (en producción sería hasheada)
        self.master_password = "secure123"  # Cambiar por una contraseña más segura
        
        self.secure_user = False  # Inicia como NO autenticado
        self.login_attempts = 0
        self.max_attempts = 3

    def login(self, password):
        """Intenta hacer login con la contraseña proporcionada."""        
        if password == self.master_password:
            self.secure_user = True
            return True
        else:
            return False
    
    def logout(self):
        """Cierra sesión del vault."""
        self.secure_user = False
        return "Logged out successfully."
    
    def is_authenticated(self):
        """Verifica si el usuario está autenticado."""
        return self.secure_user
    
    def reset_attempts(self):
        """Resetea los intentos de login (solo para testing)."""
        self.login_attempts = 0

    # Escritura de llaves o hashes desde instrucciones especiales
    def write_secure_reg(self, index, valor):
        if self.secure_user:
            if 0 <= index < 8:
                self.secure_regs[index] = valor
                return True
        return False

    # Lectura controlada (solo por CPU)
    def get_secure_reg(self, index):
        if self.secure_user:
            if 0 <= index < 8:
                return self.secure_regs[index]
        return 0
    
    def get_password(self):
        return self.master_password
    
    def write_authorization(self, result):
        self.secure_user = result
        
    def unathorize(self):
        self.secure_user = False

    #Login y tenemos contraseña en boveda, me compara la que le doy con la hardcoded en boveda
    # Esto activa un registro interno para comprobar si se logueó o no
    # Si no está logueado, las de modificar no modifican y las de cargar me devuleven 0

