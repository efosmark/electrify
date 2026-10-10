import numpy as np
from matplotlib.ticker import EngFormatter, NullFormatter, FixedLocator


default_settings = {
    "show_grid": True,
    "show_phase": True,
    "show_gain": True,
    "show_gain_max": False,
    "show_gain_min": False,
    "show_bandwidth": True,
    "show_phase_0deg_points": False,
    "show_legend": True,

    "f_min": 1e6,
    "f_max": 1e9,
    "f_samples": 300,

    "fig_size_x": 18.5,
    "fig_size_y": 10.5,

    "y_autoscale": True,
    "y_normalize": True,
    # "y_min": -30,
    # "y_max": 3,

    # "y_min_phase": -200,
    # "y_max_phase": 200,

    # "title": "",

    "verbose": False,
}


def set_up_frequency_axis(ax, config, ymin, ymax):
    ax.set_xscale('log')
    ax.xaxis.set_tick_params('major', width=1, rotation=270, size=10)
    ax.xaxis.set_tick_params('minor', width=1, rotation=270, size=10)
    ax.xaxis.set_major_formatter(EngFormatter('Hz', places=0))
    ax.xaxis.set_minor_formatter(EngFormatter('Hz', places=0))
    ax.set_ylabel('Gain (dB)', color='b', fontsize=15)
    ax.set_xlabel('Frequency (Hz)', fontsize=15)
    
    ax.set_xlim(config['f_min'], config['f_max'])
    ax.set_xbound(lower=config['f_min'], upper=config['f_max'])

    if config.get("y_autoscale"):
        spacing = (ymax-ymin) * 0.05
        upper = min(300, ymax + spacing)
        lower = max(-300, ymin - spacing)

        if 'y_max' in config and upper > config['y_max']:
            upper = config['y_max']

        if 'y_min' in config and lower < config['y_min']:
            lower = config['y_min']

        ax.set_ybound(lower=lower)
        ax.set_ylim(bottom=lower)
        ax.set_ybound(upper=upper)
        ax.set_ylim(top=upper)

    else:
        if 'y_min' in config:
            ax.set_ybound(lower=config['y_min'])
            ax.set_ylim(bottom=config['y_min'])

        if 'y_max' in config:
            ax.set_ybound(upper=config['y_max'])
            ax.set_ylim(top=config['y_max'])

    bottom, top = ax.get_ylim()
    ticks = []
    for f in range(int(bottom), int(top), 1):
        if -12 <= f <= 12:
            if f % 3 == 0:
                ticks.append(f)
        elif f % 10 == 0:
            ticks.append(f)
    ax.yaxis.set_major_locator(FixedLocator(ticks))


def set_up_bandwidth_axis(ax, bwPoints, config):
    ax.set_xticks([], minor=True)
    ax.xaxis.set_tick_params('major', width=1, length=2,
                             rotation=270, color="red", labelcolor="red")
    ax.set_xscale('log')
    ax.set_xbound(lower=config['f_min'], upper=config['f_max'])
    ax.xaxis.set_major_formatter(EngFormatter('Hz', places=1))
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.set_xticks(bwPoints)


def set_up_phase_axis(ax, config):
    ax.set_ylabel('Phase', color='darkgreen', fontsize=15)
    if 'y_min_phase' in config:
        ax.set_ybound(lower=config['y_min_phase'])
    if 'y_max_phase' in config:
        ax.set_ybound(upper=config['y_max_phase'])


def get_domain(domain_type, f_min, f_max, sample_count):
    if domain_type == "geom":
        return np.geomspace(f_min, f_max, sample_count)
    elif domain_type == "linear":
        return np.linspace(f_min, f_max, sample_count)
    elif domain_type != "static":
        raise ValueError("Unknown domain_type. Must be 'geom', 'linear', or 'static'.")



