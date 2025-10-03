from manim import *
from manim_voiceover import VoiceoverScene

# from manim_voiceover.services.gtts import GTTSService
from manim_voiceover.services.recorder import RecorderService


class MyAwesomeScene(VoiceoverScene):
    def construct(self):
        # self.set_speech_service(GTTSService())
        self.set_speech_service(RecorderService())
        circle = Circle()
  
        with self.voiceover(text="This circle is drawn as I speak.") as tracker:
            self.play(Create(circle))
