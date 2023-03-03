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
visible_bands = [200, 450, 550, 800]
noise_floor = [200]
amplitudes = noise_floor * (num_bands + len(visible_bands))


class SpectrumAnalyzer:
    def __init__(self):
        self.min_frequency = 0
        self.max_frequency = 1000
        self.min_amplitude = 0
        self.max_amplitude = 1000
        self.num_bands = 100
        self.visible_bands = [200, 450, 550, 800]
        self.noise_floor = [200]
        self.amplitudes = noise_floor * (num_bands + len(visible_bands))
        
        self.create_options_window()
        self.control_frame = tk.Frame(self.options)
        self.control_frame.pack()
        self.create_control_frame()
        

        self.amplitude_slider = tk.Scale(self.control_frame, from_=0, to=1000, orient=tk.HORIZONTAL, resolution=1, command=self.set_amplitude)
        self.amplitude_text = tk.Entry(self.control_frame)
        self.amplitude_slider.pack()
        self.amplitude_text.pack()
        self.label = tk.Label(self.options)
        self.label.pack()


        self.root = tk.Tk()
        
        self.create_plot_frame()
        self.create_bar_plot()
        
        self.selected_band = np.where(frequencies == visible_bands[0])[0][0]
        self.create_animation()
        # self.select_band()
        # self.wiggle()
        # self.update()
        self.update_label()

    def select_band(self, selected_band):
        self.selected_band = np.where(self.frequencies == selected_band)[0][0]

    def create_options_window(self):
        self.options = tk.Tk()
        self.options.geometry('300x250')
        self.options.winfo_toplevel().title('Options')

    def create_plot_frame(self):
        self.plot_frame = tk.Frame(self.root)
        self.plot_frame.winfo_toplevel().title('Spectrum Analyzer')
        self.plot_frame.pack()

    def create_bar_plot(self):
        global frequencies
        frequencies = np.arange(min_frequency, max_frequency, (max_frequency - min_frequency) // (num_bands))
        try:
            for i in visible_bands:
                i // 10
        except:
            print('One of the visible bands may show incorrectly')
        
        # Remove the borders from the Spectrum Analyzer frame
        self.fig, self.ax = plt.subplots()
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.spines['left'].set_visible(False)
        
        # Create the bar plot
        self.frequencies = np.arange(self.min_frequency, self.max_frequency, (self.max_frequency - self.min_frequency) // (self.num_bands))
        self.bar_plot = self.ax.bar(frequencies, self.noise_floor * (self.num_bands), color='red', width=[5] * (self.num_bands))

        # Set the x/y axis limits
        plt.ylim((0,1000))
        plt.xlim((self.min_frequency-100, self.max_frequency+100))
        
        # Set plot labels
        self.ax.set_title('Spectrum Analyzer')
        self.ax.set_xlabel('Frequency (Hz)')
        self.ax.set_ylabel('Amplitude')

        # Set the x-axis ticks and labels
        self.ax.set_xticks(self.visible_bands)
        
        # Create the FigureCanvasTkAgg widget and add it to the plot frame
        self.canvas = FigureCanvasTkAgg(self.fig, self.plot_frame)
        self.canvas.get_tk_widget().pack()

    def create_control_frame(self):
        band_buttons = []
        for i, visible_band in enumerate(visible_bands):
            band_button = tk.Button(self.control_frame, text=f'Select Band {i+1}', command=lambda visible_band=visible_band: self.select_band(visible_band))
            band_buttons.append(band_button)
        for band_button in band_buttons:
            band_button.pack()
    
    def set_amplitude(self, amplitude):
        try:
            self.amplitudes[self.selected_band] = int(amplitude)
        except TypeError:
            amplitudes[self.selected_band] = 0

        
    # Create a wiggle effect to give a noisy feel
    def wiggle(self, frame):
        num_bars_to_wiggle = int(len(self.bar_plot) * 0.1)  # Determine number of bars to wiggle
        bars_to_wiggle = random.sample(range(len(self.bar_plot)), num_bars_to_wiggle)  # Select random bars to wiggle
        for i, rect in enumerate(self.bar_plot):
            try:
                if i in bars_to_wiggle:
                    # Calculate a sine wave with period 100 frames and amplitude 10 pixels
                    wiggle_amount = 10 * np.sin(frame / 100 * 2 * np.pi)
                    rect.set_height(int(self.amplitudes[i] + int(wiggle_amount)))
            except IndexError:
                rect.set_height(int(self.amplitudes[i]) - 10)
    
    def update(self, frame):
        for i, rect in enumerate(self.bar_plot):
            try:
                rect.set_height(int(amplitudes[i]))
            except IndexError:
                print(i)
                pass
        self.wiggle(frame)
        self.update_label()
        return self.bar_plot,
    
    def update_label(self):     
        #frequency = frequencies[selected_band]
        if self.amplitude_text.get():
            amplitude = int(self.amplitude_text.get())
            amplitudes[self.selected_band] = amplitude
        else:
            amplitude = amplitudes[self.selected_band]
        # Update the label with the selected band and frequency
        self.label.configure(text=f'Selected Band\nFrequency: {frequencies[self.selected_band]} Hz\nAmplitude: {amplitudes[self.selected_band]}')

        # Update the color of the bar based on the amplitude
        if amplitude >= 500:
            self.bar_plot[self.selected_band].set_color('green')
            self.bar_plot[self.selected_band].set_zorder(100)
        else:
            self.bar_plot[self.selected_band].set_color('red')

        # Update the amplitudes of the adjacent bars
        band_list = range(1,5)
        band_variance = [0.9, 0.95, 0.9, 0.8, 0.6]
        for i in band_list:
            adjacent_bands = [self.selected_band-i, self.selected_band+i]
            for band in adjacent_bands:
                if 0 <= band < len(amplitudes):
                    if amplitudes[self.selected_band] * band_variance[i] >= noise_floor[0]:
                        amplitudes[band] = amplitudes[self.selected_band] * band_variance[i]
                if amplitudes[self.selected_band] <= noise_floor[0]:
                    amplitudes[band] = noise_floor[0]
        self.root.after(500, self.update_label)
    
    def create_animation(self):
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=1000/60)
   
# Start the main loop
SpectrumAnalyzer().root.mainloop()
