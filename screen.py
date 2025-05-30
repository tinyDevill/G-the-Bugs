# screen.py
import pygame

class Camera:
    def __init__(self, width, height, zoom):
        self.rect = pygame.Rect(0, 0, width, height)
        self.zoom = zoom 

    def update(self, target, world_width, world_height):
        if target: 
            self.rect.center = target.rect.center
        
        self.rect.left = max(0, self.rect.left)
        self.rect.top = max(0, self.rect.top)
        
        if self.rect.right > world_width:
            self.rect.right = world_width
        if self.rect.bottom > world_height:
            self.rect.bottom = world_height
        
        if self.rect.width < 1: self.rect.width = 1
        if self.rect.height < 1: self.rect.height = 1


def load_assets(screen_width_for_scaling, screen_height_for_scaling):
    assets = {}
    try:
        assets['start_button_img'] = pygame.transform.scale(pygame.image.load("assets/image/start_button.png").convert_alpha(), (200, 100))
        assets['exit_button_img'] = pygame.transform.scale(pygame.image.load("assets/image/exit_button.png").convert_alpha(), (200, 100))
        assets['home_screen'] = pygame.image.load("assets/image/home_screen.png").convert_alpha()
        
        # Scene 1 Assets
        assets['bg1'] = pygame.image.load("assets/image/platform/pl1/bg1.png").convert() # Assuming pl1 is your scene1 folder
        assets['floor1_1'] = pygame.image.load("assets/image/platform/pl1/floor1_1.png").convert_alpha()
        assets['floor1_2'] = pygame.image.load("assets/image/platform/pl1/floor1_2.png").convert_alpha()
        assets['floor1_3'] = pygame.image.load("assets/image/platform/pl1/floor1_3.png").convert_alpha() # Corrected key
        assets['floor1_4'] = pygame.image.load("assets/image/platform/pl1/floor1_4.png").convert_alpha()
        assets['wall1'] = pygame.image.load("assets/image/platform/pl1/wall1.png").convert_alpha() # Assuming wall1 is the left wall
        assets['truth_seeker_img'] = pygame.image.load("assets/image/truth_seeker.gif").convert_alpha() # Corrected path assuming .gif

        # Scene 2 Assets (already partially there, consolidated)
        assets['second_bg'] = pygame.image.load("assets/image/platform/pl2/bg2.png").convert() # Renamed from main_bg potentially
        assets['floor1_img'] = pygame.image.load("assets/image/platform/pl2/floor2_1.png").convert_alpha() # This was your 'floor1_img' for scene 2
        assets['floor2_img'] = pygame.image.load("assets/image/platform/pl2/floor2_2.png").convert_alpha()
        assets['platform_img'] = pygame.image.load("assets/image/platform/pl2/platform2.png").convert_alpha()
        assets['benchbottom_img'] = pygame.image.load("assets/image/platform/pl2/benchbottom.png").convert_alpha()
        assets['benchside2_1_img'] = pygame.image.load("assets/image/platform/pl2/benchside2_1.png").convert_alpha()
        assets['benchside2_2_img'] = pygame.image.load("assets/image/platform/pl2/benchside2_2.png").convert_alpha()
        assets['wall_img'] = pygame.image.load("assets/image/platform/pl2/wall2_1.png").convert_alpha()   
        assets['steelsoul_img'] = pygame.image.load("assets/image/steelsoul.png").convert_alpha() # Assuming steelsoul is a character or item in scene 2

        # Scene 3 Assets
        assets['bg3'] = pygame.transform.scale(pygame.image.load("assets/image/platform/pl3/bg3.png").convert(), (1600, screen_height_for_scaling))
        assets['floor3_1'] = pygame.image.load("assets/image/platform/pl3/floor3_1.png").convert_alpha()
        assets['floor3_2'] = pygame.image.load("assets/image/platform/pl3/floor3_2.png").convert_alpha()
        assets['upfloor3_1'] = pygame.image.load("assets/image/platform/pl3/upfloor3_1.png").convert_alpha()
        assets['upfloor3_2'] = pygame.image.load("assets/image/platform/pl3/upfloor3_2.png").convert_alpha()
        assets['upfloor3_3'] = pygame.image.load("assets/image/platform/pl3/upfloor3_3.png").convert_alpha()
        assets['upfloor3_4'] = pygame.image.load("assets/image/platform/pl3/upfloor3_4.png").convert_alpha()
        assets['upfloor3_5'] = pygame.image.load("assets/image/platform/pl3/upfloor3_5.png").convert_alpha()
        assets['upfloor3_6'] = pygame.image.load("assets/image/platform/pl3/upfloor3_6.png").convert_alpha()
        assets['floatfloor3'] = pygame.image.load("assets/image/platform/pl3/floatfloor3.png").convert_alpha()
        assets['wall3'] = pygame.image.load("assets/image/platform/pl3/wall3.png").convert_alpha()
        assets['noze_img'] = pygame.image.load("assets/image/noze.png").convert_alpha()
        
        # Scene 4 Assets
        assets['bg4'] = pygame.image.load("assets/image/platform/pl4/bg4.png").convert()
        assets['floor4_1'] = pygame.image.load("assets/image/platform/pl4/floor4_1.png").convert_alpha()
        assets['floor4_2'] = pygame.image.load("assets/image/platform/pl4/floor4_2.png").convert_alpha()
        assets['floor4_3'] = pygame.image.load("assets/image/platform/pl4/floor4_3.png").convert_alpha()
        assets['wall4_1'] = pygame.image.load("assets/image/platform/pl4/wall4_1.png").convert_alpha()
        assets['wall4_2'] = pygame.image.load("assets/image/platform/pl4/wall4_2.png").convert_alpha()
        assets['hornhead_img'] = pygame.image.load("assets/image/Hornhead.png").convert_alpha() 

        # Scene 5 Assets
        assets['bg5'] = pygame.image.load("assets/image/platform/pl5/bg5.png").convert()
        assets['floor5_1'] = pygame.image.load("assets/image/platform/pl5/floor5_1.png").convert_alpha()
        assets['floor5_2'] = pygame.image.load("assets/image/platform/pl5/floor5_2.png").convert_alpha()
        assets['wall5_1'] = pygame.image.load("assets/image/platform/pl5/wall5_1.png").convert_alpha()
        assets['wall5_2'] = pygame.image.load("assets/image/platform/pl5/wall5_2.png").convert_alpha()

        # Witcher Assets
        assets['witcher_img'] = pygame.image.load("assets/image/boss1.png").convert_alpha()
        assets['witcher2_img'] = pygame.image.load("assets/image/boss2.png").convert_alpha() # New Witcher frame
        assets['bullet_img'] = pygame.image.load("assets/image/bullet.png").convert_alpha()   # New Bullet

        # General Backgrounds (if still used or as fallbacks) - some might be redundant now
        assets['main_bg'] = assets.get('second_bg') # Default main_bg to scene 2 bg for now
        # assets['forest_bg'] = pygame.image.load("assets/image/platform/forest_bg.png").convert_alpha() # Example path
        # assets['mountain_bg'] = pygame.image.load("assets/image/platform/mountain_bg.png").convert_alpha() # Example path
        # assets['ruins_bg'] = pygame.image.load("assets/image/platform/ruins_bg.png").convert_alpha() # Example path


    except pygame.error as e:
        print(f"Error loading an asset in screen.py: {e}")
    
    placeholder_surface = pygame.Surface((50,50)); placeholder_surface.fill((255,0,255)) # Magenta
    keys_to_check = [
        'start_button_img', 'exit_button_img', 'home_screen',
        'bg1', 'floor1_1', 'floor1_2', 'floor1_3', 'floor1_4', # scene 1
        'second_bg', 'floor1_img', 'floor2_img', 'platform_img', # scene 2 (using existing names)
        'benchbottom_img', 'benchside2_1_img', 'benchside2_2_img', 'wall_img',
        'truth_seeker_img', 'steelsoul_img', 'noze_img', 'hornhead_img', 
        'bg3', 'floor3_1', 'floor3_2', 'upfloor3_1', 'upfloor3_2', 'upfloor3_3', 'upfloor3_4', # scene 3
        'upfloor3_5', 'upfloor3_6', 'floatfloor3', 'wall3',
        'bg4', 'floor4_1', 'floor4_2', 'floor4_3', 'wall4_1', 'wall4_2', # scene 4
        'bg5', 'floor5_1', 'floor5_2', 'wall5_1', 'wall5_2', # scene 5
        'witcher_img', 'witcher2_img', 'bullet_img', # witcher
        'main_bg', 'forest_bg', 'mountain_bg', 'ruins_bg' # general backgrounds
    ]
    for key in keys_to_check:
        if key not in assets:
            assets[key] = placeholder_surface
            print(f"Using placeholder for missing asset: {key}")
    return assets

