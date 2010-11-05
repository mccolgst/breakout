import pygame, sys, pygame.time, os
from pygame.locals import *

DIRECTIONS = {'none': -1, 'left':0, 'right': 1, 'down' : 2, 'up':3, 'downleft':4, 'downright':5, 'upleft':6, 'upright':7}
MOVESPEED = 4
BALLSPEED = 3

pygame.init()
screen = pygame.display.set_mode((460, 460), 0, 32)
pygame.display.set_caption('Breakout!')

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
		self.rect = pygame.rect.Rect(self.x,self.y,70,15)
	
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
		self.width = 55
		self.height = 15
		self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)

	def update(self):
		pygame.draw.rect(screen, (255,0,0), self.rect)

class Ball(object):
	def __init__(self):
		self.x = background.get_width()/2 - 50
		self.y = 250
		self.width = 15
		self.height = 15
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

class Game():
    def __init__(self):
        self.player = Player()
        self.keyboard = Keyboard(self.player)
        self.current_level = 0
        self.blocks = self.make_blocks(self.load_level(self.current_level))
        self.ball = Ball()
        self.updateables = [self.player, self.ball]
        self.levels = self.all_levels()

    def all_levels(self):
        levels = [f for f in os.listdir('.') if f[-3:] == 'lvl']
        return levels

    def load_level(self, level = 0):
        f = open('level'+str(level)+'.lvl')
        leveldata = [l.rstrip().split(',') for l in f.readlines()]
        return leveldata

    def next_level(self):
        del self.blocks[:]
		#todo: mid level transition text perhaps? (need to learn about scene transitions)
        self.blocks = self.make_blocks(self.load_level(self.current_level))
		

    def make_blocks(self, leveldata): 
        blocks = []
        y = 40
        for line in leveldata:
            x = 50
            for b in line:
                if int(b) == 1:
                    blocks.append(Block(x, y))
                x += 70
            y += 25
        return blocks

    def update(self):
        keepGoing = True
        keepGoing = self.keyboard.handle_input()
        for u in self.updateables:
            u.update()

        for b in self.blocks:
            b.update()
            if self.ball.rect.colliderect(b.rect):
                self.ball.change_direction('y')
                self.blocks.pop(self.blocks.index(b))

        if self.player.rect.colliderect(self.ball.rect):
            self.ball.change_direction('y')

        if len(self.blocks) == 0: #won (this level)
            self.current_level += 1
            print self.current_level
            print self.levels
            if self.current_level >= len(self.levels):
                keepGoing = False
            else:
                self.next_level()
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
				if event.key == K_ESCAPE:
					return False
				if event.key == K_RIGHT:
					self.player.move = DIRECTIONS['right']

				if event.key == K_LEFT:
					self.player.move = DIRECTIONS['left']

			if event.type == KEYUP:
				self.player.move = 2 #todo: fix
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

