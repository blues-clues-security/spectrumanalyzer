import tkinter as tk
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

# Global Variables
min_frequency = 0
max_frequency = 1000
min_amplitude = 0
max_amplitude = 1000
num_bands = 100

# Multiply number of selected bands by 3 to account for peak and 2 troughs
#num_bands = num_bands * 30

# Create a list to store the visible bands and the amplitudes of each band
visible_bands = [200, 450, 550, 800]
noise_floor = [200]
amplitudes = noise_floor * (num_bands + len(visible_bands))

# Create the main window
root = tk.Tk()

# Create options window
options = tk.Tk()
options.geometry('300x250')

# Create a frame for the buttons and sliders
control_frame = tk.Frame(options)
control_frame.winfo_toplevel().title('Options')
control_frame.pack()

# Create a button to select a specific frequency band in the list of visible_bands
def select_band(band_num):
    global selected_band
    selected_band = np.where(frequencies == visible_bands[band_num])[0][0]

# Create a slider to control the amplitude of the selected frequency band
def set_amplitude(amplitude):
    global amplitudes
    try:
        amplitudes[selected_band] = int(amplitude)
    except TypeError:
        amplitudes[selected_band] = 0

band_button1 = tk.Button(control_frame, text='Select Band 1', command=lambda: select_band(0))
band_button2 = tk.Button(control_frame, text='Select Band 2', command=lambda: select_band(1))
band_button3 = tk.Button(control_frame, text='Select Band 3', command=lambda: select_band(2))
band_button4 = tk.Button(control_frame, text='Select Band 4', command=lambda: select_band(3))
band_button1.pack()
band_button2.pack()
band_button3.pack()
band_button4.pack()

amplitude_slider = tk.Scale(control_frame, from_=0, to=1000, orient=tk.HORIZONTAL, resolution=1, command=set_amplitude)
amplitude_text = tk.Entry(control_frame)
amplitude_slider.pack()
amplitude_text.pack()

# Create a frame for the plot
plot_frame = tk.Frame(root)
plot_frame.winfo_toplevel().title('Spectrum Analyzer')
plot_frame.pack()

# Remove the borders from the Spectrum Analyzer frame
fig, ax = plt.subplots()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

# Create the FigureCanvasTkAgg widget and add it to the plot frame
canvas = FigureCanvasTkAgg(fig, plot_frame)
canvas.get_tk_widget().pack()

# Create a range of frequencies
# Note: This may cause issues if num_bands is not set to 100, or if visible_bands are not divisible by 10
frequencies = np.arange(min_frequency, max_frequency, (max_frequency - min_frequency) // (num_bands))
try:
    for i in visible_bands:
        i // 10
except:
    print('One of the visible bands may show incorrectly')

# Create the bar plot
bar_plot = ax.bar(frequencies, noise_floor * (num_bands), color='red', width=[5] * (num_bands))

# Set the x/y axis limits
plt.ylim((0,1000))
plt.xlim((min_frequency-100, max_frequency+100))

# Set plot labels
ax.set_title('Spectrum Analyzer')
ax.set_xlabel('Frequency (Hz)')
ax.set_ylabel('Amplitude')

# Create a label to display the data
label = tk.Label(options)
label.pack()

# Set the x-axis ticks and labels
ax.set_xticks(visible_bands)

# Create a wiggle effect to give a noisy feel
def wiggle(frame):
    num_bars_to_wiggle = int(len(bar_plot) * 0.1)  # Determine number of bars to wiggle
    bars_to_wiggle = random.sample(range(len(bar_plot)), num_bars_to_wiggle)  # Select random bars to wiggle
    for i, rect in enumerate(bar_plot):
        try:
            if i in bars_to_wiggle:
                # Calculate a sine wave with period 100 frames and amplitude 10 pixels
                wiggle_amount = 10 * np.sin(frame / 100 * 2 * np.pi)
                rect.set_height(int(amplitudes[i] + int(wiggle_amount)))
        except IndexError:
            rect.set_height(int(amplitudes[i]) - 10)
        except TypeError:
            pass


# Define the update function used to animate the main line
def update(frame):
    for i, rect in enumerate(bar_plot):
        try:
            rect.set_height(int(amplitudes[i]))
        except IndexError:
            print(i)
            pass
    wiggle(frame)
    return bar_plot,


# Set the initial selected_band to the first visible band
selected_band = np.where(frequencies == visible_bands[0])[0][0]

# Define the update function
def update_label():     
    #frequency = frequencies[selected_band]
    if amplitude_text.get():
        amplitude = int(amplitude_text.get())
        amplitudes[selected_band] = amplitude
    else:
        amplitude = amplitudes[selected_band]
    # Update the label with the selected band and frequency
    label.configure(text=f'Selected Band\nFrequency: {frequencies[selected_band]} Hz\nAmplitude: {amplitudes[selected_band]}')

    # Update the color of the bar based on the amplitude
    if amplitude >= 500:
        bar_plot[selected_band].set_color('green')
        bar_plot[selected_band].set_zorder(100)
    else:
        bar_plot[selected_band].set_color('red')

    # Update the amplitudes of the adjacent bars
    band_list = range(1,5)
    band_variance = [0.9, 0.95, 0.9, 0.8, 0.6]
    for i in band_list:
        adjacent_bands = [selected_band-i, selected_band+i]
        for band in adjacent_bands:
            if 0 <= band < len(amplitudes):
                if amplitudes[selected_band] * band_variance[i] >= noise_floor[0]:
                    amplitudes[band] = amplitudes[selected_band] * band_variance[i]
            if amplitudes[selected_band] <= noise_floor[0]:
                amplitudes[band] = noise_floor[0]

    # Schedule the next update in 500 milliseconds
    root.after(500, update_label)
    
# Schedule the first update
root.after(500, update_label)

# Create the animation using the update function and a frame rate of 60 FPS
ani = animation.FuncAnimation(fig, update, interval=1000/60)

# Start the main loop
root.mainloop()