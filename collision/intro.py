import manim as ma
from manim import Scene, TexTemplate, config

# use & modify the default `TexTemplate` class
AR_PREAMBLE = r"""
\usepackage[utf8]{inputenc}
\usepackage{arabtex}
\usepackage[english, arabic]{babel}

%\babelfont{rm}[Renderer=Harfbuzz]{FreeSerif}
\usepackage{amsmath}
\usepackage{amssymb}
"""

config.tex_template = TexTemplate(
    tex_compiler="latex", preamble=AR_PREAMBLE, output_format='.dvi'
)


class EPRExperiment(Scene):
    def construct(self):
        title = ma.Title(r"التجربة").set_color(ma.BLUE)
        self.add(title)
        self.wait()
        self.play(ma.Transform(title, ma.Title("اكتشاف التصادم").set_color(ma.BLUE)))
        self.wait()
        self.next_section()

        particle1 = ma.VGroup(
            ma.Circle(0.4, ma.RED, fill_opacity=1),
            ma.Tex("1"),
        )
        particle2 = ma.VGroup(
            ma.Circle(0.4, ma.RED, fill_opacity=1),
            ma.Tex("2"),
        )
        numberline = ma.NumberLine(None, 10)
        x_label = ma.MathTex("x").next_to(numberline)
        self.play(ma.Create(numberline), ma.Create(x_label))
        self.play(ma.Create(particle1))
        self.wait()

        # throw them apart
        arrow1 = ma.Arrow(ma.LEFT, ma.RIGHT, color=ma.GOLD).next_to(
            particle1, ma.UP + 0.5 * ma.RIGHT
        )
        arrow2 = ma.Arrow(ma.RIGHT, ma.LEFT, color=ma.GOLD).next_to(
            particle2, ma.UP + 0.5 * ma.LEFT
        )

        self.play(
            ma.FadeIn(arrow1),
            arrow1.animate.shift(ma.RIGHT * 3),
            particle1.animate.shift(ma.RIGHT * 3),
            ma.FadeIn(arrow2),
            arrow2.animate.shift(ma.LEFT * 3),
            particle2.animate.shift(ma.LEFT * 3),
        )

        p_1 = ma.MathTex("p_1").next_to(arrow1, ma.UP)
        p_2 = ma.MathTex("p_2").next_to(arrow2, ma.UP)
        x_1 = ma.MathTex("x_1").next_to(particle1.submobjects[0], ma.DOWN)
        x_2 = ma.MathTex("x_2").next_to(particle2.submobjects[0], ma.DOWN)
        self.play(
            ma.FadeIn(p_1),
            ma.FadeIn(p_2),
            ma.FadeIn(x_1),
            ma.FadeIn(x_2),
        )

        self.wait()
        self.next_section()

        cond = (
            ma.VGroup(
                ma.MathTex(r"x_2 = -x_1"),
                ma.MathTex(r"p_2 = - p_1"),
                ma.MathTex(r"\Delta{x_1}\Delta{p_1} \ge \hbar/2"),
            )
            .arrange(ma.DOWN)
            .shift(1.4 * ma.UP)
            .scale(0.7)
        )
        self.play(ma.Create(cond))
        self.next_section()
        #
        # line1 = (
        #     ma.BulletedList(
        #         "Measuring $x_2$ allows you to predict $x_1$, so $x_1$ becomes `real.'",
        #         "Measuring $p_2$ allows you to predict $p_1$, so $p_1$ becomes `real.'",
        #         "Reality for particle 1 depends on measurements made on particle 2.",
        #     )
        #     .scale(0.7)
        #     .shift(2.3 * ma.DOWN)
        # )
        #
        # self.play(ma.Write(line1[0]))
        # self.next_section()
        # self.play(ma.Write(line1[1]))
        # self.next_section()
        # self.play(ma.Write(line1[2]))
        # self.next_section()
