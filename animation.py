#animation.py

class Animation:
    def __init__(self, frames, frame_duration, loop=True):
        self.frames = frames
        self.frame_duration = frame_duration
        self.loop = loop
        self.current_frame = 0
        self.time_since_last = 0
        self.done = False

    def reset(self):
        self.current_frame = 0
        self.time_since_last = 0
        self.done = False

    # Keep the existing update method and other code
    def update(self, dt):
        self.time_since_last += dt
        if self.time_since_last >= self.frame_duration:
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    self.done = True
            self.time_since_last = 0

    def get_current_frame(self):
        return self.frames[self.current_frame]
