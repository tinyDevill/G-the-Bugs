# scene_config.py

# Define Scene IDs as constants for easier reference and less typos
SCENE_ID_SHRINE_START = 'shrine_start'
SCENE_ID_SHRINE_AFTER_TRUTHSEEKER_TALK = 'shrine_after_truthseeker_talk' # Example
SCENE_ID_CAVE_PATH_ENTRY = 'cave_path_entry'
# Add more scene IDs as needed

# Define screen dimensions here if needed for coordinates, or get from game instance
# For simplicity, we'll use absolute coordinates assuming a known game height (e.g., 600)
GAME_HEIGHT = 600
GAME_WIDTH = 1200 # Assuming the main game width for now

SCENES_DATA = [
    {
        'id': SCENE_ID_SHRINE_START,
        'player_start_pos': (50, GAME_HEIGHT - 300),
        'background_key': 'main_bg', # Key from Game.background_image_assets
        'world_dimensions': (GAME_WIDTH, GAME_HEIGHT), # Tuple (width, height)
        'platform_definitions': [ # (x, y, w, h, image_key, is_wall)
            (0, GAME_HEIGHT - 50, GAME_WIDTH, 50, 'floor1_img', False),
            (0, 400, 400, 200, 'floor2_img', False),
            (500, 450, 150, 20, 'platform_img', False),
            (800, 400, 150, 20, 'platform_img', False),
            (125, 330, 30, 80, 'benchside2_1_img', False),
            (155, 370, 60, 40, 'benchbottom_img', False),
            (215, 330, 30, 80, 'benchside2_2_img', False),
            (0, 0, 10, GAME_HEIGHT, 'wall_img', True),
            (GAME_WIDTH - 10, 0, 10, GAME_HEIGHT, 'wall_img', True)
        ],
        'npc_definitions': [
            {
                'name': 'truth_seeker', 'x': 300, 'y': GAME_HEIGHT - 200 - 70, # y is top
                'width': 50, 'height': 70, 'image_key': 'truth_seeker',
                'on_interaction_end': {
                    'set_story_flag': 'truth_seeker_initial_talk_done',
                }
            }
        ],
        'enemy_definitions': [
            {'x': 890, 'y': (GAME_HEIGHT - 200 - 60), 'width': 60, 'height': 60, 'type': 'default_enemy'}, # Adjusted y to be on the floor (400-60)
            {'x': 590, 'y': (GAME_HEIGHT - 200 - 60), 'width': 60, 'height': 60, 'type': 'default_enemy'}  # Adjusted y to be on the floor (400-60)
        ],
        'transitions': [
            {
                'type': 'player_at_location_and_flag', # We'll check an additional condition in game.py
                'rect_coords': (GAME_WIDTH - 50, GAME_HEIGHT - 100, 40, 80), # This is (1150, 500, 40, 80)
                'required_story_flag': 'truth_seeker_initial_talk_done', # Condition: Player interacted with NPC
                'must_all_enemies_be_slain': True, # New Condition: All enemies must be slain
                'target_scene_id': SCENE_ID_CAVE_PATH_ENTRY # The scene to change to
            }
            # You might have other transitions here, e.g., one that doesn't require enemies slain but different flags
        ]
    },
    {
        'id': SCENE_ID_CAVE_PATH_ENTRY,
        'player_start_pos': (50, GAME_HEIGHT - 70 - 50), # Player height = 50
        'background_key': 'cave_bg',
        'world_dimensions': (1600, GAME_HEIGHT), # A wider cave area
        'platform_definitions': [
            (0, GAME_HEIGHT - 70, 1600, 70, 'floor1_img', False), # Wider floor
            (300, GAME_HEIGHT - 150, 200, 20, 'platform_img', False),
            (600, GAME_HEIGHT - 250, 150, 20, 'platform_img', False),
            (0, 0, 10, GAME_HEIGHT, 'wall_img', True), # Left wall
            (1600 - 10, 0, 10, GAME_HEIGHT, 'wall_img', True), # Right wall
        ],
        'npc_definitions': [
            {
                'name': 'steelsoul', 'x': 700, 'y': GAME_HEIGHT - 70 - 70,
                'width': 50, 'height': 70, 'image_key': 'steelsoul',
            },
        ],
        'enemy_definitions': [
            {'x': 610, 'y': 400, 'width': 60, 'height': 60, 'type': 'cave_enemy_1'},
            {'x': 910, 'y': 350, 'width': 60, 'height': 60, 'type': 'cave_enemy_2'}
        ],
        'transitions': [
            {
                'type': 'player_at_location',
                'rect_coords': (10, GAME_HEIGHT - 120, 40, 80), # Exit on the left to go back
                'target_scene_id': SCENE_ID_SHRINE_START
            },
        ]
    },
]
