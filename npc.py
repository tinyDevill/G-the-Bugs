# npc.py
import pygame

# --- DIALOGS ---
truth_seeker_dialogs = {
    "intro": ["you...", "you have the void in your soul...", "so... finally...", ".. the destiny will be fulfilled."],
    "quest_offer": ["bring me the void heart from the deepest cave...", "only then can the seal be broken."],
    "waiting_for_heart": ["the void heart... have you found it?"],
    "has_heart": ["Ah, the void heart! Give it here... quickly!"],
    "outro": ["It is done... the path is clear... but at what cost?"]
}
steelsoul_dialogs = {
    "default": ["hey, whatchu doing here?", "wow, you have a cool sword?", "so, you just walking and slay that empty life corpse, right?","they once life. doing their job and so cheerful. but, after that black goo arrived from nowhere. i wonder, where it come from?"],
    "dialog2": ["this area is full of silent. but, i like it.", "this is so peacefully."]
}

# Updated Noze Dialogs as per your specification for the "easter egg" NPC
noze_dialogs = {
    "initial_offer": [
        "oh. you're so tiny, mwehehehe...",
        "this, take it. mwehehe..."
        # After these lines, game.py needs to handle a "Yes/No" prompt
        # and set 'noze_item_accepted' or 'noze_item_declined' flags.
    ],
    "item_accepted_followup": ["mwhehehe... you'll like it."],
    "item_declined_followup": ["nyeh. you waste my kindness."]
}

lost_knight_dialogs = {"default": ["Lost... so lost... was there ever a purpose?"]}

# Hornhead Dialogs as per your specification
hornhead_dialogs = {
    "first_encounter": [
        "why are you here?",
        "you must run, save your life. that crazy bug is doing something non sense. he sacrifice so much soul just so he can reach immortality. but, in the end? he became crazy bug instead. the void make his mind is empty. everything he thought is just to guard the void source from anyone."
        # After this, 'hornhead_first_talk_done' should be set to True in story_flags.
        # This can be done via 'on_interaction_end' in scene_config.py for Hornhead.
    ],
    "subsequent_talk": [
        "bah... i'm not strong bug. if you still won't run, i'll leave you. i told you after all."
    ]
}

witcher_dialogs = { # Placeholder, you can define Witcher's dialogs similarly
    "introduction": ["They call me Witcher. I hunt more than just beasts.", "These ruins whisper tales of forgotten magic."],
    "quest_hint": ["Something ancient stirs here. Its power could be yours... or your undoing."],
    "warning": ["Tread carefully. Not all that is dead stays buried."]
}
# ... other dialogs can be added here

