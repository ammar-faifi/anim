import gettext
from functools import partial
from pathlib import Path

import numpy as np
from manim import *

# from manimlib import *

AR_PREAMBLE = r"""
\usepackage[utf8]{inputenc}
\usepackage{arabtex}
\usepackage[arabic]{babel}

\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{kpfonts}
"""


# Setup translation with its domain
languages = ["en"]
localedir = Path(__file__).parent / "locale"
t = gettext.translation("messages", localedir, languages, fallback=True)
_ = t.gettext
# right to left lang ?
IS_RTL = False

# For Arabic LaTeX
# config.tex_template = TexTemplate(preamble=AR_PREAMBLE)
config.background_color = GRAY_E


def create_square_glow(vmobject, length: float = 1, color=YELLOW):
    glow_group = VGroup()

    for idx in range(50):
        glow_group.add(
            Cube(
                length * (1.01**idx),
                stroke_opacity=0,
                fill_color=color,
                fill_opacity=0.006 - idx / 10_000,
            ).move_to(vmobject)
        )

    return glow_group


def create_glow(vmobject, rad=1, col=YELLOW):
    glow_group = VGroup()

    for idx in range(60):
        glow_group.add(
            Circle(
                radius=rad * (1.002 ** (idx**2)) / 400,
                stroke_opacity=0,
                fill_color=col,
                fill_opacity=0.2 - idx / 300,
            ).move_to(vmobject)
        )

    return glow_group


# Constants
k_B = 1.380649e-23  # Boltzmann constant
c = 2.998e8  # Speed of light


def rayleigh_jeans(wavelength, temperature):
    # with scaling to kW
    return (2 * c * k_B * temperature) / (wavelength**4) * 1e-12


def planck_spectral_radiance(wavelength, temperature):
    """
    Calculate spectral radiance using Planck's law.

    B(λ,T) = (2hc²/λ⁵) × 1/(exp(hc/λkT) - 1)

    Parameters:
    -----------
    wavelength : float or array
        Wavelength in meters
    temperature : float
        Temperature in Kelvin

    Returns:
    --------
    float or array : Spectral radiance in W⋅sr⁻¹⋅m⁻³
    """
    # Physical constants
    h = 6.62607015e-34  # Planck constant (J⋅s)
    c = 299792458  # Speed of light (m/s)
    k_B = 1.380649e-23  # Boltzmann constant (J/K)

    # Avoid division by zero and overflow
    exponent = (h * c) / (wavelength * k_B * temperature)

    # Use np.clip to avoid overflow in exponential
    exponent = np.clip(exponent, 0, 700)  # e^700 is near float64 limit

    numerator = 2 * h * c**2 / (wavelength**5)
    denominator = np.expm1(exponent)  # expm1(x) = exp(x) - 1, more accurate for small x

    return numerator / denominator


def planck_spectral_radiance_normalized(wavelength, temperature, scale_factor=1e-12):
    """
    Calculate normalized spectral radiance for better visualization.

    Parameters:
    -----------
    wavelength : float or array
        Wavelength in meters
    temperature : float
        Temperature in Kelvin
    scale_factor : float
        Scaling factor for the output (default: 1e-12 for kW units)

    Returns:
    --------
    float or array : Scaled spectral radiance
    """
    return planck_spectral_radiance(wavelength, temperature) * scale_factor


def planck_function_nm(wavelength_nm, temperature, scale_factor=1e-12):

    wavelength_m = wavelength_nm * 1e-9  # Convert nm to meters
    return planck_spectral_radiance_normalized(wavelength_m, temperature, scale_factor)


def stefan_boltzmann_law(temperature):
    """
    Calculate total radiated power using Stefan-Boltzmann law.

    j* = σT⁴, where σ = 5.670374419×10⁻⁸ W⋅m⁻²⋅K⁻⁴

    Parameters:
    -----------
    temperature : float
        Temperature in Kelvin

    Returns:
    --------
    float : Total radiated power per unit area (W⋅m⁻²)
    """
    stefan_boltzmann_constant = 5.670374419e-8  # W⋅m⁻²⋅K⁻⁴
    return stefan_boltzmann_constant * temperature**4


