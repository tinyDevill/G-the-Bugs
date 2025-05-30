# npc.py
import pygame
import random # For Witcher's random jumps
from gameobject import Animation, Projectile # Import Projectile

# --- DIALOGS ---
truth_seeker_dialogs = {
    "intro": ["you...", "you have the void in your soul...", "so... finally...", ".. the destiny will be fulfilled."],
    "quest_offer": ["bring me the void heart from the deepest cave...", "only then can the seal be broken."],
    "waiting_for_heart": ["the void heart... have you found it?"],
    "has_heart": ["Ah, the void heart! Give it here... quickly!"],
    "outro": ["It is done... the path is clear... but at what cost?"]
}
steelsoul_dialogs = {
    "default": ["hey, whatchu doing here?", "wow, you have a cool sword?", "so, you just walking and slay that empty life corpse, right?","they once life. doing their job and so cheerful. but, after that black goo arrived from nowhere. i wonder, where it come from?"],
    "dialog2": ["this area is full of silent. but, i like it.", "this is so peacefully."]
}
noze_dialogs = {
    "initial_offer": [
        "oh. you're so tiny, mwehehehe...",
        "this, take it. mwehehe..."
    ],
    "item_accepted_followup": ["mwhehehe... you'll like it."],
    "item_declined_followup": ["nyeh. you waste my kindness."]
}
lost_knight_dialogs = {"default": ["Lost... so lost... was there ever a purpose?"]}
hornhead_dialogs = {
    "first_encounter": [
        "why are you here?",
        "you must run, save your life. that crazy bug is doing something non sense. he sacrifice so much soul just so he can reach immortality. but, in the end? he became crazy bug instead. the void make his mind is empty. everything he thought is just to guard the void source from anyone."
    ],
    "subsequent_talk": [
        "bah... i'm not strong bug. if you still won't run, i'll leave you. i told you after all."
    ]
}
witcher_dialogs = { 
    "introduction": ["They call me Witcher. I hunt more than just beasts.", "These ruins whisper tales of forgotten magic."],
    "quest_hint": ["Something ancient stirs here. Its power could be yours... or your undoing."],
    "warning": ["Tread carefully. Not all that is dead stays buried."]
}

