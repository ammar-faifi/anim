from manim import *


class TISE(Scene):
    def construct(self):
        title = Title('Start Solving Time-Dependent Schrödinger Equation')

        self.play(Write(title))
        self.wait()

        steps = VGroup(
            Text("1. Solve Shcödinger's PDE",),
            Text("2. Using Hamiltonian Operator",),
            Text("3. Find the general solution",),
            Text("4. Talk about some intresting properties."),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).scale(0.7).shift(0.2*UP)

        for obj in steps:
            self.play((Write(obj)))
            self.wait()

        self.play(FadeOut(steps))
        self.wait()

        tdse = MathTex(
            r'i\hbar \frac{\partial \Psi}{\partial t} = - \frac{\hbar^2}{2m} \frac{\partial^2 \Psi}{\partial x^2}+U\Psi'
        ).scale(1.5)
        func = VGroup(
            MathTex(r'\Psi = \Psi(x, t)'),
            MathTex(r'U = U(x)'),
            MathTex(r'\Psi(x, t) = \psi(x) \phi(t)'),
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT).shift(UP).scale(0.5)

        text_sep = Text('Separation of Variables').shift(2*DOWN)
        self.play(Write(tdse))
        self.play(Write(func[0]))
        self.play(tdse.animate.shift(1.5*UP).scale(0.25))
        self.play(FadeIn(text_sep))
        self.wait()
        self.play(FadeOut(text_sep))
        self.play(Write(func[1]))
        self.play(Write(func[2]))


