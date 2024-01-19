import pygame
import sys
import webbrowser
import random

# Constants
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 50
BULLET_SIZE = 10
TARGET_SIZE = 30
EXPLOSION_SIZE = 50  # Size of the explosion effect
FPS = 60
BLACK = (0, 0, 0)
RED = (255, 0, 0)

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
        self.speed = 2  # Initial speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - TARGET_SIZE)
            self.rect.y = random.randint(0, HEIGHT // 2)
            
            # Increase speed every 10 points
            if score > 0 and score % 10 == 0:
                self.speed += 5  # Increase speed by 5 units

# Explosion class
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.explosion_image = pygame.image.load("explosion.gif")  # Load explosion image
        self.explosion_image = pygame.transform.scale(self.explosion_image, (EXPLOSION_SIZE, EXPLOSION_SIZE))
        self.image = self.explosion_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.explosion_duration = 10

    def update(self):
        self.explosion_duration -= 1
        if self.explosion_duration <= 0:
            self.kill()

# Function to display login screen
def show_login_screen():
    username = ""
    password = ""
    input_active = None  # To keep track of which input box is active (username or password)
    
    font = pygame.font.Font(None, 36)
    input_font = pygame.font.Font(None, 24)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Check username and password (dummy check for demonstration)
                    if username == "admin" and password == "admin1234":
                        return True
                elif event.key == pygame.K_BACKSPACE:
                    if input_active == "username":
                        username = username[:-1]
                    elif input_active == "password":
                        password = password[:-1]
                elif event.key == pygame.K_TAB:
                    # Switch between input boxes on Tab key
                    if input_active == "username":
                        input_active = "password"
                    else:
                        input_active = "username"
                else:
                    if input_active == "username":
                        username += event.unicode
                    elif input_active == "password":
                        password += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the mouse click is inside the input boxes
                if 300 <= event.pos[0] <= 500 and 200 <= event.pos[1] <= 230:
                    input_active = "username"
                elif 300 <= event.pos[0] <= 500 and 250 <= event.pos[1] <= 280:
                    input_active = "password"
                # Check if the mouse click is inside the hyperlink area
                elif 200 <= event.pos[0] <= 500 and 350 <= event.pos[1] <= 380:
                    webbrowser.open("https://disc-login.netlify.app")
        
        screen.fill(BLACK)
        title_text = font.render("Login", True, RED)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))
        
        username_text = font.render("Username:", True, RED)
        screen.blit(username_text, (150, 200))
        pygame.draw.rect(screen, RED, (300, 200, 200, 30), 2)
        username_input = input_font.render(username, True, RED)
        screen.blit(username_input, (310, 205))
        
        password_text = font.render("Password:", True, RED)
        screen.blit(password_text, (150, 250))
        pygame.draw.rect(screen, RED, (300, 250, 200, 30), 2)
        password_input = input_font.render("*" * len(password), True, RED)
        screen.blit(password_input, (310, 255))
        
        # Render the hyperlink text as an image
        hyperlink_text = font.render("Don't have an account? Sign up here", True, RED)
        # Draw the hyperlink text
        screen.blit(hyperlink_text, (200, 350))
        # Underline the hyperlink text
        pygame.draw.line(screen, RED, (200, 380), (500, 380), 2)
        
        pygame.display.flip()
        clock.tick(FPS)

# Game initialization
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Shooting Game")
clock = pygame.time.Clock()

# Show login screen
if show_login_screen():
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
