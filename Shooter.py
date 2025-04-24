from pygame import *
from random import randint
from time import time as timer
from time import sleep

#arka plan müziği
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play(loops = 999999)
fire_sound = mixer.Sound('Laser.ogg')
explosion_sound = mixer.Sound('explosion.ogg')

#karakterler ve yazıtlar
font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.Font(None, 36)


#böyle resimlere ihtiyacımız var:
img_back = "galaxy.jpg" #oyunun arka planı
img_hero = "rocket.png" #kahraman
img_bullet = "bullet.png" #mermi
img_enemy = "ufo.png" #düşman
img_ast = "asteroid.png"
icon = image.load('ufo.png')

score = 0 #düşmüş gemiler
lost = 0 #kaçırılan gemiler
max_lost = 3 #Bu kadar çok şeyi kaçırırsanız kaybettiniz.
goal = 10
games_won = 0
games_lost = 0
music_timer_started = False

#sprite'lar için ebeveyn sınıfı
class GameSprite(sprite.Sprite):
 #Sınıf kurucusu
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       #sınıf kurucusunu çağırıyoruz (Sprite):
       sprite.Sprite.__init__(self)


       # Her sprite image - resim özelliğini depolamalıdır
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed


       # Her sprite, içine yazıldığı dikdörtgenin  rect özelliğini saklamalıdır
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
 #pencereye kahraman çizen yöntem
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))


#ana oyuncunun sınıfı
class Player(GameSprite):
   #Sprite'ı klavye oklarıyla kontrol etme yöntemi
   def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
 # atış yöntemi (orada bir mermi oluşturmak için oyuncunun yerini kullanırız)
   def fire(self):
       bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
       bullets.add(bullet)


#sprite-düşman sınıfı  
class Monster(GameSprite):
   #düşmanın hareketi
   def update(self):
       self.rect.y += self.speed
       global lost
       #ekranın kenarına ulaştığında kaybolur
       if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)
           self.rect.y = 0
           lost = lost + 1
class Asteroid(GameSprite):
    def update(self):
       self.rect.y += self.speed
       global lost
       #ekranın kenarına ulaştığında kaybolur
       if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)
           self.rect.y = 0

def play_music():
    mixer.music.load('space.ogg')
    mixer.music.play()

#mermi sprite sınıfı  
class Bullet(GameSprite):
   #düşmanın hareketi
   def update(self):
       self.rect.y += self.speed
       #ekranın kenarına ulaştığında kaybolur
       if self.rect.y < 0:
           self.kill()


#Bir pencere oluşturalım
string = "Shooter"
win_width = 700
win_height = 500
display.set_icon(icon)
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
display.set_caption(string)

# sprite oluşturalım
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)


monsters = sprite.Group()
for i in range(1, 6):
   monster = Monster(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(2,3))
   monsters.add(monster)

#asteroid sprite oluşturma
asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Asteroid(img_ast,randint(80,win_width - 80), -40,80,50,randint(2,4))
    asteroids.add(asteroid)

bullets = sprite.Group()


# "oyun bitti" değişkeni: True olduğunda, sprite ana döngüde çalışmayı durdurur
finish = False
#Ana oyun döngüsü:
run = True #bayrak pencereyi kapat düğmesiyle sıfırlanır
reload_check = False
shots = 0
while run:
   #Kapat düğmesindeki olayı tıklayın
   for e in event.get():
       if e.type == QUIT:
           run = False
       #space'e basılma durumunda sprite ateş ediyor
       elif e.type == KEYDOWN:
           if e.key == K_SPACE and reload_check == False:
               fire_sound.play()
               ship.fire()
               shots += 1
               if shots >= 6 and reload_check == False: #eğer oyuncu 5 atış attıysa
                    last_time = timer() #gerçekleştiği zaman
                    reload_check = True #yeniden yükleme bayrağı
           elif e.key == K_SPACE and reload_check == True:
                a = timer()
                if a == 3:
                    reload_check = False




   if not finish:
       # arka planı güncelliyoruz
       window.blit(background,(0,0))


       #ekrana metin yazıyoruz
       text = font2.render("Score: " + str(score), 1, (255, 255, 255))
       window.blit(text, (10, 20))


       text_lose = font2.render("Missed: "+ str(lost), 1, (255, 255, 255))
       window.blit(text_lose, (10, 50))
       
       text_w = font2.render("Games won: "+ str(games_won), 1, (255, 255, 255))
       window.blit(text_w, (10, 80))

       text_l = font2.render("Games lost: "+ str(games_lost), 1, (255, 255, 255))
       window.blit(text_l, (10, 110))


       #sprite hareketleri üretiyoruz
       ship.update()
       monsters.update()
       bullets.update()
       asteroids.update()
 
       #dolma testi

       if reload_check == True:
           now_time = timer()
           if now_time-last_time <= 3:
                if finish == False:
                    reload_text = font2.render("Reloading...",1,(255,0,0))
                    window.blit(reload_text,(260,460))
                else:
                    pass
           else:
               shots = 0
               reload_check = False


       #Döngünün her yinelenmesinde onları yeni bir konumda güncelliyoruz
       ship.reset()
       monsters.draw(window)
       bullets.draw(window)
       asteroids.draw(window)
       #mermi canavar çarpışması kontrolu
       collides = sprite.groupcollide(monsters,bullets,True,True)
       collides_a = sprite.groupcollide(asteroids,bullets,True,True)
       for c in collides:
           #döngü canavarlar vurulana kadar tekrarlanır
           explosion_sound.play()
           monster = Monster(img_enemy,randint(80, win_width - 80),-40,80,50,randint(2,3))
           monsters.add(monster)
           score += 1
       for c in collides_a:
           explosion_sound.play()
           asteroid = Asteroid(img_ast,randint(80,win_width - 80), -40,80,50,randint(2,4))
           asteroids.add(asteroid)
       #kaybetme durumları: lost un 3 olması ve düşmanın değmesi
       if sprite.spritecollide(ship,monsters, False):
           games_lost += 1
           finish = True
           window.blit(lose,(250,250))
       if sprite.spritecollide(ship,asteroids,False):
           games_lost += 1
           finish = True
           window.blit(lose,(250,250))
       if lost >= max_lost:
           games_lost += 1
           finish = True
           window.blit(lose,(250,250))
       #kazanma kontrolu
       if score >= goal:
           if lost >= max_lost:
               games_lost += 1
               finish = True
               window.blit(lose,(250,250))
           elif sprite.spritecollide(ship,monsters, False):
               games_lost += 1
               finish = True
               window.blit(lose,(250,250))
           elif sprite.spritecollide(ship,asteroids,False):
               games_lost += 1
               finish = True
               window.blit(lose,(250,250))
           else:
                games_won += 1
                finish = True
                window.blit(win,(250,250))
       display.update()
    
   else:
       finish = False
       score = 0
       lost = 0
       shots = 0
       lives = 3
       reload_check = False
       for b in bullets:
           b.kill()
       for m in monsters:
           m.kill()
       for a in asteroids:
           a.kill()
       time.delay(1500)
       for i in range(1,6):
           monster = Monster(img_enemy,randint(80,win_width-80),-40,80,50,randint(2,3))
           monsters.add(monster)
       for i in range(1,3):
           asteroid = Asteroid(img_ast,randint(80,win_width - 80), -40,80,50,randint(2,5))
           asteroids.add(asteroid)
   #döngü her 0.05 saniyede bir çalışır
   time.delay(50)
