import pygame
import random
class GameSprite(pygame.sprite.Sprite): #=> game sprite adalah komopenen yang ada dialam sebuah game
    #property
    def __init__(self, player_image, player_x, player_y, size_width, size_height, player_speed):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(player_image), (size_width, size_height))
        self.rect = self.image.get_rect() #ambil posisi player
        self.rect.x = player_x #memberi nilai pada posisi x
        self.rect.y = player_y #memberi nilai pada posisi y
        #sehingga playernya itu bisa ditempatin
        self.speed = player_speed #untuk pergerakan musuh/player/npc
    #ini untuk membuat gambar berubah
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    #metode
#membuat sebuah kelas untuk player (player juga merupakan salah satu game sprite)
class Player(GameSprite):
    #dia berupa logika pergerakan player
    def update(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire (self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)
#membuat sebuah kelas untuk musuh (musuh juga merupakan saah satu game sprite)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost 
        if self.rect.y > win_height:
            self.rect.x = random.randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

win_width = 1080
win_height = 720
window = pygame.display.set_mode((win_width, win_height))
background = pygame.transform.scale(
    pygame.image.load("galaxy.jpg"),
    (win_width, win_height))

bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()

for _ in range (5):
    enemy = Enemy("ufo.png", random.randint(80, win_width - 80), 0, 64, 64, 5)
    enemies.add(enemy)

player = Player("rocket.png", 5, win_height-80, 80, 100, 10)
pygame.mixer.init()
pygame.mixer.music.load("space.ogg")
pygame.mixer.music.play()

pygame.font.init()
score_text = pygame.font.Font(None, 60)
show = score_text.render("Score:0", True, pygame.Color("white"))
score = 0

lost = 0 

fps = pygame.time.Clock()
run = True 
finish = False
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif  event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                sound = pygame.mixer.Sound("fire.ogg")
                sound.play()
                player.fire()
    if not finish:
        window.blit(background, (0,0))

        player.update()
        player.reset()
        bullets.update()
        bullets.draw(window)
        enemies.update()
        enemies.draw(window)
        collides = pygame.sprite .groupcollide(enemies, bullets, True, True)
        for c in collides:
             score += 1
             text = "Score" + str(score)
             show = score_text.render(text, True, pygame.Color ("white"))
             enemy = Enemy("ufo.png", random.randint(80, win_width - 80), 0, 64, 64, 5)
             enemies.add(enemy)
        window.blit(show, (10,10))
        if pygame.sprite.spritecollide(player, enemies, False) or lost >= 10:
            over_text = "Game Over! Total Score: " + str(score)
            over = score_text.render(over_text, True, pygame.Color("White"))
            window.fill(pygame.Color("red"))
            window.blit(over, ((win_width - over.get_width()) // 2, (win_height - over.get_height()) // 2))
            finish = True
    pygame.display.update()
    fps.tick(60)