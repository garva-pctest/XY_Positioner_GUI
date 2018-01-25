"""
    Created by Ganesh Arvapalli on 1/15/18
    ganesh.arvapalli@pctest.com
"""

import Tkinter as tk


class LocationSelectGUI(tk.Tk):
    """Tkinter GUI that allows user to select specific location along scan path.

    Attributes:
        grid = Grid of buttons showing arrangement of scan path
        choiceVar = Desired location within grid
    """

    def __init__(self, parent, grid):
        tk.Tk.__init__(self, parent)
        self.parent = parent
        self.grid = grid
        self.setup()

    def setup(self):
        """Set up GUI and instantiate relevant variables

        :return:
        """
        self.title('Please select a location on the grid')
        self.choiceVar = tk.IntVar()
        self.choiceVar = 0

        # Instructions
        label = tk.Label(self, text='Please select a location to move to.', background='lightgreen', padx=20, pady=10)
        label.grid(row=0, column=0)

        # Set up button grid (value of button = value at grid point) Extra comment
        innerFrame = tk.Frame(self, background='orange')
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                btn = tk.Button(innerFrame, text=str(int(self.grid[i][j])),
                                command=lambda row=i, col=j: self.selected(row, col), padx=10, pady=10)
                btn.config(background='lightblue')
                btn.grid(row=i, column=j, sticky="nsew")

        innerFrame.grid_rowconfigure(len(self.grid), weight=1)
        innerFrame.grid_columnconfigure(len(self.grid[0]), weight=1)
        innerFrame.grid(row=1, column=0)

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.config(background='lightgreen')

    def selected(self, row, col):
        """Set selected value to be value of grid where button was pressed

        :param row: button row position
        :param col: button col position
        :return:
        """
        self.choiceVar = self.grid[row][col]
        self.destroy()
        self.quit()

    def get_gui_value(self):
        """Make selected value available outside of GUI by storing at as part of GUI

        :return: Grid value where button was pressed
        """
        return self.choiceVar