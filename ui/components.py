from PyQt6.QtWidgets import QPushButton, QComboBox, QGraphicsDropShadowEffect, QProgressBar, QLabel, QWidget, QVBoxLayout, QAbstractButton, QApplication
from PyQt6.QtCore import QPropertyAnimation, pyqtProperty, QEasingCurve, Qt, QRectF, QPointF, QPoint, QTimer, QRect, pyqtSignal
from PyQt6.QtGui import QColor, QPainter, QRadialGradient, QBrush, QPen, QScreen, QLinearGradient

import webbrowser
import random

class RainbowLabel(QLabel):
    def __init__(self, text, parent=None, url=None):
        super().__init__(text, parent)
        self.url = url
        self._hue = 0.0
        self._speed = 0.005
        self._base_style = ""
        self._is_hovering = False
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(30)
        
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setOffset(0, 0)
        self.setGraphicsEffect(self.shadow)
        
        if self.url:
            self.setCursor(Qt.CursorShape.PointingHandCursor)

    def enterEvent(self, event):
        self._is_hovering = True
        self._speed = 0.015 
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._is_hovering = False
        self._speed = 0.005
        self.update() # Ensure final paint is clean
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if self.url and event.button() == Qt.MouseButton.LeftButton:
            webbrowser.open(self.url)
        super().mousePressEvent(event)

    def paintEvent(self, event):
        if self._is_hovering and random.random() > 0.8:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            # Main color from palette
            main_color = self.palette().color(self.foregroundRole())
            rect = self.rect()
            
            # Glitch layer 1 (Cyan)
            if random.random() > 0.5:
                painter.setOpacity(0.6)
                painter.setPen(QColor(0, 255, 255))
                painter.drawText(rect.adjusted(random.randint(-3, 3), 0, 0, 0), self.alignment(), self.text())
            
            # Glitch layer 2 (Magenta)
            if random.random() > 0.5:
                painter.setOpacity(0.6)
                painter.setPen(QColor(255, 0, 255))
                painter.drawText(rect.adjusted(random.randint(-3, 3), 0, 0, 0), self.alignment(), self.text())
            
            # Original text with slight jitter
            painter.setOpacity(1.0)
            painter.setPen(main_color)
            painter.drawText(rect.adjusted(random.randint(-1, 1), 0, 0, 0), self.alignment(), self.text())
            painter.end()
        else:
            super().paintEvent(event)

    def setStyleSheet(self, style):
        self._base_style = style
        super().setStyleSheet(style)

    def animate(self):
        self._hue += self._speed
        if self._hue > 1.0:
            self._hue = 0.0
        
        color = QColor.fromHslF(self._hue, 1.0, 0.6)
        self.shadow.setColor(color)
        
        color_style = f"color: {color.name()};"
        super().setStyleSheet(self._base_style + color_style)


