"""
STOCK MANAGER DIALOG
Handles product stock updates with logging
"""

import os
import pandas as pd
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QInputDialog, QMessageBox, QScrollArea, QWidget
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont
from modules.activity_logger import activity_logger


class StockManagerDialog(QDialog):
    """Dialog for updating product stock"""
    
    def __init__(self, parent=None, employee_id="000", employee_name="Unknown"):
        super().__init__(parent)
        self.setWindowTitle("Stock Manager")
        self.setGeometry(250, 150, 800, 600)
        self.setStyleSheet("QDialog { background-color: #f8fafc; }")
        
        self.employee_id = employee_id
        self.employee_name = employee_name
        
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
        
        # Show logged in user
        user_info = QLabel(f"👤 Logged in as: {self.employee_name} ({self.employee_id})")
        user_info.setFont(QFont("Arial", 12))
        user_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        user_info.setStyleSheet("color: #64748b; margin: 5px;")
        layout.addWidget(user_info)
        
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
            product_widget.setMinimumHeight(60)
            product_widget.setMaximumHeight(60)
            
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
            h_layout.setContentsMargins(10, 5, 10, 5)
            product_widget.setLayout(h_layout)
            
            # Product info - ALL IN ONE LINE
            info_label = QLabel(f"🏷️ {row['product_id']} - {row['name']}  |  📊 Stock: {int(row['stock'])}")
            info_label.setFont(QFont("Arial", 13))
            info_label.setStyleSheet("color: #1e293b;")
            info_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
            h_layout.addWidget(info_label, 1)
            
            # Update button
            update_btn = QPushButton("✏️ Update")
            update_btn.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            update_btn.setFixedSize(QSize(100, 40))
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
        
        if ok and new_stock != current_stock:
            # Update stock
            self.products.at[index, 'stock'] = new_stock
            self.save_products()
            
            # Log the stock update
            activity_logger.log_stock_update(
                self.employee_id,
                self.employee_name,
                product['product_id'],
                product['name'],
                current_stock,
                new_stock
            )
            
            QMessageBox.information(
                self,
                "Stock Updated",
                f"✅ {product['name']}\n"
                f"Stock updated: {current_stock} → {new_stock}\n\n"
                f"Change has been logged."
            )
            
            # Refresh the dialog
            self.close()
            new_dialog = StockManagerDialog(self.parent(), self.employee_id, self.employee_name)
            new_dialog.exec()
