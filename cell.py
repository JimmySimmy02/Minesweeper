from tkinter import *
import random
import settings
from tkinter import messagebox
import sys
import time
from PIL import ImageTk, Image
import pygame

class Cell:

  #Initialise Cell List
  all = []
  #Initialise Labels
  cellcount_label_object = None
  mines_left_label_object = None
  #Initialise cellcount
  cellcount = settings.grid_cells - settings.mines_count
  #Initialise Mines, Flags Left
  flags_left = settings.mines_count
  truemines_left = settings.mines_count
  #Initialise firstclick variable
  first_click = True

  #Initialise Cell Attributes
  def __init__(self,x,y, is_mine = False):
    self.is_mine = is_mine
    self.cell_btn_object = None
    self.x=x
    self.y=y
    self.is_opened = False
    self.is_marked = False
    self.is_iterated = False
    
    #Append object to Cell.all
    Cell.all.append(self)

  #Create Button Function
  def create_btn_object(self, location):
    btn = Button(
        location,
        width=6,
        height=4,
    )

    self.cell_btn_object = btn
    btn.bind('<Button-1>', self.left_click_actions)
    btn.bind('<Button-3>', self.right_click_actions)

  #Create Cellcount Label Function
  @staticmethod
  def create_cellcount_label(location):
    lbl = Label(
      location,
      bg = 'black',
      fg = 'white',
      text = f'Cells Remaining: {Cell.cellcount}',
      width = 16,
      height = 4,
      font=('', 15)
    )
    Cell.cellcount_label_object = lbl

  #Create Minesleft Label Function
  @staticmethod
  def create_MinesLeft_label(location):
    lbl = Label(
      location,
      bg = 'black',
      fg = 'white',
      text = f'Flags Left: {Cell.flags_left}',
      width = 16,
      height = 4,
      font=('', 15)
    )
    Cell.mines_left_label_object = lbl

  #Create Replay Button
  @staticmethod
  def create_replay_button(button_location, game_location):
    image = Image.open('Images/image_GreenBannerRect.png')
    image = image.resize((800, 200), Image.LANCZOS)
    Cell.Replay_Button_Image = ImageTk.PhotoImage(image)
    btn = Button(
      button_location,
      width = 200,
      height = 50,
      image = Cell.Replay_Button_Image,
      text = 'Replay',
      fg = 'white',
      font = ('', 15),
      compound = 'center'
    )
    Cell.replay_button_object = btn
    btn.bind('<Button-1>',lambda event: Cell.reset(game_location))
  
  #Left Click Function
  def left_click_actions(self, event):
    if Cell.first_click:
      #Place Mines
      Cell.randomize_mines(self)
      self.expose_connected_cells(self)
      self.show_cell()
      Cell.first_click = False
    else:
      if self.is_mine:
        if not self.is_marked:
          self.show_mine()
      else:
        if not self.is_marked:
          self.expose_connected_cells(self)
          self.show_cell()
          #Win Game
          if Cell.truemines_left <= 0:
            messagebox.showinfo(title = 'Well Done', message = 'You Win!')
      
  #Right Click Function
  def right_click_actions(self, event):
    if not self.is_marked:
      if not self.is_opened:
        self.cell_btn_object.configure(
        text = 'X'
        )
        self.is_marked = True
        Cell.flags_left-=1
        Cell.update_minesleft_label()
        if self.is_mine:
          Cell.truemines_left-=1

        #Win Game
        if Cell.truemines_left <= 0:
          messagebox.showinfo(title = 'Well Done', message = 'You Win!')
    else:
      self.cell_btn_object.configure(
        text = ' '
      )
      self.is_marked = False
      Cell.flags_left += 1
      if self.is_mine:
        Cell.truemines_left+=1
      Cell.update_minesleft_label()

  #Recursively expose connected 0 cells function
  def expose_connected_cells(self, cell):
    if cell.surrounded_cells_mines_count == 0 and not cell.is_iterated:
      cell.show_cell()
      cell.is_iterated = True
      for cell_obj in self.surrounded_cells:
        cell_obj.show_cell()
      for neighbor in cell.surrounded_cells:
        neighbor.show_cell()
        self.expose_connected_cells(neighbor)
      
  #Show Mine Function
  def show_mine(self):
    image_mine = Image.open('Images/image_mine2.png')
    image_mine = image_mine.resize((65, 65), Image.LANCZOS)
    image_mine = ImageTk.PhotoImage(image_mine)
    self.cell_btn_object.config(image = image_mine)
    self.cell_btn_object.image = image_mine
    Cell.play_explosion_sound()
    #Endgame Message
    messagebox.showinfo("Game Over", "You clicked on a mine :(")
  
  def get_cell_by_axis(self, x, y):
    for cell in Cell.all:
      if cell.x == x and cell.y == y:
        return cell

  #Get Surrounding Cells Function, remove nonextistent cells
  @property
  def surrounded_cells(self):
    cells = [
      self.get_cell_by_axis(self.x-1, self.y-1),
      self.get_cell_by_axis(self.x-1, self.y),
      self.get_cell_by_axis(self.x-1, self.y+1),
      self.get_cell_by_axis(self.x, self.y-1),
      self.get_cell_by_axis(self.x, self.y+1),
      self.get_cell_by_axis(self.x+1, self.y-1),
      self.get_cell_by_axis(self.x+1, self.y),
      self.get_cell_by_axis(self.x+1, self.y+1)
    ]
    cells = [cell for cell in cells if cell is not None]
    return cells

  #Count Surrounding Mines Function
  @property
  def surrounded_cells_mines_count(self):
    counter = 0
    for cell in self.surrounded_cells:
      if cell.is_mine:
        counter += 1
    return counter

  #Display Surrounding Mines Function
  def show_cell(self): 
    if not self.is_opened and not self.is_marked:
      Cell.cellcount -= 1
      surrounding_count = self.surrounded_cells_mines_count

      #Configure Text Colour
      if surrounding_count == 1:
        self.cell_btn_object.configure(fg = 'blue')
      elif surrounding_count == 2:
        self.cell_btn_object.configure(fg = 'green')
      elif surrounding_count == 3:
        self.cell_btn_object.configure(fg = 'red')
      elif surrounding_count == 4:
        self.cell_btn_object.configure(fg = 'navy')
      elif surrounding_count == 5:
        self.cell_btn_object.configure(fg = 'saddle brown')
      elif surrounding_count == 6:
        self.cell_btn_object.configure(fg = 'cyan')
      elif surrounding_count == 7:
        self.cell_btn_object.configure(fg = 'black')
      elif surrounding_count == 8:
        self.cell_btn_object.configure(fg = 'gray')

      self.cell_btn_object.configure(text = surrounding_count)
      
      Cell.update_cellcount_label()
    #Mark Cell as opened
    self.is_opened = True

  #Update cellcount label
  def update_cellcount_label():
    if Cell.cellcount_label_object:
      Cell.cellcount_label_object.configure(
      text = 'Cells Remaining: ' + str(Cell.cellcount))

  #Update mines left label
  def update_minesleft_label():
    if Cell.mines_left_label_object:
      Cell.mines_left_label_object.configure(
      text = 'Flags Left: ' + str(Cell.flags_left))
      
  #Create Mines Function
  def randomize_mines(self):
    all_cells = Cell.all.copy()
    all_cells.remove(self)
    picked_cells = random.sample(all_cells, settings.mines_count)
    for cell in picked_cells:
      cell.is_mine = True

  #Name Cell Function
  def __repr__(self):
    return f'Cell({self.x},{self.y})'
    
  #Reset Game Function
  @staticmethod
  def reset(location):

    # Destroy all button objects
    for cell in Cell.all:
        cell.cell_btn_object.destroy()
      
    #Reset Variables
    Cell.all = []
    Cell.cellcount = settings.grid_cells - settings.mines_count
    Cell.mines_left = settings.mines_count
    Cell.first_click = True

    # Create new button objects
    for x in range(settings.grid_width):
      for y in range(settings.grid_height):
        c1 = Cell(x,y)
        c1.create_btn_object(location)
        c1.cell_btn_object.grid(column = x, row = y)

    # Reset labels
    Cell.update_cellcount_label()
    Cell.update_minesleft_label()

  #Play random explosion sound
  @staticmethod
  def play_explosion_sound():
    expl_sound = random.choice(['Sounds/explosion1.mp3',
                                'Sounds/explosion2.mp3', 
                                'Sounds/explosion3.mp3',
                                'Sounds/explosion4.mp3'])
    pygame.mixer.init()
    pygame.mixer.music.load(expl_sound)
    pygame.mixer.music.play()

  #Choose random loading screen Function
  @staticmethod
  def choose_random_loading_screen():
    loading_screen = random.choice(['Images/image_Loadingscreen_1.png',
                                    'Images/image_Loadingscreen_2.png',
                                    'Images/image_Loadingscreen_3.png'])
    image = Image.open(loading_screen)
    image = ImageTk.PhotoImage(image)
    return image
    
  #Create Background Label Function
  @staticmethod
  def create_background_label(location):
    image = Cell.choose_random_loading_screen()
    lbl = Label(
      location,
      image = image,
      bg = 'black'
    )
    lbl.image = image