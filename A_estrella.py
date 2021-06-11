from numpy import cos
from Mapa import Mapa
from Agente import Agente
class A_estrella:
    def __init__(self):
        self.Agente = Agente()
        self.mapa = Mapa().mapa
        self.costos = []
    
    def calcular_costo(self,opcion,posicion):
        if posicion == opcion:
            return 0
        mapa_opcion = self.mapa[opcion[1]-1,opcion[0]-1]
        if mapa_opcion == self.costos[0][0]:
            return self.costos[0][1]
        elif mapa_opcion ==  self.costos[1][0]:
            return self.costos[1][1]
        elif mapa_opcion ==  self.costos[2][0]:
            return self.costos[2][1]
        elif mapa_opcion ==  self.costos[3][0]:
            return self.costos[3][1]
        elif mapa_opcion ==  self.costos[4][0]:
            return self.costos[4][1]

    def calcular_distancia(self,posicion_a,posicion_final): 
        return abs(posicion_a[0]-posicion_final[0])+abs(posicion_a[1]-posicion_final[1])

    def calcular_heurisitica(self,opcion,posicion_a,posicion_b,costo_previo):
        d = self.calcular_distancia(opcion,posicion_b)
        c = self.calcular_costo(opcion,posicion_a)
        c = c+costo_previo
        h = d+c
        return h,c

    def verificar_costo(self,valor_mapa):
        for valor in self.costos:
            if valor[0] == valor_mapa:
                return valor[1]

    def verificar_opciones(self,x,y,nodos_cerrados,nodos_abiertos_aux):
        opciones = []
        if y<=14:
            abajo = (x,y+1)
            mapa_abajo = self.mapa[y+1-1,x-1]
            valor = self.verificar_costo(mapa_abajo)
            if abajo not in nodos_cerrados and abajo not in nodos_abiertos_aux:
                if valor!=None:
                    opciones.append(abajo)
        if x>1:
            izquierda = (x-1,y)
            mapa_izquierda = self.mapa[y-1,x-1-1]
            valor = self.verificar_costo(mapa_izquierda)
            if izquierda not in nodos_cerrados and izquierda not in nodos_abiertos_aux:
                if valor!=None:
                    opciones.append(izquierda)
        if y>1:
            arriba = (x,y-1)
            mapa_arriba = self.mapa[y-1-1,x-1]
            valor = self.verificar_costo(mapa_arriba)
            if arriba not in nodos_cerrados and arriba not in nodos_abiertos_aux:
                if valor!=None:
                    opciones.append(arriba)
        if x<=14:
            derecha = (x+1,y)
            mapa_derecha = self.mapa[y-1,x-1+1]
            valor = self.verificar_costo(mapa_derecha)
            if derecha not in nodos_cerrados and derecha not in nodos_abiertos_aux:
                if valor!=None:
                    opciones.append(derecha)
        return opciones
    
    def calcular_ruta_optima(self, nodos,posicion_final):
        ruta_optima = []
        nodo = nodos.pop()
        while nodo[0]!=posicion_final:
            nodo = nodos.pop()
        ruta_optima.append(nodo[0])
        nodo_padre = nodo[2]
        while nodos:
            nodo =  nodos.pop()
            if len(nodo)!=2:
                if nodo_padre==nodo[0]: 
                    if nodo[2] not in ruta_optima:
                        ruta_optima.append(nodo[0])
                        nodo_padre = nodo[2]
            else:
                if nodo[0] not in ruta_optima:
                    ruta_optima.append(nodo[0])
        return ruta_optima

    def a_estrella(self, posicion_inicial, posicion_final, costos, costo_subtotal):
        self.costos = costos
        nodos_abiertos_aux = []
        nodos_cerrados = []
        nodos_abiertos = []
        aux = []
        h_0 =  self.calcular_heurisitica(posicion_inicial,posicion_inicial,posicion_final,costo_subtotal)
        aux.append((posicion_inicial,h_0[0],costo_subtotal))
        nodos_abiertos_aux.append(posicion_inicial)     
        nodos_abiertos.append((posicion_inicial,h_0[0]))
        while posicion_final not in nodos_abiertos_aux:
            costo_previo = aux[len(aux)-1][2]
            nodo_x = nodos_abiertos_aux.pop()
            del aux[len(aux)-1]
            opciones = self.verificar_opciones(nodo_x[0],nodo_x[1],nodos_cerrados,nodos_abiertos_aux)
            for opcion in opciones:
                h,c = self.calcular_heurisitica(opcion,nodo_x,posicion_final,costo_previo)
                if ((opcion,h,c)) not in aux:
                    aux.append((opcion,h,c))
                    nodos_abiertos.append((opcion,h,nodo_x))
            aux = sorted(aux, key = lambda aux: aux[1],reverse=True)
            for nodo in aux:
                    nodos_abiertos_aux.append(nodo[0])
            nodos_cerrados.append(nodo_x)
            if posicion_final in nodos_abiertos_aux:
                nodos_cerrados.append(posicion_final)
            
        ruta_optima = self.calcular_ruta_optima(nodos_abiertos.copy(),posicion_final)
        nodos_abiertos.reverse()
        nodos_cerrados.reverse()
        for n_a in nodos_abiertos:
            if n_a[0] == posicion_final:
                nodos_abiertos.remove(n_a)
                nodos_abiertos.insert(0,n_a)
                costo_subtotal = n_a[1]            
        return nodos_abiertos,nodos_cerrados, ruta_optima,costo_subtotal
        
# obj = Aestrella()
# obj.a_estrella((2,4),(7,4),[(0,None),(1,2),(2,4),(3,3),(4,1)])
