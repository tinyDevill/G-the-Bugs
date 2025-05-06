import pygame

class GameObject:
    def __init__(self, x, y, width, height, image=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = image
        self.scaled_image = None

    def scale_image(self, zoom):
        if self.image:
            self.scaled_image = pygame.transform.scale(
                self.image, 
                (int(self.rect.width * zoom), int(self.rect.height * zoom))
            )
        return self.scaled_image

class Player(GameObject):
    def __init__(self, x, y, width, height, image):
        super().__init__(x, y, width, height, image)
        self.velocity_y = 0
        self.on_ground = False
        self.speed = 5
        self.jump_power = -15
        self.gravity = 0.9

    def move(self, dx=0, dy=0):
        self.rect.x += dx
        self.rect.y += dy

    def jump(self):
        if self.on_ground:
            self.velocity_y = self.jump_power
            self.on_ground = False

    def apply_gravity(self):
        self.velocity_y += self.gravity
        self.move(dy=self.velocity_y)

class Platform(GameObject):
    def __init__(self, x, y, width, height, image, is_wall=False):
        super().__init__(x, y, width, height, image)
        self.is_wall = is_wall

    def draw(self, screen, camera_rect, zoom):
        screen_x = int((self.rect.x - camera_rect.x) * zoom)
        screen_y = int((self.rect.y - camera_rect.y) * zoom)
        
        if self.is_wall and self.scaled_image:
            scaled_height = self.scaled_image.get_height()
            for y_offset in range(0, int(self.rect.height * zoom), scaled_height):
                screen.blit(self.scaled_image, (screen_x, screen_y + y_offset))
        elif self.scaled_image:
            screen.blit(self.scaled_image, (screen_x, screen_y))

def create_platforms(screen_width, screen_height, platform_img, wall_img):
    return [
        Platform(0, screen_height - 50, screen_width, 50, platform_img),
        Platform(200, 450, 150, 20, platform_img),
        Platform(400, 400, 150, 20, platform_img),
        Platform(0, 0, 10, screen_height, wall_img, is_wall=True),
        Platform(screen_width - 10, 0, 10, screen_height, wall_img, is_wall=True)
    ]
