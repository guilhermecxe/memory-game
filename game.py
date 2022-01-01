from PIL import ImageTk, Image
import os
import random
import time

from tkinter.messagebox import askquestion
import tkinter as tk

WAIT_TIME_IN_SECONDS = 1.5
ROWS = 4
COLUMNS = 8

class MemoryGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Memory Game')
        self.iconbitmap('icon.ico')
        self.state('zoomed') # maximized window
        self.configure(background='#44633F')
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.main_frame = tk.Frame(self, bg='#44633F')
        self.main_frame.grid(row=1, column=0, sticky='')

        self.cards_closed = True
        self.last_card_opened_at = 0
        self.rounds_count = 1
        self.pairs_found = 0

        self.__get_images_files()
        self.__create_rounds_label()
        self.__create_cards_frames()

    def __create_rounds_label(self):
        self.rounds_label = tk.Label(self, text='Round: 1', bg='#5CAB7D', fg='white', font='Helvetica 11 bold')
        self.rounds_label.grid(row=0, column=0, sticky='ew')

    def __create_cards_frames(self):
        self.images_matrix = []

        for i in range(ROWS):
            self.images_matrix.append([])
            for j in range(COLUMNS):
                self.images_matrix[i].append(self.__get_image())

                frame_img = tk.Frame(self.main_frame, bg='#e0df7e', width=150, height=150)
                frame_img.grid(row=i, column=j, padx=5, pady=5)
                frame_img.pack_propagate(False) # so the frame don't adapt to the label insert inside it later

                frame_img.bind("<Button>", lambda event, frame=frame_img: self.__card_click(frame))

    def __get_images_files(self):
        self.images = os.listdir('imgs') + os.listdir('imgs')
        assert len(self.images) == (ROWS*COLUMNS), (f"Images amount ({len(self.images)/2}) incompatible "
                                                    f"with the amount of rows and columns ({ROWS}, {COLUMNS})")
        random.shuffle(self.images)
        return self.images

    def __get_image(self):
        image_file = f'imgs/{self.images.pop(0)}'
        image = Image.open(image_file).resize((150, 150), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image)
        return image, image_file

    def __card_click(self, frame):
        if (time.time() - self.last_card_opened_at) <= (WAIT_TIME_IN_SECONDS + 0.5):
            return

        row = frame.grid_info()['row']
        column = frame.grid_info()['column']

        label = tk.Label(frame, bg='yellow')
        label.pack(fill=tk.BOTH, expand=True)
        label.configure(image=self.images_matrix[row][column][0])

        if self.cards_closed:
            self.first_label = label
            self.first_image_opened = self.images_matrix[row][column][1]
            self.cards_closed = False
        else:
            self.last_label = label
            self.last_card_opened_at = time.time()

            if self.first_image_opened == self.images_matrix[row][column][1]:
                self.__next_round(right=True)
            else:
                self.after(int(WAIT_TIME_IN_SECONDS*1000), self.__next_round)

    def __next_round(self, right=False):
        if right:
            self.pairs_found += 1
            if self.pairs_found == (ROWS*COLUMNS)/2:
                answer = askquestion("Congratulations!", "Would you like to play again?")
                if answer == 'yes':
                    self.destroy()
                    self.__init__()
                else:
                    self.quit()
        else:
            self.first_label.destroy()
            self.last_label.destroy()

        self.last_card_opened_at = 0
        self.cards_closed = True

        self.rounds_count += 1
        self.rounds_label.configure(text=f'Round: {self.rounds_count}')