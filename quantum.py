from manim import *


class TISE(Scene):
    def fade_in_out(self, obj, delay=1):
        self.play(FadeIn(obj))
        self.wait(delay)
        self.play(FadeOut(obj))

    def construct(self):
        title = Title("Solving Time-Dependent Schrödinger Equation")

        self.play(Write(title))
        self.wait()

        steps = (
            VGroup(
                Text(
                    "1. Solve Shcödinger's PDE",
                ),
                Text(
                    "2. Using Hamiltonian operator",
                ),
                Text(
                    "3. Find the general solution",
                ),
                Text("4. Some intresting properties."),
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.5)
            .scale(0.7)
            .shift(0.2 * UP)
        )

        for obj in steps:
            self.play((Write(obj)))
            self.wait()

        self.play(FadeOut(steps))
        self.wait()

        tdse = MathTex(
            r"i\hbar",
            r"\frac{\partial\Psi}{\partial t}",
            r"= - \frac{\hbar^2}{2m}",
            r"\frac{\partial^2 \Psi}{\partial x^2}",
            r"+U\Psi",
        ).scale(1.5)
        func = (
            VGroup(
                MathTex(r"\Psi = \Psi(x, t)"),
                MathTex(r"U = U(x)"),
                MathTex(r"\Psi(x, t) = \psi(x) \phi(t)"),
                MathTex(
                    r"\frac{\partial\Psi}{\partial t} = \psi(x)\frac{d \phi(t)}{d t}"
                ),
                MathTex(
                    r"\frac{\partial^2 \Psi}{\partial x^2} = \phi(t) \frac{d^2 \psi(x)}{d x^2}"
                ),
            )
            .arrange(DOWN, aligned_edge=LEFT)
            .scale(0.7)
            .to_edge(LEFT)
            .shift(UP)
        )

        self.play(Write(tdse))
        self.play(Write(func[0]))
        self.play(tdse.animate.shift(1.8 * UP).scale(0.5))
        self.fade_in_out(Text("Separation of Variables").shift(2 * DOWN))
        self.play(Write(func[1]))
        self.play(Write(func[2]))

        self.play(Circumscribe(tdse[1]), Circumscribe(tdse[3]))
        self.wait()
        self.play(Write(func[3]))
        self.play(Write(func[4]))
