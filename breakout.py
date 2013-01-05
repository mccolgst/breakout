#!/usr/bin/python
import pygame, sys, pygame.time, os
from math import cos
from pygame.locals import *

#todo
#powerups (multiple ball? lazers?)
#add challenge
#fix riquochet so that it's realistic, use trig


DIRECTIONS = {'none': -1, 'left':0, 'right': 1, 'down' : 2, 'up':3, 'downleft':4, 'downright':5, 'upleft':6, 'upright':7}
MOVESPEED = 4
BALLSPEED = 4
LEVEL_TOP_MARGIN = 40
LEVEL_LEFT_MARGIN = 50
BLOCK_TOP_MARGIN = 40
BLOCK_LEFT_MARGIN = 70

pygame.init()
screen = pygame.display.set_mode((460, 460), 0, 32)
pygame.display.set_caption('Breakout!')

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))

screen.blit(background, (0,0))
pygame.display.flip()

class Player(object):
	def __init__(self):
		self.x = background.get_width()/2 - 50
		self.y = background.get_height() - 50
		self.move = 2
		self.img = pygame.transform.scale2x(pygame.image.load('images/player.png'))
		self.rect = pygame.rect.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
	
	def update(self):
		if self.move == DIRECTIONS['left']:
			self.rect.x-=MOVESPEED
		elif self.move == DIRECTIONS['right']:
			self.rect.x+=MOVESPEED
		#pygame.draw.rect(screen, (255,0,0), self.rect)
		screen.blit(self.img, self.rect)

class Block(object):
	def __init__(self, x, y, hitpoints):
		self.x = x
		self.y = y
		self.hitpoints = hitpoints
		self.img = self.get_image()
		self.rect = pygame.rect.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())

	def update(self):
		if self.hitpoints % 2 == 0:
			self.color = (0,255,0)
		elif self.hitpoints % 3 == 0:
			self.color = (0,0,255)
		else:
			self.color = (255,0,0)
		#pygame.draw.rect(screen, self.color, self.rect)
		screen.blit(self.img, self.rect)

	def hit(self):
		self.hitpoints = self.hitpoints - 1
		if self.hitpoints is not 0:
			self.img = self.get_image()
		return self.hitpoints
	
	def get_image(self):
		return pygame.transform.scale2x(pygame.image.load('images/block'+str(self.hitpoints - 1)+'.png'))

class Ball(object):
	def __init__(self):
		self.x = background.get_width()/2 - 50
		self.y = 250
		self.dx = BALLSPEED
		self.dy = BALLSPEED
		self.img = pygame.transform.scale2x(pygame.image.load('images/ball.png'))
		self.rect = pygame.rect.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
		self.go = False

	def update(self):
		if self.go == True:
			if self.rect.x >= background.get_width() - self.rect.width:
				self.change_direction('x')
			elif self.rect.x <= 0:
				self.change_direction('x')
		#	if self.rect.y >= background.get_height() - self.height:
		#		self.change_direction('y')
			elif self.rect.y <= 0:
				self.change_direction('y')
			self.rect.x += self.dx
			self.rect.y += self.dy
		screen.blit(self.img, self.rect)

	def change_direction(self, coord):
		if coord == 'x':
			self.dx = self.dx * -1
		elif coord == 'y':
			self.dy = self.dy * -1

	def bounce(self, player_rect):
		#hit_player_x = self.rect.midbottom[0] - player_rect.midbottom[0] #get where it hits on the player, making the center 0
		#self.dx = (((hit_player_x * .2) / BALLSPEED) ** 2) * ((hit_player_x * .2) / BALLSPEED) #dx = (x**2) * x
		self.change_direction('y')

	def reset(self):
		self.rect.x = background.get_width()/2 - 50
		self.rect.y = 250

