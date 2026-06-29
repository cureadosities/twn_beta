import time


class Timer:
    # 01 - Creates a new timer object
    def __init__(self):
        self.duration = 0
        self.remaining = 0
        self.start_time = None
        self.running = False
        self.finished = False
        self.alarm_played = False
    
    # 02 - Sets the timer duration and resets the timer
    def set_duration(self, seconds):
        self.duration = seconds
        self.remaining = seconds
        self.start_time = None
        self.running = False
        self.finished = False
        self.alarm_played = False

    # 03 - Starts or restarts the timer
    def play(self):
        if self.duration <= 0:
            return
        
        if self.finished:
            self.remaining = self.duration
            self.finished = False
            self.alarm_played = False
        
        if not self.running:
            self.start_time = time.time()
            self.running = True

    # 04 - Pauses the timer and stores the remaining time
    def pause(self):
        if self.running:
            elapsed = time.time() - self.start_time
            self.remaining = max(0, self.remaining - elapsed)
            self.start_time = None
            self.running = False
    
    # 05 - Stops the timer and resets back to the full duration
    def stop(self):
        self.remaining = self.duration
        self.start_time = None
        self.running = False
        self.finished = False
        self.alarm_played = False

    # 06 - Updates the remaining time based on how much time has passed
    def update(self):
        if not self.running:
            return
        
        now = time.time()
        elapsed = now - self.start_time
        
        self.remaining = max(0, self.remaining - elapsed)
        self.start_time = now

        if self.remaining <= 0:
            self.remaining = 0
            self.running = False
            self.finished = True

    # 07 - Returns the timer's progress
    def progress(self):
        if self.duration <= 0:
            return 0
        
        return 1 - (self.remaining / self.duration)