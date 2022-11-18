import Main

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