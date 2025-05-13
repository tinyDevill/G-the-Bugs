# character.py
import pygame
from animation import Animation

class Player:
    def __init__(self, x, y, width, height):
        self.alive = True
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = 5
        self.jump_power = -15
        self.velocity_y = 0
        self.on_ground = False
        self.health = 3
        self.max_health = 3
        self.facing = "right"
        self.is_attacking = False
        self.attack_cooldown = 0

        
        # Load gambar animasi
        self.load_animations()
        self.current_animation = self.idle_anim
        self.facing = "right"
        
    def load_animations(self):
        # Animasi idle
        idle_img = pygame.image.load("assets/image/player_idle.png").convert_alpha()
        self.idle_anim = Animation([idle_img], 100)
        
        # Animasi jalan
        walk1 = pygame.image.load("assets/image/walk1.png").convert_alpha()
        walk2 = pygame.image.load("assets/image/walk2.png").convert_alpha()
        self.walk_anim = Animation([walk1, walk2], 100)
        
        # Animasi serang
        att1 = pygame.image.load("assets/image/att1.png").convert_alpha()
        att2 = pygame.image.load("assets/image/att2.png").convert_alpha()
        att3 = pygame.image.load("assets/image/att3.png").convert_alpha()
        self.attack_anim = Animation([att1, att2, att3], 50, loop=False)
        
    def move(self, dx=0):
        if not self.is_attacking:  # Tidak bisa bergerak saat menyerang
            self.rect.x += dx
            if dx > 0:
                self.facing = "right"
            elif dx < 0:
                self.facing = "left"

    def jump(self):
        if self.on_ground:
            self.velocity_y = self.jump_power
            self.on_ground = False

    def apply_gravity(self, gravity=1):
        self.velocity_y += gravity
        self.rect.y += self.velocity_y

    def attack(self):
        if not self.is_attacking and self.attack_cooldown <= 0:
            self.is_attacking = True
            self.attack_anim.current_frame = 0
            self.attack_anim.done = False
            self.attack_cooldown = 30  # Cooldown 30 frame

    def update(self, dt):
        # Update animasi
        if self.is_attacking:
            self.current_animation = self.attack_anim
            self.attack_anim.update(dt)
            if self.attack_anim.done:
                self.is_attacking = False
        elif self.velocity_y != 0 or not self.on_ground:
            self.current_animation = self.idle_anim
        else:
            if self.current_animation != self.walk_anim:
                self.current_animation = self.walk_anim
            self.walk_anim.update(dt)
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def draw(self, screen, camera_rect, zoom):
        # Dapatkan frame animasi saat ini
        frame = self.current_animation.get_current_frame()
        
        # Flip gambar jika menghadap kiri
        if self.facing == "left":
            current_frame = pygame.transform.flip(frame, True, False)  # Corrected variable from current_frame to frame
        else:
            current_frame = frame  # Use original frame if facing right
        
        # Skalakan gambar sesuai zoom
        scaled_width = int(self.rect.width * zoom)
        scaled_height = int(self.rect.height * zoom)
        scaled_img = pygame.transform.scale(current_frame, (scaled_width, scaled_height))  # Use current_frame here
        
        # Hitung posisi render
        screen_x = int((self.rect.x - camera_rect.x) * zoom)
        screen_y = int((self.rect.y - camera_rect.y) * zoom)
        
        # Gambar ke layar
        screen.blit(scaled_img, (screen_x, screen_y))

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.die()

    def die(self):
        self.alive = False
        print("Player has died!")
