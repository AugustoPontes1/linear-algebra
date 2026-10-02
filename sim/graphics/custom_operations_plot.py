import matplotlib.pyplot as plt

from matplotlib.widgets import RadioButtons, Slider

from sim.calculations.custom_space import PRESETS
from sim.calculations.rules import VectorSpaceAxioms
from sim.calculations.vector import Vector


class CustomOperationsPlot:
    def __init__(self):
        self.operations_name = "Usual"
        self.rule_index = 0
        
        self.u = Vector(1, 2)
        self.v = Vector(2, 1)
        self.w = Vector(-1, 2)
        
        self.a = 2
        self.b = -1
        
        self.fig, self.ax = plt.subplots(
            figsize=(11,1 )
        )
        
        plt.subplots_adjust(
            left=0.08,
            right=0.70,
            bottom=0.40,
            top=0.90,
        )
        
        self.create_controls()
        self.update()
    
    def create_slider(
        self,
        position,
        label,
        initial,
    ):
        axis = self.fig.add_axes(
            position
        )
        
        slider = Slider(
            axis,
            label,
            -5,
            5,
            valinit=initial,
            valstep=1,
        )

        slider.on_changed(
            self.on_change
        )
        
        return slider

    def create_controls(self):
        self.ux = self.create_slider(
            [0.08, 0.30, 0.25, 0.025],
            "ux",
            1,
        )
        
        self.uy = self.create_slider(
            [0.08, 0.26, 0.25, 0.025],
            "uy",
            2,
        )
        
        self.vx = self.create_slider(
            [0.38, 0.30, 0.25, 0.025],
            "vx",
            2,
        )
        
        self.vy = self.create_slider(
            [0.38, 0.26, 0.25, 0.025],
            "vy",
            1,
        )
        
        self.wx = self.create_slider(
            [0.08, 0.20, 0.25, 0.025],
            "wx",
            -1
        )
        
        self.wy = self.create_slider(
            [0.08, 0.16, 0.25, 0.025],
            "wy",
            2,
        )
        
        self.slider_a = self.create_slider(
            [0.38, 0.20, 0.25, 0.025],
            "a",
            2,
        )
        
        self.slider_b = self.create_slider(
            [0.38, 0.16, 0.25, 0.025],
            "b",
            -1,
        )
        
        preset_axis = self.fig.add_axes([
            0.73,
            0.58,
            0.24,
            0.28,
        ])
        
        self.present_radio = RadioButtons(
            preset_axis,
            tuple(PRESETS.keys())
        )
        
        self.present_radio.on_clicked(
            self.change_preset
        )
        
        rule_axis = self.fig.add_axes([
            0.73,
            0.10,
            0.24,
            0.40,
        ])
        
        self.rule_radio = RadioButtons(
            rule_axis,
            (
        
                "Associatividade",
                "Comutatividade",
                "Vetor nulo",
                "Vetor oposto",
                "Distrib. vetores",
                "Distrib. escalares",
                "Assoc. escalares",
                "Identidade",                
            ),
        )
        
        self.rule_radio.on_clicked(
            self.change_rule
        )
    
    def on_change(self, _):
        self.u = Vector(
            self.ux.val,
            self.uy.val,
        )
        
        self.v = Vector(
            self.vx.val,
            self.vy.val,
        )
        
        self.w = Vector(
            self.wx.val,
            self.wy.val,
        )
        
        self.a = self.slider_a.val
        self.b = self.slider_b.val
        
        self.update()
    
    def change_preset(self, name):
        self.operations_name = name
        self.update()
    
    def change_rule(self, label):
        labels = (
            "Associatividade",
            "Comutatividade",
            "Vetor nulo",
            "Vetor oposto",
            "Distrib. vetores",
            "Distrib. escalares",
            "Assoc. escalares",
            "Identidade",            
        )
        
        self.rule_index = labels.index(
            label
        )
        
        self.update()
    
    def draw_vector(
        self,
        vector,
        label,
    ):
        if not isinstance(vector, Vector):
            return
        
        x, y = vector.values
        
        self.ax.quiver(
            0,
            0,
            x,
            y,
            angles="xy",
            scale_units="xy",
            scale=1,
            label=label,
        )
        
    def update(self):
        operations = PRESETS[
            self.operations_name
        ]
        
        results = VectorSpaceAxioms.check_all(
            operations,
            self.u,
            self.v,
            self.w,
            self.a,
            self.b
        )
        
        result = results[
            self.rule_index
        ]
        
        self.ax.clear()
        
        self.ax.axhline(0)
        self.ax.axvline(0)
        
        self.ax.set_xlim(-15, 15)
        self.ax.set_ylim(-15, 15)
        
        self.ax.set_aspect("equal")
        self.ax.grid(True)
        
        self.draw_vector(
            self.u,
            f"u{self.u.values}",
        )
        
        self.draw_vector(
            self.v,
            f"v={self.v.values}",
        )
        
        self.draw_vector(
            result.left,
            f"Lado Esquerdo: {result.left}",
        )
        
        self.draw_vector(
            result.right,
            f"Lado direito: {result.right}",
        )
        
        status = (
            "SATISFEITA"
            if result.valid
            else "FALHOU"
        )
        
        self.ax.set_title(
            f"{self.operations_name}\n"
            f"{result.name}\n"
            f"{status}"
        )
        
        self.ax.legend()
        
        self.fig.canvas.draw_idle()

    def show(self):
        plt.show()

if __name__ == "__main__":
    CustomOperationsPlot().show()