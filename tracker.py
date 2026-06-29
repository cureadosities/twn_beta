import time
import win32gui # type: ignore
import win32process # type: ignore
import psutil


BLOCK_SECONDS = 600


APP_CATEGORIES = {
    "WINWORD.EXE": "Working",
    "EXCEL.EXE": "Working",
    "notepad.exe": "Working",
    "Obsidian.exe": "Working",
    "Notion.exe": "Working",

    "POWERPNT.EXE": "Creating",
    "Canva.exe": "Creating",
    "Figma.exe": "Creating",

    "Code.exe": "Coding",

    "WhatsApp.exe": "Chatting",
    "Claude.exe": "Chatting",
    "ChatGPT.exe": "Chatting",

    "Zoom.exe": "Meeting",
    "Teams.exe": "Meeting",
    "ms-teams.exe": "Meeting",

    "chrome.exe": "Other",
}

class ActivityTracker:
    # 01 - Creates a new activity tracker
    def __init__(self):
        self.categories = {
            "Working": 0,
            "Creating": 0,
            "Coding": 0,
            "Chatting": 0,
            "Meeting": 0,
            "Other": 0,
        }
    
        self.current_category = None
        self.accumulated_seconds = 0
        self.last_check = time.time()

    # 02 - Gets the process name of the currently active foreground window
    def get_active_process_name(self):
        try:
            hwnd = win32gui.GetForegroundWindow()
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(pid)
            return process.name()
        except Exception:
            return None

    # 03 - Converts an application process name into one of the tracker categories
    def categories_process(self, process_name):
        if process_name is None:
            return None
        
        return APP_CATEGORIES.get(process_name, "Other")
    
    # 04 - Updates the current category timer and adds visual blocks
    def update(self):
        now = time.time()
        elapsed = now - self.last_check
        self.last_check = now

        process_name = self.get_active_process_name()
        category = self.categories_process(process_name)

        if category is None:
            return
        
        if category == self.current_category:
            self.accumulated_seconds += elapsed
        else:
            self.current_category = category
            self.accumulated_seconds = 0
        
        while self.accumulated_seconds >= BLOCK_SECONDS:
            self.categories[category] += 1
            self.accumulated_seconds -= BLOCK_SECONDS