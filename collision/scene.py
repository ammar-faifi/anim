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
        pass
        newton_eq = ma.MathTex("F = ma")
        verlet = ma.MathTex(
            r"\displaystyle {\boldsymbol {M}}{\ddot {\mathbf {x} }}(t)=F{\bigl (}\mathbf {x} (t){\bigr )}=-\nabla V{\bigl (}\mathbf {x} (t){\bigr )}"
        )

        self.play(ma.Write(newton_eq))
        self.wait()
        self.embed()


class Collision(Scene):
    def construct(self):
        self.next_section(skip_animations=True)
        circle1 = ma.VGroup(
            ma.Circle(1.0, ma.RED, fill_opacity=1), ma.MathTex("1")
        ).shift(2 * ma.LEFT)
        circle2 = ma.VGroup(
            ma.Circle(1.0, ma.GREEN, fill_opacity=1), ma.MathTex("2")
        ).shift(2 * ma.RIGHT)
        circle3 = ma.VGroup(
            ma.Circle(1.0, ma.BLUE, fill_opacity=1), ma.MathTex("3")
        ).shift(2 * ma.RIGHT)

        self.play(ma.Create(circle1))
        self.play(ma.Create(circle2))
        self.wait()

        self.play(ma.FadeOut(circle1[1]), ma.FadeOut(circle2[1]))

        dist = ma.DoubleArrow(circle1[0].get_left(), circle1[0].get_right(), buff=0)
        self.play(ma.FadeIn(dist))
        self.wait()
        self.play(ma.FadeOut(dist))
        self.wait()

        dist = ma.DoubleArrow(circle1[0].get_center(), circle2[0].get_center(), buff=0)
        self.play(ma.FadeIn(dist))
        self.wait()
        self.play(ma.FadeOut(dist))
        self.wait()

        self.play(circle2.animate.next_to(circle1, buff=0))
        self.play(ma.FadeOut(circle2[1]))

        dist = ma.DoubleArrow(circle1[0].get_center(), circle2[0].get_center(), buff=0)
        self.play(ma.FadeIn(dist))
        self.wait()
        self.play(dist.animate.shift(ma.UP * 2))
        self.wait()

        self.play(circle2[0].animate.next_to(circle1, buff=-0.5))

        self.next_section()

        dist = ma.DoubleArrow(circle1[0].get_center(), circle2[0].get_center(), buff=0)
        self.play(ma.FadeIn(dist))
        self.wait()
        self.play(dist.animate.shift(ma.UP * 1.5))
        self.wait()

        inter = ma.Intersection(
            circle1[0],
            circle2[0],
            fill_color=ma.YELLOW,
            stroke_color=ma.YELLOW,
            fill_opacity=1,
        )
        self.play(ma.Create(inter))
        self.wait()
        self.play(ma.ScaleInPlace(inter, 1.5))
        self.play(ma.ScaleInPlace(inter, 1 / 1.5))
        self.wait()
        self.play(ma.FadeOut(inter))

        diff = inter.get_right() - inter.get_left()
        self.play(circle2[0].animate.shift(diff / 2))
        self.play(circle1[0].animate.shift(-diff / 2))
        self.wait()

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
