import pygame

class Camera:
    def __init__(self, width, height, zoom):
        self.rect = pygame.Rect(0, 0, width, height)
        self.zoom = zoom

    def update(self, target, world_width, world_height):
        self.rect.center = target.rect.center
        self.rect.x = max(0, min(self.rect.x, world_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, world_height - self.rect.height))

class Lighting:
    def __init__(self, radius, max_alpha=128):
        self.radius = radius
        self.max_alpha = max_alpha
        self.gradient_surface = self.create_gradient_surface()
    
    def create_gradient_surface(self):
        diameter = self.radius * 2
        surface = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
        center = (self.radius, self.radius)
        
        for x in range(diameter):
            for y in range(diameter):
                dx = x - center[0]
                dy = y - center[1]
                distance = (dx**2 + dy**2)**0.5
                alpha = self.max_alpha - int((distance / self.radius) * self.max_alpha)
                alpha = max(0, min(alpha, self.max_alpha))
                surface.set_at((x, y), (0, 0, 0, alpha))
        return surface
    
    def draw(self, screen, player_pos, zoom):
        light_mask = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        light_mask.fill((0, 0, 0, self.max_alpha))

        gradient_pos = (
            int(player_pos[0] - self.radius * zoom),
            int(player_pos[1] - self.radius * zoom)
        )
        scaled_gradient = pygame.transform.scale(
            self.gradient_surface,
            (int(self.radius * 2 * zoom), int(self.radius * 2 * zoom))
        )
        light_mask.blit(scaled_gradient, gradient_pos)
        screen.blit(light_mask, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

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
    for platform in platforms:
        platform.scale_image(zoom)
    player.scale_image(zoom)

    for platform in platforms:
        platform.draw(screen, camera_rect, zoom)

    player_pos = (
        (player.rect.x - camera_rect.x) * zoom,
        (player.rect.y - camera_rect.y) * zoom
    )
    screen.blit(player.scaled_image, player_pos)