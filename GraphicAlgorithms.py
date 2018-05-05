



def flood_fill(plot_array, j, i):
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

def line_draw(plot_array, x_start, y_start, x_end, y_end):
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
