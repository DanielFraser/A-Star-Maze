from tkinter import *


def gui(currentMap, size, start, goal):
    unblocked_points = list()
    blocked_points = list()
    width = size
    height = size
    root = Tk()
    w = Canvas(root, width=width * 7, height=height * 7)
    cell_x, cell_y = 0, 0
    topLine = StringVar()


    def cell_clicked_event(event):
        cell_x, cell_y = round(event.x / 7), round(event.y / 7)
        f_val, g_val, h_val = 1,1,1
        ans = "f=" + str(f_val) + "\t" + "g=" + str(g_val) + "\t" + "h=" + str(
            h_val) + "\t" + "are the values for the coordinates:" + "\t" + "(" + str(cell_x) + "," + str(
            cell_y) + ")"
        topLine.set(ans)


    for x in range(0, width * 7, 7):
        for y in range(0, height * 7, 7):
            #print("{},{} = {}".format(x/7, y/7, currentMap[round(x / 7), round(y / 7)]))
            if currentMap[round(y / 7)][round(x / 7)] == 0:
                single_cell = w.create_rectangle(x, y, x + 7, y + 7, fill='green')
                w.tag_bind(single_cell, "<ButtonPress-1>", cell_clicked_event)
            elif currentMap[round(y / 7)][round(x / 7)] == 1:
                single_cell = w.create_rectangle(x, y, x + 7, y + 7, fill='purple')
                w.tag_bind(single_cell, "<ButtonPress-1>", cell_clicked_event)
            if [round(y / 7), round(x / 7)] == start:
                single_cell = w.create_rectangle(x, y, x + 7, y + 7, fill='yellow')
                w.tag_bind(single_cell, "<ButtonPress-1>", cell_clicked_event)
            elif [round(y / 7), round(x / 7)] == goal:
                single_cell = w.create_rectangle(x, y, x + 7, y + 7, fill='red')
                w.tag_bind(single_cell, "<ButtonPress-1>", cell_clicked_event)

    lab = Label(root, textvariable=topLine)
    lab.pack()
    w.pack()
    root.mainloop()