from tkinter import *








root = Tk()
frame=Frame(root)
Grid.rowconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 0, weight=1)
frame.grid(row=0, column=0, sticky=N+S+E+W)
grid=Frame(frame)
grid.grid(sticky=N+S+E+W, column=0, row=7, columnspan=2)
Grid.rowconfigure(frame, 7, weight=1)
Grid.columnconfigure(frame, 0, weight=1)


## this code is executed on button push
def prompt_placement(_id):
    print('placeholder'+str(_id))

##def place_ships():
    

class bButton:
    def __init__(self,ID):
        self._id=ID
        self.btn = Button(frame,bg='white',activebackground='grey',text="",command=self.change_text)
    def change_text(self):
        self.btn.configure(text="X")
        print(self._id)

#example values
for x in range(10):
    for y in range(5):
        b = bButton((x,y))
       ## btn = Button(frame,command=prompt_placement)
        b.btn.grid(column=x, row=y, sticky=N+S+E+W)

for x in range(10):
  Grid.columnconfigure(frame, x, weight=1)

for y in range(5):
  Grid.rowconfigure(frame, y, weight=1)


root.mainloop()
