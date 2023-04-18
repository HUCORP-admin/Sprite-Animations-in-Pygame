import pygame as pg


class AnimatedSprite(pg.sprite.Sprite):
	def __init__(self, *groups):
		super().__init__(groups)

		# control
		self.elapsed_time = 0
		self.active_anim = None
		self.active_name = ""
		self.animation_storage = {}

	def store_animation(self, name, anim):
		self.animation_storage[name] = anim

		# if no animation playing, start this one
		if self.active_name == "":
			self.set_active_animation(name)

	def set_active_animation(self, name):
		# check if animation with name exist
		if name not in self.animation_storage.keys():
			print(f'No animation: {name}')
			return

		# check if this animation is already running
		if name == self.active_name:
			return

		self.active_name = name
		self.active_anim = self.animation_storage[name]
		self.elapsed_time = 0

	def is_animation_finished(self):
		return self.active_anim.is_animation_finished(self.elapsed_time)

	def update(self, dt):
		self.elapsed_time += dt
