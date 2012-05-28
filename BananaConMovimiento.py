
import pilas
from pilas.actores import Banana

class BananaConMovimiento(Banana):

	def __init__(self, x=0, y=0):
		Banana.__init__(self, x, y)

	def actualizar(self):
		self.x += 0.5
		self.y += 0.5

		if self.x > 320:
			self.x = -320

		if self.y > 240:
			self.y = -240


def main():
	BananaConMovimiento()

if __name__ == "main":
	main()