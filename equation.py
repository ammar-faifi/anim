from manim import *


class Eq(Scene):
    def construct(self):
        title = Tex('An $e^-$ inside potential').to_corner(UP + LEFT)
        axes = Axes(
            x_range=[-10, 10, 11],
            y_range=[-1.5, 1.5, 4],
            x_length=6,
            y_length=3,
            axis_config={"color": WHITE},
            tips=False,
        ).shift(2*DOWN)
        plate_l = Rectangle(color=RED, height=6, width=2,
                            fill_opacity=1).shift(4*LEFT)
        plate_r = Rectangle(color=BLUE, height=6, width=2,
                            fill_opacity=1).shift(4*RIGHT)

        def func(x):
            return np.array([1.0, 0.0, 0.0])
        x_range = [plate_l.get_right()[0], plate_r.get_left()[0], 1.]
        y_range = [plate_l.get_bottom()[1], plate_l.get_top()[1], 1.]
        vector_field = ArrowVectorField(
            func, x_range=x_range, y_range=y_range, length_func=lambda x: x / 2, opacity=0.5
        )
        el = Dot().move_to([0, plate_l.get_center()[1], 0])
        plates = VGroup(plate_l, plate_r)
        set_up = VGroup(plates, el, vector_field)

        """ start of show """
        self.play(Create(title))
        self.play(FadeIn(plates))
        self.play(Create(vector_field))

        self.play(Create(el))
        self.play(set_up.animate.scale(0.5).shift(1.2 * UP))

        disc = [axes.point_to_coords(plate_l.get_right())[0],
                axes.point_to_coords(plate_r.get_left())[0]]

        def potential(x):
            if disc[0] <= x <= disc[1]:
                return 0
            else:
                return 1

        plot = axes.plot(potential, discontinuities=disc, dt=0.1, color=WHITE)
        plot.make_jagged()

        self.play(Create(axes))
        self.play(FadeIn(plot))
        self.wait(1)
