"""
AKBAR JAYA CASHIER SYSTEM - MAIN PROGRAM (IMPROVED UI v1.3)
Enhanced with:
- Colorful square buttons for elderly users (16pt font)
- Better receipt alignment
- Color-coded product categories
- Modern, attractive interface
- Modular structure with separate files
- FIXED: Buttons stay visible
- v1.2: Buttons moved to BOTTOM, smaller size (140x80)
- v1.3: Receipt hidden until checkout, cart gets more space
- v1.4: Cart hides after checkout, focus on receipt only
- v1.5: Catalog view - click category (AJ, PK, OB) to see products
- v1.6: Welcome screen with Stock/Price management

Run: python main_prog_improved.py
"""

import sys
import os
import pandas as pd
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QScrollArea, QMessageBox, QInputDialog, 
    QTextEdit, QLineEdit, QFileDialog, QGridLayout, QDialog
)
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtGui import QFont
from datetime import datetime

# Import our custom modules
from receipt_improved import generate_receipt_text
from report_improved import generate_sales_report
from modules.welcome_screen import WelcomeScreen


class LargePaymentDialog(QDialog):
    """Large payment dialog for elderly customers with big text and buttons"""
    
    def __init__(self, parent, total_amount):
        super().__init__(parent)
        self.setWindowTitle("Payment")
        self.setGeometry(250, 150, 900, 700)  # Much larger window
        self.setStyleSheet("QDialog { background-color: #f8fafc; }")
        self.setModal(True)
        
        self.total_amount = total_amount
        self.payment_amount = 0.0
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize payment dialog with large UI elements"""
        layout = QVBoxLayout()
        layout.setSpacing(30)
        self.setLayout(layout)
        
        # Title
        title = QLabel("💳 PAYMENT")
        title.setFont(QFont("Arial", 48, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            color: white;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #10b981, stop:1 #059669);
            padding: 40px;
            border-radius: 15px;
        """)
        layout.addWidget(title)
        
        # Total amount display - VERY LARGE
        total_label = QLabel(f"TOTAL AMOUNT:")
        total_label.setFont(QFont("Arial", 36, QFont.Weight.Bold))
        total_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        total_label.setStyleSheet("color: #1e40af; margin-top: 20px;")
        layout.addWidget(total_label)
        
        total_value = QLabel(f"${self.total_amount:.2f}")
        total_value.setFont(QFont("Arial", 72, QFont.Weight.Bold))
        total_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        total_value.setStyleSheet("""
            color: #dc2626;
            background-color: #fee2e2;
            padding: 30px;
            border-radius: 15px;
            border: 5px solid #ef4444;
        """)
        layout.addWidget(total_value)
        
        # Payment input section
        input_container = QWidget()
        input_container.setStyleSheet("""
            background-color: #ffffff;
            border-radius: 15px;
            padding: 30px;
            border: 3px solid #cbd5e1;
        """)
        input_layout = QVBoxLayout()
        input_container.setLayout(input_layout)
        
        payment_label = QLabel("💵 Enter Payment Received:")
        payment_label.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        payment_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        payment_label.setStyleSheet("color: #1e293b; margin-bottom: 20px;")
        input_layout.addWidget(payment_label)
        
        self.payment_input = QLineEdit()
        self.payment_input.setFont(QFont("Arial", 64, QFont.Weight.Bold))
        self.payment_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.payment_input.setPlaceholderText("0.00")
        self.payment_input.setStyleSheet("""
            QLineEdit {
                padding: 30px;
                border: 5px solid #3b82f6;
                border-radius: 15px;
                background-color: #eff6ff;
                color: #1e40af;
            }
            QLineEdit:focus {
                border: 5px solid #10b981;
                background-color: #d1fae5;
            }
        """)
        input_layout.addWidget(self.payment_input)
        
        layout.addWidget(input_container)
        
        # Buttons - EXTRA LARGE
        buttons_container = QWidget()
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)
        buttons_container.setLayout(buttons_layout)
        
        # Confirm button
        confirm_btn = QPushButton("✅\nCONFIRM\nPAYMENT")
        confirm_btn.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        confirm_btn.setMinimumSize(QSize(350, 180))
        confirm_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        confirm_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: white;
                border-radius: 20px;
                padding: 20px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        confirm_btn.clicked.connect(self.validate_payment)
        buttons_layout.addWidget(confirm_btn)
        
        # Cancel button
        cancel_btn = QPushButton("❌\nCANCEL")
        cancel_btn.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        cancel_btn.setMinimumSize(QSize(350, 180))
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #ef4444;
                color: white;
                border-radius: 20px;
                padding: 20px;
            }
            QPushButton:hover {
                background-color: #dc2626;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        layout.addWidget(buttons_container)
        
        # Set focus to payment input
        self.payment_input.setFocus()
    
    def validate_payment(self):
        """Validate payment amount"""
        try:
            payment = float(self.payment_input.text())
            
            if payment < self.total_amount:
                # Show error in large format
                error_msg = QMessageBox(self)
                error_msg.setWindowTitle("Insufficient Payment")
                error_msg.setIcon(QMessageBox.Icon.Warning)
                error_msg.setText(f"⚠️ INSUFFICIENT PAYMENT\n\n"
                                f"Required: ${self.total_amount:.2f}\n"
                                f"Received: ${payment:.2f}\n\n"
                                f"Please enter at least ${self.total_amount:.2f}")
                error_msg.setStyleSheet("""
                    QMessageBox {
                        font-size: 24px;
                    }
                    QLabel {
                        font-size: 24px;
                        min-width: 500px;
                    }
                """)
                error_msg.exec()
                self.payment_input.setFocus()
                self.payment_input.selectAll()
                return
            
            self.payment_amount = payment
            self.accept()
            
        except ValueError:
            error_msg = QMessageBox(self)
            error_msg.setWindowTitle("Invalid Input")
            error_msg.setIcon(QMessageBox.Icon.Warning)
            error_msg.setText("⚠️ INVALID AMOUNT\n\nPlease enter a valid number!")
            error_msg.setStyleSheet("""
                QMessageBox {
                    font-size: 24px;
                }
                QLabel {
                    font-size: 24px;
                    min-width: 400px;
                }
            """)
            error_msg.exec()
            self.payment_input.setFocus()
            self.payment_input.selectAll()

##FIXED version
class LargeCompletionDialog(QDialog):
    """Large completion dialog showing payment and change for elderly customers"""
    
    def __init__(self, parent, payment, change):
        super().__init__(parent)
        self.setWindowTitle("Transaction Complete")
        
        # --- ORIGINAL FIXED SIZE ---
        # self.setGeometry(250, 150, 900, 700)  # Much larger window
        
        # --- FIXED VERSION: allow resizing + move to center later ---
        self.resize(900, 800)
        self.setMinimumHeight(800)
        self.setSizeGripEnabled(True)
        # self.move(250, 150)  # commented, replaced with center_on_screen() below

        self.setStyleSheet("QDialog { background-color: #f8fafc; }")
        self.setModal(True)
        
        self.payment = payment
        self.change = change
        
        self.init_ui()
        self.center_on_screen()  # <-- auto center after building UI
    
    def init_ui(self):
        """Initialize completion dialog with large UI elements"""

        # --- ORIGINAL DIRECT LAYOUT ---
        # layout = QVBoxLayout()
        # layout.setSpacing(30)
        # self.setLayout(layout)
        
        # --- FIX VERSION: wrap layout inside QScrollArea so content scrolls if too tall ---
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        container = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(30)
        container.setLayout(layout)

        scroll_area.setWidget(container)

        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)
        
        # Success icon and title
        title = QLabel("✅ TRANSACTION\nCOMPLETE!")
        title.setFont(QFont("Arial", 56, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            color: white;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #10b981, stop:1 #059669);
            padding: 50px;
            border-radius: 20px;
        """)
        layout.addWidget(title)
        
        # Payment received
        payment_container = QWidget()
        payment_container.setStyleSheet("""
            background-color: #dbeafe;
            border-radius: 15px;
            padding: 30px;
            border: 4px solid #3b82f6;
        """)
        payment_layout = QVBoxLayout()
        payment_container.setLayout(payment_layout)
        
        payment_label = QLabel("💵 Payment Received:")
        payment_label.setFont(QFont("Arial", 32, QFont.Weight.Bold))
        payment_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        payment_label.setStyleSheet("color: #1e40af;")
        payment_layout.addWidget(payment_label)
        
        payment_value = QLabel(f"${self.payment:.2f}")
        payment_value.setFont(QFont("Arial", 64, QFont.Weight.Bold))
        payment_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        payment_value.setStyleSheet("color: #1e40af; margin: 10px;")
        payment_layout.addWidget(payment_value)
        
        layout.addWidget(payment_container)
        
        # Change to give
        change_container = QWidget()
        change_container.setStyleSheet("""
            background-color: #d1fae5;
            border-radius: 15px;
            padding: 30px;
            border: 4px solid #10b981;
        """)
        change_layout = QVBoxLayout()
        change_container.setLayout(change_layout)
        
        change_label = QLabel("💰 Change to Return:")
        change_label.setFont(QFont("Arial", 32, QFont.Weight.Bold))
        change_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        change_label.setStyleSheet("color: #047857;")
        change_layout.addWidget(change_label)
        
        change_value = QLabel(f"${self.change:.2f}")
        change_value.setFont(QFont("Arial", 72, QFont.Weight.Bold))
        change_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        change_value.setStyleSheet("color: #047857; margin: 10px;")
        change_layout.addWidget(change_value)
        
        layout.addWidget(change_container)
        
        # Thank you message
        thank_you = QLabel("🙏 Thank You!")
        thank_you.setFont(QFont("Arial", 36, QFont.Weight.Bold))
        thank_you.setAlignment(Qt.AlignmentFlag.AlignCenter)
        thank_you.setStyleSheet("color: #6366f1; margin: 20px;")
        layout.addWidget(thank_you)
        
        # OK button - EXTRA LARGE
        ok_btn = QPushButton("✅\nOK")
        ok_btn.setFont(QFont("Arial", 32, QFont.Weight.Bold))
        ok_btn.setMinimumSize(QSize(400, 150))
        ok_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border-radius: 20px;
                padding: 20px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        ok_btn.clicked.connect(self.accept)
        layout.addWidget(ok_btn, alignment=Qt.AlignmentFlag.AlignCenter)
    
    def center_on_screen(self):
        """Center the dialog on the current screen"""
        screen = QApplication.primaryScreen()
        if screen:
            screen_geometry = screen.availableGeometry()
            x = (screen_geometry.width() - self.width()) // 2
            y = (screen_geometry.height() - self.height()) // 2
            self.move(x, y)


##--------------Fixed

class LargeCustomerNameDialog(QDialog):
    """Large dialog for entering customer name - elderly-friendly"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Customer Name")
        self.resize(900, 600)
        self.setStyleSheet("QDialog { background-color: #f8fafc; }")
        self.setModal(True)
        
        self.customer_name = "Customer"
        
        self.init_ui()
        self.center_on_screen()
    
    def init_ui(self):
        """Initialize customer name dialog with large UI elements"""
        layout = QVBoxLayout()
        layout.setSpacing(30)
        self.setLayout(layout)
        
        # Title
        title = QLabel("👤 CUSTOMER NAME")
        title.setFont(QFont("Arial", 48, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            color: white;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #3b82f6, stop:1 #2563eb);
            padding: 40px;
            border-radius: 15px;
        """)
        layout.addWidget(title)
        
        # Instructions
        instructions = QLabel("Please enter the customer's name:")
        instructions.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instructions.setStyleSheet("color: #1e40af; margin: 20px;")
        layout.addWidget(instructions)
        
        # Name input section
        input_container = QWidget()
        input_container.setStyleSheet("""
            background-color: #ffffff;
            border-radius: 15px;
            padding: 30px;
            border: 3px solid #cbd5e1;
        """)
        input_layout = QVBoxLayout()
        input_container.setLayout(input_layout)
        
        name_label = QLabel("📝 Customer Name:")
        name_label.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setStyleSheet("color: #1e293b; margin-bottom: 20px;")
        input_layout.addWidget(name_label)
        
        self.name_input = QLineEdit()
        self.name_input.setFont(QFont("Arial", 48, QFont.Weight.Bold))
        self.name_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_input.setPlaceholderText("Enter name here...")
        self.name_input.setText("Customer")  # Default value
        self.name_input.setStyleSheet("""
            QLineEdit {
                padding: 30px;
                border: 5px solid #3b82f6;
                border-radius: 15px;
                background-color: #eff6ff;
                color: #1e40af;
            }
            QLineEdit:focus {
                border: 5px solid #10b981;
                background-color: #d1fae5;
            }
        """)
        input_layout.addWidget(self.name_input)
        
        layout.addWidget(input_container)
        
        # Buttons - EXTRA LARGE
        buttons_container = QWidget()
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)
        buttons_container.setLayout(buttons_layout)
        
        # OK button
        ok_btn = QPushButton("✅\nOK")
        ok_btn.setFont(QFont("Arial", 32, QFont.Weight.Bold))
        ok_btn.setMinimumSize(QSize(350, 150))
        ok_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: white;
                border-radius: 20px;
                padding: 20px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        ok_btn.clicked.connect(self.accept_name)
        buttons_layout.addWidget(ok_btn)
        
        # Skip button (use default "Customer")
        skip_btn = QPushButton("⏭️\nSKIP\n(Use 'Customer')")
        skip_btn.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        skip_btn.setMinimumSize(QSize(350, 150))
        skip_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        skip_btn.setStyleSheet("""
            QPushButton {
                background-color: #6b7280;
                color: white;
                border-radius: 20px;
                padding: 20px;
            }
            QPushButton:hover {
                background-color: #4b5563;
            }
        """)
        skip_btn.clicked.connect(self.skip_name)
        buttons_layout.addWidget(skip_btn)
        
        layout.addWidget(buttons_container)
        
        # Set focus to name input and select all text
        self.name_input.setFocus()
        self.name_input.selectAll()
    
    def accept_name(self):
        """Accept the entered name"""
        name = self.name_input.text().strip()
        if name:
            self.customer_name = name
        else:
            self.customer_name = "Customer"
        self.accept()
    
    def skip_name(self):
        """Skip and use default 'Customer'"""
        self.customer_name = "Customer"
        self.accept()
    
    def center_on_screen(self):
        """Center the dialog on the current screen"""
        screen = QApplication.primaryScreen()
        if screen:
            screen_geometry = screen.availableGeometry()
            x = (screen_geometry.width() - self.width()) // 2
            y = (screen_geometry.height() - self.height()) // 2
            self.move(x, y)

class AkbarCashier(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Akbar Jaya Cashier System - Enhanced UI v1.8")
        self.setGeometry(100, 100, 1200, 800)
        self.cart = []

        self.setStyleSheet("QMainWindow { background-color: #f8fafc; }")

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_widget.setStyleSheet("background-color: #f8fafc;")
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        # Title
        self.title_label = QLabel("AKBAR JAYA")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont("Arial", 32, QFont.Weight.Bold)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet("""
            color: #1e3a8a;
            background-color: #dbeafe;
            padding: 20px;
            border-radius: 10px;
            margin: 5px;
        """)
        self.main_layout.addWidget(self.title_label)

        # Date & Time
        self.datetime_label = QLabel()
        self.datetime_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        datetime_font = QFont("Arial", 16, QFont.Weight.Bold)
        self.datetime_label.setFont(datetime_font)
        self.datetime_label.setStyleSheet("color: #059669; padding: 5px;")
        self.main_layout.addWidget(self.datetime_label)

        # Cashier Name
        self.cashier_label = QLabel()
        self.cashier_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cashier_font = QFont("Arial", 18, QFont.Weight.Bold)
        self.cashier_label.setFont(cashier_font)
        self.cashier_label.setStyleSheet("""
            color: #7c3aed;
            background-color: #f3e8ff;
            padding: 10px;
            border-radius: 8px;
            margin: 5px;
        """)
        self.main_layout.addWidget(self.cashier_label)

        # Cashier name and ID will be set from welcome screen
        self.cashier_name = "Cashier"  # Default, will be updated
        self.employee_id = "000"  # Default, will be updated
        self.cashier_label.setText(f"👤 Cashier: {self.cashier_name} (ID: {self.employee_id})")

        # Update datetime every second
        def update_datetime():
            now = datetime.now().strftime("%A, %B %d, %Y - %H:%M:%S")
            self.datetime_label.setText(f"🕒 {now}")

        self.timer = QTimer()
        self.timer.timeout.connect(update_datetime)
        self.timer.start(1000)
        update_datetime()

        # Main horizontal layout
        self.h_layout = QHBoxLayout()
        self.main_layout.addLayout(self.h_layout)

        # Left panel: Products
        self.product_area = QWidget()
        self.product_layout = QVBoxLayout()
        self.product_area.setLayout(self.product_layout)
        self.product_area.setStyleSheet("""
            background-color: #ffffff;
            border-radius: 10px;
            padding: 10px;
        """)

        # Title for catalog section
        catalog_title = QLabel("📂 Product Catalog")
        catalog_title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        catalog_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        catalog_title.setStyleSheet("""
            color: #1e40af;
            background-color: #dbeafe;
            padding: 10px;
            border-radius: 8px;
            margin: 5px;
        """)
        self.product_layout.addWidget(catalog_title)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.product_area)
        self.scroll.setStyleSheet("QScrollArea { border: none; }")
        self.h_layout.addWidget(self.scroll, 2)

        # Right panel: Cart & Receipt with buttons at BOTTOM
        self.cart_area = QWidget()
        self.cart_layout = QVBoxLayout()
        self.cart_layout.setSpacing(10)
        self.cart_area.setLayout(self.cart_layout)
        self.cart_area.setStyleSheet("""
            background-color: #ffffff;
            border-radius: 10px;
            padding: 15px;
        """)
        self.h_layout.addWidget(self.cart_area, 1)

        # Cart section - NOW BIGGER (no max height initially)
        self.cart_scroll_area = QScrollArea()
        self.cart_scroll_area.setWidgetResizable(True)
        self.cart_scroll_area.setMinimumHeight(200)
        # NO maximum height - cart can grow to fill space
        self.cart_scroll_area.setStyleSheet("""
            QScrollArea {
                border: 2px solid #cbd5e1;
                border-radius: 8px;
                background-color: #f8fafc;
            }
        """)
        
        self.cart_label = QLabel("🛒 Shopping Cart:\n\n  (Empty)")
        self.cart_label.setFont(QFont("Arial", 14))  # Slightly bigger font
        self.cart_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.cart_label.setStyleSheet("color: #1e40af; padding: 10px; background-color: transparent;")
        self.cart_label.setWordWrap(True)
        
        self.cart_scroll_area.setWidget(self.cart_label)
        self.cart_layout.addWidget(self.cart_scroll_area, 1)  # Takes available space

        # Receipt display - HIDDEN BY DEFAULT
        self.receipt_display = QTextEdit()
        self.receipt_display.setReadOnly(True)
        self.receipt_display.setFont(QFont("Courier New", 11))
        self.receipt_display.setStyleSheet("""
            QTextEdit {
                background-color: #f8fafc;
                border: 2px solid #cbd5e1;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        self.receipt_display.hide()  # HIDDEN AT START
        self.cart_layout.addWidget(self.receipt_display, 1)

        # Buttons at BOTTOM - Smaller size (140x80)
        button_container = QWidget()
        button_grid = QGridLayout()
        button_grid.setSpacing(8)
        button_container.setLayout(button_grid)
        
        # Checkout - GREEN
        self.checkout_btn = QPushButton("💳\nCHECKOUT")
        self.checkout_btn.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.checkout_btn.setMinimumSize(QSize(140, 80))
        self.checkout_btn.setMaximumSize(QSize(140, 80))
        self.checkout_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: white;
                border-radius: 12px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        self.checkout_btn.clicked.connect(self.checkout)
        button_grid.addWidget(self.checkout_btn, 0, 0)

        # Cancel - RED
        self.cancel_btn = QPushButton("❌\nCANCEL")
        self.cancel_btn.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.cancel_btn.setMinimumSize(QSize(140, 80))
        self.cancel_btn.setMaximumSize(QSize(140, 80))
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #ef4444;
                color: white;
                border-radius: 12px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #dc2626;
            }
        """)
        self.cancel_btn.clicked.connect(self.cancel_item)
        button_grid.addWidget(self.cancel_btn, 0, 1)

        # Print - BLUE
        self.print_btn = QPushButton("🖨️\nPRINT")
        self.print_btn.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.print_btn.setMinimumSize(QSize(140, 80))
        self.print_btn.setMaximumSize(QSize(140, 80))
        self.print_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border-radius: 12px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        self.print_btn.clicked.connect(self.print_receipt)
        button_grid.addWidget(self.print_btn, 1, 0)

        # PDF - PURPLE
        self.pdf_btn = QPushButton("📄\nSAVE PDF")
        self.pdf_btn.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.pdf_btn.setMinimumSize(QSize(140, 80))
        self.pdf_btn.setMaximumSize(QSize(140, 80))
        self.pdf_btn.setStyleSheet("""
            QPushButton {
                background-color: #8b5cf6;
                color: white;
                border-radius: 12px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #7c3aed;
            }
        """)
        self.pdf_btn.clicked.connect(self.print_receipt_to_pdf)
        button_grid.addWidget(self.pdf_btn, 1, 1)

        # Report - ORANGE (spans 2 columns)
        self.report_btn = QPushButton("📊\nREPORT")
        self.report_btn.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.report_btn.setMinimumSize(QSize(288, 80))
        self.report_btn.setMaximumSize(QSize(288, 80))
        self.report_btn.setStyleSheet("""
            QPushButton {
                background-color: #f59e0b;
                color: white;
                border-radius: 12px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #d97706;
            }
        """)
        self.report_btn.clicked.connect(lambda: generate_sales_report(self))
        button_grid.addWidget(self.report_btn, 2, 0, 1, 2)
        
        # Add buttons at BOTTOM of layout
        self.cart_layout.addWidget(button_container)

        self.refresh_product_list()
        self.show_stock_summary()

    def load_products(self):
        data_path = os.path.join("data", "products.csv")
        os.makedirs("data", exist_ok=True)
        
        if not os.path.exists(data_path) or os.stat(data_path).st_size == 0:
            sample_data = """product_id,name,category,price,stock
AJ001,Milo 3-in-1,Drink,1.80,25
AJ002,Maggi Curry,Food,3.50,40
AJ003,Sprite Can,Drink,1.60,30
AJ004,Rice 5kg,Food,13.50,10
AJ005,Battery AA,Electronics,2.00,15
"""
            with open(data_path, "w", encoding="utf-8") as f:
                f.write(sample_data)
        
        try:
            df = pd.read_csv(data_path)
        except Exception as e:
            print(f"[ERROR] Failed to load products.csv: {e}")
            df = pd.DataFrame(columns=["product_id", "name", "category", "price", "stock"])
        
        return df

    def refresh_product_list(self):
        self.products = self.load_products()
        
        if 'price' in self.products.columns:
            self.products['price'] = pd.to_numeric(self.products['price'], errors='coerce').fillna(0.0)
        if 'stock' in self.products.columns:
            self.products['stock'] = pd.to_numeric(self.products['stock'], errors='coerce').fillna(0).astype(int)

        # Clear existing buttons (skip the title label at index 0)
        for i in reversed(range(self.product_layout.count())):
            if i > 0:  # Keep the title label
                widget = self.product_layout.itemAt(i).widget()
                if widget:
                    widget.setParent(None)

        # Get unique catalog prefixes (first 2 characters of product_id)
        catalogs = {}
        for _, p in self.products.iterrows():
            prefix = p['product_id'][:2]  # Get first 2 chars (AJ, PK, OB, etc.)
            if prefix not in catalogs:
                catalogs[prefix] = []
            catalogs[prefix].append(p)
        
        # Default colors for categories
        colors = {
            'Drink': '#3b82f6',
            'Food': '#10b981',
            'Electronics': '#f59e0b',
            'default': '#6366f1'
        }
        
        # Create catalog buttons
        for prefix in sorted(catalogs.keys()):
            products_in_catalog = catalogs[prefix]
            
            # Check if any product in this catalog has low stock
            has_low_stock = any(int(p.get('stock', 0)) <= 5 for p in products_in_catalog)
            
            # Determine color based on first product's category or low stock
            first_product = products_in_catalog[0]
            category = str(first_product.get('category', 'default'))
            color = colors.get(category, colors['default'])
            
            if has_low_stock:
                color = '#ef4444'  # Red for low stock
            
            # Count products in catalog
            count = len(products_in_catalog)
            
            # Create catalog button
            btn = QPushButton(f"📁\n{prefix}\n({count} items)")
            btn.setFont(QFont("Arial", 20, QFont.Weight.Bold))
            btn.setMinimumSize(QSize(150, 150))
            btn.setMaximumSize(QSize(150, 150))
            
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: none;
                    border-radius: 15px;
                    padding: 10px;
                }}
                QPushButton:hover {{
                    background-color: {color};
                    opacity: 0.85;
                    transform: scale(1.05);
                }}
            """)
            
            # Connect to open catalog dialog
            btn.clicked.connect(lambda _, p=prefix: self.open_catalog_dialog(p))
            self.product_layout.addWidget(btn)
        
        # Add stretch to push buttons to top
        self.product_layout.addStretch()

    def open_catalog_dialog(self, catalog_prefix):
        """Open a dialog showing all products in the selected catalog"""
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Catalog: {catalog_prefix}")
        dialog.setGeometry(200, 200, 800, 600)
        dialog.setStyleSheet("QDialog { background-color: #f8fafc; }")
        
        layout = QVBoxLayout()
        dialog.setLayout(layout)
        
        # Title
        title = QLabel(f"📂 {catalog_prefix} Products")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            color: #1e40af;
            background-color: #dbeafe;
            padding: 15px;
            border-radius: 10px;
            margin: 10px;
        """)
        layout.addWidget(title)
        
        # Scroll area for products
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_widget.setLayout(scroll_layout)
        scroll.setWidget(scroll_widget)
        
        # Filter products by prefix
        catalog_products = self.products[self.products['product_id'].str.startswith(catalog_prefix)]
        
        # Default colors
        colors = {
            'Drink': '#3b82f6',
            'Food': '#10b981',
            'Electronics': '#f59e0b',
            'default': '#6366f1'
        }
        
        # Create product buttons
        for _, p in catalog_products.iterrows():
            try:
                label_text = (
                    f"🏷️ {p['product_id']}\n"
                    f"📦 {p['name']}\n"
                    f"💰 ${float(p['price']):.2f}\n"
                    f"📊 Stock: {int(p['stock'])}\n"
                )
            except:
                label_text = f"{p.get('product_id','Unknown')} — {p.get('name','Unnamed')}"
            
            btn = QPushButton(label_text)
            btn.setFont(QFont("Arial", 14, QFont.Weight.Bold))
            btn.setMinimumHeight(100)
            
            category = str(p.get('category', 'default'))
            color = colors.get(category, colors['default'])
            
            if int(p.get('stock', 0)) <= 5:
                color = '#ef4444'
            
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: none;
                    border-radius: 10px;
                    padding: 15px;
                    text-align: left;
                }}
                QPushButton:hover {{
                    background-color: {color};
                    opacity: 0.85;
                }}
            """)
            
            # Add to cart and close dialog
            btn.clicked.connect(lambda _, pid=p['product_id']: self.add_to_cart_and_close(pid, dialog))
            scroll_layout.addWidget(btn)
        
        layout.addWidget(scroll)
        
        # Close button
        close_btn = QPushButton("❌ Close")
        close_btn.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        close_btn.setMinimumHeight(50)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #6b7280;
                color: white;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #4b5563;
            }
        """)
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        dialog.exec()
    
    def add_to_cart_and_close(self, product_id, dialog):
        """Add product to cart and optionally close dialog"""
        self.add_to_cart(product_id)
        # Don't close dialog automatically - let user add multiple items
        # dialog.close()

    def add_to_cart(self, product_id):
        product = self.products[self.products['product_id'] == product_id].iloc[0]
        current_qty_in_cart = self.cart.count(product_id)
        
        if product['stock'] <= current_qty_in_cart:
            QMessageBox.warning(self, "Out of Stock", 
                              f"{product['name']} has only {product['stock']} left in stock!")
            return
        
        self.cart.append(product_id)
        self.update_cart_label()

    def update_cart_label(self):
        text = "🛒 Shopping Cart:\n\n"
        summary = {}
        for pid in self.cart:
            summary[pid] = summary.get(pid, 0) + 1
        
        if not summary:
            text += "  (Empty)\n"
        else:
            for pid, qty in summary.items():
                product = self.products[self.products['product_id'] == pid].iloc[0]
                name = product['name']
                price = float(product['price'])
                total = price * qty
                text += f"  • {name}\n"
                text += f"    {qty} × ${price:.2f} = ${total:.2f}\n\n"
            
            grand_total = sum(float(self.products[self.products['product_id'] == pid].iloc[0]['price']) 
                            for pid in self.cart)
            text += f"───────────────────\n"
            text += f"TOTAL: ${grand_total:.2f}\n"
        
        self.cart_label.setText(text)

    def show_stock_summary(self):
        low_stock = self.products[self.products['stock'] <= 5]
        msg = f"📊 Total Products: {len(self.products)}\n\n"
        
        if not low_stock.empty:
            msg += "⚠️ LOW STOCK ALERT:\n\n"
            for _, p in low_stock.iterrows():
                msg += f"  • {p['name']}\n"
                msg += f"    ID: {p['product_id']}\n"
                msg += f"    Stock: {p['stock']} remaining\n\n"
        else:
            msg += "✅ All products have sufficient stock."
        
        QMessageBox.information(self, "Stock Summary", msg)

    def checkout(self):
        if not self.cart:
            QMessageBox.information(self, "Empty Cart", "Your cart is empty!")
            return

        total = sum(float(self.products[self.products['product_id'] == pid].iloc[0]['price']) 
                   for pid in self.cart)
        
        # Create a larger, elderly-friendly payment dialog
        payment_dialog = LargePaymentDialog(self, total)
        result = payment_dialog.exec()
        
        if result != QDialog.DialogCode.Accepted:
            return
        
        payment = payment_dialog.payment_amount
        ok = True
        
        if not ok or payment < total:
            QMessageBox.warning(self, "Payment Error", 
                              f"Payment must be at least ${total:.2f}.")
            return
        
        change = payment - total

        # Use custom large dialog for customer name input
        name_dialog = LargeCustomerNameDialog(self)
        result = name_dialog.exec()
        
        if result == QDialog.DialogCode.Accepted:
            customer_name = name_dialog.customer_name
        else:
            customer_name = "Customer"

        for pid in self.cart:
            idx = self.products[self.products['product_id'] == pid].index[0]
            self.products.at[idx, 'stock'] -= 1
        self.products.to_csv(os.path.join("data", "products.csv"), index=False)

        self.save_sales(customer_name)

        receipt_text = generate_receipt_text(
            self.cart, self.products,
            customer_name=customer_name,
            payment_amount=payment,
            change_amount=change,
            cashier_name=f"{self.cashier_name} (ID: {self.employee_id})"
        )
        
        # NEW v1.4: Show receipt box and HIDE cart completely
        self.receipt_display.setPlainText(receipt_text)
        self.receipt_display.show()  # Show receipt after checkout
        
        # HIDE cart completely to focus on receipt
        self.cart_scroll_area.hide()

        self.cart = []
        self.update_cart_label()
        self.refresh_product_list()
        
        # Show large completion dialog for elderly
        completion_dialog = LargeCompletionDialog(self, payment, change)
        completion_dialog.exec()

    def print_receipt(self):
        if not self.receipt_display.toPlainText().strip():
            QMessageBox.warning(self, "No Receipt", "No receipt to print.")
            return
        
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        
        if dialog.exec() == QPrintDialog.DialogCode.Accepted:
            self.receipt_display.print(printer)
        
        # Reset: Hide receipt, show cart again, clear data
        self.cart = []
        self.update_cart_label()
        self.receipt_display.clear()
        self.receipt_display.hide()  # Hide receipt again
        self.cart_scroll_area.show()  # Show cart again
        self.refresh_product_list()
        
        QMessageBox.information(self, "Ready", "✅ Transaction completed!")

    def print_receipt_to_pdf(self):
        if not self.receipt_display.toPlainText().strip():
            QMessageBox.warning(self, "No Receipt", "No receipt to save.")
            return
        
        printer = QPrinter()
        printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Receipt as PDF", "", "PDF Files (*.pdf)"
        )
        
        if filename:
            printer.setOutputFileName(filename)
            self.receipt_display.print(printer)
            QMessageBox.information(self, "Saved", f"✅ Receipt saved as PDF:\n{filename}")

    def cancel_item(self):
        if not self.cart:
            QMessageBox.information(self, "Cart Empty", "No items to cancel.")
            return

        summary = {}
        for pid in self.cart:
            summary[pid] = summary.get(pid, 0) + 1
        
        items_list = [
            f"{self.products[self.products['product_id']==pid].iloc[0]['name']} x {qty}" 
            for pid, qty in summary.items()
        ]

        item, ok = QInputDialog.getItem(
            self, "Cancel Item", "Select item to remove:", items_list, 0, False
        )
        
        if ok and item:
            pid_to_remove = None
            for pid, qty in summary.items():
                name = self.products[self.products['product_id']==pid].iloc[0]['name']
                if item.startswith(name):
                    pid_to_remove = pid
                    break
            
            if pid_to_remove:
                self.cart.remove(pid_to_remove)
                self.update_cart_label()
                QMessageBox.information(self, "Item Removed", f"✅ {item} removed from cart.")

    def save_sales(self, customer_name="Customer"):
        sales_path = os.path.join("data", "sales.csv")
        os.makedirs("data", exist_ok=True)
        
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df_sale = pd.DataFrame([{
            'datetime': now,
            'customer_name': customer_name,
            'cashier_name': self.cashier_name,
            'employee_id': self.employee_id,
            'products': ",".join(self.cart)
        }])
        
        if os.path.exists(sales_path) and os.stat(sales_path).st_size > 0:
            try:
                df_existing = pd.read_csv(sales_path)
                df_sale = pd.concat([df_existing, df_sale], ignore_index=True)
            except pd.errors.EmptyDataError:
                pass
        
        df_sale.to_csv(sales_path, index=False)


def main():
    print("=" * 60)
    print("AKBAR JAYA CASHIER SYSTEM - v1.8")
    print("NEW: User Management System with Registration")
    print("Features: Fullscreen welcome, User database, Auto-registration")
    print("=" * 60)
    
    app = QApplication(sys.argv)
    
    # Show welcome screen first
    welcome = WelcomeScreen()
    result = welcome.exec()
    
    # If user selected cashier mode, start the cashier system
    if result == QDialog.DialogCode.Accepted and welcome.selected_mode == "cashier":
        win = AkbarCashier()
        win.cashier_name = welcome.cashier_name
        win.employee_id = welcome.employee_id
        win.cashier_label.setText(f"👤 Cashier: {win.cashier_name} (ID: {win.employee_id})")
        win.show()
        sys.exit(app.exec())
    else:
        print("\n✅ Thank you for using Akbar Jaya Cashier System!")
        sys.exit(0)


if __name__ == "__main__":
    main()
