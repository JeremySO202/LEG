class Aut:
    # Aut <password_value>
    # Autentica el acceso a la bóveda usando una contraseña codificada
    def __init__(self, password_int, _procesador):
        self.password_input = password_int
        self.procesador = _procesador
        self.ejecucion = [self.decode, self.execute, self.memory, self.writeback]
        
    def reset(self):
        self.ejecucion = [self.decode, self.execute, self.memory, self.writeback]
    
    def decode(self):
        print(f"Decodificando contraseña recibida: {self.password_input}")
        # Guardamos el valor de la contraseña directamente
        self.procesador.regRF.data = self.password_input
        print(f"Valor de contraseña: {self.procesador.regRF.data}")
    
    def execute(self):
        print(f"Verificando contraseña contra la bóveda")
        if self.procesador.regRF.data is None:
            raise ValueError("La contraseña recibida es None y no puede verificarse.")
        
        # Obtener la contraseña almacenada en la bóveda (ahora es numérica)
        vault_password = self.procesador.vault.get_password()
        
        print(f"Contraseña recibida: {self.procesador.regRF.data}")
        print(f"Contraseña de la bóveda: {vault_password}")
        
        # Usar ALU para comparar (operación 13 = comparación de igualdad)
        self.procesador.regALU.data = self.procesador.ALU.operar(
            self.procesador.regRF.data, 
            vault_password, 
            13  # Operación de comparación
        )
        print(f"Resultado de verificación - ALU: {self.procesador.regALU.data}")
    
    def memory(self):
        print(f"Sin operación de memoria para Aut")
        self.procesador.regDM.data = self.procesador.regALU.data
    
    def writeback(self):
        print(f"Actualizando estado de autenticación de la bóveda")
        # Si regDM.data == 1, la contraseña es correcta
        is_authenticated = (self.procesador.regDM.data == 1)
        self.procesador.vault.write_authorization(is_authenticated)
        print(f"Estado de autenticación: {'Autenticado' if is_authenticated else 'No autenticado'}")
        print(f"Acceso a bóveda: {'Permitido' if self.procesador.vault.is_authenticated() else 'Denegado'}")
    
    def ejecutar(self):
        if self.ejecucion:
            fase = self.ejecucion.pop(0)
            fase()
        else:
            print("No hay más fases para ejecutar en Aut.")
