# character.py
import pygame
from gameobject import Animation

class Player:
    def __init__(self, x, y, width, height):
        self.alive = True
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = 200 # Pixels per second

        self.default_jump_power = -15 # The normal jump power
        self.jump_power = self.default_jump_power # Current jump power, can be modified
        self.original_jump_power = self.default_jump_power # Store the initial jump_power for resetting

        self.jump_power = -13 # Keep as instantaneous velocity change
        self.velocity_y = 0
        self.on_ground = False
        self.health = 100
        self.max_health = 3
        self.facing = "right"
        self.is_attacking = False
        self.attack_cooldown_max = 0.5 # Seconds for cooldown
        self.attack_cooldown_timer = 0
        self.load_animations()
        self.current_animation = self.idle_anim

        # --- Healing Mechanics ---
        self.time_since_last_damage = 0.0  # Time since the player last took damage
        self.heal_after_no_damage_duration = 10.0  # Seconds before healing starts
        self.heal_interval = 1.0  # Heal 1 HP every X seconds once healing starts
        self.time_accumulated_for_heal_tick = 0.0 # Accumulator for heal ticks

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
        """
        Handles player's horizontal movement based on input.
        Allows movement even when attacking.
        Updates player's facing direction.
        Animation is handled in the update() method.
        """
        actual_dx = dx_normalized * self.speed * dt_seconds
        self.rect.x += actual_dx

        if dx_normalized > 0:
            self.facing = "right"
        elif dx_normalized < 0:
            self.facing = "left"
        # If dx_normalized is 0, facing remains unchanged.
        # Animation (idle/walk) will be determined in the update() method based on movement and state.

    def jump(self):
        if self.on_ground:
            self.velocity_y = self.jump_power
            self.on_ground = False # Will be corrected by collision if immediately lands

    def apply_gravity(self, gravity_accel=30, max_fall_speed=20):
        self.velocity_y += gravity_accel * (1.0/60.0) # Assuming dt for physics is ~1/60 for now.
        if self.velocity_y > max_fall_speed:
            self.velocity_y = max_fall_speed
        self.rect.y += self.velocity_y

    def attack(self):
        """Initiates an attack if not already attacking and cooldown allows."""
        if not self.is_attacking and self.attack_cooldown_timer <= 0:
            self.is_attacking = True
            self.current_animation = self.attack_anim # Immediately switch to attack animation
            self.attack_anim.reset()
            self.attack_cooldown_timer = self.attack_cooldown_max

    def get_attack_rect(self):
        """
        Returns the hitbox for the attack if the attack is active and on a damaging frame.
        Returns None otherwise.
        """
        # Only return a rect if attacking and on a frame that should deal damage
        # Example: damage on frame index 1 (second frame) of the attack animation
        if not self.is_attacking or self.attack_anim.current_frame_index < 1 : # or some other condition like specific frames
            return None

        attack_width = self.rect.width + 20
        attack_height = self.rect.height
        if self.facing == "right":
            return pygame.Rect(self.rect.right, self.rect.top, attack_width, attack_height)
        else: # facing left
            return pygame.Rect(self.rect.left - attack_width, self.rect.top, attack_width, attack_height)

    def update(self, dt_seconds, enemies_list):
        """
        Updates player state, animations, attack logic, and healing.
        """
        # Cooldown timer
        if self.attack_cooldown_timer > 0:
            self.attack_cooldown_timer -= dt_seconds

        # Attack Logic
        if self.is_attacking:
            self.current_animation = self.attack_anim # Ensure attack animation is playing
            self.attack_anim.update(dt_seconds)
            if self.attack_anim.done:
                self.is_attacking = False
                # Attack finished, animation will be re-evaluated below based on current movement

            # Deal damage during active attack frames
            attack_rect = self.get_attack_rect()
            if attack_rect:
                # Example: Damage on frame 1 (0-indexed). Could be specific frames.
                # To prevent hitting multiple times with one swing on the same enemy,
                # you might need a list of enemies already hit in this current swing.
                # For simplicity, this hits on frame 1.
                if self.attack_anim.current_frame_index == 1: # Or other specific damage frames
                    for enemy_instance in enemies_list:
                        if enemy_instance.alive and attack_rect.colliderect(enemy_instance.rect):
                            enemy_instance.take_damage(1) # Player damage = 1
                            # To hit only one enemy per swing or per frame, add more logic here

        # Animation selection (if not attacking, or if attack just finished)
        if not self.is_attacking:
            # Check current movement input to decide between idle and walk
            # This requires getting key state, which is usually done in the game loop's input handling.
            # For now, we assume that if player.move was called with non-zero dx, they are "trying to move".
            # A more robust way is to check pygame.key.get_pressed() here.
            keys = pygame.key.get_pressed() # Get current key state for accurate animation
            is_moving_input = keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]

            if not self.on_ground:
                self.current_animation = self.idle_anim # Or a dedicated jump/fall animation
            elif is_moving_input: # Player is pressing left/right
                self.current_animation = self.walk_anim
            else: # Player is on ground and not pressing left/right
                self.current_animation = self.idle_anim

        # Always update the chosen current animation
        if self.current_animation:
            self.current_animation.update(dt_seconds)

        # --- Healing Logic ---
        if self.alive and self.health < self.max_health:
            self.time_since_last_damage += dt_seconds
            if self.time_since_last_damage >= self.heal_after_no_damage_duration:
                self.time_accumulated_for_heal_tick += dt_seconds
                if self.time_accumulated_for_heal_tick >= self.heal_interval:
                    self.health += 1
                    self.health = min(self.health, self.max_health)
                    self.time_accumulated_for_heal_tick -= self.heal_interval


    def draw(self, screen, camera_rect, zoom):
        if not self.alive: return

        frame_to_draw = self.current_animation.get_current_frame()
        if not frame_to_draw:
            # Fallback rectangle if no frame (should ideally not happen)
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
        if scaled_width <=0 or scaled_height <=0: return # Avoid scaling to zero or negative

        scaled_img = pygame.transform.scale(display_frame, (scaled_width, scaled_height))

        screen_x = int((self.rect.x - camera_rect.x) * zoom)
        screen_y = int((self.rect.y - camera_rect.y) * zoom)

        screen.blit(scaled_img, (screen_x, screen_y))

    def take_damage(self, damage):
        if not self.alive: return

        self.health -= damage
        self.time_since_last_damage = 0.0
        self.time_accumulated_for_heal_tick = 0.0 # Reset healing accumulator on damage

        if self.health <= 0:
            self.health = 0
            self.die()

    def die(self):
        self.alive = False
        print("Player has died!")
        # Additional death logic can be added here, like respawning or game over screen.
