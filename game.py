import pygame as pg
import sys

from os import path


class BaseGame:
	def __init__(self, width, height):
		# initialization
		pg.init()

		# screen
		self.width = width
		self.height = height

		self.screen = None
		self.surface = pg.display.set_mode((width, height))
		self.clock = pg.time.Clock()

		# current directory
		self.dir = path.dirname(__file__)

		# colors
		self.white = (255, 255, 255)
		self.black = (0, 0, 0)
		self.green = (0, 255, 0)
		self.red = (255, 0, 0)

	def set_screen(self, scr):
		# delete existing screen
		if self.screen != None:
			del self.screen
			self.screen = None

		self.screen = scr
		
		# show new screen
		if self.screen != None:
			self.screen.show()

	def quit(self):
		# exit the game
		pg.quit()
		sys.exit()

	def events(self):
		# handle events in game loop
		for e in pg.event.get():
			if e.type == pg.QUIT:
				self.quit()
