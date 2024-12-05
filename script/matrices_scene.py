from manim import *
from nice_animations.my_objects.matrices import MSImage, VisuSITS, create_ms_images, create_matrix
from nice_animations.my_objects.model import Model

config.background_color = WHITE
config.pixel_height = 1080
config.pixel_width = 1920
config.frame_height = 8
config.frame_width = 14.2


class ColorMatrixScene(Scene):
    def __init__(self, T: int = 5):
        super().__init__()
        self.T = T
        self.ms_colors = [GREY_E, PURE_BLUE, PURE_GREEN, PURE_RED]
        self.n_pix = 4


    def construct(self):
        # Define a 3x3 color matrix
        T = 5
        sits_group = Group()
        l_images = []
        for i in range(T):
            ms_images = create_ms_images(colors=self.ms_colors, square_size=1, n_pix=self.n_pix,
                                         n_im=len(self.ms_colors), shift=0.3)
            l_images += [ms_images]
            if i > 0:
                ms_images.next_to(l_images[i - 1], buff=0.55)
            sits_group.add(ms_images)
        sits_group = sits_group.scale_to_fit_width(0.4 * config.frame_width)
        input_text=Text("Input SITS",color=BLACK,font="sans-serif",font_size=19)
        input_text.next_to(sits_group,direction=LEFT)

        self.add(input_text)
        ms_width = sits_group[1].width
        # sits=sits.scale(0.1)
        self.add(sits_group)
        sste = Model(label="Spectro Spatial Encoder", color=GRAY_A, width=int(0.8 * sits_group.width), height=1)
        sste.next_to(sits_group, direction=UP, buff=0.3)
        print(type(sste.width))
        background = RoundedRectangle(width=sste.width*1.7, height=3.8*sste.height, color=DARK_BLUE, fill_color=BLUE_A, fill_opacity=0.3,
                             stroke_width=4, stroke_opacity=0.8,corner_radius=0.1)
        label_background=Text("SSTE",font_size=30,color=BLACK,font="sans-serif")
        #label_background.next_to(background,RIGHT,buff=0.1)
        #self.add(label_background)
        background.next_to(sits_group.get_top(),UP,buff=0.11)
        #print( sste.get_top() )
        self.camera.frame_center = sste.get_top() + np.array([0,0.5,0])
        # self.play(FadeIn(sits))
        # self.camera.frame_center=sits.get_center()
        #self.wait(0.3)
        self.add(background)
        self.add(sste)
        self.play(FadeIn(sste))
        #self.wait(0.1)
        l_encoded_path = []
        l_latent_repr=Group()
        for idx in range(T):
            #arrow = Arrow(start=sits_group[idx].get_top(), end=sste.get_bottom(), color=BLACK, buff=0.3, tip_length=0.1)
            #self.add(arrow)
            self.play(sits_group[idx].animate.scale(1.05))
            self.wait(0.01)
            encoded_patch = create_ms_images(colors=[PURPLE_E, PURPLE_A], square_size=1, n_pix=self.n_pix, n_im=2,
                                             shift=0.3)
            encoded_patch.scale_to_fit_width(ms_width/1.05)
            encoded_patch.next_to(sits_group[idx], direction=UP, buff=1.5)
            l_encoded_path += [encoded_patch]
            #arrow_encoder = Arrow(start=sste.get_top(), end=encoded_patch.get_bottom(), buff=0.2, tip_length=0.1,
           #                       color=BLACK)
            latent_repr = create_ms_images(colors=[LIGHT_PINK, PINK], square_size=1, n_pix=self.n_pix, n_im=2,
                                           shift=0.3)
            latent_repr.scale_to_fit_width(ms_width/1.05)
            latent_repr.next_to(encoded_patch,direction=UP,buff=1.5)
            l_latent_repr.add(latent_repr)
            #self.add(arrow_encoder)
            self.add(encoded_patch)
            self.play(FadeIn(encoded_patch), sits_group[idx].animate.scale(1 / 1.05))
            self.wait(0.01)
        intermediate_embedding = Group(*l_encoded_path)
        transformer = Model(label="Temporal Transformer" , color=GRAY_A, width=sste.width, height=1)
        transformer.next_to(intermediate_embedding, direction=UP, buff=0.2)
        self.add(transformer)
        self.play(FadeIn(transformer))
        self.wait(0.05)
        for id_pix in range(self.n_pix**2):
            actions=[]
            out_actions=[]
            for t in range(T):
                for c in range(2):
                    pixel = intermediate_embedding[t][c][id_pix]
                    red_border = Rectangle(width=pixel.width + 0.001, height=pixel.height + 0.001, fill_opacity=0,
                                           stroke_opacity=1, stroke_color=PURE_RED, stroke_width=2)
                    red_border.move_to(pixel.get_center())
                    red_border.z_index=c
                    actions+=[FadeIn(red_border)]
                    out_actions+=[FadeOut(red_border)]

            self.play(*actions,run_time=0.2)
            self.wait(0.005)
            #self.wait(0.01)
            display_lat_repr_pix=[]
            for t in range(T):
                for feat in range(2):
                    l_latent_repr[t][feat][id_pix].z_index=feat
                    self.add(l_latent_repr[t][feat][id_pix])
                    display_lat_repr_pix+=[FadeIn(l_latent_repr[t][feat][id_pix])]
            self.play(*display_lat_repr_pix,run_time=0.2)
            self.wait(0.005)
            self.play(*out_actions,run_time=0.2)
            self.wait(0.005)
        self.wait(0.05)

