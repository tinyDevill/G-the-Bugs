# gameobject.py
import pygame

class GameObject:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        
    def draw(self, screen, camera_rect, zoom):
        pass 

class Platform(GameObject):
    def __init__(self, x, y, width, height, image, is_wall=False):
        super().__init__(x, y, width, height)
        self.image = image
        self.is_wall = is_wall

    def draw(self, screen, camera_rect, zoom):
        if not self.image: return
        screen_x = int((self.rect.x - camera_rect.x) * zoom)
        screen_y = int((self.rect.y - camera_rect.y) * zoom)
        
        scaled_width = int(self.rect.width * zoom)
        scaled_height = int(self.rect.height * zoom)
        if scaled_width <= 0 or scaled_height <= 0: return

        scaled_img = pygame.transform.scale(self.image, (scaled_width, scaled_height))
        screen.blit(scaled_img, (screen_x, screen_y))

def create_platforms_for_level(platform_definitions, platform_image_assets):
    platforms = []
    for p_def in platform_definitions:
        x, y, width, height, image_key, is_wall = p_def
        image = platform_image_assets.get(image_key)
        if image:
            platforms.append(Platform(x, y, width, height, image, is_wall))
        else:
            print(f"Warning: Platform image_key '{image_key}' not found in assets. Platform not created.")
    return platforms

class Animation:
    def __init__(self, frames, frame_duration_seconds, loop=True):
        self.frames = frames if frames else [pygame.Surface((1,1))] 
        self.frame_duration = frame_duration_seconds 
        self.loop = loop
        self.current_frame_index = 0
        self.time_since_last_frame = 0
        self.done = False

    def reset(self):
        self.current_frame_index = 0
        self.time_since_last_frame = 0
        self.done = False

    def update(self, dt_seconds):
        if not self.frames or (self.done and not self.loop):
            return

        self.time_since_last_frame += dt_seconds
        if self.time_since_last_frame >= self.frame_duration:
            self.time_since_last_frame -= self.frame_duration 
            
            self.current_frame_index += 1
            if self.current_frame_index >= len(self.frames):
                if self.loop:
                    self.current_frame_index = 0
                else:
                    self.current_frame_index = len(self.frames) - 1
                    self.done = True
            
    def get_current_frame(self):
        if not self.frames: return None
        return self.frames[self.current_frame_index]

# NEW Projectile class
class Projectile(GameObject):
    def __init__(self, x, y, width, height, image, velocity_x, velocity_y, damage, max_lifetime_seconds=5):
        super().__init__(x, y, width, height)
        self.image = image
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.damage = damage
        self.alive = True
        self.lifetime = 0
        self.max_lifetime = max_lifetime_seconds

    def update(self, dt_seconds):
        if not self.alive:
            return
        self.rect.x += self.velocity_x * dt_seconds
        self.rect.y += self.velocity_y * dt_seconds
        self.lifetime += dt_seconds
        if self.lifetime > self.max_lifetime:
            self.alive = False

    def draw(self, screen, camera_rect, zoom):
        if not self.alive or not self.image:
            return
        
        screen_x = int((self.rect.x - camera_rect.x) * zoom)
        screen_y = int((self.rect.y - camera_rect.y) * zoom)
        
        # Assuming projectile image is already desired size, or scale it if needed
        # For simplicity, let's assume it's pre-scaled or small enough
        # scaled_width = int(self.rect.width * zoom) 
        # scaled_height = int(self.rect.height * zoom)
        # if scaled_width <= 0 or scaled_height <= 0: return
        # scaled_img = pygame.transform.scale(self.image, (scaled_width, scaled_height))
        
        # If projectile image is small and shouldn't scale with world zoom, draw it directly
        # For now, let's make it scale like other game objects
        scaled_img = pygame.transform.scale(self.image, (int(self.rect.width * zoom), int(self.rect.height * zoom)))
        screen.blit(scaled_img, (screen_x, screen_y))
