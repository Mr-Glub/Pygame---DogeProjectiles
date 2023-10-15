import pygame
import random
import sys

# Initializing Pygame
pygame.init()

# Initializing surface
surface = pygame.display.set_mode((400, 300))

# Initializing RGB Color
color = (0, 0, 0)

# Changing surface color
surface.fill(color)

pygame.display.set_caption('Dodge Projectiles!')
FONT = pygame.font.Font(None, 36)

mainMenu = True
running = True
score = 0


font = pygame.font.Font(None, 36)

class Projectile:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 5, 5)
        self.speed = 1

    def move(self):
        self.rect.move_ip(0, self.speed)

    def draw(self):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)

class Pickup:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 5, 5)
        self.speed = 1.5

    def move(self):
        self.rect.move_ip(0, self.speed)

    def draw(self):
        pygame.draw.rect(surface, (0, 255, 0), self.rect)


clock = pygame.time.Clock()

def GameStart():
    global running
    global mainMenu
    global score

    score = 0
    playerSpeed = 200
    playerYVelocity = 0
    playerSize = 20
    PlayerPos_x = 100
    PlayerPos_y = 270 - playerSize

    Lives = 1

    spawnTime = 1
    currentSpawnTime = spawnTime

    PspawnTime = 5
    PcurrentSpawnTime = PspawnTime

    projectiles = []
    pickups = []

    surface.fill((0,0,0))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()

        dt = clock.tick(60) / 1000.0

        surface.fill(color)
        pygame.draw.rect(surface, (100, 100, 100), [0, 260, 1000, 40], 0)

        scoreText = font.render(f"Score: {score}\nLives: {Lives}", True, (255, 255, 255))
        surface.blit(scoreText, (10, 10))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and PlayerPos_x > 0:
            PlayerPos_x -= playerSpeed * dt
        if keys[pygame.K_d] and PlayerPos_x < (400- playerSize):
            PlayerPos_x += playerSpeed * dt
        if keys[pygame.K_SPACE] and PlayerPos_y >= 235:
            playerYVelocity = 250
        if keys[pygame.K_s] and PlayerPos_y < 270-playerSize:
            playerYVelocity -= 100

        PlayerPos_y -= playerYVelocity * dt
        playerYVelocity -= playerYVelocity * dt

        if PlayerPos_y >= 270 - playerSize:
            PlayerPos_y = 270 - playerSize
            playerYVelocity = 0

        if PlayerPos_y < 235:
            playerYVelocity += -5

        player_rect = pygame.Rect(PlayerPos_x, PlayerPos_y, 10, 10)

        

        currentSpawnTime -= dt
        if currentSpawnTime <= 0:
            newProjectile = Projectile(random.randint(0, 400), 0)
            projectiles.append(newProjectile)
            currentSpawnTime = spawnTime

        for projectile in projectiles:
            projectile.move()
            projectile.draw()

        for projectile in projectiles[:]:
            if projectile.rect.y >= 260:
                projectiles.remove(projectile)
            if player_rect.colliderect(projectile.rect):
                Lives -= 1
                projectiles.remove(projectile)
                if Lives <= 0:
                    running = False
                    mainMenu = True
                    Menu()
            else:
                score += 1

        PcurrentSpawnTime -= dt
        if PcurrentSpawnTime <= 0:
            newPickup = Pickup(random.randint(0, 400), 0)
            pickups.append(newPickup)
            PcurrentSpawnTime = PspawnTime

        for pickup in pickups[:]:
            if pickup.rect.y >= 260:
                pickups.remove(pickup)

        for pickup in pickups:
            pickup.move()
            pickup.draw()

            if player_rect.colliderect(pickup.rect):
                Lives += 1
                pickups.remove(pickup)

        spawnTime -= 0.01 * dt

        pygame.draw.rect(surface, (50, 50, 100), (PlayerPos_x, PlayerPos_y, 10, 10), 0)

        pygame.display.flip()

def Menu():
    global mainMenu
    global running

    surface.fill((0,0,0))

    event = ""
    while mainMenu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                mainMenu = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = True
                    GameStart()
                if event.key == pygame.K_ESCAPE:
                    mainMenu = False
                    pygame.quit()
                    
        text_start = FONT.render("Start Game (Enter)", True, (255,255,255))
        text_quit = FONT.render("Quit (Esc)", True, (255,255,255))
        text_score = FONT.render(f"PreviousScore = {score}",True, (255,255,255))

        surface.blit(text_start, (10, 200))
        surface.blit(text_quit, (10, 100))
        surface.blit(text_score, (10,0))

        pygame.display.flip()

Menu()

pygame.quit()
