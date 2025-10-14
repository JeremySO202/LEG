# ISA Decisions
---
## Decisions made for the ISA design
Durante el diseño de la arquitectura del set de instrucciones (ISA) de LEG, se tomaron varias decisiones clave para adaptar la arquitectura a sus casos de uso previstos y optimizar su rendimiento.

### Manejo de datos

Se establece que LEG utilizará 16 registros, se define de esta manera para que cada uno utilice 4 bits en direccionamiento lo que facilida su decodificación además de permitir que cada una de las instrucciones sean más compactas y el almacenamiento más eficiente. 

Se estableció que LEG solo trabaja con operaciones sin signo, ya que fue diseñado con un enfoque más que todo centrado en el modelado de software para aplicaciones relacionadas con la seguridad de la información, especificamente en el dominio de la firma digital y verificación de integridad de datos. Sin embargo, a pesar de este enfoque especializado, LEG también permite el desarrollo de aplicaciones generales.

Además,  no se trabajaran operaciones con acceso a memoria, la mayor parte de las instrucción de LEG se harán entre registros. Las unicas instrucciones que podrán operar con inmediatos con las instrucciones de memoria por su offset y las instrucciones más basicas como lo son Smai, Rtai y Muli se establece de esa manera ya que estas son las que el usuario más puede ocupar para el desarrollo de sus aplicaciones.  En RISC-V se promedia que entre un 20–25% las instrucciones anteriores son utilizadas por los usuarios.

Por otro lado, se define que LEG utiliza big endian para el almacenamiento y la manipulación de datos. Esta decisión se tomó
ya que muchos estandares de seguridad y criptografia utilizan big endian para representar sus datos. Además de que facilita en su parte la interpretación de los mismos.

---

### Set de instrucciones

En relacion con las instrucciones se definieron un total de 31. Entre ellas se establecieron 14 aritmeticas, aritmetico-logicas y shifts que abarcan las instrucciones más utilizadas en RISCV. Se definen 4 instrucciones para el hashing de datos las cuales están pensadas para facilitar el proceso de hashing al usuario además de dismuir el tiempo de ejecución unificando operaciones complejas en una sola instrucción. Se definen además 2 instrucciones de interacción con el vault las cuales permiten al usuario cargar datos de la bóveda de seguridad. Se añadió 1 instrucción de autenticación (AUT) que permite validar credenciales numéricas para obtener acceso a los registros seguros de la bóveda. Se definen 2 instrucciones de carga y almacenamiento las cuales permiten al usuario cargar y guardar datos de la memoria principal. Se definen 3 instrucciones de control de flujo las cuales permiten al usuario realizar saltos condicionales. Finalmente, se define una instrucción NOP la cual no realiza ninguna operación y es utilizada para evitar hazards en el pipeline.

Se define que LEG no tendrá instrucciones de punto flotante, ya que el enfoque del proyecto está más orientado hacia la seguridad de la información y el modelado de software en ese dominio específico. La inclusión de instrucciones de punto flotante podría agregar complejidad innecesaria al diseño del procesador y desviar el enfoque del proyecto de su objetivo principal.

Para la encodificación de las instrucciones se decidió utilizar un opcode de 6 bits, esto permite una mayor cantidad de instrucciones en el set y a su vez permite que las instrucciones sean más compactas. Se decidió utilizar un formato fijo de 32 bits para todas las instrucciones, esto facilita la decodificación y el diseño del procesador. Se decidió utilizar 6 formatos de instrucciones: R, I, M, B, H, V y A. El formato R es utilizado para instrucciones que operan entre registros, el formato I es utilizado para instrucciones que operan con un registro y un inmediato, el formato M es utilizado para instrucciones de carga y almacenamiento, el formato B es utilizado para instrucciones de control de flujo, el formato H es utilizado para instrucciones de hashing, el formato V es utilizado para instrucciones de interacción con el vault, y el formato A es utilizado para instrucciones de autenticación que requieren una contraseña numérica de 16 bits.

Se decidió que LEG no tendrá instrucciones de llamada a subrutinas o funciones, ya que el enfoque del proyecto está más orientado hacia la seguridad de la información y el modelado de software en ese dominio específico. La inclusión de instrucciones de llamada a subrutinas podría agregar complejidad innecesaria al diseño del procesador y desviar el enfoque del proyecto de su objetivo principal.

---

### Seguridad y Autenticación

Para garantizar la seguridad de los datos sensibles, LEG implementa un sistema de bóveda (vault) con acceso restringido. Se diseñó la instrucción AUT (Authentication) como un mecanismo de control de acceso que valida credenciales antes de permitir operaciones con registros seguros.

**Decisiones de diseño de AUT:**

1. **Formato tipo A**: Se creó un nuevo formato de instrucción (tipo A) específicamente para autenticación, ya que ninguno de los formatos existentes (R, I, B, M, H, V) se ajustaba a los requisitos de la instrucción. El formato A utiliza 16 bits para codificar la contraseña numérica, permitiendo valores en el rango 0-65535.

2. **Contraseña numérica**: Se decidió utilizar una contraseña numérica de 16 bits en lugar de cadenas de texto por las siguientes razones:
   - Simplicidad en la codificación binaria de la instrucción
   - Comparación directa en hardware sin necesidad de conversiones
   - Consistencia con el enfoque de LEG de trabajar con datos sin signo
   - Eficiencia en la decodificación y ejecución

3. **Seguridad de la bóveda**: La instrucción AUT establece un flag de autenticación (`secure_user`) en el componente vault que controla el acceso a los registros K0-K3 (llaves) y H0-H3 (hashes). Sin autenticación exitosa, las instrucciones GRDK y operaciones con registros seguros son bloqueadas.

4. **Ejecución en pipeline**: AUT se ejecuta en las cuatro etapas estándar del pipeline (Decode, Execute, Memory, Writeback), utilizando la ALU para realizar la comparación de contraseñas (operación 13: igualdad).

5. **Opcode asignado**: Se le asignó el opcode 011011 (27 en decimal) a la instrucción AUT, evitando conflictos con otras instrucciones del ISA.

Esta implementación refuerza el enfoque de seguridad de LEG, proporcionando un mecanismo de control de acceso a nivel de hardware para proteger datos sensibles durante el procesamiento criptográfico y de hashing.













