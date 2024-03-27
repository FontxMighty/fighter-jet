
import sys
import pygame
import random
import time

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 800
BACKGROUND = pygame.image.load(r'C:\Users\Dell\Downloads\backgroung.png')
BACKGROUND_RECT = BACKGROUND.get_rect()
JET = pygame.image.load(r'C:\Users\Dell\Downloads\jet (1).png')
ENEMY = pygame.image.load(r'C:\Users\Dell\Downloads\enemy.png')
BULLET = pygame.image.load(r'C:\Users\Dell\Downloads\laser.png')

FPS = 60
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Adjust the distance for a collision (smaller value means closer)
COLLISION_DISTANCE = 30

class Enemy(pygame.sprite.Sprite):
    def _init_(self):
        pygame.sprite.Sprite._init_(self)
        self.image = ENEMY
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WINDOW_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed = random.randrange(1, 5)
        self.health = 100

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > WINDOW_HEIGHT + 10:
            self.rect.x = random.randrange(WINDOW_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed = random.randrange(1, 8)

enemies = pygame.sprite.Group()
for i in range(7):
    enemy = Enemy()
    enemies.add(enemy)

class Player(pygame.sprite.Sprite):
    def _init_(self):
        pygame.sprite.Sprite._init_(self)
        self.image = JET
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = WINDOW_HEIGHT - 10
        self.score = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def _init_(self, x, y):
        pygame.sprite.Sprite._init_(self)
        self.image = BULLET
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -15

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

bullets = pygame.sprite.Group()

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load(r"C:\Users\Dell\Downloads\stranger-things-124008.mp3")
pygame.mixer.music.play(-1)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Kill The Enemy')
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

font = pygame.font.SysFont('comicsans', 30, True)
game_over_font = pygame.font.SysFont('comicsans', 60, True)

game_over = False

run = True

while run:
    clock.tick(FPS)

    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
        player.score += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and len(bullets) < 10:
        player.shoot()

    if keys[pygame.K_LEFT] and player.rect.x > 0:
        player.rect.x -= 7

    elif keys[pygame.K_RIGHT] and player.rect.x < WINDOW_WIDTH - 50:
        player.rect.x += 7

    if keys[pygame.K_UP] and player.rect.y > 600:
        player.rect.y -= 3

    elif keys[pygame.K_DOWN] and player.rect.y < WINDOW_HEIGHT - 100:
        player.rect.y += 3

    all_sprites.update()
    text = font.render(f'Score: {player.score}', 1, RED)
    screen.blit(BACKGROUND, BACKGROUND_RECT)
    screen.blit(text, (650, 50))
    all_sprites.draw(screen)

    # Check for collision between the player and enemies
    if not game_over:
        for enemy in enemies:
            if player.rect.colliderect(enemy.rect):
                game_over = True
                break
    if game_over:
        game_over_text = game_over_font.render("Game Over!", 1, RED)
        game_over_text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        screen.blit(game_over_text, game_over_text_rect)
        score_text = font.render(f'Your Score: {player.score}', 1, RED)
        score_text_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        screen.blit(score_text, score_text_rect)
        pygame.display.flip()
        time.sleep(5)  # Wait for 5 seconds
        run = False

    pygame.display.flip()
    screen.fill(BLACK)

pygame.quit()
