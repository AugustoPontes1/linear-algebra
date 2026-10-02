import numpy as np
import matplotlib.pyplot as plt

from matplotlib.widgets import RadioButtons, Slider

from sim.calculations.polynoms import Polynomial


class FunctionSpacePlot:
    def __init__(self):
        self.f = Polynomial(0, 0, 1)
        self.g = Polynomial(0, 1, 0)
        
        self.scalar = 2
        self.mode = "Par"
        
        self.fig, self.ax = plt.subplots(
            figsize=(10, 7)
        )
        
        plt.subplots_adjust(
            right=0.76,
            bottom=0.35,
        )
        
        self.create_controls()
        self.update()
    
    def create_slider(
        self,
        x,
        y,
        label,
        value,
    ):
        ax = self.fig.add_axes([
            x,
            y,
            0.25,
            0.025,
        ])
        
        slider = Slider(
            ax,
            label,
            -4,
            4,
            valinit=value,
            valstep=1,
        )
        
        slider.on_changed(
            self.on_change
        )
        
        return slider

    def create_controls(self):
        self.f0 = self.create_slider(
            0.08, 0.25, "a₀", 0
        )
        