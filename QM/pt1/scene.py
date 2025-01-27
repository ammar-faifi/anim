import gettext import os

from manim import *

AR_PREAMBLE = r"""
\usepackage[utf8]{inputenc}
\usepackage{arabtex}
\usepackage[arabic]{babel}

\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{kpfonts}
"""

config.tex_template = TexTemplate(preamble=AR_PREAMBLE)


# Setup translatoin with its domain
languages = ["ar"]
localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "locale")
translate = gettext.translation("messages", localedir, languages, fallback=True)
_ = translate.gettext
# right to left lang ?
IS_RTL = True


class Introduction(Scene):
    """
    Points to mention:
        - black body
            - what is the problem
            - what was the solution
        - how is this trigger the idea of qunta
        - Eienstin's naming photons
        - Later, Hydrogen atom's qunatization of its energy level
        - Bohr's role
    """

    def construct(self):

        title = Title(_("How was Quantum Physics started?"))
        sub_title = Title(_("Ultraviolet catastrophe"))

        self.play(Write(title, reverse=True, remover=False))
        self.play(Transform(title, sub_title))

        paul_portrait = ImageMobject("./Paul_Ehrenfest.jpg")
        paul_name = Text(_("Paul Ehrenfest")).next_to(paul_portrait, DOWN)
        self.play(FadeIn(paul_portrait))
        self.wait()
        self.play(Write(paul_name, reverse=IS_RTL, remover=not IS_RTL))
        self.play(FadeOut(paul_portrait), Uncreate(paul_name))
        self.wait()


class RayleighJeansCatastrophe(Scene):
    def construct(self):
        # Constants
        k_B = 1.380649e-23  # Boltzmann constant
        c = 2.998e8  # Speed of light

        # Create axes
        axes = Axes(
            x_range=[0, 3e-6, 0.5e-6],
            y_range=[0, 5e13, 1e13],
            axis_config={"color": WHITE},
            x_axis_config={
                "numbers_to_include": np.arange(0, 3.5e-6, 0.5e-6),
                "numbers_with_elongated_ticks": np.arange(0, 3.5e-6, 0.5e-6),
            },
            y_axis_config={
                "numbers_to_include": np.arange(0, 6e13, 1e13),
                "numbers_with_elongated_ticks": np.arange(0, 6e13, 1e13),
            },
            tips=False,
        )

        # Labels
        x_label = axes.get_x_axis_label("Wavelength (m)")
        y_label = axes.get_y_axis_label(
            r"Spectral Radiance\\(W\cdot sr^{-1}\cdot m^{-3})"
        )
        labels = VGroup(x_label, y_label)

        # Title
        title = Text("Rayleigh-Jeans Catastrophe", font_size=40)
        title.to_edge(UP)

        # Visible spectrum range (380nm to 750nm)
        visible_range = Rectangle(
            width=axes.x_axis.unit_size * (750e-9 - 380e-9), height=6, fill_opacity=0.3
        )
        visible_range.move_to(
            axes.c2p((380e-9 + 750e-9) / 2, 2.5e13, 0), aligned_edge=ORIGIN
        )

        # Create gradient for visible spectrum
        colors = [PURPLE, BLUE, GREEN, YELLOW, RED]
        visible_range.set_color_by_gradient(*colors)

        # Function to calculate Rayleigh-Jeans spectral radiance
        def rayleigh_jeans(wavelength, temperature):
            return (2 * c * k_B * temperature) / (wavelength**4)

        # Create graphs for different temperatures
        temperatures = [3000, 4000, 5000]
        graphs = VGroup()
        temp_labels = VGroup()

        for i, temp in enumerate(temperatures):
            wavelengths = np.linspace(1e-7, 3e-6, 1000)
            spectral_radiance = [rayleigh_jeans(w, temp) for w in wavelengths]

            graph = axes.plot_line_graph(
                x_values=wavelengths, y_values=spectral_radiance, line_color=BLUE
            )

            temp_label = Text(f"{temp}K", font_size=24, color=BLUE_A)
            temp_label.next_to(graph, RIGHT)

            graphs.add(graph)
            temp_labels.add(temp_label)

        # Visible spectrum label
        visible_label = Text("Visible Spectrum", font_size=24)
        visible_label.next_to(visible_range, UP)

        # Animation sequence
        self.play(Write(title))
        self.play(Create(axes), Write(labels))
        self.wait()

        self.play(FadeIn(visible_range), Write(visible_label))
        self.wait()

        for graph, label in zip(graphs, temp_labels):
            self.play(Create(graph), Write(label), run_time=1.5)
            self.wait(0.5)

        self.wait(2)
