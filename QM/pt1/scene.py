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
        big_q = Text("?!", font_size=100).to_edge(RIGHT)
        big_q2 = Text("?", font_size=200).next_to(big_q, UL)
        big_q3 = Text("?", font_size=250).next_to(big_q2, DL)
        big_q4 = Text("?", font_size=150).next_to(big_q3, UL)
        self.play(Create(big_q))
        self.play(Create(big_q2))
        self.play(Create(big_q3))
        self.play(Create(big_q4))

        self.play(*[FadeOut(mobj) for mobj in self.mobjects if mobj != self.title])

        self.wait()


class PlanckLaw(Scene):
    """
    # Points to mention:
        - Plank idea of qunta
        - Plank's equation
        - E2 - E1 directly propotional to f of light
        - `h` is the proptionality constant

    # Visuals:
        - Show equation
        - show electron jumps E2-E1 ?
        - show the plots from his law
    """

    def construct(self):

        self.next_section(skip_animations=True)

        plank_law = MathTex(
            r"B = \frac{2h\nu^3}{c^2} \cdot \frac{1}{e^{\frac{h\nu}{k_B T}} - 1}"
        )
        quanta_eq = MathTex(r"E_2 - E_1 = h \nu").next_to(plank_law, DOWN)

        # self.play(Write(plank_law))
        # self.play(Write(quanta_eq))

        # Title
        title = Title(r"Plank's Law")
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Create nucleus
        nucleus = Dot(ORIGIN, radius=0.15, color=RED).shift(DOWN)
        nucleus_label = Text(_("Nucleus"), font_size=20).next_to(
            nucleus, DOWN, buff=0.3
        )

        # Ground state orbit (dashed)
        ground_orbit = Circle(radius=1.5, color=BLUE, stroke_width=2)
        ground_orbit.set_stroke(opacity=0.5)
        ground_orbit.move_to(nucleus.get_center())

        # Excited state orbit (dashed)
        excited_orbit = Circle(radius=2.5, color=PURPLE, stroke_width=2)
        excited_orbit.set_stroke(opacity=0.5)
        excited_orbit.move_to(nucleus.get_center())

        # Energy level labels
        ground_label = MathTex("E_1", font_size=32, color=BLUE)
        ground_label.move_to(ground_orbit.point_at_angle(0) + RIGHT * 0.5)

        excited_label = MathTex("E_2", font_size=32, color=PURPLE)
        excited_label.move_to(excited_orbit.point_at_angle(0) + RIGHT * 0.5)

        # Create electron
        electron = Dot(radius=0.1, color=YELLOW).set_z_index(2)
        electron.move_to(ground_orbit.point_at_angle(PI / 2))
        electron_label = Text("e⁻", font_size=24, color=YELLOW).next_to(electron, DOWN)

        # Draw initial setup
        self.play(
            Create(nucleus),
            Write(nucleus_label),
            Create(ground_orbit),
            Create(excited_orbit),
            Write(ground_label),
            Write(excited_label),
        )
        self.play(FadeIn(electron), Write(electron_label))
        self.wait()

        # # Phase 1: Absorption - Incident photon
        # absorption_text = Text("Absorption", font_size=28, color=GREEN).to_edge(DOWN)
        # self.play(Write(absorption_text))
        #
        # # Create incoming photon (EM wave)
        # photon_start = LEFT * 6 + UP * 0.5
        # photon_path = Line(photon_start, nucleus.get_center() + LEFT * 1, color=GREEN)
        #
        # # EM wave representation
        # wave = FunctionGraph(
        #     lambda x: 0.3 * np.sin(5 * x), x_range=[-6, -1], color=GREEN
        # ).shift(UP * 0.5)
        #
        # photon_label = MathTex(r"h\nu = E_2 - E_1", font_size=24, color=GREEN)
        # photon_label.next_to(wave, UP)
        #
        # self.play(Create(wave), Write(photon_label), run_time=1.5)
        #
        # # Photon approaches atom
        # self.play(
        #     wave.animate.shift(RIGHT * 5),
        #     photon_label.animate.shift(RIGHT * 5),
        #     run_time=1.5,
        # )
        #
        # # Absorption occurs - photon disappears, electron excites
        # self.play(FadeOut(wave), FadeOut(photon_label), run_time=0.3)

        # Electron moves to excited state with orbital motion
        ground_orbit.set_stroke(opacity=0.3)
        excited_orbit.set_stroke(opacity=1)
        electron.move_to(excited_orbit.point_at_angle(PI / 2))
        electron_label.next_to(electron, DOWN)

        # # Electron orbits in excited state briefly
        # self.play(
        #     Rotate(electron, angle=2 * PI, about_point=nucleus.get_center()),
        #     Rotate(electron_label, angle=2 * PI, about_point=nucleus.get_center()),
        #     run_time=2,
        #     rate_func=linear,
        # )
        # self.wait(0.5)
        #
        # # Phase 2: Emission - Spontaneous emission
        # self.play(FadeOut(absorption_text))
        # emission_text = Text(
        #     "Spontaneous Emission", font_size=28, color=YELLOW
        # ).to_edge(DOWN)
        # self.play(Write(emission_text))
        #
        # # Electron returns to ground state
        # current_angle = PI * 2  # After one orbit
        # ground_return = ground_orbit.point_at_angle(current_angle)
        #
        # arc_path_return = ArcBetweenPoints(
        #     electron.get_center(), ground_return, angle=PI / 3
        # )
        #
        # # Create emitted photon
        # emitted_wave = FunctionGraph(
        #     lambda x: 0.3 * np.sin(5 * x), x_range=[0, 5], color=YELLOW
        # ).move_to(nucleus.get_center())
        #
        # emitted_photon_label = MathTex(r"h\nu", font_size=24, color=YELLOW)
        # emitted_photon_label.next_to(emitted_wave, UP)
        #
        # self.play(
        #     MoveAlongPath(electron, arc_path_return),
        #     electron_label.animate.move_to(ground_return + RIGHT * 0.3),
        #     electron.animate.set_color(YELLOW),
        #     ground_orbit.animate.set_stroke(opacity=1),
        #     excited_orbit.animate.set_stroke(opacity=0.5),
        #     Create(emitted_wave),
        #     Write(emitted_photon_label),
        #     run_time=1,
        # )
        #
        # # Photon moves away
        # self.play(
        #     emitted_wave.animate.shift(RIGHT * 6),
        #     emitted_photon_label.animate.shift(RIGHT * 6),
        #     run_time=1.5,
        # )
        #
        # self.play(FadeOut(emitted_wave), FadeOut(emitted_photon_label))
        #
        # # Final orbit in ground state
        # self.play(
        #     Rotate(electron, angle=2 * PI, about_point=nucleus.get_center()),
        #     Rotate(electron_label, angle=2 * PI, about_point=nucleus.get_center()),
        #     run_time=2,
        #     rate_func=linear,
        # )
        #
        # self.wait(2)

        atom_model = VGroup(
            nucleus,
            electron,
            ground_orbit,
            excited_orbit,
            ground_label,
            excited_label,
            nucleus_label,
            electron_label,
        )
        self.play(atom_model.animate.scale(0.6).to_edge(LEFT))

        energy_density = MathTex(r"\frac{du}{d\nu}")

        plank_lhs = MathTex(r"\frac{du}{d\nu}")
        plank_rhs = MathTex(r"\frac{du}{d\nu}").to_edge(RIGHT)

        plank_eq = MathTex(
            r"\frac{N_2}{N_1} = "
            r"\frac{B_{12} (\frac{du}{d\nu})}{B_{21} (\frac{du}{d\nu}) + A_{21}}"
        )

        N1, N2 = MathTex("N_1"), MathTex("N_2")
        B12, B21 = MathTex("B_{12}"), MathTex("N_{21}")
        self.play(Write(plank_lhs), Write(plank_rhs))

        self.play(Transform(plank_lhs, MathTex(r"B_{12}\frac{du}{d\nu}")))
        self.play(
            Transform(plank_lhs, MathTex(r"N_1 \left[ B_{12}\frac{du}{d\nu} \right]"))
        )
        self.play(
            Transform(plank_rhs, MathTex(r"B_{21}\frac{du}{d\nu}").to_edge(RIGHT))
        )
        self.play(
            Transform(
                plank_rhs, MathTex(r"B_{21}\frac{du}{d\nu} + A{21}").to_edge(RIGHT)
            )
        )

        self.play(
            Transform(
                plank_rhs,
                MathTex(r"N_2 \left[ B_{21}\frac{du}{d\nu} + A{21} \right]").to_edge(
                    RIGHT
                ),
            )
        )

        self.play(Circumscribe(plank_lhs))
        self.play(Circumscribe(plank_rhs))

        self.play(
            Transform(
                plank_rhs,
                MathTex(r"= N_2 \left[ B_{21}\frac{du}{d\nu} + A{21} \right]").to_edge(
                    RIGHT
                ),
            )
        )
        self.play(FadeOut(plank_lhs), FadeOut(plank_rhs), Write(plank_eq))
        self.play(plank_eq.animate.scale(0.7).next_to(atom_model, UP))

        boltz_2 = MathTex(r"N_2 \propto \exp{\left(-\frac{E_2}{kT} \right)}")
        boltz_1 = MathTex(r"N_1 \propto \exp{\left(-\frac{E_1}{kT} \right)}").next_to(
            boltz_2, DOWN
        )
        boltz_eq = MathTex(
            r"\frac{N_2}{N_1} = " r"\exp{\left( - \frac{E_2 - E_1}{kT} \right)}"
        )

        self.play(Write(boltz_2))
        self.play(Write(boltz_1))
        self.play(
            Transform(
                boltz_2, MathTex(r"N_2 = N_0 \exp{\left(-\frac{E_2}{kT} \right)}")
            ),
            Transform(
                boltz_1,
                MathTex(r"N_1 = N_0 \exp{\left(-\frac{E_1}{kT} \right)}").next_to(
                    boltz_2, DOWN
                ),
            ),
        )
        self.play(Uncreate(boltz_2), Uncreate(boltz_1), Write(boltz_eq))
        self.play(
            boltz_eq.animate.shift(DOWN),
            plank_eq.animate.scale(1.3).next_to(boltz_eq, UP),
            FadeOut(atom_model),
        )

        self.play(
            Uncreate(boltz_eq),
            Transform(
                plank_eq,
                MathTex(
                    r"\exp{\left( - \frac{E_2 - E_1}{kT} \right)} = "
                    r"\frac{B_{12} (\frac{du}{d\nu})}{B_{21} (\frac{du}{d\nu}) + A_{21}}"
                ),
            ),
        )

        self.play(
            Transform(
                plank_eq,
                MathTex(
                    r"\frac{du}{d\nu} = "
                    r"\frac{A_{21} / B_{21}} {\exp{\left(\frac{E_2 - E_1}{kT} \right)} - 1}"
                ),
            ),
        )

        self.play(plank_eq.animate.shift(2 * DOWN))

        plank_assump = (
            VGroup(
                MathTex(r"E_2 - E_1"),
                VGroup(
                    MathTex(r"\propto \nu"),
                    MathTex(r"= h \nu"),
                ),
            )
            .arrange()
            .set_color(BLUE)
        )
        self.play(Write(plank_assump[0]), Write(plank_assump[1][0]))
        self.play(Circumscribe(plank_assump))
        self.play(Transform(plank_assump[1][0], plank_assump[1][1]))
        self.play(FadeOut(plank_assump), FadeOut(plank_eq))

        self.next_section()
        plank_law = MathTex(
            r"B = \frac{2hc^2}{\lambda^2} \frac{1}{e^{\frac{hc}{\lambda kT} - 1}"
        ).scale(1.5)
        self.play(Write(plank_law))
        self.play(Circumscribe(plank_law[0][0]))
        self.play(Circumscribe(plank_law[0][3]))
        self.play(Circumscribe(plank_law[0][4]))
        self.play(Circumscribe(plank_law[0][7]), Circumscribe(plank_law[0][15]))
        self.play(Circumscribe(plank_law[0][16]))
        self.play(Circumscribe(plank_law[0][17]))

        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait()


