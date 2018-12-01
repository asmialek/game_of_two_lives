import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import mpl_toolkits.axes_grid1
import matplotlib.widgets


# stolen from: https://stackoverflow.com/questions/44985966
#              /managing-dynamic-plotting-in-matplotlib-animation-module


class Player(FuncAnimation):
    def __init__(self, fig, func, frames=None, init_func=None, fargs=None,
                 save_count=None, min=0, max=100, pos=(0.345, 0.02), **kwargs):
        self.i = 0
        self.min = 0
        self.max = max-1
        self.runs = True
        self.forwards = True
        self.fig = fig
        self.func = func
        self.setup(pos)
        FuncAnimation.__init__(self, self.fig, self.func, frames=self.play(),
                               init_func=init_func, fargs=fargs,
                               save_count=save_count, **kwargs)

    def play(self):
        while self.runs:
            self.i = self.i + self.forwards - (not self.forwards)
            if self.max > self.i > self.min:
                self.button_forward.active = True
                self.button_oneforward.active = True
                self.button_back.active = True
                self.button_oneback.active = True
                if self.i == 0:
                    self.i = 1
                    yield 1
                else:
                    yield self.i
            else:
                if self.i >= self.max:
                    self.i = self.max
                    self.button_forward.active = False
                    self.button_oneforward.active = False
                elif self.i <= self.min:
                    self.i = self.min
                    self.button_back.active = False
                    self.button_oneback.active = False
                self.stop()
                if self.i == 0:
                    self.i = 1
                    yield 1
                else:
                    yield self.i

    def start(self):
        self.runs = True
        self.button_stop.active = True
        self.event_source.start()

    def stop(self, event=None):
        self.runs = False
        self.button_stop.active = False
        self.event_source.stop()

    def forward(self, event=None):
        self.forwards = True
        self.button_stop.active = True
        self.start()

    def backward(self, event=None):
        self.forwards = False
        self.button_stop.active = True
        self.start()

    def oneforward(self, event=None):
        self.forwards = True
        self.button_back.active = True
        self.button_oneback.active = True
        self.onestep()

    def onebackward(self, event=None):
        self.forwards = False
        self.button_forward.active = True
        self.button_oneforward.active = True
        self.onestep()

    def onestep(self):
        if self.max > self.i > self.min:
            self.i = self.i + self.forwards - (not self.forwards)
        elif self.i == self.min and self.forwards:
            self.i += 1
        elif self.i == self.max and not self.forwards:
            self.i -= 1
        self.func(self.i)
        self.fig.canvas.draw_idle()

    def setup(self, pos):
        playerax = self.fig.add_axes([pos[0], pos[1], 0.32, 0.06])
        divider = mpl_toolkits.axes_grid1.make_axes_locatable(playerax)

        bax = divider.append_axes("right", size="80%", pad=0.05)
        sax = divider.append_axes("right", size="80%", pad=0.05)
        fax = divider.append_axes("right", size="80%", pad=0.05)
        ofax = divider.append_axes("right", size="100%", pad=0.05)

        self.button_oneback = matplotlib.widgets.Button(playerax,
                                                        label='$\u29CF$')
        self.button_back = matplotlib.widgets.Button(bax,
                                                     label='$\u25C0$')
        self.button_stop = matplotlib.widgets.Button(sax,
                                                     label='$\u25A0$')
        self.button_forward = matplotlib.widgets.Button(fax,
                                                        label='$\u25B6$')
        self.button_oneforward = matplotlib.widgets.Button(ofax,
                                                           label='$\u29D0$')

        self.button_oneback.on_clicked(self.onebackward)
        self.button_back.on_clicked(self.backward)
        self.button_stop.on_clicked(self.stop)
        self.button_forward.on_clicked(self.forward)
        self.button_oneforward.on_clicked(self.oneforward)


if __name__ == '__main__':
    fig, ax = plt.subplots()
    x = np.linspace(0, 6*np.pi, num=100)
    y = np.sin(x)

    ax.plot(x, y)
    point, = ax.plot([], [], marker="o", color="crimson", ms=5)

    def update(i):
        point.set_data(x[i], y[i])

    ani = Player(fig, update, max=len(y)-1)

    plt.show()