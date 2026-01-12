from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QFont

# fonts definition
title_font = QFont("Inter")
title_font.setWeight(QFont.Weight.Bold)
title_font.setPointSize(20)

sub_font = QFont("Inter")
sub_font.setWeight(QFont.Weight.Medium)
sub_font.setPointSize(14)

third_font = QFont("Inter")
third_font.setWeight(QFont.Weight.Normal)
third_font.setPointSize(12)

styles = {
    1: title_font,
    2: sub_font,
    3: third_font,
}

class Title(QLabel):
    def __init__(self, text, size):
        super().__init__(text)
        self.setFont(styles[size])
