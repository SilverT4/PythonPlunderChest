import tkinter as tk
from tkinter import ttk
import playsound as ps
from functools import partial
import sys
cursors = ["X_cursor",
           "arrow",
           "based_arrow_down",
           "based_arrow_up",
           "boat",
           "bogosity",
           "bottom_left_corner",
           "bottom_right_corner",
           "bottom_side",
           "bottom_tee",
           "box_spiral",
           "center_ptr",
           "circle",
           "clock",
           "coffee_mug",
           "cross",
           "cross_reverse",
           "crosshair",
           "diamond_cross",
           "dot",
           "dotbox",
           "double_arrow",
           "draft_large",
           "draft_small",
           "draped_box",
           "exchange",
           "fleur",
           "gobbler",
           "gumby",
           "hand1",
           "hand2",
           "heart",
           "icon",
           "iron_cross",
           "left_ptr",
           "left_side",
           "left_tee",
           "leftbutton",
           "ll_angle",
           "lr_angle",
           "man",
           "middlebutton",
           "mouse",
           "none",
           "pencil",
           "pirate",
           "plus",
           "question_arrow",
           "right_ptr",
           "right_side",
           "right_tee",
           "rightbutton",
           "rtl_logo",
           "sailboat",
           "sb_down_arrow",
           "sb_h_double_arrow",
           "sb_left_arrow",
           "sb_right_arrow",
           "sb_up_arrow",
           "sb_v_double_arrow",
           "shuttle",
           "sizing",
           "spider",
           "spraycan",
           "star",
           "target",
           "tcross",
           "top_left_arrow",
           "top_left_corner",
           "top_right_corner",
           "top_side",
           "top_tee",
           "trek",
           "ul_angle",
           "umbrella",
           "ur_angle",
           "watch",
           "xterm"]
win_cursors = ["no",
               "starting",
               "size",
               "size_ne_sw",
               "size_ns",
               "size_nw_se",
               "size_we",
               "uparrow",
               "wait"]
osx_cursors = ["copyarrow",
               "aliasarrow",
               "contextualmenuarrow",
               "text",
               "cross-hair",
               "closedhand",
               "openhand",
               "pointinghand",
               "resizeleft",
               "resizeright",
               "resizeleftright",
               "resizeup",
               "resizedown",
               "resizeupdown",
               "notallowed",
               "poof",
               "countinguphand",
               "countingdownhand",
               "countingupanddownhand",
               "spinning"]

match sys.platform:
    case "win32" | "cygwin":
        cursors.extend(win_cursors)
    case "darwin":
        cursors.extend(osx_cursors)
    case _:
        print(sys.platform)
root = tk.Tk()
root.title("cursor tester")
cv=tk.StringVar()
def switchCursor(c:tk.Event):
    testButton.configure(cursor=clist.get())
clist = ttk.Combobox(root,values=cursors,width=max([len(s) for s in cursors]))
clist.grid(row=0,column=0)
clist.bind("<<ComboboxSelected>>",switchCursor)
testButton = tk.Button(text="sexooooo",command=partial(ps.playsound,"../random-sounds/confirmSmall.wav"))
testButton.grid(row=0,column=1)
root.mainloop()
