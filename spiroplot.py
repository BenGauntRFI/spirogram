
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RangeSlider


def phasor(theta, r):
    """
    Caluclates the complex exponential for given r and theta.
    :param theta: phase angle, can be numpy array
    :param r: magnitude, should be a float
    :return: numpy array of complex values with magnitude r and phase angles given by thetas
    """
    return r * np.exp(1j * theta)

def spiro_sum(theta, theta_ratios, r_vals):
    """
    Adds together a series of phasors to create a complex pattern.
    :param theta: numpy array of phase angles to map over
    :param theta_ratios: numpy array with ratios for each phasor determining how fast it rotates in relation
    to the global theta value. 1.0 = same speed, 0.5 = half as fast, 2.0 = twice as fast
    :param r_vals: numpy array with a radius for each phasor
    :return: numpy array of complex values making up the spirogram.  Same size as theta.
    """

    spirograph = np.zeros(theta.shape)
    for i in range(len(theta_ratios)):
        phasor_vals = phasor(theta * theta_ratios[i], r_vals[i])
        spirograph = spirograph + phasor_vals

    return spirograph




if __name__ == '__main__':
    N = 10000 #number of points for full theta array
    NUM_LOOPS = 25 #how many times to loop round
    NUM_PHASORS = 3

    theta_arr = np.linspace(0, NUM_LOOPS * 2 * np.pi, N)

    theta_ratios_arr = np.ones(NUM_PHASORS)
    r_vals_arr = np.ones(NUM_PHASORS)

    complex_spirograph = spiro_sum(theta_arr, theta_ratios_arr, r_vals_arr)

    fig, ax = plt.subplots()
    line, = ax.plot(np.real(complex_spirograph), np.imag(complex_spirograph), lw=2)
    ax.set_xlabel('Real component')
    ax.set_ylabel('Imaginary component')
    ax.set_aspect('equal', 'box')

    slider_fig, fig_axes = plt.subplots(nrows=2 * NUM_PHASORS)

    sliders = [None] * 2 * NUM_PHASORS
    for i in range(NUM_PHASORS):
        sliders[2 * i] = Slider(
            ax=fig_axes[2 * i],
            label=f'Theta {i + 1}',
            valmin=0.1,
            valmax=1.9,
            valinit=1.0
        )

        sliders[(2 * i) + 1] = Slider(
            ax=fig_axes[(2 * i) + 1],
            label=f'Radius {i + 1}',
            valmin=0.0,
            valmax=2.0,
            valinit=1.0
        )


    def update(val):
        for i in range(NUM_PHASORS):
            theta_ratios_arr[i] = sliders[2 * i].val
            r_vals_arr[i] = sliders[(2 * i) + 1].val

        complex_spirograph = spiro_sum(theta_arr, theta_ratios_arr, r_vals_arr)
        line.set_xdata(np.real(complex_spirograph))
        line.set_ydata(np.imag(complex_spirograph))
        fig.canvas.draw_idle()

    def on_close(event):
        plt.close('all')

    fig.canvas.mpl_connect('close_event', on_close)
    slider_fig.canvas.mpl_connect('close_event', on_close)

    for slider in sliders:
        slider.on_changed(update)


    plt.show()