class Game():
	def __init__(self):
		self.c = pygame.time.Clock()
		self.player = Player()
		self.current_level = 0
		self.ball = Ball()
		self.blocks = []
		self.keyboard = Keyboard(self.player, self.ball)
		self.updateables = [self.player, self.ball]
		self.levels = self.all_levels()
		#self.next_level()
		self.init_screen()

	def init_screen(self):
		welcome_img = pygame.image.load('images/welcome.png')
		welcome_screen = pygame.Surface(screen.get_size())
		welcome_screen.blit(welcome_img, get_rect_for_center(screen, welcome_img))
		screen.blit(welcome_screen, (0, 0))
		pygame.display.update()
		while self.keyboard.start_game() is not True:
			self.c.tick(100)

		del welcome_screen

	def all_levels(self):
		levels = [f for f in os.listdir('levels') if f[-3:] == 'lvl']
		return levels

	def load_level(self, level = 0):
		f = open('levels/level'+str(level)+'.lvl')
		leveldata = [l.rstrip().split(',') for l in f.readlines()]
		return self.make_blocks(leveldata)

	def next_level(self):
		del self.blocks[:]
		self.blocks = self.load_level(self.current_level)
		self.ball.reset()
		self.ball.go = False
		self.transition_screen("Level: %s" %str(self.current_level + 1))

	def transition_screen(self, text):
		transition = pygame.Surface(screen.get_size())
		transition.fill((0, 0, 0))
		#todo:clean up!
		transition_image = pygame.image.load('images/ready.png')
		transition.blit(transition_image, get_rect_for_center(transition, transition_image))
		screen.blit(transition, (0, 0))
		pygame.display.update()
		pygame.time.wait(1500)
		del transition

	def win(self):
		self.transition_screen("You win!")
		

	def make_blocks(self, leveldata): 
		blocks = []
		y = LEVEL_TOP_MARGIN
		for line in leveldata:
			x = LEVEL_LEFT_MARGIN
			for b in line:
				if int(b) != 0:
					blocks.append(Block(x, y, int(b)))
				x += BLOCK_LEFT_MARGIN
			y += BLOCK_TOP_MARGIN
		return blocks

	def update(self):
		keepGoing = True
		keepGoing = self.keyboard.handle_input()
		for u in self.updateables:
			u.update()

		for b in self.blocks: #use collidedict, collidepoint
			b.update()
			if self.ball.rect.colliderect(b.rect):
				#this looks weird and needs to be fixed
				#todo: determine if hit sides or top and change direction accordingly
				self.ball.change_direction('y')
				self.ball.change_direction('x')
				if b.hit() <= 0:
					self.blocks.pop(self.blocks.index(b))

		if self.player.rect.colliderect(self.ball.rect):
			#self.ball.change_direction('y')
			self.ball.bounce(self.player.rect) #send player data to compare to ball data collision

		if len(self.blocks) == 0: #won (this level)
			self.current_level += 1
			if self.current_level >= len(self.levels):#won (the game)
				self.win()
				keepGoing = False
			else:
				self.next_level()
		if self.ball.rect.y >= background.get_height() - self.ball.rect.height: #lost (the game)
			keepGoing = False
		return keepGoing


class Keyboard(object):
	def __init__(self, player, ball):#todo: fix, not sure if keyboardcontroller should require a player instance...
		self.player = player
		self.ball = ball

	def start_game(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				return False
			if event.type == KEYDOWN:
				if event.key == K_SPACE:
					return True
	
	def handle_input(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				return False
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					return False
				if event.key == K_RIGHT:
					self.player.move = DIRECTIONS['right']

				if event.key == K_LEFT:
					self.player.move = DIRECTIONS['left']

				if event.key == K_SPACE and self.ball.go == False:
					self.ball.go = True

			if event.type == KEYUP:
				self.player.move = 2 #todo: fix, '2' doesn't make sense as a 'move'
		return True

def get_rect_for_center(surface, image_to_center):
	image_width = image_to_center.get_width()
	image_height = image_to_center.get_height()
	xpos = (surface.get_width() / 2) - (image_width / 2)
	ypos = (surface.get_height() / 2) - (image_height / 2)
	return pygame.Rect(xpos, ypos, image_width, image_height)

def main():
	game = Game()
	keepGoing = True
	while keepGoing:
		game.c.tick(100)
		screen.blit(background, (0, 0))
		keepGoing = game.update()
		pygame.display.flip()

if __name__ == '__main__':
    main()

