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

En relacion con las instrucciones se definieron un total de ###. Entre ellas se establecieron 14 aritmeticas, aritmetico-logicas y shifts que abarcan las instrucciones más utilizadas en RISCV. Se definen 4 instrucciones para el hashing de datos las cuales están pensadas para facilitar el proceso de hashing al usuario además de dismuir el tiempo de ejecución unificando operaciones complejas en una sola instrucción. Se definen además ## instrucciones de interacción con el vault las cuales permiten al usuario cargar y guardar datos de la bóveda de seguridad. Se definen 2 instrucciones de carga y almacenamiento las cuales permiten al usuario cargar y guardar datos de la memoria principal. Se definen 3 instrucciones de control de flujo las cuales permiten al usuario realizar saltos condicionales. Finalmente, se define una instrucción NOP la cual no realiza ninguna operación y es utilizada para evitar hazards en el pipeline.

Se define que LEG no tendrá instrucciones de punto flotante, ya que el enfoque del proyecto está más orientado hacia la seguridad de la información y el modelado de software en ese dominio específico. La inclusión de instrucciones de punto flotante podría agregar complejidad innecesaria al diseño del procesador y desviar el enfoque del proyecto de su objetivo principal.

Para la encodificación de las instrucciones se decidió utilizar un opcode de 6 bits, esto permite una mayor cantidad de instrucciones en el set y a su vez permite que las instrucciones sean más compactas. Se decidió utilizar un formato fijo de 32 bits para todas las instrucciones, esto facilita la decodificación y el diseño del procesador. Se decidió utilizar 5 formatos de instrucciones: R, I, M, B, H y V. El formato R es utilizado para instrucciones que operan entre registros, el formato I es utilizado para instrucciones que operan con un registro y un inmediato, el formato M es utilizado para instrucciones de carga y almacenamiento, el formato B es utilizado para instrucciones de control de flujo, el formato H es utilizado para instrucciones de hashing y el formato V es utilizado para instrucciones de interacción con el vault.

Se decidió que LEG no tendrá instrucciones de llamada a subrutinas o funciones, ya que el enfoque del proyecto está más orientado hacia la seguridad de la información y el modelado de software en ese dominio específico. La inclusión de instrucciones de llamada a subrutinas podría agregar complejidad innecesaria al diseño del procesador y desviar el enfoque del proyecto de su objetivo principal.














