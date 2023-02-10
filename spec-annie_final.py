import tkinter as tk
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import rcParams

# Global Variables
min_frequency = 0
max_frequency = 1000
min_amplitude = -1000
max_amplitude = 1000
num_bands = 4
selected_band = 3

# Multiply number of selected bands by 3 to account for peak and 2 troughs
num_bands = num_bands * 3

# Create a list to store the visible bands and the amplitudes of each band
visible_bands = [200, 450, 550, 850]
amplitudes = [0] * num_bands

# Create the main window
root = tk.Tk()

# Create options window
options = tk.Tk()
options.geometry('300x250')

# Create a frame for the buttons and sliders
control_frame = tk.Frame(options)
control_frame.winfo_toplevel().title('Options')
control_frame.pack()

# Create a button to select a specific frequency band
def select_band(band_num):
    global selected_band
    if selected_band == 0:
        selected_band = 3
    else:
        # Some weird math here to account for the offset on the line to control each frequency
        # TODO: set selected band based on number of frequencies presented
        selected_band = band_num * 2 + 1

band_button1 = tk.Button(control_frame, text='Select Band 1', command=lambda: select_band(1))
band_button2 = tk.Button(control_frame, text='Select Band 2', command=lambda: select_band(2))
band_button3 = tk.Button(control_frame, text='Select Band 3', command=lambda: select_band(3))
band_button4 = tk.Button(control_frame, text='Select Band 4', command=lambda: select_band(4))
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
amplitude_text = tk.Entry(control_frame)
amplitude_slider.pack()
amplitude_text.pack()

# Create a frame for the plot
plot_frame = tk.Frame(root)
plot_frame.winfo_toplevel().title('Spectrum Analyzer')
plot_frame.pack()

# Set the lines in Spectrum Analyzer to be spikey
rcParams['path.sketch'] = (10, 10, 100)

# Remove the borders from the Spectrum Analyzer frame
fig, ax = plt.subplots()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

# Create the FigureCanvasTkAgg widget and add it to the plot frame
canvas = FigureCanvasTkAgg(fig, plot_frame)
canvas.get_tk_widget().pack()

# Initiate line based on the frequencies specified
# Note: amplitude/y values is set to 0 initially
frequencies = np.linspace(min_frequency, max_frequency, num_bands)
line, = ax.plot(frequencies, [0] * num_bands, color='red', linestyle='solid')

# Set the y axis limits
plt.ylim((-1000,1000))

# Set plot labels
ax.set_title('Spectrum Analyzer')
ax.set_xlabel('Frequency (Hz)')
ax.set_ylabel('Amplitude')

# Define the update function used to animate the main line
def update(frame):
    line.set_data(frequencies, amplitudes)
    return line,

# Create a label to display the data
label = tk.Label(options)
label.pack()

# Define the update function
def update_label():     
    #frequency = frequencies[selected_band]
    if amplitude_text.get():
        amplitude = int(amplitude_text.get())
        amplitudes[selected_band] = amplitude
    else:
        amplitude = amplitudes[selected_band]
    # Update the label with the selected band and frequency
    label.configure(text='Selected Band: {}\nFrequency: {} Hz\nAmplitude: {}'.format(selected_band, frequencies[selected_band], amplitudes[selected_band]))
    #update(frequency, amplitude)
    line.set_data(frequencies[selected_band], amplitudes[selected_band])
    # Schedule the next update in 500 milliseconds
    root.after(500, update_label)
    
# Schedule the first update
root.after(500, update_label)

# Create the animation using the update function and a frame rate of 60 FPS
ani = animation.FuncAnimation(fig, update, interval=1000/60)

# Start the main loop
root.mainloop()