from manim import *

config.background_color = WHITE
config.pixel_height = 1080
config.pixel_width = 1920
config.frame_height = 6
config.frame_width = 80

def periodic_fun(x):
    return 2*(np.sin(x / 3) + np.cos(x / 3))


def periodic_fun1(x):
    return 2*(np.sin(x / 5) + np.cos(x / 5))

class IrregularPlot(Scene):
    def __init__(self):
        super().__init__()
        self.T=40
    def construct(self):
        axes = NumberPlane(x_range=[0,self.T+0.1],y_range=[-4.5,4.5], background_line_style={"stroke_color": BLACK,
                        "stroke_width": 4,
                        "stroke_opacity": 0.6},x_length=20,
                           color=BLACK,tips=True)

        x_label=axes.get_x_axis_label("T")
        axes.add_coordinates()  # Add number labels to axes
        x1=np.arange(0,self.T)
        x2=np.random.choice(np.arange(0,self.T,0.3),40)
        print(len(x1))
        # Create dots for each data point
        data_points = [(x,periodic_fun(x)) for x in x1]
        data_points2 = [(x, periodic_fun(x)) for x in x2]
        # Label the axes

        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("T")
        dots = VGroup(*[
            Dot(axes.c2p(x, y), color=DARK_BLUE,radius=0.07) for x, y in data_points
        ])
        dots2 = VGroup(*[
            Dot(axes.c2p(x, y), color=DARK_BLUE, radius=0.07) for x, y in data_points2
        ])
        text1 = Text("Regular time series", color=BLACK, font_size=60).next_to(axes.get_top(),UP,buff=0.3)
        text2 = Text("Irregular time series", color=BLACK, font_size=60).next_to(axes.get_top(), UP, buff=0.3)
        plots=Group(axes,dots,dots2,text1,text2)
        plots.scale_to_fit_width(0.85*config.frame_width)
        #plots.scale_to_fit_height(0.9 * config.frame_height)
        self.camera.frame_center = dots.get_center()
        # Add the axes, labels, and dots to the scene
        self.add(axes,x_label,y_label)
        #self.play(FadeIn(dots),FadeIn(text1))
        self.add(dots,text1)
        self.wait(1)
        self.remove(dots,text1)
        self.add(dots2,text2)
        #self.play(FadeOut(dots),FadeOut(text1),FadeIn(dots2),FadeIn(text2))
        self.wait(1)
        #self.play(FadeOut(dots2),FadeOut(text2))

class UnalignedPlot(Scene):
    def __init__(self):
        super().__init__()
        self.T = 40
    def scatter_plot(self,data_points:list,axes,color:ManimColor):
        return VGroup(*[
                Dot(axes.c2p(x, y), color=color, radius=0.07) for x, y in data_points
            ])
    def construct(self):
        axes = NumberPlane(x_range=[0, self.T + 0.1], y_range=[-4.5,4.5],
                               background_line_style={"stroke_color": BLACK,
                                                      "stroke_width": 4,
                                                      "stroke_opacity": 0.6}, x_length=20,
                               color=BLACK, tips=True)
        x_label = axes.get_x_axis_label("T")
        axes.add_coordinates()  # Add number labels to axes
        x1 = np.arange(0, self.T)
        xbis=np.arange(0, self.T,1.5)
        x2 = np.random.choice(np.arange(0, self.T, 0.3), 40)
        x3 = np.random.choice(np.arange(0, self.T, 0.5), 40)
        print(len(x1))
        # Create dots for each data point
        data_points = [(x, periodic_fun(x)) for x in x1]
        data_points2 = [(x, periodic_fun1(x)) for x in x1]
        data_points3 = [(x, periodic_fun1(x)) for x in xbis]
        data_points4 = [(x, periodic_fun1(x)) for x in x2]
        data_points5 = [(x, periodic_fun(x)) for x in x3]
        # Label the axes

        # x_label = axes.get_x_axis_label("x")
        # y_label = axes.get_y_axis_label("T")
        dots=self.scatter_plot(data_points,axes,color=DARK_BLUE)
        dots2=self.scatter_plot(data_points2,axes,color=RED)
        dots3=self.scatter_plot(data_points3,axes,color=RED)
        dots4=self.scatter_plot(data_points4,axes,color=RED)
        dots5=self.scatter_plot(data_points5,axes,color=DARK_BLUE)
        text1 = Text("Aligned regular time series", color=BLACK, font_size=60).next_to(axes.get_top(), UP, buff=0.3)
        text2 = Text("Unaligned regular time series", color=BLACK, font_size=60).next_to(axes.get_top(), UP, buff=0.3)
        text3 = Text("Unaligned irregular time series", color=BLACK, font_size=60).next_to(axes.get_top(), UP, buff=0.3)
        plots = Group(axes, dots, dots2, text1, text2,dots3,dots4,text3,dots5)
        plots.scale_to_fit_width(0.9 * config.frame_width)
        self.camera.frame_center = dots.get_center()
        # Add the axes, labels, and dots to the scene
        self.add(axes, x_label)
        self.add(dots,dots2,text1)
        #self.play(FadeIn(dots),FadeIn(dots2), FadeIn(text1))
        self.wait(1)
        self.remove(dots2,text1)
        self.add(dots3,text2)
        self.wait(1)
        self.remove(dots,dots2,text2)
        self.add(dots5,dots4,text3)
        self.wait(1)
        # self.play(FadeOut(dots2), FadeOut(text1), FadeIn(dots3), FadeIn(text2))
        # self.wait(3)
        # self.play(FadeOut(dots),FadeIn(dots5), FadeOut(text2), FadeIn(dots4), FadeIn(text3))
        # self.wait(3)
        # self.play(FadeOut(dots4),FadeOut(dots5), FadeOut(text3))