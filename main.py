import sys
import os
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    from ui.styles import QSS_THEME
    app.setStyleSheet(QSS_THEME)
    app.setQuitOnLastWindowClosed(False)

    window = MainWindow()

    # System Tray Setup
    tray_icon = QSystemTrayIcon(parent=window)
    window.tray_icon = tray_icon
    
    # Use a standard icon if local icon not found
    icon_path = os.path.join(os.path.dirname(__file__), "resources", "icon.png")
    if os.path.exists(icon_path):
        tray_icon.setIcon(QIcon(icon_path))
    else:
        # Fallback to a system standard icon
        tray_icon.setIcon(window.style().standardIcon(window.style().StandardPixmap.SP_DriveHDIcon))

    tray_menu = QMenu()
    
    show_action = QAction("Open BackUp Sync", window)
    show_action.triggered.connect(window.showNormal)
    show_action.triggered.connect(window.activateWindow)
    
    quit_action = QAction("Exit", window)
    quit_action.triggered.connect(app.quit)
    
    tray_menu.addAction(show_action)
    tray_menu.addSeparator()
    tray_menu.addAction(quit_action)
    
    tray_icon.setContextMenu(tray_menu)
    tray_icon.setToolTip("BackUp Sync")
    
    # Handle Double Click to Restore
    def on_tray_activated(reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            window.showNormal()
            window.activateWindow()
            window.raise_()

    tray_icon.activated.connect(on_tray_activated)
    tray_icon.show()

    # Handle window close to minimize to tray
    def on_close(event):
        if tray_icon.isVisible():
            window.hide()
            tray_icon.showMessage(
                "BackUp Sync",
                "Application is still running in the system tray.",
                QSystemTrayIcon.MessageIcon.Information,
                2000
            )
            event.ignore()

    window.closeEvent = on_close

    # Check if started minimized
    if "--minimized" not in sys.argv:
        window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
