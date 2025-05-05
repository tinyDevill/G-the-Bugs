import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("G The Bugs Draft")

# Load images
platform_image = pygame.image.load("tile_2.png")
dinding_image = pygame.image.load("dinding.png")
background = pygame.transform.scale(pygame.image.load("bg.png"), (WIDTH, HEIGHT))
player_image = pygame.image.load("player.png").convert_alpha()

# Game variables
clock = pygame.time.Clock()
FPS = 45
zoom = 1.5  # Zoom factor diubah menjadi 1.5x
camera_width = int(WIDTH / zoom)
camera_height = int(HEIGHT / zoom)
camera_rect = pygame.Rect(0, 0, camera_width, camera_height)

# Generate radial gradient untuk lighting
light_radius = 800
gradient_surface = pygame.Surface((light_radius*2, light_radius*2), pygame.SRCALPHA)
for x in range(light_radius*2):
    for y in range(light_radius*2):
        dx = x - light_radius
        dy = y - light_radius
        distance = (dx**2 + dy**2)**0.5
        if distance > light_radius:
            alpha = 0
        else:
            alpha = int((1 - distance/light_radius) * 51)  # Transisi dari 0 ke 51 alpha
        gradient_surface.set_at((x, y), (0, 0, 0, 51 - alpha))

class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.base_image = pygame.transform.scale(player_image, (width, height))
        self.image = pygame.transform.scale(self.base_image, (int(width * zoom), int(height * zoom)))
        self.velocity_y = 0
        self.on_ground = False

    def update_rect(self):
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

player = Player(50, HEIGHT - 100, 50, 50)
player_speed = 5
gravity = 0.9
jump_power = -15

# Platforms
platforms = [
    pygame.Rect(0, HEIGHT - 50, WIDTH, 50),
    pygame.Rect(200, 450, 150, 20),
    pygame.Rect(400, 400, 150, 20),
    # Tambahkan dinding kiri dan kanan
    pygame.Rect(0, 0, 10, HEIGHT),          # Dinding kiri
    pygame.Rect(WIDTH-10, 0, 10, HEIGHT)    # Dinding kanan
]

# platforms 
def draw_platforms(camera):
    for platform in platforms:
        screen_x = int((platform.x - camera.x) * zoom)  # Cast ke integer
        screen_y = int((platform.y - camera.y) * zoom)  # Cast ke integer
        scaled_width = int(platform.width * zoom)       # Cast ke integer
        scaled_height = int(platform.height * zoom)     # Cast ke integer
        
        # Gunakan gambar yang berbeda untuk dinding
        if platform in [platforms[-2], platforms[-1]]:  # Dinding kiri dan kanan
            scaled_image = pygame.transform.scale(dinding_image, (scaled_width, scaled_height))
            # Gambar dinding dengan pola berulang
            for y in range(0, scaled_height, scaled_image.get_height()):
                screen.blit(scaled_image, (screen_x, screen_y + y))
        else:
            scaled_image = pygame.transform.scale(platform_image, (scaled_width, scaled_height))
            screen.blit(scaled_image, (screen_x, screen_y))

        

def check_horizontal_collision():
    player.update_rect()
    for platform in platforms:
        if player.rect.colliderect(platform):
            return True
    return False

def check_vertical_collision():
    player.on_ground = False
    temp_rect = player.rect.copy()
    temp_rect.y = int(player.y + player.velocity_y)
    for platform in platforms:
        if temp_rect.colliderect(platform):
            if player.velocity_y > 0:
                player.y = platform.top - player.height
                player.velocity_y = 0
                player.on_ground = True
            elif player.velocity_y < 0:
                player.y = platform.bottom
                player.velocity_y = 0
            return True
    return False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update camera position
    camera_rect.center = (player.x, player.y)
    camera_rect.x = max(0, min(camera_rect.x, WIDTH - camera_rect.width))
    camera_rect.y = max(0, min(camera_rect.y, HEIGHT - camera_rect.height))

    # Draw background
    bg_sub = background.subsurface(camera_rect)
    bg_scaled = pygame.transform.scale(bg_sub, (WIDTH, HEIGHT))
    screen.blit(bg_scaled, (0, 0))

    # Player movement
    keys = pygame.key.get_pressed()
    original_x = player.x
    if keys[pygame.K_LEFT]:
        player.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player.x += player_speed
    if check_horizontal_collision():
        player.x = original_x
        player.update_rect()

    # Jumping
    if keys[pygame.K_SPACE] and player.on_ground:
        player.velocity_y = jump_power
        player.on_ground = False

    # Gravity and vertical collision
    if not check_vertical_collision():
        player.velocity_y += gravity
        player.y += player.velocity_y
    else:
        player.y = int(player.y)

    # Clamp player position
    player.y = max(0, min(player.y, HEIGHT - player.height))
    player.update_rect()

    # Draw platforms
    draw_platforms(camera_rect)

    # Draw player
    player_screen_x = (player.x - camera_rect.x) * zoom
    player_screen_y = (player.y - camera_rect.y) * zoom
    screen.blit(player.image, (player_screen_x, player_screen_y))

    # Lighting effect dengan gradasi
    light_mask = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    light_mask.fill((0, 0, 0, 128))  # Latar gelap 50% di seluruh layar
    
    # Buat lingkaran terang di sekitar pemain
    pygame.draw.circle(light_mask, (0, 0, 0, 0), 
                       (int(player_screen_x + player.width * zoom // 2), 
                        int(player_screen_y + player.height * zoom // 2)), 
                       light_radius // 2)
    
    # Hitung posisi untuk gradient
    center_x = player_screen_x + (player.width * zoom) // 2
    center_y = player_screen_y + (player.height * zoom) // 2
    gradient_pos = (int(center_x - light_radius), int(center_y - light_radius))
    
    # Gambar gradasi radial
    light_mask.blit(gradient_surface, gradient_pos) # Posisi gradient sesuai dengan posisi player
    screen.blit(light_mask, (0, 0))#make sure to draw the mask after the player and platforms
    

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()