class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name, base_dialogs, image_surface=None):
        super().__init__()
        self.name = name
        self.rect = pygame.Rect(x, y, width, height)
        self.base_dialogs = base_dialogs 
        
        self.image_surface_original = image_surface # Store original for Witcher
        if image_surface:
            self.image = pygame.transform.scale(image_surface, (width, height))
        else:
            self.image = pygame.Surface((width, height))
            if name == "noze": 
                self.image.fill((200, 150, 250)) 
            elif name == "hornhead": 
                self.image.fill((180, 100, 80)) 
            else:
                self.image.fill((180, 180, 180)) 

        self.active = True 
        self.current_dialog_key = "default"

    def interact(self, player_data, story_flags_from_game):
        current_dialog_lines = ["..."] 
        self.current_dialog_key = "fallback"

        if self.name == "truth_seeker":
            # ... (truth_seeker dialog logic remains the same)
            if not story_flags_from_game.get("truth_seeker_initial_talk_done"):
                current_dialog_lines = self.base_dialogs.get("intro", ["Intro missing."])
                self.current_dialog_key = "intro" 
            elif not story_flags_from_game.get("truth_seeker_quest_accepted"):
                current_dialog_lines = self.base_dialogs.get("quest_offer", ["Quest offer missing."])
                self.current_dialog_key = "quest_offer"
            elif not story_flags_from_game.get("void_heart_obtained"): 
                current_dialog_lines = self.base_dialogs.get("waiting_for_heart", ["Waiting missing."])
                self.current_dialog_key = "waiting_for_heart"
            elif story_flags_from_game.get("void_heart_obtained"):
                current_dialog_lines = self.base_dialogs.get("has_heart", ["Has heart dialog missing."])
                self.current_dialog_key = "has_heart" 
            else:
                current_dialog_lines = self.base_dialogs.get("outro", ["Outro missing."])
                self.current_dialog_key = "outro"
        elif self.name == "steelsoul":
            # ... (steelsoul dialog logic remains the same)
            if story_flags_from_game.get("steelsoul_met_before", False): 
                current_dialog_lines = self.base_dialogs.get("dialog2", ["Steelsoul speaks again."])
                self.current_dialog_key = "dialog2"
            else:
                current_dialog_lines = self.base_dialogs.get("default", ["Steelsoul speaks."])
                self.current_dialog_key = "default"
        elif self.name == "noze":
            # ... (noze dialog logic remains the same)
            if story_flags_from_game.get("noze_item_accepted"):
                current_dialog_lines = self.base_dialogs.get("item_accepted_followup", ["mwhehehe... you'll like it."])
                self.current_dialog_key = "item_accepted_followup"
            elif story_flags_from_game.get("noze_item_declined"):
                current_dialog_lines = self.base_dialogs.get("item_declined_followup", ["nyeh. you waste my kindness."])
                self.current_dialog_key = "item_declined_followup"
            else:
                current_dialog_lines = self.base_dialogs.get("initial_offer", ["oh. you're so tiny, mwehehehe...", "this, take it. mwehehe..."])
                self.current_dialog_key = "initial_offer"
        elif self.name == "lost_knight":
            # ... (lost_knight dialog logic remains the same)
            current_dialog_lines = self.base_dialogs.get("default", ["Lost Knight sighs."])
            self.current_dialog_key = "default"
        elif self.name == "hornhead":
            # ... (hornhead dialog logic remains the same)
            if story_flags_from_game.get("hornhead_first_talk_done"):
                current_dialog_lines = self.base_dialogs.get("subsequent_talk", ["bah... i'm not strong bug. if you still won't run, i'll leave you. i told you after all."])
                self.current_dialog_key = "subsequent_talk"
            else:
                current_dialog_lines = self.base_dialogs.get("first_encounter", ["why are you here?", "you must run..."])
                self.current_dialog_key = "first_encounter"
        elif self.name == "witcher": # Witcher specific dialog logic (can be expanded)
            if story_flags_from_game.get("witcher_quest_hint_received"):
                current_dialog_lines = self.base_dialogs.get("warning", ["Be wary."])
                self.current_dialog_key = "warning"
            else:
                current_dialog_lines = self.base_dialogs.get("introduction", ["Witcher introduction."])
                self.current_dialog_key = "introduction"
        else: 
            current_dialog_lines = self.base_dialogs.get("default", [f"{self.name} has nothing to say."])
            self.current_dialog_key = "default"

        return {'dialog': current_dialog_lines, 'dialog_key_spoken': self.current_dialog_key}

    def draw(self, screen, camera_rect, zoom): # This method is now used by both NPC and WitcherNPC
        if not self.active or not self.image: 
            return
        
        # If self.image is dynamically changed by an animation, it will be reflected here
        current_image_to_draw = self.image 

        scaled_width = int(self.rect.width * zoom)
        scaled_height = int(self.rect.height * zoom)
        if scaled_width <= 0 or scaled_height <= 0: return

        # Check for facing if the NPC has this attribute (Witcher will)
        if hasattr(self, 'facing') and self.facing == "left":
             current_image_to_draw = pygame.transform.flip(current_image_to_draw, True, False)

        scaled_img = pygame.transform.scale(current_image_to_draw, (scaled_width, scaled_height))
        screen_x = int((self.rect.x - camera_rect.x) * zoom)
        screen_y = int((self.rect.y - camera_rect.y) * zoom)
        screen.blit(scaled_img, (screen_x, screen_y))

