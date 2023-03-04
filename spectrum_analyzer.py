import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

class SpectrumAnalyzer:
    """
    A class representing a spectrum analyzer.

    ...

    Attributes
    ----------
    min_frequency : int
        minimum frequency in the range of frequencies to be plotted
    max_frequency : int
        maximum frequency in the range of frequencies to be plotted
    min_amplitude : int
        minimum amplitude in the range of amplitudes to be plotted
    max_amplitude : int
        maximum amplitude in the range of amplitudes to be plotted
    num_bands : int
        number of frequency bands to be plotted
    visible_bands : list of int
        list of frequencies for the visible bands
    noise_floor : list of int
        amplitude of the noise floor
    amplitudes : list of int
        amplitudes of each band to be plotted

    Methods
    -------
    select_band(selected_band):
        Sets the currently selected band to the given frequency.

    create_options_window():
        Creates the options window.

    create_bar_plot_frame():
        Creates the frame for the spectrum analyzer plot.

    create_control_frame():
        Creates the frame for the control buttons and sliders.

    set_amplitude(amplitude):
        Sets the amplitude of the currently selected band.

    wiggle(frame):
        Creates a wiggle effect to give a noisy feel to the plot.

    update(frame):
        Updates the amplitude of each bar in the plot.

    update_label():
        Updates the label displaying the selected band and its amplitude.

    create_animation():
        Creates the animation using the update function and a frame rate of 60 FPS.
    """
    def __init__(self):
        """
        Constructs all the necessary attributes for the SpectrumAnalyzer object.

        Initializes the window for the options, the frame for the spectrum analyzer plot,
        the list of frequencies to be plotted, the selected band, and the animation.
        """
        self.create_initial_options_windows()
        self.amplitudes = self.noise_floor * (self.num_bands + len(self.visible_bands))
        self.create_options_window()
        self.create_control_frame()
        self.create_bar_plot_frame()
        self.create_animation()
        self.update_label()

    def select_band(self, selected_band):
        """
        Sets the currently selected band to the given frequency.

        Parameters
        ----------
        selected_band : int
            the frequency of the selected band
        """
        self.selected_band = np.where(self.frequencies == selected_band)[0][0]
    
    def create_initial_options_windows(self):
        """
        Creates the initial options window for the Spectrum Analyzer.
        """
        # Create initial options window
        self.init_options = tk.Tk()
        self.init_options.geometry('520x400')
        self.init_options.winfo_toplevel().title('Initial Options')

         # Create two frames to hold the options
        left_frame = tk.Frame(self.init_options)
        right_frame = tk.Frame(self.init_options)
        left_frame.pack(side=tk.LEFT, padx=10)
        right_frame.pack(side=tk.LEFT, padx=20)
        
        # Set starting variables to entry fields
        self.min_frequency = tk.Entry(left_frame)
        self.min_frequency.insert(0, '0')
        self.minfreq_label = tk.Label(left_frame, text="Enter minimum frequency\n(Default: 0)")
        self.max_frequency = tk.Entry(left_frame)
        self.max_frequency.insert(0, '1000')
        self.maxfreq_label = tk.Label(left_frame, text="Enter maximum frequency\n(Default: 1000)")
        self.min_amplitude = tk.Entry(left_frame)
        self.min_amplitude.insert(0, '0')
        self.minamp_label = tk.Label(left_frame, text="Enter minimum amplitude\n(Default: 0)")
        self.max_amplitude = tk.Entry(left_frame)
        self.max_amplitude.insert(0, '1000')
        self.maxamp_label = tk.Label(left_frame, text="Enter maximum amplitude\n(Default: 1000)")
        self.num_bands = tk.Entry(right_frame)
        self.num_bands.insert(0, '100')
        self.numbands_label = tk.Label(right_frame, text="Enter number of bars to display\n(For best results: 100)")
        self.visible_bands = tk.Entry(right_frame)
        self.visible_bands.insert(0, '200,400,550,800')
        self.visbands_label = tk.Label(right_frame, text="Enter the monitor frequencies\n(Example: 200,400,550,800)")
        self.noise_floor = tk.Entry(right_frame)
        self.noise_floor.insert(0, '200')
        self.noisefloor_label = tk.Label(right_frame, text="Enter the amplitude of the noise floor")
        self.transmit_strength = tk.Entry(right_frame)
        self.transtr_label = tk.Label(right_frame, text="Enter the transmit signal strength\n(when the bar should turn green)")
        
        # Build lists to display all buttons
        self.init_optionslabels = [
            self.minfreq_label,
            self.maxfreq_label,
            self.minamp_label,
            self.maxamp_label,
            self.numbands_label,
            self.visbands_label,
            self.noisefloor_label,
            self.transtr_label
        ]
        self.init_optionsbuttons = [
            self.min_frequency,
            self.max_frequency,
            self.min_amplitude,
            self.max_amplitude,
            self.num_bands,
            self.visible_bands,
            self.noise_floor,
            self.transmit_strength
        ]
        # Display the created entry buttons on the initial options window
        for i, button in enumerate(self.init_optionsbuttons):
            self.init_optionslabels[i].pack()
            self.init_optionsbuttons[i].pack(side=tk.TOP, pady=5)

        # Create the submit button, focus the window and wait until the submit button has been pressed to continue execution
        self.submit_button = tk.Button(self.init_options, text="Submit", command=self.submit_init_options)
        self.submit_button.pack(side="right", pady=20, padx=25)
        self.init_options.grab_set()
        self.init_options.focus_set()
        self.init_options.wait_window()

    def submit_init_options(self):
        """
        Gets the input values from the initial options window and saves them as instance variables.
        """
        try:
            self.noise_floor = self.noise_floor.get()
            self.noise_floor = [int(self.noise_floor)]
            self.min_frequency = self.min_frequency.get()
            self.min_frequency = int(self.min_frequency)
            self.max_frequency = self.max_frequency.get()
            self.max_frequency = int(self.max_frequency)
            self.min_amplitude = self.min_amplitude.get()
            self.min_amplitude = int(self.min_amplitude)
            self.max_amplitude = self.max_amplitude.get()
            self.max_amplitude = int(self.max_amplitude)
            self.num_bands = self.num_bands.get()
            self.num_bands = int(self.num_bands)
            self.visible_bands = self.visible_bands.get()
            self.visible_bands = self.visible_bands.split(',')
            self.visible_bands = list(map(int,self.visible_bands))
            self.transmit_strength = self.transmit_strength.get()
            self.transmit_strength = int(self.transmit_strength)
        except Exception as e:
            print(e)
        
        # Close the initial options window after entry
        self.init_options.destroy()
                

    def create_options_window(self):
        """
        Creates the options window.
        """
        self.options = tk.Tk()
        self.options.geometry('300x250')
        self.options.winfo_toplevel().title('Options')

    def create_bar_plot_frame(self):
        """
        Creates the frame for the spectrum analyzer plot.
        """
        self.root = tk.Tk()
        self.plot_frame = tk.Frame(self.root)
        self.plot_frame.winfo_toplevel().title('Spectrum Analyzer')
        self.plot_frame.pack()
        self.frequencies = np.arange(self.min_frequency, self.max_frequency, (self.max_frequency - self.min_frequency) // (self.num_bands))
        try:
            for i in self.visible_bands:
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
        self.bar_plot = self.ax.bar(self.frequencies, self.noise_floor * (self.num_bands), color='red', width=[5] * (self.num_bands))

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
        self.selected_band = np.where(self.frequencies == self.visible_bands[0])[0][0]
        self.canvas = FigureCanvasTkAgg(self.fig, self.plot_frame)
        self.canvas.get_tk_widget().pack()

    def create_control_frame(self):
        """
        Creates the frame for the control buttons and sliders.
        """
        self.control_frame = tk.Frame(self.options)
        self.control_frame.pack()
        band_buttons = []
        for i, visible_band in enumerate(self.visible_bands):
            band_button = tk.Button(self.control_frame, text=f'Select Band {i+1}', command=lambda visible_band=visible_band: self.select_band(visible_band))
            band_buttons.append(band_button)
        for band_button in band_buttons:
            band_button.pack()
        self.amplitude_slider = tk.Scale(self.control_frame, from_=0, to=1000, orient=tk.HORIZONTAL, resolution=1, command=self.set_amplitude)
        self.amplitude_text = tk.Entry(self.control_frame)
        self.amplitude_slider.pack()
        self.amplitude_text.pack()
        self.label = tk.Label(self.options)
        self.label.pack()
    
    def set_amplitude(self, amplitude):
        """
        Sets the amplitude of the currently selected band.

        Parameters
        ----------
        amplitude : int
            The amplitude of the currently selected band.
        """
        try:
            self.amplitudes[self.selected_band] = int(amplitude)
        except TypeError:
            self.amplitudes[self.selected_band] = 0

    def wiggle(self, frame):
        """
        Creates a wiggle effect to give a noisy feel to the plot.

        Parameters
        ----------
        frame : int
            The current frame of the animation.
        """
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
        """
        Updates the amplitude of each bar in the plot.

        Parameters
        ----------
        frame : int
            the current frame of the animation
        """
        for i, rect in enumerate(self.bar_plot):
            try:
                rect.set_height(int(self.amplitudes[i]))
            except IndexError:
                print(i)
                pass
        self.wiggle(frame)
        self.update_label()
        return self.bar_plot,
    
    def update_label(self):
        """
        Updates the label displaying the selected band and its amplitude.
        """     
        if self.amplitude_text.get():
            amplitude = int(self.amplitude_text.get())
            self.amplitudes[self.selected_band] = amplitude
        else:
            amplitude = self.amplitudes[self.selected_band]
        # Update the label with the selected band and frequency
        self.label.configure(text=f'Selected Band\nFrequency: {self.frequencies[self.selected_band]} Hz\nAmplitude: {self.amplitudes[self.selected_band]}')

        # Update the color of the bar based on the amplitude
        if amplitude >= self.transmit_strength:
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
                if 0 <= band < len(self.amplitudes):
                    if self.amplitudes[self.selected_band] * band_variance[i] >= self.noise_floor[0]:
                        self.amplitudes[band] = self.amplitudes[self.selected_band] * band_variance[i]
                if self.amplitudes[self.selected_band] <= self.noise_floor[0]:
                    self.amplitudes[band] = self.noise_floor[0]
        self.root.after(500, self.update_label)
    
    def create_animation(self):
        """
        Creates the animation using the update function and a frame rate of 60 FPS.
        """
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=1000/60)
   
# Start the main loop
SpectrumAnalyzer().root.mainloop()
