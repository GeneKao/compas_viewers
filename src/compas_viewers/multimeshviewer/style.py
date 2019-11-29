STYLE = """
QMainWindow {}

QDockWidget#Sidebar {
}

QGroupBox, QSlider, QLabel, QDockWidget {
background-color: rgba(255, 255, 255, 0.0);
}

QGroupBox, QSlider, QLabel, QLineEdit, QColorButton {
margin: 0;
padding: 0;
border: 0;
}

QGroupBox {
    border-bottom: 1px solid white;
    padding-top: 12px;
    padding-bottom: 12px;
    padding-left: 12px;
    padding-right: 12px;
}

QSlider::groove:horizontal {
    border: 1px solid #999999;
    height: 2px;
    background-color: #999999;
}

QSlider::handle:horizontal {
    background-color: #333333;
    border: 1px solid #333333;
    width: 3px;
    margin: -4px 0;
}

"""
