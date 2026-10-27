import tkinter as tk
from tkinter import ttk

class Theme:
    # Colors
    PRIMARY = "#2563EB"       # Indigo / Royal Blue
    PRIMARY_HOVER = "#1D4ED8"
    PRIMARY_LIGHT = "#EFF6FF"
    
    SUCCESS = "#10B981"       # Emerald green
    SUCCESS_LIGHT = "#ECFDF5"
    
    WARNING = "#F59E0B"       # Amber
    WARNING_LIGHT = "#FFFBEB"
    
    DANGER = "#EF4444"        # Red
    DANGER_LIGHT = "#FEF2F2"
    
    INFO = "#06B6D4"          # Cyan
    INFO_LIGHT = "#ECFEFF"

    # Neutrals
    SIDEBAR_BG = "#0F172A"    # Deep Slate
    SIDEBAR_ITEM = "#1E293B"
    SIDEBAR_ACTIVE = "#2563EB"
    SIDEBAR_TEXT = "#F8FAFC"
    SIDEBAR_MUTED = "#94A3B8"

    BG_MAIN = "#F8FAFC"       # Light gray background
    SURFACE = "#FFFFFF"       # White card background
    SURFACE_ALT = "#F1F5F9"   # Table alternate row
    BORDER = "#E2E8F0"        # Card & input border
    
    TEXT_MAIN = "#0F172A"     # Near black
    TEXT_MUTED = "#64748B"    # Slate 500
    TEXT_WHITE = "#FFFFFF"

    # Fonts
    FONT_TITLE = ("Helvetica Neue", 16, "bold")
    FONT_HEADER = ("Helvetica Neue", 13, "bold")
    FONT_SUBTITLE = ("Helvetica Neue", 11, "bold")
    FONT_BODY = ("Helvetica Neue", 11)
    FONT_BODY_BOLD = ("Helvetica Neue", 11, "bold")
    FONT_SMALL = ("Helvetica Neue", 10)
    FONT_STAT_NUM = ("Helvetica Neue", 22, "bold")

    @classmethod
    def apply_theme(cls, root: tk.Tk):
        root.configure(bg=cls.BG_MAIN)
        style = ttk.Style(root)
        
        # Pick standard modern engine theme
        available_themes = style.theme_names()
        if "clam" in available_themes:
            style.theme_use("clam")

        # Treeview styling (Data Table)
        style.configure(
            "Treeview",
            background=cls.SURFACE,
            foreground=cls.TEXT_MAIN,
            fieldbackground=cls.SURFACE,
            font=cls.FONT_BODY,
            rowheight=32,
            borderwidth=0
        )
        style.map(
            "Treeview",
            background=[("selected", cls.PRIMARY_LIGHT)],
            foreground=[("selected", cls.PRIMARY)]
        )
        style.configure(
            "Treeview.Heading",
            background="#E2E8F0",
            foreground="#334155",
            font=cls.FONT_SUBTITLE,
            padding=8,
            relief="flat"
        )
        style.map(
            "Treeview.Heading",
            background=[("active", "#CBD5E1")]
        )

        # Buttons
        style.configure(
            "Primary.TButton",
            background=cls.PRIMARY,
            foreground=cls.TEXT_WHITE,
            font=cls.FONT_BODY_BOLD,
            padding=(12, 7),
            borderwidth=0,
            focuscolor=cls.PRIMARY
        )
        style.map(
            "Primary.TButton",
            background=[("active", cls.PRIMARY_HOVER), ("pressed", "#1E40AF")]
        )

        style.configure(
            "Success.TButton",
            background=cls.SUCCESS,
            foreground=cls.TEXT_WHITE,
            font=cls.FONT_BODY_BOLD,
            padding=(12, 7),
            borderwidth=0
        )
        style.map(
            "Success.TButton",
            background=[("active", "#059669")]
        )

        style.configure(
            "Danger.TButton",
            background=cls.DANGER,
            foreground=cls.TEXT_WHITE,
            font=cls.FONT_BODY_BOLD,
            padding=(12, 7),
            borderwidth=0
        )
        style.map(
            "Danger.TButton",
            background=[("active", "#DC2626")]
        )

        # Entries & Comboboxes
        style.configure(
            "TEntry",
            padding=6,
            fieldbackground=cls.SURFACE,
            foreground=cls.TEXT_MAIN,
            font=cls.FONT_BODY
        )
        style.configure(
            "TCombobox",
            padding=5,
            fieldbackground=cls.SURFACE,
            foreground=cls.TEXT_MAIN,
            font=cls.FONT_BODY
        )

        # Notebook (tabs)
        style.configure(
            "TNotebook",
            background=cls.BG_MAIN,
            borderwidth=0
        )
        style.configure(
            "TNotebook.Tab",
            padding=(16, 8),
            font=cls.FONT_SUBTITLE,
            background=cls.SURFACE_ALT,
            foreground=cls.TEXT_MUTED
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", cls.SURFACE)],
            foreground=[("selected", cls.PRIMARY)]
        )
