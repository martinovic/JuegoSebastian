import pilas.mundo
import pilas.fondos
import pilas.comportamientos
import pilas.actores
import pilas.habilidades

__author__="marcelo"
__date__ ="$19/03/2012 20:33:50$"
"""
Dedicado a mi hijo Sebastian
"""

import pilas
import BananaConMovimiento
import random
from pilas.actores import Banana
from pilas.actores import Moneda
from pilas.actores import Bomba
import sys

class Juego:

        comidas = 0
        tiempoJuego = 60
        running = 0

        def __init__(self):
            """
                Instancia de inicio
            """
            pilas.iniciar(600, 600, "Mono come bananas")
			# Sonido
            self.sonido1 = pilas.sonidos.cargar("smile.ogg")
            self.sonido2 = pilas.sonidos.cargar("shout.ogg")
            self.sonido3 = pilas.sonidos.cargar("explosion.ogg")
            self.runGame()

        def runGame(self):
            """
                    Metodo para ejecutar el juego
            """
            # Defino las bases del juego
            # fondo, sonidos, timer
            pilas.mundo.motor.ocultar_puntero_del_mouse()
            # Esto desabilita la musica y los sonidos
            pilas.mundo.deshabilitar_musica()
            pilas.mundo.deshabilitar_sonido()
            self.puntaje = pilas.actores.Puntaje('0',-190,280, pilas.colores.amarillo)
            pilas.actores.Texto('Puntaje:',-260, 280)
            pilas.actores.Texto('Tiempo:', 185,280)
            # instancia el contador de bananas
            self.contador = 0
            self.cuentaMonedas = 0
            self.cuentaBombas = 0
            
			# Fondo
            pilas.fondos.Selva()
            # Temporizador
            self.t = pilas.actores.Temporizador(260, 280, pilas.colores.amarillo)
            self.t.ajustar(self.tiempoJuego, self.terminoTiempo)
            self.t.iniciar()
            # Acciones del mono
            self.mono = pilas.actores.Mono()
            self.mono.aprender(pilas.habilidades.SeguirAlMouse)

            #self.mono.decir("Tengo mucha hambre")
            #self.mono.gritar()
            # Armo las bananas y disparo el evento de colision
            self.crearBananas()
            self.crearMonedas()
            self.crearBombas()

            pilas.eventos.click_de_mouse.conectar(self.eventoMonoBanana)
            self.listaBanas =  [self.banana1, self.banana2, self.banana3]
            self.listaMonedas = [self.moneda1, self.moneda2]
            self.listaBombas = [self.bomba1, self.bomba2, self.bomba3]

            self.testeaColisiones()
            # Esto es para poder reiniciar el juego
            # como el pilas.ejecutar crea un loop debo evitar que se llame
            # mas de una vez.
            if self.running == 0:
                    self.running = 1
                    pilas.ejecutar()

            #print self.running

        def monoAtrapaBanana(self, mono, banana):
            """
                    Evento cuando se atrapa una banana
                    incrementa el contador
            """
            self.puntaje.aumentar(1)
            banana.eliminar()
            self.contador += 1
            if self.contador >=3:
                self.contador = 0
                self.ponerTodasLasBananas()
            #print self.contador

        def monoAtrapaMonedas(self, mono, moneda):
            self.puntaje.aumentar(3)
            moneda.eliminar()
            #mono.sonreir()
            self.cuentaMonedas += 1
            if self.cuentaMonedas >= 2:
                self.cuentaMonedas = 0
                self.ponerTodasLasMonedas()

        def monoAtrapaBombas(self, mono, bomba):
            bomba.explotar()
            #mono.sonreir()
            self.cuentaBombas += 1
            if self.cuentaBombas >= 3:
                self.cuentaBombas = 0
                self.terminoTiempo()

        def terminoTiempo(self):
            """
            Cuando termina el tiempo pone el menu y muestra
            volver a jugar o salir.
            """
            puntos = self.puntaje.obtener_texto()
            #print puntos
            # Elimina el temporizador
            self.t.eliminar()
            self.mono.decir("Muy bien !!! quiero mas bananas ")
            self.mono.gritar()
            # Espera 5 segundos
            ##time.sleep(5)
            texto = "He comido %s bananas " % str(puntos)
            self.mono.decir(texto)
            self.mono.eliminar()
            self.banana1.eliminar()
            self.banana2.eliminar()
            self.banana3.eliminar()
            # Muestra el menu
            opciones = [('Comenzar a jugar', self.comenzar), ('Salir', self.salir)]
            self.menu = pilas.actores.Menu(opciones)

        def comenzar(self):
            """
            Evento para reiniciar el juegoMoneda
            """
            pilas.reiniciar()
            self.runGame()

        def salir(self):
            """
                    Evento para salir del juego
            """
            sys.exit(0)

        def ponerTodasLasBananas(self):
            """
                    Muestra en pantalla las bananas
            """
            self.crearBananas()
            self.listaBanas =  [self.banana1, self.banana2, self.banana3]
            self.testeaColisiones()

        def ponerTodasLasMonedas(self):
            self.crearMonedas()
            self.listaMonedas = [self.moneda1, self.moneda2]
            self.testeaColisiones()

        def ponerTodasLasBombas(self):
            self.crearBombas()
            self.listaBombas = [self.bomba1, self.bomba2, self.bomba3]
            self.testeaColisiones()

        def crearBananas(self):
            """
                    Genera bananas de manera aleatoria
            """
            self.banana1 = BananaConMovimiento(x=self.getRandom(), y=self.getRandom())
            self.banana2 = BananaConMovimiento(x=self.getRandom(), y=self.getRandom())
            self.banana3 = BananaConMovimiento(x=self.getRandom(), y=self.getRandom())

        def crearMonedas(self):
            self.moneda1 = MonedaConMovimiento(x=self.getRandom(), y=self.getRandom());
            self.moneda2 = MonedaConMovimiento(x=self.getRandom(), y=self.getRandom());

        def crearBombas(self):
            self.bomba1 = BombasConMovimiento(x=self.getRandom(), y=self.getRandom());
            self.bomba2 = BombasConMovimiento(x=self.getRandom(), y=self.getRandom());
            self.bomba3 = BombasConMovimiento(x=self.getRandom(), y=self.getRandom());

        def testeaColisiones(self):
            """
                    Testea colisiones
            """
            pilas.mundo.colisiones.agregar(self.mono, self.listaBanas, self.monoAtrapaBanana)
            pilas.mundo.colisiones.agregar(self.mono, self.listaMonedas, self.monoAtrapaMonedas)
            pilas.mundo.colisiones.agregar(self.mono, self.listaBombas, self.monoAtrapaBombas)

        def getRandom(self):
            """
                    Obtiene numeros random para la posicion inicial de las bananas
            """
            saltoRandom = random.randrange(1,50,10)
            return random.randrange(-250, 250, saltoRandom)

        def eventoMonoBanana(self, event):
            self.sonido2.reproducir()