def draw_background_scaled_with_camera(screen, background_surface, camera_world_view_rect, screen_render_width, screen_render_height):
    """
    Draws a portion of the background_surface, defined by camera_world_view_rect,
    and scales it to fill the screen. This makes the background zoom visually
    consistent with other game objects affected by the camera's zoom.
    """
    if not background_surface:
        screen.fill((10,10,10)) # Dark fallback
        return

    # camera_world_view_rect is the rectangle (in world coordinates) that the camera sees.
    # Its width/height are typically screen_dimension / game_zoom.

    # Clamp the view rectangle to be within the bounds of the background_surface
    # to prevent subsurface errors.
    clamped_view_rect = camera_world_view_rect.copy()
    clamped_view_rect.left = max(0, clamped_view_rect.left)
    clamped_view_rect.top = max(0, clamped_view_rect.top)
    
    # Adjust width/height if clamping moved left/top or if view goes beyond right/bottom
    if clamped_view_rect.right > background_surface.get_width():
        clamped_view_rect.width = background_surface.get_width() - clamped_view_rect.left
    if clamped_view_rect.bottom > background_surface.get_height():
        clamped_view_rect.height = background_surface.get_height() - clamped_view_rect.top

    if clamped_view_rect.width <= 0 or clamped_view_rect.height <= 0:
        # Clamped view is invalid or has no area
        return

    try:
        # Take the subsurface corresponding to what the camera sees in the world
        bg_sub_view = background_surface.subsurface(clamped_view_rect)
        
        # Scale this subsurface up to the full screen dimensions
        bg_view_scaled_to_screen = pygame.transform.scale(bg_sub_view, (screen_render_width, screen_render_height))
        
        screen.blit(bg_view_scaled_to_screen, (0, 0))
    except ValueError as e:
        # This can happen if clamping logic is imperfect or rect dimensions are problematic
        print(f"Error creating subsurface for background: {e}")
        print(f"  Background size: {background_surface.get_size()}")
        print(f"  Original camera_world_view_rect: {camera_world_view_rect}")
        print(f"  Clamped_view_rect: {clamped_view_rect}")
        # screen.fill((25,0,0)) # Fallback color to indicate an error

