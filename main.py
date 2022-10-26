import time
import pygame
import threading

pygame.font.init()

W_WIDTH = 1024
W_HEIGHT = 600
FONT_SIZE = 30
BAR_SPACING = 200
BAR_GUTTER = 20

START_TIME = time.time()

TARGET_COLOR = (0, 150, 0)
WARNING_COLOR = (200, 200, 0)
FAULT_COLOR = (255, 0, 0)

COLOR_BACKGROUND = (0, 0, 0)

screen = pygame.display.set_mode([W_WIDTH, W_HEIGHT])
pygame.display.set_caption('NER17D_GUI')
font = pygame.font.Font(pygame.font.get_default_font(), FONT_SIZE)



class WarningBars:
    top_margin = 20
    left_margin = 20

    def __init__(self):
        self.warning_bars = []
        self.num_bars = 0

    def add_bar(self, title, unit, target, warning, fault):
        self.warning_bars.append(
            WarningBar(self.left_margin + self.num_bars * BAR_SPACING, self.top_margin, title, unit, target, warning, fault))
        self.num_bars += 1

    def update_bars(self, values):
        for i, bar in enumerate(self.warning_bars):
            bar.update_value(values[i])

    def draw_bars(self):
        for bar in self.warning_bars:
            bar.draw_bar()


class WarningBar:
    fault_line = 80
    margin = 20
    target_line = 300
    width = BAR_SPACING - BAR_GUTTER
    height = 300
    title_size = 30
    title_font = pygame.font.Font(pygame.font.get_default_font(), title_size)

    def __init__(self, x, y, title, unit, target, warning, fault):
        self.x_pos = x
        self.y_pos = y
        self.title = title
        self.unit = unit
        self.target = target
        self.warning = warning
        self.fault = fault
        self.warning_line = self.target_line - (
                    (self.target_line - self.fault_line) * (self.warning - self.target) / (self.fault - self.target))
        self.value = target
        self.state = 0
        self.title_color = TARGET_COLOR
        self.flipped = fault < target

    def draw_bar(self):
        # draw lines
        pygame.draw.line(screen, FAULT_COLOR, (self.x_pos, self.y_pos + self.fault_line),
                         (self.x_pos + self.width, self.y_pos + self.fault_line), 2)
        pygame.draw.line(screen, TARGET_COLOR, (self.x_pos, self.y_pos + self.target_line),
                         (self.x_pos + self.width, self.y_pos + self.target_line), 1)
        pygame.draw.line(screen, WARNING_COLOR, (self.x_pos, self.y_pos + self.warning_line),
                         (self.x_pos + self.width, self.y_pos + self.warning_line), 1)

        # draw title
        title = font.render(self.title, False, self.title_color)
        title_rect = title.get_rect(center=(self.x_pos + self.width / 2, self.y_pos + self.title_size / 2))
        screen.blit(title, title_rect)

        # draw value
        value = font.render(str(self.value) + self.unit, False, self.title_color)
        value_rect = value.get_rect(center=(self.x_pos + self.width / 2, self.y_pos + 3 * self.title_size / 2))
        screen.blit(value, value_rect)

        # draw bars
        scaled_value = ((self.value - self.target) / (self.fault - self.target)) * (self.target_line - self.fault_line)

        if self.value <= self.target and not self.flipped or self.value >= self.target and self.flipped:
            pygame.draw.rect(screen, TARGET_COLOR, (self.x_pos + self.margin, self.y_pos + self.target_line,
                                                         self.width - 2 * self.margin, abs(scaled_value)), 0)
        else:
            if self.value > self.warning and not self.flipped or self.value < self.warning and self.flipped:
                pygame.draw.rect(screen, FAULT_COLOR,
                                 (self.x_pos + self.margin, self.y_pos + self.target_line - scaled_value,
                                  self.width - 2 * self.margin,
                                  abs(scaled_value)), 0)
            else:
                pygame.draw.rect(screen, WARNING_COLOR,
                                 (self.x_pos + self.margin, self.y_pos + self.target_line - scaled_value,
                                  self.width - 2 * self.margin,
                                  scaled_value), 0)

    def update_value(self, value):
        self.value = value

        # under target value (green)
        if self.value <= self.target and not self.flipped or self.value >= self.target and self.flipped:
            if self.state is not 0:
                self.title_color = TARGET_COLOR
                self.state = 0

        # under warning value (yellow)
        elif self.value <= self.warning and not self.flipped or self.value >= self.warning and self.flipped :
            if self.state is not 1:
                self.title_color = WARNING_COLOR
                self.state = 1

        # under fault value (red)
        else:
            if self.state is not 2:
                self.new_warning()
                self.title_color = FAULT_COLOR
                self.state = 2

    def new_warning(self):
        print("new warning")
        pass

    def new_fault(self):
        print("new fault")
        pass


