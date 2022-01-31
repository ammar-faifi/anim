from manim import *


class Mine(Scene):
    def construct(self):
        title = Tex(r"Let's learn diagonalization")
        we_know = Tex(
            r"we know that a \textit{tronsformation matrix equation} \\ is written like"
        )
        matrix_eq = Tex(r"R=Mr")
        VGroup(title, we_know, matrix_eq).arrange(DOWN)
        group1 = [we_know, matrix_eq]
        self.play(Write(title))
        self.wait()
        self.play(FadeIn(we_know), FadeIn(matrix_eq))
        self.wait()

        first_t = Tex("First")
        first_t.to_corner(UP + LEFT)
        self.play(
            Transform(title, first_t),
            LaggedStart(*[FadeOut(obj, direction=DOWN) for obj in group1]),
        )
        self.wait()

        matrix_M = Matrix([["a", "b"], ["c", "d"]]).set_color(YELLOW)
        consider_t = Tex(r"Let $M$ be a transformation matrix")
        t1 = Tex(r"M = ")
        group2 = VGroup(t1, matrix_M).arrange(RIGHT)
        VGroup(consider_t, group2).arrange(DOWN)

        self.play(Write(consider_t))
        self.play(Create(matrix_M), Create(t1))
        self.wait()

        objs = [group2, consider_t]
        thus_t = Tex("Thus we have")
        thus_t.to_corner(LEFT + UP)

        self.play(FadeOut(title))
        self.play(*[FadeOut(obj) for obj in objs])
        self.play(Write(thus_t))
        self.wait()

        right_arrow = MathTex(r"\Rightarrow")
        # matrix_r = Matrix([["x"], ["y"]])
        matrix_r = MathTex(r"\begin{bmatrix} x \\ y \end{bmatrix}")
        matrix_R = Matrix([["X"], ["Y"]])
        equal_sign = MathTex("=")

        matrix_eq_group = VGroup(
            matrix_eq, right_arrow, matrix_R, equal_sign, matrix_M, matrix_r
        ).arrange(RIGHT)

        self.play(Create(matrix_eq_group))
        self.wait()
        self.play(FadeOut(matrix_eq_group))

        lambda_condition_1 = MathTex("R", "=", "\lambda")
        lambda_condition_1.align_to(matrix_r, LEFT)
        lambda_condition = (
            VGroup(lambda_condition_1, matrix_r).arrange().shift(3 * RIGHT)
        )

        lambda_condition_t = Tex("The eigenvalue condition is")
        finally_t = Tex("Finally")
        finally_t.to_corner(LEFT + UP)

        lambda_condition_eq = VGroup(
            MathTex("Mr = \lambda r"),
            right_arrow,
            matrix_M,
            matrix_r.copy(),
            equal_sign,
            MathTex(r"\lambda"),
            matrix_r,
        ).arrange(RIGHT)

        self.play(Write(lambda_condition_t))
        self.wait()
        self.play(FadeOut(lambda_condition_t))

        self.play(Create(lambda_condition))
        self.wait()
        self.play(FadeOut(lambda_condition))

        self.play(FadeOut(thus_t))
        self.play(Write(finally_t))
        self.play(Create(lambda_condition_eq))

        def fadeInAndOut(self, obj, time=2):
            self.play(FadeIn(obj))
            self.wait(time)
            self.play(FadeOut(obj))
