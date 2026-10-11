# ui_manager.py
import customtkinter as ctk
from bubble_widget import BubbleWidget
from background import OceanBackground

class UIManager:
    def __init__(self, root, game_logic):
        self.root = root
        self.game = game_logic
        self.bubble_widgets = {}
        self.setup_ui()

    def setup_ui(self):
        self.root.geometry("950x700")
        self.root.title("Word Bubbles")

        # ===== Заминаи зериобӣ =====
        self.bg = OceanBackground(self.root)
        self.bg.place(x=0, y=0, relwidth=1, relheight=1)

        # ===== Тугмаи "Skip tutorial" дар болои чап =====
        self.skip_btn = ctk.CTkButton(
            self.root,
            text="Skip tutorial",
            command=self.start_game,
            width=140, height=35,
            fg_color="#0d3a52", hover_color="#1a5a7a",
            text_color="#ffffff",
            font=("Arial", 14, "bold"),
            corner_radius=18
        )
        self.skip_btn.place(x=20, y=20)

        # ===== Компаси гирд дар болои марказ =====
        self.compass = ctk.CTkCanvas(
            self.root, width=90, height=90,
            highlightthickness=0, bg="#1e5a7a"
        )
        self.compass.place(relx=0.5, y=10, anchor="n")
        self._draw_compass()
        self._animate_compass()

        # ===== Панели асосӣ (қуттии тираи кабуд) =====
        self.main_panel = ctk.CTkFrame(
            self.root,
            fg_color="#1a4a5a",
            corner_radius=0,
            border_width=0
        )
        self.main_panel.place(relx=0.5, rely=0.35, anchor="center",
                              relwidth=0.75, relheight=0.4)

        # Матни дастур
        self.instruction = ctk.CTkLabel(
            self.main_panel,
            text="Make a word starting with these letters, and press ENTER",
            font=("Arial", 20),
            text_color="#d0e8f0"
        )
        self.instruction.place(relx=0.5, rely=0.3, anchor="center")

        # Stem (ҳарфҳои оғозкунанда)
        self.stem_display = ctk.CTkLabel(
            self.main_panel,
            text="",
            font=("Arial", 32, "bold"),
            text_color="#ffffff"
        )
        self.stem_display.place(relx=0.5, rely=0.55, anchor="center")

        # ===== Майдони вуруд (сафед) =====
        self.entry = ctk.CTkEntry(
            self.root,
            placeholder_text="",
            width=500, height=60,
            font=("Arial", 28),
            fg_color="#ffffff",
            text_color="#000000",
            border_width=0,
            corner_radius=0
        )
        self.entry.place(relx=0.5, rely=0.6, anchor="center")
        self.entry.bind("<Return>", self.on_submit)

        # ===== Паёми натиҷа =====
        self.message_label = ctk.CTkLabel(
            self.root, text="",
            font=("Arial", 16, "bold"),
            text_color="#ffffff"
        )
        self.message_label.place(relx=0.5, rely=0.7, anchor="center")

        # ===== Вақт ва холҳо =====
        self.time_label = ctk.CTkLabel(
            self.root, text="",
            font=("Arial", 22, "bold"),
            text_color="#ffffff"
        )
        self.time_label.place(relx=0.08, rely=0.72, anchor="center")

        self.score_label = ctk.CTkLabel(
            self.root, text="Score: 0",
            font=("Arial", 22, "bold"),
            text_color="#ffffff"
        )
        self.score_label.place(relx=0.92, rely=0.72, anchor="center")

        # ===== Ҳубобҳо дар поён =====
        self.bubble_frame = ctk.CTkFrame(
            self.root,
            fg_color="#0d2a3a",
            corner_radius=15,
            border_width=2,
            border_color="#1a4a5a"
        )
        self.bubble_frame.place(relx=0.5, rely=0.92, anchor="center",
                                relwidth=0.9, relheight=0.15)

        # Ҳубобҳо: 3-4, 5, 6, 7, 8, 9, 10+
        bubble_labels = ["3,4", "5", "6", "7", "8", "9", "10+"]
        bubble_keys = [4, 5, 6, 7, 8, 9, 10]

        for label, key in zip(bubble_labels, bubble_keys):
            widget = BubbleWidget(self.bubble_frame, label, size=85)
            widget.pack(side="left", expand=True, padx=5, pady=5)
            self.bubble_widgets[key] = widget

        # ===== Тугмаи Start (пинҳон, танҳо пас аз бозӣ нишон медиҳем) =====
        self.start_btn = ctk.CTkButton(
            self.root,
            text="▶ Start Game",
            command=self.start_game,
            width=200, height=45,
            font=("Arial", 16, "bold"),
            fg_color="#2a7a9a", hover_color="#3a8aba"
        )
        self.start_btn.place(relx=0.5, rely=0.8, anchor="center")

    def _draw_compass(self):
        """Компаси гирд мекашад"""
        c = self.compass
        c.delete("all")
        # Доираи беруна
        c.create_oval(5, 5, 85, 85, fill="#0d2a3a", outline="#3a8aba", width=3)
        # Доираи дарунӣ
        c.create_oval(20, 20, 70, 70, fill="#1a4a5a", outline="#5ab0d0", width=2)
        # Сӯзани компас
        c.create_line(45, 45, 45, 20, fill="#f1c40f", width=3)
        c.create_line(45, 45, 45, 70, fill="#ffffff", width=3)
        # Марказ
        c.create_oval(40, 40, 50, 50, fill="#ffffff", outline="")

    def _animate_compass(self):
        """Компасро давр мезанонад (эффекти зебо)"""
        # Инҷо метавонем сӯзанро давр занем, аммо барои соддагӣ
        # танҳо ҳар 2 сония аз нав мекашем
        self.root.after(2000, self._animate_compass)

    def start_game(self):
        self.skip_btn.place_forget()
        self.start_btn.place_forget()
        self.game.reset_game()
        stem, duration = self.game.start_round()
        self.stem_display.configure(text=stem.upper())
        self.time_label.configure(text=f"⏱ {duration}")
        self.score_label.configure(text="Score: 0")
        self.message_label.configure(text="", text_color="#ffffff")
        self.entry.configure(state="normal")
        self.entry.delete(0, "end")
        self.entry.focus()

        for widget in self.bubble_widgets.values():
            widget.set_progress(0)

        self.update_timer()

    def on_submit(self, event=None):
        if not self.game.is_running:
            return

        word = self.entry.get().strip()
        self.entry.delete(0, "end")

        if not word:
            return

        success, msg, points, bubble_updates = self.game.submit_word(word)

        if success:
            self.message_label.configure(text=msg, text_color="#90ee90")
            self.score_label.configure(text=f"Score: {self.game.score}")

            for length in bubble_updates:
                progress = self.game.bubble_levels[length]
                # Барои калимаҳои 10+ калиди 10 истифода мешавад
                key = 10 if length >= 10 else length
                if key in self.bubble_widgets:
                    self.bubble_widgets[key].set_progress(progress)
        else:
            self.message_label.configure(text=msg, text_color="#ff6b6b")

    def update_timer(self):
        if self.game.is_running:
            self.game.tick(1)
            self.time_label.configure(text=f"⏱ {int(self.game.time_left)}")

            if self.game.time_left > 0:
                self.root.after(1000, self.update_timer)
            else:
                self.end_round()

    def end_round(self):
        self.message_label.configure(text="⏰ Вақт тамом шуд!", text_color="#f1c40f")
        self.entry.configure(state="disabled")

        if self.game.next_round():
            self.root.after(2000, self.start_next_round)
        else:
            self.game_over()

    def start_next_round(self):
        stem, duration = self.game.start_round()
        self.stem_display.configure(text=stem.upper())
        self.time_label.configure(text=f"⏱ {duration}")
        self.message_label.configure(
            text=f"Даври {self.game.current_round + 1} оғоз шуд!",
            text_color="#90ee90"
        )
        self.entry.configure(state="normal")
        self.entry.delete(0, "end")
        self.entry.focus()

        for widget in self.bubble_widgets.values():
            widget.set_progress(0)

        self.update_timer()

    def game_over(self):
        self.message_label.configure(
            text=f"🏁 Бозӣ тамом! Холи ниҳоӣ: {self.game.score}",
            text_color="#3a8aba"
        )
        self.entry.configure(state="disabled")
        self.start_btn.configure(text="🔄 Play Again")
        self.start_btn.place(relx=0.5, rely=0.8, anchor="center")