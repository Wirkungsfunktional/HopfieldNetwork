import numpy as np

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
        self.bresenham_line_draw()
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

    def bresenham_line_draw(self):
        dx = self.x_end - self.x_start
        dy = self.y_end - self.y_start
        x = self.x_start
        y = self.y_start
        inc_x1 = 0
        inc_x2 = 0
        inc_y1 = 0
        inc_y2 = 0


        if dx < 0:
            inc_x1 = -1
            inc_x2 = -1
        elif dx > 0:
            inc_x1 = 1
            inc_x2 = 1
        if dy < 0:
            inc_y1 = -1
        elif dy>0:
            inc_y1 = 1
        l = np.abs(dx);
        s = np.abs(dy);
        if not (l>s):
            l, s = s, l
            if dy < 0:
                inc_y2 = -1
            elif (dy>0):
                inc_y2 = 1
            inc_x2 = 0

        step = l / 2;
        for i in range(l+1):
            self.canvas.data.set_point(y, x, -1)
            step += s
            if not (step < l):
                step -= l
                x += inc_x1
                y += inc_y1
            else:
                x += inc_x2
                y += inc_y2


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


class RectangleDrawTool(GraphicTool):
    def __init__(self, canvas):
        super().__init__(canvas)

    def on_release(self, event):
        super().on_release(event)
        self.draw_rectangle()
        super().update()

    def draw_rectangle(self):
        inc_range = lambda a, b: range(a, b+1)
        for i in inc_range(*sorted([self.x_start, self.x_end])):
            self.canvas.data.set_point( self.y_start, i, -1)
            self.canvas.data.set_point( self.y_end, i, -1)
        for i in inc_range(*sorted([self.y_start, self.y_end])):
            self.canvas.data.set_point( i, self.x_start, -1)
            self.canvas.data.set_point( i, self.x_end, -1)


class CircleDrawTool(GraphicTool):
    def __init__(self, canvas):
        super().__init__(canvas)


    def on_release(self, event):
        super().on_release(event)
        self.draw_circle()
        super().update()

    def draw_circle(self):
        r = int(np.sqrt((self.x_end - self.x_start)**2 + (self.y_end - self.y_start)**2 ))
        x = 0
        y = r
        y0 = self.y_start
        x0 = self.x_start
        d = 1 - r
        deltaE = 3
        deltaSE = -2 * r + 5
        self.canvas.data.set_point(y0 + y, x0 + x, -1)
        self.canvas.data.set_point(y0 - y, x0 + x, -1)
        self.canvas.data.set_point(y0 + y, x0 - x, -1)
        self.canvas.data.set_point(y0 - y, x0 - x, -1)
        self.canvas.data.set_point(y0 + x, x0 + y, -1)
        self.canvas.data.set_point(y0 - x, x0 + y, -1)
        self.canvas.data.set_point(y0 + x, x0 - y, -1)
        self.canvas.data.set_point(y0 - x, x0 - y, -1)

        while y > x:
            if d < 0:
                d += deltaE;
                deltaE += 2;
                deltaSE += 2;
                x += 1;
            else:
                d += deltaSE;
                deltaE += 2;
                deltaSE += 4;
                x += 1;
                y -= 1;
            self.canvas.data.set_point(y0 + y, x0 + x, -1)
            self.canvas.data.set_point(y0 - y, x0 + x, -1)
            self.canvas.data.set_point(y0 + y, x0 - x, -1)
            self.canvas.data.set_point(y0 - y, x0 - x, -1)
            self.canvas.data.set_point(y0 + x, x0 + y, -1)
            self.canvas.data.set_point(y0 - x, x0 + y, -1)
            self.canvas.data.set_point(y0 + x, x0 - y, -1)
            self.canvas.data.set_point(y0 - x, x0 - y, -1)