def draw_objects(screen, player, platforms, npcs, enemies_list, projectiles_list, camera_rect, zoom): # Added projectiles_list
    for platform in platforms:
        platform.draw(screen, camera_rect, zoom)
    
    for npc_instance in npcs: 
        if npc_instance.active: 
            npc_instance.draw(screen, camera_rect, zoom)

    for enemy in enemies_list: 
        if enemy.alive:
            enemy.draw(screen, camera_rect, zoom)

    for projectile in projectiles_list: # DRAW PROJECTILES
        if projectile.alive:
            projectile.draw(screen, camera_rect, zoom)

    if player and player.alive:
        player.draw(screen, camera_rect, zoom)
 

def draw_darkness_with_light(screen, player, camera_rect, zoom, light_radius=120):
    if not player: return
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180)) 

    player_screen_pos = (
        int((player.rect.centerx - camera_rect.x) * zoom),
        int((player.rect.centery - camera_rect.y) * zoom)
    )
    # Ensure radius is positive
    actual_radius = max(1, int(light_radius))
    pygame.draw.circle(overlay, (0, 0, 0, 0), player_screen_pos, actual_radius) # Transparent circle
    screen.blit(overlay, (0, 0))


def draw_text(surface, text, font, color, rect, aa=True, bkg=None): # Keep your text wrapper
    y = rect.top
    line_spacing = -2
    font_height = font.size("Tg")[1]
    while text:
        i = 1
        if y + font_height > rect.bottom: break
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1
        if i < len(text): i = text.rfind(" ", 0, i) + 1
        
        image = font.render(text[:i], aa, color, bkg)
        if bkg: image.set_colorkey(bkg)
        
        surface.blit(image, (rect.left, y))
        y += font_height + line_spacing
        text = text[i:]
    return text
