# background.py
import customtkinter as ctk
import random

class OceanBackground(ctk.CTkCanvas):
    """
    Заминаи зериобӣ бо моҳӣ, ҳубобҳо ва растаниҳо.
    Ин Canvas дар паси ҳамаи виҷетҳо ҷойгир мешавад.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, highlightthickness=0, **kwargs)
        self.configure(bg="#1e5a7a")
        self.fish = []
        self.bubbles = []
        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        self.width = event.width
        self.height = event.height
        self.redraw()

    def redraw(self):
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()

        if w < 10 or h < 10:
            return

        # ===== Заминаи gradient (тақлид бо чанд росткунҷа) =====
        # Аз боло тиратар, аз поён равшантар
        for i in range(20):
            ratio = i / 20
            color = self._blend_color("#0d3a52", "#2a7a9a", ratio)
            y1 = int(h * i / 20)
            y2 = int(h * (i + 1) / 20)
            self.create_rectangle(0, y1, w, y2, fill=color, outline="")

        # ===== Нурҳои офтоб =====
        for i in range(5):
            x = w * (0.1 + i * 0.2)
            self.create_polygon(
                x, 0, x + 40, 0, x + 100, h, x + 30, h,
                fill="#3a8aaa", outline="", stipple="gray50"
            )

        # ===== Растаниҳо дар поён =====
        self._draw_seaweed(w, h)

        # ===== Моҳӣ =====
        self._draw_fish(w, h)

        # ===== Ҳубобҳои хурд =====
        for _ in range(15):
            x = random.randint(0, w)
            y = random.randint(0, h)
            r = random.randint(3, 10)
            self.create_oval(x, y, x + r, y + r,
                             outline="#5ab0d0", fill="", width=1)

    def _blend_color(self, c1, c2, ratio):
        """Ду рангро омехта мекунад"""
        r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
        r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        return f"#{r:02x}{g:02x}{b:02x}"

    def _draw_seaweed(self, w, h):
        """Растаниҳои баҳрӣ дар поён"""
        for i in range(6):
            x = 50 + i * (w // 6)
            base_y = h
            for j in range(5):
                offset = random.randint(-15, 15)
                top_y = h - (j + 1) * 40
                self.create_line(
                    x + offset, base_y - j * 40,
                    x + offset * 2, top_y,
                    fill="#1a5a3a", width=3, smooth=True
                )

    def _draw_fish(self, w, h):
        """Моҳӣ дар гӯшаҳо"""
        positions = [
            (80, 200, "#1a3a4a", 1),
            (120, 480, "#0d2a3a", -1),
            (w - 150, 550, "#1a3a4a", 1),
            (w - 80, 300, "#0d2a3a", -1),
        ]
        for x, y, color, direction in positions:
            self._draw_single_fish(x, y, color, direction)

    def _draw_single_fish(self, x, y, color, direction):
        """Як моҳӣ мекашад"""
        d = direction
        # Бадан
        self.create_oval(x - 25, y - 15, x + 25, y + 15,
                         fill=color, outline="#0a1a2a", width=1)
        # Думи
        self.create_polygon(
            x - 25 * d, y,
            x - 45 * d, y - 15,
            x - 45 * d, y + 15,
            fill=color, outline="#0a1a2a"
        )
        # Чашм
        self.create_oval(x + 10 * d - 3, y - 5,
                         x + 10 * d + 3, y + 1,
                         fill="#ffffff", outline="")
        self.create_oval(x + 10 * d - 1, y - 3,
                         x + 10 * d + 2, y,
                         fill="#000000", outline="")
        # Бол
        self.create_polygon(
            x, y - 15,
            x + 10 * d, y - 25,
            x + 15 * d, y - 15,
            fill=color, outline="#0a1a2a"
        )