class BananaConMovimiento(Banana):
        """
            Clase para posicionar bananas
        """
        def __init__(self, x=0, y=0):
            Banana.__init__(self, x, y)
            self.circulo = pilas.fisica.Circulo(x, y, 20, restitucion=4, friccion=self.getRandom(), amortiguacion=0)
            self.imitar(self.circulo)
            self._empujar()

        def _empujar(self):
            dx = 1
            dy = 1
            self.circulo.impulsar(dx * 100000, dy * 100000)

        def getRandom(self):
            """
                    Obtiene numeros random para la posicion inicial de las bananas
            """
            return random.randrange(0, 16, 3)

class MonedaConMovimiento(Moneda):
        """
            Clase para posicionar bananas
        """
        def __init__(self, x=0, y=0):
            Moneda.__init__(self, x, y)
            self.circulo = pilas.fisica.Circulo(x, y, 20, restitucion=4, friccion=self.getRandom(), amortiguacion=0)
            self.imitar(self.circulo)
            self._empujar()

        def _empujar(self):
            dx = 1
            dy = 1
            self.circulo.impulsar(dx * 100000, dy * 100000)

        def getRandom(self):
            """
				Obtiene numeros random para la posicion inicial de las bananas
            """
            return random.randrange(0, 16, 3)

class BombasConMovimiento(Bomba):
        """
            Clase para posicionar bananas
        """
        def __init__(self, x=100, y=100):
            Bomba.__init__(self, x, y)
            self.circulo = pilas.fisica.Circulo(x, y, 20, \
										restitucion=4, \
										friccion=self.getRandom(), \
										amortiguacion=0)
            self.imitar(self.circulo)
            self._empujar()

        def _empujar(self):
            dx = 1
            dy = 1
            self.circulo.impulsar(dx * 100000, dy * 100000)

        def getRandom(self):
            """
                    Obtiene numeros random para la posicion inicial de las bananas
            """
            return random.randrange(0, 16, 3)

def main():
        Juego()


if __name__ == "__main__":
    main();
