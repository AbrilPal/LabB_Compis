from collections import deque
from graphviz import Digraph

class Estado:
    contador_ids = 0
    def __init__(self):
        self.id = Estado.contador_ids
        Estado.contador_ids += 1
        self.transiciones = {}
        self.epsilon_transiciones = set()
        self.final = False

    def add_transition(self, simbolo, estado):
        if simbolo in self.transiciones:
            if estado not in self.transiciones[simbolo]:
                self.transiciones[simbolo].add(estado)
        else:
            self.transiciones[simbolo] = {estado}

    def add_epsilon_transition(self, estado):
        self.epsilon_transiciones.add(estado)

    def get_transitions(self, simbolo):
        return self.transiciones.get(simbolo, set())

    def get_epsilon_transitions(self):
        return self.epsilon_transiciones

    def get_closure(self):
        closure = set()
        nodos = [self]
        while nodos:
            nodo = nodos.pop()
            closure.add(nodo)
            for estado in nodo.get_epsilon_transitions():
                if estado not in closure:
                    nodos.append(estado)
        return list(closure)

    def get_move(self, simbolo):
        move = set()
        for estado in self.get_closure():
            for transicion in estado.get_transitions(simbolo):
                move |= transicion.get_closure()
        return move

    def __str__(self):
        return f"{self.id}"

class AFD:
    def __init__(self, inicial, finales):
        self.inicial = inicial
        self.finales = finales
        self.estados = [inicial]
        self.transiciones = {}

    def add_estado(self, estado):
        if estado not in self.estados:
            self.estados.append(estado)

    def add_transicion(self, origen, simbolo, destino):
        print(destino, "destino")
        self.transiciones[(origen, simbolo)] = destino

    def get_destino(self, origen, simbolo):
        return self.transiciones.get((origen, simbolo), None)

    def construir_desde_afn(self, afn, alfabeto):
        # Obtener el cierre-épsilon del estado inicial del AFN
        cierre_inicial = afn.inicial.get_closure()
        # Crear un estado inicial del AFD a partir del cierre-épsilon obtenido
        inicial = Estado()
        for est in cierre_inicial:
            if est == afn.final:
                inicial.final = True
        self.inicial = inicial
        self.estados = [inicial]

        # Procesar los estados en la cola
        cola = deque([inicial])
        while cola:
            est = cola.popleft()
            # Obtener las transiciones del estado actual
            for simbolo in alfabeto:
                # Obtener el conjunto de estados alcanzados por el símbolo actual
                conjunto = set()
                for e in est.get_closure():
                    conjunto |= e.get_transitions(simbolo)
                # Si el conjunto obtenido no es vacío
                if conjunto:
                    # Obtener el cierre-épsilon del conjunto obtenido
                    cierre = set()
                    for e in conjunto:
                        cierre |= e.get_closure()
                    # Crear un nuevo estado para el conjunto obtenido si aún no ha sido creado
                    nuevo_estado = None
                    for e in self.estados:
                        if e.get_closure() == cierre:
                            nuevo_estado = e
                            break
                    if nuevo_estado is None:
                        nuevo_estado = Estado()
                        for e in cierre:
                            if e in afn.final:
                                nuevo_estado.final = True
                        self.estados.append(nuevo_estado)
                        cola.append(nuevo_estado)
                    # Añadir la transición al AFD
                    self.add_transicion(est, simbolo, nuevo_estado)

    def match(self, cadena):
        estado_actual = self.inicial
        for simbolo in cadena:
            estado_actual = self.get_destino(estado_actual, simbolo)
            if estado_actual is None:
                return False
        return estado_actual.final
    
def imprimir_afd(afd):
    g = Digraph('AFD')
    estados_visitados = set()
    # Agregar nodos y etiquetas para los estados finales
    for estado in afd.estados:
        if estado.final:
            g.node(str(estado.id), shape='doublecircle')
            estados_visitados.add(estado)
    # Agregar nodos y etiquetas para los estados no finales
    for estado in afd.estados:
        if estado not in estados_visitados:
            g.node(str(estado.id))
    # Agregar transiciones
    for origen, simbolo in afd.transiciones:
        destino = afd.transiciones[(origen, simbolo)]
        g.edge(str(origen.id), str(destino.id), label=simbolo)
    print(g)

