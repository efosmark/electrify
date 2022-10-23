from .qt_screens.ui_solutiondialog import Ui_SolutionDialog
from PySide6 import QtWidgets
import matplotlib.gridspec as gridspec
from gfd.profile import GFDProfile
from gfd.solution import GFDSolution
from gfd.geneticcircuit import GeneticCircuit

from .circuit_canvas import draw_circuit

import electrify as e


class SolutionDialog(QtWidgets.QDialog, Ui_SolutionDialog):

    def __init__(self, profile: GFDProfile):
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.profile = profile
        self.gfd = GeneticCircuit(freq_domain=self.profile.domain)
        # self.closeBtn.clicked.connect(self.hide)
        # self.frequencyInput.setValue(e.mega(15))
        # self.recomputeBtn.clicked.connect(self._onRecompute)
        # self.circuitCanvas.configure(2000, 2000)

        # self.mainBodePlot.configure(
        #     self.profile,
        #     ylabel=None,
        #     xlabel=None,
        #     width=500,
        #     height=300
        # )

        # fig = self.circuitCanvas.figure
        # gs = gridspec.GridSpec(2, 2, height_ratios=[1, 4], figure=fig)
        # self.axfq = fig.add_subplot(gs[0, 0])
        # self.bar_ax = fig.add_subplot(gs[0, 1])
        # self.axck = fig.add_subplot(gs[1, :])

        # self.mainBodePlot.axfq.set_ylim(-60, 1)
        # self.mainBodePlot.axdv.set_axis_off()
        # self.mainBodePlot.axph.set_axis_off()
        # #self.bar_ax = self.fitnessCanvas.figure.add_subplot(111)
        # self.bar_container = None

        #self.fitnessCanvas.configure(width=300, height=300, tight=dict(pad=0.3))

    def _onRecompute(self):
        self.solution.chromosome = eval(self.chromosomeText.toPlainText())
        self.recompute()

    def recompute(self):
        if self.solution is not None:
            self.chromosomeText.setPlainText(str(self.solution.chromosome))

            # self.mainBodePlot.plot_fq(self.solution)
            # self.mainBodePlot.plot_ph(self.solution)
            # self.mainBodePlot.plot_dv(self.solution)
            # self.mainBodePlot.draw()

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

            #c = self.gfd.create_circuit(self.solution.chromosome)
            # c.solve(f=self.frequencyInput.getValue())
            # c.solver.annotate()

            # self.axck.clear()
            #draw_circuit(self.axck, c)
            # self.circuitCanvas.draw()

            # self.mainBodePlot.draw()

    def display(self, solution: GFDSolution):
        self.solution = solution
        self.recompute()
        self.show()
