import electrify as e
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication, QMainWindow
from gfd.solution import GFDSolution
from gfd.profile import GFDProfile
from gfd.gfd_process import GFDThread
from electrify_ui.plot_navbar import PlotNavBar
from electrify_ui.qt_screens.ui_form import Ui_MainWindow
from electrify_ui.solution_dialog import SolutionDialog
import sys
import yaml


DEFAULT_PROFILE_FILE = './default-profile.yaml'


class GeneticCircuitMainWindow(QMainWindow, Ui_MainWindow):
    uiReady = Signal(bool)
    weightsChanged = Signal(object)
    bandwidthsChanged = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.solutions = []
        self.profile = GFDProfile()
        self._init_profile()
        self._initUi()
        self.sln_dialog = SolutionDialog(self.profile)

    def _init_profile(self):
        profile = None
        with open(DEFAULT_PROFILE_FILE, 'r') as file:
            profile = yaml.safe_load(file).get('profile')
        if profile is None:
            return
        if 'min_frequency' in profile:
            self.profile.f_min = profile['min_frequency']
        if 'max_frequency' in profile:
            self.profile.f_max = profile['max_frequency']
        if 'passband' in profile:
            self.profile.passbands.extend(profile['passband'])
        if 'stopband' in profile:
            self.profile.stopbands.extend(profile['stopband'])
        if 'simulate' in profile:
            simsettings = profile['simulate']
            if 'sample_count' in simsettings:
                self.profile.sample_count = simsettings['sample_count']
            if 'domain_type' in simsettings:
                self.profile.domain_type = simsettings['domain_type']
            if 'derivative_delta' in simsettings:
                self.profile.derivative_delta = simsettings['derivative_delta']
        if 'weights' in profile:
            self.profile.weights = profile['weights']

    def _initUi(self):
        self.setupUi(self)
        self.uiReady.connect(self._onReady)
        self.startStopButton.clicked.connect(self._onClickStart)
        self.stopResetButton.clicked.connect(self._onClickStop)
        self.displaySolutionDialogBtn.clicked.connect(self._onDisplaySolution)
        self.paginator.pageChanging.connect(self._onPageChanging)

        self.weightsFrame.setWeights(dict(self.profile.weights))
        self.weightsFrame.weightsChanged.connect(self._onWeightsChanged)

        self._init_main_plot()
        self._init_mini_plot()

        self.uiReady.emit(True)

    def _init_main_plot(self):
        self.mainBodePlot.configure(
            self.profile,
            hlines=[0, -3],
            ylabel=None,
            xlabel=None,
            include_polar=False,
            vspans=[
                *[(a, b, "red") for a, b in self.profile.stopbands],
                *[(a, b, "green") for a, b in self.profile.passbands]
            ])
        self.mainBodePlot.axdv.set_axis_off()

        self.toolbar = PlotNavBar(self.mainBodePlot, self, coordinates=False)
        self.horizontalLayoutControl.layout().addWidget(self.toolbar)

    def _init_mini_plot(self):
        self.miniplot.configure(
            self.profile,
            tight=dict(pad=0),
            hlines=[-3, -60],
        )
        self.miniplot.axfq.set_ylim(bottom=-65, top=1)
        self.miniplot.axfq.set_ybound(lower=-65, upper=1)
        self.miniplot.axfq.set_axis_off()
        self.miniplot.axdv.set_axis_off()
        self.miniplot.axph.set_axis_off()

    def _solutionReady(self, solution: GFDSolution):
        if solution.new_best or len(self.paginator.pages) == 0:
            page_id = self.paginator.addPage(solution)
            self.paginator.goToPage(page_id)

        self.miniplot.plot_fq(
            solution,
            width=1,
            color='red',
            alpha=0.25,
            persist=True
        )
        self.miniplot.plot_ph(solution)
        # self.miniplot.plot_dv(solution)
        self.miniplot.draw()
        self.generationLabel.setText(str(solution.generation_id))
        self.circuitLabel.setText(str(solution.circuit_id))
        self.computeTimeLabel.setText('{}S'.format(e.format_value(solution.sim_time)))
        self.fitnessLabel_2.setText('{:.0f}'.format(solution.fitness))

    def _onPageChanging(self, page_id, solution: GFDSolution):
        self.mainBodePlot.plot_fq(solution)
        # self.mainBodePlot.plot_dv(solution)
        self.mainBodePlot.plot_ph(solution)
        self.mainBodePlot.draw()

        if solution.fitness and solution.best_fitness:
            self.fitnessLabel.setText('F=[{:.3f}]  Fb=[{:.3f}]'.format(solution.fitness, solution.best_fitness))
        self.paginator.pageChanged(page_id)
        self.displaySolutionDialogBtn.setEnabled(True)

    def _onDisplaySolution(self):
        solution = self.paginator.getCurrentPageModel()
        if solution is not None:
            self.sln_dialog.display(solution)

    def _onClickStart(self):
        self._best_fitness_found = 0.0
        self.gfd = GFDThread(
            profile=self.profile
        )
        self.gfd.solutionReady.connect(self._solutionReady)
        self.gfd.start()
        self.bandsTab.setEnabled(False)
        self.weightControlsTab.setEnabled(False)
        self.startStopButton.setEnabled(False)
        self.stopResetButton.setEnabled(True)
        self.setStatus("Running...")

    def _onClickStop(self):
        self.gfd.stop()
        self.bandsTab.setEnabled(True)
        self.weightControlsTab.setEnabled(True)
        self.startStopButton.setEnabled(True)
        self.stopResetButton.setEnabled(False)
        self.setStatus("Stopped.")

    def _onWeightsChanged(self, weights):
        self.profile.weights = weights
        self.weightsChanged.emit(weights)

    def _onReady(self):
        self.setStatus("Ready.")
        self.show()

    def setStatus(self, message):
        self.statusBar().showMessage(message)


if __name__ == "__main__":
    app = QApplication([])
    widget = GeneticCircuitMainWindow()
    sys.exit(app.exec())
