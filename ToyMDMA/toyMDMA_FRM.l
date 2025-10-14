AUT 12345
MOV L14 0 #Direccion de inicio de archivo
CRG L15 L14 0 #Carga tamano de archivo
SMAI L15 L15 2 #Resta 1 al tamano por que la primera posicion es el tamano

#Cargar llave inicial
CRG L10 L14 1 
GRDK L10 0

SMAI L14 L14 2 #Suma 1 a direccion por que la primera posicion es el tamano, ademas se ejecuta todo una vez antes de entrar al ciclo para tomar de la boveda

CRG L13 L14 0 #Cargar bloque 64 bits en L13

#non-linear mixes
MIX L5 H0 H1 H2 
MIX L6 H1 H2 H3

OEX L7 H0 H1
OEX L7 L7 H2
OEX L7 L7 H3

#Multiply-mix step
MULA L8 L13 

# Round updates with multiplication and mod
#A
SMA L1 H0 L5 # A + F
SMA L1 L1 L8 # A + F + MUL
ROL L1 L1 7 # ROL(A + F + MUL, 7)
SMA L1 L1 L2 # ROL(A + F + MUL, 7) + B
#B
SMA L2 L2 L6 # B + G
SMA L2 L2 L13 #B + F + bloque
ROL L2 L2 11 # ROL(B + F + bloque, 11)
MULI L10 L2 3 # L10 = C * 3
SMA L2 L2 L10 
#C
SMA L3 L3 L7 # C + H
SMA L3 L3 L8 # C + H + MUL
ROL L3 L3 17 # ROL(C + H + MUL, 17)
MODP L10 L4 # L10 = D % 0xFFFFFFFB 
SMA L3 L3 L10 # ROL(C + H + MUL, 17) + (C + H + MUL) + D % 0xFFFFFFFB
#D
SMA L4 L4 L1 # D + A
SMA L4 L4 L13 # D + A + bloque
ROL L4 L4 19 # ROL(D + A + bloque, 19)
MULI L10 L5 5 # L10 = F * 5
OEX L4 L4 L10 # ROL(D + A + bloque, 19) ^ (F * 5)


# L1 = A, L2 = B, L3 = C, L4 = D
# F = L5, G = L6, H = L7, MUL = L8
# L10 = variable temporal
# L13 = bloque de 64 bits
# L14 = direccion en archivo
# L15 = tamano de archivo

#Repetir hasta que se lea todo el archivo

SMAI L14 L14 1 #Suma 1 a direccion
RIM L14 L15 29 #Si ya se leyo todo el archivo, terminar

CRG L13 L14 0 #Cargar bloque 64 bits

MIX L5 L1 L2 L3
MIX L6 L2 L3 L4

OEX L7 L1 L2
OEX L7 L7 L3
OEX L7 L7 L4

MULA L8 L13 

SMA L1 L1 L5 # A + F
SMA L1 L1 L8 # A + F + MUL
ROL L1 L1 7 # ROL(A + F + MUL, 7)
SMA L1 L1 L2 # ROL(A + F + MUL, 7) + B

SMA L2 L2 L6 # B + G
SMA L2 L2 L13 #B + F + bloque
ROL L2 L2 11 # ROL(B + F + bloque, 11)
MULI L10 L2 3 # L10 = C * 3
SMA L2 L2 L10 

SMA L3 L3 L7 # C + H
SMA L3 L3 L8 # C + H + MUL
ROL L3 L3 17 # ROL(C + H + MUL, 17)
MODP L10 L4 # L10 = D % 0xFFFFFFFB 
SMA L3 L3 L10 # ROL(C + H + MUL, 17) + (C + H + MUL) + D % 0xFFFFFFFB

SMA L4 L4 L1 # D + A
SMA L4 L4 L13 # D + A + bloque
ROL L4 L4 19 # ROL(D + A + bloque, 19)
MULI L10 L5 5 # L10 = F * 5
OEX L4 L4 L10 # ROL(D + A + bloque, 19) ^ (F * 5)


RIG L0 L0 -29

FRM L1 L1 0
FRM L2 L2 0 
FRM L3 L3 0
FRM L4 L4 0

GRD L14 L1 0
GRD L14 L2 1
GRD L14 L3 2
GRD L14 L4 3