def bode_plot(fig, yfuncs, **kwargs):
    config = {**default_settings, **kwargs}

    samples = int(config['f_samples'])
    domain_type = config['domain_type']

    if domain_type == 'static':
        x = config['domain']
    else:
        x = get_domain(domain_type, config['f_min'], config['f_max'], samples)

    zero = np.zeros(samples)

    axfq = fig.add_subplot(111)

    xmin = None
    xmax = None
    ymin = None
    ymax = None
    primary_y = None
    for i, (yfunc, _conf) in enumerate(yfuncs):
        _conf = {**config, **_conf}

        if domain_type == "static":
            y = tuple(yfunc)
        else:
            y = tuple(yfunc(float(f)) for f in np.nditer(x))

        if _conf.get('baseline'):
            y = y - _conf['baseline']

        if primary_y is None:
            primary_y = y

        axfq.plot(
            x, y,
            color=_conf.get('color', 'gray'),
            linewidth=_conf.get('linewidth', 1),
            label=_conf.get('label', "static" if domain_type == "static" else yfunc.__name__),
            linestyle=_conf.get('linestyle', "-"),
        )

        if ymin is None or min(y) < ymin and _conf.get('y_autoscale'):
            ymin = min(y)

        if ymax is None or max(y) > ymax and _conf.get('y_autoscale'):
            ymax = max(y)

    if config.get("show_gain_max"):
        xmax = x[np.argmax(primary_y)]
        text = "{}    {:.1f}dB".format(format_value(xmax, places=3, unit="Hz"), ymax)
        bbox_props = dict(boxstyle="square,pad=0.5", fc="w", ec="k", lw=0.72)
        arrowprops = dict(arrowstyle="->", connectionstyle="angle,angleA=0,angleB=60")
        kw = dict(
            xycoords='data',
            textcoords="axes fraction",
            arrowprops=arrowprops,
            bbox=bbox_props,
            ha="right",
            va="top"
        )
        axfq.annotate(text, xy=(xmax, ymax), xytext=(0.97, 0.98), **kw)

    if config.get("show_gain_min"):
        xmin = x[np.argmin(primary_y)]
        text = "{}    {:.1f}dB".format(format_value(xmin, places=3, unit="Hz"), ymin)
        bbox_props = dict(boxstyle="square,pad=0.5", fc="w", ec="k", lw=0.72)
        arrowprops = dict(
            arrowstyle="->", connectionstyle="angle,angleA=0,angleB=-60")
        kw = dict(xycoords='data', textcoords="axes fraction",
                  arrowprops=arrowprops, bbox=bbox_props, ha="right", va="top")
        axfq.annotate(text, xy=(xmin, ymin), xytext=(0.97, 0.04), **kw)

    if config.get('hlines'):
        for hline in config['hlines']:
            axfq.axhline(y=hline, color='black', linestyle='dotted')

    if config.get('vlines'):
        for vline in config['vlines']:
            axfq.axvline(x=vline, color='black', linestyle='dotted')

    if config.get('vspans'):
        for (lower, upper, color) in config['vspans']:
            axfq.axvspan(lower, upper, alpha=0.2, color=color)

    if config.get('show_bandwidth'):
        axbw = axfq.twiny()
        minus3dB = zero - 3
        axbw.plot(x, minus3dB, color="red", linestyle='dotted', label="-3dB")
        bwPoints = []
        bwMax = config['f_max']

        crossoverPoints = np.argwhere(np.diff(np.sign(primary_y - minus3dB))).flatten()
        if crossoverPoints.any():
            for i in crossoverPoints:
                bwPoints.append(x[i])
                axbw.axvline(x=x[i], color='red', linestyle='dotted')

        if len(bwPoints) > 0:
            bwMax = bwPoints[-1]

        axbw.fill_between(
            x=x,
            y1=primary_y,
            y2=minus3dB,
            where=(x < bwMax) & (primary_y > minus3dB),
            color='blue',
            alpha=0.2
        )

        set_up_bandwidth_axis(axbw, bwPoints, config)

    if config.get('phasefuncs'):
        axph = axfq.twinx()
        set_up_phase_axis(axph, config)

        primary_yp = None

        for i, (ypfunc, _conf) in enumerate(config.get('phasefuncs')):
            _conf = {**config, **_conf}
            yp = tuple(ypfunc(float(f)) for f in np.nditer(x))

            if primary_yp is None:
                primary_yp = yp

            axph.plot(
                x, yp,
                color=_conf.get('color', 'darkgreen'),
                linewidth=_conf.get('linewidth', 1),
                label=_conf.get('label', ypfunc.__name__),
                linestyle=_conf.get('linestyle', "dashed"),
            )

            if config['show_phase_0deg_points']:
                axph.plot(x, zero, color="green", linestyle='dotted', label="0°")
                idx = np.argwhere(np.diff(np.sign(zero - yp))).flatten()
                if idx.any() > 0:
                    for i in idx:
                        axph.plot(x[i], zero[i], 'go', label="0° = {}Hz".format(format(x[i])))

    set_up_frequency_axis(axfq, config, ymin, ymax)
    #fig.legend(loc="upper right", bbox_to_anchor=(1, 1), bbox_transform=axfq.transAxes)

    return fig
