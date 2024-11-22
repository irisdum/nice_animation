from manim import *
from nice_animations.my_objects.attention_utils import create_item
from nice_animations.my_objects.matrices import create_vector

config.background_color = WHITE
config.pixel_height = 1080
config.pixel_width = 1920


def construct_one_sample(idx: int | str = 1, font_size=30, key_feat: int = 2, val_feat: int = 3, square_size: float = 1,
                         stroke_width=5, width_sample: float = 10) -> Group:
    sample_group = Group()
    text_beg = Text("(", font_size=font_size + 20, color=BLACK)
    key = create_vector(row=1, col=key_feat, color=PURE_GREEN, square_size=square_size, stroke_width=stroke_width)
    key_text = MathTex(f"k_{idx}", font_size=font_size, color=PURE_GREEN)
    key_text.next_to(key, UP, buff=0.1)
    key_group = Group(key, key_text)
    value = create_vector(row=1, col=val_feat, color=PINK, square_size=square_size, stroke_width=stroke_width)
    value_text = MathTex(f"v_{idx}", font_size=font_size, color=PINK)
    value_text.next_to(value, UP, buff=0.1)
    value_group = Group(value, value_text)
    virgule = Text(',', font_size=font_size + 20, color=BLACK)
    text_end = Text(")", font_size=font_size + 20, color=BLACK)
    sample_group.add(text_beg, key_group, virgule, value_group, text_end)
    sample_group.arrange(RIGHT, buff=.8)
    return sample_group


def define_query(font_size: float, square_size: float):
    query = create_vector(row=1, col=2, color=PURE_RED, square_size=square_size, stroke_width=5)
    query_text = MathTex(f"q", font_size=font_size, color=PURE_RED)
    query_text.next_to(query, UP, buff=0.1)
    return Group(query, query_text)



class BroadDef(Scene):
    def __init__(self, T: int = 30, square_size: int = 1, font_size: int = 150):
        super().__init__()
        self.font_size = font_size
        self.square_size = square_size
        self.T = T

    def construct(self):
        l_input = Group()
        beg = Text("{", font_size=self.font_size + 60, color=BLACK)
        end = Text("}", font_size=self.font_size + 60, color=BLACK)
        l_keys = []
        l_values = []
        for i in range(1, 5):
            sample = construct_one_sample(i, font_size=self.font_size, square_size=self.square_size)
            l_keys += [sample[1][0]]
            l_values += [sample[3][0]]
            l_input.add(sample)
            virgule = Text(",", font_size=self.font_size + 40, color=BLACK)
            l_input.add(virgule)
        l_input.arrange(RIGHT, buff=0.5)
        # virgule2 = Text(",", font_size=self.font_size + 40, color=BLACK)
        # n_sample.next_to(l_input.get_right()+np.array([5,0,0]))
        input_seq = Group(beg, l_input, end)
        input_seq.arrange(RIGHT, buff=2)
        query_group = define_query(font_size=self.font_size, square_size=self.square_size)
        query_group.next_to(input_seq.get_left() + np.array([-3, -3, 0]))
        group_arrow = Group()
        weighted_values = Group()
        group_plus = Group()
        temp_weight = Group()
        for idx, s in enumerate(l_values):
            arrow = Arrow(s.get_bottom(), s.get_bottom() + np.array([0, -4, 0]), color=BLACK)
            text_arrow = MathTex(f"a_{idx + 1}", font_size=self.font_size, color=BLACK)
            text_arrow.next_to(arrow.get_center(), LEFT, buff=0.2)
            group_arrow.add(arrow)
            group_arrow.add(text_arrow)
            temp_query_group = define_query(font_size=self.font_size, square_size=self.square_size)
            temp_query_group.next_to(text_arrow, direction=LEFT, buff=4)
            temp_weight.add(temp_query_group)
            temp_query_arrow = Arrow(temp_query_group.get_right(), text_arrow.get_left(), color=BLACK)
            temp_key_arrow = Arrow(l_keys[idx].get_right(), text_arrow.get_left(), color=BLACK)
            temp_weight.add(temp_query_arrow, temp_key_arrow)
            w_value = create_vector(row=1, col=2, color=PINK, square_size=self.square_size, stroke_width=5)
            w_value_text = MathTex(f"a_{idx + 1} v_{idx + 1}", font_size=self.font_size, color=PINK)
            w_value_text.next_to(w_value, UP, buff=0.1)
            weighted_value = Group(w_value, w_value_text)
            weighted_value.next_to(arrow.get_bottom(), DOWN, buff=0.5)
            if idx > 0:
                plus = MathTex("+", color=BLACK, font_size=self.font_size + 20)
                plus.next_to(weighted_value, LEFT, buff=2.5)
                group_plus.add(plus)
            weighted_values.add(weighted_value)
        output = create_vector(row=1, col=2, color=LIGHT_BROWN, square_size=self.square_size, stroke_width=5)
        output_text = MathTex("o", font_size=self.font_size, color=LIGHT_BROWN)
        output_text.next_to(output, UP, buff=0.1)
        output_group = Group(output, output_text)
        output_group.next_to(weighted_values, LEFT, buff=6)
        equal_text = MathTex("=", font_size=self.font_size + 20, color=BLACK)
        equal_text.next_to(output, RIGHT, buff=2)
        global_group = Group(input_seq, query_group, group_arrow, weighted_values, output_group, group_plus, equal_text,
                             temp_weight)
        global_group.scale_to_fit_width(0.9 * config.frame_width)
        self.camera.frame_center = global_group.get_center()
        self.add(input_seq)
        self.wait(1)
        self.add(query_group)
        self.wait(1)
        self.add(group_arrow)
        self.add(weighted_values)
        self.add(output_group)
        self.add(group_plus, equal_text)
        self.wait(1)
        self.remove(query_group)
        self.add(temp_weight)
        self.wait(1)


