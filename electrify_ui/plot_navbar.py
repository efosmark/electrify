from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class PlotNavBar(NavigationToolbar):
    toolitems = (
        ('Home', 'Reset original view', 'home', 'home'),
        (None, None, None, None),
        ('Pan',
         'Left button pans, Right button zooms\n'
         'x/y fixes axis, CTRL fixes aspect',
         'move', 'pan'),
        ('Zoom', 'Zoom to rectangle\nx/y fixes axis', 'zoom_to_rect', 'zoom'),
        (None, None, None, None),
        ('Save', 'Save the figure', 'filesave', 'save_figure'),
    )
