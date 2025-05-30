# scene_config.py

# Define Scene IDs
SCENE_ID_SCENE1 = 'scene1'
SCENE_ID_SCENE2 = 'scene2'
SCENE_ID_SCENE3 = 'scene3'
SCENE_ID_SCENE4 = 'scene4'
SCENE_ID_SCENE5 = 'scene5' # Witcher's scene (and final boss)

# Default start scene (can be overridden in game.py if needed, but good to have a constant)
SCENE_ID_SHRINE_START = SCENE_ID_SCENE1 # Let's make scene1 the starting scene

GAME_WIDTH = 1200
GAME_HEIGHT = 600
# Define the scene data structure
SCENES_DATA = [
    {
        "id": SCENE_ID_SCENE1,
        "background_key": "bg1",
        "world_dimensions": (1200, 600), # Width, Height of the scene world
        "player_start_pos": (100, 90),
        "platform_definitions": [
            # x,  y,   w,   h,  image_key, is_wall
            (0, 160, 670, 500, 'floor1_1', False),
            (663, 110, 340, 100, 'floor1_2', False),
            (663, 212, 280, 59, 'floor1_3', False), # Slightly raised
            (663, 357, 580, 280, 'floor1_4', False),
            (0, 0, 50, 150, 'wall1', True),        # Left boundary wall
        ],
        "npc_definitions": [
            {   "x": 350, "y": 95, "width": 50, "height": 70, "name": "truth_seeker", "image_key": "truth_seeker",
                'on_interaction_end': {
                'set_story_flag': 'truth_seeker_initial_talk_done',
                }
            },
        ],
        "enemy_definitions": [
            # Example enemy
            {"id": "s1_enemy1", "x": 900, "y": 50, "width": 40, "height": 40, "type": "default_enemy", "attack_range": 10, "damage": 1},
            {"id": "s1_enemy2", "x": 900, "y": 305, "width": 40, "height": 40, "type": "default_enemy", "attack_range": 10, "damage": 1}
        ],
        "transitions": [
            {"type": "player_at_location", "rect_coords": (1190, 307, 10, 20), "target_scene_id": SCENE_ID_SCENE2, "target_player_pos": (600, 00)}
        ]
    },
    {
        "id": SCENE_ID_SCENE2,
        'player_start_pos': (50, 100), 
        'background_key': 'second_bg',
        'world_dimensions': (GAME_WIDTH, GAME_HEIGHT),
        'platform_definitions': [
            (0, GAME_HEIGHT - 200, 402, 200, 'floor2_img', False),
            (395, 520, 810, 90, 'floor1_img', False),
            (125, GAME_HEIGHT - 270, 30, 80, 'benchside2_1_img', False),
            (155, GAME_HEIGHT - 230, 60, 40, 'benchbottom_img', False),
            (215, GAME_HEIGHT - 270, 30, 80, 'benchside2_2_img', False),
            (-10, 0, 10, GAME_HEIGHT, 'wall_img', True),
            (GAME_WIDTH, 0, 10, GAME_HEIGHT, 'wall_img', True)
        ],
        'npc_definitions': [
            {
                'name': 'truth_seeker', 'x': 300, 'y': 330,
                'width': 50, 'height': 70, 'image_key': 'truth_seeker',
                'on_interaction_end': {
                    'set_story_flag': 'truth_seeker_initial_talk_done',
                }
            }
        ],
        'enemy_definitions': [
            {'id': 'shrine_enemy_floor_1', 'x': 890, 'y': GAME_HEIGHT - 80 - 60, 'width': 60, 'height': 60, 'type': 'default_enemy', 'attack_range': 10, 'damage': 1},
            {'id': 'shrine_enemy_platform_1', 'x': 500, 'y': GAME_HEIGHT - 200 - 60, 'width': 60, 'height': 60, 'type': 'default_enemy', 'attack_range': 10, 'damage': 1}
        ],
        'transitions': [
            {
                'type': 'player_at_location_and_flag',
                'rect_coords': (GAME_WIDTH - 60, GAME_HEIGHT - 180, 50, 160), # x = 1140, y = 420
                'required_story_flag': 'truth_seeker_initial_talk_done',
                'must_all_enemies_be_slain': True,
                "target_scene_id": SCENE_ID_SCENE3, 
                "target_player_pos": (0, 50)
            },
            {"type": "player_at_location", "rect_coords": (0, 0, 20, 700), "target_scene_id": SCENE_ID_SCENE1, "target_player_pos": (1530, 450)}
            
        ]
    },
    {
        "id": SCENE_ID_SCENE3,
        "background_key": "bg3",
        "world_dimensions": (1200, 600),
        "player_start_pos": (100, 50),
        "platform_definitions": [
            (0, 570, 1205, 50, 'floor3_1', False),
            (940, 495, 400, 200, 'floor3_2', False),
            (0, 400, 712, 85, 'upfloor3_1', False),
            (0, 315, 520, 85, 'upfloor3_2', False),
            (0, 240, 720, 60, 'upfloor3_3', False),
            (0, 195, 520, 50, 'upfloor3_4', False),
            (0, 145, 340, 40, 'upfloor3_5', False),
            (0, 100, 200, 50, 'upfloor3_6', False),
            (860, 315, 260, 80, 'floatfloor3', False), # High floating platform
            # (0, 0, 50, 750, 'wall3', True),           # Left boundary wall
            (2150, 0, 50, 750, 'wall3', True),        # Right boundary wall
            (1700, 600, 150, 30, 'upfloor3_1', False), # Another platform
        ],
        "npc_definitions": [
             {"x": 530, "y": 330, "width": 50, "height": 70, "name": "noze", "image_key": "noze_img"},
        ],
        "enemy_definitions": [
            {"id": "s3_enemy1", "x": 600, "y": 180, "width": 60, "height": 60, "type": "cave_dweller"},
            {"id": "s3_enemy2", "x": 180, "y": 510, "width": 60, "height": 60, "type": "cave_dweller"},
            {"id": "s3_enemy_float", "x": 1000, "y": 200, "width": 60, "height": 60, "type": "flyer"} # Enemy on floating platform
        ],
        "transitions": [
            {"type": "player_at_location", "rect_coords": (-30, 50, 20, 20), "target_scene_id": SCENE_ID_SCENE2, "target_player_pos": (1100, 420)},
            {"type": "player_at_location", "rect_coords": (0, 520, 20, 20), "target_scene_id": SCENE_ID_SCENE4, "target_player_pos": (1090, 390)}
        ]
    },
    {
        "id": SCENE_ID_SCENE4,
        "background_key": "bg4",
        "world_dimensions": (1200, 600),
        "player_start_pos": (1090, 390),
        "platform_definitions": [
            (0, 480, 1200, 100, 'floor4_1', False),
            (10, 180, 200, 100, 'floor4_2', False),
            (713, 248, 500, 50, 'floor4_3', False),
            (390, 0, 245, 270, 'wall4_1', False), # middle wall


        ],
        "npc_definitions": [
             {"x": 110, "y": 400, "width": 60, "height": 80, "name": "hornhead", "image_key": "hornhead_img",
              # Example of setting a flag after first interaction with Hornhead
              'on_interaction_end': {'set_story_flag': 'hornhead_first_talk_done', 'if_dialog_key_was': 'first_encounter'}
             },
        ],
        "enemy_definitions": [
            {"id": "s4_enemy1", "x": 874, "y": 420, "width": 60, "height": 60, "type": "heavy_guard"},
            {"id": "s4_enemy2", "x": 500, "y": 420, "width": 60, "height": 60, "type": "heavy_guard"},
        ],
        "transitions": [
            {"type": "player_at_location", "rect_coords": (0, 430, 20, 20), "target_scene_id": SCENE_ID_SCENE5, "target_player_pos": (1130, 510)},
            {"type": "player_at_location", "rect_coords": (1170,    430, 10, 10), "target_scene_id": SCENE_ID_SCENE3, "target_player_pos": (30, 470)}
        ]
    },
    {
        "id": SCENE_ID_SCENE5, # Witcher's Scene / Final Boss Arena
        "background_key": "bg5",
        "world_dimensions": (1200, 600), # More contained arena
        "player_start_pos": (1130, 400),
        "platform_definitions": [
            (0, 400, 800, 150, 'floor5_1', False),
            (800, 500, 500, 50, 'floor5_2', False), # Make it a continuous floor

            (0, 0, 60, 600, 'wall5_1', True),      # Left wall
            (780, 500, 30, 400, 'wall5_2', True),   # Right wall
            # Optional platforms for boss fight dynamics
            # (200, 400, 150, 30, 'platform_img', False), # Using a generic platform asset
            # (1150, 400, 150, 30, 'platform_img', False),
            (675, 300, 150, 30, 'floatfloor3', False), # Central high platform
        ],
        "npc_definitions": [
             # Witcher is an NPC that also acts as a boss.
             # His special behaviors (jumping, projectiles) are handled by WitcherNPC class.
             {"x": 700, "y": 230, "width": 50, "height": 70, "name": "witcher", "image_key": "witcher_img"},
        ],
        "enemy_definitions": [
            # Potentially add some minor enemies or leave it for the Witcher boss fight
        ],
        "transitions": [
            {"type": "player_at_location", "rect_coords": (0, 0, 20, 600), "target_scene_id": SCENE_ID_SCENE4, "target_player_pos": (1930, 580)},
            # Potentially a transition to an "ending scene" if the Witcher is defeated
            # This would require a story flag like "witcher_defeated"
            # {"type": "player_at_location_and_flag", "rect_coords": (700, 0, 100, 100), "required_story_flag": "witcher_defeated", "target_scene_id": "SCENE_ID_ENDING", "target_player_pos": (100,100)}
        ]
    },
]
