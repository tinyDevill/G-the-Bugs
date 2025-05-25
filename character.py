# character.py
import pygame
from gameobject import Animation 

class Player:
    def __init__(self, x, y, width, height):
        self.alive = True
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = 200 # Pixels per second
        self.jump_power = -15 # Keep as instantaneous velocity change
        self.velocity_y = 0
        self.on_ground = False
        self.health = 3
        self.max_health = 3
        self.facing = "right"
        self.is_attacking = False
        self.attack_cooldown_max = 0.5 # Seconds for cooldown
        self.attack_cooldown_timer = 0 
        self.load_animations()
        self.current_animation = self.idle_anim

    def load_animations(self):
        try:
            idle_img = pygame.image.load("assets/image/player_idle.png").convert_alpha()
            walk1 = pygame.image.load("assets/image/walk1.png").convert_alpha()
            walk2 = pygame.image.load("assets/image/walk2.png").convert_alpha()
            att1 = pygame.image.load("assets/image/att1.png").convert_alpha()
            att2 = pygame.image.load("assets/image/att2.png").convert_alpha()
            att3 = pygame.image.load("assets/image/att3.png").convert_alpha()
            
            self.idle_anim = Animation([idle_img], 0.2)
            self.walk_anim = Animation([walk1, walk2], 0.1)
            self.attack_anim = Animation([att1, att2, att3], 0.07, loop=False) # Faster attack
        except pygame.error as e:
            print(f"Error loading player animation images: {e}")
            # Fallback animations with placeholder surfaces
            placeholder = pygame.Surface((self.rect.width, self.rect.height)); placeholder.fill((0,255,0))
            self.idle_anim = Animation([placeholder], 1)
            self.walk_anim = Animation([placeholder], 1)
            self.attack_anim = Animation([placeholder], 1, loop=False)
            
    def move(self, dx_normalized, dt_seconds): # dx_normalized is -1, 0, or 1
        if not self.is_attacking:
            actual_dx = dx_normalized * self.speed * dt_seconds
            self.rect.x += actual_dx
            if dx_normalized > 0:
                self.facing = "right"
                if self.on_ground and not self.is_attacking: self.current_animation = self.walk_anim
            elif dx_normalized < 0:
                self.facing = "left"
                if self.on_ground and not self.is_attacking: self.current_animation = self.walk_anim
            # If dx_normalized is 0, idle animation will be set in update if on ground

    def jump(self):
        if self.on_ground:
            self.velocity_y = self.jump_power
            self.on_ground = False # Will be corrected by collision if immediately lands

    def apply_gravity(self, gravity_accel=30, max_fall_speed=20): # gravity_accel in units/sec^2
        # Convert gravity to change per frame: dv = a * dt
        self.velocity_y += gravity_accel * (1.0/60.0) # Assuming dt for physics is ~1/60 for now.
                                                     # Better: pass actual dt_seconds if physics vary
        if self.velocity_y > max_fall_speed: 
            self.velocity_y = max_fall_speed
        self.rect.y += self.velocity_y # Simple Euler integration for position

    def attack(self):
        if not self.is_attacking and self.attack_cooldown_timer <= 0:
            self.is_attacking = True
            self.current_animation = self.attack_anim
            self.attack_anim.reset()
            self.attack_cooldown_timer = self.attack_cooldown_max 

    def get_attack_rect(self):
        if not self.is_attacking or self.attack_anim.current_frame_index < 1: # Damage on 2nd+ frame
            return None
        # Attack hitbox slightly larger and in front
        attack_width = self.rect.width + 20 
        attack_height = self.rect.height 
        if self.facing == "right":
            return pygame.Rect(self.rect.right, self.rect.top, attack_width, attack_height)
        else: # facing left
            return pygame.Rect(self.rect.left - attack_width, self.rect.top, attack_width, attack_height)

    def update(self, dt_seconds, enemies_list): # Takes a list of enemies
        # Cooldown timer
        if self.attack_cooldown_timer > 0:
            self.attack_cooldown_timer -= dt_seconds

        # Animation and Attack Logic
        if self.is_attacking:
            self.current_animation = self.attack_anim # Ensure it's set
            self.attack_anim.update(dt_seconds)
            if self.attack_anim.done:
                self.is_attacking = False
                # self.current_animation = self.idle_anim # Set based on movement below
            
            # Deal damage
            attack_rect = self.get_attack_rect()
            if attack_rect: # Check if attack is active and rect is valid
                # This simple version hits all enemies in rect on specific frames.
                # For more advanced, add a list to player: self.hit_this_swing = []
                # Clear it on attack_anim.reset(). Add enemy to it when hit.
                if self.attack_anim.current_frame_index == 1: # Example: damage dealt on frame 1 (0-indexed)
                    for enemy_instance in enemies_list:
                        if enemy_instance.alive and attack_rect.colliderect(enemy_instance.rect):
                            enemy_instance.take_damage(1) # Player damage = 1
                            # print(f"Player hit enemy {id(enemy_instance)}")
                            # To hit only one enemy: break 
        
        # Set animation based on state (if not attacking)
        if not self.is_attacking:
            keys = pygame.key.get_pressed() # Simple way to check if moving for animation
            is_moving_for_anim = keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]

            if not self.on_ground: # Jumping/Falling
                 self.current_animation = self.idle_anim # Or a dedicated jump/fall animation
            elif is_moving_for_anim:
                 self.current_animation = self.walk_anim
            else: # Idle on ground
                 self.current_animation = self.idle_anim
        
        # Always update the current animation (unless it's a non-looping one that's done)
        if self.current_animation:
            self.current_animation.update(dt_seconds)


    def draw(self, screen, camera_rect, zoom):
        if not self.alive: return
        
        frame_to_draw = self.current_animation.get_current_frame()
        if not frame_to_draw: # Fallback if animation somehow has no frame
            pygame.draw.rect(screen, (0,255,0), 
                             ((self.rect.x - camera_rect.x) * zoom,
                              (self.rect.y - camera_rect.y) * zoom,
                              self.rect.width * zoom, self.rect.height * zoom))
            return
            
        display_frame = frame_to_draw
        if self.facing == "left":
            display_frame = pygame.transform.flip(frame_to_draw, True, False)
        
        scaled_width = int(self.rect.width * zoom)
        scaled_height = int(self.rect.height * zoom)
        if scaled_width <=0 or scaled_height <=0: return

        scaled_img = pygame.transform.scale(display_frame, (scaled_width, scaled_height))
        
        screen_x = int((self.rect.x - camera_rect.x) * zoom)
        screen_y = int((self.rect.y - camera_rect.y) * zoom)
        
        screen.blit(scaled_img, (screen_x, screen_y))

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.die()

    def die(self):
        self.alive = False
        print("Player has died!")
