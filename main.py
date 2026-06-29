import os
import ctypes
import tkinter as tk
import tkinter.font as tkfont
from tkinter import Canvas
from PIL import Image, ImageTk, ImageDraw
import winsound

from timer import Timer
from tracker import ActivityTracker


# ═════════════════════════════════════════════════════════════════════════════
#  INTERFACE
# ═════════════════════════════════════════════════════════════════════════════

BG = "#251E12"
TEXT = "#f6f1e5"
MUTED = "#3d3326"

WINDOW_WIDTH = 430
WINDOW_HEIGHT = 750

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ASSET_DIR = os.path.join(BASE_DIR, "assets")
FONT_DIR = os.path.join(ASSET_DIR, "fonts")
ICON_DIR = os.path.join(ASSET_DIR, "icons")
IMAGE_DIR = os.path.join(ASSET_DIR, "images")
SOUND_DIR = os.path.join(ASSET_DIR, "sounds")

FONT_FILE = "RobotoMono-Regular.ttf"
FONT_FAMILY = "Roboto Mono"
FALLBACK_FONT_FAMILY = "Courier New"

FONT = (FONT_FAMILY, 11)
FONT_SMALL = (FONT_FAMILY, 10)
FONT_TITLE = (FONT_FAMILY, 12)

PAINTING_PATH = os.path.join(IMAGE_DIR, "painting.png")
FOOTER_PATH = os.path.join(IMAGE_DIR, "footer.png")
ALARM_PATH = os.path.join(SOUND_DIR, "alarm.wav")


# ═════════════════════════════════════════════════════════════════════════════
#  ANCHORS
# ═════════════════════════════════════════════════════════════════════════════

ANCHORS = {
    "One song": {
        "duration": 5 * 60,
        "icon": "song.png",
    },
    "One meditation": {
        "duration": 10 * 60,
        "icon": "meditation.png",
    },
    "One pomodoro": {
        "duration": 25 * 60,
        "icon": "pomodoro.png",
    },
    "One podcast": {
        "duration": 45 * 60,
        "icon": "podcast.png",
    },
    "One workout": {
        "duration": 60 * 60,
        "icon": "workout.png",
    },
    "One movie": {
        "duration": 120 * 60,
        "icon": "movie.png",
    },
}


# ═════════════════════════════════════════════════════════════════════════════
#  FONT
# ═════════════════════════════════════════════════════════════════════════════

# Loads Roboto Mono
def load_custom_font():
    font_path = os.path.join(FONT_DIR, FONT_FILE)

    if os.path.exists(font_path):
        try:
            ctypes.windll.gdi32.AddFontResourceExW(font_path, 0x10, 0)
        except Exception:
            pass

# Chooses Roboto Mono if available, otherwise chooses Courier New
def choose_font_family(root):
    available_fonts = set(tkfont.families(root))

    if FONT_FAMILY in available_fonts:
        return FONT_FAMILY
    
    return FALLBACK_FONT_FAMILY


# ═════════════════════════════════════════════════════════════════════════════
#  FUNCTION
# ═════════════════════════════════════════════════════════════════════════════

