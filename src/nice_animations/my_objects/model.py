from manim import *

class Model(Mobject):
    def __init__(self, label:str, color: ManimColor,width:int=6, height:int=2):
        super().__init__(color)
        rec=RoundedRectangle(width=width, height=height, color=BLACK, fill_color=color, fill_opacity=1,
                             stroke_width=1, stroke_opacity=0.8,corner_radius=0.1)
        label = Text(label, color=BLACK, font="sans-serif")
        label.scale_to_fit_width(0.9*rec.width)
        label.move_to(rec.get_center())
        self.add(rec,label)