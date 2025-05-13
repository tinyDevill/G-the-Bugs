import pygame

truth_seeker_dialogs = {
    "intro": [
        "you...",
        "you have the void in your soul. you must have risen from the void.",
        "so... finally...",
        ".. the destiny will be fulfilled."
    ],
    "request_crystal": [
        "you... bring me the white crystal...",
        "and you...",
        "...will...",
        "...fulfill your destiny."
    ],
    "before_crystal": [
        "give it to me...",
        "you... don't have it? and then, find it...",
        "...and bring it to me..."
    ],
    "after_geo_donation": [
        "give it to me...",
        "...and now..."
    ],
    "give_seal": [
        "this...",
        "with that thing...",
        "you... finally can do your destiny..."
    ]
}

steelsoul_dialogs = {
    "default": [
        "hey, whatchu doing here?",
        "wow, you have a cool sword?",
        "so, you just walking and slay that empty life corpse, right?",
        "they once life. doing their job and so cheerful. but, after that black goo arrived from nowhere. i wonder, where it come from?",
        "this area is full of silent. but, i like it.",
        "this is so peacefully."
    ]
}

noze_dialogs = {
    "offer": ["oh. you're so tiny, mwehehehe...", "this, take it. mwehehe..."],
    "accepted": ["mwhehehe... you'll like it."],
    "rejected": ["nyeh. you waste my kindness."],
    "loop_yes": ["mwhehehe... you'll like it."],
    "loop_no": ["nyeh. you waste my kindness."]
}

lost_knight_dialogs = {
    "default": [
        "why are you here?",
        "you must run, save your life. that crazy bug is doing something non sense.",
        "he sacrifice so much soul just so he can reach immortality. but, in the end?",
        "he became crazy bug instead. the void make his mind is empty.",
        "everything he thought is just to guard the void source from anyone.",
        "bah... i'm not strong bug. if you still won't run, i'll leave you. i told you after all."
    ]
}

class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name, dialogs, image=None):
        super().__init__()
        self.name = name
        self.rect = pygame.Rect(x, y, width, height)
        self.dialogs = dialogs
        self.dialog_index = 0
        self.image = image if image else pygame.Surface((width, height))
        self.image.fill((180, 180, 180))
        self.has_given_item = False
        self.active = True

    def interact(self, player_data):
        """
        player_data: dictionary yang menyimpan data player seperti geo, inventory
        """
        current_dialog = []

        if self.name == "truth_seeker":
            has_crystal = "white_crystal" in player_data.get("inventory", [])
            has_seal = "white_seal" in player_data.get("inventory", [])
            geo = player_data.get("geo", 0)

            if not has_crystal:
                if geo >= 100:
                    player_data["geo"] -= 100
                    player_data["inventory"].append("white_crystal")
                    current_dialog = self.dialogs["after_geo_donation"]
                else:
                    current_dialog = self.dialogs["before_crystal"]
            elif has_crystal and not has_seal:
                if not self.has_given_item:
                    self.has_given_item = True
                    player_data["inventory"].append("white_seal")
                    current_dialog = self.dialogs["give_seal"]
                else:
                    current_dialog = ["...you already got what you need..."]
            else:
                current_dialog = ["...go fulfill your destiny..."]

        elif self.name == "steelsoul":
            current_dialog = self.dialogs["default"]

        elif self.name == "noze":
            if not self.has_given_item:
                current_dialog = self.dialogs["offer"]
            else:
                if "noze_item" in player_data.get("inventory", []):
                    current_dialog = self.dialogs["loop_yes"]
                else:
                    current_dialog = self.dialogs["loop_no"]

        elif self.name == "lost_knight":
            current_dialog = self.dialogs["default"]

        return current_dialog

    def give_noze_item(self, player_data, accepted):
        if accepted:
            player_data["inventory"].append("noze_item")
            self.has_given_item = True
            return self.dialogs["accepted"]
        else:
            return self.dialogs["rejected"]

    def draw(self, screen, camera_rect, zoom):
        screen.blit(self.image, ((self.rect.x - camera_rect.x) * zoom,
                                 (self.rect.y - camera_rect.y) * zoom))

def create_npcs():
    return [
        NPC(100, 500, 40, 60, "truth_seeker", truth_seeker_dialogs),
        NPC(300, 500, 40, 60, "steelsoul", steelsoul_dialogs),
        NPC(600, 500, 40, 60, "noze", noze_dialogs),
        NPC(900, 500, 40, 60, "lost_knight", lost_knight_dialogs),
    ]
