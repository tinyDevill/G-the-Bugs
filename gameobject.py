import pygame

class GameObject:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        
    def draw(self, screen, camera_rect, zoom):
        pass  # Akan dioverride oleh subclass

class Platform(GameObject):
    def __init__(self, x, y, width, height, image, is_wall=False):
        super().__init__(x, y, width, height)
        self.image = image
        self.is_wall = is_wall

    def draw(self, screen, camera_rect, zoom):
        screen_x = int((self.rect.x - camera_rect.x) * zoom)
        screen_y = int((self.rect.y - camera_rect.y) * zoom)
        scaled_img = pygame.transform.scale(
            self.image, 
            (int(self.rect.width * zoom), int(self.rect.height * zoom))
        )
        screen.blit(scaled_img, (screen_x, screen_y))

def create_platforms(screen_width, screen_height, platform_img, wall_img):
    return [
        Platform(0, screen_height-50, screen_width, 50, platform_img),
        Platform(200, 450, 150, 20, platform_img),
        Platform(400, 400, 150, 20, platform_img),
        Platform(0, 0, 10, screen_height, wall_img, is_wall=True),
        Platform(screen_width-10, 0, 10, screen_height, wall_img, is_wall=True)
    ]
