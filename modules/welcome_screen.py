"""
WELCOME SCREEN MODULE - WITH CENTRALIZED TRANSLATION SYSTEM
Shows welcome message with options:
1. Start as Cashier
2. Update Stock
3. Update Prices

FEATURES:
- Language selection (English/Bahasa Indonesia) with flags
- Centralized translation system
- Proper fullscreen rendering
- Role-based access control
- Activity logging
"""

import os
import pandas as pd
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QScrollArea, QWidget
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont
from datetime import datetime

# Import translation system
from modules.translations import LanguageManager, tr

# Import helper dialogs from separate modules
from modules.employee_login import EmployeeLoginDialog
from modules.stock_manager import StockManagerDialog
from modules.price_manager import PriceManagerDialog


class FlagButton(QPushButton):
    """Custom button to display flag with text"""
    
    def __init__(self, flag_emoji, text, parent=None):
        super().__init__(parent)
        self.flag_emoji = flag_emoji
        self.flag_text = text
        self.setMinimumSize(QSize(120, 60))
        self.setMaximumSize(QSize(120, 60))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Set text
        self.setText(f"{flag_emoji}\n{text}")
        self.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        
        # Default style (not selected)
        self.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #1e40af;
                border: 3px solid #cbd5e1;
                border-radius: 10px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #eff6ff;
                border: 3px solid #3b82f6;
            }
        """)
    
    def set_selected(self, selected):
        """Highlight button when selected"""
        if selected:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #3b82f6;
                    color: white;
                    border: 3px solid #1e40af;
                    border-radius: 10px;
                    padding: 5px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #2563eb;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #ffffff;
                    color: #1e40af;
                    border: 3px solid #cbd5e1;
                    border-radius: 10px;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #eff6ff;
                    border: 3px solid #3b82f6;
                }
            """)


