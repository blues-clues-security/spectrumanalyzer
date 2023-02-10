import tkinter as tk
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Global Variables
min_frequency = 0
max_frequency = 1000
min_amplitude = -1000
max_amplitude = 1000
num_bands = 4
selected_band = 1


# Create a list to store the visible bands and the amplitudes of each band
visible_bands = [200, 450, 550, 850]
amplitudes = [0] * num_bands

# Create the main window
root = tk.Tk()

# Create a frame for the buttons and sliders
control_frame = tk.Frame(root)
control_frame.pack()

# Create a button to select a specific frequency band
def select_band(band_num):
    global selected_band
    selected_band = band_num

band_button1 = tk.Button(control_frame, text='Select Band 0', command=lambda: select_band(0))
band_button2 = tk.Button(control_frame, text='Select Band 1', command=lambda: select_band(1))
band_button3 = tk.Button(control_frame, text='Select Band 2', command=lambda: select_band(2))
band_button4 = tk.Button(control_frame, text='Select Band 3', command=lambda: select_band(3))
band_button1.pack()
band_button2.pack()
band_button3.pack()
band_button4.pack()

# Create a slider to control the amplitude of the selected frequency band
def set_amplitude(amplitude):
    global amplitudes
    try:
        amplitudes[selected_band] = amplitude
    except selected_band is None:
        amplitudes[selected_band] = 0

amplitude_slider = tk.Scale(control_frame, from_=-1000, to=1000, orient=tk.HORIZONTAL, resolution=1, command=set_amplitude)
amplitude_slider.pack()

# Create a frame for the plot
plot_frame = tk.Frame(root)
plot_frame.pack()

fig, ax = plt.subplots()

# Create the FigureCanvasTkAgg widget and add it to the plot frame
canvas = FigureCanvasTkAgg(fig, plot_frame)
canvas.get_tk_widget().pack()

frequencies = np.linspace(min_frequency, max_frequency, num_bands)
amplitudes = np.linspace(min_amplitude, max_amplitude, num_bands)
line, = ax.plot(frequencies, amplitudes, color='red', linestyle='solid')

ax.set_title('Spectrum Analyzer')
ax.set_xlabel('Frequency (Hz)')
ax.set_ylabel('Amplitude')

#Define the update function
def update(frame):
    # Filter the frequencies and amplitudes based on the visible bands
    # amplitudes = amplitudes.tolist()
    # frequencies = [frequencies[i] for i in visible_bands]
    # amplitudes = [amplitudes[i] for i in visible_bands]
    # Update the line object with the new data
    line.set_data(frequencies, amplitudes)
    return line,

# Define the function to select a frequency band
def select_band(band_num):
    global selected_band
    selected_band = band_num

# Create a label to display the data
label = tk.Label(root)
label.pack()

# Define the update function
def update_label():     
    frequency = frequencies[selected_band]
    amplitude = amplitudes[selected_band]
    # Update the label with the selected band and frequency
    label.configure(text='Selected Band: {}\nFrequency: {} Hz\nAmplitude: {}'.format(selected_band, frequency, amplitude))
    #update(frequency, amplitude)
    line.set_data(frequency, amplitude)
    # Schedule the next update in 500 milliseconds
    root.after(500, update_label)
    

# Schedule the first update
root.after(500, update_label)

# Create the animation using the update function and a frame rate of 30 FPS
ani = animation.FuncAnimation(fig, update, interval=1000/30)

# Start the main loop
root.mainloop()