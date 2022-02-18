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

        tdse = (
            MathTex(
                r"i\hbar",
                r"\frac{\partial\Psi}{\partial t}",
                r"= - \frac{\hbar^2}{2m}",
                r"\frac{\partial^2 \Psi}{\partial x^2}",
                r"+U\Psi",
            )
            .scale(1.5)
            .shift(RIGHT)
        )
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

        tise = (
            MathTex(
                r"i \hbar \psi\frac{d \phi}{d t}",
                "=",
                r"- \frac{\hbar^2}{2m} \frac{d^2 \psi}{d x^2} \phi +" r"U \psi \phi",
            )
            .scale(0.75)
            .next_to(tdse, DOWN, buff=1)
        )
        tise_1 = (
            MathTex(
                r"i \hbar \frac{1}{\phi} \frac{d \phi}{d t}",
                "=",
                r"- \frac{\hbar^2}{2m} \frac{1}{\psi} \frac{d^2 \psi}{d x^2} +" r"U",
            )
            .scale(0.75)
            .next_to(tdse, DOWN, buff=1)
        )
        self.play(Write(tise))
        self.wait()
        self.play(Transform(tise, tise_1))
        self.wait()

        frame_t = SurroundingRectangle(tise_1[0])
        frame_x = SurroundingRectangle(tise_1[2])
        equal_E = MathTex("=E").scale(0.75).next_to(tise_1)
        self.play(Create(frame_t))
        self.play(ReplacementTransform(frame_t, frame_x))
        self.wait()
        self.play(FadeOut(frame_x))
        self.wait()
        self.play(Create(equal_E))
        self.wait()

        separation = MathTex(r"\Psi(x, t) = \phi(t) \psi(x)").to_edge(UP, 2)
        time_dep = (
            VGroup(
                # 0
                MathTex(
                    r"i \hbar \frac{1}{\phi} \frac{d \phi}{d t} = E",
                ),
                # 1
                MathTex(
                    r" \frac{1}{\phi} \frac{d \phi}{d t} = \frac{E}{i \hbar }",
                ),
                # 2
                MathTex(
                    r"\frac{d \phi}{\phi} = \frac{E}{i \hbar }\, dt",
                ),
                # 3
                MathTex(
                    r"\int \frac{d \phi}{\phi} = \int \frac{E}{i \hbar }\, dt",
                ),
                # 4
                MathTex(
                    r"{\ln(\phi)} = \frac{E}{i \hbar }t + C",
                ),
                # 5
                MathTex(
                    r"e^{\ln(\phi)} = e^{\frac{E}{i \hbar }t + C}",
                ),
                # 6
                MathTex(
                    r"\phi = e^{\frac{E}{i \hbar }t} \times {{e^C}}",
                ),
            )
            .arrange(DOWN)
            .to_edge(LEFT, buff=1)
            .shift(1.5 * DOWN)
        )
        time_dep_sol = (
            MathTex(r"\phi(t) = e^{\frac{E}{i \hbar }t}").scale(2).to_edge(LEFT, 1)
        )

        time_ind = VGroup(
            MathTex(
                r"- \frac{\hbar^2}{2m} \frac{1}{\psi} \frac{d^2 \psi}{d x^2} + U = E",
            ),
            MathTex(
                r"- \frac{\hbar^2}{2m} \frac{d^2 \psi}{d x^2} + U\psi = E \psi",
            ),
        ).to_edge(RIGHT, buff=1)

        self.play(*[FadeOut(obj) for obj in [tdse, func, equal_E]])
        self.play(
            ReplacementTransform(tise.copy(), time_dep[0]),
            ReplacementTransform(tise, time_ind[0]),
        )
        self.wait()
        self.play(Transform(time_ind[0], time_ind[1]))
        self.play(Transform(time_dep[0], time_dep[1]))
        self.fade_in_out(Text("Separable DE", 2).to_edge(UP, 1.5))

        self.play(Transform(time_dep[1], time_dep[2]))
        self.play(Transform(time_dep[2], time_dep[3]))
        self.play(
            LaggedStart(*[FadeOut(obj) for obj in time_dep[:4]]),
        )
        time_dep.shift(3 * UP)
        self.play(Write(time_dep[4]))
        self.play(ReplacementTransform(time_dep[4], time_dep[5]))
        self.play(ReplacementTransform(time_dep[5], time_dep[6]))
        self.play(Circumscribe(time_dep[6][-1]))
        self.fade_in_out(separation)
        self.play(ReplacementTransform(time_dep[6].copy(), time_dep_sol))
        self.play(
            LaggedStart(FadeOut(time_dep[5]), FadeOut(time_dep[6])),
        )
