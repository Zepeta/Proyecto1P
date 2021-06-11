import pygame
class Agente():
    def __init__(self):
        self.agente = ""
        self.tipo_agente = []
        self.posicion_human = (3,14)
        self.posicion_octopus = (2,10)
        self.posicion_monkey = (5,14)
        self.costos = {
            "Human":[
                (0,None),
                (1,1),
                (2,2),
                (3,3),
                (4,4)
            ],
            "Monkey":[
                (0,None),
                (1,2),
                (2,4),
                (3,3),
                (4,1)
            ],
            "Octopus":[
                (0,None),
                (1,2),
                (2,1),
                (3,None),
                (4,3)
            ]
        }
    def definir_agente(self,agente):
        self.agente = agente
        self.tipo_agente = self.costos[agente]
        posicion_incial  =self.definir_posicion_inicial()
        return self.tipo_agente, posicion_incial
    def definir_posicion_inicial(self):
        if self.agente == "Human":
            return self.posicion_human
        elif self.agente == "Octopus":
            return self.posicion_octopus
        elif self.agente == "Monkey":
            return self.posicion_monkey