class VaswaniAttention(Scene):
    def __init__(self, T: int = 30, square_size: int = 2, font_size: int = 70):
        super().__init__()
        self.font_size = font_size
        self.square_size = square_size
        self.T = T

    def update_scores(self, score, plot_scores):
        self.add(score[1], score[2])
        self.wait(1)
        for i in range(3):
            hightlight_score = Group(*[score[0][i * 4 + j] for j in range(4)])
            removed_score = Group(*[plot_scores[i * 4 + j] for j in range(4)])
            new_labels = Group(*[MathTex(r"a_{" + f"{i},{j}" + r"}", font_size=20, color=BLACK) for j in range(4)])
            for idx, elem in enumerate(new_labels):
                elem.move_to(removed_score[idx].get_center())
            new_labels.move_to(hightlight_score.get_center())
            # plot_norm_score=Group(*[normalized_score[0][i * 4 + j] for j in range(4)])
            self.play(hightlight_score.animate.set_color(GRAY_A), FadeOut(removed_score), FadeIn(new_labels))
            self.wait(0.2)
            self.play(hightlight_score.animate.set_color(BLACK))
        self.wait(1)

    def construct(self):
        input1 = create_item("Sequence A ", "X_A", 3, 2, BLACK, square_size=self.square_size, font_size=self.font_size)
        input2 = create_item("Sequence B ", "X_B", 4, 2, BLACK, square_size=self.square_size, font_size=self.font_size)
        input2.next_to(input1.get_bottom(), DOWN, buff=3 * self.square_size)
        axis1 = MathTex("l_A", font_size=self.font_size + 10, color=BLACK)
        arrow_axis1 = DoubleArrow(input1[0].get_top(), input1[0].get_bottom(), color=BLACK)
        arrow_axis1.next_to(input1[0].get_center(), LEFT, buff=2 * self.square_size)
        axis1.next_to(arrow_axis1, LEFT, buff=0.1 * self.square_size)
        labeled_input1 = Group(input1, axis1, arrow_axis1)
        axis2 = MathTex("l_B", font_size=self.font_size + 10, color=BLACK)
        arrow_axis2 = DoubleArrow(input2[0].get_top(), input2[0].get_bottom(), color=BLACK)
        arrow_axis2.next_to(input2[0].get_center(), LEFT, buff=2 * self.square_size)
        axis2.next_to(arrow_axis2, LEFT, buff=0.1 * self.square_size)
        labeled_input2 = Group(input2, axis2, arrow_axis2)
        query = create_item("Query", "Q=X_A W_Q", 3, 2, PURE_RED, square_size=self.square_size,
                            font_size=self.font_size)
        key = create_item("Key", "K^{T}=W_K^{T}X_B{T}", 2, 4, PURE_GREEN, square_size=self.square_size,
                          font_size=self.font_size)
        value = create_item("Value", "V=X_B W_V", 4, 3, color=PINK, square_size=self.square_size,
                            font_size=self.font_size)
        score = create_item("Attention score", "A=\sigma({QK^T}/{d_K})", 3, 4, square_size=self.square_size,
                            font_size=self.font_size, color=BLACK)

        output = create_item("Output", "O=AV", 4, 3, color=GOLD_E, square_size=self.square_size,
                             font_size=self.font_size)

        query.move_to(input1.get_center() + np.array([self.square_size * 5, 0, 0]))
        key.move_to(input2.get_center() + np.array([self.square_size * 5, self.square_size * 3, 0]))
        score.next_to(key, RIGHT, buff=2 * self.square_size)
        label_score_y = MathTex("l_A", font_size=self.font_size + 10, color=BLACK)
        arrow_y = DoubleArrow(score[0].get_bottom(), score[0].get_top(), color=BLACK)
        arrow_y.next_to(score[0].get_left(), LEFT, buff=0.1 * self.square_size)
        label_score_y.next_to(arrow_y.get_left(), LEFT, buff=0.1 * self.square_size)
        label_score_x = MathTex("l_B", font_size=self.font_size + 10, color=BLACK)
        arrow_x = DoubleArrow(score[0].get_left(), score[0].get_right(), color=BLACK)
        arrow_x.next_to(score[0].get_bottom(), DOWN, buff=0.05 * self.square_size)
        label_score_x.next_to(arrow_x.get_bottom(), DOWN, buff=0.05 * self.square_size)
        group_label_score = Group(label_score_x, arrow_x, label_score_y, arrow_y)
        value.move_to(input2.get_center() + np.array([self.square_size * 7, self.square_size * -2, 0]))
        arrow_query = Arrow(input1.get_right(), query.get_left(), color=BLACK)
        arrow_key = Arrow(input2.get_right(), key.get_left(), color=BLACK)
        arrow_value = Arrow(input2.get_right(), value.get_left(), color=BLACK)
        output.next_to(value.get_center() + np.array([5 * self.square_size, -1 * self.square_size, 0]))
        dk_labels = MathTex(r"d_{K}", font_size=self.font_size + 10, color=BLACK)
        arrow_dk = DoubleArrow(query[0].get_bottom(), query[0].get_top(), color=BLACK)
        arrow_dk.next_to(query[0], DOWN, buff=0.1 * self.square_size)
        dk_labels.next_to(arrow_dk, DOWN, buff=0.1 * self.square_size)
        global_group = Group(labeled_input1, labeled_input2, query, key, value, score, output, arrow_value, arrow_key,
                             arrow_query, group_label_score)
        global_group.scale_to_fit_height(0.9 * config.frame_height)
        # global_group.scale_to_fit_width(0.9*config.frame_width)
        self.camera.frame_center = global_group.get_center()
        self.add(labeled_input1, labeled_input2, query, key, value, arrow_query, arrow_value, arrow_key)
        self.wait(1)
        plot_scores = Group()
        for i in range(3):
            if i == 0:
                wait_time = 0.5
            else:
                wait_time = 0.01
            l_query = [query[0][i * 2 + k] for k in range(2)]
            group_query = Group(*l_query)
            one_query = MathTex(r"\mathbf{q}" + f"_{i}", color=BLACK, font_size=30)
            one_query.next_to(group_query.get_right(), RIGHT, buff=0.2 * self.square_size)
            self.add(one_query)
            self.play(group_query.animate.set_color(BLACK), run_time=0.1)
            for j in range(4):
                l_key = [key[0][k] for k in [j, 4 + j]]
                group_key = Group(*l_key)
                one_key = MathTex(r"\mathbf{k}" + f"_{j}", color=BLACK, font_size=30)
                one_key.next_to(group_key.get_bottom(), DOWN, buff=0.1 * self.square_size)
                plot_score = MathTex(r"\frac{\mathbf{q}" + f"_{i}" + r"\mathbf{k}^T" + f"_{j}" + r"}{d_K}", color=BLACK,
                                     font_size=self.square_size * 8)
                plot_score.move_to(score[0][i * 4 + j].get_center())
                plot_scores.add(plot_score)
                self.add(one_key)
                self.play(group_key.animate.set_color(BLACK), FadeIn(score[0][i * 4 + j]), FadeIn(plot_score),
                          run_time=wait_time)
                self.play(group_key.animate.set_color(PURE_GREEN), run_time=wait_time)
                self.remove(one_key)
                self.wait(wait_time)
            self.play(group_query.animate.set_color(PURE_RED))
            self.remove(one_query)
        self.wait(1)
        self.add(group_label_score)
        # self.add(text_norm_score,arrow_normalized_score,arrow_norm_label,math_norm)
        self.wait(0.1)
        self.update_scores(score, plot_scores)

        group_scores = Group(score, label_score_x, label_score_y)
        arrow_score_output = Arrow(group_scores.get_bottom(), output.get_top(), color=BLACK)
        arrow_value_output = Arrow(value.get_right(), output.get_left(), color=BLACK)
        self.add(output[1], output[2])
        self.play(FadeIn(arrow_score_output), FadeIn(arrow_value_output))
        for i in range(3):
            l_score = [score[0][i * 4 + k] for k in range(4)]
            group_score = Group(*l_score)
            self.play(group_score.animate.set_color(LIGHTER_GRAY))
            for j in range(3):
                l_value = [value[0][k] for k in [j, j + 3, j + 6, j + 9]]

                group_value = Group(*l_value)
                self.play(group_value.animate.set_color(LIGHTER_GRAY),
                          FadeIn(output[0][i * 3 + j]), run_time=0.3)
                self.play(group_value.animate.set_color(PINK),
                          run_time=0.1)
            self.play(group_score.animate.set_color(BLACK))
        self.wait(1)