class GlowButton(QPushButton):
    def __init__(self, text, parent=None, glow_color="#00FF41"):
        super().__init__(text, parent)
        self.glow_color = QColor(glow_color)
        self._inner_glow = 0.0
        self._click_scale = 1.0
        
        # Setup outer shadow effect
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(0)
        self.shadow.setOffset(0, 0)
        self.shadow.setColor(self.glow_color)
        self.setGraphicsEffect(self.shadow)
        
        # Setup outer animation
        self.outer_anim = QPropertyAnimation(self, b"blurRadius")
        self.outer_anim.setDuration(300)
        self.outer_anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        
        # Setup inner animation
        self.inner_anim = QPropertyAnimation(self, b"innerGlow")
        self.inner_anim.setDuration(300)
        self.inner_anim.setEasingCurve(QEasingCurve.Type.OutQuad)

        # Setup click animation
        self.click_anim = QPropertyAnimation(self, b"clickScale")
        self.click_anim.setDuration(100)
        self.click_anim.setEasingCurve(QEasingCurve.Type.OutQuad)

    @pyqtProperty(float)
    def blurRadius(self):
        return self.shadow.blurRadius()

    @blurRadius.setter
    def blurRadius(self, value):
        self.shadow.setBlurRadius(value)

    @pyqtProperty(float)
    def innerGlow(self):
        return self._inner_glow

    @innerGlow.setter
    def innerGlow(self, value):
        self._inner_glow = value
        self.update()

    @pyqtProperty(float)
    def clickScale(self):
        return self._click_scale

    @clickScale.setter
    def clickScale(self, value):
        self._click_scale = value
        self.update()

    def enterEvent(self, event):
        self.outer_anim.stop()
        self.outer_anim.setEndValue(25)
        self.outer_anim.start()
        
        self.inner_anim.stop()
        self.inner_anim.setEndValue(1.0)
        self.inner_anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.outer_anim.stop()
        self.outer_anim.setEndValue(0)
        self.outer_anim.start()
        
        self.inner_anim.stop()
        self.inner_anim.setEndValue(0.0)
        self.inner_anim.start()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self.click_anim.stop()
        self.click_anim.setEndValue(0.96)
        self.click_anim.start()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.click_anim.stop()
        self.click_anim.setEndValue(1.0)
        self.click_anim.start()
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Apply click scaling from center
        if self._click_scale != 1.0:
            center = self.rect().center()
            painter.translate(QPointF(center))
            painter.scale(self._click_scale, self._click_scale)
            painter.translate(-QPointF(center))

        # We must draw the button manually now because super().paintEvent(event)
        # would draw it unscaled or cause clipping issues with the painter state transformation.
        # However, to keep it simple, we can just let QPushButton draw into our transformed painter
        # by passing the painter to the style engine.
        
        # Actually, let's draw a professional custom button background first
        rect = QRectF(self.rect())
        
        # Draw background
        painter.setBrush(QBrush(QColor("#0A0A0A")))
        painter.setPen(QPen(QColor("#1A1A1A"), 1))
        if self.underMouse():
            painter.setPen(QPen(QColor("#00FF41"), 1))
        painter.drawRoundedRect(rect, 10, 10)

        # Draw inner glow
        if self._inner_glow > 0:
            gradient = QRadialGradient(QPointF(rect.center()), max(rect.width(), rect.height()) / 2)
            color = QColor(self.glow_color)
            color.setAlpha(int(60 * self._inner_glow))
            gradient.setColorAt(0, QColor(0, 0, 0, 0))
            gradient.setColorAt(0.7, QColor(0, 0, 0, 0))
            gradient.setColorAt(1, color)
            painter.setBrush(QBrush(gradient))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(rect, 10, 10)

        # Draw text
        painter.setPen(QColor("#FFFFFF") if self.underMouse() else QColor("#E0E0E0"))
        painter.setFont(self.font())
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.text())
        
        painter.end()

