import pygame
import sys
import random

# Constants
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 50
BULLET_SIZE = 10
TARGET_SIZE = 30
EXPLOSION_SIZE = 50  # Size of the explosion effect
FPS = 60
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("rocketship.png")  # Load player image
        self.image = pygame.transform.scale(self.image, (PLAYER_SIZE, PLAYER_SIZE))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
        self.speed = 5

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("rocketship.png")  # Load bullet image
        self.image = pygame.transform.scale(self.image, (BULLET_SIZE, BULLET_SIZE))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

# Target class
class Target(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("asteroid.png")  # Load asteroid image
        self.image = pygame.transform.scale(self.image, (TARGET_SIZE, TARGET_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - TARGET_SIZE)
        self.rect.y = random.randint(0, HEIGHT // 2)

    def update(self):
        self.rect.y += 3
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - TARGET_SIZE)
            self.rect.y = random.randint(0, HEIGHT // 2)

# Explosion class
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((EXPLOSION_SIZE, EXPLOSION_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.explosion_duration = 10

    def update(self):
        self.explosion_duration -= 1
        if self.explosion_duration <= 0:
            self.kill()

# Game initialization
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Shooting Game")
clock = pygame.time.Clock()

player = Player()
bullets = pygame.sprite.Group()
targets = pygame.sprite.Group()
explosions = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

score = 0  # Initialize the score

# Initial targets
for _ in range(5):
    target = Target()
    targets.add(target)
    all_sprites.add(target)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # Shoot a bullet when the space key is pressed
            bullet = Bullet(player.rect.centerx, player.rect.top)
            bullets.add(bullet)
            all_sprites.add(bullet)

    # Update player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player.rect.left > 0:
        player.rect.x -= player.speed
    if keys[pygame.K_d] and player.rect.right < WIDTH:
        player.rect.x += player.speed

    all_sprites.update()

    # Check for collisions between bullets and targets
    hits = pygame.sprite.groupcollide(targets, bullets, True, True)
    for hit in hits:
        explosion = Explosion(hit.rect.centerx, hit.rect.centery)
        explosions.add(explosion)
        all_sprites.add(explosion)
        target = Target()
        targets.add(target)
        all_sprites.add(target)
        score += 1  # Increase the score when a target is hit

    # Check for collisions between player and targets
    hits = pygame.sprite.spritecollide(player, targets, False)
    if hits:
        print("Game Over! Score:", score)
        running = False

    # Draw background
    screen.fill(BLACK)

    # Draw sprites
    all_sprites.draw(screen)

    # Display the score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, RED)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
