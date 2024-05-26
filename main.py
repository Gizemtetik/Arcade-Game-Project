import pygame
from pygame import image
from pygame.locals import *  #QUİT,K_DOWN,vs. gibi sık kullanılan sabitler için.
from pygame import mixer
import pickle
from os import path


#44100 = standard ve yüksek kalitede
#diğerleri standard oyunlarda kullanılan ses bitleri ,
#buffer = sürekli çalması
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()


#oyunun saniyede kaç kare (frame per second, FPS) hızında çalışacağını belirler
clock = pygame.time.Clock()
fps = 120
#FPS değeri, oyun performansını ve akıcılığını etkiler(120-240)

screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('VOID')

#define font
#oyundaki tüm yazı tipleri
font = pygame.font.SysFont('Bauhaus 93', 70)
font_score = pygame.font.SysFont('Bauhaus 93', 30)

#define game variables
tile_size = 15
game_over = 0
main_menu = True  #oyun henüz ana menüde
level = 1  #kaçıncı seviye , ilk seviye henüz
max_levels = 7 #toplam 7 seviye var.
score = 0

#define colours
white = (255, 255, 255)
blue = (0, 0, 255)

#load images
bg_img = pygame.image.load("C:/Masaüstü\OYUNPROJE_RECREA\oyunprojeödevi\img\matthew-mcbrayer-qD9xzm7yK9U-unsplash.jpg")
bg_img = pygame.transform.scale(bg_img, (600, 600))
restart_img = pygame.image.load("C:/Masaüstü\OYUNPROJE_RECREA\oyunprojeödevi\img\Adsız tasarım.png")
start_img = pygame.image.load('img/button.png')
start_img = pygame.transform.scale(start_img, (80, 80))
exit_img = pygame.image.load('img/button.png')
exit_img = pygame.transform.scale(exit_img, (80, 80))

#load sounds
pygame.mixer.music.load("C:/Masaüstü\OYUNPROJE_RECREA\oyunprojeödevi\img\lady-of-the-80x27s-128379.mp3")
pygame.mixer.music.play(-1, 0.0, 5000)
coin_fx = pygame.mixer.Sound("C:/Masaüstü\OYUNPROJE_RECREA\oyunprojeödevi\img\collect-points-190037.mp3")
coin_fx.set_volume(0.5)
game_over_fx = pygame.mixer.Sound('img/game_over.wav')
game_over_fx.set_volume(0.5)

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

#function to reset level
#pickle import gerekli
#başlangıç konumunu sıfırlar ve yeni level verilerini yükler.
def reset_level(level):
	player.reset(80, 525)
	blob_group.empty()
	coin_group.empty()
	lava_group.empty()
	exit_group.empty()

	#load in level data and create world
	if path.exists(f'level{level}_data'): #o dosya var mı yok mu diye kontrol edildi.
		# level derecesine göre dosya adı da değişir.
		pickle_in = open(f'level{level}_data', 'rb') #rb = read binary
		#dosyayı okur.
		world_data = pickle.load(pickle_in)#verileri yükleyip worlddata'ya atar.
	world = World(world_data)#world nesnesi oluşturur.
	#create dummy coin for showing the score
	score_coin = Coin(tile_size // 2, tile_size // 2) #başlangıç koordinatları.
	coin_group.add(score_coin) #score_coin nesnesini coin_group adlı gruba ekler.
	return world #oluşturulan world nesnesini geri döndürür.

class Button():
	def __init__(self, x, y, image):
		self.image = image #button resmi
		self.rect = self.image.get_rect() #düğmenin konumunu ve boyutu
		#koordinatlar
		self.rect.x = x
		self.rect.y = y
		self.clicked = False #düğme tıklanmadı

	def draw(self):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos): #çarpışıyolar mı
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button
		screen.blit(self.image, self.rect)
		return action

