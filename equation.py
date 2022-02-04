from manim import *


class Eq(Scene):
    def construct(self):
        title = Tex('An $e^-$ inside potential').to_corner(UP + LEFT)
        axes = Axes(
            x_range=[-10, 10, 4],
            y_range=[-1.5, 1.5, 4],
            x_length=6,
            y_length=3,
            axis_config={"color": WHITE, 'font_size': 5},
        ).shift(2.3*DOWN)
        x_label = axes.get_x_axis_label(MathTex('x', font_size=30))
        y_label = axes.get_y_axis_label(MathTex('V(x)', font_size=30))
        axes_g = VGroup(axes, x_label, y_label)
        
        plate_l = Rectangle(color=BLUE, height=6, width=2,
                            fill_opacity=1).shift(4*LEFT)
        plate_r = Rectangle(color=RED, height=6, width=2,
                            fill_opacity=1).shift(4*RIGHT)
        pos_sign = MathTex('+', font_size=70).move_to(plate_r.get_center())
        neg_sign = MathTex('-', font_size=70).move_to(plate_l.get_center())

        def func(x):
            return np.array([-1.0, 0.0, 0.0])
        x_range = [plate_l.get_right()[0], plate_r.get_left()[0], 1.]
        y_range = [plate_l.get_bottom()[1], plate_l.get_top()[1], 1.]
        vector_field = ArrowVectorField(
            func, x_range=x_range, y_range=y_range, length_func=lambda x: x / 2, opacity=0.5
        )
        el = Dot().move_to([0, plate_l.get_center()[1], 0])
        plates = VGroup(plate_l, plate_r, pos_sign, neg_sign)
        set_up = VGroup(plates, el, vector_field)

        """ start of show """
        self.play(Create(title))
        self.play(FadeIn(plates))
        self.play(Create(vector_field))

        self.play(Create(el))
        self.play(set_up.animate.scale(0.5).shift(1.2 * UP))

        disc = [axes.point_to_coords(plate_r.get_left())[0]]

        def potential(x):
            if x >= disc[0]:
                return 1
            else:
                return 0

        plot = axes.plot(potential, discontinuities=disc, dt=0.1, color=BLUE)
        plot.make_jagged()
        eps = 1e-8
        plot2 = axes.plot_line_graph(
            [-8, disc[0], disc[0]+eps, disc[0]+3], [0, 0, 1, 1], add_vertex_dots=False)

        self.wait(2)
        self.play(Create(axes_g))
        self.play(FadeIn(plot2))
        self.wait(1)
