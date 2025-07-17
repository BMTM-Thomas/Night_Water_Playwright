from playwright.sync_api import sync_playwright, expect

@staticmethod
def dnd_drag_random():
    with sync_playwright() as p:  
        print("test")

@staticmethod
def dnd_drag_random2(): 
    with sync_playwright() as p: 
        dnd_drag_random()
        print("test")