class Player():
	def __init__(self, x, y):
		self.reset(x, y) #başlangıç durumu

	def update(self, game_over):
		dx = 0
		dy = 0
		if game_over == 0:
			#get keypresses
			key = pygame.key.get_pressed() #basılan tuşlar
			if key[pygame.K_UP] : #yukarı ok (5 piksel)
				self.vel_y = -5	
				self.vel_x = 0		
			if key[pygame.K_DOWN] :
				self.vel_y =  5
				self.vel_x = 0
			if key[pygame.K_RIGHT] :
				self.vel_x =  5
				self.vel_y = 0
			if key[pygame.K_LEFT]:
				self.vel_x = -5
				self.vel_y = 0

            #hareketi güncelledi.
			dy += self.vel_y
			dx += self.vel_x			
				
			#check for collision
			for tile in world.tile_list:
				#check for collision in x direction
				#oyuncunun boyutları
				#tile (karo) çarpıştı mı ?
				if tile[1].colliderect(self.rect.x + dx, self.rect.y, 15, 15):
					dx = 0
				#check for collision in y direction
				if tile[1].colliderect(self.rect.x, self.rect.y + dy, 15, 15):
					dy=0

			#check for collision with enemies
			if pygame.sprite.spritecollide(self, blob_group, False):
				game_over = -1 #oyun bitti
				game_over_fx.play() #oyun bitiş sesi

			#check for collision with lava
			if pygame.sprite.spritecollide(self, lava_group, False):
				game_over = -1
				game_over_fx.play()

			#check for collision with exit
			if pygame.sprite.spritecollide(self, exit_group, False):
				game_over = 1 #oyun kazanıldı

			#update player coordinates
			self.rect.x += dx
			self.rect.y += dy

		elif game_over == -1: #oyun kaybedildi.
			self.image = self.dead_image #ölü resmi
			#game over yazısı
			draw_text('GAME OVER!', font, blue, (screen_width // 2) - 200, screen_height // 2)
			#görsel bi efekt sadece her oyunda var hemen hemen
			if self.rect.y > 200:
				self.rect.y -= 5

		#draw player onto screen
		screen.blit(self.image, self.rect)
		return game_over

	def reset(self, x, y):
		self.images = []
		img = pygame.image.load("C:/Masaüstü\OYUNPROJE_RECREA\oyunprojeödevi\img/boy.png")
		img = pygame.transform.scale(img, (15, 15))
		self.images.append(img)
		self.dead_image = pygame.image.load('img/ghost.png')
		self.image = self.images[0]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.vel_y = 0
		self.vel_x = 0	

class World():
	def __init__(self, data):
		self.tile_list = []

		#load images
		brick = pygame.image.load("C:/Masaüstü\OYUNPROJE_RECREA\oyunprojeödevi\img\duvarforgame.jpg")
#nesneleri yönetmek
#boyutları
		row_count = 0
		for row in data:
			col_count = 0
			for tile in row:
				if tile == 1:
					img = pygame.transform.scale(brick, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 2:
					blob = Enemy(col_count * tile_size, row_count * tile_size)
					blob_group.add(blob)
				if tile == 3:
					lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
					lava_group.add(lava)
				if tile == 4:
					coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
					coin_group.add(coin)
				if tile == 5:
					exit = Exit(col_count * tile_size, row_count * tile_size)
					exit_group.add(exit)
				col_count += 1
			row_count += 1

	def draw(self):
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])

class Enemy(pygame.sprite.Sprite):
#düşman sağa sola hareket eder
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('img/shooterOpen.png')
		self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
		self.rect = self.image.get_rect()#düşmanın boyutu
		self.rect.x = x
		self.rect.y = y
		self.move_direction = 1
		self.move_counter = 0

	def update(self):
		self.rect.x += self.move_direction
		self.move_counter += 1
		if abs(self.move_counter) > 50:#sağa sola gider.(zaman birimi)
			self.move_direction *= -1
			self.move_counter *= -1

class Lava(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/hiddenSpikes.png')
		self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Coin(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/coin.png')
		self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

class Exit(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/goal.png')
		self.image = pygame.transform.scale(img, (tile_size,tile_size))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

player = Player(80,525) #koordinat

blob_group = pygame.sprite.Group() #ex ; düşman eklemek istenirse bu gruba eklenebilir.
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

#create dummy coin for showing the score
#score gösteriyor
score_coin = Coin(tile_size // 2, tile_size // 2) #oyunun köşesi
coin_group.add(score_coin)

#load in level data and create world
#dosya okuma = burada yukarıda kullanılan pickle gerekli
#dosya var mı ; varsa pickle.load fonksiyonu ile dosyadan veriler okunur ve world_data değişkenine atanır
if path.exists(f'level{level}_data'):
	pickle_in = open(f'level{level}_data', 'rb')
	world_data = pickle.load(pickle_in)

world = World(world_data)

#create buttons
restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, restart_img)
start_button = Button(screen_width // 2 - 110, screen_height // 2, start_img)
exit_button = Button(screen_width // 2 + 70, screen_height // 2, exit_img)

run = True
while run:

	clock.tick(fps)

	screen.blit(bg_img, (0, 0)) #background resmi

#false durumunda exit ve start
	if main_menu == True:
		if exit_button.draw():
			run = False
		if start_button.draw():
			main_menu = False

#eğer ana menüde değilsek oyun world çizer.
	else:
		world.draw()
#her şeyi günceller.
		if game_over == 0:#oyun devam mı değil mi ?
			blob_group.update() #blob günceller.
			# update score
			#check if a coin has been collected
			if pygame.sprite.spritecollide(player, coin_group, True):#sprite ile coin çakışıyor mu
				score += 1 #artar
				coin_fx.play() #ses efekti
			draw_text('X ' + str(score), font_score, white, tile_size - 10, 10)
		#ekrana çizer
		#gruptaki spritelar oyun ekranına aktarılır
		blob_group.draw(screen)
		lava_group.draw(screen)
		coin_group.draw(screen)
		exit_group.draw(screen)

        #oyuncunun pozisyonunu ve diğer özelliklerini günceller
		game_over = player.update(game_over)

		#if player has died
		if game_over == -1:
			if restart_button.draw():
				world_data = []
				world = reset_level(level)
				game_over = 0
				score = 0

		#if player has completed the level
		if game_over == 1:
			#reset game and go to next level
			level += 1
			if level <= max_levels:#yeni level
				#reset level
				world_data = []
				world = reset_level(level)
				game_over = 0
			else:
				draw_text('YOU WIN!', font, blue, (screen_width // 2) - 140, screen_height // 2)
				if restart_button.draw():#yeni oyun başlar çünkü tamamladı
					level = 1
					#reset level
					world_data = []
					world = reset_level(level)
					game_over = 0
					score = 0

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()