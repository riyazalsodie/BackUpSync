QSS_THEME = """
QMainWindow {
    background-color: transparent;
}

QWidget#WindowFrame {
    background-color: #000000;
    border: 1px solid #1A1A1A;
    border-radius: 15px;
}

QWidget#TitleBar {
    background-color: #0A0A0A;
    border-top-left-radius: 15px;
    border-top-right-radius: 15px;
    border-bottom: 1px solid #1A1A1A;
}

QLabel#TitleLabel {
    color: #00FF41;
    font-weight: bold;
    font-size: 14px;
    margin-left: 15px;
}

QPushButton#MinimizeButton, QPushButton#CloseButton, QPushButton#PinButton {
    background-color: transparent;
    border: none;
    border-radius: 0px;
    color: #888888;
    font-weight: bold;
    font-size: 14px;
    min-width: 45px;
    max-width: 45px;
    min-height: 45px;
    max-height: 45px;
    padding: 0px;
}

QPushButton#MinimizeButton:hover, QPushButton#PinButton:hover {
    background-color: #1A1A1A;
    color: #FFFFFF;
}

QPushButton#CloseButton {
    border-top-right-radius: 15px; /* Match window frame radius */
    font-size: 18px;
    font-weight: normal;
}

QPushButton#CloseButton:hover {
    background-color: #E81123;
    color: #FFFFFF;
    border-top-right-radius: 15px;
}

QWidget {
    background-color: transparent;
    color: #FFFFFF;
    font-family: 'JetBrains Mono', 'Consolas', monospace;
    font-size: 14px;
    font-weight: 500;
}

QFrame#container {
    background-color: transparent;
}

QFrame#SectionFrame {
    background-color: #050505;
    border: 1px solid #1A1A1A;
    border-radius: 12px;
}

QLabel#SectionTitle {
    color: #888888;
    font-weight: bold;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 5px;
}

QLabel {
    background: transparent;
    color: #BBBBBB;
}

QLabel#PathLabel {
    color: #E0E0E0;
    font-weight: 500;
    font-size: 13px;
}

QLabel#PathValue {
    color: #00FF41;
    font-weight: bold;
    font-family: 'JetBrains Mono', 'Consolas', monospace;
    font-size: 12px;
    background-color: #0A0A0A;
    border: 1px solid #1A1A1A;
    border-radius: 6px;
    padding: 8px;
}

QLabel#title {
    font-size: 24px;
    font-weight: bold;
    color: #00FF41;
}

QPushButton {
    background-color: #0A0A0A;
    border: 1px solid #1A1A1A;
    border-radius: 10px;
    padding: 12px 24px;
    font-weight: 600;
    color: #E0E0E0;
    min-width: 100px;
    letter-spacing: 0.5px;
}

QPushButton:hover {
    border: 1px solid #00FF41;
    color: #FFFFFF;
}

QPushButton:pressed {
    background-color: #00CC33;
    border-color: #00CC33;
}

QPushButton#secondary {
    border-color: #333333;
    color: #888888;
}

QPushButton#secondary:hover {
    background-color: #333333;
    color: #FFFFFF;
}

QLineEdit {
    background-color: #121212;
    border: 1px solid #222222;
    border-radius: 8px;
    padding: 8px;
    color: #FFFFFF;
}

QLineEdit:focus {
    border: 1px solid #00FF41;
}

QComboBox {
    background-color: #0A0A0A;
    border: 1px solid #1A1A1A;
    border-radius: 10px;
    padding: 10px 15px;
    color: #E0E0E0;
    min-width: 150px;
    font-weight: 500;
}

QComboBox:hover {
    border: 1px solid #333333;
}

QComboBox:focus {
    border: 1px solid #00FF41;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 30px;
    border-left: none;
}

QComboBox::down-arrow {
    image: none;
    width: 8px;
    height: 8px;
    background-color: #00FF41;
    border-radius: 4px;
    border: 2px solid #005014; /* Darker green ring for "glow" contrast */
    margin-top: 0px;
}

QComboBox QAbstractItemView {
    background-color: #0A0A0A;
    border: 1px solid #1A1A1A;
    border-radius: 0px;
    selection-background-color: #00FF41;
    selection-color: #000000;
    outline: none;
}

QComboBox QAbstractItemView::item {
    padding: 10px;
    min-height: 30px;
    color: #E0E0E0;
}

QComboBox QAbstractItemView::item:selected {
    background-color: #00FF41;
    color: #000000;
}

QProgressBar {
    background-color: #0A0A0A;
    border: 1px solid #1A1A1A;
    border-radius: 12px;
    text-align: center;
    color: transparent; /* We'll use a custom label for progress text for better control */
    height: 24px;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #008F24, stop:0.5 #00FF41, stop:1 #008F24);
    border-radius: 11px;
    border: 1px solid #00FF41;
}

QTextEdit {
    background-color: #0A0A0A;
    border: 1px solid #222222;
    border-radius: 10px;
    color: #00FF41;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
}

QCheckBox {
    spacing: 10px;
}

QCheckBox::indicator {
    width: 20px;
    height: 20px;
}

QCheckBox::indicator:unchecked {
    border: 1px solid #333333;
    background: #111111;
    border-radius: 4px;
}

QCheckBox::indicator:checked {
    border: 1px solid #00FF41;
    background: #00FF41;
    border-radius: 4px;
}

/* Custom ScrollBar Styling */
QScrollBar:vertical {
    border: none;
    background: #050505;
    width: 12px;
    margin: 0px 0px 0px 0px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #00FF41, stop:1 #008F24);
    min-height: 25px;
    border-radius: 6px;
    border: 1px solid #005014;
}

QScrollBar::handle:vertical:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #33FF6B, stop:1 #00CC33);
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}

QScrollBar:horizontal {
    border: none;
    background: #050505;
    height: 12px;
    margin: 0px 0px 0px 0px;
    border-radius: 6px;
}

QScrollBar::handle:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00FF41, stop:1 #008F24);
    min-width: 25px;
    border-radius: 6px;
    border: 1px solid #005014;
}

QScrollBar::handle:horizontal:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #33FF6B, stop:1 #00CC33);
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: none;
}

/* QMenu (Tray Menu) Styling */
QMenu {
    background-color: #0A0A0A;
    border: 1px solid #1A1A1A;
    border-radius: 8px;
    padding: 5px;
    font-family: 'JetBrains Mono';
}

QMenu::item {
    background-color: transparent;
    padding: 10px 30px;
    color: #BBBBBB;
    border-radius: 5px;
    margin: 2px;
}

QMenu::item:selected {
    background-color: #00FF41;
    color: #000000;
    font-weight: bold;
}

QMenu::separator {
    height: 1px;
    background: #1A1A1A;
    margin: 5px 10px;
}

QMenu::indicator {
    width: 13px;
    height: 13px;
}
"""