class GlowComboBox(QComboBox):
    def __init__(self, parent=None, glow_color="#00FF41"):
        super().__init__(parent)
        self.glow_color = QColor(glow_color)
        self._inner_glow = 0.0
        self._click_scale = 1.0
        
        # Setup outer shadow effect
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(0)
        self.shadow.setOffset(0, 0)
        self.shadow.setColor(self.glow_color)
        self.setGraphicsEffect(self.shadow)
        
        # Setup outer animation
        self.outer_anim = QPropertyAnimation(self, b"blurRadius")
        self.outer_anim.setDuration(300)
        self.outer_anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        
        # Setup inner animation
        self.inner_anim = QPropertyAnimation(self, b"innerGlow")
        self.inner_anim.setDuration(300)
        self.inner_anim.setEasingCurve(QEasingCurve.Type.OutQuad)

        # Setup click animation
        self.click_anim = QPropertyAnimation(self, b"clickScale")
        self.click_anim.setDuration(100)
        self.click_anim.setEasingCurve(QEasingCurve.Type.OutQuad)

    @pyqtProperty(float)
    def blurRadius(self):
        return self.shadow.blurRadius()

    @blurRadius.setter
    def blurRadius(self, value):
        self.shadow.setBlurRadius(value)

    @pyqtProperty(float)
    def innerGlow(self):
        return self._inner_glow

    @innerGlow.setter
    def innerGlow(self, value):
        self._inner_glow = value
        self.update()

    @pyqtProperty(float)
    def clickScale(self):
        return self._click_scale

    @clickScale.setter
    def clickScale(self, value):
        self._click_scale = value
        self.update()

    def enterEvent(self, event):
        self.outer_anim.stop()
        self.outer_anim.setEndValue(25)
        self.outer_anim.start()
        
        self.inner_anim.stop()
        self.inner_anim.setEndValue(1.0)
        self.inner_anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.outer_anim.stop()
        self.outer_anim.setEndValue(0)
        self.outer_anim.start()
        
        self.inner_anim.stop()
        self.inner_anim.setEndValue(0.0)
        self.inner_anim.start()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self.click_anim.stop()
        self.click_anim.setEndValue(0.97)
        self.click_anim.start()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.click_anim.stop()
        self.click_anim.setEndValue(1.0)
        self.click_anim.start()
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Apply click scaling from center
        if self._click_scale != 1.0:
            center = self.rect().center()
            painter.translate(QPointF(center))
            painter.scale(self._click_scale, self._click_scale)
            painter.translate(-QPointF(center))

        rect = QRectF(self.rect())
        
        # Draw background
        painter.setBrush(QBrush(QColor("#0A0A0A")))
        painter.setPen(QPen(QColor("#1A1A1A"), 1))
        if self.underMouse() or self.hasFocus():
            painter.setPen(QPen(QColor("#00FF41"), 1))
        painter.drawRoundedRect(rect, 10, 10)

        # Draw inner glow
        if self._inner_glow > 0:
            gradient = QRadialGradient(QPointF(rect.center()), max(rect.width(), rect.height()) / 2)
            color = QColor(self.glow_color)
            color.setAlpha(int(60 * self._inner_glow))
            gradient.setColorAt(0, QColor(0, 0, 0, 0))
            gradient.setColorAt(0.7, QColor(0, 0, 0, 0))
            gradient.setColorAt(1, color)
            painter.setBrush(QBrush(gradient))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(rect, 10, 10)

        # Draw arrow
        arrow_color = QColor("#00FF41")
        arrow_x = rect.width() - 20
        arrow_y = rect.height() / 2
        
        painter.setBrush(QBrush(arrow_color))
        painter.setPen(QPen(QColor("#005014"), 1))
        painter.drawEllipse(QPointF(arrow_x, arrow_y), 4, 4)

        # Draw current text
        text_rect = rect.adjusted(15, 0, -35, 0)
        painter.setPen(QColor("#FFFFFF") if self.underMouse() else QColor("#E0E0E0"))
        painter.setFont(self.font())
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, self.currentText())
        
        painter.end()


class AnimatedCheckBox(QAbstractButton):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setText(text)
        self.setCheckable(True)
        self._checked_ratio = 0.0
        self.setMinimumHeight(30)
        
        self.anim = QPropertyAnimation(self, b"checkedRatio")
        self.anim.setDuration(300)
        self.anim.setEasingCurve(QEasingCurve.Type.OutBack)
        
        self.toggled.connect(self.start_anim)

    @pyqtProperty(float)
    def checkedRatio(self):
        return self._checked_ratio
        
    @checkedRatio.setter
    def checkedRatio(self, v):
        self._checked_ratio = v
        self.update()

    def start_anim(self, checked):
        self.anim.stop()
        self.anim.setEndValue(1.0 if checked else 0.0)
        self.anim.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Box geometry
        box_size = 18
        box_y = (self.height() - box_size) / 2
        box_rect = QRectF(0, box_y, box_size, box_size)
        
        # Draw border box
        painter.setPen(QPen(QColor("#00FF41" if self.isChecked() else "#333333"), 1.2))
        painter.setBrush(QBrush(QColor("#080808")))
        painter.drawRoundedRect(box_rect, 5, 5)
        
        # Draw glowing dot
        if self._checked_ratio > 0:
            center = box_rect.center()
            dot_radius = (box_size / 4) * self._checked_ratio
            
            # Dot glow
            grad = QRadialGradient(center, dot_radius * 2.8)
            grad.setColorAt(0, QColor(0, 255, 65, int(200 * self._checked_ratio)))
            grad.setColorAt(1, QColor(0, 255, 65, 0))
            
            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(center, dot_radius * 2.8, dot_radius * 2.8)
            
            # Center bright dot
            painter.setBrush(QBrush(QColor("#00FF41")))
            painter.drawEllipse(center, dot_radius, dot_radius)

        # Draw text
        painter.setPen(QColor("#FFFFFF") if self.underMouse() else QColor("#BBBBBB"))
        painter.setFont(self.font())
        text_rect = self.rect().adjusted(box_size + 12, 0, 0, 0)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, self.text())
        
        painter.end()


