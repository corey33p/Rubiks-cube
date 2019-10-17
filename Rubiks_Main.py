from Rubiks_Display import Display
from Rubiks_Cube import Cube
from tkinter import mainloop
import os
import win32gui
import win32con
import threading
from queue import Queue
from PIL import Image
import time
import traceback
from collections import Counter

class Parent:
    def __init__(self):
        self.main_queue = Queue()
        self.cube = Cube(self)
        self.display  = Display(self)
        # self.resize_CLI_window()
        #
        self.pause = False
        main_queue_thread = threading.Thread(target=lambda: self.main_queue_thread())
        main_queue_thread.daemon = True
        main_queue_thread.start()
       
        mainloop()
    def resize_CLI_window(self):
        def get_windows():
            def check(hwnd, param):
                title = win32gui.GetWindowText(hwnd)
                if 'Rubiks_Main' in title and 'Notepad++' not in title:
                    param.append(hwnd)
            wind = []
            win32gui.EnumWindows(check, wind)
            return wind
        self.cli_handles = get_windows()
        for window in self.cli_handles:
            # win32gui.MoveWindow(window,-1020,300,1015,640,True)
            win32gui.MoveWindow(window,16,62,1087,851,True)
            # win32gui.MoveWindow(window,-141,1107,1002,989,True)
    def main_queue_thread(self):
        while True: 
            time.sleep(.25)
            try:
                next_action = self.main_queue.get(False)
                next_action()
            except Exception as e: 
                if str(e) != "": 
                    print(traceback.format_exc())
        self.main_queue.queue.clear()
        self.close()
    def close(self):
        for handle in self.cli_handles:
            win32gui.PostMessage(handle,win32con.WM_CLOSE,0,0)

if __name__ == '__main__':
    main_object = Parent()
    