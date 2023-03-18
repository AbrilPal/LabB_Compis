from graphviz import Digraph

# Definimos la clase Estado, que representa un estado del AFD
class Estado:
    def __init__(self, identificador, aceptacion=False):
        self.id = identificador
        self.aceptacion = aceptacion
        self.transiciones = {}

    def agregar_transicion(self, simbolo, estado_destino):
        if simbolo in self.transiciones:
            self.transiciones[simbolo].append(estado_destino)
        else:
            self.transiciones[simbolo] = [estado_destino]

    def obtener_transiciones(self, simbolo):
        return self.transiciones.get(simbolo, [])

    def __str__(self):
        return str(self.id)

# Definimos la clase AFD, que representa el Autómata Finito Determinístico
class AFD:
    def __init__(self, estados, estado_inicial, alfabeto):
        self.estados = estados
        self.estado_inicial = estado_inicial
        self.alfabeto = alfabeto

    def obtener_estado_por_id(self, identificador):
        for estado in self.estados:
            if estado.id == identificador:
                return estado
        return None

    def __str__(self):
        return f"Estados: {[str(estado) for estado in self.estados]}\n" + \
               f"Estado inicial: {self.estado_inicial}\n" + \
               f"Alfabeto: {self.alfabeto}"


def construir_AFD(expresion_regular):
    # Definimos una función auxiliar para crear nuevos estados
    contador_estados = 0
    def nuevo_estado():
        nonlocal contador_estados
        estado = Estado(contador_estados)
        contador_estados += 1
        return estado

    # Definimos una función auxiliar para crear transiciones vacías
    def transicion_vacia(estado_origen, estado_destino):
        estado_origen.agregar_transicion("", estado_destino)

    # Definimos una función auxiliar para agregar la clausura vacía de un estado
    def agregar_clausura_vacia(estado, visitados):
        visitados.add(estado)
        for destino in estado.obtener_transiciones(""):
            if destino not in visitados:
                agregar_clausura_vacia(destino, visitados)
    
    # Definimos una función auxiliar para agregar una transición a un estado a partir de un símbolo
    def agregar_transicion(estado_origen, estado_destino, simbolo):
        if simbolo in afd.alfabeto:
            estado_origen.agregar_transicion(simbolo, estado_destino)

    # Definimos las variables necesarias para construir el AFD
    afd = AFD([], None, set())
    pila = []
    visitados = set()

    # Recorremos la expresión regular
    for simbolo in expresion_regular:
        if simbolo == "(":
            pila.append("(")
        elif simbolo == ")":
            while pila and pila[-1] != "(":
                operando2 = pila.pop()
                operando1 = pila.pop()
                # Agregamos una transición vacía desde el primer operando al segundo
                transicion_vacia(operando1[1], operando2[0])
                # Unimos los alfabetos de ambos operandos
                afd.alfabeto |= operando1[2] | operando2[2]
                # Agregamos ambos operandos a la pila
                pila.append((operando1[0], operando2[1], afd.alfabeto.copy()))
            pila.pop() # Sacamos el paréntesis de la pila
        elif simbolo == '?':
            # Obtenemos el último operando que está en la pila
            operando = pila.pop()
            # Creamos un nuevo estado inicial y otro de aceptación
            estado_inicial = nuevo_estado()
            estado_aceptacion = nuevo_estado()
            # Agregamos una transición vacía desde el estado inicial hacia el primer estado del operando
            transicion_vacia(estado_inicial, operando[0])
            # Agregamos una transición vacía desde el primer estado del operando hacia el estado de aceptación
            transicion_vacia(operando[0], estado_aceptacion)
            # Agregamos una transición vacía desde el estado inicial hacia el estado de aceptación
            transicion_vacia(estado_inicial, estado_aceptacion)
            # Agregamos una marca a la pila para indicar que hay un nuevo operando
            pila.append((estado_inicial, estado_aceptacion, set()))
        elif simbolo == '*':
            # Obtenemos el último operando que está en la pila
            operando = pila.pop()
            # Creamos un nuevo estado inicial y otro de aceptación
            estado_inicial = nuevo_estado()
            estado_aceptacion = nuevo_estado()
            # Agregamos una transición vacía desde el estado inicial hacia el primer estado del operando
            transicion_vacia(estado_inicial, operando[0])
            # Agregamos una transición vacía desde el último estado del operando hacia el estado de aceptación
            transicion_vacia(operando[1], estado_aceptacion)
            # Agregamos una transición vacía desde el último estado del operando hacia el primer estado del operando
            transicion_vacia(operando[1], operando[0])
            # Agregamos una transición vacía desde el estado inicial hacia el estado de aceptación
            transicion_vacia(estado_inicial, estado_aceptacion)
            # Agregamos una marca a la pila para indicar que hay un nuevo operando
            pila.append((estado_inicial, estado_aceptacion, set()))
        elif simbolo == '+':
            # Obtenemos el último operando que está en la pila
            operando = pila.pop()
            # Creamos un nuevo estado inicial y otro de aceptación
            estado_inicial = nuevo_estado()
            estado_aceptacion = nuevo_estado()
            # Agregamos una transición vacía desde el estado inicial hacia el primer estado del operando
            transicion_vacia(estado_inicial, operando[0])
            # Agregamos una transición vacía desde el último estado del operando hacia el estado de aceptación
            transicion_vacia(operando[1], estado_aceptacion)
            # Agregamos una transición vacía desde el último estado del operando hacia el primer estado del operando
            transicion_vacia(operando[1], operando[0])
            # Agregamos una marca a la pila para indicar que hay un nuevo operando
            pila.append((operando[0], estado_aceptacion, set()))
        elif simbolo == '.':
            # Obtenemos los últimos dos operandos que están en la pila
            operando2 = pila.pop()
            operando1 = pila.pop()
            # Agregamos las transiciones desde el
            estado_inicial = nuevo_estado()
            # Creamos un nuevo estado de aceptación
            estado_aceptacion = nuevo_estado()
            # Agregamos una transición vacía desde el estado inicial hacia el primer estado del operando
            transicion_vacia(estado_inicial, operando[0])
            # Agregamos una transición vacía desde el último estado del operando hacia el estado de aceptación
            transicion_vacia(operando[1], estado_aceptacion)
            # Agregamos una transición vacía desde el estado inicial hacia el estado de aceptación
            transicion_vacia(estado_inicial, estado_aceptacion)
            # Agregamos una transición vacía desde el último estado del operando hacia el primer estado del operando
            transicion_vacia(operando[1], operando[0])
            # Agregamos una marca a la pila para indicar que hay un nuevo operando
            pila.append((estado_inicial, estado_aceptacion, set()))
        elif simbolo == '+':
            # Obtenemos el último operando que está en la pila
            operando = pila.pop()
            # Creamos un nuevo estado inicial
            estado_inicial = nuevo_estado()
            # Creamos un nuevo estado de aceptación
            estado_aceptacion = nuevo_estado()
            # Agregamos una transición vacía desde el estado inicial hacia el primer estado del operando
            transicion_vacia(estado_inicial, operando[0])
            # Agregamos una transición vacía desde el último estado del operando hacia el estado de aceptación
            transicion_vacia(operando[1], estado_aceptacion)
            # Agregamos una transición vacía desde el último estado del operando hacia el primer estado del operando
            transicion_vacia(operando[1], operando[0])
            # Agregamos una marca a la pila para indicar que hay un nuevo operando
            pila.append((estado_inicial, estado_aceptacion, set()))
        elif simbolo == '|':
            # Obtenemos los dos últimos operandos que están en la pila
            operando2 = pila.pop()
            operando1 = pila.pop()
            # Creamos un nuevo estado inicial
            estado_inicial = nuevo_estado()
            # Creamos un nuevo estado de aceptación
            estado_aceptacion = nuevo_estado()
            # Agregamos una transición vacía desde el estado inicial hacia el primer estado de cada operando
            transicion_vacia(estado_inicial, operando1[0])
            transicion_vacia(estado_inicial, operando2[0])
            # Agregamos una transición vacía desde el último estado de cada operando hacia el estado de aceptación
            transicion_vacia(operando1[1], estado_aceptacion)
            transicion_vacia(operando2[1], estado_aceptacion)
            # Unimos los alfabetos de ambos operandos
            afd.alfabeto |= operando1[2] | operando2[2]
            # Agregamos una marca a la pila para indicar que hay un nuevo operando
            pila.append((estado_inicial, estado_aceptacion, afd.alfabeto.copy()))
        elif simbolo == '.':
            # Obtenemos los dos últimos operandos que están en la pila
            operando2, visitados2 = pila.pop()
            operando1, visitados1 = pila.pop()
            # Creamos una nueva expresión regular que representa la concatenación de los operandos
            nueva_expresion = operando1 + operando2
            # Unimos los conjuntos de estados visitados de ambos operandos
            visitados = visitados1 | visitados2
            # Agregamos la clausura vacía del primer operando
            agregar_clausura_vacia(operando1, visitados)
            # Agregamos el alfabeto del primer operando
            afd.alfabeto |= operando1.alfabeto
            # Agregamos el nuevo operando a la pila
            pila.append((nueva_expresion, visitados))
        else: # Si no es ningún símbolo especial, es un símbolo del alfabeto
            afd.alfabeto.add(simbolo)
            if not pila:
                print("hola")
                estado_inicial = nuevo_estado()
                estado_aceptacion = nuevo_estado()
                # Agregamos una transición desde el estado inicial hacia el estado de aceptación
                agregar_transicion(estado_inicial, estado_aceptacion, simbolo)
                # Agregamos una marca a la pila para indicar que hay un nuevo operando
                pila.append((estado_inicial, estado_aceptacion, set()))
            else:
                print("no")
                # Obtenemos el último operando que está en la pila
                operando = pila.pop()
                # Creamos un nuevo estado inicial y otro de aceptación
                estado_inicial = nuevo_estado()
                estado_aceptacion = nuevo_estado()
                # Agregamos una transición desde el estado inicial hacia el estado de aceptación
                agregar_transicion(estado_inicial, estado_aceptacion, simbolo)
                # Agregamos una transición desde el estado inicial hacia el primer estado del operando
                transicion_vacia(estado_inicial, operando[0])
                # Agregamos una transición vacía desde el último estado del operando hacia el estado de aceptación
                transicion_vacia(operando[1], estado_aceptacion)
                # Agregamos una transición vacía desde el último estado del operando hacia el primer estado del operando
                transicion_vacia(operando[1], operando[0])
                # Agregamos una marca a la pila para indicar que hay un nuevo operando
                pila.append((estado_inicial, estado_aceptacion, set()))


    # Al salir del ciclo, sólo debe haber un operando en la pila
    operando = pila.pop()
    # Agregamos la clausura vacía del operando
    agregar_clausura_vacia(operando[0], visitados)
    # Agregamos el alfabeto del operando
    afd.alfabeto |= operando[2]
    # Agregamos el estado inicial, los estados de aceptación y el alfabeto al AFD
    afd.estado_inicial = operando[0]
    afd.estados_aceptacion = visitados
    afd.alfabeto = sorted(list(afd.alfabeto))
    return afd



# Definimos la función que dibuja el AFD utilizando Graphviz
def dibujar_AFD(afd):
    g = Digraph()

    # Dibujamos los estados
    for estado in afd.estados:
        g.node(str(estado), shape='circle')
        if estado.aceptacion:
            g.node(str(estado) + "_", shape='doublecircle')

    # Dibujamos las transiciones
    for estado in afd.estados:
        for simbolo in afd.alfabeto:
            destinos = estado.obtener_transiciones(simbolo)
            for destino in destinos:
                g.edge(str(estado), str(destino), label=simbolo)

    # Dibujamos la flecha hacia el estado inicial
    g.node("inicio", shape='none')
    g.edge("inicio", str(afd.estado_inicial), arrowhead='none')

    # Mostramos el grafo
    g.view()

# Ejemplo de uso
expresion_regular = "(a|b)*(b|a)*abb"
afd = construir_AFD(expresion_regular)
dibujar_AFD(afd)
