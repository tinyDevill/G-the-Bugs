# game.py
import pygame
import sys
import math
import random # If not already imported

# Import WitcherNPC along with NPC
from npc import NPC, WitcherNPC, truth_seeker_dialogs, steelsoul_dialogs, noze_dialogs, hornhead_dialogs, witcher_dialogs
from character import Player
from enemy import Enemy
from gameobject import Platform, Animation, Projectile, create_platforms_for_level # Added Projectile
from screen import (load_assets, Camera, draw_background_scaled_with_camera, draw_objects,
                    draw_darkness_with_light, draw_text)

from scene_config import SCENES_DATA, SCENE_ID_SCENE1, SCENE_ID_SCENE2, SCENE_ID_SCENE3, SCENE_ID_SCENE4, SCENE_ID_SCENE5

class Game:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 1200, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("G The Bugs Draft - Scene Demo")

        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.zoom = 1 
        self.font = pygame.font.Font(None, 36)
        self.dialog_font = pygame.font.Font(None, 28)
        self.interaction_prompt_font = pygame.font.Font(None, 22)

        self.loaded_assets = load_assets(self.WIDTH, self.HEIGHT)

        self.platform_image_assets = {
            'floor1_img': self.loaded_assets.get('floor1_img'),      # From scene 2 def
            'floor2_img': self.loaded_assets.get('floor2_img'),      # From scene 2 def
            'platform_img': self.loaded_assets.get('platform_img'),  # From scene 2 def
            'benchbottom_img': self.loaded_assets.get('benchbottom_img'),
            'benchside2_1_img': self.loaded_assets.get('benchside2_1_img'),
            'benchside2_2_img': self.loaded_assets.get('benchside2_2_img'),
            'wall_img': self.loaded_assets.get('wall_img'),          # From scene 2 def

            # Scene 1
            'floor1_1': self.loaded_assets.get('floor1_1'),
            'floor1_2': self.loaded_assets.get('floor1_2'),
            'floor1_3': self.loaded_assets.get('floor1_3'),
            'floor1_4': self.loaded_assets.get('floor1_4'),
            'wall1': self.loaded_assets.get('wall1'),
            # Scene 3
            'floor3_1': self.loaded_assets.get('floor3_1'),
            'floor3_2': self.loaded_assets.get('floor3_2'),
            'upfloor3_1': self.loaded_assets.get('upfloor3_1'),
            'upfloor3_2': self.loaded_assets.get('upfloor3_2'),
            'upfloor3_3': self.loaded_assets.get('upfloor3_3'),
            'upfloor3_4': self.loaded_assets.get('upfloor3_4'),
            'upfloor3_5': self.loaded_assets.get('upfloor3_5'),
            'upfloor3_6': self.loaded_assets.get('upfloor3_6'),
            'floatfloor3': self.loaded_assets.get('floatfloor3'),
            'wall3': self.loaded_assets.get('wall3'),
            # Scene 4
            'floor4_1': self.loaded_assets.get('floor4_1'),
            'floor4_2': self.loaded_assets.get('floor4_2'),
            'floor4_3': self.loaded_assets.get('floor4_3'),
            'wall4_1': self.loaded_assets.get('wall4_1'),
            'wall4_2': self.loaded_assets.get('wall4_2'),
            # Scene 5
            'floor5_1': self.loaded_assets.get('floor5_1'),
            'floor5_2': self.loaded_assets.get('floor5_2'),
            'wall5_1': self.loaded_assets.get('wall5_1'),
            'wall5_2': self.loaded_assets.get('wall5_2'),
        }
        self.npc_image_assets = {
            'truth_seeker': self.loaded_assets.get('truth_seeker_img'),
            'steelsoul': self.loaded_assets.get('steelsoul_img'),
            'noze_img': self.loaded_assets.get('noze_img'),
            'hornhead_img': self.loaded_assets.get('hornhead_img'),
            'witcher_img': self.loaded_assets.get('witcher_img'), # Base image for Witcher
            # Add witcher2 and bullet if they are treated as NPC assets, or handle separately
            'witcher2_img': self.loaded_assets.get('witcher2_img'),
            'bullet_img': self.loaded_assets.get('bullet_img')
        }
        self.background_image_assets = {
            'main_bg': self.loaded_assets.get('main_bg'), # Fallback or default
            'bg1': self.loaded_assets.get('bg1'), # Scene 1 BG
            'bg3': self.loaded_assets.get('bg3'), # Scene 3 BG
            'bg4': self.loaded_assets.get('bg4'), # Scene 4 BG
            'bg5': self.loaded_assets.get('bg5'), # Scene 5 BG
            'second_bg': self.loaded_assets.get('second_bg'), # Scene 2 BG
        }
        self.all_npc_dialogs = {
            'truth_seeker': truth_seeker_dialogs,
            'steelsoul': steelsoul_dialogs,
            'noze': noze_dialogs,
            'hornhead': hornhead_dialogs,    
            'witcher': witcher_dialogs,    
        }
        self.raw_enemy_images = { # For standard enemies
            'idle': pygame.image.load("assets/image/mob1_1.png").convert_alpha(),
            'walk1': pygame.image.load("assets/image/mob1_1.png").convert_alpha(),
            'walk2': pygame.image.load("assets/image/mob1_2.png").convert_alpha(),
            'attack1': pygame.image.load("assets/image/mob1_1.png").convert_alpha(),
            'attack2': pygame.image.load("assets/image/mob1_2.png").convert_alpha(),
            'attack3': pygame.image.load("assets/image/mob1_2.png").convert_alpha()
        }
        self.start_button_img = self.loaded_assets.get('start_button_img')
        self.exit_button_img = self.loaded_assets.get('exit_button_img')
        self.home_screen_img = self.loaded_assets.get('home_screen')

        self.scenes_data = SCENES_DATA
        self.current_scene_id = None
        self.story_flags = {}

        self.platforms = []
        self.npcs = []
        self.enemies = []
        self.projectiles = [] # NEW list for projectiles

        self.player = Player(0, 0, 40, 50) # Dimensions might need adjustment based on player art
        self.camera = Camera(int(self.WIDTH / self.zoom), int(self.HEIGHT / self.zoom), self.zoom)

        self.state = "menu"
        self.light_angle = 0
        self.player_data = {"geo": 0, "inventory": []}
        self.jump_requested = False
        self.interacting_npc = None
        self.active_dialog = []
        self.current_dialog_line_index = 0
        self.dialog_box_rect = pygame.Rect(50, self.HEIGHT - 110, self.WIDTH - 100, 90)
        self.npc_interaction_candidate = None
        self.dialog_choice_active = False
        self.dialog_choice_prompt_text = ""
        self.dialog_choice_options = []
        self.dialog_choice_selected_index = 0
        self.dialog_choice_callback = None
        self.dialog_choice_rect = pygame.Rect(0, 0, 0, 0)
        self.choice_option_rects = []

        self.reset_game()

    def reset_game(self):
        self.player.health = self.player.max_health
        self.player.alive = True
        self.player.jump_power = self.player.original_jump_power 
        self.player.time_since_last_damage = 0.0
        self.player.time_accumulated_for_heal_tick = 0.0
        self.player_data = {"geo": 0, "inventory": []}
        self.story_flags = {
            "truth_seeker_initial_talk_done": False,
            "truth_seeker_quest_accepted": False,
            "void_heart_obtained": False,
            "noze_item_accepted": False,    
            "noze_item_declined": False,    
            "noze_cursed_jump_active": False,
            "hornhead_first_talk_done": False, 
        }
        self.defeated_enemy_uids = set() 
        self.platforms.clear()
        self.npcs.clear() # Clear NPCs
        self.enemies.clear() # Clear enemies
        self.projectiles.clear() # Clear projectiles
        self.npc_interaction_candidate = None 
        self.dialog_choice_active = False 
        if self.scenes_data:
            self.load_scene(SCENE_ID_SCENE1) # Load the first scene by default
        else:
            print("CRITICAL ERROR: No scenes defined in scenes_data. Cannot start game.")
            pygame.quit()
            sys.exit("No scenes available to load.")

    def load_scene(self, scene_id_to_load):
        scene_config = next((sc for sc in self.scenes_data if sc['id'] == scene_id_to_load), None)

        if not scene_config:
            print(f"CRITICAL Error: Scene with ID '{scene_id_to_load}' not found.")
            # ... (error handling as before)
            if not self.current_scene_id and self.scenes_data:
                print("Attempting to load first defined scene as emergency fallback.")
                scene_config = self.scenes_data[0]
            else:
                pygame.quit()
                sys.exit(f"Failed to load scene: {scene_id_to_load}")


        print(f"Loading scene: {scene_config['id']}")
        self.current_scene_id = scene_config['id']
        # Use scene-specific background key, fallback to a generic one if needed
        self.current_background = self.background_image_assets.get(scene_config.get('background_key'), 
                                                                  self.background_image_assets.get('main_bg'))
        self.current_world_width, self.current_world_height = scene_config.get('world_dimensions', (self.WIDTH * 2, self.HEIGHT)) # Example larger world
        self.player.rect.topleft = scene_config['player_start_pos']
        self.player.velocity_y = 0
        self.player.on_ground = False
        
        self.platforms.clear()
        self.npcs.clear()
        self.enemies.clear()
        self.projectiles.clear() # Clear projectiles on scene load
        self.npc_interaction_candidate = None

        self.platforms = create_platforms_for_level(scene_config.get('platform_definitions', []), self.platform_image_assets)

        npc_default_w, npc_default_h = 50, 70 # Adjust as needed
        for npc_def in scene_config.get('npc_definitions', []):
            required_flag = npc_def.get('appears_if_flag_true')
            if required_flag and not self.story_flags.get(required_flag, False):
                continue
            
            name = npc_def['name']
            dialogs = self.all_npc_dialogs.get(name)
            image = self.npc_image_assets.get(npc_def['image_key'])
            
            if dialogs and image:
                if name == 'witcher': # Special instantiation for Witcher
                    witcher_img2 = self.npc_image_assets.get('witcher2_img')
                    bullet_img = self.npc_image_assets.get('bullet_img')
                    if witcher_img2 and bullet_img:
                        self.npcs.append(WitcherNPC(npc_def['x'], npc_def['y'], 
                                                    npc_def.get('width', npc_default_w), 
                                                    npc_def.get('height', npc_default_h), 
                                                    name, dialogs, image, 
                                                    witcher_img2, bullet_img, self)) # Pass game_ref=self
                    else:
                        print(f"WitcherNPC Load Warning: Missing witcher2_img or bullet_img for {name}")
                else: # Standard NPC
                    self.npcs.append(NPC(npc_def['x'], npc_def['y'], 
                                         npc_def.get('width', npc_default_w), 
                                         npc_def.get('height', npc_default_h), 
                                         name, dialogs, image))
            else:
                print(f"NPC Load Warning: Missing dialogs or image for {name} (key: {npc_def['image_key']})")
        
        # ... (enemy loading remains the same)
        enemy_default_w, enemy_default_h = 60, 60
        for enemy_def in scene_config.get('enemy_definitions', []):
            enemy_uid = enemy_def.get('id') 
            if not enemy_uid: 
                enemy_uid = f"{self.current_scene_id}_enemy_{enemy_def['x']}_{enemy_def['y']}_{enemy_def.get('type', 'unknown')}"
                print(f"Warning: Enemy at ({enemy_def['x']},{enemy_def['y']}) in scene {self.current_scene_id} has no 'id'. Generated: {enemy_uid}")
            if enemy_uid in self.defeated_enemy_uids:
                print(f"Enemy {enemy_uid} already defeated. Not spawning.")
                continue 
            self.enemies.append(Enemy(
                enemy_def['x'], enemy_def['y'], 
                enemy_def.get('width', enemy_default_w), 
                enemy_def.get('height', enemy_default_h), 
                self.raw_enemy_images, 
                attack_range=enemy_def.get('attack_range', 50), 
                damage=enemy_def.get('damage', 1),
                enemy_uid=enemy_uid 
            ))

        self.dialog_choice_active = False 
        self.camera.rect.center = self.player.rect.center # Initial camera position
        self.camera.update(self.player, self.current_world_width, self.current_world_height) # Ensure bounds
        self.light_angle = 0
        self.interacting_npc = None
        self.active_dialog = []
        self.current_dialog_line_index = 0

    def update_npc_interaction_candidate(self):
        """Identifies an NPC the player might interact with."""
        if self.active_dialog or not self.player or not self.player.alive:
            self.npc_interaction_candidate = None
            return

        self.npc_interaction_candidate = None # Reset before checking
        interaction_radius = 60 # How close player needs to be to an NPC
        
        # Find the first NPC in range (can be improved to find the *closest* if needed)
        for npc_instance in self.npcs:
            if npc_instance.active:
                # Simple bounding box proximity check
                dist_x = abs(self.player.rect.centerx - npc_instance.rect.centerx)
                dist_y = abs(self.player.rect.centery - npc_instance.rect.centery)
                
                # Check if player's interaction range (defined by radius around player center)
                # overlaps with NPC's interaction range (defined by radius around NPC center)
                # Or more simply, if their centers are within a certain distance.
                # The current approach is a rectangular area check:
                if dist_x < interaction_radius and dist_y < (npc_instance.rect.height / 2 + interaction_radius / 2) : # Make Y range more forgiving
                    self.npc_interaction_candidate = npc_instance
                    return # Found a candidate, no need to check further for this simple implementation

    def check_scene_location_triggers(self):
        if not self.current_scene_id or not self.player or not self.player.alive: return
        current_scene_cfg = next((sc for sc in self.scenes_data if sc['id'] == self.current_scene_id), None)
        if not current_scene_cfg or not current_scene_cfg.get('transitions'): return

        for transition in current_scene_cfg['transitions']:
            is_location_type = transition.get('type') == 'player_at_location' or \
                               transition.get('type') == 'player_at_location_and_flag'
            if is_location_type:
                trigger_rect = pygame.Rect(transition['rect_coords'])
                conditions_met = False
                if self.player.rect.colliderect(trigger_rect):
                    if transition.get('type') == 'player_at_location_and_flag':
                        flag_name = transition.get('required_story_flag')
                        if flag_name and self.story_flags.get(flag_name, False):
                            conditions_met = True
                        elif not flag_name:
                            conditions_met = True
                        else:
                            conditions_met = False
                    else:
                        conditions_met = True
                else:
                    conditions_met = False

                if conditions_met and transition.get('must_all_enemies_be_slain', False):
                    if self.enemies:
                        conditions_met = False
                
                if conditions_met:
                    target_scene_id = transition['target_scene_id']
                    target_player_pos_override = transition.get('target_player_pos') # GET OVERRIDE POS

                    print(f"Player triggered scene change to: {target_scene_id} via combined conditions.")
                    self.load_scene(target_scene_id)

                    if target_player_pos_override: # APPLY OVERRIDE POS if defined
                        self.player.rect.topleft = target_player_pos_override
                                # Ensure camera updates if player position changes drastically
                        self.camera.update(self.player, self.current_world_width, self.current_world_height) 
                        print(f"Player position set to: {target_player_pos_override} in new scene.")
                    break # Exit loop once a transition is made
    
    def start_interaction(self, npc):
        self.interacting_npc = npc
        interaction_result = npc.interact(self.player_data, self.story_flags)
        self.active_dialog = interaction_result.get('dialog', ["..."])
        self.last_dialog_key_spoken_by_npc = interaction_result.get('dialog_key_spoken', None)
        self.current_dialog_line_index = 0
        self.npc_interaction_candidate = None # Clear candidate once interaction starts

    def advance_dialog(self):
        if not self.active_dialog or not self.interacting_npc:
            self.end_interaction()
            return
        self.current_dialog_line_index += 1
        if self.current_dialog_line_index >= len(self.active_dialog):
            self.handle_npc_dialog_completion()
    def end_interaction(self):
        self.interacting_npc = None
        self.active_dialog = []
        self.current_dialog_line_index = 0
        self.last_dialog_key_spoken_by_npc = None
        # Potentially re-check for interaction candidate if player is still near an NPC
        # self.update_npc_interaction_candidate() # This will be called in the main loop anyway



    def activate_dialog_choice(self, prompt, options, callback_function):
        """Activates the Yes/No choice prompt."""
        self.dialog_choice_active = True
        self.dialog_choice_prompt_text = prompt
        self.dialog_choice_options = options
        self.dialog_choice_selected_index = 0  # Default to the first option ("Yes")
        self.dialog_choice_callback = callback_function

        # Define the visual appearance of the choice box
        # You can customize dimensions and positioning
        font_for_size_check = self.dialog_font # or self.font
        prompt_width, prompt_height = font_for_size_check.size(prompt)
        option_widths = [font_for_size_check.size(opt)[0] for opt in options]
        max_option_width = max(option_widths) if option_widths else 100

        box_width = max(prompt_width, max_option_width) + 60 # Add padding
        box_height = prompt_height + (len(options) * (font_for_size_check.get_height() + 10)) + 60 # Padding and space for options
        
        self.dialog_choice_rect = pygame.Rect(
            (self.WIDTH - box_width) // 2,
            (self.HEIGHT - box_height) // 2 - 30, # Slightly above center
            box_width,
            box_height
        )
        # Clear regular dialog as we are now in a choice prompt
        self.active_dialog = []
        self.current_dialog_line_index = 0


    def handle_noze_item_choice(self, selected_option_index):
        """Callback specific to Noze's item offer choice."""
        chosen_option = self.dialog_choice_options[selected_option_index]

        if chosen_option == "Yes":
            self.story_flags["noze_item_accepted"] = True
            self.story_flags["noze_item_declined"] = False # Ensure other choice is false
            print("Player accepted Noze's item. Jump power modified!")
            self.player.jump_power = -50  # Set very high jump power
            self.story_flags["noze_cursed_jump_active"] = True # Activate the curse for the next landing
            # You might add an item to inventory here if you wish:
            # self.player_data["inventory"].append("Noze's 'Gift'")
        else: # "No"
            self.story_flags["noze_item_declined"] = True
            self.story_flags["noze_item_accepted"] = False # Ensure other choice is false
            print("Player declined Noze's item.")
        
        self.dialog_choice_active = False # Deactivate the choice prompt
        self.end_interaction() # End the overall interaction with Noze


    def draw_dialog_choice_prompt(self):
        """Draws the Yes/No prompt box and options on the screen."""
        if not self.dialog_choice_active:
            return

        # 1. Draw background box (semi-transparent)
        overlay_surface = pygame.Surface(self.dialog_choice_rect.size, pygame.SRCALPHA)
        overlay_surface.fill((20, 20, 20, 210)) # Dark, semi-transparent
        self.screen.blit(overlay_surface, self.dialog_choice_rect.topleft)
        pygame.draw.rect(self.screen, (150, 150, 150), self.dialog_choice_rect, 2, border_radius=3) # Border

        # 2. Draw prompt text
        prompt_surface = self.dialog_font.render(self.dialog_choice_prompt_text, True, (230, 230, 230))
        prompt_pos_x = self.dialog_choice_rect.centerx - prompt_surface.get_width() // 2
        prompt_pos_y = self.dialog_choice_rect.top + 20
        self.screen.blit(prompt_surface, (prompt_pos_x, prompt_pos_y))

        # 3. Draw options ("Yes", "No")
        self.choice_option_rects.clear() # Clear previous rects for mouse detection
        option_start_y = prompt_pos_y + prompt_surface.get_height() + 25
        option_spacing = self.dialog_font.get_height() + 10

        for i, option_text in enumerate(self.dialog_choice_options):
            color = (200, 200, 200) # Default color
            prefix = "  "
            if i == self.dialog_choice_selected_index:
                color = (255, 255, 100) # Highlighted color for selected option
                prefix = "> "
            
            option_surface = self.dialog_font.render(prefix + option_text, True, color)
            option_pos_x = self.dialog_choice_rect.centerx - option_surface.get_width() // 2
            option_pos_y = option_start_y + i * option_spacing
            option_rect = option_surface.get_rect(topleft=(option_pos_x, option_pos_y))
            
            self.screen.blit(option_surface, option_rect.topleft)
            self.choice_option_rects.append(option_rect)


    def handle_npc_dialog_completion(self):
        if not self.interacting_npc or not self.current_scene_id:
            self.end_interaction()
            return

        npc_name_interacted = self.interacting_npc.name
        dialog_key_just_finished = self.last_dialog_key_spoken_by_npc

        # --- Special handling for Noze's item offer ---
        if npc_name_interacted == "noze" and dialog_key_just_finished == "initial_offer":
            if not self.story_flags.get("noze_item_accepted") and not self.story_flags.get("noze_item_declined"):
                self.activate_dialog_choice(
                    prompt="Do you want to take the thing?",
                    options=["Yes", "No"],
                    callback_function=self.handle_noze_item_choice
                )
                # Interaction is not fully over; waiting for player's choice.
                # We return here to prevent normal 'on_interaction_end' flag setting from scene_config
                # and to keep 'self.interacting_npc' set for the callback.
                return 
            # If choice already made, just end interaction (NPC.interact will give follow-up)
            # This case should ideally be handled by NPC.interact() already giving the followup.
            # For safety, we can end here if flags are already set.
            # self.end_interaction() # This might be redundant if NPC.interact changes dialog
            # return

        # --- Normal on_interaction_end processing (for other NPCs or other dialogs) ---
        current_scene_cfg = next((sc for sc in self.scenes_data if sc['id'] == self.current_scene_id), None)
        npc_config_in_scene = None
        if current_scene_cfg:
            npc_config_in_scene = next((npc_def for npc_def in current_scene_cfg.get('npc_definitions', []) if npc_def['name'] == npc_name_interacted), None)
        
        scene_changed_by_dialog = False
        if npc_config_in_scene:
            on_end_actions = npc_config_in_scene.get('on_interaction_end')
            if on_end_actions:
                # Check if this on_end_action should apply only to specific dialog keys (optional advanced feature)
                # Example: dialog_key_condition = on_end_actions.get('if_dialog_key_was')
                # if not dialog_key_condition or dialog_key_condition == dialog_key_just_finished:

                flag_to_set = on_end_actions.get('set_story_flag')
                if flag_to_set:
                    # Prevent re-setting flags if already set, or handle as needed
                    if not self.story_flags.get(flag_to_set, False) or on_end_actions.get("allow_reset", False):
                         self.story_flags[flag_to_set] = True
                         print(f"Story flag set by {npc_name_interacted} (dialog: '{dialog_key_just_finished}'): {flag_to_set} = True")
                
                next_scene_trigger = on_end_actions.get('next_scene_if_flag_is_also_set')
                if next_scene_trigger:
                    required_flag = next_scene_trigger.get('flag')
                    target_scene_id = next_scene_trigger.get('scene_id')
                    if target_scene_id and ((required_flag and self.story_flags.get(required_flag)) or not required_flag):
                        print(f"NPC {npc_name_interacted} triggering scene change to {target_scene_id}.")
                        self.load_scene(target_scene_id)
                        scene_changed_by_dialog = True
        
        # If no scene change occurred and we are not in a dialog choice, end the interaction.
        if not scene_changed_by_dialog and not self.dialog_choice_active:
            self.end_interaction()


    def check_horizontal_collisions(self, original_x):
        if not self.player or not self.player.alive: return
        for platform in self.platforms:
            if self.player.rect.colliderect(platform.rect):
                overlap_y = max(0, min(self.player.rect.bottom, platform.rect.bottom) - max(self.player.rect.top, platform.rect.top))
                if overlap_y > self.player.rect.height / 4 or platform.is_wall:
                    if self.player.rect.x < original_x: self.player.rect.left = platform.rect.right
                    elif self.player.rect.x > original_x: self.player.rect.right = platform.rect.left

    def check_vertical_collisions(self):
        if not self.player or not self.player.alive: return
        was_in_air = not self.player.on_ground # Check if player was in air before this collision check
        self.player.on_ground = False
        for platform in self.platforms:
            if platform.is_wall: continue
            if self.player.rect.colliderect(platform.rect):
                if self.player.velocity_y > 0 and (self.player.rect.bottom - self.player.velocity_y) <= platform.rect.top + 1 and self.player.rect.bottom >= platform.rect.top:
                    self.player.rect.bottom = platform.rect.top
                    self.player.velocity_y = 0
                    self.player.on_ground = True

                    if was_in_air and self.story_flags.get("noze_cursed_jump_active"):
                        print("Noze's curse strikes upon landing!")
                        self.player.take_damage(3) # Apply lethal damage
                        self.player.jump_power = self.player.original_jump_power # Reset jump power
                        self.story_flags["noze_cursed_jump_active"] = False # Deactivate curse

                    break # Player can only be on one platform at a time like this

                elif self.player.velocity_y < 0 and \
                     (self.player.rect.top - self.player.velocity_y) >= platform.rect.bottom - 1 and \
                     self.player.rect.top <= platform.rect.bottom:
                    self.player.rect.top = platform.rect.bottom
                    self.player.velocity_y = 0
                   

            

    def handle_input(self): # Event handling for KEYDOWN is now primary in the event loop
        if not self.player or not self.player.alive : return
        if self.dialog_choice_active: return
        keys = pygame.key.get_pressed()
        original_x = self.player.rect.x
        player_moved_x_input = 0
        if not self.player.is_attacking and not self.active_dialog: # self.dialog_choice_active already handled above
            if keys[pygame.K_LEFT]: player_moved_x_input = -1
            if keys[pygame.K_RIGHT]: player_moved_x_input = 1
        self.player.move(player_moved_x_input, self.clock.get_time() / 1000.0)
        if keys[pygame.K_z] and not self.active_dialog: self.player.attack()
        if player_moved_x_input != 0 : self.check_horizontal_collisions(original_x)

    def run(self):
        running = True
        current_game_time_seconds = 0
        while running:
            dt_seconds = self.clock.tick(self.FPS) / 1000.0
            current_game_time_seconds += dt_seconds

            # --- Event Handling ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False
                
                # Dialog choice input handling (should take precedence)
                if self.dialog_choice_active:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            self.dialog_choice_selected_index = (self.dialog_choice_selected_index - 1 + len(self.dialog_choice_options)) % len(self.dialog_choice_options)
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            self.dialog_choice_selected_index = (self.dialog_choice_selected_index + 1) % len(self.dialog_choice_options)
                        elif event.key == pygame.K_RETURN or event.key == pygame.K_e: 
                            if self.dialog_choice_callback:
                                self.dialog_choice_callback(self.dialog_choice_selected_index)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1: 
                            mouse_pos = event.pos
                            for i, option_rect in enumerate(self.choice_option_rects):
                                if option_rect.collidepoint(mouse_pos):
                                    self.dialog_choice_selected_index = i 
                                    if self.dialog_choice_callback:
                                        self.dialog_choice_callback(self.dialog_choice_selected_index)
                                    break 
                    if event.type != pygame.QUIT : # Consume event if choice is active
                        continue # Skip other event processing for this event
                
                # Regular event handling if not in dialog choice
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if self.state == "menu":
                        # ... (menu button logic remains the same)
                        play_rect_center_x = self.WIDTH // 2
                        play_rect_center_y = self.HEIGHT // 2 - 40
                        play_rect = self.start_button_img.get_rect(center=(play_rect_center_x, play_rect_center_y)) if self.start_button_img else pygame.Rect(play_rect_center_x - 100, play_rect_center_y - 25, 200, 50)
                        exit_rect_center_y = self.HEIGHT // 2 + 40
                        exit_rect = self.exit_button_img.get_rect(center=(play_rect_center_x, exit_rect_center_y)) if self.exit_button_img else pygame.Rect(play_rect_center_x - 100, exit_rect_center_y - 25, 200, 50)
                        if play_rect.collidepoint(mouse_pos):
                            self.state = "playing"
                            self.reset_game()
                        elif exit_rect.collidepoint(mouse_pos): running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.state == "playing": self.state = "paused"
                        elif self.state == "paused": self.state = "playing"
                    
                    if self.state == "playing":
                        if event.key == pygame.K_SPACE: self.jump_requested = True
                        if event.key == pygame.K_e: 
                            if self.active_dialog: 
                                self.advance_dialog()
                            elif self.npc_interaction_candidate: 
                                self.start_interaction(self.npc_interaction_candidate)
                        
                        # Temp Scene Switchers
                        if self.scenes_data:
                            # ... (scene switcher logic remains same)
                            current_scene_index = next((i for i, s_data in enumerate(self.scenes_data) if s_data['id'] == self.current_scene_id), -1)
                            if current_scene_index != -1:
                                if event.key == pygame.K_PAGEUP:
                                    self.load_scene(self.scenes_data[(current_scene_index - 1 + len(self.scenes_data)) % len(self.scenes_data)]['id'])
                                if event.key == pygame.K_PAGEDOWN:
                                    self.load_scene(self.scenes_data[(current_scene_index + 1) % len(self.scenes_data)]['id'])
            
            # --- Game State Updates ---
            if self.state == "playing":
                if not self.player.alive: self.state = "menu" # Check for player death
                
                self.update_npc_interaction_candidate() 
                self.handle_input() # Player movement and attack input
                
                if self.player.alive:
                    self.player.update(dt_seconds, self.enemies) # Player update, including attack checks
                    self.player.apply_gravity()
                    self.check_vertical_collisions() # Player vertical collisions
                
                self.camera.update(self.player, self.current_world_width, self.current_world_height)
                
                # Update NPCs (including Witcher's special behavior)
                for npc_instance in self.npcs:
                    if isinstance(npc_instance, WitcherNPC):
                        npc_instance.update_behavior(dt_seconds, self.player.rect, self.platforms)
                    # Add other general NPC update logic here if needed (e.g., animations, simple movements)

                # Update Enemies
                for i_enemy in self.enemies[:]: 
                    if i_enemy.alive:
                        damage_val = i_enemy.update(dt_seconds, self.player.rect, self.platforms, current_game_time_seconds)
                        if damage_val > 0 and self.player.alive:
                            self.player.take_damage(damage_val)
                            if not self.player.alive:
                                print("Player died, returning to menu.")
                                self.state = "menu"
                                # Reset dialog/interaction states on player death
                                self.dialog_choice_active = False 
                                self.active_dialog = [] 
                                self.current_dialog_line_index = 0
                                self.interacting_npc = None
                                self.last_dialog_key_spoken_by_npc = None
                                break # Stop processing enemies if player died
                    else: 
                        if i_enemy.uid and i_enemy.uid not in self.defeated_enemy_uids:
                            self.defeated_enemy_uids.add(i_enemy.uid)
                            print(f"Enemy {i_enemy.uid} permanently defeated and recorded.")
                        self.enemies.remove(i_enemy) 
                
                # Update Projectiles & Check Collisions
                for proj in self.projectiles[:]:
                    if proj.alive:
                        proj.update(dt_seconds)
                        if self.player.alive and proj.rect.colliderect(self.player.rect):
                            self.player.take_damage(proj.damage)
                            proj.alive = False # Projectile hits once
                            if not self.player.alive:
                                print("Player died from projectile, returning to menu.")
                                self.state = "menu" 
                                # Reset dialog/interaction states
                                self.dialog_choice_active = False; self.active_dialog = []; # etc.
                                break # Stop processing projectiles if player died
                    if not proj.alive:
                        self.projectiles.remove(proj)

                if self.jump_requested:
                    if self.player.on_ground and self.player.alive and not self.active_dialog:
                        self.player.jump()
                    self.jump_requested = False
                
                if self.state == "playing": # Re-check as player might have died
                    self.check_scene_location_triggers()

            # --- Drawing ---
            self.screen.fill((10, 10, 10)) # Default dark background
            if self.state == "menu":
                # ... (menu drawing remains the same)
                if self.home_screen_img: 
                    self.screen.blit(pygame.transform.scale(self.home_screen_img, (self.WIDTH, self.HEIGHT)), (0,0))
                elif self.background_image_assets.get('main_bg'): 
                    self.screen.blit(pygame.transform.scale(self.background_image_assets['main_bg'], (self.WIDTH, self.HEIGHT)), (0,0))
                else: 
                    self.screen.fill((30, 30, 70)) 

                if self.start_button_img: 
                    self.screen.blit(self.start_button_img, self.start_button_img.get_rect(center=(self.WIDTH//2, self.HEIGHT//2 - 40)))
                if self.exit_button_img: 
                    self.screen.blit(self.exit_button_img, self.exit_button_img.get_rect(center=(self.WIDTH//2, self.HEIGHT//2 + 40)))
            
            elif self.state == "playing" or self.state == "paused":
                # Use the new draw_background_scaled_with_camera if you want parallax/zoomable backgrounds
                # For now, using simple scaled background
                if self.current_background:
                    # Simple scaling:
                    self.screen.blit(pygame.transform.scale(self.current_background, (self.WIDTH, self.HEIGHT)), (0, 0))
                    # OR for camera-scaled background (ensure self.current_background is large enough):
                    # draw_background_scaled_with_camera(self.screen, self.current_background, self.camera.rect, self.WIDTH, self.HEIGHT)
                else: self.screen.fill((30,30,30)) # Fallback bg color
                
                # Pass self.projectiles to draw_objects
                draw_objects(self.screen, self.player, self.platforms, self.npcs, self.enemies, self.projectiles, self.camera.rect, self.zoom)
                
                if self.player and self.player.alive:
                    self.light_angle += 0.05 * (dt_seconds * self.FPS if dt_seconds > 0 else 1)
                    # draw_darkness_with_light(self.screen, self.player, self.camera.rect, self.zoom, int(100 + math.sin(self.light_angle) * 8)) # Optional light effect

                # Interaction Prompt Drawing
                if self.npc_interaction_candidate and not self.active_dialog:
                    # ... (interaction prompt drawing remains the same)
                    prompt_text = "[E] Interact"
                    prompt_surf = self.interaction_prompt_font.render(prompt_text, True, (255, 255, 255))
                    npc_world_rect = self.npc_interaction_candidate.rect
                    prompt_world_x = npc_world_rect.centerx
                    prompt_world_y = npc_world_rect.top - 7 
                    prompt_screen_x = int((prompt_world_x - self.camera.rect.x) * self.zoom)
                    prompt_screen_y = int((prompt_world_y - self.camera.rect.y) * self.zoom)
                    prompt_display_rect = prompt_surf.get_rect(midbottom=(prompt_screen_x, prompt_screen_y))
                    bg_padding_x = 5; bg_padding_y = 2
                    bg_rect = prompt_display_rect.inflate(bg_padding_x * 2, bg_padding_y * 2)
                    prompt_bg_surface = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
                    pygame.draw.rect(prompt_bg_surface, (0, 0, 0, 170), prompt_bg_surface.get_rect(), border_radius=3)
                    self.screen.blit(prompt_bg_surface, bg_rect.topleft)
                    self.screen.blit(prompt_surf, prompt_display_rect)

                # UI Elements (Health, Geo, Coords)
                # ... (UI drawing remains the same)
                health_surf = self.font.render(f"Health: {self.player.health if self.player else 'N/A'}", True, (255,255,255))
                self.screen.blit(health_surf, (10,10))
                geo_surf = self.font.render(f"Geo: {self.player_data['geo']}", True, (255,223,0))
                self.screen.blit(geo_surf, (10,40))
                if self.player:
                    coords_surf = self.font.render(f"Coords: ({int(self.player.rect.x)}, {int(self.player.rect.y)})", True, (200,200,200))
                    self.screen.blit(coords_surf, (10, 70))


                # Dialog Box and Dialog Choice Prompt
                if self.active_dialog and self.interacting_npc:
                    # ... (dialog box drawing remains the same)
                    pygame.draw.rect(self.screen, (30,30,30,210), self.dialog_box_rect) # Semi-transparent
                    pygame.draw.rect(self.screen, (200,200,200), self.dialog_box_rect, 2) # Border
                    if 0 <= self.current_dialog_line_index < len(self.active_dialog):
                        draw_text(self.screen, self.active_dialog[self.current_dialog_line_index], self.dialog_font, (230,230,230), self.dialog_box_rect.inflate(-20,-20))
                    prompt_surf = self.dialog_font.render("E >", True, (180,180,180))
                    self.screen.blit(prompt_surf, (self.dialog_box_rect.right - prompt_surf.get_width()-10, self.dialog_box_rect.bottom - prompt_surf.get_height()-5))
                
                if self.dialog_choice_active: # Must be drawn after normal dialog box potentially
                    self.draw_dialog_choice_prompt()
                
                if self.state == "paused":
                    # ... (paused overlay drawing remains the same)
                    overlay = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
                    overlay.fill((0,0,0,150)) # alpha
                    self.screen.blit(overlay, (0,0))
                    resume_text = self.font.render("PAUSED - ESC to Resume", True, (255,255,255))
                    self.screen.blit(resume_text, resume_text.get_rect(center=(self.WIDTH/2, self.HEIGHT/2)))
            
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()
