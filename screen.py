#screen.py

import pygame

class Camera:
    def __init__(self, width, height, zoom):
        self.rect = pygame.Rect(0, 0, width, height)
        self.zoom = zoom

    def update(self, target, world_width, world_height):
        self.rect.center = target.rect.center
        self.rect.x = max(0, min(self.rect.x, world_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, world_height - self.rect.height))

def load_assets(width, height):
    # Load background
    background = pygame.image.load("assets/image/platform/pl2/bg2.png").convert()
    background = pygame.transform.scale(background, (width, height))
    
    # Load platform assets
    floor1_img = pygame.image.load("assets/image/platform/pl2/floor2_2.png").convert_alpha()
    floor2_img = pygame.image.load("assets/image/platform/pl2/floor2_1.png").convert_alpha()
    platform_img = pygame.image.load("assets/image/platform/pl2/platform2.png").convert_alpha()
    benchbottom_img = pygame.image.load("assets/image/platform/pl2/benchbottom.png").convert_alpha()
    benchside2_1_img = pygame.image.load("assets/image/platform/pl2/benchside2_1.png").convert_alpha()
    benchside2_2_img = pygame.image.load("assets/image/platform/pl2/benchside2_2.png").convert_alpha()
    wall_img = pygame.image.load("assets/image/platform/pl2/wall2_1.png").convert_alpha()
    
    # Load button images
    start_button_img = pygame.image.load("assets/image/start_button.png").convert_alpha()
    start_button_img = pygame.transform.scale(start_button_img, (200, 100))  # Sesuaikan ukuran
    
    exit_button_img = pygame.image.load("assets/image/exit_button.png").convert_alpha()
    exit_button_img = pygame.transform.scale(exit_button_img, (200, 100))  # Ukuran sama dengan tombol start
    
    return background,floor1_img,floor2_img, platform_img,benchbottom_img,benchside2_1_img,benchside2_2_img, wall_img, start_button_img, exit_button_img

def draw_background(screen, background, camera_rect, screen_width, screen_height):
    bg_sub = background.subsurface(camera_rect)
    bg_scaled = pygame.transform.scale(bg_sub, (screen_width, screen_height))
    screen.blit(bg_scaled, (0, 0))
def draw_objects(screen, player, platforms, camera_rect, zoom):
    # Gambar platform terlebih dahulu
    for platform in platforms:
        platform.draw(screen, camera_rect, zoom)
    
    # gambar pemain mengguanakan method draw milik player
    player.draw(screen, camera_rect, zoom)
  

def draw_darkness_with_light(screen, player, camera_rect, zoom, light_radius=120):
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # Semi transparan

    player_pos = (
        int((player.rect.centerx - camera_rect.x) * zoom),
        int((player.rect.centery - camera_rect.y) * zoom)
    )

    pygame.draw.circle(overlay, (0, 0, 0, 0), player_pos, light_radius)

    screen.blit(overlay, (0, 0))
