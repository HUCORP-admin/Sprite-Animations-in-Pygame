from os import path

from game import BaseGame
from screen import Screen


class Launcher(BaseGame):
	def __init__(self):
		super().__init__(1280, 720)

		# locate asset directories
		self.img_dir = path.join(self.dir, 'img')

		# control
		self.fps = 60

	def start(self):
		screen = Screen(self)
		self.set_screen(screen)


if __name__ == "__main__":
	launcher = Launcher()
	launcher.start()
