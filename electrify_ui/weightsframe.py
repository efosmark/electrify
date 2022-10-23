from electrify_ui.namedslider import NamedSlider
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Signal


WEIGHT_TITLES = {
    "pb_avg": "PB Average",
    "pb_range": "PB Range",
    "sb_avg": "SB Average",
    "sb_range": "SB Range",
    "sim_time": "Sim Time",
    "num_elements": "# Elements",
    "phase_avg": "Phase Avg",
    "phase_shift": "Phase Shift"
}


class WeightsFrame(QFrame):
    weightsChanged = Signal(object)

    def __init__(self, parent=None):
        QFrame.__init__(self, parent=parent)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

    def setWeights(self, weights):
        self._weights = weights
        for field, value in self._weights.items():
            self._weights[field] = value
            selector = NamedSlider(parent=self)
            selector.configure(field, WEIGHT_TITLES.get(field, field), value)
            selector.valueChanged.connect(self._onWeightValueChanged)
            self.verticalLayout.addWidget(selector)

    def _onWeightValueChanged(self, field, value):
        self._weights[field] = value
        self.weightsChanged.emit(self._weights)
