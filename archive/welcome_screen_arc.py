"""
WELCOME SCREEN MODULE
Shows welcome message with options:
1. Start as Cashier
2. Update Stock
3. Update Prices
"""

import os
import pandas as pd
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QInputDialog, QMessageBox, QScrollArea,
    QWidget, QLineEdit, QSpinBox, QDoubleSpinBox, QGridLayout,
    QFormLayout
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPixmap


class WelcomeScreen(QDialog):
    """Welcome screen with system options"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Akbar Jaya Cashier System - Welcome")
        self.setGeometry(200, 100, 900, 700)
        self.setStyleSheet("QDialog { background-color: #f8fafc; }")
        self.setModal(True)
        
        self.selected_mode = None
        self.cashier_name = "Cashier"
        self.employee_id = "000"
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the welcome screen UI"""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        self.setLayout(layout)
        
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
        
        title = QLabel("🏪 AKBAR JAYA")
        title.setFont(QFont("Arial", 48, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: white;")
        title_layout.addWidget(title)
        
        subtitle = QLabel("Point of Sale System v1.5")
        subtitle.setFont(QFont("Arial", 20))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #dbeafe; margin-top: 10px;")
        title_layout.addWidget(subtitle)
        
        layout.addWidget(title_container)
        
        # Welcome message
        welcome_msg = QLabel("Welcome! Please select an option to continue:")
        welcome_msg.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        welcome_msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_msg.setStyleSheet("color: #1e40af; margin: 20px;")
        layout.addWidget(welcome_msg)
        
        # Option buttons
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
        cashier_title = QLabel("💳 Start as Cashier")
        cashier_title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        cashier_title.setStyleSheet("color: white;")
        cashier_desc = QLabel("Process sales transactions, manage cart, print receipts")
        cashier_desc.setFont(QFont("Arial", 14))
        cashier_desc.setStyleSheet("color: #d1fae5; margin-top: 5px;")
        
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
        stock_title = QLabel("📦 Update Stock")
        stock_title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        stock_title.setStyleSheet("color: white;")
        stock_desc = QLabel("Add or modify product inventory levels")
        stock_desc.setFont(QFont("Arial", 14))
        stock_desc.setStyleSheet("color: #dbeafe; margin-top: 5px;")
        
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
        price_title = QLabel("💰 Update Prices")
        price_title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        price_title.setStyleSheet("color: white;")
        price_desc = QLabel("Modify individual product prices")
        price_desc.setFont(QFont("Arial", 14))
        price_desc.setStyleSheet("color: #ede9fe; margin-top: 5px;")
        
        price_content.addWidget(price_title)
        price_content.addWidget(price_desc)
        price_btn.setLayout(price_content)
        price_btn.clicked.connect(self.open_price_manager)
        buttons_layout.addWidget(price_btn)
        
        layout.addWidget(buttons_container)
        
        # Guidelines section
        guidelines = QLabel("""
📖 Quick Guidelines:
• Cashier Mode: Click catalogs (AJ, PK, OB) → Select products → Checkout
• Stock Update: Select products to add/remove inventory
• Price Update: Select products to modify prices
• All changes are saved to products.csv automatically
        """)
        guidelines.setFont(QFont("Arial", 13))
        guidelines.setStyleSheet("""
            background-color: #fef3c7;
            color: #78350f;
            padding: 20px;
            border-radius: 10px;
            border: 2px solid #fbbf24;
        """)
        guidelines.setWordWrap(True)
        layout.addWidget(guidelines)
        
        # Footer
        footer = QLabel("© 2025 Akbar Jaya Store • v1.5 with Catalog System")
        footer.setFont(QFont("Arial", 11))
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("color: #64748b; margin-top: 10px;")
        layout.addWidget(footer)
    
    def start_cashier_mode(self):
        """Start the cashier mode after asking name and employee ID"""
        # Create a custom dialog for name and ID input
        login_dialog = EmployeeLoginDialog(self)
        result = login_dialog.exec()
        
        if result == QDialog.DialogCode.Accepted:
            self.cashier_name = login_dialog.employee_name
            self.employee_id = login_dialog.employee_id
            self.selected_mode = "cashier"
            self.accept()
    
    def open_stock_manager(self):
        """Open the stock management dialog after employee verification"""
        # Require employee login
        login_dialog = EmployeeLoginDialog(self, for_management=True)
        result = login_dialog.exec()
        
        if result == QDialog.DialogCode.Accepted:
            dialog = StockManagerDialog(self)
            dialog.exec()
    
    def open_price_manager(self):
        """Open the price management dialog after employee verification"""
        # Require employee login
        login_dialog = EmployeeLoginDialog(self, for_management=True)
        result = login_dialog.exec()
        
        if result == QDialog.DialogCode.Accepted:
            dialog = PriceManagerDialog(self)
            dialog.exec()


class EmployeeLoginDialog(QDialog):
    """Dialog for employee login with name and ID"""
    
    def __init__(self, parent=None, for_management=False):
        super().__init__(parent)
        self.setWindowTitle("Employee Login")
        self.setGeometry(400, 300, 500, 350)
        self.setStyleSheet("QDialog { background-color: #f8fafc; }")
        self.setModal(True)
        
        self.employee_name = "Cashier"
        self.employee_id = "000"
        self.for_management = for_management
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize login dialog UI"""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        self.setLayout(layout)
        
        # Title
        if self.for_management:
            title_text = "🔐 Management Access"
            subtitle_text = "Enter employee credentials to continue"
        else:
            title_text = "👤 Employee Login"
            subtitle_text = "Please enter your information"
        
        title = QLabel(title_text)
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            color: #1e40af;
            background-color: #dbeafe;
            padding: 20px;
            border-radius: 10px;
        """)
        layout.addWidget(title)
        
        subtitle = QLabel(subtitle_text)
        subtitle.setFont(QFont("Arial", 14))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #64748b; margin: 10px;")
        layout.addWidget(subtitle)
        
        # Form container
        form_container = QWidget()
        form_container.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_container.setLayout(form_layout)
        
        # Name input
        self.name_input = QLineEdit()
        self.name_input.setFont(QFont("Arial", 14))
        self.name_input.setPlaceholderText("Enter your full name")
        self.name_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #cbd5e1;
                border-radius: 8px;
                font-size: 16px;
            }
            QLineEdit:focus {
                border: 2px solid #3b82f6;
            }
        """)
        
        name_label = QLabel("👤 Employee Name:")
        name_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        name_label.setStyleSheet("color: #1e293b;")
        form_layout.addRow(name_label, self.name_input)
        
        # ID input
        self.id_input = QLineEdit()
        self.id_input.setFont(QFont("Arial", 14))
        self.id_input.setPlaceholderText("Enter employee ID")
        self.id_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #cbd5e1;
                border-radius: 8px;
                font-size: 16px;
            }
            QLineEdit:focus {
                border: 2px solid #3b82f6;
            }
        """)
        
        id_label = QLabel("🆔 Employee ID:")
        id_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        id_label.setStyleSheet("color: #1e293b;")
        form_layout.addRow(id_label, self.id_input)
        
        layout.addWidget(form_container)
        
        # Buttons
        buttons_container = QWidget()
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        buttons_container.setLayout(buttons_layout)
        
        # Login button
        login_btn = QPushButton("✅ Login")
        login_btn.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        login_btn.setMinimumHeight(60)
        login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: white;
                border-radius: 10px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        login_btn.clicked.connect(self.validate_and_accept)
        buttons_layout.addWidget(login_btn)
        
        # Cancel button
        cancel_btn = QPushButton("❌ Cancel")
        cancel_btn.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        cancel_btn.setMinimumHeight(60)
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #ef4444;
                color: white;
                border-radius: 10px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #dc2626;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        layout.addWidget(buttons_container)
        
        # Set focus to name input
        self.name_input.setFocus()
    
    def validate_and_accept(self):
        """Validate inputs and accept dialog"""
        name = self.name_input.text().strip()
        emp_id = self.id_input.text().strip()
        
        if not name:
            QMessageBox.warning(
                self,
                "Invalid Input",
                "⚠️ Please enter your name!"
            )
            self.name_input.setFocus()
            return
        
        if not emp_id:
            QMessageBox.warning(
                self,
                "Invalid Input",
                "⚠️ Please enter your employee ID!"
            )
            self.id_input.setFocus()
            return
        
        # Validate ID format (alphanumeric)
        if not emp_id.replace("-", "").isalnum():
            QMessageBox.warning(
                self,
                "Invalid ID Format",
                "⚠️ Employee ID should contain only letters and numbers!"
            )
            self.id_input.setFocus()
            return
        
        # Store credentials
        self.employee_name = name
        self.employee_id = emp_id
        
        self.accept()


