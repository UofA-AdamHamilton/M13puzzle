import numpy as np
def sin(x):
    return np.sin(x)

def generate_plot():
    """Generates a matplotlib figure and returns the figure object."""
    t = np.arange(0.0, 2.0, 0.01)
    s = 1 + np.sin(2 * np.pi * t)
    fig, ax = plt.subplots()
    ax.plot(t, s)
    ax.set(xlabel="time (s)", ylabel="voltage (mV)", title="About as simple as it gets, folks")
    ax.grid()
    return fig # Return the figure object

def change_color(line, color_var, canvas):
    line.set_color(color_var.get())
    canvas.draw_idle()

def change_linestyle(line, style_var, canvas):
    line.set_linestyle("-" if style_var.get() == "solid" else "--")
    canvas.draw_idle()