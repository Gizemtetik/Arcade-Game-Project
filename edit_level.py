import pygame
import pickle
from os import path


pygame.init()

clock = pygame.time.Clock()
fps = 120 #ekranın her saniyede kaç kez güncellenmesi

#game window
tile_size = 15
cols = 40
margin = 100
screen_width = tile_size * cols  #yaygın oyunlarda 
screen_height = (tile_size * cols) + margin  #yaygın oyunlarda

screen = pygame.display.set_mode((screen_width, screen_height))  #bir pencere oluşturur ve bu pencerenin boyutunu belirlemek için bir argüman
pygame.display.set_caption('Level Editor')


#load images
bg_img = pygame.image.load("C:/Masaüstü\OYUNPROJE_RECREA\oyunprojeödevi\img\matthew-mcbrayer-qD9xzm7yK9U-unsplash.jpg")
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height - margin)) #belirtilen genişlik ve yükseklik değerlerinden bir kenar boşluğunu çıkarmak
dirt_img = pygame.image.load("C:/Masaüstü\OYUNPROJE_RECREA\oyunprojeödevi\img\duvarforgame.jpg")
blob_img = pygame.image.load('img/shooterOpen.png')
lava_img = pygame.image.load('img/hiddenSpikes.png')
coin_img = pygame.image.load('img/coin.png')
exit_img = pygame.image.load('img/goal.png')
save_img = pygame.image.load("C:/Masaüstü\OYUNPROJE_RECREA\oyunprojeödevi\img\saveblue.png")
load_img = pygame.image.load("C:/Masaüstü\OYUNPROJE_RECREA\oyunprojeödevi\img\loadblueee.png")


#define game variables
clicked = False  # mouse click false iken level 1 ' dan başlamak.
level = 1

#define colours
white = (255, 255, 255) # DEĞİŞTİRLEBİLİR.......!
pinky = (246, 155, 209)
blackblue=(0, 0, 135)

font = pygame.font.SysFont('Futura', 24)

#create empty tile list
world_data = []  # oyun dünyasını create etmek 
for row in range(41):
	r = [0] * 41
	world_data.append(r)

#create boundary
for tile in range(0, 40):
	world_data[39][tile] = 1   # alt sınır
	world_data[0][tile] = 1  # üst sınır
	world_data[tile][0] = 1  # sol satır
	world_data[tile][39] = 1  # sağ satır

#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):   # oyun içinde oynayan kişiye(kullanıcıya) bilgi vermek için yapıldı....
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

def draw_grid(): #grid çizer
	for c in range(0,40):
		#vertical lines
		pygame.draw.line(screen, blackblue, (c * tile_size, 0), (c * tile_size, screen_height - margin)) # dikey çizgiler
		#horizontal lines
		pygame.draw.line(screen, blackblue, (0, c * tile_size), (screen_width, c * tile_size)) # yatay çizgiler

# aşağıdaki kod bloğu ;
# 
def draw_world():
	for row in range(40):
		for col in range(40):
			if world_data[row][col] > 0:
				if world_data[row][col] == 1:
					#dirt blocks
					img = pygame.transform.scale(dirt_img, (tile_size, tile_size)) # yüklenen görüntüyü belirli bir boyuta dönüştürür.
					screen.blit(img, (col * tile_size, row * tile_size)) # görüntüyü ekranın belirli bir konumuna çizer.
				if world_data[row][col] == 2:
					#enemy blocks
					img = pygame.transform.scale(blob_img, (tile_size, tile_size))
					screen.blit(img, (col * tile_size, row * tile_size ))
				if world_data[row][col] == 3:
					#lava
					img = pygame.transform.scale(lava_img, (tile_size, tile_size // 2))
					screen.blit(img, (col * tile_size, row * tile_size + (tile_size // 2)))
				if world_data[row][col] == 4:
					#coin
					img = pygame.transform.scale(coin_img, (tile_size // 2, tile_size // 2))
					screen.blit(img, (col * tile_size + (tile_size // 4), row * tile_size + (tile_size // 4)))
				if world_data[row][col] == 5:
					#exit
					img = pygame.transform.scale(exit_img, (tile_size,tile_size))
					screen.blit(img, (col * tile_size, row * tile_size ))
	
class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button
		screen.blit(self.image, (self.rect.x, self.rect.y))

		return action

#create load and save buttons
save_button = Button(screen_width // 2 - 150, screen_height - 80, save_img)
load_button = Button(screen_width // 2 + 50, screen_height - 80, load_img)

#main game loop
run = True
while run:

	clock.tick(fps)

	#draw background
	screen.fill(pinky)
	screen.blit(bg_img, (0, 0))

	#load and save level
	if save_button.draw():
		#save level data
		pickle_out = open(f'level{level}_data', 'wb')
		pickle.dump(world_data, pickle_out)
		pickle_out.close()
	if load_button.draw():
		#load in level data
		if path.exists(f'level{level}_data'):
			pickle_in = open(f'level{level}_data', 'rb')
			world_data = pickle.load(pickle_in)


	#show the grid and draw the level tiles
	draw_grid()
	draw_world()


	#text showing current level
	draw_text(f'Level: {level}', font, white, tile_size, screen_height - 60)
	draw_text('Press UP or DOWN to change level', font, white, tile_size, screen_height - 30)

	#event handler
	for event in pygame.event.get():
		#quit game
		if event.type == pygame.QUIT:
			run = False
		#mouseclicks to change tiles
		if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
			clicked = True
			pos = pygame.mouse.get_pos()
			x = pos[0] // tile_size
			y = pos[1] // tile_size
			#check that the coordinates are within the tile area
			if x < 40 and y < 40:
				#update tile value
				if pygame.mouse.get_pressed()[0] == 1:
					world_data[y][x] += 1
					if world_data[y][x] > 5:
						world_data[y][x] = 0
				elif pygame.mouse.get_pressed()[2] == 1:
					world_data[y][x] -= 1
					if world_data[y][x] < 0:
						world_data[y][x] = 5
		if event.type == pygame.MOUSEBUTTONUP:
			clicked = False
		#up and down key presses to change level number
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				level += 1
			elif event.key == pygame.K_DOWN and level > 1:
				level -= 1

	#update game display window
	pygame.display.update()

pygame.quit()