# --- NEW WITCHER NPC CLASS ---
class WitcherNPC(NPC):
    def __init__(self, x, y, width, height, name, base_dialogs, image_surface, witcher_image2, bullet_image_asset, game_ref):
        super().__init__(x, y, width, height, name, base_dialogs, image_surface)
        
        self.game_ref = game_ref # Reference to the main game object to add projectiles
        self.original_y = y # To return after jump
        self.witcher_frame1 = image_surface # Already scaled by NPC init, but we might want originals
        self.witcher_frame2 = witcher_image2
        self.bullet_image = bullet_image_asset

        # Animation for jumping
        # Scale frames to NPC's dimensions
        scaled_frame1 = pygame.transform.scale(self.witcher_frame1, (width, height))
        scaled_frame2 = pygame.transform.scale(self.witcher_frame2, (width, height))
        self.jump_anim = Animation([scaled_frame1, scaled_frame2], frame_duration_seconds=0.3, loop=True)
        self.idle_image = scaled_frame1 # Default image
        self.image = self.idle_image # Set initial image for drawing

        # Jump mechanics
        self.is_jumping = False
        self.velocity_y = 0
        self.jump_power = -10 # How high the Witcher jumps
        self.gravity = 0.5 # Simple gravity for Witcher
        self.jump_interval_min = 3.0 # Min seconds between jumps
        self.jump_interval_max = 7.0 # Max seconds
        self.time_to_next_jump = random.uniform(self.jump_interval_min, self.jump_interval_max)
        self.time_since_last_jump_check = 0

        # Projectile mechanics
        self.projectile_range = 250 # Increased range
        self.projectile_damage = 1
        self.projectile_speed = 250
        self.projectile_cooldown = 2.0 # Seconds
        self.time_since_last_shot = self.projectile_cooldown # Can shoot immediately

        self.facing = "right" # or "left"

    def update_behavior(self, dt_seconds, player_rect, platforms): # platforms might be needed for landing
        self.time_since_last_jump_check += dt_seconds
        self.time_since_last_shot += dt_seconds

        # --- Jumping Logic ---
        if self.is_jumping:
            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y
            self.image = self.jump_anim.get_current_frame() # Update image from jump animation
            self.jump_anim.update(dt_seconds)

            # Simple landing: if returned to original y or below
            if self.rect.y >= self.original_y:
                self.rect.y = self.original_y
                self.is_jumping = False
                self.velocity_y = 0
                self.image = self.idle_image # Back to idle image
                self.time_to_next_jump = random.uniform(self.jump_interval_min, self.jump_interval_max)
                self.time_since_last_jump_check = 0
        else: # Not currently jumping, check if should jump
            if self.time_since_last_jump_check >= self.time_to_next_jump:
                self.is_jumping = True
                self.velocity_y = self.jump_power
                self.jump_anim.reset()
        
        # --- Look at Player ---
        if player_rect.centerx < self.rect.centerx:
            self.facing = "left"
        else:
            self.facing = "right"

        # --- Projectile Logic ---
        distance_to_player_x = abs(player_rect.centerx - self.rect.centerx)
        distance_to_player_y = abs(player_rect.centery - self.rect.centery) # For vertical alignment

        if distance_to_player_x < self.projectile_range and \
           distance_to_player_y < self.rect.height * 2 and \
           self.time_since_last_shot >= self.projectile_cooldown:
            
            self.time_since_last_shot = 0
            
            # Calculate direction vector
            dx = player_rect.centerx - self.rect.centerx
            dy = player_rect.centery - self.rect.centery
            magnitude = (dx**2 + dy**2)**0.5
            
            proj_vel_x = 0
            proj_vel_y = 0
            if magnitude > 0:
                proj_vel_x = (dx / magnitude) * self.projectile_speed
                proj_vel_y = (dy / magnitude) * self.projectile_speed

            # Spawn projectile (adjust spawn position based on Witcher size/facing)
            bullet_w, bullet_h = 10, 10 # Or get from bullet_image.get_size()
            spawn_x = self.rect.centerx
            if self.facing == "right":
                spawn_x = self.rect.right
            else:
                spawn_x = self.rect.left - bullet_w
            
            new_projectile = Projectile(spawn_x, self.rect.centery - bullet_h / 2,
                                        bullet_w, bullet_h,
                                        self.bullet_image,
                                        proj_vel_x, proj_vel_y, self.projectile_damage)
            self.game_ref.projectiles.append(new_projectile) # Add to game's list
