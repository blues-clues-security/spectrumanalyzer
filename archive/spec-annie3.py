import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.use('TkAgg')

# Global Variables
min_frequency = 0
max_frequency = 1000
num_bands = 100

# Define the frequencies of the spectrum analyzer
frequencies = np.linspace(min_frequency, max_frequency, num_bands)

# Create the main window
root = tk.Tk()

# Create a frame for the buttons and sliders
control_frame = tk.Frame(root)
control_frame.pack()

# Create a button to select a specific frequency band
def select_band(band_num):
    global selected_band
    selected_band = band_num

band_button = tk.Button(control_frame, text='Select Band 0', command=lambda: select_band(0))
band_button.pack()

# Create a slider to control the amplitude of the selected frequency band
def set_amplitude(amplitude):
    global amplitudes
    amplitudes[selected_band] = amplitude

amplitude_slider = tk.Scale(control_frame, from_=0, to=1, orient=tk.HORIZONTAL, resolution=0.01, command=set_amplitude)
amplitude_slider.pack()

# Create a frame for the plot
plot_frame = tk.Frame(root)
plot_frame.pack()

# Create a list to store the visible bands and the amplitudes of each band
visible_bands = []
amplitudes = [0] * num_bands

# Create a button to toggle the visibility of a specific frequency band
def toggle_band(band_num):
    global visible_bands
    if band_num in visible_bands:
        visible_bands.remove(band_num)
    else:
        visible_bands.append(band_num)

band_button = tk.Button(control_frame, text='Toggle Band 0', command=lambda: toggle_band(0))
band_button.pack()

# Create a list to store the visible bands and the amplitudes of each band
visible_bands = []
amplitudes = [0] * num_bands

fig, ax = plt.subplots()

def generate_data(frame):
    amplitudes = []
    for frequency in frequencies:
        amplitude = np.sin(2 * np.pi * frequency * frame / num_bands)
        amplitudes.append(amplitude)
    return amplitudes


frequencies = np.linspace(min_frequency, max_frequency, num_bands)
amplitudes = generate_data(1)
line, = ax.plot(frequencies, amplitudes, color='red', linestyle='solid')

ax.set_title('Spectrum Analyzer')
ax.set_xlabel('Frequency (Hz)')
ax.set_ylabel('Amplitude')

def update(frame):
    # # Generate the data for the spectrum analyzer
    # frequencies = np.linspace(min_frequency, max_frequency, num_bands)
    # amplitudes = generate_data(frame)
    # Filter the frequencies and amplitudes based on the visible bands
    frequencies = [frequencies[i] for i in visible_bands]
    amplitudes = [amplitudes[i] for i in visible_bands]
    # Update the line object with the new data
    line.set_data(frequencies, amplitudes)
    return line,

ani = animation.FuncAnimation(fig, update, interval=1000/30)


# Create the FigureCanvasTkAgg widget and add it to the plot frame
canvas = FigureCanvasTkAgg(fig, plot_frame)
canvas.get_tk_widget().pack()

# Start the main loop
root.mainloop()