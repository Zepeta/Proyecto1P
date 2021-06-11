import pygame,sys
from Agente import Agente
from Mapa import Mapa
from A_estrella import A_estrella
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_q
)

class Proyecto:
    def __init__(self):
        self.Mapa = Mapa()
        self.Agente = Agente()
        self.a_estrella = A_estrella()                        
        self.running = True
        self.WIDTH = 480
        self.HEIGHT = 505
        self.screen  = pygame.display.set_mode([self.WIDTH,self.HEIGHT])
        self.menu = True
        self.tipo_costos = []
        self.posicion_inicial = ()
        self.meta = ()
        self.nodos_abiertos = []
        self.nodos_cerrados = []
        self.ruta_optima = []
        self.costo_subtotal = 0
        self.bandera = False
    def mostrarInterfaz(self):
        pygame.init()
        pygame.display.set_caption("Proyecto 1")
        lista_textos = []
        lista_rp = []
        self.screen.fill((255,255,255)) 
        while self.running:
            self.screen.fill((169,169,169))
            self.Mapa.definir_Mapa(self.screen)
            letra = pygame.font.SysFont(None, 30)
            
            texto = letra.render("Comenzar", True, (0,0,0))
            self.screen.blit(texto,(10,485))

            if lista_rp:
                texto_c = letra.render("Continuar", True, (0,0,0))
                self.screen.blit(texto_c,(150,485))
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_q:
                        self.menu = True
                        self.elegir_agente()
                    if event.key == K_ESCAPE:
                        self.running = False
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    self.posicion = pygame.mouse.get_pos() 
                    if (self.posicion[0]//30,self.posicion[1]//30) == self.Mapa.temple:
                        self.meta = self.Mapa.temple
                    if (self.posicion[0]//30,self.posicion[1]//30) == self.Mapa.key:
                        self.meta = self.Mapa.key
                    if (self.posicion[0]//30,self.posicion[1]//30) == self.Mapa.stones:
                        self.meta = self.Mapa.stones
                    if self.posicion[1]//30==16:
                        if self.posicion[0]>=10 and self.posicion[0]<=109 and self.posicion[1]>=485 and self.posicion[1]<=505:
                            if self.posicion_inicial!=() and self.tipo_costos!=() and self.meta!=():
                                self.nodos_abiertos, self.nodos_cerrados, self.ruta_optima, self.costo_subtotal = self.a_estrella.a_estrella(self.posicion_inicial,self.meta,self.tipo_costos,self.costo_subtotal)                         
                                # print("nodos_cerrados",self.nodos_cerrados)
                                # print("nodos_abiertos",self.nodos_abiertos)
                                self.ruta_optima.reverse()
                                print("ruta_optima",self.ruta_optima)
                        if self.posicion[0]>=150 and self.posicion[0]<=249 and self.posicion[1]>=484 and self.posicion[1]<=501:
                            if lista_rp:
                                self.nodos_abiertos, self.nodos_cerrados, self.ruta_optima, self.costo_subtotal = self.a_estrella.a_estrella(self.meta,self.Mapa.portal,self.tipo_costos,self.costo_subtotal)  
                                print("costo total:",self.nodos_abiertos[0][1])
            
            self.trazar_recorrido(lista_textos,lista_rp)
            
            # if self.bandera:
            #     self.nodos_abiertos, self.nodos_cerrados, self.ruta_optima, self.costo_subtotal = self.a_estrella.a_estrella(self.meta,self.Mapa.portal,self.tipo_costos,self.costo_subtotal)                               
            
            imgH, rectH = self.dibujar_posicion(self.Agente.posicion_human[0],self.Agente.posicion_human[1],"H")
            self.screen.blit(imgH,rectH)

            imgO, rectO = self.dibujar_posicion(self.Agente.posicion_octopus[0],self.Agente.posicion_octopus[1],"O")
            self.screen.blit(imgO, rectO)

            imgM, rectM = self.dibujar_posicion(self.Agente.posicion_monkey[0],self.Agente.posicion_monkey[1],"M")
            self.screen.blit(imgM, rectM)

            imgK, rectK = self.dibujar_posicion(self.Mapa.key[0],self.Mapa.key[1],"K")
            self.screen.blit(imgK,rectK)

            imgT, rectT = self.dibujar_posicion(self.Mapa.temple[0],self.Mapa.temple[1],"T")
            self.screen.blit(imgT,rectT)

            imgS, rectS = self.dibujar_posicion(self.Mapa.stones[0],self.Mapa.stones[1],"S")
            self.screen.blit(imgS,rectS)

            imgP, rectP = self.dibujar_posicion(self.Mapa.portal[0],self.Mapa.portal[1],"P")
            self.screen.blit(imgP,rectP) 
            pygame.display.flip()

    def trazar_recorrido(self,lista_textos,lista_rp):
        if self.nodos_abiertos:
            nodo_abierto = self.nodos_abiertos.pop()
            if self.posicion_inicial == self.Agente.posicion_human:
                img, rect = self.dibujar_posicion(nodo_abierto[0][0],nodo_abierto[0][1],"H("+str(nodo_abierto[1])+")")
            elif self.posicion_inicial == self.Agente.posicion_monkey:
                img, rect = self.dibujar_posicion(nodo_abierto[0][0],nodo_abierto[0][1],"M("+str(nodo_abierto[1])+")")
            elif self.posicion_inicial == self.Agente.posicion_octopus:
                img, rect = self.dibujar_posicion(nodo_abierto[0][0],nodo_abierto[0][1],"O("+str(nodo_abierto[1])+")")
            lista_textos.append((img,rect))
            pygame.time.delay(100)
        else:
            del lista_textos[:len(lista_textos)-1]
            while self.ruta_optima:
                nodo = self.ruta_optima.pop()
                letra = pygame.font.SysFont(None, 19)
                img = letra.render("X", True, (255,0,0))
                rect = img.get_rect()
                rect.x = nodo[0]*30+3
                rect.y = nodo[1]*30+9
                lista_rp.append((img,rect))
            for i in range(0,len(lista_rp)):
                self.screen.blit(lista_rp[i][0],lista_rp[i][1])      
        for i in range(0,len(lista_textos)):    
            self.screen.blit(lista_textos[i][0],lista_textos[i][1])

    def dibujar_posicion(self,x,y,texto):
        letra = pygame.font.SysFont(None, 19)
        imgI = letra.render(texto, True, (0,0,0))
        rect = imgI.get_rect()
        rect.x = x*30+2
        rect.y = y*30+8
        return imgI, rect
    
    def elegir_agente(self):
        self.screen.fill((255,255,255))
        while self.menu:
            letra = pygame.font.SysFont(None, 30)
                
            texto = letra.render("Elegir al agente", True, (0,0,0))
            self.screen.blit(texto,(160,40))

            texto_human = letra.render("Human", True, (0,0,0))
            self.screen.blit(texto_human,(160,110))
            
            texto_monkey = letra.render("Monkey", True, (0,0,0))
            self.screen.blit(texto_monkey,(160,160))

            texto_octopus = letra.render("Octopus", True, (0,0,0))
            self.screen.blit(texto_octopus,(160,210))
        
            for event in pygame.event.get(): 
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if pos[0]>=160 and pos[0]<=226 and pos[1]>=110 and pos[1]<=125:
                        self.tipo_costos,self.posicion_inicial = self.Agente.definir_agente("Human")
                        self.menu = False
                    if pos[0]>=160 and pos[0]<=235 and pos[1]>=159 and pos[1]<=175:
                        self.tipo_costos,self.posicion_inicial = self.Agente.definir_agente("Monkey")
                        self.menu = False
                    if pos[0]>=160 and pos[0]<=245 and pos[1]>=209 and pos[1]<=225:
                        self.tipo_costos,self.posicion_inicial = self.Agente.definir_agente("Octopus")
                        self.menu = False
                if event.type == QUIT:
                    self.running = False
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_q:
                        self.menu = False
                    if event.key == K_ESCAPE:
                        self.running = False
                        sys.exit()
            pygame.display.update()
        
proyecto = Proyecto()
proyecto.mostrarInterfaz()


# pkg load signal
# b= [0.729441, -2.18832, 2.18832, -0.729441  ]
# a=[1, -2.37409, 1.92936, -0.532075]
# freqz(b, a)
