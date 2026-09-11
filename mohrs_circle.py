import tkinter as tk
from tkinter import ttk, messagebox
import math
import os
import sys
from PIL import Image, ImageTk


class RoundedEntry(tk.Frame):
    """Compact rounded input field with a ttk.Entry inside."""
    def __init__(self, parent, width=100, height=34, **kwargs):
        super().__init__(parent, width=width, height=height,
                         bg=kwargs.pop("frame_bg", "#EEF3F8"), highlightthickness=0)
        self.pack_propagate(False)

        self._bg = kwargs.pop("bg", "#F7F9FC")
        self._border = kwargs.pop("border", "#C7D3E0")
        self._focus = kwargs.pop("focus", "#3B82F6")
        self._radius = 8

        self.canvas = tk.Canvas(self, bg=self["bg"], highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.entry = ttk.Entry(self, justify="center", style="Modern.TEntry", **kwargs)
        self.entry.place(x=4, y=3, relwidth=1.0, width=-8, relheight=1.0, height=-6)
        self.entry.bind("<FocusIn>", self._on_focus)
        self.entry.bind("<FocusOut>", self._on_blur)
        self.bind("<Configure>", lambda e: self._draw(self._focus if self.entry.focus_get() is self.entry else self._border))
        self._draw(self._border)

    def _rounded_rect(self, x1, y1, x2, y2, r, fill, outline):
        c = self.canvas
        c.create_arc(x1, y1, x1+2*r, y1+2*r, start=90, extent=90, fill=fill, outline=outline)
        c.create_arc(x2-2*r, y1, x2, y1+2*r, start=0, extent=90, fill=fill, outline=outline)
        c.create_arc(x1, y2-2*r, x1+2*r, y2, start=180, extent=90, fill=fill, outline=outline)
        c.create_arc(x2-2*r, y2-2*r, x2, y2, start=270, extent=90, fill=fill, outline=outline)
        c.create_rectangle(x1+r, y1, x2-r, y2, fill=fill, outline=outline)
        c.create_rectangle(x1, y1+r, x2, y2-r, fill=fill, outline=outline)

    def _draw(self, outline):
        self.canvas.delete("all")
        w, h = max(self.winfo_width(), 10), max(self.winfo_height(), 10)
        self._rounded_rect(1, 1, w-1, h-1, self._radius, self._bg, outline)

    def _on_focus(self, _event=None):
        self._draw(self._focus)

    def _on_blur(self, _event=None):
        self._draw(self._border)

    def get(self):
        return self.entry.get()

    def delete(self, first, last=None):
        return self.entry.delete(first, last)

    def insert(self, index, string):
        return self.entry.insert(index, string)

    def focus_set(self):
        return self.entry.focus_set()


class MohrCircleApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Mohr's Circle")
        self.root.geometry("1150x760")
        self.root.minsize(900, 650)

        # App icon / logo
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        logo_path = os.path.join(base_path, "a_clean_modern_vector_style_graphic_icon_illus.png")
        self.logo_photo = None
        if os.path.exists(logo_path):
            try:
                icon_image = Image.open(logo_path).convert("RGBA")
                icon_image.thumbnail((64, 64), Image.Resampling.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(icon_image)
                self.root.iconphoto(True, self.logo_photo)
            except Exception:
                self.logo_photo = None

        # -------------------------
        # Fonts / polished light theme
        # -------------------------
        self.title_font = ("Segoe UI", 24, "bold")
        self.subtitle_font = ("Segoe UI", 10)
        self.label_font = ("Segoe UI", 10, "bold")
        self.graph_font = ("Segoe UI", 13, "bold")
        self.graph_small_font = ("Segoe UI", 11, "bold")
        self.axis_font = ("Segoe UI", 8)
        self.axis_tick_font = ("Segoe UI", 7)
        self.result_font = ("Segoe UI", 12, "bold")

        self.unit = tk.StringVar(value="MPa")

        # Clean, modern light palette
        self.theme = {
            "bg": "#EAF1F7",
            "surface": "#F8FAFC",
            "surface2": "#DDE8F2",
            "text": "#172B3A",
            "muted": "#65788A",
            "border": "#C7D4E0",
            "accent": "#3B82F6",
            "accent_hover": "#2563EB",
            "entry": "#F4F7FA",
            "canvas": "#F7FAFC",
            "button_text": "#FFFFFF"
        }

        # =========================
        # Main frame
        # =========================
        self.setup_styles()

        main = ttk.Frame(root, padding=15, style="Main.TFrame")
        main.pack(fill="both", expand=True)

        # =========================
        # TITLE
        # =========================
        header = ttk.Frame(main, style="Main.TFrame")
        header.pack(fill="x", pady=(0, 4))

        if self.logo_photo is not None:
            logo_label = tk.Label(
                header,
                image=self.logo_photo,
                bg=self.theme["bg"],
                bd=0,
                highlightthickness=0
            )
            logo_label.pack(side="left", padx=(0, 12))

        title_box = ttk.Frame(header, style="Main.TFrame")
        title_box.pack(side="left", expand=True)
        ttk.Label(title_box, text="MOHR'S CIRCLE", font=self.title_font,
                  style="Title.TLabel").pack(anchor="w")

        ttk.Label(title_box, text="Plane Stress Analysis", font=self.subtitle_font,
                  style="Subtitle.TLabel").pack(anchor="w", pady=(0, 8))

        # =====================================================
        # GRAPH - TOP
        # =====================================================
        graph_frame = ttk.LabelFrame(
            main,
            text="Mohr's Circle Diagram",
            padding=10,
            style="Card.TLabelframe"
        )
        graph_frame.pack(
            fill="both",
            expand=True,
            pady=(0, 12)
        )

        self.canvas = tk.Canvas(
            graph_frame,
            background=self.theme["canvas"],
            highlightthickness=0
        )
        self.canvas.pack(
            fill="both",
            expand=True
        )

        # Redraw graph when window size changes
        self.canvas.bind(
            "<Configure>",
            self.redraw_graph
        )

        # =========================
        # RESULTS - BOTTOM
        # =========================
        result_frame = ttk.Frame(main, style="Card.TFrame")
        result_frame.pack(fill="x", pady=(0, 10))

        self.avg_label = ttk.Label(
            result_frame,
            text="σavg\n—",
            font=self.result_font,
            justify="center",
            style="Result.TLabel"
        )
        self.avg_label.pack(side="left", expand=True)

        self.radius_label = ttk.Label(
            result_frame,
            text="R\n—",
            font=self.result_font,
            justify="center",
            style="Result.TLabel"
        )
        self.radius_label.pack(side="left", expand=True)

        self.max_label = ttk.Label(
            result_frame,
            text="σmax\n—",
            font=self.result_font,
            justify="center",
            style="Result.TLabel"
        )
        self.max_label.pack(side="left", expand=True)

        self.min_label = ttk.Label(
            result_frame,
            text="σmin\n—",
            font=self.result_font,
            justify="center",
            style="Result.TLabel"
        )
        self.min_label.pack(side="left", expand=True)

        self.angle_label = ttk.Label(
            result_frame,
            text="θ\n—",
            font=self.result_font,
            justify="center",
            style="Result.TLabel"
        )
        self.angle_label.pack(side="left", expand=True)

        # =====================================================
        # INPUT - BOTTOM
        # =====================================================
        input_frame = ttk.LabelFrame(
            main,
            text="Input Values",
            padding=11,
            style="Card.TLabelframe"
        )
        input_frame.pack(fill="x")

        # Center the complete input group
        for col in range(11):
            input_frame.columnconfigure(col, weight=1)

        # Unit system — compact dropdown
        ttk.Label(
            input_frame,
            text="Unit:",
            font=self.label_font
        ).grid(
            row=0,
            column=0,
            padx=(5, 8),
            pady=5
        )

        self.unit_combo = ttk.Combobox(
            input_frame,
            textvariable=self.unit,
            values=("MPa", "ksi"),
            state="readonly",
            width=7,
            justify="center",
            style="Modern.TCombobox"
        )
        self.unit_combo.grid(
            row=0,
            column=1,
            columnspan=2,
            padx=(0, 26),
            pady=2
        )
        self.unit_combo.bind("<<ComboboxSelected>>", lambda e: self.redraw_graph())

        # Sigma X
        ttk.Label(
            input_frame,
            text="σx",
            font=self.label_font
        ).grid(
            row=0,
            column=3,
            padx=(10, 5)
        )

        self.sigma_x_entry = RoundedEntry(
            input_frame, width=96, height=34,
            frame_bg=self.theme["surface"], bg=self.theme["entry"],
            border=self.theme["border"], focus=self.theme["accent"]
        )
        self.sigma_x_entry.grid(
            row=0, column=4, padx=(0, 20), pady=1
        )

        # Sigma Y
        ttk.Label(
            input_frame,
            text="σy",
            font=self.label_font
        ).grid(
            row=0,
            column=5,
            padx=(5, 5)
        )

        self.sigma_y_entry = RoundedEntry(
            input_frame, width=96, height=34,
            frame_bg=self.theme["surface"], bg=self.theme["entry"],
            border=self.theme["border"], focus=self.theme["accent"]
        )
        self.sigma_y_entry.grid(
            row=0, column=6, padx=(0, 20), pady=1
        )

        # Tau XY
        ttk.Label(
            input_frame,
            text="τxy",
            font=self.label_font
        ).grid(
            row=0,
            column=7,
            padx=(5, 5)
        )

        self.tau_entry = RoundedEntry(
            input_frame, width=96, height=34,
            frame_bg=self.theme["surface"], bg=self.theme["entry"],
            border=self.theme["border"], focus=self.theme["accent"]
        )
        self.tau_entry.grid(
            row=0, column=8, padx=(0, 20), pady=1
        )

        # Calculate button
        self.calculate_button = self.make_button(
            input_frame, "Calculate", self.calculate, width=105
        )
        self.calculate_button.grid(row=0, column=9, padx=(5, 4))

        self.clear_button = self.make_button(
            input_frame, "Clear", self.clear, width=85, secondary=True
        )
        self.clear_button.grid(row=0, column=10, padx=4)

        # Save last values for redraw
        self.data = None

        # Draw axes after startup
        self.root.after(
            150,
            self.draw_empty_graph
        )

        # Press Enter to calculate
        self.root.bind(
            "<Return>",
            lambda event: self.calculate()
        )

    # ==========================================================
    # MODERN UI / THEME
    # ==========================================================

    def setup_styles(self):
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        t = self.theme
        style.configure("Main.TFrame", background=t["bg"])
        style.configure("Card.TFrame", background=t["surface"])
        style.configure("Title.TLabel", background=t["bg"], foreground=t["text"])
        style.configure("Subtitle.TLabel", background=t["bg"], foreground=t["muted"])
        style.configure("Result.TLabel", background=t["surface"], foreground=t["text"], padding=(4, 8))
        style.configure("TLabel", background=t["surface"], foreground=t["text"])
        style.configure("Card.TLabelframe", background=t["surface"], foreground=t["text"], bordercolor=t["border"], relief="solid", borderwidth=1)
        style.configure("Card.TLabelframe.Label", background=t["surface"], foreground=t["text"], font=("Segoe UI", 10, "bold"))
        style.configure("TEntry", fieldbackground=t["entry"], foreground=t["text"], bordercolor=t["border"], lightcolor=t["accent"], darkcolor=t["border"], padding=7)
        style.configure("Modern.TEntry", fieldbackground="#F7F9FC", foreground=t["text"], borderwidth=0, relief="flat", padding=(5, 2))
        style.map("TEntry", fieldbackground=[("focus", "#F7F9FC")], bordercolor=[("focus", t["accent"])], lightcolor=[("focus", t["accent"])], darkcolor=[("focus", t["accent"])])
        style.configure("TRadiobutton", background=t["surface"], foreground=t["text"], focuscolor=t["surface"])
        style.map("TRadiobutton", background=[("active", t["surface"])], foreground=[("active", t["text"])])
        style.configure("Modern.TCombobox", fieldbackground="#F4F7FA", background="#F4F7FA", foreground=t["text"], bordercolor=t["border"], arrowcolor=t["accent"], padding=(7, 5), relief="flat")
        style.map("Modern.TCombobox", fieldbackground=[("readonly", "#F4F7FA")], foreground=[("readonly", t["text"])], bordercolor=[("focus", t["accent"])])
        self.root.configure(bg=t["bg"])

    def make_button(self, parent, text, command, width=105, secondary=False):
        """Clean rectangular button with a subtle hover effect."""
        button = tk.Button(
            parent,
            text=text,
            command=command,
            width=max(1, width // 9),
            height=1,
            font=("Segoe UI", 9, "bold"),
            bg=self.theme["surface2"] if secondary else self.theme["accent"],
            fg=self.theme["text"] if secondary else self.theme["button_text"],
            activebackground=self.theme["border"] if secondary else self.theme["accent_hover"],
            activeforeground=self.theme["text"] if secondary else self.theme["button_text"],
            relief="solid",
            bd=1,
            highlightthickness=0,
            cursor="hand2"
        )

        normal_bg = self.theme["surface2"] if secondary else self.theme["accent"]
        hover_bg = self.theme["border"] if secondary else self.theme["accent_hover"]

        button.bind("<Enter>", lambda e: button.configure(bg=hover_bg))
        button.bind("<Leave>", lambda e: button.configure(bg=normal_bg))
        return button

    # ==========================================================
    # CALCULATE
    # ==========================================================

    def calculate(self):

        try:
            sigma_x = float(self.sigma_x_entry.get())
            sigma_y = float(self.sigma_y_entry.get())
            tau_xy = float(self.tau_entry.get())

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Please enter valid numerical values."
            )
            return

        # Center
        sigma_avg = (sigma_x + sigma_y) / 2

        # Radius
        radius = math.sqrt(
            ((sigma_x - sigma_y) / 2) ** 2 +
            tau_xy ** 2
        )

        # Principal stresses
        sigma_max = sigma_avg + radius
        sigma_min = sigma_avg - radius

        # Angle θ = angle between the positive horizontal (σ) axis
        # and the diameter XY (equivalently, the radius CX).
        # This is the Mohr-circle angle, so it is atan2(2τxy, σx-σy).
        theta = math.degrees(
            math.atan2(
                2 * tau_xy,
                sigma_x - sigma_y
            )
        )

        unit = self.unit.get()

        # =========================
        # Results
        # =========================
        self.avg_label.config(
            text=f"σavg\n{sigma_avg:.2f} {unit}"
        )

        self.radius_label.config(
            text=f"Radius R\n{radius:.2f} {unit}"
        )

        self.max_label.config(
            text=f"σmax\n{sigma_max:.2f} {unit}"
        )

        self.min_label.config(
            text=f"σmin\n{sigma_min:.2f} {unit}"
        )

        self.angle_label.config(
            text=f"θp\n{theta:.2f}°"
        )

        # Save data for redraw
        self.data = {
            "sigma_x": sigma_x,
            "sigma_y": sigma_y,
            "tau_xy": tau_xy,
            "center": sigma_avg,
            "radius": radius,
            "sigma_max": sigma_max,
            "sigma_min": sigma_min,
            "theta": theta
        }

        self.draw_mohr_circle()

    # ==========================================================
    # REDRAW WHEN RESIZED
    # ==========================================================

    def redraw_graph(self, event=None):

        if self.data is None:
            self.draw_empty_graph()
        else:
            self.draw_mohr_circle()

    # ==========================================================
    # EMPTY GRAPH
    # ==========================================================

    def draw_empty_graph(self):

        self.canvas.delete("all")

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        if width < 100 or height < 100:
            return

        origin_x = width / 2
        origin_y = height / 2

        # Horizontal axis
        self.canvas.create_line(
            40, origin_y,
            width - 40, origin_y,
            arrow=tk.LAST,
            width=1
        )

        # Vertical axis
        self.canvas.create_line(
            origin_x, height - 35,
            origin_x, 35,
            arrow=tk.LAST,
            width=1
        )

        self.canvas.create_text(
            width - 55,
            origin_y - 15,
            text="σ",
            font=self.graph_font
        )

        self.canvas.create_text(
            origin_x + 15,
            35,
            text="τ",
            font=self.graph_font
        )

        self.canvas.create_text(
            width / 2,
            25,
            text="Enter stress values below to draw Mohr's Circle",
            font=self.graph_small_font
        )

    # ==========================================================
    # DRAW MOHR CIRCLE
    # ==========================================================

    def draw_mohr_circle(self):

        if self.data is None:
            return

        self.canvas.delete("all")

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        if width < 100 or height < 100:
            return

        sigma_x = self.data["sigma_x"]
        sigma_y = self.data["sigma_y"]
        tau_xy = self.data["tau_xy"]
        center = self.data["center"]
        radius = self.data["radius"]
        sigma_max = self.data["sigma_max"]
        sigma_min = self.data["sigma_min"]
        theta = self.data["theta"]

        # ======================================================
        # GRAPH RANGE
        # ======================================================

        graph_limit = max(
            abs(sigma_max), abs(sigma_min), abs(tau_xy), radius, abs(center)
        )
        if graph_limit == 0:
            graph_limit = 1
        graph_limit *= 1.30

        available_width = width - 190
        available_height = height - 90
        scale_x = available_width / (2 * graph_limit)
        scale_y = available_height / (2 * graph_limit)
        scale = min(scale_x, scale_y)

        origin_x = width / 2
        origin_y = height / 2

        def X(value):
            return origin_x + value * scale

        def Y(value):
            return origin_y - value * scale

        # ======================================================
        # COLORS
        # ======================================================

        axis_color = "#9AA9B7"
        tick_color = "#CBD5DF"
        circle_color = "#426A9E"
        diameter_color = "#7B8794"
        point_x_color = "#C44B5C"
        point_y_color = "#4D8A5B"
        principal_color = "#343A40"
        text_color = self.theme["text"]
        secondary_text = self.theme["muted"]
        angle_color = "#A66A2C"

        # ======================================================
        # AXES
        # ======================================================

        self.canvas.create_line(
            40, origin_y, width - 40, origin_y,
            arrow=tk.LAST, width=1, fill=axis_color
        )
        self.canvas.create_line(
            origin_x, height - 35, origin_x, 35,
            arrow=tk.LAST, width=1, fill=axis_color
        )

        self.canvas.create_text(
            width - 55, origin_y - 18,
            text="σ", font=self.axis_font, fill=text_color
        )
        self.canvas.create_text(
            origin_x + 20, 35,
            text="τ", font=self.axis_font, fill=text_color
        )

        # ======================================================
        # AXIS TICKS / NUMBERS
        # Horizontal-axis numbers are BELOW the σ-axis.
        # Vertical-axis numbers remain beside the τ-axis.
        # ======================================================

        # Only mark the stress values where the Mohr circle intersects the axes.
        for value in (sigma_min, sigma_max):
            x = X(value)
            self.canvas.create_line(
                x, origin_y - 4, x, origin_y + 4,
                width=1, fill=tick_color
            )
            self.canvas.create_text(
                x, origin_y + 18,
                text=f"{value:.2f}",
                font=self.axis_tick_font,
                fill=secondary_text
            )

        for value in (radius, -radius):
            y = Y(value)
            self.canvas.create_line(
                origin_x - 4, y, origin_x + 4, y,
                width=1, fill=tick_color
            )
            self.canvas.create_text(
                origin_x - 24, y,
                text=f"{value:.2f}",
                font=self.axis_tick_font,
                fill=secondary_text
            )

        # ======================================================
        # CIRCLE
        # ======================================================

        left = X(center - radius)
        right = X(center + radius)
        top = Y(radius)
        bottom = Y(-radius)

        self.canvas.create_oval(
            left, top, right, bottom,
            width=3, outline=circle_color
        )

        # ======================================================
        # CENTER: only the symbol C is shown on the graph.
        # The numerical center value is kept in the output section.
        # ======================================================

        cx = X(center)
        cy = Y(0)

        self.canvas.create_oval(
            cx - 4, cy - 4, cx + 4, cy + 4,
            fill=text_color, outline=""
        )
        self.canvas.create_text(
            cx, cy - 20,
            text="C",
            font=self.graph_font,
            fill=text_color
        )

        # ======================================================
        # X AND Y POINTS — opposite ends of the XY diameter
        # ======================================================

        px = X(sigma_x)
        py = Y(tau_xy)
        qx = X(sigma_y)
        qy = Y(-tau_xy)

        self.canvas.create_line(
            px, py, qx, qy,
            fill=diameter_color, width=2
        )

        # Radius CX: this is part of the XY diameter.
        self.canvas.create_line(
            cx, cy, px, py,
            fill="#8B9299", width=2, dash=(5, 3)
        )

        self.canvas.create_oval(
            px - 6, py - 6, px + 6, py + 6,
            fill=point_x_color, outline=""
        )
        self.canvas.create_oval(
            qx - 6, qy - 6, qx + 6, qy + 6,
            fill=point_y_color, outline=""
        )

        # ======================================================
        # X / Y COORDINATES — outside the circle
        # ======================================================

        def outside_label(point_x, point_y, text, color, prefer_right=True):
            dx = point_x - cx
            dy = point_y - cy
            length = math.hypot(dx, dy)
            if length == 0:
                dx, dy, length = 1, 0, 1

            ux, uy = dx / length, dy / length
            offset = 20
            lx = point_x + ux * offset
            ly = point_y + uy * offset

            # Keep the text visibly outside the circle and away from the point.
            anchor = "w" if ux >= 0 else "e"
            if abs(ux) < 0.25:
                anchor = "center"

            self.canvas.create_text(
                lx, ly,
                text=text,
                anchor=anchor,
                font=self.graph_small_font,
                fill=color
            )

        outside_label(
            px, py,
            f"X ({sigma_x:.2f}, {tau_xy:.2f})",
            point_x_color
        )
        outside_label(
            qx, qy,
            f"Y ({sigma_y:.2f}, {-tau_xy:.2f})",
            point_y_color
        )

        # ======================================================
        # PRINCIPAL STRESSES
        # Only σmin / σmax values are marked on the σ-axis.
        # Their labels are ABOVE the axis and OUTSIDE the circle.
        # ======================================================

        max_x = X(sigma_max)
        min_x = X(sigma_min)

        self.canvas.create_oval(
            max_x - 5, cy - 5, max_x + 5, cy + 5,
            fill=principal_color, outline=""
        )
        self.canvas.create_oval(
            min_x - 5, cy - 5, min_x + 5, cy + 5,
            fill=principal_color, outline=""
        )

        # Stagger labels when the principal points are close together.
        if abs(max_x - min_x) < 85:
            max_label_y = cy - 42
            min_label_y = cy - 24
        else:
            max_label_y = cy - 25
            min_label_y = cy - 25

        self.canvas.create_text(
            max_x, max_label_y,
            text=f"σmax = {sigma_max:.2f}",
            font=self.axis_tick_font,
            fill=principal_color
        )
        self.canvas.create_text(
            min_x, min_label_y,
            text=f"σmin = {sigma_min:.2f}",
            font=self.axis_tick_font,
            fill=principal_color
        )


        # ======================================================
        # RADIUS LABEL
        # Put R directly ON the CX diameter, but offset slightly
        # along the diameter so it does not cover the line/points.
        # ======================================================

        dx = px - cx
        dy = py - cy
        length = math.hypot(dx, dy)

        if length > 0:
            ux, uy = dx / length, dy / length
            # Slightly toward C from the midpoint, with a tiny normal offset.
            radius_label_x = cx + dx * 0.53 - uy * 10
            radius_label_y = cy + dy * 0.53 + ux * 10
        else:
            radius_label_x, radius_label_y = cx, cy - 12

        self.canvas.create_text(
            radius_label_x, radius_label_y,
            text=f"R = {radius:.2f}",
            font=self.graph_small_font,
            fill=secondary_text
        )

        # ======================================================
        # THETA
        # The theta value is kept in the output panel, but its numeric
        # value is intentionally not displayed on the graph.
        # ======================================================

        # ======================================================
        # UNIT
        # ======================================================

        self.canvas.create_text(
            width - 65, height - 20,
            text=self.unit.get(),
            font=self.graph_small_font,
            fill=secondary_text
        )

    # ==========================================================
    # CLEAR
    # ==========================================================

    def clear(self):

        self.sigma_x_entry.delete(0, tk.END)
        self.sigma_y_entry.delete(0, tk.END)
        self.tau_entry.delete(0, tk.END)

        self.avg_label.config(text="σavg\n—")
        self.radius_label.config(text="R\n—")
        self.max_label.config(text="σmax\n—")
        self.min_label.config(text="σmin\n—")
        self.angle_label.config(text="θ\n—")

        self.data = None

        self.draw_empty_graph()


# ==============================================================
# RUN
# ==============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = MohrCircleApp(root)

    root.mainloop()