# scene_config.py

# Define Scene IDs as constants
SCENE_ID_SHRINE_START = 'shrine_start'
SCENE_ID_SCENE2 = 'cave_path_entry'
SCENE_ID_SCENE3 = 'scene3'
SCENE_ID_SCENE4 = 'scene4'
SCENE_ID_SCENE5 = 'scene5'

GAME_HEIGHT = 600
GAME_WIDTH = 1200
PLAYER_HEIGHT = 50 # Assuming player height is 50 for y-calculations

SCENES_DATA = [
    {
        'id': SCENE_ID_SHRINE_START,
        'player_start_pos': (50, 200), 
        'background_key': 'main_bg',
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
                'target_scene_id': SCENE_ID_SCENE2,
                # Player will start at SCENE_ID_SCENE2's default player_start_pos
            }
        ]
    },
    {
        'id': SCENE_ID_SCENE2, # Cave Path Entry
        'player_start_pos': (50, GAME_HEIGHT - 70 - PLAYER_HEIGHT),
        'background_key': 'cave_bg',
        'world_dimensions': (1600, GAME_HEIGHT),
        'platform_definitions': [
            (0, GAME_HEIGHT - 70, 1600, 70, 'floor1_img', False),
            (300, GAME_HEIGHT - 150, 200, 20, 'platform_img', False),
            (600, GAME_HEIGHT - 250, 150, 20, 'platform_img', False),
            (900, GAME_HEIGHT - 200, 200, 20, 'platform_img', False),
            (-10, 0, 10, GAME_HEIGHT, 'wall_img', True),
            (1600, 0, 10, GAME_HEIGHT, 'wall_img', True),
        ],
        'npc_definitions': [
            {
                'name': 'steelsoul', 'x': 700, 'y': GAME_HEIGHT - 70 - 70,
                'width': 50, 'height': 70, 'image_key': 'steelsoul',
            }
        ],
        'enemy_definitions': [
            {'id': 'cave_crawler_1', 'x': 450, 'y': GAME_HEIGHT - 70 - 60, 'width': 60, 'height': 60, 'type': 'cave_crawler', 'attack_range': 10, 'damage': 1},
            {'id': 'cave_bat_1', 'x': 1000, 'y': GAME_HEIGHT - 200 - 60, 'width': 60, 'height': 60, 'type': 'cave_bat', 'attack_range': 10, 'damage': 1}
        ],
        'transitions': [
            {
                'type': 'player_at_location',
                'rect_coords': (10, GAME_HEIGHT - 120, 40, 100), # Adjusted rect_coords slightly from 1
                'target_scene_id': SCENE_ID_SHRINE_START,
                'target_player_pos': (1100, 420) # Specific position for player in target scene
            },
            {
                'type': 'player_at_location',
                'rect_coords': (1600 - 60, GAME_HEIGHT - 140, 50, 120),
                'target_scene_id': SCENE_ID_SCENE3,
                # Player starts at Scene 3's default player_start_pos
            }
        ]
    },
    {
        'id': SCENE_ID_SCENE3, # Forest Path
        'player_start_pos': (50, GAME_HEIGHT - 90 - PLAYER_HEIGHT),
        'background_key': 'forest_bg',
        'world_dimensions': (1800, GAME_HEIGHT),
        'platform_definitions': [
            (0, GAME_HEIGHT - 90, 1800, 90, 'floor1_img', False),
            (200, GAME_HEIGHT - 180, 150, 20, 'platform_img', False),
            (500, GAME_HEIGHT - 220, 200, 20, 'platform_img', False),
            (900, GAME_HEIGHT - 150, 100, 20, 'platform_img', False),
            (1300, GAME_HEIGHT - 250, 250, 20, 'platform_img', False),
            (-10, 0, 10, GAME_HEIGHT, 'wall_img', True),
            (1800, 0, 10, GAME_HEIGHT, 'wall_img', True),
        ],
        'npc_definitions': [
            {
                'name': 'noze', 'x': 800, 'y': GAME_HEIGHT - 90 - 70,
                'width': 50, 'height': 70, 'image_key': 'noze_img',
            }
        ],
        'enemy_definitions': [
            {'id': 'forest_spider_1', 'x': 300, 'y': GAME_HEIGHT - 90 - 60, 'width': 60, 'height': 60, 'type': 'forest_spider', 'attack_range': 10, 'damage': 1},
            {'id': 'forest_boar_1', 'x': 1000, 'y': GAME_HEIGHT - 90 - 60, 'width': 70, 'height': 50, 'type': 'wild_boar', 'attack_range': 10, 'damage': 1},
            {'id': 'forest_bird_1', 'x': 1400, 'y': GAME_HEIGHT - 250 - 60, 'width': 50, 'height': 50, 'type': 'angry_bird', 'attack_range': 10, 'damage': 1}
        ],
        'transitions': [
            {
                'type': 'player_at_location',
                'rect_coords': (10, GAME_HEIGHT - 140, 40, 120), # Left exit to Cave Path
                'target_scene_id': SCENE_ID_SCENE2,
                'target_player_pos': (1500, GAME_HEIGHT - 70 - PLAYER_HEIGHT) # Appear at right side of Scene 2
            },
            {
                'type': 'player_at_location',
                'rect_coords': (1800 - 60, GAME_HEIGHT - 160, 50, 140), # Right exit to Scene 4
                'target_scene_id': SCENE_ID_SCENE4,
                # Player starts at Scene 4's default player_start_pos
            }
        ]
    },
    {
        'id': SCENE_ID_SCENE4, # Mountain Ascent
        'player_start_pos': (80, GAME_HEIGHT + 200 - 60 - PLAYER_HEIGHT), # Base of mountain
        'background_key': 'mountain_bg',
        'world_dimensions': (GAME_WIDTH, GAME_HEIGHT + 200), # Taller scene
        'platform_definitions': [
            (0, GAME_HEIGHT + 200 - 60, GAME_WIDTH, 60, 'floor2_img', False),
            (200, GAME_HEIGHT + 200 - 180, 150, 20, 'platform_img', False),
            (50, GAME_HEIGHT + 200 - 300, 120, 20, 'platform_img', False),
            (300, GAME_HEIGHT + 200 - 420, 180, 20, 'platform_img', False),
            (GAME_WIDTH - 200, GAME_HEIGHT + 200 - 550, 150, 20, 'platform_img', False), # Top platform
            (-10, 0, 10, GAME_HEIGHT + 200, 'wall_img', True),
            (GAME_WIDTH, 0, 10, GAME_HEIGHT + 200, 'wall_img', True),
        ],
        'npc_definitions': [
            {
                'name': 'hornhead', 'x': 800, 'y': GAME_HEIGHT + 200 - 60 - 90, # On the base floor
                'width': 70, 'height': 90, 'image_key': 'hornhead_img',
                'on_interaction_end': {
                    'set_story_flag': 'hornhead_first_talk_done'
                }
            }
        ],
        'enemy_definitions': [
            {'id': 'mountain_goat_1', 'x': 400, 'y': GAME_HEIGHT + 200 - 60 - 60, 'width': 60, 'height': 60, 'type': 'mountain_goat', 'attack_range': 10, 'damage': 1},
            {'id': 'mountain_eagle_1', 'x': 100, 'y': GAME_HEIGHT + 200 - 300 - 60, 'width': 80, 'height': 80, 'type': 'eagle', 'attack_range': 10, 'damage': 1}
        ],
        'transitions': [
            {
                'type': 'player_at_location',
                'rect_coords': (10, GAME_HEIGHT + 200 - 110, 40, 90), # Left exit (bottom) to Forest Path
                'target_scene_id': SCENE_ID_SCENE3,
                'target_player_pos': (1700, GAME_HEIGHT - 90 - PLAYER_HEIGHT) # Appear at right side of Scene 3
            },
            {
                'type': 'player_at_location',
                'rect_coords': (GAME_WIDTH - 200 + 75 - 20, GAME_HEIGHT + 200 - 550 - PLAYER_HEIGHT - 10, 40, PLAYER_HEIGHT + 10), # Trigger on the top platform for exit
                'target_scene_id': SCENE_ID_SCENE5,
                # Player starts at Scene 5's default player_start_pos
            }
        ]
    },
    {
        'id': SCENE_ID_SCENE5, # Ancient Ruins
        'player_start_pos': (100, GAME_HEIGHT - 100 - PLAYER_HEIGHT), # Start left side of ruins
        'background_key': 'ruins_bg',
        'world_dimensions': (2000, GAME_HEIGHT),
        'platform_definitions': [
            (0, GAME_HEIGHT - 100, 2000, 100, 'floor1_img', False),
            (150, GAME_HEIGHT - 200, 200, 30, 'platform_img', False),
            (500, GAME_HEIGHT - 250, 100, 150, 'wall_img', False), # Visually a wall, acts as platform on top
            (480, GAME_HEIGHT - 250 - 20, 140, 20, 'platform_img', False), # Top of broken wall
            (900, GAME_HEIGHT - 180, 300, 25, 'platform_img', False),
            (1500, GAME_HEIGHT - 300, 150, 20, 'platform_img', False),
            (-10, 0, 10, GAME_HEIGHT, 'wall_img', True),
            (2000, 0, 10, GAME_HEIGHT, 'wall_img', True),
        ],
        'npc_definitions': [
            {
                'name': 'witcher', 'x': 1600, 'y': GAME_HEIGHT - 100 - 80,
                'width': 60, 'height': 80, 'image_key': 'witcher_img',
            }
        ],
        'enemy_definitions': [
            {'id': 'ruins_golem_1', 'x': 250, 'y': GAME_HEIGHT - 100 - 70, 'width': 70, 'height': 70, 'type': 'stone_golem', 'attack_range': 10, 'damage': 1},
            {'id': 'ruins_soul_1', 'x': 1000, 'y': GAME_HEIGHT - 100 - 60, 'width': 50, 'height': 50, 'type': 'lost_soul', 'attack_range': 10, 'damage': 1},
            {'id': 'ruins_defender_1', 'x': 500, 'y': GAME_HEIGHT - 250 - 20 - 60, 'width': 60, 'height': 60, 'type': 'ruin_defender', 'attack_range': 10, 'damage': 1}
        ],
        'transitions': [
            {
                'type': 'player_at_location',
                'rect_coords': (10, GAME_HEIGHT - 150, 40, 130), # Left exit to Mountain Ascent
                'target_scene_id': SCENE_ID_SCENE4,
                # Target player position should be where they exited Scene 4 to Scene 5 from
                # Scene 4 transition to Scene 5 was on platform at (GAME_WIDTH - 200, GAME_HEIGHT + 200 - 550)
                # So, y should be GAME_HEIGHT + 200 - 550 - PLAYER_HEIGHT
                'target_player_pos': (GAME_WIDTH - 200 + 50, GAME_HEIGHT + 200 - 550 - PLAYER_HEIGHT)
            }
        ]
    }
]
