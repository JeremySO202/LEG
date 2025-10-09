class vault:
    def __init__(self):
        # Llaves privadas (solo lectura/escritura segura)
        self.keys = [0]*4  # cada una de 64 bits
        # Valores iniciales de hash
        self.hashes = [0]*4  # A, B, C, D

    # Escritura de llaves o hashes desde instrucciones especiales
    def write_key(self, index, valor):
        if 0 <= id < 4:
            self.keys[index] = valor

    def write_hash(self, index, valor):
        if 0 <= index < 4:
            self.hashes[index] = valor

    # Lectura controlada (solo por CPU)
    def compare_key(self, index):
        return self.keys[index]

    def compare_hash(self, index):
        return self.hashes[index]
    
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
    
