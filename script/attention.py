from manim import *
from nice_animations.my_objects.attention_utils import create_item

config.background_color = WHITE
config.pixel_height = 1080
config.pixel_width = 1920
config.frame_height = 20
config.frame_width = 31


class Attention(Scene):
    def __init__(self, T: int = 30, min_T: int = 20, square_size: int = 0.9,font_size:int=33):
        super().__init__()
        self.T = T
        self.min_T = min_T
        self.square_size = square_size
        self.split_size = 5
        self.colors = [PURE_RED, PURE_BLUE]
        self.font_size=65
    def construct(self):
        input= create_item("Input", "X", 4, 2, BLACK, square_size=self.square_size, font_size=self.font_size)
        query= create_item("Query", "Q=XW_Q", 4, 2, PURE_RED, square_size=self.square_size, font_size=self.font_size)
        key= create_item("Key", "K^{T}=W_K^{T}X^{T}", 2, 4, PURE_GREEN, square_size=self.square_size, font_size=self.font_size)
        value= create_item("Value", "V=XW_V", 4, 3, color=PINK, square_size=self.square_size, font_size=self.font_size)
        score= create_item("Attention score", "A=\sigma({QK^T}/ \sqrt{d_K})", 4, 4, square_size=self.square_size, font_size=self.font_size, color=BLACK)
        output= create_item("Output", "O=AV", 4, 3, color=GOLD_E, square_size=self.square_size, font_size=self.font_size)
        self.add(input)
        self.camera.frame_center = input.get_center()+np.array([12,0,0])
        self.wait(1)
        query.move_to(input.get_center()+np.array([5,6,0]))

        key.move_to(input.get_center()+np.array([5,0,0]))

        value.move_to(input.get_center()+np.array([5,-6,0]))
        arrow_query = Arrow(input.get_right(), query.get_left(), color=BLACK)
        arrow_key = Arrow(input.get_right(), key.get_left(), color=BLACK)
        arrow_value = Arrow(input.get_right(), value.get_left(), color=BLACK)
        self.play(FadeIn(arrow_query), FadeIn(arrow_key), FadeIn(arrow_value), run_time=0.5)
        self.add(query)
        self.add(key)
        self.add(value)
        self.play(FadeIn(query),FadeIn(key),FadeIn(value))
        self.wait(0.05)
        #self.play(FadeOut(arrow_query), FadeOut(arrow_key), FadeOut(arrow_value), run_time=0.5)
        self.wait(3)
        score.move_to(key.get_center() + np.array([10, 3, 0]))
        print(len(query[0]))
        self.add(score[1])
        self.add(score[2])
        arrow_query_score=Arrow(query.get_right(),score.get_left(),color=BLACK)
        arrow_key_score=Arrow(key.get_right(),score.get_left(),color=BLACK)
        self.play(FadeIn(arrow_query_score),FadeIn(arrow_key_score),run_time=0.1)
        for i in range(4):
            for j in range(4):
                l_query=[query[0][i*2+k] for k in range(2)]
                group_query=Group(*l_query)
                l_key=[key[0][k] for k in [j,4+j]]
                group_key=Group(*l_key)
                self.play(group_query.animate.set_color(LIGHTER_GRAY),group_key.animate.set_color(LIGHTER_GRAY),FadeIn(score[0][i*4+j]),run_time=0.3)
                self.play(group_query.animate.set_color(PURE_RED),group_key.animate.set_color(PURE_GREEN),run_time=0.1)
        #self.play(FadeOut(arrow_query_score), FadeOut(arrow_key_score), run_time=0.1)
        self.wait(3)
        output.move_to(score.get_center()+np.array([7,-5,0]))
        self.add(output[1])
        self.add(output[2])

        arrow_score_output=Arrow(score.get_right(),output.get_left(),color=BLACK)
        arrow_value_output=Arrow(value.get_right(),output.get_left(),color=BLACK)
        self.play(FadeIn(arrow_score_output),FadeIn(arrow_value_output))
        for i in range(4):
            for j in range(3):
                l_score=[score[0][i*4+k] for k in range(4)]
                l_value= [value[0][k] for k in [j,j+3,j+6,j+9]]
                group_score=Group(*l_score)
                group_value = Group(*l_value)
                self.play(group_score.animate.set_color(LIGHTER_GRAY), group_value.animate.set_color(LIGHTER_GRAY),
                          FadeIn(output[0][i*3+j]), run_time=0.3)
                self.play(group_score.animate.set_color(BLACK), group_value.animate.set_color(PINK),
                          run_time=0.1)
        self.wait(3)
