import pygame

class Player:
    def __init__(self, x, y, width, height, image):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = image
        self.scaled_image = image
        self.speed = 5
        self.jump_power = -15
        self.velocity_y = 0
        self.on_ground = False
        self.health = 3  # Pemain memiliki 3 nyawa
        self.max_health = 3

    def move(self, dx=0):
        self.rect.x += dx

    def jump(self):
        self.velocity_y = self.jump_power

    def apply_gravity(self, gravity=1):
        self.velocity_y += gravity
        self.rect.y += self.velocity_y

    def scale_image(self, zoom):
        self.scaled_image = pygame.transform.scale(
            self.image,
            (int(self.rect.width * zoom), int(self.rect.height * zoom))
        )

    def draw(self, screen, camera_rect, zoom):
        screen.blit(self.scaled_image, (
            int((self.rect.x - camera_rect.x) * zoom),
            int((self.rect.y - camera_rect.y) * zoom)
        ))

    def take_damage(self, damage):
        self.health -= 1  # Kurangi 1 nyawa setiap kali terkena serangan
        if self.health <= 0:
            self.die()

    def die(self):
        # Aksi ketika pemain mati, misalnya berhenti permainan atau reset
        print("Player has died!")
        self.health = self.max_health  # Reset health pemain
        # Reset posisi atau menu game over bisa ditambahkan di sini
