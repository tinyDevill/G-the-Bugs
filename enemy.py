import pygame
from animation import Animation
from gameobject import GameObject  # Make sure this path matches your project structure

class Enemy(GameObject):
    def __init__(self, x, y, width, height, images, attack_range=50, damage=1):
        super().__init__(x, y, width, height)
        self.alive = True  # Tambah status hidup
        self.speed = 2
        self.attack_range = attack_range  # Tambahkan ini
        self.damage = damage  # Tambahkan ini
        self.direction = 1
        self.health = 1
        self.is_attacking = False
        self.facing = "left"
        self.current_animation = None
        self.velocity_y = 0
        self.on_ground = False
        self.attack_cooldown = 1000
        self.last_attack_time = 0
        
        self.load_animations(images)
        self.current_animation = self.idle_anim
        self.patrol_bounds = (x-100, x+100)

    def load_animations(self, images):
        self.idle_anim = Animation([images['idle']], 200)
        self.walk_anim = Animation([images['walk1'], images['walk2']], 100)
        self.attack_anim = Animation([images['attack1'], images['attack2'], images['attack3']], 50, loop=False)

    def take_damage(self, damage):
        print(f"Enemy taking damage: {damage}")  # Debug print
        self.health -= damage
        print(f"Enemy health after damage: {self.health}")  # Debug print
        if self.health <= 0:
            self.die()

    def die(self):
        print("Enemy is dying!")  # Debug print
        self.alive = False
        print("Enemy died")
       

    def patrol(self):
        self.move()
        # Update patrol bounds berdasarkan posisi awal
        if self.rect.left < self.patrol_bounds[0] or self.rect.right > self.patrol_bounds[1]:
            self.direction *= -1
            self.facing = "right" if self.direction == 1 else "left"

    def move(self):
        if not self.is_attacking:
            self.rect.x += self.speed * self.direction

    def apply_gravity(self, gravity=0.8):
        if not self.on_ground:
            self.velocity_y += gravity
            self.rect.y += self.velocity_y

    def check_platform_collision(self, platforms):
        self.on_ground = False
        for platform in platforms:
            if platform.rect.colliderect(self.rect):
                if self.velocity_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0

    def attack(self, player_rect):
        current_time = pygame.time.get_ticks()
        damage_dealt = 0
        
        if current_time - self.last_attack_time > self.attack_cooldown:
            self.is_attacking = True
            self.current_animation = self.attack_anim
            self.current_animation.reset()  # Now works with the new reset() method
            self.last_attack_time = current_time
            
            attack_rect = self.rect.inflate(30, 10)
            if attack_rect.colliderect(player_rect):
                damage_dealt = self.damage
        
        return damage_dealt

    def update(self, dt, player_rect, platforms):
        if not self.alive:  # Jangan update jika sudah mati
            return 0
        damage_dealt = 0  # Inisialisasi nilai damage
        # Update animasi
        if self.is_attacking:
            self.current_animation.update(dt)
            if self.current_animation.done:
                self.is_attacking = False
                self.current_animation = self.walk_anim
        else:
            if abs(self.rect.centerx - player_rect.centerx) < self.attack_range:
                damage_dealt = self.attack(player_rect)  # Dapatkan nilai damage
            else:
                self.patrol()
                self.current_animation = self.walk_anim
                self.current_animation.update(dt)
        
        self.apply_gravity()
        self.check_platform_collision(platforms)

        return damage_dealt  # Kembalikan nilai damage

    def draw(self, screen, camera_rect, zoom):
        frame = self.current_animation.get_current_frame()
        
        # Flip gambar berdasarkan arah hadap
        if self.facing == "left":
            frame = pygame.transform.flip(frame, True, False)
        
        scaled_img = pygame.transform.scale(
            frame,
            (int(self.rect.width * zoom), int(self.rect.height * zoom))
        )

        screen.blit(
            scaled_img,
            ((self.rect.x - camera_rect.x) * zoom,
            (self.rect.y - camera_rect.y) * zoom)
        )
