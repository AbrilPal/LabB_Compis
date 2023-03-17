import graphviz

class EstadoAFD:
    contador_ids = 0

    def __init__(self, estados_afn):
        self.id = EstadoAFD.contador_ids
        EstadoAFD.contador_ids += 1
        self.estados_afn = estados_afn
        self.transiciones = {}

    def add_transition(self, simbolo, estado):
        self.transiciones[simbolo] = estado

    def __str__(self):
        return f"{self.id}"

class AFD:
    def __init__(self, inicial, finales):
        self.inicial = inicial
        self.finales = finales
        self.estados = set([inicial] + list(finales))
    
    def procesar_cadena(self, cadena):
        estado_actual = self.inicial
        for simbolo in cadena:
            if simbolo not in estado_actual.transiciones:
                return False
            estado_actual = estado_actual.transiciones[simbolo]
        return estado_actual in self.finales
    
    def print_transiciones(self):
        print()
        print("----------- AFD --------------")
        print()
        print("transiciones:\n")
        for estado in self.estados:
            print(f"Estado {estado.id}:")
            for simbolo, transicion in estado.transiciones.items():
                print(f"  {simbolo} -> {transicion.id}")


def construir_AFD_desde_AFN(afn, alfabeto):
    inicial = EstadoAFD(afn.inicial.get_closure())
    estados_afd = {inicial}
    nodos = [inicial]

    while nodos:
        estado_afd = nodos.pop()

        for simbolo in alfabeto:
            estados_afn_transicion = set()

            for estado_afn in estado_afd.estados_afn:
                estados_afn_transicion |= estado_afn.get_transitions(simbolo)

            estados_afn_transicion_closure = set()
            for estado_afn_transicion in estados_afn_transicion:
                estados_afn_transicion_closure |= set(estado_afn_transicion.get_closure())

            nuevo_estado_afd = None
            for estado_afd_existente in estados_afd:
                if estado_afd_existente.estados_afn == estados_afn_transicion_closure:
                    nuevo_estado_afd = estado_afd_existente
                    break

            if nuevo_estado_afd is None:
                nuevo_estado_afd = EstadoAFD(estados_afn_transicion_closure)
                estados_afd.add(nuevo_estado_afd)
                nodos.append(nuevo_estado_afd)

            estado_afd.add_transition(simbolo, nuevo_estado_afd)

    finales_afd = set()
    for estado_afd in estados_afd:
        for estado_afn in estado_afd.estados_afn:
            if estado_afn == afn.final:
                finales_afd.add(estado_afd)

    return AFD(inicial, finales_afd)

def graficar_AFD(afd):
    dot = graphviz.Digraph()
    dot.attr(rankdir='LR')
    dot.node(str(afd.inicial.id), shape='point', color='blue')
    for estado in afd.estados:
        dot.node(str(estado.id), shape='doublecircle' if estado in afd.finales else 'circle', 
                 peripheries='2' if estado in afd.finales else '1', 
                 style='bold' if estado in afd.finales else '', 
                 color='red' if estado in afd.finales else 'blue' if estado == afd.inicial else 'black')
        for simbolo, transicion in estado.transiciones.items():
            dot.edge(str(estado.id), str(transicion.id), label=simbolo)
    return dot

