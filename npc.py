# npc.py
import pygame

# KEEP YOUR EXISTING DIALOG DICTIONARIES (truth_seeker_dialogs, etc.) HERE
truth_seeker_dialogs = {
    "intro": ["you...", "you have the void in your soul...", "so... finally...", ".. the destiny will be fulfilled."],
    "quest_offer": ["bring me the void heart from the deepest cave...", "only then can the seal be broken."],
    "waiting_for_heart": ["the void heart... have you found it?"],
    "has_heart": ["Ah, the void heart! Give it here... quickly!"],
    "outro": ["It is done... the path is clear... but at what cost?"]
}
steelsoul_dialogs = {"default": ["Ho there, traveler! This cave is treacherous.", "Watch your step."]}
noze_dialogs = {"default": ["Mhehehe... shiny things? Got any for Noze?"]}
lost_knight_dialogs = {"default": ["Lost... so lost... was there ever a purpose?"]}
# ... other dialogs

class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name, base_dialogs, image_surface=None):
        super().__init__()
        self.name = name
        self.rect = pygame.Rect(x, y, width, height)
        self.base_dialogs = base_dialogs # Store all dialog options for this NPC type
        
        if image_surface:
            self.image = pygame.transform.scale(image_surface, (width, height))
        else:
            self.image = pygame.Surface((width, height)); self.image.fill((180, 180, 180))

        self.active = True # NPCs are active by default when loaded in a scene
        self.current_dialog_key = "default" # For tracking which dialog sequence was just completed

    def interact(self, player_data, story_flags_from_game):
        current_dialog_lines = ["..."] # Default fallback
        self.current_dialog_key = "fallback" # Reset for safety

        if self.name == "truth_seeker":
            if not story_flags_from_game.get("truth_seeker_initial_talk_done"):
                current_dialog_lines = self.base_dialogs.get("intro", ["Intro missing."])
                self.current_dialog_key = "intro" # Record that this sequence is being given
            elif not story_flags_from_game.get("truth_seeker_quest_accepted"):
                current_dialog_lines = self.base_dialogs.get("quest_offer", ["Quest offer missing."])
                self.current_dialog_key = "quest_offer"
            elif not story_flags_from_game.get("void_heart_obtained"): # Example flag
                current_dialog_lines = self.base_dialogs.get("waiting_for_heart", ["Waiting missing."])
                self.current_dialog_key = "waiting_for_heart"
            elif story_flags_from_game.get("void_heart_obtained"):
                current_dialog_lines = self.base_dialogs.get("has_heart", ["Has heart dialog missing."])
                self.current_dialog_key = "has_heart" # This interaction might set another flag via Game class
            else:
                current_dialog_lines = self.base_dialogs.get("outro", ["Outro missing."])
                self.current_dialog_key = "outro"
        
        elif self.name == "steelsoul":
            current_dialog_lines = self.base_dialogs.get("default", ["Steelsoul speaks."])
            self.current_dialog_key = "default"
        
        elif self.name == "noze":
            current_dialog_lines = self.base_dialogs.get("default", ["Noze mhehehes."])
            self.current_dialog_key = "default"
            # Noze might check player_data['geo'] and offer items, modifying player_data.
            # This is complex and depends on how you want item transactions to work.

        else: # Fallback for other NPCs or undefined states
            current_dialog_lines = self.base_dialogs.get("default", [f"{self.name} has nothing to say."])
            self.current_dialog_key = "default"

        return {'dialog': current_dialog_lines, 'dialog_key_spoken': self.current_dialog_key}

    def draw(self, screen, camera_rect, zoom):
        if not self.active or not self.image: # Ensure image exists
            return
        
        scaled_width = int(self.rect.width * zoom)
        scaled_height = int(self.rect.height * zoom)
        if scaled_width <= 0 or scaled_height <= 0: return

        scaled_img = pygame.transform.scale(self.image, (scaled_width, scaled_height))
        screen_x = int((self.rect.x - camera_rect.x) * zoom)
        screen_y = int((self.rect.y - camera_rect.y) * zoom)
        screen.blit(scaled_img, (screen_x, screen_y))

# create_npcs function might not be needed if Game.load_scene handles NPC creation directly
# def create_npcs(): # ...
