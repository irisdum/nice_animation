from random import shuffle

from manim import *

def create_matrix(color:ManimColor, square_size=0.5,n_pix=4)->Group:
    color_shades = [color.interpolate(other=WHITE, alpha=1 / (i + 1)) for i in range(30)] * 30
    shuffle(color_shades)
    # print(color_shades)
    # Create the 3x3 grid of squares
    one_matrix=Group()
    for i in range(n_pix):
        for j in range(n_pix):
            square = Square(side_length=square_size, stroke_color=BLACK, stroke_width=1,
                            fill_color=color_shades[(n_pix * i + j)], fill_opacity=1)
            # Position each square
            square.move_to(square_size * (j - 1, 1 - i, 0))  # Offset for correct grid layout
            one_matrix.add(square)
    return one_matrix
class ColorfulMatrix(Mobject):
    def __init__(self, color:ManimColor, square_size=0.5,n_pix=4, **kwargs):
        super().__init__(**kwargs)
        num_shades=n_pix**2
        color_shades=[color.interpolate(other=WHITE,alpha=1/(i+1)) for i in range(30)]*30
        shuffle(color_shades)
        #print(color_shades)
        # Create the 3x3 grid of squares
        for i in range(n_pix):
            for j in range(n_pix):
                square = Square(side_length=square_size,stroke_color=BLACK,stroke_width=1,fill_color=color_shades[(n_pix*i+j)],fill_opacity=1)
                # Position each square
                square.move_to(square_size * (j - 1, 1 - i, 0))  # Offset for correct grid layout
                self.add(square)

class MSImage(Mobject):
    def __init__(self, colors: list[ManimColor], square_size, n_pix=4, n_im: int = 4,shift:float=0.3, **kwargs):
        super().__init__()
        assert len(colors)==n_im
        for k in range(n_im):
            matrix=ColorfulMatrix(color=colors[k],square_size=square_size,n_pix=n_pix)
            matrix.set_stroke(WHITE)
            matrix.move_to((shift*k,-shift*k,0))
            #matrix.move_to(square_size * (k - 1.5, 1.5 - k, 0))
            self.add(matrix)
def create_ms_images(colors: list[ManimColor], square_size, n_pix=4, n_im: int = 4,shift:float=0.3)->Group:
    ms_image=Group()
    assert len(colors) == n_im
    for k in range(n_im):
        matrix = create_matrix(color=colors[k], square_size=square_size, n_pix=n_pix)
        matrix.z_index=k
        matrix.set_stroke(WHITE)
        matrix.move_to((shift * k, -shift * k, 0))
        # matrix.move_to(square_size * (k - 1.5, 1.5 - k, 0))
        ms_image.add(matrix)
    return ms_image

class VisuSITS(Mobject):
    def __init__(self, colors: list[ManimColor], square_size, n_pix=4, n_im: int = 4, shift: float = 0.3,T:int=4):
        super().__init__()
        l_images=[]
        for i in range(T):
            ms_images=MSImage(colors=colors,square_size=square_size,n_pix=n_pix,n_im=n_im,shift=shift)
            l_images+=[ms_images]
            if i>0:
                ms_images.next_to(l_images[i-1])
            self.add(ms_images)
        self.all_images=ms_images
