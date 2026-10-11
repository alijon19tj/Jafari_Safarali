# main.py
import customtkinter as ctk
from dictionary import Dictionary
from game_logic import GameLogic
from ui_manager import UIManager

def main():
    ctk.set_appearance_mode("dark")

    dictionary = Dictionary("words.txt")
    game = GameLogic(dictionary)

    root = ctk.CTk()
    root.resizable(False, False)
    ui = UIManager(root, game)
    root.mainloop()

if __name__ == "__main__":
    main()