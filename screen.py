# screen.py
import pygame

class Camera:
    def __init__(self, width, height, zoom):
        self.rect = pygame.Rect(0, 0, width, height)
        self.zoom = zoom # zoom factor (e.g., 1.0 = no zoom, 2.0 = zoomed in)

    def update(self, target, world_width, world_height):
        if target: # Ensure target exists
            self.rect.center = target.rect.center
        
        # Calculate camera view dimensions based on screen size and zoom
        # Note: self.rect.width/height are the *world units* visible, not screen pixels.
        # If self.rect.width/height were screen pixels, zoom would be applied at draw time.
        # Here, self.rect.width/height are already "zoomed out" world view.

        # Keep the camera within the bounds of the game world.
        self.rect.left = max(0, self.rect.left)
        self.rect.top = max(0, self.rect.top)
        
        if self.rect.right > world_width:
            self.rect.right = world_width
        if self.rect.bottom > world_height:
            self.rect.bottom = world_height
        
        # Prevent camera view from being smaller than 1x1 pixel if possible
        if self.rect.width < 1: self.rect.width = 1
        if self.rect.height < 1: self.rect.height = 1


def load_assets(screen_width_for_scaling, screen_height_for_scaling): # Parameters might be for default scaling
    assets = {}
    try:
        
        start_button_img = pygame.image.load("assets/image/start_button.png").convert_alpha()
        assets['start_button_img'] = pygame.transform.scale(start_button_img, (200, 100))
        exit_button_img = pygame.image.load("assets/image/exit_button.png").convert_alpha()
        assets['exit_button_img'] = pygame.transform.scale(exit_button_img, (200, 100))
        assets['home_screen'] = pygame.image.load("assets/image/home_screen.png").convert_alpha()
        
        assets['main_bg'] = pygame.image.load("assets/image/platform/pl2/bg2.png").convert()
        assets['floor1_img'] = pygame.image.load("assets/image/platform/pl2/floor2_1.png").convert_alpha()
        assets['floor2_img'] = pygame.image.load("assets/image/platform/pl2/floor2_2.png").convert_alpha()
        assets['platform_img'] = pygame.image.load("assets/image/platform/pl2/platform2.png").convert_alpha()
        assets['benchbottom_img'] = pygame.image.load("assets/image/platform/pl2/benchbottom.png").convert_alpha()
        assets['benchside2_1_img'] = pygame.image.load("assets/image/platform/pl2/benchside2_1.png").convert_alpha()
        assets['benchside2_2_img'] = pygame.image.load("assets/image/platform/pl2/benchside2_2.png").convert_alpha()
        assets['wall_img'] = pygame.image.load("assets/image/platform/pl2/wall2_1.png").convert_alpha()
        
        assets['truth_seeker_img'] = pygame.image.load("assets/image/truth_seeker.gif").convert_alpha()
    
        # Load other assets and add them to the dictionary
        assets['steelsoul_img'] = pygame.image.load("assets/image/steelsoul.png").convert_alpha()
        assets['noze_img'] = pygame.image.load("assets/image/noze.png").convert_alpha()
        cave_bg_temp = pygame.image.load("assets/image/platform/pl3/bg3.png").convert()
        assets['cave_bg'] = pygame.transform.scale(cave_bg_temp, (1600, screen_height_for_scaling)) # Example scale
        assets['hornhead_img'] = pygame.image.load("assets/image/Hornhead.png").convert_alpha()  # EXAMPLE PATH
        assets['witcher_img'] = pygame.image.load("assets/image/witcher.png").convert_alpha()    # EXAMPLE PATH


    except pygame.error as e:
        print(f"Error loading an asset in screen.py: {e}")
        # You might want to fill missing assets with placeholder surfaces
        placeholder_surface = pygame.Surface((50,50)); placeholder_surface.fill((255,0,255)) # Magenta
        for key in ['main_bg', 'floor1_img', 'floor2_img', 'platform_img', 'benchbottom_img', 
                    'benchside2_1_img', 'benchside2_2_img', 'wall_img', 'start_button_img', 
                    'exit_button_img', 'truth_seeker_img', 'steelsoul_img', 'noze_img', 'cave_bg']:
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

def draw_objects(screen, player, platforms, npcs, enemies_list, camera_rect, zoom): # Added enemies_list
    for platform in platforms:
        platform.draw(screen, camera_rect, zoom)
    
    for npc in npcs: # NPCs are already filtered by scene loading
        if npc.active: 
            npc.draw(screen, camera_rect, zoom)

    for enemy in enemies_list: # Draw all enemies from the list
        if enemy.alive:
            enemy.draw(screen, camera_rect, zoom)

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
