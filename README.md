# Proyecto #1: ISA específica tipo RISC para Aplicaciones de Seguridad de la Información

## Introducción

LEG es un ISA tipo RISC orientado a aplicaciones de Seguridad de la Información, específicamente para el cifrado y firma de documentos. 

Este proyecto define las instrucciones que soporta LEG y las decisiones que se tomaron para el diseño del ISA, además se implementó un simulador de un procesador LEG para ejecutar las instrucciones.
Se cuenta con un ensamblador para el lenguaje LEG que genera la entrada de instrucciones para el procesador.
El programa de prueba para el procesador implementa la función de firma digital para archivos a través del algoritmo ToyMDMA para generar el hash y también verifica la autenticidad de la firma digital.

## Instrucciones de compilación

### Dependencias

La implementación del simulador del procesador fue escrita con Python, sin necesidad de  bibliotecas adicionales

## Instrucciones de ejecución

Para ejecutar el programa principal se debe correr el archivo main.py de la carpeta Micro-architecture.

Para ver la ayuda, ejecutar con la opción -h o --help

```bash
python Micro-Architecture/main.py -h
``` 
El programa toma como parámetros: 
- instructions_file
- input_file
- output_file
- interval (opcional)

Y las opciones:
```
-S, --step         Ejecución paso a paso
-R, --registers    Imprimir estado de los registros
-h, --help         Ayuda del programa
```

Para firmar un archivo, se debe ejectuar el programa ToyMDMA/toyMDMA_FRM.txt
Para verificar la firma, se debe ejecutar el programa ToyMDMA/toyMDMA_CHK.txt

Los archivos .txt contienen las instrucciones ensambladas en binario de cada programa

Mapa de memoria:
```
  Memory[0]          Número de bloques de datos
  Memory[1]          Llave de encripción de 64-bit (user provided)
  Memory[2+]         Bloques del archivo de 64-bits (user provided)
  ```


## Ejemplo

En la carpeta ToyMDMA se encuentra un archivo de prueba pruebaHash.txt, para agregar una firma a este archivo y escribirlo en un archivo llamado output.txt se ejecuta:

```bash
python Micro-architecture/main.py ToyMDMA/toyMDMA_FRM.txt ToyMDMA/pruebaHash.txt output.txt 0.5
```
El archivo para guardar la salida debe existir previamente. El programa solicitará que se introduzca una llave, en el ejemplo se utiliza: 0x0123401234012340
