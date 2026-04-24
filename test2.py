import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter + Matplotlib Example")

        self.current_choice = None

        # ---- Main layout frames ----
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        plot_frame = tk.Frame(main_frame)
        plot_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        button_frame = tk.Frame(main_frame)
        button_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

        # ---- Matplotlib figure ----
        self.fig = Figure(figsize=(5, 4))
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Current Choice")
        self.text = self.ax.text(
            0.5, 0.5, "None",
            ha="center", va="center", fontsize=20
        )
        self.ax.set_xticks([])
        self.ax.set_yticks([])

        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # ---- Buttons ----
        tk.Button(
            button_frame,
            text="Choose 1, 2, or 3",
            command=self.choose_number,
            width=20
        ).pack(pady=5)

        tk.Button(
            button_frame,
            text="Save Choice",
            command=self.save_choice,
            width=20
        ).pack(pady=5)

        tk.Button(
            button_frame,
            text="Load Choice",
            command=self.load_choice,
            width=20
        ).pack(pady=5)

    # ---- Button callbacks ----
    def choose_number(self):
        value = simpledialog.askinteger(
            "Choose Number",
            "Enter 1, 2, or 3:",
            minvalue=1,
            maxvalue=3
        )
        if value is not None:
            self.set_choice(value)

    def set_choice(self, value):
        self.current_choice = value
        self.text.set_text(str(value))
        self.canvas.draw_idle()

    def save_choice(self):
        if self.current_choice is None:
            messagebox.showwarning("No choice", "No number selected.")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")]
        )
        if filename:
            with open(filename, "w") as f:
                f.write(str(self.current_choice))

    def load_choice(self):
        filename = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt")]
        )
        if filename:
            try:
                with open(filename, "r") as f:
                    value = int(f.read().strip())
                if value in (1, 2, 3):
                    self.set_choice(value)
                else:
                    raise ValueError
            except Exception:
                messagebox.showerror(
                    "Error",
                    "File does not contain a valid choice (1, 2, or 3)."
                )


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
