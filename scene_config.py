# scene_config.py

# Define Scene IDs as constants for easier reference and less typos
SCENE_ID_SHRINE_START = 'shrine_start'
SCENE_ID_SHRINE_AFTER_TRUTHSEEKER_TALK = 'shrine_after_truthseeker_talk' # Example
SCENE_ID_SCENE2 = 'cave_path_entry'
SCENE_ID_SCENE3 = 'scene3' # New Scene 3 ID
SCENE_ID_SCENE4 = 'scene4' # New Scene 4 ID
SCENE_ID_SCENE5 = 'scene5' # New Scene 5 ID

# Define screen dimensions here if needed for coordinates, or get from game instance
# For simplicity, we'll use absolute coordinates assuming a known game height (e.g., 600)
GAME_HEIGHT = 600
GAME_WIDTH = 1200 # Assuming the main game width for now

SCENES_DATA = [
    {
        'id': SCENE_ID_SHRINE_START,
        'player_start_pos': (50, 200), # Player height 50, on floor2_img
        'background_key': 'main_bg', # Key from Game.background_image_assets
        'world_dimensions': (GAME_WIDTH, GAME_HEIGHT), # Tuple (width, height)
        'platform_definitions': [ # (x, y, w, h, image_key, is_wall)
            (0, GAME_HEIGHT - 200, 402, 200, 'floor2_img', False), # Ground platform for player start
            (395, 520, 810, 90, 'floor1_img', False), # Main long floor
            # (500, GAME_HEIGHT - 200, 150, 20, 'platform_img', False),
            # (800, GAME_HEIGHT - 250, 150, 20, 'platform_img', False),
            (125, GAME_HEIGHT - 270, 30, 80, 'benchside2_1_img', False), # Bench Y adjusted for floor2_img
            (155, GAME_HEIGHT - 230, 60, 40, 'benchbottom_img', False), # Bench Y
            (215, GAME_HEIGHT - 270, 30, 80, 'benchside2_2_img', False), # Bench Y
            (-10, 0, 10, GAME_HEIGHT, 'wall_img', True), # Adjusted left wall to allow exit from 0
            (GAME_WIDTH, 0, 10, GAME_HEIGHT, 'wall_img', True)   # Adjusted right wall
        ],
        'npc_definitions': [
            {
                'name': 'truth_seeker', 'x': 300, 'y': 330, # On floor2_img
                'width': 50, 'height': 70, 'image_key': 'truth_seeker',
                'on_interaction_end': { # This will be checked when dialog ends in Game class
                    'set_story_flag': 'truth_seeker_initial_talk_done',
                }
            }
        ],
        'enemy_definitions': [
            # Enemy Y is top of enemy. Floor1_img top is GAME_HEIGHT - 80. Enemy height 60.
            {'x': 890, 'y': GAME_HEIGHT - 80 - 60, 'width': 60, 'height': 60, 'type': 'default_enemy', 'attack_range': 70, 'damage': 1},
            # Platform_img at Y = GAME_HEIGHT - 200, H=20. Enemy top: GAME_HEIGHT - 200 - 60
            {'x': 500, 'y': GAME_HEIGHT - 200 - 60, 'width': 60, 'height': 60, 'type': 'default_enemy', 'attack_range': 50, 'damage': 1}
        ],
        'transitions': [
            {
                'type': 'player_at_location_and_flag',
                # Trigger zone slightly before the absolute edge for smoother transition
                'rect_coords': (GAME_WIDTH - 60, GAME_HEIGHT - 180, 50, 160), # Right edge, on floor1_img
                'required_story_flag': 'truth_seeker_initial_talk_done',
                'must_all_enemies_be_slain': True,
                'target_scene_id': SCENE_ID_SCENE2
            }
        ]
    },
    {
        'id': SCENE_ID_SCENE2, # Scene 2
        'player_start_pos': (50, GAME_HEIGHT - 70 - 50), # Player height = 50, on floor
        'background_key': 'cave_bg', # User needs to ensure 'cave_bg' is loaded
        'world_dimensions': (1600, GAME_HEIGHT), # A wider cave area
        'platform_definitions': [
            (0, GAME_HEIGHT - 70, 1600, 70, 'floor1_img', False), # Wider floor
            (300, GAME_HEIGHT - 150, 200, 20, 'platform_img', False),
            (600, GAME_HEIGHT - 250, 150, 20, 'platform_img', False),
            (900, GAME_HEIGHT - 200, 200, 20, 'platform_img', False), # Another platform
            (-10, 0, 10, GAME_HEIGHT, 'wall_img', True), # Left wall
            (1600, 0, 10, GAME_HEIGHT, 'wall_img', True), # Right wall
        ],
        'npc_definitions': [
            {
                'name': 'steelsoul', 'x': 700, 'y': GAME_HEIGHT - 70 - 70, # On floor
                'width': 50, 'height': 70, 'image_key': 'steelsoul',
            },
            
        ],
        'enemy_definitions': [
            {'x': 450, 'y': GAME_HEIGHT - 70 - 60, 'width': 60, 'height': 60, 'type': 'cave_crawler', 'attack_range': 40, 'damage': 1},
            {'x': 1000, 'y': GAME_HEIGHT - 200 - 60, 'width': 60, 'height': 60, 'type': 'cave_bat', 'attack_range': 80, 'damage': 1} # On platform
        ],
        'transitions': [
            {
                'type': 'player_at_location',
                'rect_coords': (1, GAME_HEIGHT - 120, 40, 100), # Exit on the left to go back
                'target_scene_id': SCENE_ID_SHRINE_START
            },
            {
                'type': 'player_at_location', # Transition to Scene 3
                'rect_coords': (1600 - 60, GAME_HEIGHT - 140, 50, 120), # Right edge
                'target_scene_id': SCENE_ID_SCENE3
            }
        ]
    },
    {
        'id': SCENE_ID_SCENE3, # New Scene 3: Forest Path
        'player_start_pos': (50, GAME_HEIGHT - 90 - 50), # On a forest floor
        'background_key': 'forest_bg', # Create 'forest_bg.png' or similar in assets
        'world_dimensions': (1800, GAME_HEIGHT), # Wider than default
        'platform_definitions': [
            (0, GAME_HEIGHT - 90, 1800, 90, 'floor1_img', False), # Forest floor (can use 'floor_grass_img')
            (200, GAME_HEIGHT - 180, 150, 20, 'platform_img', False), # Tree branch like platform
            (500, GAME_HEIGHT - 220, 200, 20, 'platform_img', False),
            (900, GAME_HEIGHT - 150, 100, 20, 'platform_img', False),
            (1300, GAME_HEIGHT - 250, 250, 20, 'platform_img', False),
            (-10, 0, 10, GAME_HEIGHT, 'wall_img', True),
            (1800, 0, 10, GAME_HEIGHT, 'wall_img', True),
        ],
        'npc_definitions': [
            { # Add a new NPC type, e.g., ''
                'name': 'noze', 'x': 800, 'y': GAME_HEIGHT - 90 - 70,
                'width': 50, 'height': 70, 'image_key': 'noze_img', # 
            }
        ],
        'enemy_definitions': [
            {'x': 300, 'y': GAME_HEIGHT - 90 - 60, 'width': 60, 'height': 60, 'type': 'forest_spider', 'attack_range': 60, 'damage': 1},
            {'x': 1000, 'y': GAME_HEIGHT - 90 - 60, 'width': 70, 'height': 50, 'type': 'wild_boar', 'attack_range': 90, 'damage': 2},
            {'x': 1400, 'y': GAME_HEIGHT - 250 - 60, 'width': 50, 'height': 50, 'type': 'angry_bird', 'attack_range': 100, 'damage': 1} # On platform
        ],
        'transitions': [
            {
                'type': 'player_at_location',
                'rect_coords': (1, GAME_HEIGHT - 140, 40, 120), # Left exit to Cave Path
                'target_scene_id': SCENE_ID_SCENE2
            },
            {
                'type': 'player_at_location',# game_height = 600, so GAME_HEIGHT - 160 = 440
                'rect_coords': (1800 - 60, GAME_HEIGHT - 160, 50, 140), # Right exit to Scene 4
                'target_scene_id': SCENE_ID_SCENE4
            }
        ]
    },
    {
        'id': SCENE_ID_SCENE4, # New Scene 4: Mountain Ascent
        'player_start_pos': (80, GAME_HEIGHT + 200 - 60 - 50), # Start at bottom of a taller scene
        'background_key': 'mountain_bg', # Create 'mountain_bg.png'
        'world_dimensions': (GAME_WIDTH, GAME_HEIGHT + 200), # Taller scene
        'platform_definitions': [
            # Ground level
            (0, GAME_HEIGHT + 200 - 60, GAME_WIDTH, 60, 'floor2_img', False), # Mountain base (use 'rock_floor_img')
            # Ascending platforms
            (200, GAME_HEIGHT + 200 - 180, 150, 20, 'platform_img', False), # Cliff edge
            (50, GAME_HEIGHT + 200 - 300, 120, 20, 'platform_img', False),  # Higher cliff
            (300, GAME_HEIGHT + 200 - 420, 180, 20, 'platform_img', False), # Even higher
            (GAME_WIDTH - 200, GAME_HEIGHT + 200 - 550, 150, 20, 'platform_img', False), # Top platform for transition
            (-10, 0, 10, GAME_HEIGHT + 200, 'wall_img', True),
            (GAME_WIDTH, 0, 10, GAME_HEIGHT + 200, 'wall_img', True),
        ],
        'npc_definitions': [
            { # NPC for Scene 4 is 'hornhead'# game_height = 600, so GAME_HEIGHT + 200 - 60 = 640, game_width = 1200,so GAME_WIDTH - 300 = 900
                'name': 'hornhead', 'x': 800, 'y': 690, # Adjust y for Hornhead's height
                'width': 70, 'height': 90, 'image_key': 'hornhead_img', # Create 'hornhead_img.png'
                'on_interaction_end': {
                'set_story_flag': 'hornhead_first_talk_done'
                }
            }    
        ],
        'enemy_definitions': [
            {'x': 400, 'y': GAME_HEIGHT + 200 - 60 - 60, 'width': 60, 'height': 60, 'type': 'mountain_goat', 'attack_range': 70, 'damage': 1},
            {'x': 100, 'y': GAME_HEIGHT + 200 - 300 - 60, 'width': 80, 'height': 80, 'type': 'eagle', 'attack_range': 150, 'damage': 2}, # Flying enemy, on platform
        ],
        'transitions': [
            {
                'type': 'player_at_location',
                'rect_coords': (1, GAME_HEIGHT + 200 - 110, 40, 90), # Left exit (bottom) to Forest Path
                'target_scene_id': SCENE_ID_SCENE3
            },
            { # Transition to Scene 5 - could be at the top
                'type': 'player_at_location',
                #parameters is ( x, y, width, height) so GAME_WIDTH - 200 = 1000, GAME_HEIGHT + 200 - 600 = 200
                'rect_coords': (1160, 690, 150, 40), # On the top platform
                'target_scene_id': SCENE_ID_SCENE5
            }
        ]
    },
    {
        'id': SCENE_ID_SCENE5, # New Scene 5: Ancient Ruins
        'player_start_pos': (GAME_WIDTH // 2, GAME_HEIGHT - 100 - 50), # Start in middle of ruins
        'background_key': 'ruins_bg', # Create 'ruins_bg.png'
        'world_dimensions': (2000, GAME_HEIGHT), # Very wide scene
        'platform_definitions': [
            (0, GAME_HEIGHT - 100, 2000, 100, 'floor1_img', False), # Ruined ground (use 'broken_stone_floor_img')
            (150, GAME_HEIGHT - 200, 200, 30, 'platform_img', False), # Fallen pillar
            (500, GAME_HEIGHT - 250, 100, 150, 'wall_img', False), # Standing broken wall (platform on top)
            (480, GAME_HEIGHT - 250 - 20, 140, 20, 'platform_img', False), # Top of broken wall
            (900, GAME_HEIGHT - 180, 300, 25, 'platform_img', False), # Long broken bridge section
            (1500, GAME_HEIGHT - 300, 150, 20, 'platform_img', False), # High ledge
            (-10, 0, 10, GAME_HEIGHT, 'wall_img', True),
            (2000, 0, 10, GAME_HEIGHT, 'wall_img', True),
        ],
        'npc_definitions': [
            { # Add a new NPC type, e.g., 'guardian_spirit'
                'name': 'witcher', 'x': 1600, 'y': GAME_HEIGHT - 100 - 80, 
                'width': 60, 'height': 80, 'image_key': 'witcher_img', 
            }
        ],
        'enemy_definitions': [
            {'x': 250, 'y': GAME_HEIGHT - 100 - 60, 'width': 70, 'height': 70, 'type': 'stone_golem', 'attack_range': 50, 'damage': 2},
            {'x': 1000, 'y': GAME_HEIGHT - 100 - 60, 'width': 50, 'height': 50, 'type': 'lost_soul', 'attack_range': 100, 'damage': 1},
            {'x': 500, 'y': GAME_HEIGHT - 250 - 20 - 60, 'width': 60, 'height': 60, 'type': 'ruin_守卫者', 'attack_range': 80, 'damage': 1} # On broken wall
        ],
        'transitions': [
            { # Example: A way back to Scene 4 (could be a specific portal or left exit)
                'type': 'player_at_location',
                'rect_coords': (1, GAME_HEIGHT - 150, 40, 130), # Left exit
                'target_scene_id': SCENE_ID_SCENE4
            }
            # You might add a "final" trigger or a loop back to an earlier scene
        ]
    }
]
