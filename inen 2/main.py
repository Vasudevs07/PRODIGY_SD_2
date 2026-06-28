import tkinter as tk
from tkinter import ttk

APP_TITLE   = "Temperature Converter"
WINDOW_SIZE = "600x500"

# VS Code dark theme colors
BG_EDITOR   = "#1e1e1e"   # editor background
BG_SIDEBAR  = "#252526"   # sidebar / panel
BG_INPUT    = "#3c3c3c"   # input background
BG_HOVER    = "#2a2d2e"   # hover
ACCENT      = "#007acc"   # VS Code blue
ACCENT_HOV  = "#1a8fd1"
TEXT_PRI    = "#d4d4d4"   # primary text
TEXT_SEC    = "#858585"   # secondary / comments
TEXT_KEY    = "#569cd6"   # keyword blue
TEXT_STR    = "#ce9178"   # string orange
TEXT_NUM    = "#b5cea8"   # number green
SUCCESS     = "#4ec9b0"   # teal
DANGER      = "#f44747"   # red squiggle
BORDER      = "#474747"
TAB_ACTIVE  = "#1e1e1e"
TAB_BG      = "#2d2d2d"

UNITS = ["Celsius", "Fahrenheit", "Kelvin"]
SYMBOLS = {"Celsius": "°C", "Fahrenheit": "°F", "Kelvin": "K"}


