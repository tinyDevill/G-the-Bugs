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
        self.interaction_prompt_font = pygame.font.Font(None, 22) # Font for "[E] Interact"

        # --- Asset Loading and Storage ---
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
        self.raw_enemy_images = {
            'idle': pygame.image.load("assets/image/enemy_idle.png").convert_alpha(),
            'walk1': pygame.image.load("assets/image/enemy_walk1.png").convert_alpha(),
            'walk2': pygame.image.load("assets/image/enemy_walk2.png").convert_alpha(),
            'attack1': pygame.image.load("assets/image/enemy_attack1.png").convert_alpha(),
            'attack2': pygame.image.load("assets/image/enemy_attack2.png").convert_alpha(),
            'attack3': pygame.image.load("assets/image/enemy_attack3.png").convert_alpha()
        }
        self.start_button_img = self.loaded_assets.get('start_button_img')
        self.exit_button_img = self.loaded_assets.get('exit_button_img')

        self.scenes_data = SCENES_DATA
        self.current_scene_id = None
        self.story_flags = {}

        self.platforms = []
        self.npcs = []
        self.enemies = []

        self.player = Player(0, 0, 40, 50)
        self.camera = Camera(int(self.WIDTH / self.zoom), int(self.HEIGHT / self.zoom), self.zoom)

        self.state = "menu"
        self.light_angle = 0
        self.player_data = {"geo": 0, "inventory": []}
        self.jump_requested = False
        self.interacting_npc = None
        self.active_dialog = []
        self.current_dialog_line_index = 0
        self.dialog_box_rect = pygame.Rect(50, self.HEIGHT - 110, self.WIDTH - 100, 90)
        
        self.npc_interaction_candidate = None # Stores NPC if player is close enough to interact

        self.reset_game()

    def reset_game(self):
        self.player.health = self.player.max_health
        self.player.alive = True
        self.player.time_since_last_damage = 0.0
        self.player.time_accumulated_for_heal_tick = 0.0
        self.player_data = {"geo": 0, "inventory": []}
        self.story_flags = {
            "truth_seeker_initial_talk_done": False,
            "truth_seeker_quest_accepted": False,
            "void_heart_obtained": False,
        }
        self.npc_interaction_candidate = None # Reset candidate on game reset
        if self.scenes_data:
            self.load_scene(SCENE_ID_SHRINE_START)
        else:
            print("CRITICAL ERROR: No scenes defined in scenes_data. Cannot start game.")
            pygame.quit()
            sys.exit("No scenes available to load.")

    def load_scene(self, scene_id_to_load):
        scene_config = next((sc for sc in self.scenes_data if sc['id'] == scene_id_to_load), None)

        if not scene_config:
            print(f"CRITICAL Error: Scene with ID '{scene_id_to_load}' not found.")
            if not self.current_scene_id and self.scenes_data:
                print("Attempting to load first defined scene as emergency fallback.")
                scene_config = self.scenes_data[0]
            else:
                pygame.quit()
                sys.exit(f"Failed to load scene: {scene_id_to_load}")

        print(f"Loading scene: {scene_config['id']}")
        self.current_scene_id = scene_config['id']
        self.current_background = self.background_image_assets.get(scene_config['background_key'], self.background_image_assets.get('main_bg'))
        self.current_world_width, self.current_world_height = scene_config.get('world_dimensions', (self.WIDTH, self.HEIGHT))
        self.player.rect.topleft = scene_config['player_start_pos']
        self.player.velocity_y = 0
        self.player.on_ground = False
        self.platforms.clear()
        self.npcs.clear()
        self.enemies.clear()
        self.npc_interaction_candidate = None # Reset candidate on scene load

        self.platforms = create_platforms_for_level(scene_config.get('platform_definitions', []), self.platform_image_assets)

        npc_default_w, npc_default_h = 50, 70
        for npc_def in scene_config.get('npc_definitions', []):
            required_flag = npc_def.get('appears_if_flag_true')
            if required_flag and not self.story_flags.get(required_flag, False):
                continue
            name = npc_def['name']
            dialogs = self.all_npc_dialogs.get(name)
            image = self.npc_image_assets.get(npc_def['image_key'])
            if dialogs and image:
                self.npcs.append(NPC(npc_def['x'], npc_def['y'], npc_def.get('width', npc_default_w), npc_def.get('height', npc_default_h), name, dialogs, image))
            else:
                print(f"NPC Load Warning: Missing dialogs or image for {name} (key: {npc_def['image_key']})")

        enemy_default_w, enemy_default_h = 60, 60
        for enemy_def in scene_config.get('enemy_definitions', []):
            self.enemies.append(Enemy(enemy_def['x'], enemy_def['y'], enemy_def.get('width', enemy_default_w), enemy_def.get('height', enemy_default_h), self.raw_enemy_images, attack_range=enemy_def.get('attack_range', 50), damage=enemy_def.get('damage', 1)))

        self.camera.rect.center = self.player.rect.center
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
                    print(f"Player triggered scene change to: {target_scene_id} via combined conditions.")
                    self.load_scene(target_scene_id)
                    break
    
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

    def handle_npc_dialog_completion(self):
        if not self.interacting_npc or not self.current_scene_id:
            self.end_interaction()
            return
        npc_name_interacted = self.interacting_npc.name
        dialog_key_just_finished = self.last_dialog_key_spoken_by_npc
        current_scene_cfg = next((sc for sc in self.scenes_data if sc['id'] == self.current_scene_id), None)
        npc_config_in_scene = None
        if current_scene_cfg:
            npc_config_in_scene = next((npc_def for npc_def in current_scene_cfg.get('npc_definitions', []) if npc_def['name'] == npc_name_interacted), None)
        
        scene_changed_by_dialog = False
        if npc_config_in_scene and dialog_key_just_finished:
            on_end_actions = npc_config_in_scene.get('on_interaction_end')
            if on_end_actions:
                flag_to_set = on_end_actions.get('set_story_flag')
                if flag_to_set:
                    self.story_flags[flag_to_set] = True
                    print(f"Story flag set by {npc_name_interacted}: {flag_to_set} = True")
                next_scene_trigger = on_end_actions.get('next_scene_if_flag_is_also_set')
                if next_scene_trigger:
                    required_flag = next_scene_trigger.get('flag')
                    target_scene_id = next_scene_trigger.get('scene_id')
                    if target_scene_id and ((required_flag and self.story_flags.get(required_flag)) or not required_flag):
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
        # Potentially re-check for interaction candidate if player is still near an NPC
        # self.update_npc_interaction_candidate() # This will be called in the main loop anyway

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
        self.player.on_ground = False
        for platform in self.platforms:
            if platform.is_wall: continue
            if self.player.rect.colliderect(platform.rect):
                if self.player.velocity_y > 0 and (self.player.rect.bottom - self.player.velocity_y) <= platform.rect.top + 1 and self.player.rect.bottom >= platform.rect.top:
                    self.player.rect.bottom = platform.rect.top
                    self.player.velocity_y = 0
                    self.player.on_ground = True
                elif self.player.velocity_y < 0 and (self.player.rect.top - self.player.velocity_y) >= platform.rect.bottom - 1 and self.player.rect.top <= platform.rect.bottom:
                    self.player.rect.top = platform.rect.bottom
                    self.player.velocity_y = 0

    def handle_input(self): # Event handling for KEYDOWN is now primary in the event loop
        if not self.player or not self.player.alive : return
        keys = pygame.key.get_pressed()
        original_x = self.player.rect.x
        player_moved_x_input = 0
        if not self.player.is_attacking and not self.active_dialog:
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

            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if self.state == "menu":
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
                        if event.key == pygame.K_e: # Interaction key
                            if self.active_dialog: # If dialog is active, advance it
                                self.advance_dialog()
                            elif self.npc_interaction_candidate: # Else, if an NPC is targeted for interaction
                                self.start_interaction(self.npc_interaction_candidate)
                        
                        # Temp Scene Switchers
                        if self.scenes_data:
                            current_scene_index = next((i for i, s_data in enumerate(self.scenes_data) if s_data['id'] == self.current_scene_id), -1)
                            if current_scene_index != -1:
                                if event.key == pygame.K_PAGEUP:
                                    self.load_scene(self.scenes_data[(current_scene_index - 1 + len(self.scenes_data)) % len(self.scenes_data)]['id'])
                                if event.key == pygame.K_PAGEDOWN:
                                    self.load_scene(self.scenes_data[(current_scene_index + 1) % len(self.scenes_data)]['id'])
            
            if self.state == "playing":
                if not self.player.alive: self.state = "menu"
                
                self.update_npc_interaction_candidate() # Update which NPC can be interacted with
                self.handle_input() # Handles player movement input and attack input
                
                if self.player.alive:
                    self.player.update(dt_seconds, self.enemies)
                    self.player.apply_gravity()
                    self.check_vertical_collisions()
                
                self.camera.update(self.player, self.current_world_width, self.current_world_height)
                
                for i_enemy in self.enemies[:]:
                    if i_enemy.alive:
                        damage_val = i_enemy.update(dt_seconds, self.player.rect, self.platforms, current_game_time_seconds)
                        if damage_val > 0 and self.player.alive:
                            self.player.take_damage(damage_val)
                            if not self.player.alive: self.state = "menu"
                    else: self.enemies.remove(i_enemy)
                
                if self.jump_requested:
                    if self.player.on_ground and self.player.alive and not self.active_dialog:
                        self.player.jump()
                    self.jump_requested = False
                
                self.check_scene_location_triggers()

            self.screen.fill((10, 10, 10))
            if self.state == "menu":
                if self.background_image_assets.get('main_bg'):
                    self.screen.blit(pygame.transform.scale(self.background_image_assets['main_bg'], (self.WIDTH, self.HEIGHT)), (0,0))
                if self.start_button_img: self.screen.blit(self.start_button_img, self.start_button_img.get_rect(center=(self.WIDTH//2, self.HEIGHT//2 - 40)))
                if self.exit_button_img: self.screen.blit(self.exit_button_img, self.exit_button_img.get_rect(center=(self.WIDTH//2, self.HEIGHT//2 + 40)))
            
            elif self.state == "playing" or self.state == "paused":
                if self.current_background:
                    self.screen.blit(pygame.transform.scale(self.current_background, (self.WIDTH, self.HEIGHT)), (0, 0))
                else: self.screen.fill((30,30,30))
                
                draw_objects(self.screen, self.player, self.platforms, self.npcs, self.enemies, self.camera.rect, self.zoom)
                
                if self.player and self.player.alive:
                    self.light_angle += 0.05 * (dt_seconds * self.FPS if dt_seconds > 0 else 1)
                    draw_darkness_with_light(self.screen, self.player, self.camera.rect, self.zoom, int(100 + math.sin(self.light_angle) * 8))

                # --- Interaction Prompt Drawing ---
                if self.npc_interaction_candidate and not self.active_dialog:
                    prompt_text = "[E] Interact"
                    prompt_surf = self.interaction_prompt_font.render(prompt_text, True, (255, 255, 255)) # White text
                    
                    # Position above the target NPC's head
                    npc_world_rect = self.npc_interaction_candidate.rect
                    prompt_world_x = npc_world_rect.centerx
                    prompt_world_y = npc_world_rect.top - 7 # Pixels above NPC's rect.top

                    # Convert world coordinates to screen coordinates
                    prompt_screen_x = int((prompt_world_x - self.camera.rect.x) * self.zoom)
                    prompt_screen_y = int((prompt_world_y - self.camera.rect.y) * self.zoom)
                    
                    prompt_display_rect = prompt_surf.get_rect(midbottom=(prompt_screen_x, prompt_screen_y))
                    
                    # Background for the prompt text for better visibility
                    bg_padding_x = 5
                    bg_padding_y = 2
                    bg_rect = prompt_display_rect.inflate(bg_padding_x * 2, bg_padding_y * 2)
                    
                    # Draw a semi-transparent background rectangle for the prompt
                    # Need a surface with SRCALPHA for the rect itself if you want alpha on the rect color
                    prompt_bg_surface = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
                    pygame.draw.rect(prompt_bg_surface, (0, 0, 0, 170), prompt_bg_surface.get_rect(), border_radius=3)
                    self.screen.blit(prompt_bg_surface, bg_rect.topleft)
                    
                    self.screen.blit(prompt_surf, prompt_display_rect) # Draw the text on top

                # UI Elements
                health_surf = self.font.render(f"Health: {self.player.health if self.player else 'N/A'}", True, (255,255,255))
                self.screen.blit(health_surf, (10,10))
                geo_surf = self.font.render(f"Geo: {self.player_data['geo']}", True, (255,223,0))
                self.screen.blit(geo_surf, (10,40))
                if self.player:
                    coords_surf = self.font.render(f"Coords: ({int(self.player.rect.x)}, {int(self.player.rect.y)})", True, (200,200,200))
                    self.screen.blit(coords_surf, (10, 70))

                if self.active_dialog and self.interacting_npc:
                    pygame.draw.rect(self.screen, (30,30,30,210), self.dialog_box_rect)
                    pygame.draw.rect(self.screen, (200,200,200), self.dialog_box_rect, 2)
                    if 0 <= self.current_dialog_line_index < len(self.active_dialog):
                        draw_text(self.screen, self.active_dialog[self.current_dialog_line_index], self.dialog_font, (230,230,230), self.dialog_box_rect.inflate(-20,-20))
                    prompt_surf = self.dialog_font.render("E >", True, (180,180,180))
                    self.screen.blit(prompt_surf, (self.dialog_box_rect.right - prompt_surf.get_width()-10, self.dialog_box_rect.bottom - prompt_surf.get_height()-5))

                if self.state == "paused":
                    overlay = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
                    overlay.fill((0,0,0,150))
                    self.screen.blit(overlay, (0,0))
                    resume_text = self.font.render("PAUSED - ESC to Resume", True, (255,255,255))
                    self.screen.blit(resume_text, resume_text.get_rect(center=(self.WIDTH/2, self.HEIGHT/2)))
            
            pygame.display.flip()
        pygame.quit()
        sys.exit()
