import pygame as pg
from sprites import Player, Platform, Enemy

class Screen:
	def __init__(self, game):
		self.game = game

	def show(self):
		# sprite groups
		self.all_sprites = pg.sprite.Group()
		self.platforms = pg.sprite.Group()

		self.player = Player(self, 40, 200, self.all_sprites)
		self.platform = Platform(self, 0, 200, self.game.width, 30, self.all_sprites, self.platforms)
		self.enemy = Enemy(self, 1000, 200, self.all_sprites)

		self.run()

	def run(self):
		while True:
			self.game.clock.tick(self.game.fps)
			self.game.events()
			self.update()
			self.draw()

	def draw(self):
		self.game.surface.fill(self.game.white)
		self.all_sprites.draw(self.game.surface)

		pg.display.flip()

	def update(self):
		self.all_sprites.update()
