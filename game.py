import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Platformer")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.velocity_y = 0
        self.on_ground = False  # Pindahkan status ground ke dalam kelas
    
    def update_rect(self):
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

player = Player(50, HEIGHT - 100, 50, 50)
player_speed = 5
gravity = 0.5
jump_power = -12  # Tambah kekuatan lompat

# Platforms
platforms = [
    pygame.Rect(0, HEIGHT - 50, WIDTH, 50),  # Ground
    pygame.Rect(200, 400, 150, 20),
    pygame.Rect(400, 300, 150, 20),
]

def check_collision():
    player.on_ground = False
    # Pindahkan player sementara untuk deteksi tabrakan
    temp_rect = player.rect.copy()
    temp_rect.y = int(player.y + player.velocity_y)
    
    for platform in platforms:
        if temp_rect.colliderect(platform):
            if player.velocity_y > 0:  # Tabrakan bawah
                player.y = platform.top - player.height
                player.velocity_y = 0
                player.on_ground = True
            elif player.velocity_y < 0:  # Tabrakan atas
                player.y = platform.bottom
                player.velocity_y = 0
            return True
    return False

running = True
while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    
    # Gerakan horizontal
    if keys[pygame.K_LEFT]:
        player.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player.x += player_speed
    
    # Lompat
    if keys[pygame.K_SPACE] and player.on_ground:
        player.velocity_y = jump_power
        player.on_ground = False

    # Update posisi vertikal
    if not check_collision():
        player.velocity_y += gravity
        player.y += player.velocity_y
    
    # Update rect dan cek batas layar
    player.update_rect()
    player.y = max(0, min(player.y, HEIGHT - player.height))
    
    # Gambar objek
    for platform in platforms:
        pygame.draw.rect(screen, GREEN, platform)
    pygame.draw.rect(screen, BLUE, player.rect)
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()