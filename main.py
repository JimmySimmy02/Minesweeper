from tkinter import *
import settings
import util
from cell import Cell
from PIL import ImageTk, Image

root = Tk()
#Override window settings
root.configure(background = 'black',)
root.geometry( f'{settings.window_width}x{settings.window_height}' )
root.title( "Minesweeper ")
root.resizable(False, False)

#Create top frame
top_frame = Frame(
  root,
  bg = 'black',
  width = settings.window_width,
  height = util.height_prct(25),
)
top_frame.place(x = 0, y = 0)

#Create Title
image_title = Image.open('Images/image_TitleBoard.png')
image_title = image_title.resize((util.width_prct(50), util.height_prct(25)), Image.LANCZOS)
image_title = ImageTk.PhotoImage(image_title)
game_title = Label(
  top_frame,
  image = image_title,
  text = 'Minesweeper',
  bg = 'black',
  fg = 'white',
  font = ('', 48),
  compound = 'center',
)
game_title.place(
  x = util.width_prct(25),
  y = 0
)

#Create left frame
left_frame = Frame(
  root,
  bg = 'black',
  width = util.width_prct(25),
  height = util.height_prct(75),
)
left_frame.place(x = 0, y = util.height_prct(25))

#Create center frame
center_frame = Frame(
  root,
  bg = '',
  width = util.width_prct(75),
  height = util.height_prct(75),
)
center_frame.place(x = util.width_prct(25), y = util.height_prct(25))

for x in range(settings.grid_width):
  for y in range(settings.grid_height):
    c1 = Cell(x,y)
    c1.create_btn_object(center_frame)
    c1.cell_btn_object.grid(column = x, row = y)
    
#Calling Background Image
Cell.create_background_label(root)

#Calling Replay Button
Cell.create_replay_button(left_frame, center_frame)
Cell.replay_button_object.pack()

#Calling Cellcount label
Cell.create_cellcount_label(left_frame)
Cell.cellcount_label_object.pack()

#Calling Minesleft label
Cell.create_MinesLeft_label(left_frame)
Cell.mines_left_label_object.pack()

#Run the window
root.mainloop()

