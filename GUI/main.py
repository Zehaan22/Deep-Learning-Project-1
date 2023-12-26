"""File for the main GUI of the project."""

import pygame
import pygame_gui as pg
import torch
import numpy as np
pygame.init()

# Defining Window variables
WIDTH, HEIGHT = 1200, 750

# Creating the Window object
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Number Recognition Software")


class Tile:
    """Class to reflect the tile elements of the grid in which the user will draw the numbers."""
    SIDE = 20  # width of the tile in pixels
    RPadding = 50  # Right Padding in px
    TPadding = 100  # Top Padding in px

    def __init__(self, x, y):
        """Create an instance of the tile element."""
        # Setting the co-ordinates for the tile
        self.x = x
        self.y = y
        self.color = 0
        self.rect = (x, y, self.SIDE, self.SIDE)

        # Creating a pygame surface for the drawing tile
        self.tile = pygame.surface.Surface((self.SIDE, self.SIDE))

    def make_tile(self):
        """Blit the tile object on the window."""
        x, y = self.index_to_coords(self.x, self.y)
        self.tile.fill(pygame.Color(
            self.color*255, self.color*255, self.color*255)
        )
        WINDOW.blit(self.tile, (x, y))

    def switch_color(self):
        """Switch the color of the tile."""
        self.color = 1-self.color

    def index_to_coords(self, i, j):
        """Convert the value from matrix indices to positional co-ords. (Top-left corner)"""
        x = i*self.SIDE + self.RPadding
        y = j*self.SIDE + self.TPadding
        return (x, y)


class DrawingSurface:
    """Class to contain the drawing grid for the game."""
    DIMS = (30, 30)  # Dimensions of the grid
    SIDE = 20  # width of the tile in pixels
    RPadding = 50  # Right Padding in px
    TPadding = 100  # Top Padding in px

    def __init__(self):
        """Create an instance of the grid."""
        self.grid = []  # Creating the grid with elements as Tile Objects
        for i in range(self.DIMS[0]):
            foo = []
            for j in range(self.DIMS[1]):
                tile = Tile(i, j)
                foo.append(tile)
            self.grid.append(foo)

    def make_surface(self):
        """Draw the drawing surface on the main Window."""
        for i in range(self.DIMS[0]):
            for j in range(self.DIMS[1]):
                self.grid[i][j].make_tile()

    def coords_to_index(self, x, y):
        """Convert the value from positional co-ords to matrix indices."""
        i = (x - self.RPadding)//self.SIDE
        j = (y - self.TPadding)//self.SIDE
        return (i, j)

    def clear_board(self):
        """Clear the drawing surface on the main Window."""
        for i in range(self.DIMS[0]):
            for j in range(self.DIMS[1]):
                self.grid[i][j].color = 0

    def store_board(self, value):
        """Store the drawing surface."""

        # Creating the array to store the value
        array = []
        for i in range(self.DIMS[0]):
            for j in range(self.DIMS[1]):
                array.append(self.grid[i][j].color)

        # Loading the data tensore
        X_data = torch.load("X_data.pt")
        X_data = X_data.numpy()
        # Adding our element to the data
        X_data = np.append(X_data, [array], axis=0)
        X_data = torch.from_numpy(X_data)
        # Saving the data matrix
        torch.save(X_data, "X_data.pt")
        print("Saved the matrix")

        # Saving the label
        y_data = torch.load("y_data.pt")
        y_data = y_data.numpy()
        # Adding our element to the data
        label = value
        y_data = np.append(y_data, [label])
        y_data = torch.from_numpy(y_data)
        # Saving the data matrix
        torch.save(y_data, "y_data.pt")
        print(f"Saved as the lable {label}")


class MainRun:
    """Class to contain the main functions to run and manage the GUI window."""

    def __init__(self):
        """Create an instance of the main GUI window."""
        # Setting the loop variables
        self.run = True
        self.CLOCK = pygame.time.Clock()
        self.FPS = 80

        # Creating the tiles
        self.sketch_board = DrawingSurface()

        # Creating the GUI Manager
        self.manager = pg.UIManager((WIDTH, HEIGHT))

        # Creating the GUI Elements
        foo_rect = pygame.Rect((750, 650), (200, 60))
        self.clear_btn = pg.elements.UIButton(
            relative_rect=foo_rect,
            text='Clear Board',
            manager=self.manager)  # Button to clear the board

        foo_rect = pygame.Rect((950, 650), (200, 60))
        self.store_btn = pg.elements.UIButton(
            relative_rect=foo_rect,
            text='Store Matrix',
            manager=self.manager)  # Button to store the board

        foo_rect = pygame.Rect((50, 50), (800, 50))
        self.title_bar = pg.elements.UITextBox(
            "<b>DL Based Digit Predictor 2000 : Beta Build (First Working Model)</b>",
            foo_rect,
            self.manager,
        )  # Title bar

        foo_rect = pygame.Rect((750, 450), (400, 200))
        self.pred_bar = pg.elements.UITextBox(
            "My Best Guess is : <br> <b>3</b>",
            foo_rect,
            self.manager
        )  # Prediction bar

        foo_rect = pygame.Rect((750, 250), (100, 30))
        self.input_box = pg.elements.UITextEntryBox(
            foo_rect,
            "1",
            self.manager
        )  # Input Box to take the number

    def update_display(self):
        """Update varoius elements of the display."""
        # Filling the background colour
        WINDOW.fill(pygame.Color(126, 34, 90))

        # Creating the tiles
        self.sketch_board.make_surface()

        # Drawing the UI elements
        self.manager.draw_ui(WINDOW)

        # Updating the display
        pygame.display.update()

    def make_stroke(self, i, j):
        """Change the color of the tiles over which mouse is moved."""
        if (0 <= i and i < self.sketch_board.DIMS[0]):
            if (0 <= j and j < self.sketch_board.DIMS[1]):
                self.sketch_board.grid[i][j].color = 1

    def handel_UI_events(self, event):
        """Handel UI events thorugh PyGame_GUI."""
        if event.user_type == pg.UI_BUTTON_PRESSED:
            # Clear the board
            if event.ui_element == self.clear_btn:
                self.sketch_board.clear_board()

            # Store the board
            if event.ui_element == self.store_btn:
                value = self.input_box.get_text()  # Getting the input from the user
                self.sketch_board.store_board(int(value))

    def run_window(self):
        """Run an iteration of the window."""
        while self.run:
            # Time Control set to FPS
            time_del = self.CLOCK.tick(self.FPS)/1000

            # Events Loop to iterate over user events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:  # To end the game
                    self.run = False

                # Event to handel a continuous stroke and single clicks
                if (event.type == pygame.MOUSEMOTION and event.buttons[0]) or (event.type == pygame.MOUSEBUTTONDOWN):
                    x, y = event.pos
                    i, j = self.sketch_board.coords_to_index(x, y)
                    self.make_stroke(i, j)

                # Handeling UI Events
                if event.type == pygame.USEREVENT:
                    self.handel_UI_events(event)

                self.manager.process_events(event)

            # Updating the display and the
            self.manager.update(time_del)

            self.update_display()


game1 = MainRun()

game1.run_window()