class PhotoelectricEffectApparatus(VGroup):
    """
    A Manim mobject representing a photoelectric effect apparatus.

    The apparatus consists of:
    - A square vacuum chamber
    - An emitter plate (bottom) - the metal surface that emits electrons
    - A collector plate (top) - catches the emitted electrons
    """

    def __init__(
        self,
        chamber_size=4,
        plate_width=2.5,
        plate_height=0.3,
        plate_separation=2,
        chamber_color=BLUE,
        emitter_color=GOLD,
        collector_color=GRAY,
        **kwargs,
    ):
        super().__init__(**kwargs)

        # Create the vacuum chamber (square)
        self.chamber = Square(
            side_length=chamber_size,
            color=chamber_color,
            stroke_width=3,
            fill_opacity=0.06,
        )

        # Create the emitter (bottom metal plate - photocathode)
        self.emitter = Rectangle(
            width=plate_width,
            height=plate_height,
            color=emitter_color,
            fill_opacity=0.8,
            stroke_width=2,
        )

        # Create the collector (top plate - anode)
        self.collector = Rectangle(
            width=plate_width,
            height=plate_height,
            color=collector_color,
            fill_opacity=0.6,
            stroke_width=2,
        )

        # Position the emitter at the bottom
        self.emitter.shift(DOWN * plate_separation / 2)

        # Position the collector at the top
        self.collector.shift(UP * plate_separation / 2)

        # Add labels
        self.emitter_label = Text("Emitter\n(Photocathode)", font_size=18)
        self.emitter_label.next_to(self.emitter, DOWN, buff=0.3)

        self.collector_label = Text("Collector\n(Anode)", font_size=18)
        self.collector_label.next_to(self.collector, UP, buff=0.3)

        # Add terminal connections (small circles for electrical connections)
        self.emitter_terminal = Circle(radius=0.1, color=RED, fill_opacity=1)
        self.emitter_terminal.next_to(self.emitter, LEFT, buff=0.1)

        self.collector_terminal = Circle(radius=0.1, color=RED, fill_opacity=1)
        self.collector_terminal.next_to(self.collector, LEFT, buff=0.1)

        # Add wires connecting to terminals
        self.emitter_wire = Line(
            self.emitter.get_left(),
            self.emitter_terminal.get_center(),
            color=RED,
            stroke_width=2,
        )

        self.collector_wire = Line(
            self.collector.get_left(),
            self.collector_terminal.get_center(),
            color=RED,
            stroke_width=2,
        )

        # Create voltage indicator (circular meter with arrow)
        voltmeter_radius = 0.5
        self.voltmeter = Circle(radius=voltmeter_radius, color=WHITE, stroke_width=3)

        # Position voltmeter to the left of the chamber
        voltmeter_position = self.chamber.get_left() + LEFT * 1.5
        self.voltmeter.move_to(voltmeter_position)

        # Create the indicator arrow (needle) inside the voltmeter
        self.voltmeter_arrow = Arrow(
            start=self.voltmeter.get_center(),
            end=self.voltmeter.get_center() + UP * voltmeter_radius * 0.7,
            color=RED,
            buff=0,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.3,
        )

        # Add V label on the voltmeter
        self.voltmeter_label = Text("V", font_size=24, color=YELLOW)
        self.voltmeter_label.move_to(self.voltmeter.get_center() + DOWN * 0.25)

        # Create connection wires from voltmeter to terminals
        # Top connection to collector terminal
        self.voltmeter_top_connection = self.voltmeter.get_top() + UP * 0.1
        self.voltmeter_to_collector = VGroup()

        # Wire going up and then right to collector terminal
        wire_point1 = self.voltmeter.get_top()
        wire_point2 = wire_point1 + UP * 0.5
        wire_point3 = [self.collector_terminal.get_center()[0], wire_point2[1], 0]
        wire_point4 = self.collector_terminal.get_center()

        self.voltmeter_to_collector.add(
            Line(wire_point1, wire_point2, color=RED, stroke_width=2),
            Line(wire_point2, wire_point3, color=RED, stroke_width=2),
            Line(wire_point3, wire_point4, color=RED, stroke_width=2),
        )

        # Bottom connection to emitter terminal
        self.voltmeter_to_emitter = VGroup()

        # Wire going down and then right to emitter terminal
        wire_point1 = self.voltmeter.get_bottom()
        wire_point2 = wire_point1 + DOWN * 0.5
        wire_point3 = [self.emitter_terminal.get_center()[0], wire_point2[1], 0]
        wire_point4 = self.emitter_terminal.get_center()

        self.voltmeter_to_emitter.add(
            Line(wire_point1, wire_point2, color=RED, stroke_width=2),
            Line(wire_point2, wire_point3, color=RED, stroke_width=2),
            Line(wire_point3, wire_point4, color=RED, stroke_width=2),
        )

        # Add all components to the VGroup
        self.add(
            self.chamber,
            self.emitter,
            self.collector,
            self.emitter_label,
            self.collector_label,
            self.emitter_terminal,
            self.collector_terminal,
            self.emitter_wire,
            self.collector_wire,
            self.voltmeter,
            self.voltmeter_label,
            self.voltmeter_to_collector,
            self.voltmeter_to_emitter,
            self.voltmeter_arrow,
        )

    def create_photon(self, color=YELLOW):
        """Create a photon (represented as a wavy arrow or dot)"""
        photon = Dot(color=color, radius=0.1)
        photon.move_to(self.chamber.get_right() + RIGHT * 0.5)
        return photon

    def create_electron(self):
        """Create an electron (represented as a small blue dot with minus sign)"""
        electron = VGroup()
        dot = Dot(color=BLUE, radius=0.08)
        minus = Text("-", font_size=16, color=WHITE)
        minus.move_to(dot.get_center())
        electron.add(dot, minus)
        return electron

    def get_emitter_surface(self):
        """Return the top surface point of the emitter for electron emission"""
        return self.emitter.get_top()

    def get_collector_surface(self):
        """Return the bottom surface point of the collector"""
        return self.collector.get_bottom()

    def set_voltage_arrow_angle(self, angle):
        """
        Rotate the voltmeter arrow to indicate voltage level.
        angle in degrees: -90 (left) to +90 (right), 0 is up
        """
        # Remove old arrow
        self.remove(self.voltmeter_arrow)

        # Create new arrow at the specified angle
        angle_rad = angle * DEGREES
        end_point = self.voltmeter.get_center() + np.array(
            [np.sin(angle_rad) * 0.35, np.cos(angle_rad) * 0.35, 0]
        )

        self.voltmeter_arrow = Arrow(
            start=self.voltmeter.get_center(),
            end=end_point,
            color=RED,
            buff=0,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.3,
        )

        # Add the new arrow back
        self.add(self.voltmeter_arrow)

    def animate_set_voltage_angle(self, angle):
        # Create new arrow at the specified angle
        angle_rad = angle * DEGREES
        end_point = self.voltmeter.get_center() + np.array(
            [np.sin(angle_rad) * 0.35, np.cos(angle_rad) * 0.35, 0]
        )

        return self.voltmeter_arrow.animate.put_start_and_end_on(
            self.voltmeter.get_center(), end_point
        )


