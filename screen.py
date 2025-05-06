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
    bg = pygame.transform.scale(pygame.image.load("assets/bg.png"), (width, height))
    platform_img = pygame.image.load("assets/tile_2.png")
    wall_img = pygame.image.load("assets/dinding.png")
    return bg, platform_img, wall_img

def draw_background(screen, background, camera_rect, screen_width, screen_height):
    bg_sub = background.subsurface(camera_rect)
    bg_scaled = pygame.transform.scale(bg_sub, (screen_width, screen_height))
    screen.blit(bg_scaled, (0, 0))

def draw_objects(screen, player, platforms, camera_rect, zoom):
    # Scale images first
    for platform in platforms:
        platform.scale_image(zoom)
    player.scale_image(zoom)
    
    # Draw platforms
    for platform in platforms:
        platform.draw(screen, camera_rect, zoom)
    
    # Draw player
    player_pos = (
        (player.rect.x - camera_rect.x) * zoom,
        (player.rect.y - camera_rect.y) * zoom
    )
    screen.blit(player.scaled_image, player_pos)
