from manim import *
from nice_animations.my_objects.model import Model

config.background_color = WHITE
config.pixel_height = 1080
config.pixel_width = 1920
config.frame_height = 8
config.frame_width = 14.2
def plot_sentences(input_text:str,color:ManimColor=BLACK)->list[Text]:
    list= input_text.split(" ")
    text=[Text(" ").move_to((0,0,0))]
    for idx,word in enumerate(list):
        text+=[Text(word,color=color,font_size=27).next_to(text[idx].get_right(),direction=RIGHT,buff=0.5)]
    return text
class MAE(Scene):
    def __init__(self, T: int = 30, min_T: int = 20, square_size: int = 1):
        super().__init__()
    def construct(self):
        sentence_1= "At the cafeteria Florian always eats french fries"
        sentence_3 = "At the cafeteria Florian always eats french vegetables"
        sentence_2= "At the [MASK] Florian always eats french [MASK]"
        label2=Text("X'",color=BLACK,font_size=25)
        label1=Text("X",color=BLACK,font_size=25)
        model=Model(label="Fondation Model",color=LIGHT_PINK,width=3,height=1)
        decoder=Model(label="Pre-training decoder",color=PURPLE_A,width=3,height=1)
        decoder.next_to(model,UP,buff=0.5)
        self.add(model)
        self.add(decoder)
        text_1=plot_sentences(sentence_1)
        text_2=plot_sentences(sentence_2)
        text_3=plot_sentences(sentence_3)
        s1_group=Group(*text_1)
        s1_group.next_to(model,DOWN,buff=2)
        action1=[Write(word) for word in text_1]
        s2_group=Group(*text_2)
        for idx,elem in enumerate(s2_group):
            elem.move_to(s1_group[idx].get_center()+np.array([0,1,0]))
        #action2 = [Write(word) for word in text_2]
        #s2_group.next_to(s1_group,direction=UP,buff=0.3)
        self.camera.frame_center =model.get_center()
        #self.add(s1_group)
        self.wait(0.1)
        self.add(label1.next_to(s1_group,LEFT))
        for act in action1:
            self.play(act,run_time=0.5)
        self.wait(0.2)
        self.add(label2.next_to(s2_group,LEFT))
        for word in s2_group:
            self.play(FadeIn(word),run_time=0.5)
        self.wait(0.1)
        arrow1=Arrow(model.get_bottom()+np.array([0,-1,0]),model.get_bottom(),color=BLACK,buff=0,tip_length=0.2)
        arrow2 = Arrow(model.get_top(), decoder.get_bottom(), color=BLACK, buff=0, tip_length=0.2)
        self.play(FadeIn(arrow1))
        self.play(FadeIn(arrow2))
        s3_group=Group()
        for idx,word in enumerate(text_3):
            word.move_to(decoder.get_top())
            s3_group.add(word)
            self.play(word.animate.move_to(s2_group[idx].get_center()+np.array([0,4,0])))
        self.wait(0.5)
        self.play(s3_group[3].animate.set_color(PURE_GREEN),s3_group[8].animate.set_color(PURE_RED))
        self.wait(1)
        #self.play(*action2)