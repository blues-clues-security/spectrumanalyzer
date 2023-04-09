import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
from matplotlib.animation import PillowWriter, FuncAnimation
import matplotlib.animation as animation
#import tkinter.ttk as ttk

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
    def __init__(self, min_frequency=0, max_frequency=1000, min_amplitude=0, max_amplitude=1000, num_bands=100, visible_bands=[200, 400, 550, 800], noise_floor=[200], num_frames=100):
        """
        Constructs all the necessary attributes for the SpectrumAnalyzer object.

        Initializes the window for the options, the frame for the spectrum analyzer plot,
        the list of frequencies to be plotted, the selected band, and the animation.
        """
        self.min_frequency = min_frequency
        self.max_frequency = max_frequency
        self.min_amplitude = min_amplitude
        self.max_amplitude = max_amplitude
        self.num_bands = num_bands
        self.visible_bands = visible_bands
        self.noise_floor = noise_floor
        self.amplitudes = [self.noise_floor[0]] * (self.num_bands)
        self.num_frames = num_frames
        self.create_bar_plot()

    def create_bar_plot(self):
        base_frequencies = np.linspace(self.min_frequency, self.max_frequency, self.num_bands - len(self.visible_bands), endpoint=False)

        visible_band_indices = []
        for visible_band in self.visible_bands:
            closest_index = np.argmin(np.abs(base_frequencies - visible_band))
            visible_band_indices.append(closest_index)

        for i, index in enumerate(visible_band_indices):
            base_frequencies = np.insert(base_frequencies, index + i, self.visible_bands[i])

        self.frequencies = base_frequencies

        self.fig, self.ax = plt.subplots()
        # self.ax.spines['top'].set_visible(False)
        # self.ax.spines['right'].set_visible(False)
        # self.ax.spines['bottom'].set_visible(False)
        # self.ax.spines['left'].set_visible(False)
        # self.fig.set_figheight(20)
        # self.fig.set_figwidth(20)

        self.bar_plot = self.ax.bar(self.frequencies, self.noise_floor * (self.num_bands), color='red', width=[5] * (self.num_bands))

        plt.ylim((0,1000))
        plt.xlim((self.min_frequency-100, self.max_frequency+100))

        self.ax.set_title('Spectrum Analyzer')
        self.ax.set_xlabel('Frequency (Hz)')
        self.ax.set_ylabel('Amplitude')

        self.ax.set_xticks(self.visible_bands)

    def update_bars(self, i):
        new_amplitudes = [random.randint(self.min_amplitude, self.max_amplitude) for _ in range(self.num_bands)]

        for bar, amplitude in zip(self.bar_plot, new_amplitudes):
            bar.set_height(amplitude)

        #return self.bar_plot
        return self.frequencies, new_amplitudes

    # def save_animation(self, filename, num_frames=100, interval=100):
    #     ani = animation.FuncAnimation(self.fig, self.update_bars, frames=num_frames, interval=interval, blit=True)
    #     ani.save(filename, writer='imagemagick', fps=30)
    

    def select_band(self, selected_band):
        """
        Sets the currently selected band to the given frequency.

        Parameters
        ----------
        selected_band : int
            the frequency of the selected band
        """
        self.selected_band = np.where(self.frequencies == selected_band)[0][0]
    
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
            if self.transmit_strength:
                self.transmit_strength = int(self.transmit_strength)
            else:
                pass
        except Exception as e:
            print(e)
        
        # Close the initial options window after entry
        self.init_options.destroy()
                
    def create_bar_plot_frame(self):
        """
        Creates the frame for the spectrum analyzer plot.
        """
        self.root = tk.Tk()
        self.plot_frame = tk.Frame(self.root)
        self.plot_frame.winfo_toplevel().title('Spectrum Analyzer')
        self.plot_frame.pack()
        base_frequencies = np.linspace(self.min_frequency, self.max_frequency, self.num_bands - len(self.visible_bands), endpoint=False)

        # Create a list of visible bands with closest frequencies in base_frequencies
        visible_band_indices = []
        for visible_band in self.visible_bands:
            closest_index = np.argmin(np.abs(base_frequencies - visible_band))
            visible_band_indices.append(closest_index)

        # Insert visible bands into the base_frequencies array
        for i, index in enumerate(visible_band_indices):
            base_frequencies = np.insert(base_frequencies, index + i, self.visible_bands[i])

        self.frequencies = base_frequencies
        
        # Remove the borders from the Spectrum Analyzer frame
        self.fig, self.ax = plt.subplots()
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.spines['left'].set_visible(False)
        self.fig.set_figheight(20)
        self.fig.set_figwidth(20)
        
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
        print(np.where(self.frequencies == self.visible_bands[0])[0])
        self.selected_band = np.where(self.frequencies == self.visible_bands[0])[0][0]
        self.canvas = FigureCanvasTkAgg(self.fig, self.plot_frame)
        self.canvas.get_tk_widget().pack()
  
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
        bars_to_wiggle = np.random.choice(len(self.bar_plot), num_bars_to_wiggle, replace=False)  # Select random bars to wiggle
        wiggle_amount = 10 * np.sin(frame / 100 * 2 * np.pi) # Calculate a sine wave with period 100 frames and amplitude 10 pixels        
        for i, rect in enumerate(self.bar_plot):
            if i in bars_to_wiggle:
                rect.set_height(max(0, int(self.amplitudes[i] + int(wiggle_amount))))
            else:
                rect.set_height(max(0, int(self.amplitudes[i])))

    def update(self, frame):
        """
        Updates the amplitude of each bar in the plot.

        Parameters
        ----------
        frame : int
            the current frame of the animation
        """
        heights = np.maximum(0, self.amplitudes)
        for rect, h in zip(self.bar_plot, heights):
            rect.set_height(h)
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
        try: 
            if amplitude >= self.transmit_strength:
                self.bar_plot[self.selected_band].set_color('green')
                self.bar_plot[self.selected_band].set_zorder(100)
            else:
                self.bar_plot[self.selected_band].set_color('red')
        except TypeError:
            self.transmit_strength = 500
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
    
    def create_animation(self):
        """
        Creates the animation using the update function and a frame rate of 60 FPS.
        """
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=1000/30)

    def save_spectrum_gif(self, file_name='spectrum.gif', dpi=80):
        fig, ax = plt.subplots()
    
        def update_spectrum_plot(frame):
            freqs, amplitudes = self.update_bars(frame)
            ax.clear()
            ax.bar(freqs, amplitudes)
            ax.set_xlabel("Frequency [Hz]")
            ax.set_ylabel("Amplitude")
            ax.set_title("Frequency Spectrum")

        ani = FuncAnimation(fig, update_spectrum_plot, frames=self.num_frames, interval=50, blit=False)

        writer = PillowWriter(fps=20)
        ani.save(file_name, writer=writer, dpi=dpi)

        plt.close(fig)

if __name__ == '__main__':
    # Example usage
    #analyzer = SpectrumAnalyzer()
    #analyzer.save_animation('images/spectrum_analyzer_animation.gif', num_frames=100, interval=100)
    #analyzer.save_spectrum_gif()
    sa = SpectrumAnalyzer(num_frames=50)
    sa.save_spectrum_gif(file_name='static/spectrum.gif', dpi=80)

    # Start the main loop
    #SpectrumAnalyzer().root.mainloop()