class TWNApp:
    # 01 - Creates the main TWN application
    def __init__(self, root):
        self.root = root
        self.root.title("Time Without Numbers")
        self.root.geometry (f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.timer = Timer()
        self.tracker = ActivityTracker()

        self.selected_anchor = None

        self.icon_cache = {}
        self.painting_image = None
        self.footer_image = None

        self.tracker_container = None
        self.canvas = None

        self.main_frame = tk.Frame(self.root, bg=BG)
        self.main_frame.pack(fill="both", expand=True)

        self.show_selection_screen()

        self.update_timer_loop()
        self.update_tracker_loop()
    
    # 02 - Removes all widget from the current screen before drawing a new screen
    def clear_screen(self):
        for child in self.main_frame.winfo_children():
            child.destroy()

        self.canvas = None
        self.tracker_container = None
    
    # 03 - Loads PNG image
    def load_png(self, path, size=None):
        try:
            image = Image.open(path).convert("RGBA")
        except FileNotFoundError:
            image = Image.new("RGBA", size or (40,40), (0, 0, 0, 0))

        if size:
            image = image.resize(size, Image.Resampling.LANCZOS)
        
        return ImageTk.PhotoImage(image)
    
    # 04 - Loads and caches icon
    def get_icon(self, filename, size):
        key = f"{filename}-{size[0]}x{size[1]}"

        if key not in self.icon_cache:
            path = os.path.join(ICON_DIR, filename)
            self.icon_cache[key] = self.load_png(path, size)

        return self.icon_cache[key]

    # 05 - Creates styled text label
    def label(self, parent, text, font=None, pady=0):
        if font is None:
            font = FONT
        
        widget = tk.Label(
            parent,
            text=text,
            fg=TEXT,
            bg=BG,
            font=font,
        )
        widget.pack(pady=pady)
        return widget
    
    # 06 - Draws horizontal dashed divider line
    def divider(self, parent):
        tk.Label(
            parent,
            text="-" * 40,
            fg = TEXT,
            bg = BG,
            font = FONT,
        ).pack(pady=(3, 3))
    
    # 07a - Draws header with logo icons and title
    def header(self, title):
        top = tk.Frame(self.main_frame, bg=BG)
        top.pack(fill="x", padx=28, pady=(12, 0))

        logo = self.get_icon("logo.png", (34, 34))

        left_logo = tk.Label(top, image=logo, bg=BG, cursor="hand2")
        left_logo.pack(side="left")
        left_logo.bind("<Button-1>", lambda e: self._go_home())

        right_logo = tk.Label(top, image=logo, bg=BG, cursor="hand2")
        right_logo.pack(side="right")
        right_logo.bind("<Button-1>", lambda e: self._go_home())

        self.label(self.main_frame, title.upper(), FONT_TITLE, pady=(5, 0))
    
    # 07b - Uses header to go to home
    def _go_home(self):
        self.timer.stop()
        self.show_selection_screen()

    # 08 - Draws timer selection screen with six timer buttons
    def show_selection_screen(self):
        self.clear_screen()

        self.header("Timer")
        self.divider(self.main_frame)

        grid = tk.Frame(self.main_frame, bg=BG)
        grid.pack(pady=(3, 3))

        names = list(ANCHORS.keys())

        for index, name in enumerate(names):
            row = index // 2
            column = index % 2

            # Creates a beige outer frame that acts as the button outline.
            card = tk.Frame(
                grid,
                bg=TEXT,
                width=176,
                height=76,
            )

            card.grid(row=row, column=column, padx=11, pady=12)
            card.grid_propagate(False)

            # Creates the actual clickable button inside the beige outline.
            button = tk.Button(
                card,
                text=name.lower(),
                image=self.get_icon(ANCHORS[name]["icon"], (30, 30)),
                compound="top",
                command=lambda n=name: self.select_anchor(n),
                width=170,
                height=70,
                fg=TEXT,
                bg=BG,
                activeforeground=TEXT,
                activebackground=BG,
                relief="flat",
                bd=0,
                highlightthickness=0,
                overrelief="flat",
                font=FONT,
                cursor="hand2",
                takefocus=0
            )

            button.place(x=3, y=3)

        self.label(self.main_frame, "TRACKER", FONT_TITLE, pady=(4, 0))
        self.divider(self.main_frame)

        self.tracker_container = tk.Frame(self.main_frame, bg=BG)
        self.tracker_container.pack(fill="x", padx=34)

        self.draw_tracker()
        self.draw_footer()

    # 09 - Stores selected timer, sets its duration, and opens timer screen
    def select_anchor(self, name):
        self.selected_anchor = name
        self.timer.set_duration(ANCHORS[name]["duration"])
        self.show_timer_screen()
    
    # 10 - Draws active timer screen with circular timer, controls, tracker, and footer
    def show_timer_screen(self):
        self.clear_screen()

        self.header(self.selected_anchor)
        self.draw_timer_area()

        controls = tk.Frame(self.main_frame, bg=BG)
        controls.pack(fill="x", padx=38, pady=(0, 6))

        self.play_pause_button = tk.Button(
            controls,
            image=self.get_current_play_icon(),
            command=self.toggle_play_pause,
            bg=BG,
            activebackground=BG,
            relief="flat",
            bd=0,
            cursor="hand2",
        )
        self.play_pause_button.pack(side="left")

        self.stop_button = tk.Button(
            controls,
            image=self.get_icon("stop.png", (40, 40)),
            command=self.stop_timer,
            bg=BG,
            activebackground=BG,
            relief="flat",
            bd=0,
            cursor="hand2",
        )
        self.stop_button.pack(side="right")

        self.divider(self.main_frame)

        self.tracker_container = tk.Frame(self.main_frame, bg=BG)
        self.tracker_container.pack(fill="x", padx=34)

        self.draw_tracker()
        self.draw_footer()
    
    # 11 - Returns correct play or pause icon
    def get_current_play_icon(self):
        if self.timer.running:
            return self.get_icon("pause.png", (40,40))
        
        return self.get_icon("play.png", (40, 40))
    
    # 12 - Creates canvas area used for circular timer and painting
    def draw_timer_area(self):
        self.canvas = Canvas(
            self.main_frame,
            width=420,
            height=310,
            bg=BG,
            highlightthickness=0,
        )
        self.canvas.pack(pady=(6, 0))

        self.prepare_painting()
        self.draw_timer_ring()

    # 13 - Loads painting
    def prepare_painting(self):
        try:
            image = Image.open(PAINTING_PATH).convert("RGBA")
        except FileNotFoundError:
            image = Image.new("RGBA", (220, 220), MUTED)

        image = image.resize((220, 220), Image.Resampling.LANCZOS)

        mask = Image.new("L", (220, 220), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 220, 220), fill=255)

        circular = Image.new("RGBA", (220, 220), (0, 0, 0, 0))
        circular.paste(image, (0,0), mask)

        self.painting_image = ImageTk.PhotoImage(circular)
    
    # 14 - Draws circular timer ring, progress arc, and painting
    def draw_timer_ring(self):
        if self.canvas is None:
            return
        
        self.canvas.delete("all")

        cx = 210
        cy = 155
        radius = 145

        self.canvas.create_oval(
            cx - radius,
            cy - radius,
            cx + radius,
            cy + radius,
            outline = MUTED,
            width = 8,
        )

        progress = self.timer.progress()

        if progress > 0:
            self.canvas.create_arc(
                cx - radius,
                cy - radius,
                cx + radius,
                cy + radius,
                start=90,
                extent=-360 * progress,
                style="arc",
                outline=TEXT,
                width=8
            )
        
        self.canvas.create_image(cx, cy, image=self.painting_image)
    
    # 15 - Switches timer and resets circular progress ring
    def toggle_play_pause(self):
        if self.timer.running:
            self.timer.pause()
        else:
            self.timer.play()
        
        self.update_control_icons()

    # 16 - Stops timer and resets circular progress ring
    def stop_timer(self):
        self.timer.stop()
        self.update_control_icons()
        self.draw_timer_ring()

    # 17 - Updates play/pause button to match current timer state
    def update_control_icons(self):
        if hasattr(self, "play_pause_button"):
            self.play_pause_button.configure(image=self.get_current_play_icon())
    
    # 18 - Plays alarm sound when timer finishes
    def play_alarm(self):
        if os.path.exists(ALARM_PATH):
            winsound.PlaySound(ALARM_PATH, winsound.SND_FILENAME | winsound.SND_ASYNC)
        else:
            winsound.MessageBeep()
    
    # 19 - Repeatedly updates timer state and redraws ring
    def update_timer_loop(self):
        self.timer.update()

        if self.timer.finished and not self.timer.alarm_played:
            self.play_alarm()
            self.timer.alarm_played = True
            self.update_control_icons()

        if self.canvas is not None:
            self.draw_timer_ring()

        self.root.after(100, self.update_timer_loop)
    
    # 20 - Repeatedly updates passive activity tracker and redraws tracker display
    def update_tracker_loop(self):
        self.tracker.update()

        if self.tracker_container is not None:
            self.draw_tracker()
        
        self.root.after(1000, self.update_tracker_loop)
    
    # 21 - Draws tracker category labels and visual activity blocks
    def draw_tracker(self):
        if self.tracker_container is None:
            return
        
        for child in self.tracker_container.winfo_children():
            child.destroy()

        for category, count in self.tracker.categories.items():
            row = tk.Frame(self.tracker_container, bg=BG)
            row.pack(fill="x", pady=1)

            tk.Label(
                row,
                text=category,
                fg=TEXT,
                bg=BG,
                font=FONT,
                width=12,
                anchor="w",
            ).pack(side="left")

            tk.Label(
                row,
                text="█" * count,
                fg=TEXT,
                bg=BG,
                font=FONT,
                anchor="w"
            ).pack(side="left")
    
    # 22 - Draws bottom footer
    def draw_footer(self):
        footer_frame = tk.Frame(self.main_frame, bg=BG)
        footer_frame.pack(side="bottom", fill="x")

        try:
            image = Image.open(FOOTER_PATH).convert("RGBA")
            image = image.resize((WINDOW_WIDTH, 68), Image.LANCZOS)
            self.footer_image = ImageTk.PhotoImage(image)

            tk.Label(
                footer_frame,
                image=self.footer_image,
                bg=BG,
            ).pack(fill="x")
        except FileNotFoundError:
            fallback_footer = tk.Frame(
                footer_frame,
                bg=MUTED,
                height=68,
            )
            fallback_footer.pack(fill="x")


# ═════════════════════════════════════════════════════════════════════════════
#  MAIN
# ═════════════════════════════════════════════════════════════════════════════

def main():
    load_custom_font()
    root = tk.Tk()
    global FONT, FONT_SMALL, FONT_TITLE
    chosen_font = choose_font_family(root)

    FONT = (chosen_font, 11)
    FONT_SMALL = (chosen_font, 10)
    FONT_TITLE = (chosen_font, 12)

    TWNApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()