class Converter:
    @staticmethod
    def to_celsius(value: float, from_unit: str) -> float:
        if from_unit == "Celsius":    return value
        if from_unit == "Fahrenheit": return (value - 32) * 5 / 9
        if from_unit == "Kelvin":     return value - 273.15

    @staticmethod
    def from_celsius(celsius: float, to_unit: str) -> float:
        if to_unit == "Celsius":    return celsius
        if to_unit == "Fahrenheit": return celsius * 9 / 5 + 32
        if to_unit == "Kelvin":     return celsius + 273.15

    @classmethod
    def convert(cls, value: float, from_unit: str, to_unit: str) -> float:
        return cls.from_celsius(cls.to_celsius(value, from_unit), to_unit)

    @staticmethod
    def validate(value: float, unit: str) -> None:
        celsius = Converter.to_celsius(value, unit)
        if celsius < -273.15:
            raise ValueError("Temperature below absolute zero (−273.15 °C).")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(WINDOW_SIZE)
        self.resizable(False, False)
        self.configure(bg=BG_EDITOR)
        self._build_ui()

    def _build_ui(self) -> None:
        # ── Title bar (activity bar style) ──
        titlebar = tk.Frame(self, bg=BG_SIDEBAR, height=35)
        titlebar.pack(fill="x")
        titlebar.pack_propagate(False)

        tk.Label(titlebar, text="  🌡  temperature_converter.py",
                 bg=BG_SIDEBAR, fg=TEXT_SEC,
                 font=("Consolas", 10)).pack(side="left", padx=8, pady=6)

        tk.Label(titlebar, text="Python  UTF-8  LF",
                 bg=BG_SIDEBAR, fg=TEXT_SEC,
                 font=("Consolas", 9)).pack(side="right", padx=14)

        # ── Tab bar ──
        tabbar = tk.Frame(self, bg=TAB_BG, height=34)
        tabbar.pack(fill="x")
        tabbar.pack_propagate(False)

        tab = tk.Frame(tabbar, bg=TAB_ACTIVE, padx=14)
        tab.pack(side="left", fill="y")
        tk.Label(tab, text="main.py", bg=TAB_ACTIVE, fg=TEXT_PRI,
                 font=("Consolas", 10)).pack(side="left", pady=6)
        tk.Label(tab, text="  ●", bg=TAB_ACTIVE, fg=ACCENT,
                 font=("Consolas", 10)).pack(side="left")

        # ── Line numbers + editor area ──
        body = tk.Frame(self, bg=BG_EDITOR)
        body.pack(fill="both", expand=True)

        # Line number gutter
        gutter = tk.Frame(body, bg=BG_EDITOR, width=48)
        gutter.pack(side="left", fill="y")
        gutter.pack_propagate(False)

        self._line_labels = []
        for i in range(1, 30):
            lbl = tk.Label(gutter, text=str(i), bg=BG_EDITOR,
                           fg=TEXT_SEC, font=("Consolas", 11),
                           anchor="e", width=3)
            lbl.pack(anchor="e", padx=(0, 8), pady=0)
            self._line_labels.append(lbl)

        # Thin separator
        tk.Frame(body, bg=BORDER, width=1).pack(side="left", fill="y")

        # Editor pane
        editor = tk.Frame(body, bg=BG_EDITOR, padx=24)
        editor.pack(side="left", fill="both", expand=True)

        self._build_editor(editor)

        # ── Status bar ──
        statusbar = tk.Frame(self, bg=ACCENT, height=24)
        statusbar.pack(fill="x", side="bottom")
        statusbar.pack_propagate(False)

        self.lbl_status = tk.Label(statusbar, text="  Ready",
                                   bg=ACCENT, fg="#ffffff",
                                   font=("Consolas", 9))
        self.lbl_status.pack(side="left", padx=6)

        tk.Label(statusbar, text="Ln 1, Col 1  |  Python 3",
                 bg=ACCENT, fg="#ffffff",
                 font=("Consolas", 9)).pack(side="right", padx=10)

    def _build_editor(self, parent) -> None:
        r = 0

        # Blank line
        self._code_line(parent, r, ""); r += 1

        # Comment
        self._code_line(parent, r, "# Enter a temperature value", color=TEXT_SEC); r += 1
        self._blank(parent, r); r += 1

        # Input field row
        row_frame = tk.Frame(parent, bg=BG_EDITOR)
        row_frame.grid(row=r, column=0, sticky="w", pady=2); r += 1

        tk.Label(row_frame, text="value", bg=BG_EDITOR, fg=TEXT_KEY,
                 font=("Consolas", 12)).pack(side="left")
        tk.Label(row_frame, text=" = ", bg=BG_EDITOR, fg=TEXT_PRI,
                 font=("Consolas", 12)).pack(side="left")

        self.entry_var = tk.StringVar()
        entry = tk.Entry(row_frame, textvariable=self.entry_var,
                         bg=BG_INPUT, fg=TEXT_NUM, insertbackground=TEXT_PRI,
                         relief="flat", font=("Consolas", 12),
                         highlightthickness=1, highlightcolor=ACCENT,
                         highlightbackground=BORDER, width=14)
        entry.pack(side="left", ipady=4, padx=(0, 6))
        entry.bind("<Return>", lambda _: self._on_convert())
        entry.focus()

        self._blank(parent, r); r += 1

        # From unit comment
        self._code_line(parent, r, "# Select source unit", color=TEXT_SEC); r += 1

        from_row = tk.Frame(parent, bg=BG_EDITOR)
        from_row.grid(row=r, column=0, sticky="w", pady=4); r += 1

        tk.Label(from_row, text="from_unit", bg=BG_EDITOR, fg=TEXT_KEY,
                 font=("Consolas", 12)).pack(side="left")
        tk.Label(from_row, text=" = ", bg=BG_EDITOR, fg=TEXT_PRI,
                 font=("Consolas", 12)).pack(side="left")

        self.from_var = tk.StringVar(value="Celsius")
        self._unit_pills(from_row, self.from_var)

        self._blank(parent, r); r += 1

        # To unit
        self._code_line(parent, r, "# Select target unit", color=TEXT_SEC); r += 1

        to_row = tk.Frame(parent, bg=BG_EDITOR)
        to_row.grid(row=r, column=0, sticky="w", pady=4); r += 1

        tk.Label(to_row, text="to_unit  ", bg=BG_EDITOR, fg=TEXT_KEY,
                 font=("Consolas", 12)).pack(side="left")
        tk.Label(to_row, text=" = ", bg=BG_EDITOR, fg=TEXT_PRI,
                 font=("Consolas", 12)).pack(side="left")

        self.to_var = tk.StringVar(value="Fahrenheit")
        self._unit_pills(to_row, self.to_var)

        self._blank(parent, r); r += 1

        # Convert + swap buttons
        btn_row = tk.Frame(parent, bg=BG_EDITOR)
        btn_row.grid(row=r, column=0, sticky="w", pady=(4, 0)); r += 1

        self._vscode_btn(btn_row, "▶  Run Convert", self._on_convert,
                         bg=ACCENT, hover=ACCENT_HOV).pack(side="left", padx=(0, 10))
        self._vscode_btn(btn_row, "⇅ Swap", self._swap,
                         bg=BG_INPUT, hover=BG_HOVER, fg=TEXT_PRI).pack(side="left")

        self._blank(parent, r); r += 1

        # Comment above output
        self._code_line(parent, r, "# Output", color=TEXT_SEC); r += 1

        # Result
        result_frame = tk.Frame(parent, bg=BG_SIDEBAR,
                                highlightthickness=1, highlightbackground=BORDER)
        result_frame.grid(row=r, column=0, sticky="ew", pady=(4, 0))

        tk.Label(result_frame, text="result", bg=BG_SIDEBAR, fg=TEXT_KEY,
                 font=("Consolas", 11), padx=12, pady=10).pack(side="left")
        tk.Label(result_frame, text="=", bg=BG_SIDEBAR, fg=TEXT_PRI,
                 font=("Consolas", 11)).pack(side="left")

        self.lbl_result = tk.Label(result_frame, text=' "—"',
                                   bg=BG_SIDEBAR, fg=TEXT_STR,
                                   font=("Consolas", 13, "bold"),
                                   padx=8, pady=10)
        self.lbl_result.pack(side="left")

        r += 1
        self._blank(parent, r); r += 1

        # All equivalents
        self.lbl_all = tk.Label(parent, text="",
                                bg=BG_EDITOR, fg=TEXT_SEC,
                                font=("Consolas", 10), anchor="w")
        self.lbl_all.grid(row=r, column=0, sticky="w", pady=(0, 4))

    def _code_line(self, parent, row, text, color=TEXT_PRI) -> tk.Label:
        lbl = tk.Label(parent, text=text, bg=BG_EDITOR, fg=color,
                       font=("Consolas", 11), anchor="w")
        lbl.grid(row=row, column=0, sticky="w", pady=1)
        return lbl

    def _blank(self, parent, row) -> None:
        tk.Label(parent, text="", bg=BG_EDITOR,
                 font=("Consolas", 6)).grid(row=row, column=0)

    def _unit_pills(self, parent, variable: tk.StringVar) -> None:
        for unit in UNITS:
            rb = tk.Radiobutton(
                parent, text=f'"{unit}"', variable=variable, value=unit,
                bg=BG_INPUT, fg=TEXT_STR,
                selectcolor=ACCENT,
                activebackground=BG_INPUT, activeforeground=TEXT_STR,
                font=("Consolas", 11), cursor="hand2",
                indicatoron=0, relief="flat", padx=10, pady=4, bd=0
            )
            rb.pack(side="left", padx=(0, 4))

    def _vscode_btn(self, parent, text, command, bg=ACCENT,
                    hover=ACCENT_HOV, fg="#ffffff") -> tk.Button:
        btn = tk.Button(parent, text=text, command=command,
                        bg=bg, fg=fg,
                        activebackground=hover, activeforeground=fg,
                        relief="flat", cursor="hand2",
                        font=("Consolas", 10), padx=14, pady=6, bd=0)
        btn.bind("<Enter>", lambda e: btn.config(bg=hover))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))
        return btn

    def _swap(self) -> None:
        f, t = self.from_var.get(), self.to_var.get()
        self.from_var.set(t)
        self.to_var.set(f)
        if self.entry_var.get().strip():
            self._on_convert()

    def _on_convert(self) -> None:
        raw = self.entry_var.get().strip()
        if not raw:
            self.lbl_result.config(text=' "Enter a value"', fg=DANGER)
            self.lbl_all.config(text="")
            self.lbl_status.config(text="  ⚠ No input")
            return
        try:
            value = float(raw)
        except ValueError:
            self.lbl_result.config(text=' "Invalid number"', fg=DANGER)
            self.lbl_all.config(text="")
            self.lbl_status.config(text="  ✗ TypeError: expected float")
            return

        from_unit = self.from_var.get()
        to_unit   = self.to_var.get()

        try:
            Converter.validate(value, from_unit)
            result = Converter.convert(value, from_unit, to_unit)
        except ValueError as exc:
            self.lbl_result.config(text=f' "{exc}"', fg=DANGER)
            self.lbl_all.config(text="")
            self.lbl_status.config(text="  ✗ ValueError")
            return

        sym = SYMBOLS
        res_text = f' "{value:g} {sym[from_unit]} → {result:.6g} {sym[to_unit]}"'
        self.lbl_result.config(text=res_text, fg=TEXT_STR)

        all_vals = {u: Converter.convert(value, from_unit, u) for u in UNITS}
        all_text = "# " + "  |  ".join(
            f"{v:.6g} {sym[u]}" for u, v in all_vals.items()
        )
        self.lbl_all.config(text=all_text, fg=TEXT_SEC)
        self.lbl_status.config(
            text=f"  ✔ Converted {value:g} {sym[from_unit]} to {result:.6g} {sym[to_unit]}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
