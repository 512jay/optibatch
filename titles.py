import pygetwindow as gw

for w in gw.getAllWindows():
    if w.visible:
        print(f"VISIBLE: {w.title}")
