# game.py
import pygame
import sys
import math

from npc import NPC, truth_seeker_dialogs, steelsoul_dialogs, noze_dialogs, lost_knight_dialogs
from character import Player  
from enemy import Enemy
from gameobject import Platform, Animation, create_platforms_for_level
from screen import (load_assets, Camera, draw_background_scaled_with_camera, draw_objects, 
                    draw_darkness_with_light, draw_text)

# Import the scene configuration
from scene_config import SCENES_DATA, SCENE_ID_SHRINE_START # Import your scene IDs

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
        
        # --- Asset Loading and Storage ---
        # load_assets should return a dictionary of all loaded surfaces
        self.loaded_assets = load_assets(self.WIDTH, self.HEIGHT) 

        self.platform_image_assets = {
            'floor1_img': self.loaded_assets.get('floor1_img'),
            'floor2_img': self.loaded_assets.get('floor2_img'),
            'platform_img': self.loaded_assets.get('platform_img'),
            'benchbottom_img': self.loaded_assets.get('benchbottom_img'),
            'benchside2_1_img': self.loaded_assets.get('benchside2_1_img'),
            'benchside2_2_img': self.loaded_assets.get('benchside2_2_img'),
            'wall_img': self.loaded_assets.get('wall_img'),
        }
        self.npc_image_assets = {
            'truth_seeker': self.loaded_assets.get('truth_seeker_img'),
            'steelsoul': self.loaded_assets.get('steelsoul_img'),
            'noze': self.loaded_assets.get('noze_img'),
            # 'lost_knight': self.loaded_assets.get('lost_knight_img'), # Add if you have this asset
        }
        self.background_image_assets = {
            'main_bg': self.loaded_assets.get('main_bg'),
            'cave_bg': self.loaded_assets.get('cave_bg'),
        }
        self.all_npc_dialogs = {
            'truth_seeker': truth_seeker_dialogs,
            'steelsoul': steelsoul_dialogs,
            'noze': noze_dialogs,
            'lost_knight': lost_knight_dialogs,
        }
        # Enemy animation images (assuming they are consistent for all 'default' enemy types)
        self.raw_enemy_images = {
            'idle': pygame.image.load("assets/image/enemy_idle.png").convert_alpha(),
            'walk1': pygame.image.load("assets/image/enemy_walk1.png").convert_alpha(),
            'walk2': pygame.image.load("assets/image/enemy_walk2.png").convert_alpha(),
            'attack1': pygame.image.load("assets/image/enemy_attack1.png").convert_alpha(),
            'attack2': pygame.image.load("assets/image/enemy_attack2.png").convert_alpha(),
            'attack3': pygame.image.load("assets/image/enemy_attack3.png").convert_alpha()
        }
        # UI Images
        self.start_button_img = self.loaded_assets.get('start_button_img')
        self.exit_button_img = self.loaded_assets.get('exit_button_img')

        # --- Scene Management ---
        self.scenes_data = SCENES_DATA
        self.current_scene_id = None # Will be set in reset_game via load_scene
        self.story_flags = {} # For story progression

        # --- Game Object Lists ---
        self.platforms = []
        self.npcs = []
        self.enemies = []

        # --- Player and Camera ---
        self.player = Player(0, 0, 40, 50) # Initialized once, position set by scene
        self.camera = Camera(int(self.WIDTH / self.zoom), int(self.HEIGHT / self.zoom), self.zoom)
        
        # --- Game State and UI ---
        self.state = "menu" 
        self.light_angle = 0
        self.player_data = {"geo": 0, "inventory": []} # Persists across scenes
        self.jump_requested = False
        self.interacting_npc = None
        self.active_dialog = []
        self.current_dialog_line_index = 0
        self.dialog_box_rect = pygame.Rect(50, self.HEIGHT - 110, self.WIDTH - 100, 90) # Adjusted dialog box

        self.reset_game() # Initialize first scene

    def reset_game(self): # For full game restart
        self.player.health = self.player.max_health
        self.player.alive = True
        self.player_data = {"geo": 0, "inventory": []} # Reset persistent player data
        self.story_flags = { # Reset story flags to their initial state
            "truth_seeker_initial_talk_done": False,
            "truth_seeker_quest_accepted": False,
            "void_heart_obtained": False, # Example
            # Add any other initial story flags here
        }
        # self.state = "playing"  # <<< REMOVE OR COMMENT OUT THIS LINE
        
        # Load the initial scene (e.g., the first scene defined in your SCENES_DATA)
        # Make sure SCENE_ID_SHRINE_START is correctly defined and imported
        if self.scenes_data: # Ensure scenes_data is populated
            self.load_scene(SCENE_ID_SHRINE_START) # Or self.scenes_data[0]['id']
        else:
            print("CRITICAL ERROR: No scenes defined in scenes_data. Cannot start game.")
            # Handle this error, perhaps by setting state to an error screen or quitting
            pygame.quit()
            sys.exit("No scenes available to load.")

    def load_scene(self, scene_id_to_load):
        scene_config = None
        for sc_data in self.scenes_data:
            if sc_data['id'] == scene_id_to_load:
                scene_config = sc_data
                break
        
        if not scene_config:
            print(f"CRITICAL Error: Scene with ID '{scene_id_to_load}' not found. Game cannot continue.")
            # Fallback to first scene if current_scene_id is None, otherwise stay or quit
            if not self.current_scene_id and self.scenes_data:
                print("Attempting to load first defined scene as emergency fallback.")
                scene_config = self.scenes_data[0]
            else:
                 pygame.quit()
                 sys.exit(f"Failed to load scene: {scene_id_to_load}")


        print(f"Loading scene: {scene_config['id']}")
        self.current_scene_id = scene_config['id']

        self.current_background = self.background_image_assets.get(scene_config['background_key'])
        if not self.current_background: # Fallback background
            print(f"Warning: Background key '{scene_config['background_key']}' not found. Using default.")
            self.current_background = self.background_image_assets.get('main_bg') 
        
        self.current_world_width = scene_config.get('world_dimensions', (self.WIDTH, self.HEIGHT))[0]
        self.current_world_height = scene_config.get('world_dimensions', (self.WIDTH, self.HEIGHT))[1]

        self.player.rect.topleft = scene_config['player_start_pos']
        self.player.velocity_y = 0
        self.player.on_ground = False 

        self.platforms.clear()
        self.npcs.clear()
        self.enemies.clear()

        self.platforms = create_platforms_for_level(
            scene_config.get('platform_definitions', []), 
            self.platform_image_assets
        )

        npc_default_w, npc_default_h = 50, 70
        for npc_def in scene_config.get('npc_definitions', []):
            # Conditional NPC appearance based on story flags (Example)
            required_flag = npc_def.get('appears_if_flag_true')
            if required_flag and not self.story_flags.get(required_flag, False):
                continue # Skip this NPC if flag condition not met

            name = npc_def['name']
            dialogs = self.all_npc_dialogs.get(name)
            image = self.npc_image_assets.get(npc_def['image_key'])
            if dialogs and image:
                new_npc = NPC(npc_def['x'], npc_def['y'], 
                              npc_def.get('width', npc_default_w), 
                              npc_def.get('height', npc_default_h), 
                              name, dialogs, image)
                self.npcs.append(new_npc)
            else:
                print(f"NPC Load Warning: Missing dialogs or image for {name} (key: {npc_def['image_key']})")
        
        enemy_default_w, enemy_default_h = 60, 60
        for enemy_def in scene_config.get('enemy_definitions', []):
            # Here you could use enemy_def.get('type') to select different enemy animation sets if needed
            new_enemy = Enemy(enemy_def['x'], enemy_def['y'],
                              enemy_def.get('width', enemy_default_w), 
                              enemy_def.get('height', enemy_default_h),
                              self.raw_enemy_images, # Pass the base animation images
                              attack_range=enemy_def.get('attack_range', 50),
                              damage=enemy_def.get('damage', 1))
            self.enemies.append(new_enemy)
        
        self.camera.rect.center = self.player.rect.center
        self.light_angle = 0
        self.interacting_npc = None
        self.active_dialog = []
        self.current_dialog_line_index = 0

    def check_scene_location_triggers(self):
        if not self.current_scene_id or not self.player or not self.player.alive: return

        current_scene_cfg = next((sc for sc in self.scenes_data if sc['id'] == self.current_scene_id), None)
        if not current_scene_cfg or not current_scene_cfg.get('transitions'): return

        for transition in current_scene_cfg['transitions']:
            if transition.get('type') == 'player_at_location' or \
               transition.get('type') == 'player_at_location_and_flag':
                
                trigger_rect = pygame.Rect(transition['rect_coords'])
                conditions_met = False
                if self.player.rect.colliderect(trigger_rect):
                    if transition.get('type') == 'player_at_location_and_flag':
                        flag_name = transition.get('required_story_flag')
                        if flag_name and self.story_flags.get(flag_name, False):
                            conditions_met = True
                        elif not flag_name: # If flag is optional or not specified for this type
                            conditions_met = True 
                    else: # type is 'player_at_location'
                         conditions_met = True
                
                if conditions_met:
                    target_scene_id = transition['target_scene_id']
                    print(f"Player triggered scene change to: {target_scene_id} via location.")
                    self.load_scene(target_scene_id)
                    break 

    def start_interaction(self, npc):
        self.interacting_npc = npc
        # NPC.interact now returns a dict: {'dialog': list_of_lines, 'dialog_key_spoken': str}
        interaction_result = npc.interact(self.player_data, self.story_flags)
        self.active_dialog = interaction_result.get('dialog', ["..."])
        # Store the key of the dialog sequence that was just initiated
        self.last_dialog_key_spoken_by_npc = interaction_result.get('dialog_key_spoken', None)
        self.current_dialog_line_index = 0

    def advance_dialog(self):
        if not self.active_dialog or not self.interacting_npc:
            self.end_interaction() # Should not happen if called correctly
            return

        self.current_dialog_line_index += 1
        if self.current_dialog_line_index >= len(self.active_dialog):
            self.handle_npc_dialog_completion() # Dialog sequence finished

    def handle_npc_dialog_completion(self):
        if not self.interacting_npc or not self.current_scene_id:
            self.end_interaction()
            return

        npc_name_interacted = self.interacting_npc.name
        dialog_key_just_finished = self.last_dialog_key_spoken_by_npc # Get the key of the dialog that just ended

        # Find this NPC's definition in the current scene config
        current_scene_cfg = next((sc for sc in self.scenes_data if sc['id'] == self.current_scene_id), None)
        npc_config_in_scene = None
        if current_scene_cfg:
            for npc_def in current_scene_cfg.get('npc_definitions', []):
                if npc_def['name'] == npc_name_interacted:
                    npc_config_in_scene = npc_def
                    break
        
        scene_changed_by_dialog = False
        if npc_config_in_scene and dialog_key_just_finished:
            # Check 'on_interaction_end' or more specific triggers in npc_config_in_scene
            # This part requires careful design of your scene_config's NPC interaction triggers.
            # Example simple trigger from scene_config:
            on_end_actions = npc_config_in_scene.get('on_interaction_end') # General action after any talk
            
            # More specific triggers based on which dialog_key finished:
            # interaction_triggers = npc_config_in_scene.get('interaction_triggers', [])
            # for trigger in interaction_triggers:
            #    if trigger.get('dialog_key_ends') == dialog_key_just_finished:
            #        # Check other conditions like story_flags
            #        if trigger.get('set_story_flag'): self.story_flags[trigger['set_story_flag']] = True
            #        if trigger.get('triggers_scene_change_to'): self.load_scene(...) etc.

            if on_end_actions: # Simplified example based on the earlier scene_config structure
                flag_to_set = on_end_actions.get('set_story_flag')
                if flag_to_set:
                    self.story_flags[flag_to_set] = True
                    print(f"Story flag set by {npc_name_interacted}: {flag_to_set} = True")

                next_scene_trigger = on_end_actions.get('next_scene_if_flag_is_also_set')
                if next_scene_trigger:
                    required_flag = next_scene_trigger.get('flag')
                    if required_flag and self.story_flags.get(required_flag):
                        target_scene_id = next_scene_trigger.get('scene_id')
                        if target_scene_id:
                            print(f"NPC {npc_name_interacted} triggering scene change to {target_scene_id} (flag '{required_flag}' was set).")
                            self.load_scene(target_scene_id)
                            scene_changed_by_dialog = True
                    elif not required_flag: # Direct scene change if no flag needed
                        target_scene_id = next_scene_trigger.get('scene_id') # Should be direct target_scene_id here
                        if target_scene_id: # If scene_id is directly under on_interaction_end
                             print(f"NPC {npc_name_interacted} triggering scene change to {target_scene_id}.")
                             self.load_scene(target_scene_id)
                             scene_changed_by_dialog = True


        if not scene_changed_by_dialog:
            self.end_interaction()

    def end_interaction(self):
        self.interacting_npc = None
        self.active_dialog = []
        self.current_dialog_line_index = 0
        self.last_dialog_key_spoken_by_npc = None


    # --- Collision Methods for Player (keep these in Game class) ---
    def check_horizontal_collisions(self, original_x):
        if not self.player or not self.player.alive: return
        for platform in self.platforms:
            if self.player.rect.colliderect(platform.rect):
                overlap_y = max(0, min(self.player.rect.bottom, platform.rect.bottom) - max(self.player.rect.top, platform.rect.top))
                if overlap_y > self.player.rect.height / 4 or platform.is_wall:
                    if self.player.rect.x < original_x:  # Moved left
                        self.player.rect.left = platform.rect.right
                    elif self.player.rect.x > original_x:  # Moved right
                        self.player.rect.right = platform.rect.left

    def check_vertical_collisions(self):
        if not self.player or not self.player.alive: return
        self.player.on_ground = False
        for platform in self.platforms:
            if platform.is_wall: continue
            if self.player.rect.colliderect(platform.rect):
                if self.player.velocity_y > 0: 
                    previous_player_bottom = self.player.rect.bottom - self.player.velocity_y
                    if previous_player_bottom <= platform.rect.top + 1 and self.player.rect.bottom >= platform.rect.top:
                        self.player.rect.bottom = platform.rect.top
                        self.player.velocity_y = 0
                        self.player.on_ground = True
                elif self.player.velocity_y < 0: 
                    previous_player_top = self.player.rect.top - self.player.velocity_y
                    if previous_player_top >= platform.rect.bottom - 1 and self.player.rect.top <= platform.rect.bottom:
                        self.player.rect.top = platform.rect.bottom
                        self.player.velocity_y = 0
    
    # --- Input Handling for Player ---
    def handle_input(self):
        if not self.player or not self.player.alive : return
        
        keys = pygame.key.get_pressed()
        original_x = self.player.rect.x
        player_moved_x_input = 0

        if not self.player.is_attacking and not self.active_dialog:
            if keys[pygame.K_LEFT]:
                player_moved_x_input = -1
            if keys[pygame.K_RIGHT]:
                player_moved_x_input = 1
        
        self.player.move(player_moved_x_input, self.clock.get_time() / 1000.0) # Pass dt for move

        if keys[pygame.K_z] and not self.active_dialog:
            self.player.attack()

        if player_moved_x_input != 0 : # Only check horizontal collisions if player tried to move
            self.check_horizontal_collisions(original_x)


    def run(self):
        running = True
        current_game_time_seconds = 0 

        while running:
            dt_seconds = self.clock.tick(self.FPS) / 1000.0
            current_game_time_seconds += dt_seconds

            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if self.state == "menu":
                        # Define play_rect based on your button image and position
                        play_rect_center_x = self.WIDTH // 2
                        play_rect_center_y = self.HEIGHT // 2 - 40 # Adjust as per your menu layout
                        
                        # Ensure start_button_img is loaded and valid before calling get_rect
                        if self.start_button_img:
                            play_rect = self.start_button_img.get_rect(center=(play_rect_center_x, play_rect_center_y))
                        else: # Fallback if image isn't loaded, create a default rect
                            play_rect = pygame.Rect(play_rect_center_x - 100, play_rect_center_y - 25, 200, 50)

                        # Similar for exit_rect
                        exit_rect_center_y = self.HEIGHT // 2 + 40
                        if self.exit_button_img:
                            exit_rect = self.exit_button_img.get_rect(center=(play_rect_center_x, exit_rect_center_y))
                        else:
                            exit_rect = pygame.Rect(play_rect_center_x - 100, exit_rect_center_y - 25, 200, 50)
                            
                        if play_rect.collidepoint(mouse_pos):
                            self.state = "playing" # Set state to playing
                            self.reset_game()      # Then reset game variables and load initial scene
                        elif exit_rect.collidepoint(mouse_pos):
                            running = False
                    # ... (paused state mouse clicks)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.state == "playing": self.state = "paused"
                        elif self.state == "paused": self.state = "playing"
                    
                    if self.state == "playing":
                        if event.key == pygame.K_SPACE: self.jump_requested = True
                        if event.key == pygame.K_e:
                            if self.active_dialog: self.advance_dialog()
                            else:
                                interaction_radius = 60 
                                for npc_instance in self.npcs: # npc_instance to avoid conflict
                                    if npc_instance.active: # Should always be true if loaded by scene
                                        dist_x = abs(self.player.rect.centerx - npc_instance.rect.centerx)
                                        dist_y = abs(self.player.rect.centery - npc_instance.rect.centery)
                                        if dist_x < interaction_radius and dist_y < interaction_radius :
                                            self.start_interaction(npc_instance)
                                            break
                        # Temporary Scene Switchers (REMOVE FOR FINAL GAME)
                        if event.key == pygame.K_PAGEUP:
                            prev_idx = (self.scenes_data.index(next(s for s in self.scenes_data if s['id'] == self.current_scene_id)) - 1 + len(self.scenes_data)) % len(self.scenes_data)
                            self.load_scene(self.scenes_data[prev_idx]['id'])
                        if event.key == pygame.K_PAGEDOWN:
                            next_idx = (self.scenes_data.index(next(s for s in self.scenes_data if s['id'] == self.current_scene_id)) + 1) % len(self.scenes_data)
                            self.load_scene(self.scenes_data[next_idx]['id'])
            
            # --- Game Logic Loop ---
            if self.state == "playing":
                if not self.player.alive:
                    self.state = "menu" # Or game_over state then menu

                self.handle_input() # Handles player x-movement and horizontal collision
                
                if self.player.alive:
                    self.player.update(dt_seconds, self.enemies) # Player attacks enemies
                    self.player.apply_gravity() # Player Y-movement due to gravity
                    self.check_vertical_collisions() # Player vertical collision resolution
                
                self.camera.update(self.player, self.current_world_width, self.current_world_height)

                for i_enemy in self.enemies[:]: # Use i_enemy to avoid conflict
                    if i_enemy.alive:
                        damage_val = i_enemy.update(dt_seconds, self.player.rect, self.platforms, current_game_time_seconds)
                        if damage_val > 0 and self.player.alive:
                            self.player.take_damage(damage_val)
                            if not self.player.alive: self.state = "menu"
                    elif not i_enemy.alive: 
                        self.enemies.remove(i_enemy)
                
                if self.jump_requested:
                    if self.player.on_ground and self.player.alive and not self.active_dialog:
                        self.player.jump()
                    self.jump_requested = False
                
                self.check_scene_location_triggers() # Check for location-based scene changes

            # --- Drawing Loop ---
            self.screen.fill((10, 10, 10)) # Default dark background

            if self.state == "menu":
                if self.background_image_assets.get('main_bg'):
                    # Menu background: entire image scaled to fit screen, static
                    menu_bg_surface = self.background_image_assets['main_bg']
                    if menu_bg_surface: # Ensure the asset exists
                        menu_bg_scaled = pygame.transform.scale(menu_bg_surface, (self.WIDTH, self.HEIGHT))
                        self.screen.blit(menu_bg_scaled, (0,0))
                if self.start_button_img:
                    play_btn_rect = self.start_button_img.get_rect(center=(self.WIDTH//2, self.HEIGHT//2 - 40))
                    self.screen.blit(self.start_button_img, play_btn_rect)
                if self.exit_button_img:
                    exit_btn_rect = self.exit_button_img.get_rect(center=(self.WIDTH//2, self.HEIGHT//2 + 40))
                    self.screen.blit(self.exit_button_img, exit_btn_rect)

            elif self.state == "playing" or self.state == "paused":
                if self.current_background:
                    # --- NEW WAY TO DRAW BACKGROUND FOR PLAYING STATE ---
                    # This makes it static and scaled to fit the entire screen, like the menu.
                    # It will NOT scroll.
                    scaled_playing_bg = pygame.transform.scale(self.current_background, (self.WIDTH, self.HEIGHT))
                    self.screen.blit(scaled_playing_bg, (0, 0))
                else:
                    self.screen.fill((30,30,30)) # Fallback if no current_background

                # draw_objects will still use camera for scrolling game elements over this static background
                draw_objects(self.screen, self.player, self.platforms, self.npcs, self.enemies, self.camera.rect, self.zoom)

                if self.player and self.player.alive:
                    self.light_angle += 0.05 * (dt_seconds * self.FPS if dt_seconds > 0 else 1)
                    pulse = math.sin(self.light_angle) * 8
                    light_radius = int(100 + pulse)
                    draw_darkness_with_light(self.screen, self.player, self.camera.rect, self.zoom, light_radius)
                
                # UI Elements (Health, Geo, Dialog)
                health_surf = self.font.render(f"Health: {self.player.health if self.player else 'N/A'}", True, (255,255,255))
                self.screen.blit(health_surf, (10,10))
                geo_surf = self.font.render(f"Geo: {self.player_data['geo']}", True, (255,223,0))
                self.screen.blit(geo_surf, (10,40))

                if self.active_dialog and self.interacting_npc:
                    pygame.draw.rect(self.screen, (30,30,30,210), self.dialog_box_rect) # Darker, more opaque
                    pygame.draw.rect(self.screen, (200,200,200), self.dialog_box_rect, 2)
                    if 0 <= self.current_dialog_line_index < len(self.active_dialog):
                        line = self.active_dialog[self.current_dialog_line_index]
                        draw_text(self.screen, line, self.dialog_font, (230,230,230), self.dialog_box_rect.inflate(-20,-20))
                    prompt_surf = self.dialog_font.render("E >", True, (180,180,180))
                    self.screen.blit(prompt_surf, (self.dialog_box_rect.right - prompt_surf.get_width()-10, self.dialog_box_rect.bottom - prompt_surf.get_height()-5))

                if self.state == "paused":
                    # ... (your pause overlay drawing)
                    overlay = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
                    overlay.fill((0,0,0,150))
                    self.screen.blit(overlay, (0,0))
                    resume_text = self.font.render("PAUSED - ESC to Resume", True, (255,255,255))
                    text_rect = resume_text.get_rect(center=(self.WIDTH/2, self.HEIGHT/2))
                    self.screen.blit(resume_text, text_rect)

            pygame.display.flip()

        pygame.quit()
        sys.exit()