class AnimatedProgressBar(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._value = 0
        self.setFormat("%p%")
        self.setFixedHeight(24)
        
        # Smooth animation for value changes
        self.anim = QPropertyAnimation(self, b"animatedValue")
        self.anim.setDuration(600)
        self.anim.setEasingCurve(QEasingCurve.Type.OutExpo)

        # Pulse effect for "active" feeling
        self._pulse = 0.0
        self.pulse_anim = QPropertyAnimation(self, b"pulse")
        self.pulse_anim.setDuration(1500)
        self.pulse_anim.setStartValue(0.0)
        self.pulse_anim.setEndValue(1.0)
        self.pulse_anim.setLoopCount(-1)
        self.pulse_anim.start()

    @pyqtProperty(float)
    def pulse(self):
        return self._pulse
    
    @pulse.setter
    def pulse(self, v):
        self._pulse = v
        self.update()

    @pyqtProperty(int)
    def animatedValue(self):
        return self._value

    @animatedValue.setter
    def animatedValue(self, value):
        self._value = value
        super().setValue(value)

    def setValue(self, value):
        if value == self._value:
            return
        self.anim.stop()
        self.anim.setEndValue(value)
        self.anim.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        radius = rect.height() / 2
        
        # 1. Draw Background
        painter.setPen(QPen(QColor("#1A1A1A"), 1))
        painter.setBrush(QBrush(QColor("#0A0A0A")))
        painter.drawRoundedRect(rect, radius, radius)
        
        # 2. Draw Progress Chunk
        if self.maximum() > 0:
            progress = self.value() / self.maximum()
            if progress > 0:
                inner_rect = rect.adjusted(2, 2, -2, -2)
                progress_width = progress * inner_rect.width()
                
                # Clip the progress drawing to the rounded bar area
                chunk_rect = QRectF(inner_rect.left(), inner_rect.top(), progress_width, inner_rect.height())
                
                # Gradient for the chunk
                chunk_grad = QLinearGradient(chunk_rect.left(), 0, chunk_rect.right(), 0)
                chunk_grad.setColorAt(0, QColor("#008F24"))
                chunk_grad.setColorAt(0.5, QColor("#00FF41"))
                chunk_grad.setColorAt(1, QColor("#008F24"))
                
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(QBrush(chunk_grad))
                
                # To keep it perfectly rounded even at low progress, we use a rounded rect
                # but we need to handle the case where width < height
                chunk_radius = chunk_rect.height() / 2
                painter.drawRoundedRect(chunk_rect, chunk_radius, chunk_radius)

                # 3. Draw Shimmer / Pulse
                shimmer_pos = (self._pulse * progress_width)
                shimmer_width = min(80.0, progress_width)
                
                shimmer_rect = QRectF(chunk_rect.left() + shimmer_pos - shimmer_width/2, chunk_rect.top(), shimmer_width, chunk_rect.height())
                
                # Only draw if it's within the chunk
                visible_shimmer = shimmer_rect.intersected(chunk_rect)
                if visible_shimmer.width() > 0:
                    shimmer_grad = QLinearGradient(visible_shimmer.left(), 0, visible_shimmer.right(), 0)
                    shimmer_grad.setColorAt(0, QColor(255, 255, 255, 0))
                    shimmer_grad.setColorAt(0.5, QColor(255, 255, 255, 60))
                    shimmer_grad.setColorAt(1, QColor(255, 255, 255, 0))
                    
                    painter.setBrush(QBrush(shimmer_grad))
                    painter.drawRoundedRect(visible_shimmer, chunk_radius, chunk_radius)

        # 4. Draw Percentage Text
        painter.setPen(QColor("#FFFFFF"))
        font = self.font()
        font.setBold(True)
        font.setPointSize(9)
        painter.setFont(font)
        
        text = f"{self.value()}%"
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, text)
        
        painter.end()

