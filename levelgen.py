#!/usr/bin/python
import os, random
MAX_HEIGHT = 4
MAX_WIDTH = 5

def generate_level():
	'''
		generate the next level randomly
	'''
	fileslist = os.listdir('levels')
	#filter the list to levels 
	#TODO: make regex OR put levels in their own database/folder
	level_list = [x for x in fileslist if '.lvl' in x] 
	level_index = len(level_list) #index of the new level to make
	of = open('levels/level%s.lvl' %level_index, 'w')

	#could convert to list comp
	for y in range(MAX_HEIGHT):
		block_row = []
		for x in range(MAX_WIDTH):
			block_health = random.randint(0,2)
			block_row.append(str(block_health))
		of.write(','.join(block_row) +"\n")
	
	of.close()

if __name__ == '__main__':
	generate_level()
