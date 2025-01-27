from manim import *
import manim as ma
from manim import Scene, TexTemplate, config

# use & modify the default `TexTemplate` class
AR_PREAMBLE = r"""
\usepackage[utf8]{inputenc}
\usepackage{arabtex}
\usepackage[arabic]{babel}

\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{kpfonts}
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
        RADIUS = 1.0

        circle1 = ma.VGroup(
            ma.Circle(RADIUS, ma.RED, fill_opacity=1), ma.MathTex("1")
        ).shift(2 * ma.LEFT)
        circle2 = ma.VGroup(
            ma.Circle(RADIUS, ma.GREEN, fill_opacity=1), ma.MathTex("2")
        ).shift(2 * ma.RIGHT)
        circle3 = ma.VGroup(
            ma.Circle(RADIUS, ma.BLUE, fill_opacity=1), ma.MathTex("3")
        ).shift(2 * ma.RIGHT)

        self.play(ma.Create(circle1))
        self.play(ma.Create(circle2))
        self.wait()

        self.play(ma.FadeOut(circle1[1]), ma.FadeOut(circle2[1]))

        dist1 = ma.DoubleArrow(circle1[0].get_left(), circle1[0].get_right(), buff=0)
        self.play(ma.FadeIn(dist1))
        self.wait()
        self.play(ma.FadeOut(dist1))
        self.wait()

        dist1 = ma.DoubleArrow(circle1[0].get_center(), circle2[0].get_center(), buff=0)
        self.play(ma.FadeIn(dist1))
        self.wait()
        self.play(ma.FadeOut(dist1))
        self.wait()

        self.play(circle2.animate.next_to(circle1, buff=0))
        self.play(ma.FadeOut(circle2[1]))

        EQ_REF = RIGHT * 4 + UP

        calc_text = Tex("حساب التداخل", color=BLUE).move_to(EQ_REF + UP)
        self.play(Write(calc_text, reverse=True, remover=False))

        dist_eq = MathTex(r"2 r - |\vec{v_2} - \vec{v_1}|").move_to(EQ_REF)
        dist_eq_1 = MathTex(r"d").move_to(EQ_REF)

        self.play(Write(dist_eq))
        self.wait()
        self.play(Transform(dist_eq[0][-9:], dist_eq_1))
        self.wait()

        dist_ineq = MathTex(r"2r - d > 0").move_to(EQ_REF + DOWN)
        self.play(Write(dist_ineq))
        self.wait()

        dis_vec = MathTex(
            r"\vec{a}",
            r"=",
            r"\frac{2r-d}{2}",
            r"\cdot",
            r"\frac{\vec{v_2} - \vec{v_1}}{d}",
        ).move_to(EQ_REF + DOWN * 2)
        self.play(Write(dis_vec))

        self.wait()
        surr = SurroundingRectangle(dis_vec[2])
        self.play(Create(surr))
        self.wait()
        self.play(Transform(surr, SurroundingRectangle(dis_vec[3])))
        self.play(Transform(surr, SurroundingRectangle(dis_vec[4])))
        self.wait()
        self.play(Transform(surr, SurroundingRectangle(dis_vec[0])))
        self.wait()
        self.play(FadeOut(surr))

        dist1 = ma.DoubleArrow(circle1[0].get_center(), circle2[0].get_center(), buff=0)
        self.play(ma.FadeIn(dist1))
        self.wait()
        self.play(dist1.animate.shift(ma.UP * 2))
        self.wait()

        self.play(circle2[0].animate.next_to(circle1, buff=-0.5))

        dist2 = ma.DoubleArrow(circle1[0].get_center(), circle2[0].get_center(), buff=0)
        self.play(ma.FadeIn(dist2))
        self.wait()
        self.play(dist2.animate.shift(ma.UP * 1.5))
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
        self.play(ma.FadeOut(dist2))
        self.play(ma.FadeOut(dist1))
        self.wait()

        mid_point_up = (circle1[0].get_center() + circle2[0].get_center()) / 2
        mid_point_up = mid_point_up + ma.UP * 1.5
        circle3.move_to(mid_point_up)
        self.play(ma.Create(circle3))
        self.wait()

        self.play(ma.FadeOut(circle3[1]))

        v1 = circle1[0].get_center()
        v2 = circle2[0].get_center()
        v3 = circle3[0].get_center()

        def displacement(p1, p2, r=RADIUS):
            overlap = 2 * r - np.linalg.norm(p2 - p1)
            return overlap * (p2 - p1) / 3.5

        self.play(circle3[0].animate.shift(displacement(v1, v3)))
        self.play(circle1[0].animate.shift(-displacement(v1, v3)))

        self.play(circle3[0].animate.shift(displacement(v2, v3)))
        self.play(circle2[0].animate.shift(-displacement(v2, v3)))

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