class StockManagerDialog(QDialog):
    """Dialog for updating product stock"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Stock Manager")
        self.setGeometry(250, 150, 800, 600)
        self.setStyleSheet("QDialog { background-color: #f8fafc; }")
        
        self.products = self.load_products()
        self.init_ui()
    
    def load_products(self):
        """Load products from CSV"""
        data_path = os.path.join("data", "products.csv")
        try:
            df = pd.read_csv(data_path)
            return df
        except:
            return pd.DataFrame(columns=["product_id", "name", "category", "price", "stock"])
    
    def save_products(self):
        """Save products to CSV"""
        data_path = os.path.join("data", "products.csv")
        self.products.to_csv(data_path, index=False)
    
    def init_ui(self):
        """Initialize stock manager UI"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Title
        title = QLabel("📦 Stock Management")
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
        
        # Instructions
        instructions = QLabel("Click on a product to update its stock level:")
        instructions.setFont(QFont("Arial", 14))
        instructions.setStyleSheet("color: #475569; margin: 10px;")
        layout.addWidget(instructions)
        
        # Scroll area for products
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_widget.setLayout(scroll_layout)
        scroll.setWidget(scroll_widget)
        
        # Create product buttons
        for idx, row in self.products.iterrows():
            product_widget = QWidget()
            product_widget.setMinimumHeight(80)
            
            # Determine color based on stock
            if int(row['stock']) <= 5:
                bg_color = "#fecaca"  # Light red
                border_color = "#ef4444"
            else:
                bg_color = "#ffffff"
                border_color = "#cbd5e1"
            
            product_widget.setStyleSheet(f"""
                QWidget {{
                    background-color: {bg_color};
                    border: 2px solid {border_color};
                    border-radius: 8px;
                    padding: 10px;
                    margin: 5px;
                }}
                QWidget:hover {{
                    border: 2px solid #3b82f6;
                }}
            """)
            
            h_layout = QHBoxLayout()
            product_widget.setLayout(h_layout)
            
            # Product info
            info_label = QLabel(
                f"🏷️ {row['product_id']} - {row['name']}\n"
                f"📊 Current Stock: {int(row['stock'])}"
            )
            info_label.setFont(QFont("Arial", 13))
            info_label.setStyleSheet("color: #1e293b;")
            h_layout.addWidget(info_label, 1)
            
            # Update button
            update_btn = QPushButton("✏️ Update")
            update_btn.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            update_btn.setMinimumSize(QSize(100, 60))
            update_btn.setStyleSheet("""
                QPushButton {
                    background-color: #3b82f6;
                    color: white;
                    border-radius: 8px;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: #2563eb;
                }
            """)
            update_btn.clicked.connect(lambda _, i=idx: self.update_stock(i))
            h_layout.addWidget(update_btn)
            
            scroll_layout.addWidget(product_widget)
        
        layout.addWidget(scroll)
        
        # Close button
        close_btn = QPushButton("✅ Done")
        close_btn.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        close_btn.setMinimumHeight(50)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: white;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
    
    def update_stock(self, index):
        """Update stock for a specific product"""
        product = self.products.iloc[index]
        current_stock = int(product['stock'])
        
        new_stock, ok = QInputDialog.getInt(
            self,
            "Update Stock",
            f"Product: {product['name']}\n"
            f"Current Stock: {current_stock}\n\n"
            f"Enter new stock level:",
            value=current_stock,
            min=0,
            max=9999
        )
        
        if ok:
            self.products.at[index, 'stock'] = new_stock
            self.save_products()
            
            QMessageBox.information(
                self,
                "Stock Updated",
                f"✅ {product['name']}\n"
                f"Stock updated: {current_stock} → {new_stock}"
            )
            
            # Refresh the dialog
            self.close()
            new_dialog = StockManagerDialog(self.parent())
            new_dialog.exec()