def get_wavelength_array(wavelength_range_nm=(200, 3000), num_points=1000):
    """
    Generate wavelength array for plotting.

    Parameters:
    -----------
    wavelength_range_nm : tuple
        Wavelength range in nanometers (min, max)
    num_points : int
        Number of points

    Returns:
    --------
    array : Wavelength array in nanometers
    """
    return np.linspace(wavelength_range_nm[0], wavelength_range_nm[1], num_points)


def wien_displacement(temperature):
    """
    Find the wavelength of maximum emission using Wien's displacement law.

    λ_max = b / T, where b = 2.897771955×10⁻³ m⋅K

    Parameters:
    -----------
    temperature : float
        Temperature in Kelvin

    Returns:
    --------
    float : Peak wavelength in meters
    """
    wien_constant = 2.897771955e-3  # Wien's displacement constant (m⋅K)
    return wien_constant / temperature


class Introduction(ThreeDScene):
    """
    # Points to mention:
        - black body
            - what is the problem
            - what was the solution
            - Rayleigh–Jeans law
            - Rayleigh–Stefan law
            - Wein law
        - how is this trigger the idea of qunta
        - Eienstin's naming photons
        - Later, Hydrogen atom's qunatization of its energy level
        - Bohr's role

    # Visuals:
        - A black body cavity radiating
        - plot raylegh-Jean for different temp
        - show the infinite dillema
        - show the law's equation
    """

    def construct(self):

        title = Title(_("How was Quantum Physics started?"))
        sub_title = Title(_("Black body"))

        this_vid_topics = BulletedList(
            _("Black body."),
            _("Black body radiation."),
            _("Ultraviolet catastrophe."),
            _("Quanta."),
            _("Photons."),
        )

        self.play(Write(title, reverse=True, remover=False))

        for l in this_vid_topics:
            self.play(Write(l, reverse=IS_RTL, remover=False))

        self.play(this_vid_topics.animate.fade_all_but(0))

        self.play(Transform(title, sub_title))
        self.play(FadeOut(this_vid_topics))

        paul_portrait = ImageMobject("./figures/Paul_Ehrenfest.jpg")
        paul_name = Text(_("Paul Ehrenfest")).next_to(paul_portrait, DOWN)
        self.play(FadeIn(paul_portrait))
        self.wait()
        self.play(Write(paul_name, reverse=IS_RTL, remover=False))
        self.play(FadeOut(paul_portrait), Uncreate(paul_name))
        self.wait()

        bb_facts = BulletedList(
            _("It absorbs all light completely."),
            _("It radiates electromagnetic waves base on its temp."),
        )

        for l in bb_facts:
            self.play(Write(l, reverse=IS_RTL, remover=False))

        self.play(bb_facts.animate.fade_all_but(1))
        self.wait()
        self.play(FadeOut(bb_facts))

        axes = (
            Axes(
                x_range=[1, 3000, 100],
                y_range=[0, 25, 2],
                axis_config={"color": BLUE},
                x_axis_config={
                    "numbers_to_include": np.arange(0, 3001, 500),
                    "numbers_with_elongated_ticks": np.arange(0, 3001, 500),
                },
                y_axis_config={
                    "numbers_to_include": np.arange(0, 25, 4),
                    "numbers_with_elongated_ticks": np.arange(0, 25, 4),
                },
                tips=False,
            )
            .scale(0.75)
            .to_edge(RIGHT)
        )

        # Labels
        y_label_m = MathTex(
            r"Spectral Radiance\\",
            r"(",
            "kW",
            r"\cdot",
            "sr^{-1}",
            r"\cdot",
            "m^{-3}",
            ")",
        )
        x_label = axes.get_x_axis_label(r"\lambda (nm)")
        y_label = axes.get_y_axis_label(y_label_m)
        labels = VGroup(x_label, y_label)
        labels.scale(0.5)

        # Visible spectrum range (380nm to 750nm)
        visible_range = Rectangle(
            width=axes.get_x_unit_size() * (750 - 380),
            height=axes.get_y_unit_size() * 25,
            fill_opacity=0.7,
            stroke_width=0,
        )
        visible_range.move_to(axes.c2p((380 + 750) / 2, 0, 0), aligned_edge=DOWN)
        colors = [GRAY_E, PURPLE, BLUE, GREEN, YELLOW, RED, GRAY_E]
        visible_range.set_color_by_gradient(colors)
        visible_range.set_sheen_direction(RIGHT)

        # Visible spectrum label
        visible_label = Text(_("Visible Spectrum"), font_size=14)
        visible_label.next_to(visible_range, UP)

        visible_brace = Brace(visible_range, buff=0.4)
        visible_brace.put_at_tip(visible_label)

        ir_range = Rectangle(
            width=(axes.c2p(3000) - visible_range.get_right())[0],
            height=axes.get_y_unit_size() * 25,
            fill_opacity=0.1,
            stroke_width=0,
        ).next_to(visible_range, RIGHT, buff=0)
        uv_range = Rectangle(
            width=(visible_range.get_left() - axes.c2p(0))[0],
            height=axes.get_y_unit_size() * 25,
            fill_opacity=0.1,
            stroke_width=0,
        ).next_to(visible_range, LEFT, buff=0)

        # Create the black body cube
        cube = Cube(
            side_length=2,
            fill_color=BLACK,
            fill_opacity=0.65,
            stroke_color=DARK_GRAY,
            stroke_width=1,
            stroke_opacity=1,
        )
        cube.set_shade_in_3d(True)
        glow_cube = create_square_glow(cube, 2).set_z_index(-2)
        black_body = VGroup(glow_cube, cube).to_edge(LEFT).rotate(PI / 2, RIGHT)

        #### Animation sequence ####

        # Show axes
        self.play(Create(axes), Write(labels))
        self.wait()

        # Highlight units
        surr = SurroundingRectangle(y_label[2])
        self.play(Create(surr))
        self.play(Transform(surr, SurroundingRectangle(y_label[4])))
        self.play(Transform(surr, SurroundingRectangle(y_label[6])))
        self.play(Uncreate(surr))
        surr = SurroundingRectangle(x_label)
        self.play(Create(surr))
        self.play(Uncreate(surr))
        self.play(FadeOut(labels))

        # Show the visible range
        self.play(Create(visible_brace))
        self.play(FadeIn(visible_range), Write(visible_label))
        self.wait()

        # Show the IR and UV ranges
        self.play(FadeIn(ir_range))
        self.play(Indicate(ir_range, 1.1))
        self.play(FadeOut(ir_range))
        self.play(FadeIn(uv_range))
        self.play(Indicate(uv_range, 1.1))
        self.play(FadeOut(uv_range))

        # Simulate temperature changes with color shifts
        temperatures = [2000, 3000, 4000, 5000, 5500]
        colors = [0xFF0017, 0xFF7C00, 0xCEB04D, 0x83B28D, 0x3DA8AD]

        # Introduce the black body visuals
        self.play(FadeIn(black_body[1]))
        self.play(Rotate(black_body[1], axis=UP), run_time=4)

        # Temperature indicator
        temp_value = Text("1000 K", font_size=28, color=colors[0])
        temp_value.next_to(black_body, DOWN)
        self.play(FadeIn(black_body[0]))
        self.play(FadeIn(temp_value))
        self.play(Indicate(temp_value))

        # Plot first Plank curve
        graph = axes.plot(partial(planck_function_nm, temperature=colors[0]))
        self.play(Create(graph))

        for temp, color in zip(temperatures[1:], colors[1:]):
            new_temp_value = Text(f"{temp} K", font_size=28, color=color)
            new_temp_value.move_to(temp_value.get_center())

            self.play(
                Transform(temp_value, new_temp_value),
                Transform(
                    graph, axes.plot(partial(planck_function_nm, temperature=temp))
                ),
                black_body[0].animate.set_color(color),
                run_time=1.5,
            )
            self.wait(0.5)

        # Show Wien's law equation
        wien_label = (
            Text(_("Wien's Law")).next_to(temp_value, DOWN, buff=0.5).scale(0.8)
        )
        wien_eq = (
            MathTex(r"\lambda_p", "=", r"\frac{b}{T}").move_to(wien_label).scale(0.6)
        )
        wien_eq_const = (
            MathTex(
                r"\lambda",
                r"\approx",
                r"\frac{2.89 \times 10^{-3} \text{m} \cdot \text{K}}{T}",
            )
            .move_to(wien_eq)
            .scale(0.6)
        )
        self.play(Write(wien_label))
        self.play(Unwrite(wien_label))
        self.play(Write(wien_eq))
        self.play(Circumscribe(wien_eq[0]))
        self.play(Circumscribe(wien_eq[2][0]))
        self.play(Circumscribe(wien_eq[2][2]))
        tmp = wien_eq.copy()
        self.play(Transform(wien_eq, wien_eq_const))
        self.play(Transform(wien_eq, tmp))

        # Repeate plots but with Wien's law as points
        peak_dots = VGroup()
        for temp, color in zip(temperatures, colors):
            new_temp_value = Text(f"{temp} K", font_size=28, color=color)
            new_temp_value.move_to(temp_value.get_center())

            self.play(
                Transform(temp_value, new_temp_value),
                Transform(
                    graph, axes.plot(partial(planck_function_nm, temperature=temp))
                ),
                black_body[0].animate.set_color(color),
                run_time=1.5,
            )
            self.wait(0.5)

            peak_at_nm = wien_displacement(temp) / 1e-9
            peak_dot = axes.plot_line_graph(
                [peak_at_nm],
                [planck_function_nm(peak_at_nm, temp)],
                vertex_dot_style={"stroke_width": 1, "fill_color": BLACK},
            )
            self.play(Create(peak_dot))
            peak_dots += peak_dot

        # Clean Screen except the title
        self.play(*[FadeOut(mobj) for mobj in self.mobjects if mobj != title])

        # Show heated iron image
        blacksmith_img = (
            Group(
                ImageMobject("./figures/Blacksmith_at_work02_s.jpg", 800),
                Text("Fir0002/Flagstaffotos, CC BY-NC 3.0", 0.6, font_size=10),
            )
            .arrange(DOWN)
            .to_edge(DOWN)
        )
        self.play(FadeIn(blacksmith_img))
        # Show indication arrow
        arrow = Arrow(start=UP, end=DOWN).shift(UP / 2)
        self.play(Create(arrow))
        self.play(arrow.animate.shift(2 * RIGHT), run_time=4)
        self.play(FadeOut(arrow), FadeOut(blacksmith_img))

        # Show thermal camera image
        human_thermal_img = (
            Group(
                ImageMobject("./figures/Human-Visible.jpg", 600),
                ImageMobject("./figures/Human-Infrared.jpg", 650),
                Text("NASA/IPAC", 0.6, font_size=10),
            )
            .arrange(DOWN)
            .to_edge(DOWN)
        )
        self.play(FadeIn(human_thermal_img))
        self.play(FadeOut(human_thermal_img))

        # Show Sun's surface temperature from as black body radiation
        sun_img = (
            Group(
                ImageMobject("./figures/sun_surface.jpg", 1080),
                Text("NASA/JAXA Hinode mission", 0.6, font_size=10),
            )
            .arrange(DOWN)
            .to_edge(DOWN)
        )
        sun_temp_label = Text("~5,800 K").to_edge(LEFT)
        sun_eff_temp_label = Text("5,778 K").next_to(sun_temp_label, DOWN)
        self.play(FadeIn(sun_img))
        self.play(Write(wien_eq))
        self.play(Write(sun_temp_label))
        self.play(Write(sun_eff_temp_label))
        self.play(*[FadeOut(mobj) for mobj in self.mobjects if mobj != title])

        # Show house daily lamps colors are from black body model
        light_temp = ImageMobject("./figures/lamp_temp.jpg", 1400).to_edge(DOWN)
        self.play(FadeIn(light_temp))
        self.play(FadeOut(light_temp))

        self.wait()
        self.axes = axes
        self.this_vid_topics = this_vid_topics
        self.title = title


