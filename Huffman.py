import math

class Nodo:
    def __init__(self,prob,valor,nodoDer,nodoIzq):   
        self.prob=prob
        self.valor=valor
        self.nodoDer=nodoDer #1 => Mayor
        self.nodoIzq=nodoIzq #0 => Menor
    

class Huffman:
    def __init__(self):   
        self.raiz = Nodo(0,0,None,None)
        self.codigos = {}
        self.datos = None
        
    def generarHuffman(self,mapaValores):
        self.datos = mapaValores
        lista=[]
        for simbolo in mapaValores:  # generamos la lista de terminales
            lista.append(Nodo(mapaValores[simbolo],simbolo,None,None))
            # NODO = (proba,simbolo,hijo1,hijo2)

        while len(lista)>1:
            lista.sort(key=lambda x:x.prob) # esto ordena de menor a mayor
            nodo1=lista.pop(0) 
            nodo2=lista.pop(0)
            # tomamos los 2 primeros que serian los de probabilidad mas baja
            lista.append(Nodo(nodo1.prob+nodo2.prob,None,nodo2,nodo1))

        self.raiz = lista[0]
        self.generarCodigos(self.raiz,"")
    
    def generarCodigos(self,nodo,codigo):
        if nodo != None:
            if nodo.valor != None:
                self.codigos[nodo.valor] = codigo
                # agregamos los codigos a un diccionario una vez que llegamos a un terminal 
            self.generarCodigos(nodo.nodoDer,codigo+"1")
            self.generarCodigos(nodo.nodoIzq,codigo+"0")

    def getCodigos(self):
        return self.codigos
    
    def longitudPromedio(self):
        prom = 0
        for simbolo in self.datos:
            prom = prom+self.datos[simbolo]*len(self.codigos[simbolo])
        return prom

def entropia(signal):
    ent = 0
    for simbolo in signal:
        ent = ent+math.log2(signal[simbolo])*signal[simbolo]
    return -ent

signal = {}
cantidad=0
nombre_archivo_output = "output.txt"
nombre_archivo_input = "signal2"

# levantamos el archivo en un diccionario
with open(nombre_archivo_input, "r") as archivo:
    for linea in archivo:
        simbolo = int(linea[:len(linea)-1])
        cantidad+=1
        if simbolo in signal:
            signal[simbolo]+=1
        else:
            signal[simbolo] = 1

# calculamos la probabilidad de cada simbolo
for simbolo in signal:
    signal[simbolo] = signal[simbolo]/cantidad

# generamos el Huffman para los simbolos
huffman = Huffman()
huffman.generarHuffman(signal)
codigos = huffman.getCodigos()

# codificamos el archivo
resultado = ""
with open(nombre_archivo_input, "r") as archivo:
    for linea in archivo:
        numero = int(linea[:len(linea)-1])
        resultado=resultado+codigos[numero]

# generamos el archivo
with open(nombre_archivo_output, "w") as archivo:
    archivo.write(resultado)

print(f"Nombre archivo: {nombre_archivo_input}")
print(f"Longitud promedio Huffman: {huffman.longitudPromedio()}")
print(f"Entropia de la señal: {entropia(signal)}")
print(f"Longitud del archivo codificado en bits: {len(resultado)}")
print(f"Tamaño del archivo codificado en kb: {len(resultado)/8000}")
print(f"se creo el archivo {nombre_archivo_output}")