class PhotoelectricEffect(Scene):
    """
    # Points to mention:
        - photoelectric effect

    # Visuals:
        - Show expreiment apartus
    """

    def construct(self):

        self.next_section(skip_animations=True)

        # Title
        title = Title(_("Photoelectric Effect"))
        self.play(Write(title))

        # Create the apparatus
        apparatus = PhotoelectricEffectApparatus()

        self.play(Write(title))
        self.play(Create(apparatus), run_time=2)

        # Demonstrate photon hitting emitter and electron emission
        for i in range(3):
            # Create photon
            photon = apparatus.create_photon()

            # Animate photon moving toward emitter
            self.play(
                photon.animate.move_to(apparatus.get_emitter_surface()), run_time=0.8
            )
            self.play(apparatus.animate_set_voltage_angle(30 * (i + 1)))

            # Remove photon and create electron
            electron = apparatus.create_electron().set_z_index(-1)
            electron.move_to(apparatus.get_emitter_surface())

            e_to = (
                apparatus.get_collector_surface() / 2
                if i == 2
                else apparatus.get_collector_surface()
            )
            self.play(
                FadeOut(photon),
                electron.animate.move_to(e_to),
            )
            self.play(FadeOut(electron))

        self.play(apparatus.animate.to_edge(LEFT))

        self.next_section()

        w_min_prop = MathTex(r"W \propto \nu_0").to_edge(RIGHT, buff=1.5)
        w_min = MathTex(r"W = h \nu_0").to_edge(RIGHT, buff=1.5)
        k_max = MathTex(r"K_{max} = h\nu - W").next_to(w_min, DOWN)

        self.play(Write(w_min_prop[0][0]))
        self.play(Write(w_min_prop[0][1:]))
        self.play(ReplacementTransform(w_min_prop, w_min))
        self.play(w_min.animate.shift(UP))
        self.play(Write(k_max[0][0:4]))
        self.play(Write(k_max[0][4:7]))
        self.play(Write(k_max[0][7:]))

        self.wait()
