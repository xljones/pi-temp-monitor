import curses
import math

"""
    Based on CursesBarGraph (markfickett/fht_curses_graph)
    https://gist.github.com/markfickett/9eb86be659df639b0eee
"""


class CursesBarGraph:
    def __init__(self):
        self._window = None
        self._max = 100

    def __enter__(self):
        self._window = curses.initscr()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        curses.endwin()

    def update(self, values):
        assert self._window
        h, w = self._window.getmaxyx()
        per_bucket = max(1, math.ceil(float(len(values)) / (w - 1)))
        self._window.erase()
        for column_num, v in enumerate(self._averaged_chunks(values, per_bucket)):
            assert column_num < w
            self._draw_bar(column_num, v, h)

        self._draw_axis_labels(h, w, column_num, len(values))
        self._window.refresh()

    def _averaged_chunks(self, iterable, n):
        summed_v = 0
        summed_count = 0
        for v in iterable:
            summed_v += v
            summed_count += 1
            if summed_count >= n:
                yield float(summed_v) / summed_count
                summed_v = 0
                summed_count = 0
        if summed_count > 0:
            yield float(summed_v) / summed_count

    def _draw_bar(self, column_num, value, h):
        bar_len = max(0, min(h - 1, int(h * (value / self._max))))
        # vline draws from the starting coordinate towards positive y (down).
        self._window.vline((h - 1) - bar_len, column_num, ord("|"), bar_len)

    def _draw_axis_labels(self, h, w, max_column, num_values):
        self._window.addstr(0, 0, str(self._max))
        self._window.addstr(h - 1, 0, str(0))
        max_column_str = str(num_values)
        self._window.addstr(
            h - 1, min(max_column, w - (len(max_column_str) + 1)), max_column_str
        )
