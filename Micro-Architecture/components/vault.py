class vault:
    def __init__(self):
        # Llaves privadas (solo lectura/escritura segura)
        self.secure_regs = [10]*8  # cada una de 64 bits 0 a 3 son llaves, 4 a 7 son hashes
        
        
        self.secure_user = True  # Indica si el usuario está autenticado

    # Escritura de llaves o hashes desde instrucciones especiales
    def write_secure_reg(self, index, valor):
        if self.secure_user:
            if 0 <= index < 8:
                self.secure_regs[index] = valor

    # Lectura controlada (solo por CPU)
    def get_secure_reg(self, index):
        if self.secure_user:
            if 0 <= index < 8:
                return self.secure_regs[index]
        return 0

    #Login y tenemos contraseña en boveda, me compara la que le doy con la hardcoded en boveda
    # Esto activa un registro interno para comprobar si se logueó o no
    # Si no está logueado, las de modificar no modifican y las de cargar me devuleven 0

