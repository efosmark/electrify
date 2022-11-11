from .qt_screens.ui_solutiondialog import Ui_SolutionDialog
from PySide6 import QtWidgets
import matplotlib.gridspec as gridspec
from gfd.profile import GFDProfile
from gfd.solution import GFDSolution
from gfd.geneticcircuit import GeneticCircuit

from .circuit_canvas import draw_circuit

import electrify as e

from .bode import BodePlotManager


class SolutionDialog(QtWidgets.QDialog, Ui_SolutionDialog):

    def __init__(self, profile: GFDProfile):
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.profile = profile
        self.gfd = GeneticCircuit(freq_domain=self.profile.domain)
        self.closeBtn.clicked.connect(self.hide)
        self.frequencyInput.setValue(e.mega(15))
        self.recomputeBtn.clicked.connect(self._onRecompute)

        fig = self.circuitCanvas.figure
        fig.set_tight_layout(True)
        gs = gridspec.GridSpec(2, 3, height_ratios=[1, 5], figure=fig)
        self.axfq = fig.add_subplot(gs[0, 0:2])
        self.axck = fig.add_subplot(gs[1, :])

        self.bode = BodePlotManager(self.axfq)
        self.bode.configure(
            self.profile.domain,
            f_max=self.profile.f_max,
            f_min=self.profile.f_min
        )

    def _onRecompute(self):
        self.solution.chromosome = eval(self.chromosomeText.toPlainText())
        self.recompute()

    def recompute(self):
        if self.solution is not None:
            self.chromosomeText.setPlainText(str(self.solution.chromosome))

            self.bode.plot_fq(self.solution)
            self.bode.plot_ph(self.solution)

            # values = [self.solution.ft_gain, self.solution.ft_phase,
            #           self.solution.ft_gain_derivative, self.solution.ft_phase_derivative]
            # if self.bar_container is None:
            #     labels = ['$H(\omega)$', r'$\theta$', r'$\frac{dg}{dx}$', r'$\frac{d\theta}{dx}$']
            #     self.bar_container = self.bar_ax.bar(labels, values, align='center', width=0.4)
            #     self.bar_ax.xaxis.set_tick_params(width=1, labelsize=12)
            #     self.bar_ax.yaxis.set_tick_params(width=1, labelsize=8)
            # else:
            #     self.bar_container.datavalues = values
            # self.fitnessCanvas.draw()

            c = self.gfd.create_circuit(self.solution.chromosome)
            c.solve(f=self.frequencyInput.getValue())
            c.solver.annotate()

            self.axck.clear()
            draw_circuit(self.axck, c)
            self.circuitCanvas.draw()

    def display(self, solution: GFDSolution):
        self.solution = solution
        self.recompute()
        self.show()
