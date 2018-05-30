

class Canvas():
    def __init__(self, fig, img, data):
        self.data = data
        self.img = img
        self.fig = fig

    def update(self):
        self.img.set_data(self.data.get_quadratic_rep())
        self.img.autoscale()
        self.fig.canvas.draw()

    def get_data(self):
        return self.data.get_quadratic_rep()

    def set_data(self, data):
        self.data = data





class GraphicTool():
    def __init__(self, canvas):
        self.x_start = None
        self.x_end = None
        self.y_start = None
        self.y_end = None
        self.canvas = canvas

    def on_click(self, event):
            self.x_start = int(event.xdata+0.5)
            self.y_start = int(event.ydata+0.5)

    def on_release(self, event):
            self.x_end = int(event.xdata+0.5)
            self.y_end = int(event.ydata+0.5)


    def on_motion(self, event):
        pass

    def update(self):
        self.canvas.update()

class LineDrawTool(GraphicTool):

    def __init__(self, canvas):
        super().__init__(canvas)

    def on_release(self, event):
        super().on_release(event)
        self.update()

    def update(self):
        self.line_draw(  self.canvas.get_data(),
                    self.x_start, self.y_start, self.x_end, self.y_end)
        super().update()

    def line_draw(self, plot_array, x_start, y_start, x_end, y_end):
        """TODO: Implement 8 case selection from generic to prototype."""


        y = y_start
        d = 0
        dx = x_end - x_start
        dy = y_end - y_start
        m = dx/dy * 1.0
        print(str(m) + " " + str(dx))
        dd_r = -dy
        dd_ro = dx - dy
        c = 2 * dy - dx
        for xx in range(x_start, x_end):
            plot_array[y][xx] = -1
            if c <= 2*d:
                d += dd_r
            else:
                y += 1
                d += dd_ro
        return plot_array

class FillDrawTool(GraphicTool):
    def __init__(self, canvas):
        super().__init__(canvas)

    def on_click(self, event):
        super().on_click(event)
        self.update()

    def update(self):
        self.flood_fill(  self.canvas.get_data(),#self.new_pattern.get_quadratic_rep(),
                                self.x_start, self.y_start)
        super().update()


    def flood_fill(self, plot_array, j, i):
        """Fill a bounded region acording to the 4 neighbour rule.
        TODO: Avoid recursion deep assertion by using queues."""
        def is_valid_field(plot_array, i, j):
            size = plot_array.shape
            if i < 0 or j < 0:
                return False
            if i > (size[0]-1) or j > (size[1]-1):
                return False
            if plot_array[i][j] == -1:
                return False
            return True
        def rec_fill(plot_array, i, j):
            if is_valid_field(plot_array, i, j) == False:
                return
            else:
                plot_array[i][j] = -1
                rec_fill(plot_array, i + 1, j)
                rec_fill(plot_array, i - 1, j)
                rec_fill(plot_array, i, j + 1)
                rec_fill(plot_array, i, j - 1)
        rec_fill(plot_array, i, j)
        return plot_array

class PenDrawTool(GraphicTool):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.is_clicked = 0

    def on_click(self, event):
        super().on_click(event)
        self.is_clicked = 1

    def on_release(self, event):
        super().on_release(event)
        self.is_clicked = 0

    def on_motion(self, event):
        if self.is_clicked:
            self.canvas.data.set_point( int(event.ydata+0.5),
                                        int(event.xdata+0.5),
                                        -1)
            super().update()
