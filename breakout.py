import pygame, sys, pygame.time
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
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.width = 75
		self.height = 20
		self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)

	def update(self):
		pygame.draw.rect(screen, (255,0,0), self.rect)

class Ball(object):
	def __init__(self):
		self.x = background.get_width()/2 - 50
		self.y = 150
		self.width = 20
		self.height = 20
		self.dx = BALLSPEED
		self.dy = BALLSPEED
		self.direction = DIRECTIONS['downright']
		self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)

	def update(self):
		if self.rect.x >= background.get_width() - self.width:
			self.change_direction('x')
		elif self.rect.x <= 0:
			self.change_direction('x')
#		if self.rect.y >= background.get_height() - self.height:
#			self.change_direction('y')
		elif self.rect.y <= 0:
			self.change_direction('y')
		self.rect.x += self.dx
		self.rect.y += self.dy
		pygame.draw.rect(screen, (255,0,0), self.rect)

	def change_direction(self, coord):
		if coord == 'x':
			self.dx = self.dx * -1
		elif coord == 'y':
			self.dy = self.dy * -1

'''class Game():
	def __init__(self):
		self.player = Player()
		self.keyboard = 
'''


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
				self.player.move = 2 #todo: fix
		return True

def make_blocks(): #todo: put in game class
	blocks = []
	x = 50
	for e in range(3):
		blocks.append(Block(x, 40))
		x += 100

	return blocks

def main():
	c = pygame.time.Clock()
	p = Player()
	k = Keyboard(p)
	b = Ball()
#	bl = Block()
#	blocks = [bl]
	blocks = make_blocks()
	updateables = [p, b]
	while k.handle_input():
		c.tick(100)
		screen.blit(background, (0, 0))
		for u in updateables:
			u.update()
		if len(blocks) == 0: #won
			return
		if b.rect.y >= background.get_height() - b.height: #lost
			return
		for block in blocks:
			block.update()
			if b.rect.colliderect(block.rect):
				b.change_direction('y')
				blocks.pop(blocks.index(block))
		if p.rect.colliderect(b.rect):
			b.change_direction('y')
		pygame.display.flip()

if __name__ == '__main__':
	main()
