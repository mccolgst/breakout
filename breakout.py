import pygame, sys, pygame.time
import math
from pygame.locals import *

DIRECTIONS = {'none': -1, 'left':0, 'right': 1, 'down' : 2, 'up':3, 'downleft':4, 'downright':5, 'upleft':6, 'upright':7}
MOVESPEED = 4
BALLSPEED = 1

pygame.init()
screen = pygame.display.set_mode((460, 460), 0, 32)
pygame.display.set_caption('Pong!')

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250,250,250))

font = pygame.font.Font(None, 36)
text = font.render("Pong", 1, (10, 10, 10))
textpos = text.get_rect(centerx=background.get_width()/2)
background.blit(text, textpos)

screen.blit(background, (0,0))
pygame.display.flip()

class Player(object):
	def __init__(self):
		self.x = background.get_width()/2 - 50
		self.y = background.get_height() - 50
		self.move = 2
		self.rect = pygame.rect.Rect(self.x,self.y,100,20)
	
	def update(self):
		if self.move == DIRECTIONS['left']:
			self.rect.x-=MOVESPEED
		elif self.move == DIRECTIONS['right']:
			self.rect.x+=MOVESPEED
		pygame.draw.rect(screen, (255,0,0), self.rect)

class Block(object):
	def __init__(self, x, y): #todo:blocks shoud have 'hit points'
		self.x = x
		self.y = y
		self.width = 75
		self.height = 20
		self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)

	def update(self):
		pygame.draw.rect(screen, (255,0,0), self.rect)

class Ball(object):
	def __init__(self, vector):
		self.x = background.get_width()/2 - 50
		self.y = 150
		self.width = 20
		self.height = 20
		self.direction = DIRECTIONS['downright']
		self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)
		self.vector = vector
		self.angle = vector[0]

	def update(self): #todo:kinda ugly
		self.vector = (self.angle, BALLSPEED)
		newpos = self.calcnewpos(self.rect, self.vector)
		self.rect = newpos
		(self.angle, z) = self.vector
		if self.rect.x >= background.get_width() - self.width:
			self.angle = math.pi - self.angle
		elif self.rect.x <= 0:
			self.angle = math.pi - self.angle
		elif self.rect.y <= 0:
			self.angle = - self.angle
		self.vector = (self.angle, z)
		pygame.draw.rect(screen, (255,0,0), self.rect)

	def calcnewpos(self, rect, vector):
		(angle, z) = vector
		(dx, dy) = (z*math.cos(angle), z*math.sin(angle))
		return rect.move(dx * 4, dy * 4)


class Game():
	def __init__(self):
		self.player = Player()
		self.keyboard = Keyboard(self.player)
		self.blocks = self.make_blocks()
		self.ball = Ball((0.47, BALLSPEED))
		self.updateables = [self.player, self.ball]

	def make_blocks(self): #todo: read level from file
		blocks = []
		x = 50
		for e in range(4):
			blocks.append(Block(x, 40))
			x += 100

		return blocks

	def update(self):
		keepGoing = True
		keepGoing =	self.keyboard.handle_input()
		for u in self.updateables:
			u.update()

		for b in self.blocks:
			b.update()
			if self.ball.rect.colliderect(b.rect):
				self.ball.angle = - self.ball.angle
				#self.ball.change_direction('y')
				self.blocks.pop(self.blocks.index(b))

		if self.player.rect.colliderect(self.ball.rect):
			print "COLLIDE"
			self.ball.angle = - self.ball.angle
			#self.ball.change_direction('y')

		if len(self.blocks) == 0: #won
			keepGoing = False
		if self.ball.rect.y >= background.get_height() - self.ball.height: #lost
			keepGoing = False
		return keepGoing



class Keyboard(object):
	def __init__(self, player):#todo: fix, not sure if keyboardcontroller should require a player instance...
		self.player = player
	
	def handle_input(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				return False
			if event.type == KEYDOWN:
				#print event # for debugging

				if event.key == K_ESCAPE:
					return False

				if event.key == K_RIGHT:
					self.player.move = DIRECTIONS['right']

				if event.key == K_LEFT:
					self.player.move = DIRECTIONS['left']

			if event.type == KEYUP:
				self.player.move = DIRECTIONS['none']

		return True


def main():
	c = pygame.time.Clock()
	g = Game()
	keepGoing = True
	while keepGoing:
		c.tick(100)
		screen.blit(background, (0, 0))
		keepGoing = g.update()
		pygame.display.flip()

if __name__ == '__main__':
	main()
