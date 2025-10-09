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
    def compare_llave(self, index):
        return self.keys[index]

    def compare_hash(self, index):
        return self.hashes[index]
    
#Comparar hash   CHLL rd, rs1, index (Registro para resultado, registro a comparar, indice del hash)
#Guardar hash    GRDLL rd, rs1, index
#Comparar llave  CHH
#Guardar llave   GRDH
    
    #Login y tenemos contraseña en boveda, me compara la que le doy con la hardcoded en boveda
    # Esto activa un registro interno para comprobar si se logueó o no
    # Si no está logueado, las de modificar no modifican y las de cargar me devuleven 0
    
