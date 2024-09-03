import manim as ma
from manim import Scene, TexTemplate, config

# use & modify the default `TexTemplate` class
AR_PREAMBLE = r"""
\usepackage[utf8]{inputenc}
\usepackage{arabtex}
\usepackage[arabic]{babel}

\usepackage{amsmath}
\usepackage{amssymb}
"""

config.tex_template = TexTemplate(preamble=AR_PREAMBLE)


class Intro(Scene):
    def construct(self):
        title = ma.Title("خطة محاكاة التصادم").set_color(ma.BLUE)
        self.play(ma.Write(title, reverse=True, remover=False))
        self.wait()

        plan = ma.BulletedList(
            "معادلات الحركة",
            "اكتشاف التصادم",
            "حل التصادم",
        )
        # play list plan
        for l in plan:
            self.play(ma.Write(l, reverse=True, remover=False))
            self.wait()

        # focus on 1st point
        self.play(ma.Create(ma.SurroundingRectangle(plan[0])))
        self.wait()


class EquationsOfMotion(Scene):
    def construct(self):
        particle1 = ma.VGroup(
            ma.Circle(1.0, ma.RED, fill_opacity=1),
            ma.MathTex("1"),
        )
        particle2 = ma.VGroup(
            ma.Circle(1.0, ma.RED, fill_opacity=1),
            ma.MathTex("2"),
        )
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

        # p_1 = ma.MathTex("p_1").next_to(arrow1, ma.UP)
        # p_2 = ma.MathTex("p_2").next_to(arrow2, ma.UP)
        # x_1 = ma.MathTex("x_1").next_to(particle1.submobjects[0], ma.DOWN)
        # x_2 = ma.MathTex("x_2").next_to(particle2.submobjects[0], ma.DOWN)
        # self.play(
        #     ma.FadeIn(p_1),
        #     ma.FadeIn(p_2),
        #     ma.FadeIn(x_1),
        #     ma.FadeIn(x_2),
        # )
        #
        # self.wait()
        # self.next_section()
        #
        # cond = (
        #     ma.VGroup(
        #         ma.MathTex(r"x_2 = -x_1"),
        #         ma.MathTex(r"p_2 = - p_1"),
        #         ma.MathTex(r"\Delta{x_1}\Delta{p_1} \ge \hbar/2"),
        #     )
        #     .arrange(ma.DOWN)
        #     .shift(1.4 * ma.UP)
        #     .scale(0.7)
        # )
        # self.play(ma.Create(cond))
