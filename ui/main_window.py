import os
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFileDialog, QComboBox, QProgressBar, 
    QTextEdit, QCheckBox, QFrame, QMessageBox, QSpacerItem, QSizePolicy, QSystemTrayIcon
)
from .styles import QSS_THEME
from .components import GlowButton, GlowComboBox, AnimatedProgressBar, Toast, RainbowLabel, AnimatedCheckBox, HotkeySelector, SyncPill
from core.backup_engine import BackupEngine
from core.gitignore_handler import GitignoreHandler
from core.startup_manager import StartupManager
from core.settings_manager import SettingsManager
from PyQt6.QtCore import Qt, pyqtSlot, QPoint, pyqtSignal, QTimer
import keyboard
import winsound

class MainWindow(QMainWindow):
    hotkey_trigger = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BackUp Sync")
        self.setFixedSize(600, 820)
        
        # Set Window Icon
        icon_path = os.path.join(os.path.dirname(__file__), "..", "resources", "icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Frameless Window Setup
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet(QSS_THEME)
        
        self.drag_pos = QPoint()
        self.is_pinned = False
        self.source_dir = ""
        self.target_dir = ""
        self.current_hotkey = "ctrl+alt+b"
        self.backup_thread = None
        self.toast = None
        self.sync_pill = None
        self.tray_icon = None # Will be set by main.py
        
        # Connect global hotkey trigger to start backup
        self.hotkey_trigger.connect(self.start_backup)
        
        self.setup_ui()
        self.setup_hotkeys()
        self.load_settings()

    def setup_ui(self):
        # Master Window Frame (Rounded)
        self.window_frame = QWidget()
        self.window_frame.setObjectName("WindowFrame")
        self.setCentralWidget(self.window_frame)
        
        window_layout = QVBoxLayout(self.window_frame)
        window_layout.setContentsMargins(0, 0, 0, 0)
        window_layout.setSpacing(0)

        # Custom Title Bar
        self.title_bar = QWidget()
        self.title_bar.setObjectName("TitleBar")
        self.title_bar.setFixedHeight(45)
        
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(15, 0, 0, 0)
        title_layout.setSpacing(0)
        
        title_label = RainbowLabel("BackUp Sync")
        title_label.setObjectName("TitleLabel")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; background: transparent; border: none;")
        title_layout.addWidget(title_label)
        
        title_layout.addStretch()

        self.pin_btn = QPushButton("📌")
        self.pin_btn.setObjectName("PinButton")
        self.pin_btn.clicked.connect(self.toggle_pin)
        self.pin_btn.setToolTip("Always on Top")
        
        self.min_btn = QPushButton("_")
        self.min_btn.setObjectName("MinimizeButton")
        self.min_btn.clicked.connect(self.showMinimized)
        
        self.close_btn = QPushButton("×")
        self.close_btn.setObjectName("CloseButton")
        self.close_btn.clicked.connect(self.close) 
        
        title_layout.addWidget(self.pin_btn)
        title_layout.addWidget(self.min_btn)
        title_layout.addWidget(self.close_btn)
        
        window_layout.addWidget(self.title_bar)

        # Main Scrollable Content Area
        content_container = QWidget()
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)

        # 1. DIRECTORIES SECTION
        dir_section = QFrame()
        dir_section.setObjectName("SectionFrame")
        dir_layout = QVBoxLayout(dir_section)
        dir_layout.setContentsMargins(15, 15, 15, 15)
        dir_layout.setSpacing(15)

        dir_title = QLabel("Storage Locations")
        dir_title.setObjectName("SectionTitle")
        dir_layout.addWidget(dir_title)

        # Source
        src_vbox = QVBoxLayout()
        src_vbox.setSpacing(5)
        self.source_title = QLabel("Source Directory")
        self.source_title.setObjectName("PathLabel")
        self.source_label = QLabel("Not selected")
        self.source_label.setObjectName("PathValue")
        self.source_label.setWordWrap(True)
        select_source_btn = GlowButton("Browse Source")
        select_source_btn.clicked.connect(self.select_source)
        src_vbox.addWidget(self.source_title)
        src_vbox.addWidget(self.source_label)
        src_vbox.addWidget(select_source_btn)
        dir_layout.addLayout(src_vbox)

        # Target
        tgt_vbox = QVBoxLayout()
        tgt_vbox.setSpacing(5)
        self.target_title = QLabel("Target Directory")
        self.target_title.setObjectName("PathLabel")
        self.target_label = QLabel("Not selected")
        self.target_label.setObjectName("PathValue")
        self.target_label.setWordWrap(True)
        select_target_btn = GlowButton("Browse Target")
        select_target_btn.clicked.connect(self.select_target)
        tgt_vbox.addWidget(self.target_title)
        tgt_vbox.addWidget(self.target_label)
        tgt_vbox.addWidget(select_target_btn)
        dir_layout.addLayout(tgt_vbox)

        content_layout.addWidget(dir_section)

        # 2. CONFIGURATION SECTION
        config_section = QFrame()
        config_section.setObjectName("SectionFrame")
        config_layout = QVBoxLayout(config_section)
        config_layout.setContentsMargins(15, 15, 15, 15)
        config_layout.setSpacing(12)

        config_title = QLabel("Backup configuration")
        config_title.setObjectName("SectionTitle")
        config_layout.addWidget(config_title)

        # Horizontal layout for Mode and Startup
        settings_row = QHBoxLayout()
        
        mode_vbox = QVBoxLayout()
        mode_vbox.setSpacing(5)
        mode_vbox.addWidget(QLabel("Conflict Strategy"))
        self.mode_combo = GlowComboBox()
        self.mode_combo.addItems(["Overwrite", "Skip", "Create", "Smart Sync"])
        self.mode_combo.currentTextChanged.connect(self.save_settings)
        mode_vbox.addWidget(self.mode_combo)
        settings_row.addLayout(mode_vbox, 2)

        settings_row.addSpacing(15)

        startup_vbox = QVBoxLayout()
        startup_vbox.setSpacing(5)
        startup_vbox.addWidget(QLabel("System Startup"))
        self.startup_check = AnimatedCheckBox("Start on Boot")
        self.startup_check.setChecked(StartupManager.is_startup_enabled())
        self.startup_check.toggled.connect(self.toggle_startup)
        startup_vbox.addWidget(self.startup_check)
        settings_row.addLayout(startup_vbox, 1)

        config_layout.addLayout(settings_row)
        
        # Hotkey setting row
        hotkey_row = QHBoxLayout()
        hotkey_row.setSpacing(10)
        hotkey_row.addWidget(QLabel("Global Hotkey:"))
        self.hotkey_btn = HotkeySelector(self.current_hotkey)
        self.hotkey_btn.hotkeyChanged.connect(self.update_hotkey)
        hotkey_row.addWidget(self.hotkey_btn)
        hotkey_row.addStretch()
        config_layout.addLayout(hotkey_row)

        content_layout.addWidget(config_section)

        # 3. FILTERS SECTION
        filter_section = QFrame()
        filter_section.setObjectName("SectionFrame")
        filter_layout = QVBoxLayout(filter_section)
        filter_layout.setContentsMargins(15, 15, 15, 15)
        filter_layout.setSpacing(8)

        filter_title = QLabel("Exclusions & Patterns")
        filter_title.setObjectName("SectionTitle")
        filter_layout.addWidget(filter_title)
        
        self.gitignore_text = QTextEdit()
        self.gitignore_text.setPlaceholderText("Enter .gitignore patterns here (e.g. node_modules/, *.log)")
        self.gitignore_text.setFixedHeight(90)
        self.gitignore_text.textChanged.connect(self.save_settings)
        filter_layout.addWidget(self.gitignore_text)
        
        content_layout.addWidget(filter_section)

        # 4. ACTION SECTION
        action_layout = QVBoxLayout()
        action_layout.setSpacing(10)

        self.progress_bar = AnimatedProgressBar()
        self.progress_bar.hide()
        self.progress_bar.setFixedHeight(12)
        action_layout.addWidget(self.progress_bar)

        self.status_label = QLabel("Ready to sync")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #666666; font-size: 11px;")
        action_layout.addWidget(self.status_label)

        self.backup_btn = GlowButton("BACKUP")
        self.backup_btn.setFixedHeight(50)
        self.backup_btn.clicked.connect(self.start_backup)
        action_layout.addWidget(self.backup_btn)

        # Developer Signature
        footer_layout = QHBoxLayout()
        footer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_layout.setSpacing(2)
        
        dev_by = QLabel("Developed By ")
        dev_by.setStyleSheet("color: #666666; font-size: 11px; background: transparent;")
        
        signature = RainbowLabel("R ! Y 4 Z", url="https://riyazz.dev")
        signature.setStyleSheet("font-size: 11px; font-weight: bold; background: transparent; border: none;")
        
        footer_layout.addWidget(dev_by)
        footer_layout.addWidget(signature)
        action_layout.addLayout(footer_layout)
        
        content_layout.addLayout(action_layout)
        
        window_layout.addWidget(content_container)

    # Mouse Events for Dragging
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Only drag if clicking title bar
            if self.title_bar.underMouse():
                self.drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
                event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            if self.title_bar.underMouse() or not self.drag_pos.isNull():
                self.move(event.globalPosition().toPoint() - self.drag_pos)
                event.accept()

    def mouseReleaseEvent(self, event):
        self.drag_pos = QPoint()

    def toggle_pin(self):
        self.is_pinned = not self.is_pinned
        if self.is_pinned:
            self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
            self.pin_btn.setText("📍")
            self.pin_btn.setStyleSheet("color: #00FF41;") # Highlight when pinned
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowStaysOnTopHint)
            self.pin_btn.setText("📌")
            self.pin_btn.setStyleSheet("color: #888888;")
        
        # After changing flags, we must show the window again
        self.show()

    def select_source(self):
        path = QFileDialog.getExistingDirectory(self, "Select Source Directory")
        if path:
            self.source_dir = path
            self.source_label.setText(path)
            gi_text = GitignoreHandler.detect_and_load(path)
            if gi_text:
                self.gitignore_text.setPlainText(gi_text)
                self.status_label.setText("Detected .gitignore in source.")
            self.save_settings()

    def select_target(self):
        path = QFileDialog.getExistingDirectory(self, "Select Target Directory")
        if path:
            self.target_dir = path
            self.target_label.setText(path)
            self.save_settings()

    @pyqtSlot()
    def toggle_startup(self):
        enabled = self.startup_check.isChecked()
        StartupManager.set_startup(enabled)

    def start_backup(self):
        if not self.source_dir or not self.target_dir:
            QMessageBox.critical(self, "Error", "Select source and target directories.")
            return

        if self.backup_thread and self.backup_thread.isRunning():
            self.backup_thread.stop()
            self.backup_btn.setText("START BACKUP")
            return

        self.backup_btn.setText("STOP BACKUP")
        self.progress_bar.show()
        
        # Use Native Notification for Start
        if hasattr(self, 'tray_icon') and self.tray_icon:
            self.tray_icon.showMessage("Backup Started 🚀", "Syncing files in the background...", QSystemTrayIcon.MessageIcon.Information, 3000)
        
        # Show SyncPill for Realtime progress
        if not self.sync_pill:
            self.sync_pill = SyncPill()
        self.sync_pill.update_progress(0, "Scanning...", 0, 0, 0.0)
        self.sync_pill.show()
        
        handler = GitignoreHandler()
        handler.add_patterns(self.gitignore_text.toPlainText())
        
        self.backup_thread = BackupEngine(
            self.source_dir, 
            self.target_dir, 
            handler, 
            self.mode_combo.currentText()
        )
        self.backup_thread.progress.connect(self.update_progress)
        self.backup_thread.finished.connect(self.on_backup_finished)
        self.backup_thread.start()

    def update_progress(self, val, msg, current, total, size_mb):
        # Update Main UI
        self.progress_bar.setValue(val)
        self.status_label.setText(f"[{current}/{total}] {msg}")
        
        # Update SyncPill Realtime
        if self.sync_pill:
            self.sync_pill.update_progress(val, msg, current, total, size_mb)

    def on_backup_finished(self, success, msg, stats):
        if self.sync_pill:
            self.sync_pill.finish()
            
        self.backup_btn.setText("START BACKUP")
        self.progress_bar.hide()
        self.status_label.setText(msg)
        
        if success:
            files = stats.get("total_files", 0)
            size_mb = stats.get("total_size", 0) / (1024 * 1024)
            duration = stats.get("elapsed_time", 0)
            speed = stats.get("speed", 0)
            
            detail_msg = (
                f"Processed {files} files ({size_mb:.2f} MB)\n"
                f"Time: {duration:.1f}s | Speed: {speed:.2f} MB/s"
            )
            
            # Play Success Sound (Windows System Sound)
            try:
                winsound.MessageBeep(winsound.MB_ICONASTERISK)
            except:
                pass
            
            if hasattr(self, 'tray_icon') and self.tray_icon:
                self.tray_icon.showMessage("Backup Successful! ✅", detail_msg, QSystemTrayIcon.MessageIcon.Information, 5000)
            
            # Optionally still show success toast if preferred, but tray is 100% reliable
            self.toast = Toast("Backup Successful! ✅", detail_msg)
            self.toast.show_toast()
        else:
            if self.tray_icon:
                self.tray_icon.showMessage("Backup Failed! ❌", msg, QSystemTrayIcon.MessageIcon.Critical, 5000)
            QMessageBox.critical(self, "Error", msg)

    def update_hotkey(self, new_hotkey):
        self.current_hotkey = new_hotkey
        self.setup_hotkeys()
        self.save_settings()
        self.status_label.setText(f"Hotkey updated to: {new_hotkey.upper()}")

    def setup_hotkeys(self):
        try:
            # Unregister all previously registered hotkeys to avoid conflicts
            keyboard.unhook_all()
            # Register the new hotkey
            keyboard.add_hotkey(self.current_hotkey, lambda: self.hotkey_trigger.emit())
        except Exception as e:
            print(f"Failed to register global hotkey: {e}")

    def save_settings(self, *args):
        data = {
            "source_dir": self.source_dir,
            "target_dir": self.target_dir,
            "conflict_strategy": self.mode_combo.currentText(),
            "gitignore_text": self.gitignore_text.toPlainText(),
            "hotkey": self.current_hotkey
        }
        SettingsManager.save_settings(data)

    def load_settings(self):
        data = SettingsManager.load_settings()
        if data:
            self.source_dir = data.get("source_dir", "")
            self.target_dir = data.get("target_dir", "")
            self.current_hotkey = data.get("hotkey", "ctrl+alt+b")
            
            self.source_label.setText(self.source_dir if self.source_dir else "Not selected")
            self.target_label.setText(self.target_dir if self.target_dir else "Not selected")
            
            self.hotkey_btn.current_hotkey = self.current_hotkey
            self.hotkey_btn.setText(self.current_hotkey.upper())
            
            strategy = data.get("conflict_strategy", "Overwrite")
            index = self.mode_combo.findText(strategy)
            if index >= 0:
                self.mode_combo.setCurrentIndex(index)
            
            gi_text = data.get("gitignore_text", "")
            self.gitignore_text.setPlainText(gi_text)
            
            # Repopulate hotkey in keyboard handler
            self.setup_hotkeys()

    def closeEvent(self, event):
        # This will be overridden by main.py to handle minimize to tray
        pass