class PriceManagerDialog(QDialog):
    """Dialog for updating product prices"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Price Manager")
        self.setGeometry(250, 150, 800, 600)
        self.setStyleSheet("QDialog { background-color: #f8fafc; }")
        
        self.products = self.load_products()
        self.init_ui()
    
    def load_products(self):
        """Load products from CSV"""
        data_path = os.path.join("data", "products.csv")
        try:
            df = pd.read_csv(data_path)
            return df
        except:
            return pd.DataFrame(columns=["product_id", "name", "category", "price", "stock"])
    
    def save_products(self):
        """Save products to CSV"""
        data_path = os.path.join("data", "products.csv")
        self.products.to_csv(data_path, index=False)
    
    def init_ui(self):
        """Initialize price manager UI"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Title
        title = QLabel("💰 Price Management")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            color: #7c3aed;
            background-color: #f3e8ff;
            padding: 15px;
            border-radius: 10px;
            margin: 10px;
        """)
        layout.addWidget(title)
        
        # Instructions
        instructions = QLabel("Click on a product to update its price:")
        instructions.setFont(QFont("Arial", 14))
        instructions.setStyleSheet("color: #475569; margin: 10px;")
        layout.addWidget(instructions)
        
        # Scroll area for products
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_widget.setLayout(scroll_layout)
        scroll.setWidget(scroll_widget)
        
        # Create product buttons
        for idx, row in self.products.iterrows():
            product_widget = QWidget()
            product_widget.setMinimumHeight(80)
            product_widget.setStyleSheet("""
                QWidget {
                    background-color: #ffffff;
                    border: 2px solid #cbd5e1;
                    border-radius: 8px;
                    padding: 10px;
                    margin: 5px;
                }
                QWidget:hover {
                    border: 2px solid #8b5cf6;
                }
            """)
            
            h_layout = QHBoxLayout()
            product_widget.setLayout(h_layout)
            
            # Product info
            info_label = QLabel(
                f"🏷️ {row['product_id']} - {row['name']}\n"
                f"💵 Current Price: ${float(row['price']):.2f}"
            )
            info_label.setFont(QFont("Arial", 13))
            info_label.setStyleSheet("color: #1e293b;")
            h_layout.addWidget(info_label, 1)
            
            # Update button
            update_btn = QPushButton("✏️ Update")
            update_btn.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            update_btn.setMinimumSize(QSize(100, 60))
            update_btn.setStyleSheet("""
                QPushButton {
                    background-color: #8b5cf6;
                    color: white;
                    border-radius: 8px;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: #7c3aed;
                }
            """)
            update_btn.clicked.connect(lambda _, i=idx: self.update_price(i))
            h_layout.addWidget(update_btn)
            
            scroll_layout.addWidget(product_widget)
        
        layout.addWidget(scroll)
        
        # Close button
        close_btn = QPushButton("✅ Done")
        close_btn.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        close_btn.setMinimumHeight(50)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: white;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
    
    def update_price(self, index):
        """Update price for a specific product"""
        product = self.products.iloc[index]
        current_price = float(product['price'])
        
        new_price, ok = QInputDialog.getDouble(
            self,
            "Update Price",
            f"Product: {product['name']}\n"
            f"Current Price: ${current_price:.2f}\n\n"
            f"Enter new price:",
            value=current_price,
            min=0.01,
            max=9999.99,
            decimals=2
        )
        
        if ok:
            self.products.at[index, 'price'] = new_price
            self.save_products()
            
            QMessageBox.information(
                self,
                "Price Updated",
                f"✅ {product['name']}\n"
                f"Price updated: ${current_price:.2f} → ${new_price:.2f}"
            )
            
            # Refresh the dialog
            self.close()
            new_dialog = PriceManagerDialog(self.parent())
            new_dialog.exec()
