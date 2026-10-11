# bubble_widget.py
import customtkinter as ctk
import math

class BubbleWidget(ctk.CTkCanvas):
    """
    Ҳубоби гирд бо 3 сегменти пуршаванда.
    progress: 0, 1, 2, 3
    """
    def __init__(self, master, label, size=80, **kwargs):
        super().__init__(master, width=size, height=size,
                         highlightthickness=0, bg="#0d2a3a", **kwargs)
        self.label = label
        self.size = size
        self.progress = 0
        self.draw()

    def draw(self):
        self.delete("all")
        s = self.size
        cx, cy = s // 2, s // 2
        r_outer = s // 2 - 3
        r_inner = r_outer - 10

        # ===== Ранги ҳалқа вобаста ба progress =====
        # 0 = тира, 1 = кабуд, 2 = кабуди равшан, 3 = тиллоӣ
        ring_colors = ["#0a1a2a", "#2a5a7a", "#3a8aba", "#f1c40f"]
        fill_colors = ["#0d1f2a", "#1a3a4a", "#1a4a6a", "#8a6a10"]

        ring_color = ring_colors[min(self.progress, 3)]
        fill_color = fill_colors[min(self.progress, 3)]

        # ===== Доираи асосӣ (фон) =====
        self.create_oval(cx - r_outer, cy - r_outer,
                         cx + r_outer, cy + r_outer,
                         fill=ring_color, outline="#0a1a2a", width=2)

        # ===== Доираи дарунӣ (фон) =====
        self.create_oval(cx - r_inner, cy - r_inner,
                         cx + r_inner, cy + r_inner,
                         fill=fill_color, outline="")

        # ===== Сегментҳои пуршаванда =====
        # 3 сегмент, ҳар як 120 дараҷа
        # Сегментҳо дар болои доираи дарунӣ кашида мешаванд
        if self.progress > 0:
            segment_color = "#5ab0d0" if self.progress < 3 else "#ffd700"
            for i in range(self.progress):
                self._draw_segment(cx, cy, r_inner + 2,
                                   start_angle=-90 + i * 120,
                                   extent=120,
                                   color=segment_color)

        # ===== Хатҳои ҷудокунанда (divider) =====
        # 3 хати аз марказ ба берун
        for i in range(3):
            angle = math.radians(-90 + i * 120 + 60)
            x1 = cx + 5 * math.cos(angle)
            y1 = cy + 5 * math.sin(angle)
            x2 = cx + (r_outer - 2) * math.cos(angle)
            y2 = cy + (r_outer - 2) * math.sin(angle)
            self.create_line(x1, y1, x2, y2,
                             fill="#0a1a2a", width=2)

        # ===== Доираи марказӣ (фон барои рақам) =====
        r_center = r_inner - 8
        self.create_oval(cx - r_center, cy - r_center,
                         cx + r_center, cy + r_center,
                         fill="#0d1f2a" if self.progress < 3 else "#f1c40f",
                         outline="#3a8aba", width=1)

        # ===== Рақам ё матн =====
        text_color = "#ffffff" if self.progress < 3 else "#1a1a1a"
        self.create_text(cx, cy, text=self.label,
                         fill=text_color,
                         font=("Arial", 14, "bold"))

        # ===== Агар 3 шуд — ситора дар гӯша =====
        if self.progress >= 3:
            self.create_text(s - 12, 12, text="★",
                             fill="#fff8b0", font=("Arial", 14, "bold"))

    def _draw_segment(self, cx, cy, r, start_angle, extent, color):
        """
        Як сегменти ҳалқаро мекашад.
        start_angle: кунҷи оғоз (дараҷа)
        extent: андозаи кунҷ (дараҷа)
        """
        # Нуқтаҳои камони беруна
        points = []
        steps = 20
        for i in range(steps + 1):
            angle = math.radians(start_angle + extent * i / steps)
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            points.append((x, y))

        # Нуқтаҳои камони даруна (баръакс)
        r_inner = r - 6
        for i in range(steps, -1, -1):
            angle = math.radians(start_angle + extent * i / steps)
            x = cx + r_inner * math.cos(angle)
            y = cy + r_inner * math.sin(angle)
            points.append((x, y))

        # Polygon месозем
        flat_points = []
        for x, y in points:
            flat_points.extend([x, y])

        self.create_polygon(flat_points, fill=color, outline="")

    def set_progress(self, value):
        self.progress = min(value, 3)
        self.draw()