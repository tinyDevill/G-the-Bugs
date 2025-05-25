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
                # 'initial_dialog_key': 'intro' # NPC decides its dialog based on game story_flags
                # Define what happens after interacting with this NPC in this scene
                'on_interaction_end': { # Optional: actions after any dialog sequence with this NPC ends
                    'set_story_flag': 'truth_seeker_initial_talk_done', # Example: Game sets this flag
                    # 'next_scene_if_flag_is_also_set': {'flag':'some_other_flag', 'scene_id': SCENE_ID_CAVE_PATH_ENTRY}
                }
            }
        ],
        'enemy_definitions': [
            {'x': 800, 'y': (400 - 60), 'width': 60, 'height': 60, 'type': 'default_enemy'}
        ],
        'transitions': [ # How to exit this scene
            {
                'type': 'player_at_location_and_flag',
                'rect_coords': (GAME_WIDTH - 50, GAME_HEIGHT - 100, 40, 80), # x,y,w,h for exit zone
                'required_story_flag': 'truth_seeker_quest_accepted', # Can only exit if this flag is true
                'target_scene_id': SCENE_ID_CAVE_PATH_ENTRY
            }
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
                # This NPC might react to flags set by Truth Seeker, or have its own simple dialog.
            },
            # Example: Noze appears only if a certain flag is set
            # This conditional appearance is handled in Game.load_scene by checking story_flags
            # before deciding to instantiate an NPC from npc_definitions.
            # Alternatively, npc_definitions itself could have a 'required_flag_to_appear'.
        ],
        'enemy_definitions': [
            {'x': 400, 'y': GAME_HEIGHT - 70 - 60, 'width': 60, 'height': 60, 'type': 'cave_enemy_1'},
            {'x': 800, 'y': GAME_HEIGHT - 70 - 60, 'width': 60, 'height': 60, 'type': 'cave_enemy_2'}
        ],
        'transitions': [
            {
                'type': 'player_at_location',
                'rect_coords': (10, GAME_HEIGHT - 120, 40, 80), # Exit on the left to go back
                'target_scene_id': SCENE_ID_SHRINE_START
            },
            # Add more transitions, e.g., deeper into the caves
        ]
    },
    # Add more scenes...
]