class CAFlexibleRec(Scene):
    def __init__(self, square_size: int = 2, font_size: int = 70):
        super().__init__()
        self.square_size = square_size
        self.font_size = font_size
    def construct(self):
        label_tok=MathTex(r"M_{\beta}",font_size=self.font_size,color=BLACK)

        token=create_vector(1,2,color=PURE_RED,square_size=self.square_size)
        l_tok = Group(*[token.copy(), token.copy()])
        print(token)
        label_tok.next_to(token,LEFT,buff=0.1*self.square_size)
        input1 = create_item("Sequence A ", "X_A", 3, 2, BLACK, square_size=self.square_size, font_size=self.font_size)
        input2 = create_item("Sequence B ", "X_B", 4, 2, BLACK, square_size=self.square_size, font_size=self.font_size)
        input2.next_to(input1.get_bottom(), DOWN, buff=3 * self.square_size)
        axis1 = MathTex("l_A", font_size=self.font_size + 10, color=BLACK)
        arrow_axis1 = DoubleArrow(input1[0].get_top(), input1[0].get_bottom(), color=BLACK)
        arrow_axis1.next_to(input1[0].get_center(), LEFT, buff=2 * self.square_size)
        axis1.next_to(arrow_axis1, LEFT, buff=0.1 * self.square_size)
        labeled_input1 = Group(input1, axis1, arrow_axis1)
        axis2 = MathTex("l_B", font_size=self.font_size + 10, color=BLACK)
        arrow_axis2 = DoubleArrow(input2[0].get_top(), input2[0].get_bottom(), color=BLACK)
        arrow_axis2.next_to(input2[0].get_center(), LEFT, buff=2 * self.square_size)
        axis2.next_to(arrow_axis2, LEFT, buff=0.1 * self.square_size)
        labeled_input2 = Group(input2, axis2, arrow_axis2)
        query = create_item("Query", "Q=X_A W_Q", 3, 2, PURE_RED, square_size=self.square_size,
                            font_size=self.font_size)
        key = create_item("Key", "K^{T}=W_K^{T}X_B{T}", 2, 4, PURE_GREEN, square_size=self.square_size,
                          font_size=self.font_size)
        value = create_item("Value", "V=X_B W_V", 4, 3, color=PINK, square_size=self.square_size,
                            font_size=self.font_size)
        score = create_item("Attention score", "A=\sigma({QK^T}/{d_K})", 3, 4, square_size=self.square_size,
                            font_size=self.font_size, color=BLACK)

        output = create_item("Output", "O=AV", 4, 3, color=GOLD_E, square_size=self.square_size,
                             font_size=self.font_size)

        query.move_to(input1.get_center() + np.array([self.square_size * 5, 0, 0]))
        key.move_to(input2.get_center() + np.array([self.square_size * 5, self.square_size * 3, 0]))
        score.next_to(key, RIGHT, buff=2 * self.square_size)
        label_score_y = MathTex("l_A", font_size=self.font_size + 10, color=BLACK)
        arrow_y = DoubleArrow(score[0].get_bottom(), score[0].get_top(), color=BLACK)
        arrow_y.next_to(score[0].get_left(), LEFT, buff=0.1 * self.square_size)
        label_score_y.next_to(arrow_y.get_left(), LEFT, buff=0.1 * self.square_size)
        label_score_x = MathTex("l_B", font_size=self.font_size + 10, color=BLACK)
        arrow_x = DoubleArrow(score[0].get_left(), score[0].get_right(), color=BLACK)
        arrow_x.next_to(score[0].get_bottom(), DOWN, buff=0.05 * self.square_size)
        label_score_x.next_to(arrow_x.get_bottom(), DOWN, buff=0.05 * self.square_size)
        group_label_score = Group(label_score_x, arrow_x, label_score_y, arrow_y)
        value.move_to(input2.get_center() + np.array([self.square_size * 7, self.square_size * -2, 0]))
        arrow_query = Arrow(input1.get_right(), query.get_left(), color=BLACK)
        arrow_key = Arrow(input2.get_right(), key.get_left(), color=BLACK)
        arrow_value = Arrow(input2.get_right(), value.get_left(), color=BLACK)
        output.next_to(value.get_center() + np.array([5 * self.square_size, -1 * self.square_size, 0]))
        dk_labels = MathTex(r"d_{K}", font_size=self.font_size + 10, color=BLACK)
        arrow_dk = DoubleArrow(query[0].get_bottom(), query[0].get_top(), color=BLACK)
        arrow_dk.next_to(query[0], DOWN, buff=0.1 * self.square_size)
        dk_labels.next_to(arrow_dk, DOWN, buff=0.1 * self.square_size)
        global_group = Group(labeled_input1, labeled_input2, query, key, value, score, output, arrow_value, arrow_key,
                             arrow_query, group_label_score,token,label_tok,l_tok)
        global_group.scale_to_fit_height(0.9 * config.frame_height)
        # global_group.scale_to_fit_width(0.9*config.frame_width)
        self.camera.frame_center = global_group.get_center()
        #create queries
        self.add(labeled_input2,token,label_tok)
        self.wait(1)
        self.add(l_tok)
        query_group=Group(token)
        pe_label=Group(MathTex(r"\phi(1)",color=BLACK,font_size=5).move_to(token.get_center()))
        for idx,tok in enumerate(l_tok):
            self.play(tok.animate.next_to(token.get_bottom(),DOWN,buff=idx*tok.width*0.5))
            pe_label.add(MathTex(r"\phi(t_{" + f"{idx}"+r"}", color=BLACK, font_size=30).move_to(tok.get_center()))
            query_group.add(tok)
        self.wait(1)

        self.play(FadeIn(pe_label))
        self.play(FadeOut(pe_label))
        self.wait(1)
        #self.add(labeled_input1, labeled_input2, query, key, value, arrow_query, arrow_value, arrow_key)