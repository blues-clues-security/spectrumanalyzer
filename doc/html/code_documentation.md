# SpectrumAnalyzer Class Reference

## Public Member Functions
- def 	`__init__` (self)
 
- def 	`select_band` (self, selected_band)
 
- def 	`create_options_window` (self)
 
- def 	`create_bar_plot_frame` (self)
 
- def 	`create_control_frame` (self)
 
- def 	`set_amplitude` (self, amplitude)
 
- def 	`wiggle` (self, frame)
 
- def 	`update` (self, frame)
 
- def 	`update_label` (self)

- def 	`create_animation` (self)
 
## Public Attributes
-  	min_frequency
-  	max_frequency
-  	min_amplitude
-  	max_amplitude
-  	num_bands
-  	visible_bands
-  	noise_floor
-  	amplitudes
-  	selected_band
-  	frequencies
-  	options
-  	root
-  	plot_frame 
- 	ax
- 	bar_plot
- 	canvas
- 	control_frame
- 	amplitude_slider
- 	amplitude_text
- 	label
- 	ani
 
## Detailed Description
A class representing a spectrum analyzer.



### Attributes
```
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
```
### Methods
```
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
```
## Constructor & Destructor Documentation
```
__init__()
def spectrum_analyzer.SpectrumAnalyzer.__init__	(	 	self	)	
Constructs all the necessary attributes for the SpectrumAnalyzer object.

Initializes the window for the options, the frame for the spectrum analyzer plot,
the list of frequencies to be plotted, the selected band, and the animation.
```

## Member Function Documentation
```
create_animation()
def spectrum_analyzer.SpectrumAnalyzer.create_animation(self)	
Creates the animation using the update function and a frame rate of 60 FPS.

create_bar_plot_frame()
def spectrum_analyzer.SpectrumAnalyzer.create_bar_plot_frame(self)	
Creates the frame for the spectrum analyzer plot.

create_control_frame()
def spectrum_analyzer.SpectrumAnalyzer.create_control_frame(self)	
Creates the frame for the control buttons and sliders.

create_options_window()
def spectrum_analyzer.SpectrumAnalyzer.create_options_window(self)	
Creates the options window.

select_band()
def spectrum_analyzer.SpectrumAnalyzer.select_band(
    self,
 	selected_band 
)		
Sets the currently selected band to the given frequency.
```

### Parameters
```
selected_band : int
    the frequency of the selected band

set_amplitude()
def spectrum_analyzer.SpectrumAnalyzer.set_amplitude	(	 	self,
 	amplitude 
)		
Sets the amplitude of the currently selected band.

amplitude : int
    The amplitude of the currently selected band.

update()
def spectrum_analyzer.SpectrumAnalyzer.update(
    self,
 	frame 
)		
Updates the amplitude of each bar in the plot.

frame : int
    the current frame of the animation

update_label()
def spectrum_analyzer.SpectrumAnalyzer.update_label(self)	
Updates the label displaying the selected band and its amplitude.

wiggle()
def spectrum_analyzer.SpectrumAnalyzer.wiggle(
    self,
 	frame 
)		
Creates a wiggle effect to give a noisy feel to the plot.

frame : int
    The current frame of the animation.