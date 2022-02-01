from manim import *


class Eq(Scene):
    def construct(self):
        title = Tex('An $e^-$ inside potential').to_corner(UP + LEFT)
        el = Dot()
        axes = Axes(
            x_range=[-10, 10.3, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=6,
            y_length=3,
            axis_config={"color": WHITE},
            x_axis_config={
                "numbers_to_include": np.arange(-10, 10.01, 2),
                "numbers_with_elongated_ticks": np.arange(-10, 10.01, 2),
            },
            tips=False,
        ).shift(1.5*DOWN)
        plate_l = Rectangle(color=BLUE, height=6, width=2,
                            fill_opacity=1).shift(4*LEFT)
        plate_r = Rectangle(color=RED, height=6, width=2,
                            fill_opacity=1).shift(4*RIGHT)
        plates = VGroup(plate_l, plate_r)

        def func(x):
            return x
        x_range = [plate_l.get_right()[0], plate_r.get_left()[0], 1]
        print(x_range)
        vector_field = ArrowVectorField(
            func, x_range=x_range, y_range=[-2, 2, 1], length_func=lambda x: x / 2
        )

        """ start of show """
        self.play(Create(title))
        self.play(Create(plates))
        self.play(Create(el))

        self.play(plates.animate.scale(0.5).shift(2*UP))
        self.play(Create(axes))

        self.play(Create(vector_field))
        self.play(vector_field.animate.scale(0.5))
