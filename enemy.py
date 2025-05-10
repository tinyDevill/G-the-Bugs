import pygame

class Enemy:
    def __init__(self, x, y, width, height, image, speed=2, attack_range=50, damage=1):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = image
        self.speed = speed
        self.direction = 1
        self.velocity_y = 0
        self.on_ground = False
        self.attack_range = attack_range
        self.damage = damage

    def move(self):
        self.rect.x += self.speed * self.direction

    def patrol(self, left_bound, right_bound):
        self.move()
        if self.rect.left < left_bound or self.rect.right > right_bound:
            self.direction *= -1

    def apply_gravity(self, gravity=3):
        self.velocity_y += gravity
        self.rect.y += self.velocity_y

    def draw(self, screen, camera_rect, zoom):
        if self.image:
            scaled_img = pygame.transform.scale(
                self.image,
                (int(self.rect.width * zoom), int(self.rect.height * zoom))
            )
            screen.blit(
                scaled_img,
                ((self.rect.x - camera_rect.x) * zoom, (self.rect.y - camera_rect.y) * zoom)
            )

    def collides_with_player(self, player_rect):
        return self.rect.colliderect(player_rect)

    def attack(self, player_rect):
        if self.rect.colliderect(player_rect):
            return self.damage
        return 0

    def update(self, player_rect):
        self.patrol(0, 800)
        # Jika musuh menyerang pemain, kurangi nyawa pemain
        return self.attack(player_rect)
