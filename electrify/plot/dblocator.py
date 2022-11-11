from matplotlib.ticker import Locator


class DbLocator(Locator):
    """
    Place a tick on every multiple of some base number of points
    plotted, e.g., on every 5th point.  It is assumed that you are doing
    index plotting; i.e., the axis is 0, len(data).  This is mainly
    useful for x ticks.
    """

    def set_params(self):
        pass

    def __call__(self):
        """Return the locations of the ticks"""
        dmin, dmax = self.axis.get_data_interval()
        return self.tick_values(dmin, dmax)

    def tick_values(self, vmin, vmax):
        ticks = []
        for f in range(vmin, vmax, 1):
            if -10 < f < 10:
                if f % 3 == 0:
                    ticks.append(f)
            elif f % 10 == 0:
                ticks.append(f)
        return self.raise_if_exceeds(ticks)