class Toast(QWidget):
    def __init__(self, title, message="", parent=None, is_success=True):
        super().__init__(None) # Toast is a top-level window
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.is_sticky = False
        self.is_closing = False
        self.is_success = is_success
        self.title = title
        self.message = message
        self.current_state = is_success # Track state for optimization
        
        # Layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        
        self.frame = QWidget()
        self.frame.setObjectName("ToastFrame")
        self.frame_layout = QVBoxLayout(self.frame)
        self.frame_layout.setContentsMargins(15, 10, 15, 10)
        self.frame_layout.setSpacing(2)
        
        title_label = QLabel(title)
        self.title_label = title_label
        title_label.setStyleSheet("color: white; font-weight: bold; font-size: 15px; background: transparent;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.frame_layout.addWidget(title_label)
        
        if message:
            msg_label = QLabel(message)
            self.msg_label = msg_label
            msg_label.setStyleSheet("color: #BBBBBB; font-size: 12px; background: transparent;")
            msg_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            msg_label.setWordWrap(True)
            self.frame_layout.addWidget(msg_label)
        else:
            self.msg_label = None
        
        self.layout.addWidget(self.frame)
        
        # Style
        border_color = "#00FF41" if is_success else "#FF3131"
        bg_color = "#0D0D0D"
        
        self.frame.setStyleSheet(f"""
            QWidget#ToastFrame {{
                background-color: {bg_color};
                border: 1px solid {border_color};
                border-radius: 12px;
            }}
        """)
        
        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(4)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: rgba(255, 255, 255, 0.1);
                border: none;
                border-radius: 2px;
            }}
            QProgressBar::chunk {{
                background-color: {border_color};
                border-radius: 2px;
            }}
        """)
        self.progress_bar.hide()
        self.frame_layout.addSpacing(5)
        self.frame_layout.addWidget(self.progress_bar)
        
        # Glow Shadow
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(25)
        self.shadow.setColor(QColor(0, 255, 65, 80) if is_success else QColor(255, 49, 49, 80))
        self.shadow.setOffset(0, 0)
        self.frame.setGraphicsEffect(self.shadow)
        
        # Adjustable size based on content
        width = 320
        height = 95 if message else 70
        self.setFixedSize(width, height)
        
        # Position Setup (Top Right)
        screen = QScreen.availableGeometry(self.screen())
        self.start_x = screen.width()  # Start off-screen right
        self.end_x = screen.width() - width - 20
        self.y_pos = 40
        
        self.move(self.start_x, self.y_pos)
        
        # Animation
        self.pos_anim = QPropertyAnimation(self, b"pos")
        self.pos_anim.setDuration(600)
        self.pos_anim.setEasingCurve(QEasingCurve.Type.OutExpo)
        
        # Timer for auto-close
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.slide_out)
        self.timer.setSingleShot(True)
        
    def set_sticky(self, sticky):
        self.is_sticky = sticky
        if sticky:
            self.timer.stop()
        else:
            self.timer.start(4000)

    def show_toast(self):
        self.show()
        self.pos_anim.setStartValue(QPoint(self.start_x, self.y_pos))
        self.pos_anim.setEndValue(QPoint(self.end_x, self.y_pos))
        self.pos_anim.start()
        self.timer.start(4000) # Show for 4 seconds

    def update_content(self, title, message="", is_success=True, duration=4000, progress=-1):
        self.title_label.setText(title)
        if self.msg_label:
            self.msg_label.setText(message)
        
        # Only update styling if state changed (Performance optimization)
        if is_success != self.current_state:
            self.current_state = is_success
            border_color = "#00FF41" if is_success else "#FF3131"
            self.frame.setStyleSheet(f"""
                QWidget#ToastFrame {{
                    background-color: #0D0D0D;
                    border: 1px solid {border_color};
                    border-radius: 12px;
                }}
            """)
            
            self.progress_bar.setStyleSheet(f"""
                QProgressBar {{
                    background-color: rgba(255, 255, 255, 0.1);
                    border: none;
                    border-radius: 2px;
                }}
                QProgressBar::chunk {{
                    background-color: {border_color};
                    border-radius: 2px;
                }}
            """)
            # Update shadow
            self.shadow.setColor(QColor(0, 255, 65, 80) if is_success else QColor(255, 49, 49, 80))
        
        if progress >= 0:
            self.progress_bar.show()
            self.progress_bar.setValue(progress)
        else:
            self.progress_bar.hide()
        
        # Reset timer if not sticky
        if self.is_sticky:
            self.timer.stop()
        elif self.timer.isActive():
            self.timer.start(duration)

    def slide_out(self):
        if self.is_closing:
            return
        self.is_closing = True
        self.pos_anim.stop()
        self.pos_anim.setEndValue(QPoint(self.start_x, self.y_pos))
        self.pos_anim.setEasingCurve(QEasingCurve.Type.InExpo)
        self.pos_anim.finished.connect(self.close)
        self.pos_anim.start()

class SyncPill(QWidget):
    """A ultra-lightweight, high-performance progress pill for real-time feedback."""
    def __init__(self, parent=None):
        super().__init__(None)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.setFixedSize(320, 105)
        
        # Layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)
        
        self.frame = QWidget()
        self.frame.setObjectName("PillFrame")
        self.frame.setStyleSheet("""
            QWidget#PillFrame {
                background-color: #0D0D0D;
                border: 1px solid #00FF41;
                border-radius: 12px;
            }
        """)
        self.frame_layout = QVBoxLayout(self.frame)
        self.frame_layout.setContentsMargins(15, 8, 15, 8)
        self.frame_layout.setSpacing(2)
        
        # Glow Shadow (Matched to Toast)
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(20)
        self.shadow.setColor(QColor(0, 255, 65, 100))
        self.shadow.setOffset(0, 0)
        self.frame.setGraphicsEffect(self.shadow)
        
        self.label = QLabel("Syncing Progress...")
        self.label.setFixedHeight(18)
        self.label.setStyleSheet("color: white; font-weight: bold; font-size: 13px; background: transparent;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.stats_label = QLabel("Waiting to start...")
        self.stats_label.setFixedHeight(15)
        self.stats_label.setStyleSheet("color: #00FF41; font-weight: bold; font-size: 10px; font-family: 'JetBrains Mono'; background: transparent;")
        self.stats_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.file_label = QLabel("...")
        self.file_label.setFixedHeight(15)
        self.file_label.setStyleSheet("color: #999999; font-size: 9px; background: transparent;")
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.file_label.setWordWrap(False)
        self.file_label.setMaximumWidth(240)
        
        self.bar = QProgressBar()
        self.bar.setFixedHeight(4)
        self.bar.setTextVisible(False)
        self.bar.setStyleSheet("""
            QProgressBar {
                background-color: rgba(255, 255, 255, 0.1);
                border: none;
                border-radius: 2px;
            }
            QProgressBar::chunk {
                background-color: #00FF41;
                border-radius: 2px;
            }
        """)
        
        self.frame_layout.addWidget(self.label)
        self.frame_layout.addWidget(self.stats_label)
        self.frame_layout.addWidget(self.bar)
        self.frame_layout.addWidget(self.file_label)
        self.layout.addWidget(self.frame)
        
        # Position matching Toast (Top Right)
        screen = QApplication.primaryScreen().availableGeometry()
        width = 320
        self.move(screen.width() - width - 20, 40)

    def update_progress(self, val, msg, current, total, size_mb):
        self.label.setText(f"Syncing... {val}%")
        self.stats_label.setText(f"{current} / {total} files | {size_mb:.2f} MB")
        
        # Abbreviate filename if too long
        filename = msg.split("\\")[-1] if "\\" in msg else msg.split("/")[-1]
        if len(filename) > 30:
            filename = filename[:27] + "..."
        self.file_label.setText(f"→ {filename}")
        
        self.bar.setValue(val)
        if not self.isVisible():
            self.show()

    def finish(self):
        self.hide()

class HotkeySelector(QPushButton):
    hotkeyChanged = pyqtSignal(str)

    def __init__(self, current_hotkey="ctrl+alt+b", parent=None):
        super().__init__(parent)
        self.current_hotkey = current_hotkey
        self.is_recording = False
        self.setText(self.current_hotkey.upper())
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(35)
        
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(10)
        self.shadow.setColor(QColor(0, 255, 65, 100))
        self.shadow.setOffset(0, 0)
        self.setGraphicsEffect(self.shadow)

        self.setStyleSheet("""
            QPushButton {
                background-color: #0A0A0A;
                border: 1px solid #1A1A1A;
                border-radius: 8px;
                color: #00FF41;
                font-family: 'JetBrains Mono';
                font-weight: bold;
                font-size: 12px;
                padding: 5px;
            }
            QPushButton:hover {
                border-color: #00FF41;
                background-color: #0D0D0D;
            }
            QPushButton:checked {
                border-color: #00FF41;
                color: #FFFFFF;
                background-color: #004D13;
            }
        """)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.start_recording()
        super().mousePressEvent(event)

    def start_recording(self):
        self.is_recording = True
        self.setText("PRESS KEYS...")
        self.setChecked(True)
        self.grabKeyboard()

    def keyPressEvent(self, event):
        if not self.is_recording:
            super().keyPressEvent(event)
            return

        key = event.key()
        if key == Qt.Key.Key_Escape:
            self.stop_recording()
            return

        modifiers = event.modifiers()
        parts = []
        if modifiers & Qt.KeyboardModifier.ControlModifier:
            parts.append("ctrl")
        if modifiers & Qt.KeyboardModifier.AltModifier:
            parts.append("alt")
        if modifiers & Qt.KeyboardModifier.ShiftModifier:
            parts.append("shift")
        
        # Get key name
        text = event.text().lower()
        key_name = ""
        
        # Mapping for special keys
        special_keys = {
            Qt.Key.Key_Control: "",
            Qt.Key.Key_Alt: "",
            Qt.Key.Key_Shift: "",
            Qt.Key.Key_Meta: "",
            Qt.Key.Key_Space: "space",
            Qt.Key.Key_Return: "enter",
            Qt.Key.Key_Enter: "enter",
            Qt.Key.Key_Escape: "esc",
        }
        
        if key in special_keys:
            key_name = special_keys[key]
        elif key >= Qt.Key.Key_F1 and key <= Qt.Key.Key_F12:
            key_name = f"f{key - Qt.Key.Key_F1 + 1}"
        else:
            key_name = text if text else ""

        if key_name:
            parts.append(key_name)
            new_hotkey = "+".join(parts)
            self.current_hotkey = new_hotkey
            self.hotkeyChanged.emit(new_hotkey)
            self.stop_recording()

    def stop_recording(self):
        self.is_recording = False
        self.setText(self.current_hotkey.upper())
        self.setChecked(False)
        self.releaseKeyboard()