class WelcomeScreen(QDialog):
    """Welcome screen with system options and role-based access"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Akbar Jaya Cashier System - Welcome")
        self.setStyleSheet("QDialog { background-color: #f8fafc; }")
        self.setModal(True)
        
        self.selected_mode = None
        self.cashier_name = "Cashier"
        self.employee_id = "000"
        self.employee_role = "Cashier"
        
        # Store UI elements that need updating
        self.ui_elements = {}
        
        # Register for language change notifications
        LanguageManager.register_observer(self.update_translations)
        
        # Initialize UI first
        self.init_ui()
        
        # THEN show fullscreen after UI is ready
        self.showFullScreen()
    
    def init_ui(self):
        """Initialize the welcome screen UI"""
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)
        
        # Create scroll area for all content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: #f8fafc; }")
        
        # Content widget inside scroll area
        content_widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        content_widget.setLayout(layout)
        scroll.setWidget(content_widget)
        
        main_layout.addWidget(scroll)
        
        # Language selector at top-right (fixed position overlay)
        lang_container = QWidget(self)
        lang_container.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.95);
            border-radius: 12px;
            padding: 10px;
            border: 2px solid #cbd5e1;
        """)
        lang_layout = QVBoxLayout()
        lang_layout.setSpacing(5)
        lang_container.setLayout(lang_layout)
        
        lang_label = QLabel(tr('language_selector'))
        lang_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        lang_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lang_label.setStyleSheet("color: #1e40af; background: transparent; border: none;")
        lang_layout.addWidget(lang_label)
        self.ui_elements['language_selector'] = lang_label
        
        # Flag buttons container
        flags_layout = QHBoxLayout()
        flags_layout.setSpacing(8)
        
        # English flag button
        self.en_flag_btn = FlagButton("🇬🇧", "English")
        self.en_flag_btn.clicked.connect(lambda: self.change_language('en'))
        flags_layout.addWidget(self.en_flag_btn)
        
        # Indonesian flag button
        self.id_flag_btn = FlagButton("🇮🇩", "Indonesia")
        self.id_flag_btn.clicked.connect(lambda: self.change_language('id'))
        flags_layout.addWidget(self.id_flag_btn)
        
        lang_layout.addLayout(flags_layout)
        
        # Position language selector at top-right
        lang_container.setFixedSize(260, 110)
        lang_container.move(self.width() - 280, 20)
        
        # Update selection based on current language
        current_lang = LanguageManager.get_language()
        self.en_flag_btn.set_selected(current_lang == 'en')
        self.id_flag_btn.set_selected(current_lang == 'id')
        
        # Logo/Title Section
        title_container = QWidget()
        title_container.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #1e3a8a, stop:1 #3b82f6);
            border-radius: 15px;
            padding: 30px;
        """)
        title_layout = QVBoxLayout()
        title_container.setLayout(title_layout)
        
        title = QLabel(tr('welcome_title'))
        title.setFont(QFont("Arial", 48, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: white;")
        title_layout.addWidget(title)
        self.ui_elements['title'] = title
        
        subtitle = QLabel(tr('welcome_subtitle'))
        subtitle.setFont(QFont("Arial", 20))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #dbeafe; margin-top: 10px;")
        title_layout.addWidget(subtitle)
        self.ui_elements['subtitle'] = subtitle
        
        layout.addWidget(title_container)
        
        # Welcome message
        welcome_msg = QLabel(tr('welcome_message'))
        welcome_msg.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        welcome_msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_msg.setStyleSheet("color: #1e40af; margin: 20px;")
        layout.addWidget(welcome_msg)
        self.ui_elements['welcome'] = welcome_msg
        
        # Option buttons container
        buttons_container = QWidget()
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(15)
        buttons_container.setLayout(buttons_layout)
        
        # Button 1: Start as Cashier
        cashier_btn = QPushButton()
        cashier_btn.setMinimumHeight(100)
        cashier_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cashier_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #10b981, stop:1 #059669);
                color: white;
                border-radius: 12px;
                text-align: left;
                padding: 20px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #059669, stop:1 #047857);
            }
        """)
        
        cashier_content = QVBoxLayout()
        cashier_title = QLabel(tr('cashier_option_title'))
        cashier_title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        cashier_title.setStyleSheet("color: white;")
        self.ui_elements['cashier_title'] = cashier_title
        
        cashier_desc = QLabel(tr('cashier_option_desc'))
        cashier_desc.setFont(QFont("Arial", 14))
        cashier_desc.setStyleSheet("color: #d1fae5; margin-top: 5px;")
        self.ui_elements['cashier_desc'] = cashier_desc
        
        cashier_content.addWidget(cashier_title)
        cashier_content.addWidget(cashier_desc)
        cashier_btn.setLayout(cashier_content)
        cashier_btn.clicked.connect(self.start_cashier_mode)
        buttons_layout.addWidget(cashier_btn)
        
        # Button 2: Update Stock
        stock_btn = QPushButton()
        stock_btn.setMinimumHeight(100)
        stock_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        stock_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3b82f6, stop:1 #2563eb);
                color: white;
                border-radius: 12px;
                text-align: left;
                padding: 20px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2563eb, stop:1 #1d4ed8);
            }
        """)
        
        stock_content = QVBoxLayout()
        stock_title = QLabel(tr('stock_option_title'))
        stock_title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        stock_title.setStyleSheet("color: white;")
        self.ui_elements['stock_title'] = stock_title
        
        stock_desc = QLabel(tr('stock_option_desc'))
        stock_desc.setFont(QFont("Arial", 14))
        stock_desc.setStyleSheet("color: #dbeafe; margin-top: 5px;")
        self.ui_elements['stock_desc'] = stock_desc
        
        stock_content.addWidget(stock_title)
        stock_content.addWidget(stock_desc)
        stock_btn.setLayout(stock_content)
        stock_btn.clicked.connect(self.open_stock_manager)
        buttons_layout.addWidget(stock_btn)
        
        # Button 3: Update Prices
        price_btn = QPushButton()
        price_btn.setMinimumHeight(100)
        price_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        price_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #8b5cf6, stop:1 #7c3aed);
                color: white;
                border-radius: 12px;
                text-align: left;
                padding: 20px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #7c3aed, stop:1 #6d28d9);
            }
        """)
        
        price_content = QVBoxLayout()
        price_title = QLabel(tr('price_option_title'))
        price_title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        price_title.setStyleSheet("color: white;")
        self.ui_elements['price_title'] = price_title
        
        price_desc = QLabel(tr('price_option_desc'))
        price_desc.setFont(QFont("Arial", 14))
        price_desc.setStyleSheet("color: #ede9fe; margin-top: 5px;")
        self.ui_elements['price_desc'] = price_desc
        
        price_content.addWidget(price_title)
        price_content.addWidget(price_desc)
        price_btn.setLayout(price_content)
        price_btn.clicked.connect(self.open_price_manager)
        buttons_layout.addWidget(price_btn)
        
        layout.addWidget(buttons_container)
        
        # Guidelines section
        guidelines = QLabel(tr('welcome_guidelines'))
        guidelines.setFont(QFont("Arial", 13))
        guidelines.setStyleSheet("""
            background-color: #fef3c7;
            color: #78350f;
            padding: 20px;
            border-radius: 10px;
            border: 2px solid #fbbf24;
        """)
        guidelines.setWordWrap(True)
        guidelines.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(guidelines)
        self.ui_elements['guidelines'] = guidelines
        
        # Footer with Exit button
        footer_container = QWidget()
        footer_layout = QHBoxLayout()
        footer_container.setLayout(footer_layout)
        
        footer = QLabel(tr('welcome_footer'))
        footer.setFont(QFont("Arial", 11))
        footer.setAlignment(Qt.AlignmentFlag.AlignLeft)
        footer.setStyleSheet("color: #64748b; margin-top: 10px;")
        footer_layout.addWidget(footer, 1)
        self.ui_elements['footer'] = footer
        
        # Exit fullscreen button
        exit_btn = QPushButton(tr('exit_button'))
        exit_btn.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        exit_btn.setMinimumHeight(40)
        exit_btn.setMaximumWidth(120)
        exit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        exit_btn.setStyleSheet("""
            QPushButton {
                background-color: #ef4444;
                color: white;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #dc2626;
            }
        """)
        exit_btn.clicked.connect(self.reject)
        footer_layout.addWidget(exit_btn)
        self.ui_elements['exit_btn'] = exit_btn
        
        layout.addWidget(footer_container)
        
        # Add extra spacing at bottom to ensure all content is visible
        layout.addStretch(1)
    
    def change_language(self, lang_code):
        """Change the interface language"""
        LanguageManager.set_language(lang_code)
        
        # Update flag button highlights
        self.en_flag_btn.set_selected(lang_code == 'en')
        self.id_flag_btn.set_selected(lang_code == 'id')
    
    def update_translations(self):
        """Update all UI text elements with current language"""
        self.ui_elements['language_selector'].setText(tr('language_selector'))
        self.ui_elements['title'].setText(tr('welcome_title'))
        self.ui_elements['subtitle'].setText(tr('welcome_subtitle'))
        self.ui_elements['welcome'].setText(tr('welcome_message'))
        self.ui_elements['cashier_title'].setText(tr('cashier_option_title'))
        self.ui_elements['cashier_desc'].setText(tr('cashier_option_desc'))
        self.ui_elements['stock_title'].setText(tr('stock_option_title'))
        self.ui_elements['stock_desc'].setText(tr('stock_option_desc'))
        self.ui_elements['price_title'].setText(tr('price_option_title'))
        self.ui_elements['price_desc'].setText(tr('price_option_desc'))
        self.ui_elements['guidelines'].setText(tr('welcome_guidelines'))
        self.ui_elements['footer'].setText(tr('welcome_footer'))
        self.ui_elements['exit_btn'].setText(tr('exit_button'))
    
    def resizeEvent(self, event):
        """Handle window resize to keep language selector in top-right"""
        super().resizeEvent(event)
        # Find the language container and reposition it
        for child in self.children():
            if isinstance(child, QWidget) and child.layout() and \
               any(isinstance(w, FlagButton) for w in [child.layout().itemAt(i).widget() 
                   for i in range(child.layout().count()) if child.layout().itemAt(i)]):
                child.move(self.width() - 280, 20)
                break
    
    def start_cashier_mode(self):
        """Start the cashier mode after asking name and employee ID"""
        # Create a custom dialog for name and ID input with role check
        login_dialog = EmployeeLoginDialog(self, required_action="cashier")
        result = login_dialog.exec()
        
        if result == QDialog.DialogCode.Accepted:
            self.cashier_name = login_dialog.employee_name
            self.employee_id = login_dialog.employee_id
            self.employee_role = login_dialog.employee_role
            self.selected_mode = "cashier"
            self.accept()
    
    def open_stock_manager(self):
        """Open the stock management dialog after employee verification"""
        # Require employee login with stock_update permission
        login_dialog = EmployeeLoginDialog(self, for_management=True, required_action="stock_update")
        result = login_dialog.exec()
        
        if result == QDialog.DialogCode.Accepted:
            dialog = StockManagerDialog(
                self,
                login_dialog.employee_id,
                login_dialog.employee_name
            )
            dialog.exec()
    
    def open_price_manager(self):
        """Open the price management dialog after employee verification"""
        # Require employee login with price_update permission
        login_dialog = EmployeeLoginDialog(self, for_management=True, required_action="price_update")
        result = login_dialog.exec()
        
        if result == QDialog.DialogCode.Accepted:
            dialog = PriceManagerDialog(
                self,
                login_dialog.employee_id,
                login_dialog.employee_name
            )
            dialog.exec()
    
    def closeEvent(self, event):
        """Clean up when closing"""
        LanguageManager.unregister_observer(self.update_translations)
        super().closeEvent(event)