class Graphs():
    def __init__(self):
        self.graphs = []
        self.num_graphs = 0

    def add_graph(self, title, unit, target, warning, fault):
        self.graphs.append(Graph(title, unit, target, warning, fault))
        self.num_graphs += 1

    def update_graphs(self, values):
        for i, bar in enumerate(self.graphs):
            bar.add_point(time.time(), values[i])

    def draw_graph(self, graph_num):
        self.graphs[graph_num].scroll_graph()


class Graph():
    x_scale = 100
    side_margin = 50
    width = 900
    height = 400
    fault_line = 80
    target_line = 400

    def __init__(self, title, unit, target, warning, fault):
        self.laps = []
        self.points = []
        self.line_color = TARGET_COLOR
        self.x_pos = 20
        self.y_pos = 20
        self.title = title
        self.unit = unit
        self.target = target
        self.warning = warning
        self.fault = fault
        self.x_offset = 0
        self.scroll = 0
        self.scrolling = False
        self.warning_line = self.target_line - (
                (self.target_line - self.fault_line) * (self.warning - self.target) / (self.fault - self.target))

    def add_point(self, time_stamp, value):
        scaled_value = ((value - self.target) / (self.fault - self.target)) * (self.target_line - self.fault_line)
        mapped_time_stamp = (time_stamp - START_TIME) * self.x_scale
        self.points.append((mapped_time_stamp, scaled_value))

    def draw_lines(self):
        pygame.draw.line(screen, FAULT_COLOR, (self.x_pos, self.y_pos + self.fault_line),
                         (self.x_pos + self.width - self.side_margin, self.y_pos + self.fault_line), 2)
        pygame.draw.line(screen, TARGET_COLOR, (self.x_pos, self.y_pos + self.target_line),
                         (self.x_pos + self.width - self.side_margin, self.y_pos + self.target_line), 1)
        pygame.draw.line(screen, WARNING_COLOR, (self.x_pos, self.y_pos + self.warning_line),
                         (self.x_pos + self.width - self.side_margin, self.y_pos + self.warning_line), 1)

    def live_scroll(self):
        self.scrolling = False

    def scroll_back(self):
        self.scrolling = True
        self.scroll -= 20

    def scroll_forward(self):
        self.scrolling = True
        self.scroll += 20

    def scroll_graph(self):
        if self.scrolling is False:
            self.scroll = (time.time() - START_TIME) * self.x_scale
            self.draw_graph()
        else:
            self.draw_graph()

    def check_color(self):
        if self.points[len(self.points) - 1][1] < 0:
            self.line_color = TARGET_COLOR
        elif self.target_line - self.points[len(self.points) - 1][1] > self.warning_line:
            self.line_color = WARNING_COLOR
        else:
            self.line_color = FAULT_COLOR

    def draw_graph(self,):
        self.check_color()
        self.draw_lines()
        for i in range(len(self.points) - 1, 0, -1):
            if self.points[i][0] - self.scroll > 0:
                continue
            pygame.draw.line(screen, self.line_color, (
                            self.x_pos + self.width - self.side_margin + self.points[i][0] - self.scroll,
                            self.y_pos + self.target_line - self.points[i][1]),
                             (self.x_pos + self.width - self.side_margin + self.points[i - 1][0] - self.scroll,
                              self.y_pos + self.target_line - self.points[i - 1][1]), 3)
            if self.width - self.side_margin + self.points[i][0] - self.scroll < 0:
                break





def main():
    """
        :return:
    """
    warning_bars = WarningBars()
    warning_bars.add_bar("Battery", " C", 0, 75, 100)
    warning_bars.add_bar("Motor", " C", 0, 50, 100)
    warning_bars.add_bar("M controller", " C", 0, 80, 100)
    warning_bars.add_bar("SOC", " %", 100, 10, 0)

    graphs = Graphs()
    graphs.add_graph("Battery", " C", 0, 75, 100)
    graphs.add_graph("Motor", " C", 0, 50, 100)

    i1 = 0
    i2 = 0
    i3 = 0
    i4 = 100

    current_screen = 0

    while True:
        screen.fill(COLOR_BACKGROUND)

        mouse = pygame.mouse.get_pos()
        i1 = mouse[0] - 100
        i2 = mouse[1] - 100
        
        graphs.update_graphs([i1, i2, i3, i4])
        warning_bars.update_bars([i1, i2, i3, i4])

        if current_screen is 0:
            warning_bars.draw_bars()
        elif current_screen is 1:
            graphs.draw_graph(0)
        elif current_screen is 2:
            graphs.draw_graph(1)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # test code
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    pass
                if event.key == pygame.K_s:
                    pass
                if event.key == pygame.K_d:
                    pass
                if event.key == pygame.K_1:
                    current_screen = 0
                if event.key == pygame.K_2:
                    current_screen = 1
                if event.key == pygame.K_3:
                    current_screen = 2
                if event.key == pygame.K_4:
                    i4 = mouse[0] - 100



if __name__ == "__main__":
    main()