class RayleighJeansCatastrophe(Introduction):
    def construct(self):

        self.next_section(skip_animations=True)

        super().construct()

        self.axes.shift(DOWN / 2)

        self.play(FadeIn(self.this_vid_topics))
        self.play(self.this_vid_topics.animate.fade_all_but(1))
        self.play(self.this_vid_topics.animate.fade_all_but(2))
        self.wait()
        self.play(
            FadeOut(self.this_vid_topics),
            Transform(self.title, Title(_("Ultraviolet catastrophe"))),
        )

        # Create graphs for different temperatures
        temperatures = [3000, 4000, 5000]
        graphs = VGroup()
        temp_labels = VGroup()

        for temp in temperatures:
            wavelengths = np.linspace(1100e-9, 3000e-9, 100)
            spectral_radiance = [rayleigh_jeans(w, temp) for w in wavelengths]

            graph = self.axes.plot_line_graph(
                x_values=wavelengths * 1e9,
                y_values=spectral_radiance,
                line_color=BLUE,
                add_vertex_dots=False,
            )

            temp_label = Text(f"{temp}K", font_size=24, color=BLUE_A)
            temp_label.next_to(graph, LEFT)

            graphs.add(graph)
            temp_labels.add(temp_label)

        #### Animation sequence ####

        # Show Rayleigh-Jeans Law equation
        rj_eq = MathTex(r"B = \frac{2 c k_B T}{\lambda^{4}}").to_edge(LEFT)
        self.play(Write(rj_eq))
        # Walk thru its symbols
        self.play(Circumscribe(rj_eq[0][0]))
        self.play(Circumscribe(rj_eq[0][3]))
        self.play(Circumscribe(rj_eq[0][4:6]))
        self.play(Circumscribe(rj_eq[0][6]))
        self.play(Circumscribe(rj_eq[0][8:10]))

        # Reshow the axes
        self.play(Create(self.axes))

        # Show Rayleigh-Jeans plots
        for graph, label in zip(graphs, temp_labels):
            self.play(Create(graph), Write(label), run_time=1.5)
            self.wait(0.5)

        # Highlihgt lambda being in deno
        self.play(Circumscribe(rj_eq[0][8:10]))

        self.next_section()

        # show B goes to inf as labmda goes to 0
        b_limit = (
            MathTex(r"B \rightarrow \infty, \, \lambda \rightarrow 0")
            .next_to(rj_eq, DOWN, buff=1)
            .set_color(RED)
        )
        self.play(Write(b_limit))

        # What is going OnNnNN !?
        big_q = Text('?!', font_size=100).to_edge(RIGHT)
        big_q2 = Text('?', font_size=200).next_to(big_q, UL)
        big_q3 = Text('?', font_size=250).next_to(big_q2, DL)
        big_q4 = Text('?', font_size=150).next_to(big_q3, UL)
        self.play(Create(big_q))
        self.play(Create(big_q2))
        self.play(Create(big_q3))
        self.play(Create(big_q4))

        self.wait()
