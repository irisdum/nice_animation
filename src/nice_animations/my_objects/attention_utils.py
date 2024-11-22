from manim import ManimColor, Group, Text, MathTex, UP
from nice_animations.my_objects.matrices import create_vector


def create_item(label:str,eq:str,row: int, col: int, color: ManimColor, square_size=0.5,font_size=40):
    item=Group()
    vector= create_vector(row=row, col=col, color=color, square_size=square_size)
    label=Text(label,font_size=font_size,color=color)
    mat_thex=MathTex(eq,font_size=font_size,color=color)
    mat_thex.next_to(vector,direction=UP,buff=0.1)
    label.next_to(mat_thex,direction=UP,buff=0.1)
    item.add(vector,label,mat_thex)
    return item