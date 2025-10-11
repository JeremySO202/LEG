class vault:
    def __init__(self):
        # Llaves privadas (solo lectura/escritura segura)
        self.secure_regs = [0]*8  # cada una de 64 bits 0 a 3 son llaves, 4 a 7 son hashes
        
        
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

#Guardar hash    GRDH index, rs1
#Guardar llave   GRDK index, rs1
# Mix y rol
#Generar firma   FRM rd, rs1, index (Registro destino, registro con hash, indice de la llave) = (A XOR K)
#Comparar firma  CHKF rd, rs1, rs2 (registro destino, la calculada, la extraida del doc)
    
    #Login y tenemos contraseña en boveda, me compara la que le doy con la hardcoded en boveda
    # Esto activa un registro interno para comprobar si se logueó o no
    # Si no está logueado, las de modificar no modifican y las de cargar me devuleven 0
    
# solo modificar las instrucciones
# en fetch se ve si tiene permisos
# modificar forwarding
    