class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name, base_dialogs, image_surface=None):
        super().__init__()
        self.name = name
        self.rect = pygame.Rect(x, y, width, height)
        self.base_dialogs = base_dialogs 
        
        if image_surface:
            self.image = pygame.transform.scale(image_surface, (width, height))
        else:
            # Default appearance if no image is provided
            self.image = pygame.Surface((width, height))
            if name == "noze": # Specific placeholder color for Noze if no image
                self.image.fill((200, 150, 250)) # A purplish color for Noze
            elif name == "hornhead": # Specific placeholder for Hornhead
                 self.image.fill((180, 100, 80)) # A brownish color for Hornhead
            else:
                self.image.fill((180, 180, 180)) # Generic grey

        self.active = True 
        self.current_dialog_key = "default" # Default key

    def interact(self, player_data, story_flags_from_game):
        current_dialog_lines = ["..."] # Default fallback
        self.current_dialog_key = "fallback" # Reset for safety

        if self.name == "truth_seeker":
            if not story_flags_from_game.get("truth_seeker_initial_talk_done"):
                current_dialog_lines = self.base_dialogs.get("intro", ["Intro missing."])
                self.current_dialog_key = "intro" 
            elif not story_flags_from_game.get("truth_seeker_quest_accepted"):
                current_dialog_lines = self.base_dialogs.get("quest_offer", ["Quest offer missing."])
                self.current_dialog_key = "quest_offer"
            elif not story_flags_from_game.get("void_heart_obtained"): 
                current_dialog_lines = self.base_dialogs.get("waiting_for_heart", ["Waiting missing."])
                self.current_dialog_key = "waiting_for_heart"
            elif story_flags_from_game.get("void_heart_obtained"):
                current_dialog_lines = self.base_dialogs.get("has_heart", ["Has heart dialog missing."])
                self.current_dialog_key = "has_heart" 
            else:
                current_dialog_lines = self.base_dialogs.get("outro", ["Outro missing."])
                self.current_dialog_key = "outro"
        
        elif self.name == "steelsoul":
            if story_flags_from_game.get("steelsoul_met_before", False): # Example flag
                 current_dialog_lines = self.base_dialogs.get("dialog2", ["Steelsoul speaks again."])
                 self.current_dialog_key = "dialog2"
            else:
                 current_dialog_lines = self.base_dialogs.get("default", ["Steelsoul speaks."])
                 self.current_dialog_key = "default"
                 # Game.py should set 'steelsoul_met_before' = True in story_flags
                 # (e.g., via on_interaction_end in scene_config.py for this NPC if this is the only initial dialog)
        
        elif self.name == "noze":
            # Noze's new dialog logic
            if story_flags_from_game.get("noze_item_accepted"):
                current_dialog_lines = self.base_dialogs.get("item_accepted_followup", ["mwhehehe... you'll like it."])
                self.current_dialog_key = "item_accepted_followup"
            elif story_flags_from_game.get("noze_item_declined"):
                current_dialog_lines = self.base_dialogs.get("item_declined_followup", ["nyeh. you waste my kindness."])
                self.current_dialog_key = "item_declined_followup"
            else:
                # This is the first interaction, or the choice hasn't been made and flagged yet.
                current_dialog_lines = self.base_dialogs.get("initial_offer", ["oh. you're so tiny, mwehehehe...", "this, take it. mwehehe..."])
                self.current_dialog_key = "initial_offer"
                # After this 'initial_offer' dialog completes (handled in game.py's
                # handle_npc_dialog_completion), game.py needs to:
                # 1. Trigger the "do you want to take the thing? yes no" prompt.
                # 2. Based on player's choice, set EITHER:
                #    story_flags_from_game["noze_item_accepted"] = True
                #    OR
                #    story_flags_from_game["noze_item_declined"] = True
                # This will ensure the correct follow-up dialog next time.
        
        elif self.name == "lost_knight":
            current_dialog_lines = self.base_dialogs.get("default", ["Lost Knight sighs."])
            self.current_dialog_key = "default"

        elif self.name == "hornhead":
            # Hornhead's new dialog logic
            if story_flags_from_game.get("hornhead_first_talk_done"):
                current_dialog_lines = self.base_dialogs.get("subsequent_talk", ["bah... i'm not strong bug. if you still won't run, i'll leave you. i told you after all."])
                self.current_dialog_key = "subsequent_talk"
            else:
                current_dialog_lines = self.base_dialogs.get("first_encounter", ["why are you here?", "you must run..."])
                self.current_dialog_key = "first_encounter"
                # Ensure 'hornhead_first_talk_done' is set to True after this interaction.
                # This can be done in scene_config.py for Hornhead's definition:
                # 'on_interaction_end': {'set_story_flag': 'hornhead_first_talk_done'}

        elif self.name == "witcher": # Placeholder logic for Witcher
            if story_flags_from_game.get("witcher_quest_hint_received"):
                 current_dialog_lines = self.base_dialogs.get("warning", ["Be wary."])
                 self.current_dialog_key = "warning"
            else:
                 current_dialog_lines = self.base_dialogs.get("introduction", ["Witcher introduction."])
                 self.current_dialog_key = "introduction"
                 # You could set "witcher_quest_hint_received" = True via on_interaction_end here.
        
        else: # Fallback for other NPCs or undefined states
            current_dialog_lines = self.base_dialogs.get("default", [f"{self.name} has nothing to say."])
            self.current_dialog_key = "default"

        return {'dialog': current_dialog_lines, 'dialog_key_spoken': self.current_dialog_key}

    def draw(self, screen, camera_rect, zoom):
        if not self.active or not self.image: 
            return
        
        scaled_width = int(self.rect.width * zoom)
        scaled_height = int(self.rect.height * zoom)
        if scaled_width <= 0 or scaled_height <= 0: return

        scaled_img = pygame.transform.scale(self.image, (scaled_width, scaled_height))
        screen_x = int((self.rect.x - camera_rect.x) * zoom)
        screen_y = int((self.rect.y - camera_rect.y) * zoom)
        screen.blit(scaled_img, (screen_x, screen_y))
