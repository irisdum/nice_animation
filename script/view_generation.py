from manim import *

config.background_color = WHITE
config.pixel_height = 1080
config.pixel_width = 1920
config.frame_height = 8
config.frame_width = 14.2

class ViewGeneration(Scene):
    def __init__(self, T: int = 30, min_T: int = 20, square_size: int = 1):
        super().__init__()
        self.T = T
        self.min_T = min_T
        self.square_size = 0.3
        self.split_size = 5
        self.colors = [PURE_RED, PURE_BLUE]

    def construct(self):
        input_sequence = Group()
        for t in range(self.T):
            square = Square(side_length=self.square_size, stroke_color=BLACK, stroke_width=3, color=GRAY_A,
                            fill_opacity=0.1)
            input_sequence.add(square)
            square.next_to(input_sequence[t - 1], direction=RIGHT,buff=0.05)
        label_input = Text("Multi-year SITS", font_size=19,color=BLACK)
        label_input.next_to(input_sequence, direction=LEFT)
        self.add(label_input)
        self.add(input_sequence)

        little_sequence = Group()
        for t in range(4, self.min_T + 4):
            square = Square(side_length=self.square_size, stroke_color=BLACK, stroke_width=3, color=GRAY_A,
                            fill_opacity=0.1)
            square.next_to(input_sequence[t], direction=DOWN, buff=0)
            little_sequence.add(square)
        label_little_sequence = Text("Input SITS", font_size=25,color=BLACK)
        label_little_sequence.next_to(little_sequence, direction=LEFT)
        self.camera.frame_center = little_sequence.get_center() + np.array([0, -2, 0])
        #self.add(label_little_sequence)
        group_little_sequence=Group()
        group_little_sequence.add(little_sequence,label_little_sequence)
        #self.add(little_sequence)
        double_arrow_T = DoubleArrow(little_sequence.get_left(), little_sequence.get_right(), color=BLACK, buff=0,
                                   tip_length=0.2)
        double_arrow_T.next_to(little_sequence,direction=UP)
        txt_arrow = MathTex("T", font_size=30, color=BLACK)
        txt_arrow.next_to(double_arrow_T, direction=UP, buff=0.1)
        #self.add(double_arrow_T)
        group_little_sequence.add(little_sequence, label_little_sequence,double_arrow_T,txt_arrow)
        self.add(group_little_sequence)
        self.play(group_little_sequence.animate.move_to(little_sequence.get_center()+np.array([0, -1, 0])))
        self.wait(1)
        group_viewa = []
        group_viewb = []
        for split_index in range(self.min_T // self.split_size):
            if split_index % 2 == 0:
                color = self.colors[0]
            else:
                color = self.colors[1]
            consecutive_group = Group()
            for i in range(self.split_size):
                square = little_sequence[split_index*self.split_size+i].copy()
                square.set_stroke(color=color)
                #square.next_to(little_sequence[split_index * self.split_size + i], direction=DOWN,buff=1)
                consecutive_group.add(square)
                self.add(consecutive_group)
            self.play(consecutive_group.animate.move_to(consecutive_group.get_center()+np.array([0,-1,0])))
            #self.play(FadeIn(consecutive_group))
            if split_index==0:
                double_arrow=DoubleArrow(consecutive_group.get_left(),consecutive_group.get_right(),color=BLACK,buff=0,tip_length=0.2)
                double_arrow.next_to(consecutive_group,direction=UP,buff=0.05)
                text_arrow=MathTex("t_w",font_size=35,color=BLACK)
                text_arrow.next_to(double_arrow,direction=UP,buff=0.05)
                self.add(double_arrow,text_arrow)
                consecutive_group.add(double_arrow)
                consecutive_group.add(text_arrow)
                self.play(FadeIn(double_arrow),FadeIn(text_arrow))
            if split_index % 2 == 0:
                group_viewa += [consecutive_group]
            else:
                group_viewb += [consecutive_group]
            self.wait(0.05)
        group_a=Group()
        for idx,subseries in enumerate(group_viewa):
            copy_a=subseries.copy()
            group_a.add(copy_a)
            self.play(copy_a.animate.move_to(little_sequence.get_center() + np.array([-5+((subseries.width+0.1)*idx), -4, 0])).align_to(little_sequence.get_center() + np.array([-5+((subseries.width+0.1)*idx), -4, 0]),DOWN), run_time=2)
        txt_viewa=Text("View A ",font_size=25,color=PURE_RED)
        txt_viewa.next_to(group_a,direction=UP,buff=0.3)

        group_b=Group()
        for idx,subseries in enumerate(group_viewb):
            copy_b=subseries.copy()
            group_b.add(copy_b)
            self.play(copy_b.animate.move_to(little_sequence.get_center() + np.array([1+((subseries.width+0.1)*idx), -4, 0])).align_to(little_sequence.get_center() + np.array([1+((subseries.width+0.1)*idx), -4, 0]),DOWN), run_time=2)
        self.add(txt_viewa)
        self.play(FadeIn(txt_viewa))
        txt_viewb=Text("View B ",font_size=25,color=PURE_BLUE)
        txt_viewb.next_to(group_b,direction=UP,buff=0.6)
        txt_viewb.align_to(txt_viewa,UP)
        self.add(txt_viewb)
        self.play(FadeIn(txt_viewb))
        self.wait(1)
