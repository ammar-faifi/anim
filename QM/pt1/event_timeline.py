import numpy as np
from manim import *


class EventTimeline(Group):
    def __init__(
        self,
        events_dict,
        timeline_length=10,
        card_width=1.5,
        card_height=2,
        card_spacing=0.3,
        image_scale=0.8,
        timeline_color=WHITE,
        card_color=WHITE,
        card_stroke_width=2,
        label_font_size=24,
        year_font_size=20,
        **kwargs,
    ):
        """
        Create a timeline with event cards.

        Parameters:
        -----------
        events_dict : dict
            Dictionary where keys are years (int) and values are tuples of (label, image_path)
        timeline_length : float
            Length of the timeline line
        card_width : float
            Width of each event card
        card_height : float
            Height of each event card
        card_spacing : float
            Vertical spacing between timeline and cards
        image_scale : float
            Scale factor for images within cards
        timeline_color : Color
            Color of the timeline line
        card_color : Color
            Color of the card borders
        card_stroke_width : float
            Width of card border strokes
        label_font_size : int
            Font size for event labels
        year_font_size : int
            Font size for year markers
        """
        super().__init__(**kwargs)

        self.events_dict = events_dict
        self.timeline_length = timeline_length
        self.card_width = card_width
        self.card_height = card_height
        self.card_spacing = card_spacing
        self.image_scale = image_scale
        self.timeline_color = timeline_color
        self.card_color = card_color
        self.card_stroke_width = card_stroke_width
        self.label_font_size = label_font_size
        self.year_font_size = year_font_size

        self._create_timeline()

    def _create_timeline(self):
        """Create the timeline visualization."""
        if not self.events_dict:
            return

        # Sort events by year
        sorted_events = sorted(self.events_dict.items())
        years = [year for year, _ in sorted_events]

        # Create main timeline line
        timeline_line = Line(
            start=LEFT * self.timeline_length / 2,
            end=RIGHT * self.timeline_length / 2,
            color=self.timeline_color,
            stroke_width=3,
        )
        self.add(timeline_line)

        # Calculate positions for events along timeline
        if len(years) == 1:
            positions = [0]
        else:
            min_year, max_year = min(years), max(years)
            year_range = max_year - min_year
            if year_range == 0:
                positions = [0]
            else:
                positions = [
                    (year - min_year) / year_range * self.timeline_length
                    - self.timeline_length / 2
                    for year in years
                ]

        # Create event cards and markers
        for i, ((year, (label, image_path)), x_pos) in enumerate(
            zip(sorted_events, positions)
        ):
            # Alternate card positions above and below timeline
            card_y = (
                self.card_spacing + self.card_height / 2
                if i % 2 == 0
                else -(self.card_spacing + self.card_height / 2)
            )

            # Create event card
            event_card = self._create_event_card(label, image_path, x_pos, card_y)
            self.add(event_card)

            # Create timeline marker (small circle)
            marker = Dot(
                point=[x_pos, 0, 0],
                radius=0.08,
                color=self.timeline_color,
                fill_opacity=1,
            )
            self.add(marker)

            # Create year label below timeline
            year_label = Text(
                str(year), font_size=self.year_font_size, color=self.timeline_color
            ).move_to([x_pos, -0.4, 0])
            self.add(year_label)

            # Create connection line from marker to card
            connection_line = Line(
                start=[x_pos, 0, 0],
                end=[x_pos, card_y - (self.card_height / 2 * np.sign(card_y)), 0],
                color=self.timeline_color,
                stroke_width=1,
                stroke_opacity=0.7,
            )
            self.add(connection_line)

    def _create_event_card(self, label, image_path, x_pos, y_pos):
        """Create an individual event card."""
        card_group = Group()

        # Create card background
        card_bg = Rectangle(
            width=self.card_width,
            height=self.card_height,
            color=self.card_color,
            stroke_width=self.card_stroke_width,
            fill_opacity=0.1,
            fill_color=self.card_color,
        )

        # Create label text (positioned at top of card)
        label_text = Text(
            label, font_size=self.label_font_size, color=WHITE
        ).scale_to_fit_width(self.card_width * 0.8)

        # Try to load and add image
        try:
            image = ImageMobject(image_path)
            # Scale image to fit in card, leaving space for label
            available_height = self.card_height * 0.6  # 60% of card height for image
            image.scale_to_fit_height(available_height * self.image_scale)
            image.scale_to_fit_width(self.card_width * 0.8 * self.image_scale)

            # Position image in center-bottom of card
            image.move_to([0, -self.card_height * 0.1, 0])

        except Exception as e:
            # If image loading fails, create a placeholder
            print(f"Warning: Could not load image {image_path}: {e}")
            placeholder_rect = Rectangle(
                width=self.card_width * 0.6,
                height=self.card_height * 0.4,
                color=GRAY,
                fill_opacity=0.3,
            ).move_to([0, -self.card_height * 0.1, 0])

            # Add "No Image" text
            no_img_text = Text("No Image", font_size=12, color=GRAY)
            no_img_text.move_to(placeholder_rect.get_center())
            image = Group(placeholder_rect, no_img_text)

        # Position label at top of card
        label_text.move_to([0, self.card_height * 0.4, 0])

        # Combine all card elements
        card_group.add(card_bg, label_text, image)
        card_group.move_to([x_pos, y_pos, 0])

        return card_group


# Example usage and animation
class EventTimelineExample(Scene):
    def construct(self):
        # Example events dictionary
        events = {
            1969: ("Moon Landing", "./figures/Paul_Ehrenfest.jpg"),
            1989: ("Fall of Berlin Wall", "path/to/berlin_wall.jpg"),
            2001: ("Internet Boom", "path/to/internet.jpg"),
            2007: ("iPhone Launch", "path/to/iphone.jpg"),
            2020: ("COVID-19 Pandemic", "path/to/covid.jpg"),
        }

        # Create timeline
        timeline = EventTimeline(
            events, timeline_length=12, card_width=2, card_height=2.5, card_spacing=0.5
        )

        # Center the timeline
        timeline.move_to(ORIGIN)

        # Add title
        title = Text("Historical Events Timeline", font_size=36, color=YELLOW)
        title.to_edge(UP, buff=0.5)

        # Animate
        self.play(Write(title))
        self.wait(0.5)

        # Animate timeline creation
        self.play(FadeIn(timeline), run_time=3)
        self.wait(2)

        # Optional: Highlight each event (get the actual event cards)
        # The timeline structure: [timeline_line, card1, marker1, year1, connection1, card2, marker2, year2, connection2, ...]
        event_cards = []
        for i, submobject in enumerate(timeline.submobjects):
            # Event cards are typically at indices 1, 6, 11, etc. (every 5th element starting from 1)
            if (
                i % 5 == 1 and i > 0
            ):  # Cards appear every 5 elements starting from index 1
                event_cards.append(submobject)

        # Highlight each event card
        for card in event_cards:
            self.play(card.animate.scale(1.2), run_time=0.5)  # Scale up card
            self.play(card.animate.scale(1 / 1.2), run_time=0.5)  # Scale back

        self.wait(2)
