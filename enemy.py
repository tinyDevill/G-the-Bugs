# enemy.py
import pygame
from gameobject import Animation, GameObject 

class Enemy(GameObject):
    def __init__(self, x, y, width, height, animation_images_dict, attack_range=50, damage=1,enemy_uid=None): # Takes dict of images
        super().__init__(x, y, width, height)
        self.uid = enemy_uid # ADDED: Store the unique ID
        self.initial_x = x # Store initial position for potential dynamic ID generation fallback
        self.initial_y = y
        # self.enemy_type_label = enemy_type_label # Store if using dynamic ID with type

        self.alive = True
        # Adjust speed to pixels per second for time-based movement
        self.speed = 80 # e.g., 80 pixels per second for patrol
        self.attack_range = attack_range 
        self.damage = damage
        self.direction = 1 
        self.health = 3 
        self.max_health = 3
        self.is_attacking = False
        self.facing = "left" 
        
        self.velocity_y = 0
        self.on_ground = False
        self.attack_cooldown_time = 2.0 
        self.last_attack_time = 0 
        
        self.animation_images = animation_images_dict # Store the passed image dictionary
        self.load_animations() # Call load_animations which now uses self.animation_images
        self.current_animation = self.idle_anim 
        
        self.patrol_start_x = x
        self.patrol_distance = 100 
        self.patrol_bounds = (self.patrol_start_x - self.patrol_distance, self.patrol_start_x + self.patrol_distance)

    def load_animations(self):
        # Uses self.animation_images which should be populated before calling this
        if not self.animation_images or not all(k in self.animation_images for k in ['idle', 'walk1', 'walk2', 'attack1', 'attack2', 'attack3']):
            print(f"Error: Enemy animation images missing for {self.rect}. Using placeholders.")
            placeholder = pygame.Surface((self.rect.width, self.rect.height)); placeholder.fill((255,0,0))
            self.idle_anim = Animation([placeholder], 1)
            self.walk_anim = Animation([placeholder, placeholder], 1)
            self.attack_anim = Animation([placeholder]*3, 1, loop=False)
            return

        self.idle_anim = Animation([self.animation_images['idle']], 0.5)
        self.walk_anim = Animation([self.animation_images['walk1'], self.animation_images['walk2']], 0.2)
        self.attack_anim = Animation([self.animation_images['attack1'], 
                                      self.animation_images['attack2'], 
                                      self.animation_images['attack3']], 0.1, loop=False)

    def take_damage(self, damage_amount):
        self.health -= damage_amount
        if self.health <= 0:
            self.health = 0
            self.die()

    def die(self):
        self.alive = False
        self.current_animation = self.idle_anim # Or a death animation

    def patrol(self, dt_seconds):
        if self.is_attacking: return

        self.rect.x += self.speed * self.direction * dt_seconds # Time-based movement

        # Patrol boundary collision
        if self.direction == 1 and self.rect.right >= self.patrol_bounds[1]:
            self.direction = -1
            self.facing = "left"
        elif self.direction == -1 and self.rect.left <= self.patrol_bounds[0]:
            self.direction = 1
            self.facing = "right"
        
        if not self.is_attacking: # Only set to walk if not in attack animation
            self.current_animation = self.walk_anim

    def apply_gravity(self, gravity_accel=30, max_fall_speed=15): # Similar to player
        if not self.on_ground:
            self.velocity_y += gravity_accel * (1.0/60.0) # Approx for now, pass dt if physics step varies
            if self.velocity_y > max_fall_speed:
                self.velocity_y = max_fall_speed
            self.rect.y += self.velocity_y

    def check_vertical_collision(self, platforms): # Renamed for consistency if user prefers
        self.on_ground = False 
        for platform in platforms:
            if platform.is_wall: continue
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0: 
                    previous_rect_bottom = self.rect.bottom - self.velocity_y
                    if previous_rect_bottom <= platform.rect.top + 1 and self.rect.bottom >= platform.rect.top:
                        self.rect.bottom = platform.rect.top
                        self.velocity_y = 0
                        self.on_ground = True
                elif self.velocity_y < 0: 
                    previous_rect_top = self.rect.top - self.velocity_y 
                    if previous_rect_top >= platform.rect.bottom - 1 and self.rect.top <= platform.rect.bottom:
                        self.rect.top = platform.rect.bottom
                        self.velocity_y = 0
    
    def check_horizontal_collision(self, platforms, original_x):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                overlap_y = max(0, min(self.rect.bottom, platform.rect.bottom) - max(self.rect.top, platform.rect.top))
                if overlap_y > self.rect.height / 4: 
                    if self.rect.x < original_x: # Moved left
                        self.rect.left = platform.rect.right
                        if self.direction == -1 : # If was moving into it, turn
                            self.direction = 1
                            self.facing = "right"
                    elif self.rect.x > original_x: # Moved right
                        self.rect.right = platform.rect.left
                        if self.direction == 1: # If was moving into it, turn
                            self.direction = -1
                            self.facing = "left"

    def can_attack(self, current_game_time_seconds):
        return current_game_time_seconds - self.last_attack_time >= self.attack_cooldown_time

    def start_attack(self, current_game_time_seconds):
        self.is_attacking = True
        self.current_animation = self.attack_anim
        self.attack_anim.reset()
        self.last_attack_time = current_game_time_seconds

    def update(self, dt_seconds, player_rect, platforms, current_game_time_seconds):
        if not self.alive: return 0 
        
        damage_dealt_this_frame = 0
        original_x = self.rect.x

        # Determine facing based on player IF not attacking AND player is close enough to be a threat/target
        # Otherwise, patrol direction dictates facing.
        distance_to_player = abs(self.rect.centerx - player_rect.centerx)
        vertical_distance = abs(self.rect.centery - player_rect.centery) # For Y-axis consideration

        if not self.is_attacking:
            if distance_to_player < self.attack_range * 2 : # If player is somewhat close, face them
                if player_rect.centerx < self.rect.centerx: self.facing = "left"
                else: self.facing = "right"
            # else: facing is determined by patrol direction

        if self.is_attacking:
            self.current_animation = self.attack_anim # Ensure it's set
            # self.attack_anim.update(dt_seconds) # Animation update is done at the end
            if self.attack_anim.done:
                self.is_attacking = False
        else: 
            if distance_to_player < self.attack_range and vertical_distance < self.rect.height and self.can_attack(current_game_time_seconds):
                # Face player before attacking
                if player_rect.centerx < self.rect.centerx: self.facing = "left"
                else: self.facing = "right"
                self.start_attack(current_game_time_seconds)
                
                # Simplified attack hitbox logic from your code
                attack_hitbox_width = self.rect.width + 20 
                attack_hitbox_height = self.rect.height
                if self.facing == "right": # Attack in facing direction
                    eff_attack_rect = pygame.Rect(self.rect.centerx, self.rect.top, attack_hitbox_width, attack_hitbox_height)
                else:
                    eff_attack_rect = pygame.Rect(self.rect.centerx - attack_hitbox_width, self.rect.top, attack_hitbox_width, attack_hitbox_height)
                
                if eff_attack_rect.colliderect(player_rect):
                    damage_dealt_this_frame = self.damage
            else: 
                self.patrol(dt_seconds) # This updates self.rect.x and potentially self.facing/self.direction

        self.check_horizontal_collision(platforms, original_x)
        
        self.apply_gravity() # apply_gravity updates self.rect.y
        self.check_vertical_collision(platforms)
        
        # Final animation selection based on state
        if self.is_attacking:
            self.current_animation = self.attack_anim
        elif not self.on_ground:
            self.current_animation = self.idle_anim # Or jump/fall animation
        elif self.current_animation == self.walk_anim : # If patrol set it
             pass # keep walk_anim
        else: # Default to idle if on ground and not walking/attacking
            self.current_animation = self.idle_anim
            
        if self.current_animation: # Ensure it's not None
            self.current_animation.update(dt_seconds)

        return damage_dealt_this_frame

    def draw(self, screen, camera_rect, zoom):
        if not self.alive and not (self.is_attacking and self.current_animation and not self.current_animation.done):
            return

        if not self.current_animation: return # Safety check
        frame = self.current_animation.get_current_frame()
        if not frame: return # Further safety

        current_display_frame = frame
        if self.facing == "left":
            current_display_frame = pygame.transform.flip(frame, True, False)
        
        scaled_width = int(self.rect.width * zoom)
        scaled_height = int(self.rect.height * zoom)
        if scaled_width <=0 or scaled_height <=0: return

        scaled_img = pygame.transform.scale(current_display_frame, (scaled_width, scaled_height))
        screen_x = int((self.rect.x - camera_rect.x) * zoom)
        screen_y = int((self.rect.y - camera_rect.y) * zoom)
        screen.blit(scaled_img, (screen_x, screen_y))
