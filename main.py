from typing import Any
from pygame import*
from random import randint

mixer.init()
mixer.music.load("bg.mp3")
mixer.music.set_volume(0.2)
mixer.music.play(-1)
fire_sound = mixer.Sound("kick.ogg")
fire_sound.set_volume(0.4)

font.init()
my_font = font.SysFont("Times", 36)
font1 = font.SysFont("Times", 80)
font2 = font.SysFont("Times", 100)
win = font1.render('You win', True, (0, 102, 0))
lose = font1.render('You lose', True, (153, 0, 0))

window = display.set_mode((700, 600))
bg = transform.scale(image.load("forest.jpg"), (700, 600))
clock = time.Clock()
game = True
finish = False
lost = 0
score = 0
max_lost = 5
hp = 3

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, x, y, width, height, speed):
        sprite.Sprite.__init__(self)
        self.speed = speed
        self.image = transform.scale(image.load(player_image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        buttons = key.get_pressed()
        if buttons[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if buttons[K_d] and self.rect.x < 645:
            self.rect.x += self.speed
    
    def fire(self):
        bullet = Bullet("paw.png", self.rect.centerx, self.rect.centery, 30, 30, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = -40
            self.rect.x = randint(0, 395)
            global lost
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
        
player = Player("cat.png", 200, 395, 90, 100, 15)
enemies = sprite.Group()
for i in range(5):
    enemy = Enemy("wasp.png", randint(0, 640), -40, 70, 50, randint(1, 4))
    enemies.add(enemy)
bullets = sprite.Group()



while game == True:
    for i in event.get():
        if i.type == QUIT:
            game = False
        elif i.type == KEYDOWN:
            if i.key == K_SPACE:
                player.fire()
                fire_sound.play()

    if finish != True:
        window.blit(bg, (0, 0))
        player.draw()
        player.update()
        enemies.draw(window)
        enemies.update()
        bullets.update()
        bullets.draw(window)
        if sprite.spritecollide(player, enemies, True):
            hp -= 1
            enemy = Enemy("wasp.png", randint(0, 640), -40, 70, 50, randint(1, 4))
            enemies.add(enemy)
        if sprite.groupcollide(enemies, bullets, True, True):
            score += 1
            enemy = Enemy("wasp.png", randint(0, 640), -40, 70, 50, randint(1, 4))
            enemies.add(enemy)
        if score > 15:
            finish = True
            window.blit(win, (240, 100))
        if hp <= 0 or lost >= 5:
            finish = True
            window.blit(lose, (230, 100))

        if hp == 3:
            life_color = (204, 0, 204)
        if hp == 2:
            life_color = (204, 0, 102)
        if hp == 1:
            life_color = (204, 0, 0)
        if hp == 0:
            life_color = (102, 0, 0)
        text_hp = font2.render(str(hp), True, (life_color))
        window.blit(text_hp, (650, -10))

        text_lost = my_font.render("Пропущено: "+ str(lost), True, (32, 32, 32))
        window.blit(text_lost, (5, 0))

        text_score = my_font.render("Рахунок: "+ str(score), True, (32, 32, 32))
        window.blit(text_score, (5, 40))

    else:
        time.delay(5000)
        finish = False
        score = 0
        hp = 3
        lost = 0
        for i in enemies:
            i.kill()

        for i in range(5):
            enemy = Enemy("wasp.png", randint(0, 640), -40, 70, 50, randint(1, 4))
            enemies.add(enemy) 

        for i in bullets:
            i.kill()
        

    display.update()
    clock.tick(40)