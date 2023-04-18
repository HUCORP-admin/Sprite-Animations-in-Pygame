import pygame as pg
from os import path

from animated_sprite import AnimatedSprite
from spritesheet import SpriteSheet, Animation

vec = pg.math.Vector2


class Player(AnimatedSprite):
	def __init__(self, screen, x, y, *groups):
		super().__init__(groups)
		self.screen = screen

		self.load()

		# sprite
		self.image = self.active_anim.get_frame(0)
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

		# physics
		self.pos = vec(x, y)
		self.vel = vec(0, 0)
		self.acc = vec(0, 0)

		# settings
		self.player_acc = 0.5
		self.player_friction = -0.12

	def load(self):
		spritesheet = SpriteSheet(path.join(self.screen.game.img_dir, 'player_spritesheet.png'), self.screen.game.green)

		# entrance animation
		entrance_frames = [(7, 47, 19, 45), (31, 44, 22, 45), (59, 52, 30, 36), (93, 60, 37, 31), (140, 61, 36, 31), (188, 62, 36, 30), \
			(237, 62, 36, 30), (285, 62, 36, 30), (332, 62, 36, 30), (385, 62, 36, 30), (431, 62, 36, 30), (477, 60, 36, 32), (523, 60, 34, 32), \
			(572, 60, 34, 32), (10, 106, 30, 40), (89, 108, 28, 29), (157, 115, 9, 7), (215, 117, 5, 5), (263, 116, 8, 7), (324, 112, 14, 23), \
			(382, 113, 18, 24), (443, 118, 20, 25), (506, 111, 28, 34), (561, 105, 32, 49), (11, 173, 45, 27), (64, 171, 48, 29), (119, 170, 47, 30), \
			(174, 169, 30, 31), (218, 169, 30, 31), (262, 168, 31, 32), (306, 168, 30, 32)]
		entrance_animation = spritesheet.get_animation(entrance_frames, 0.10, Animation.PlayMode.NORMAL, resize=1.5)
		self.store_animation('entrance', entrance_animation)

		# standing animation
		standing_frames = [(8, 251, 29, 32), (51, 251, 30, 32), (96, 252, 30, 31), (137, 252, 30, 31), (183, 252, 30, 31), (227, 252, 30, 31), \
			(268, 252, 30, 31), (312, 252, 30, 31)]
		standing_animation = spritesheet.get_animation(standing_frames, 0.10, Animation.PlayMode.LOOP, resize=1.5)
		self.store_animation('standing', standing_animation)

		# running animation
		running_frames = [(3, 330, 40, 34), (59, 334, 34, 30), (106, 336, 44, 28), (166, 333, 54, 30), (233, 333, 48, 30), (295, 334, 33, 30), \
			(342, 334, 44, 30), (397, 334, 52, 30), (466, 332, 46, 31)]
		running_animation = spritesheet.get_animation(running_frames, 0.095, Animation.PlayMode.LOOP, resize=1.5)
		self.store_animation('running', running_animation)

		# halting animation
		halting_frames = [(6, 414, 48, 31), (65, 414, 42, 31), (126, 414, 30, 31), (173, 413, 30, 32)]
		halting_animation = spritesheet.get_animation(halting_frames, 0.15, Animation.PlayMode.NORMAL, resize=1.5)
		self.store_animation('halting', halting_animation)

	def get_keys(self):
		keys = pg.key.get_pressed()
		if self.active_name != 'entrance':
			if keys[pg.K_LEFT]:
				self.acc.x = -self.player_acc
			elif keys[pg.K_RIGHT]:
				self.acc.x = self.player_acc

	def animate(self):
		# change entrance animation
		if self.active_name == 'entrance':
			if self.active_anim.get_frame_index(self.elapsed_time) > 13 and \
				self.active_anim.get_frame_index(self.elapsed_time) < 17:
				self.vel.x = -3
			
			elif self.active_anim.get_frame_index(self.elapsed_time) > 17 and self.active_anim.get_frame_index(self.elapsed_time) < 25:
				self.vel.x = 1.5

			elif self.active_anim.get_frame_index(self.elapsed_time) > 25:
				self.vel.x = 0

			if self.is_animation_finished():
				self.set_active_animation('standing')

		# change standing animation
		if self.active_name == 'standing':
			if self.acc.x > 0:
				self.set_active_animation('running')

		# change running animation
		if self.active_name == 'running':
			if self.acc.x < 0:
				self.set_active_animation('halting')

		# change halting animaiton
		if self.active_name == 'halting':
			if self.active_anim.is_animation_finished(self.elapsed_time):
				self.set_active_animation('standing')


		bottom = self.rect.bottom
		self.image = self.active_anim.get_frame(self.elapsed_time)
		self.rect = self.image.get_rect()
		self.rect.bottom = bottom

	def update(self):
		super().update(1/self.screen.game.fps)
		self.animate()

		# update vectors
		self.acc = vec(0, 0)
		self.get_keys()

		# apply friction
		self.acc.x += self.vel.x*self.player_friction
		# equations of motion
		self.vel += self.acc
		self.pos += self.vel + 0.5*self.acc

		self.rect.midbottom = self.pos


class Enemy(AnimatedSprite):
	def __init__(self, screen, x, y, *groups):
		super().__init__(groups)
		self.screen = screen

		self.load()

		# sprite
		self.image = self.active_anim.get_frame(0)
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

		# physics
		self.pos = vec(x, y)
		self.vel = vec(0, 0)
		self.acc = vec(0, 0)

		# settings
		self.player_acc = 0.5
		self.player_friction = -0.12

	def load(self):
		spritesheet = SpriteSheet(path.join(self.screen.game.img_dir, 'enemy_spritesheet.png'), (34, 177, 76))

		# standing animation
		standing_frames = [(28, 247, 34, 63), (73, 248, 34, 62), (115, 248, 35, 61)]
		standing_animation = spritesheet.get_animation(standing_frames, 0.20, Animation.PlayMode.LOOP, flip=True)
		self.store_animation('standing', standing_animation)

	def animate(self):
		bottom = self.rect.bottom
		self.image = self.active_anim.get_frame(self.elapsed_time)
		self.rect = self.image.get_rect()
		self.rect.bottom = bottom

	def update(self):
		# update frame
		super().update(1/self.screen.game.fps)
		self.animate()

		# update vectors
		self.acc = vec(0, 0)

		# apply friction
		self.acc.x += self.vel.x*self.player_friction
		# equations of motion
		self.vel += self.acc
		self.pos += self.vel + 0.5*self.acc

		self.rect.midbottom = self.pos

class Platform(pg.sprite.Sprite):
	def __init__(self, game, x, y, w, h, *groups):
		super().__init__(groups)
		self.screen = game

		# position
		self.x = x
		self.y = y

		# sprite
		self.image = pg.Surface((w, h))
		self.image.fill(self.screen.game.black)
		self.rect = self.image.get_rect()

	def update(self):
		self.rect.x = self.x
		self.rect.y = self.y
