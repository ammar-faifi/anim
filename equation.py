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
        self.wait()
        self.play(set_up.animate.scale(0.5).shift(1.2 * UP))

        disc_l = axes.point_to_coords(plate_l.get_right())[0]
        disc_r = axes.point_to_coords(plate_r.get_left())[0]

        eps = 1e-8
        plot = axes.plot_line_graph(
            [-8, disc_l, disc_l+eps, disc_r, disc_r+eps, disc_r+3], [-1, -1, 0, 0, 1, 1], add_vertex_dots=False)
        plot2 = axes.plot_line_graph(
            [-8, disc_r+3], [-0.8, -0.8], add_vertex_dots=False)
        plot_E = axes.plot_line_graph([-8, 8], [0.5, 0.5], add_vertex_dots=False, line_color=BLUE)


        self.wait()
        self.play(Create(axes_g))
        self.play(FadeIn(plot))
        self.wait()

        force_arrow = Arrow([-0.5, 1, 0], [+0.5, 1, 0])
        force_label = MathTex('F_e', font_size=20).next_to(force_arrow)
        self.play(Create(force_arrow), Create(force_label))
        self.wait()
        el_origin = el.get_center()
        self.play(el.animate(rate_func=rate_functions.ease_in_quad).move_to(
            plate_r.get_left()))
        self.play(FadeOut(force_arrow), FadeOut(force_label))
        self.wait()

        self.play(
            plate_r.animate.set_color(BLUE),
            Transform(pos_sign, neg_sign.copy().move_to(plate_r.get_center())),
            Transform(plot, plot2),
            FadeOut(vector_field),
        )
        force_arrow.next_to(el, LEFT).flip().shift(DOWN * 0.1)
        force_label.next_to(force_arrow, DOWN)
        self.play(FadeIn(VGroup(force_arrow, force_label)))
        self.wait()

        self.play(el.animate(
            rate_func=rate_functions.ease_in_quad).move_to(el_origin))
        self.play(FadeOut(VGroup(force_arrow, force_label)))
        self.wait()
        self.play(Transform(title, Tex('$e^-$ can reach the plates with enough energy').to_corner(UL)))

        energy_eq = MathTex('E = K + V').to_edge()

        self.play(Create(plot_E))
        self.play(Write(energy_eq))
        self.wait()
        self.play(Transform(energy_eq, MathTex('K = E - V').to_edge()))
        self.wait()
        self.play(Transform(energy_eq, MathTex('K > V').to_edge()))
        self.play(Indicate(plot2))
        self.play(Indicate(plot_E, WHITE))



class Scene3D(ThreeDScene):
    def construct(self):
        ax = ThreeDAxes()

        self.add(ax)
        self.set_camera_orientation(phi=2*PI/5, theta=PI/5)
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait()
        self.stop_ambient_camera_rotation()
        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES)
        self.wait()
