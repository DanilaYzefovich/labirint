# Разработай свою игру в этом файле!
from pygame import *

win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))
display.set_caption('Maze (Лабиринт)')

class GameSprite(sprite.Sprite):
    def __init__(self, image_name, x, y, width, height):
        super().__init__()
        img = image.load(image_name)
        self.image = transform.scale(img, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, image_name, x, y, width, height, speed_x, speed_y):
        super().__init__(image_name, x, y, width, height)
        self.speed_x = speed_x
        self.speed_y = speed_y

    def move(self):
       
        if self.rect.x <= win_width-75 and self.speed_x > 0 or self.rect.x >= 0 and self.speed_x < 0:
            self.rect.x += self.speed_x
        
        if self.rect.y <= win_width-75 and self.speed_y > 0 or self.rect.y >= 0 and self.speed_y < 0:
            self.rect.y += self.speed_y
        
        platforms_touched = sprite.spritecollide(self, walls, False)
        if self.speed_x > 0:
            for platform in platforms_touched:
                self.rect.right = min(self.rect.right, platform.rect.left)
        elif self.speed_x < 0:
            for platform in platforms_touched:
                self.rect.left = max(self.rect.left, platform.rect.right)
        elif self.speed_y > 0:
            for platform in platforms_touched:
                self.rect.botton = min(self.rect.botton, platform.rect.top)
        elif self.speed_y > 0:
            for platform in platforms_touched:
               self.rect.top = max(self.rect.top, platform.rect.botton)

    def fire(self):
        bullet = Bullet(image_name='free-icon-bullet-6015753.png',
                        x=self.rect.right,
                        y=self.rect.centery,
                        width=15,
                        height=15,
                        speed=5)
        bullets.add(bullet)

class Enemy(GameSprite):
    direction = 'left'
    def __init__(self, image_name, x, y, width, height, speed):
        super().__init__(image_name, x, y, width, height)
        self.speed = speed
    def move(self):
        if self.rect.x >= win_width - 120:
            self.direction = 'left'
        elif self.rect.x <= 250:
            self.direction = 'right'
        if self.direction == 'left':

            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
class Bullet(GameSprite):
    def __init__(self, image_name, x, y, width, height, speed):
        super().__init__(image_name, x, y, width, height)
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_width:
            self.kill()

font.init()
font = font.SysFont('Arial', 60)
def win():
    window.fill((0, 255, 100))
    win_text = font.render('YOU WIN!', True, (0, 255, 0))
    window.blit(win_text, (180, 220))

def lose():
    window.fill((0, 255, 100))
    lose_text = font.render('YOU LOSE!', True, (0, 255, 0))
    window.blit(win_text, (180, 220))


background = GameSprite(image_name='msg-4176981761-145.jpg',
                        x=0,
                        y=0,
                        width=win_width,
                        height=win_height)
platform1 = GameSprite(image_name='photo_5237838383160613363_y.jpg',
                      x=320,
                      y=100,
                      width=100,
                      height=300)
platform2 =  GameSprite(image_name='photo_5237838383160613363_y.jpg',
                      x=150,
                      y=100,
                      width=100,
                      height=300)
#platform2.rotate(90)

walls = sprite.Group()
walls.add(platform1)
walls.add(platform2)

bullets = sprite.Group()
ghost = Player(image_name='free-icon-arcade-11104205.png',
               x=35,
               y=275,
               width=75,
               height=75,
               speed_x=0,
               speed_y=0)

vilian1 = Enemy(image_name='free-icon-ghost-121202.png',
               x=win_width-120,
               y=20,
               width=50,
               height=50,
               speed=3)
vilian2 = Enemy(image_name='free-icon-ghost-121202.png',
               x=win_width-120,
               y=420,
               width=50,
               height=50,
               speed=3)




finish = GameSprite(image_name='free-icon-ghost-236417.png',
                    x=600,
                    y=400,
                    width=75,
                    height=75
                    )


clock = time.Clock()
FPS = 60
end = False

run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_w:
                ghost.speed_y = -5
            elif e.key == K_s:
                ghost.speed_y = 5
            elif e.key == K_d:
                ghost.speed_x = 5
            elif e.key == K_a:
                ghost.speed_x = -5
            elif e.key == K_SPACE:
                ghost.fire()
        elif e.type == KEYUP:
            if e.key == K_w:
                ghost.speed_y = 0
            elif e.key == K_s:
                ghost.speed_y = 0
            elif e.key == K_d:
                ghost.speed_x = 0
            elif e.key == K_a:
                ghost.speed_x = 0

    if not end:

        background.draw()
        platform1.draw()
        platform2.draw()
        vilian1.draw()
        vilian1.move()
        vilian2.draw()
        vilian2.move()
        finish.draw()
        ghost.draw()
        ghost.move()
        bullets.draw(window)
        bullets.update()

        sprite.groupcollide(bullets, walls, True, False)

        if sprite.spritecollide(vilian1, bullets, True):
            vilian1.rect.x = win_width + 50
            vilian1.rect.y = win_height + 50
            vilian1.kill()
        if sprite.spritecollide(vilian2, bullets, True):
            vilian2.rect.x = win_width + 50
            vilian2.rect.y = win_height + 50
            vilian2.kill()

        if ghost.rect.colliderect(finish.rect):
            win()
            end = True
        if ghost.rect.colliderect(vilian1.rect):
            lose()
            end = True
        if ghost.rect.colliderect(vilian2.rect):
            lose()
            end = True
         

    display.update()
    clock.tick(FPS)

