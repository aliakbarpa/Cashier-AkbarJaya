import sys
import os
import pandas as pd
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QScrollArea, QMessageBox, QInputDialog, QTextEdit, QLineEdit, QFileDialog
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtGui import QFont
from datetime import datetime
from receipt import generate_receipt_text
from report import generate_sales_report

class AkbarCashier(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Akbar Jaya Cashier")
        self.setGeometry(100, 100, 900, 600)
        self.cart = []

        # --- Main widget ---
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_widget.setStyleSheet("background-color: #F0F0F0;")
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        # --- Title --- [FIXED: Changed from 50 to 24]
        self.title_label = QLabel("Akbar Jaya")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont("Arial", 24, QFont.Weight.Bold)  # FIXED: Was 50, now 24
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet("color: #333333; margin-bottom: 10px;")
        self.main_layout.addWidget(self.title_label)

        # --- Date & Time Label ---
        self.datetime_label = QLabel()
        self.datetime_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        datetime_font = QFont("Arial", 14)
        self.datetime_label.setFont(datetime_font)
        self.datetime_label.setStyleSheet("color: #2ec7c0; margin-bottom: 5px;")
        self.main_layout.addWidget(self.datetime_label)

        # --- Cashier Name Label --- [FIXED: Changed from 40 to 16]
        self.cashier_label = QLabel()
        self.cashier_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cashier_font = QFont("Arial", 16, QFont.Weight.Bold)  # FIXED: Was 40, now 16
        self.cashier_label.setFont(cashier_font)
        self.cashier_label.setStyleSheet("color: #222222; margin-bottom: 15px;")
        self.main_layout.addWidget(self.cashier_label)

        # --- Ask cashier name ---
        cashier_name, ok = QInputDialog.getText(
            self, "Cashier Name", "Enter your name:", text="Cashier"
        )
        if not ok or cashier_name.strip() == "":
            self.cashier_name = "Cashier"
        else:
            self.cashier_name = cashier_name

        self.cashier_label.setText(f"Cashier: {self.cashier_name}")

        # --- Update datetime every second ---
        def update_datetime():
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.datetime_label.setText(now)

        self.timer = QTimer()
        self.timer.timeout.connect(update_datetime)
        self.timer.start(1000)
        update_datetime()

        # --- Horizontal layout for product & cart ---
        self.h_layout = QHBoxLayout()
        self.main_layout.addLayout(self.h_layout)

        # --- Left panel: Products ---
        self.product_area = QWidget()
        self.product_layout = QVBoxLayout()
        self.product_area.setLayout(self.product_layout)
        self.product_area.setStyleSheet("background-color: #FFFFFF;")

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search products by ID or Name...")
        self.search_bar.textChanged.connect(self.search_products)
        self.product_layout.addWidget(self.search_bar)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.product_area)
        self.h_layout.addWidget(self.scroll, 2)

        # --- Right panel: Cart & Receipt ---
        self.cart_area = QWidget()
        self.cart_layout = QVBoxLayout()
        self.cart_area.setLayout(self.cart_layout)
        self.cart_area.setStyleSheet("background-color: #EFEFEF; color: black;")
        self.h_layout.addWidget(self.cart_area, 1)

        self.cart_label = QLabel("Cart:")
        self.cart_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.cart_layout.addWidget(self.cart_label)

        self.checkout_btn = QPushButton("Checkout")
        self.checkout_btn.clicked.connect(self.checkout)
        self.cart_layout.addWidget(self.checkout_btn)

        self.cancel_btn = QPushButton("Cancel Item")
        self.cancel_btn.clicked.connect(self.cancel_item)
        self.cart_layout.addWidget(self.cancel_btn)

        self.receipt_display = QTextEdit()
        self.receipt_display.setReadOnly(True)
        self.receipt_display.setFont(QFont("Courier New", 10))
        self.cart_layout.addWidget(self.receipt_display)

        self.print_btn = QPushButton("Print Receipt")
        self.print_btn.clicked.connect(self.print_receipt)
        self.cart_layout.addWidget(self.print_btn)

        self.pdf_btn = QPushButton("Save Receipt as PDF")
        self.pdf_btn.clicked.connect(self.print_receipt_to_pdf)
        self.cart_layout.addWidget(self.pdf_btn)

        # --- Generate Report Button ---
        self.report_btn = QPushButton("Generate Sales Report")
        self.report_btn.clicked.connect(lambda: generate_sales_report(self))
        self.cart_layout.addWidget(self.report_btn)

        # Load products
        self.refresh_product_list()

        # Show stock summary at startup
        self.show_stock_summary()

    # ---------- Load Products ----------
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
        except pd.errors.EmptyDataError:
            df = pd.DataFrame(columns=["product_id", "name", "category", "price", "stock"])
        except Exception as e:
            print(f"[ERROR] Failed to load products.csv: {e}")
            df = pd.DataFrame(columns=["product_id", "name", "category", "price", "stock"])
        return df

    # ---------- Refresh Product List ----------
    def refresh_product_list(self):
        self.products = self.load_products()
        if 'price' in self.products.columns:
            self.products['price'] = pd.to_numeric(self.products['price'], errors='coerce').fillna(0.0)
        if 'stock' in self.products.columns:
            self.products['stock'] = pd.to_numeric(self.products['stock'], errors='coerce').fillna(0).astype(int)

        for i in reversed(range(self.product_layout.count())):
            widget = self.product_layout.itemAt(i).widget()
            if widget and widget != self.search_bar:
                widget.setParent(None)

        for _, p in self.products.iterrows():
            try:
                label = (
                    f"Product ID: {p['product_id']}\n"
                    f"Name: {p['name']}\n"
                    f"Price: ${float(p['price']):.2f}\n"
                    f"Stock Available: {int(p['stock'])}\n"
                    f"Click to add 1 item to cart"
                )
            except:
                label = f"{p.get('product_id','Unknown')} — {p.get('name','Unnamed')}"
            btn = QPushButton(label)
            font = QFont()
            font.setBold(True)
            btn.setFont(font)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #FFFFFF;
                    color: #000000;
                    border: 1px solid #AAAAAA;
                    border-radius: 5px;
                    padding: 10px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #DDDDDD;
                }
            """)
            btn.clicked.connect(lambda _, pid=p['product_id']: self.add_to_cart(pid))
            self.product_layout.addWidget(btn)

    # ---------- Search Products ----------
    def search_products(self):
        query = self.search_bar.text().strip().lower()
        for i in range(self.product_layout.count()):
            widget = self.product_layout.itemAt(i).widget()
            if isinstance(widget, QPushButton):
                text = widget.text().lower()
                widget.setVisible(query in text)

    # ---------- Add Product to Cart ----------
    def add_to_cart(self, product_id):
        product = self.products[self.products['product_id'] == product_id].iloc[0]
        current_qty_in_cart = self.cart.count(product_id)
        if product['stock'] <= current_qty_in_cart:
            QMessageBox.warning(self, "Out of Stock", f"{product['name']} has only {product['stock']} left in stock!")
            return
        self.cart.append(product_id)
        self.update_cart_label()

    # ---------- Update Cart ----------
    def update_cart_label(self):
        text = "Cart:\n"
        summary = {}
        for pid in self.cart:
            summary[pid] = summary.get(pid, 0) + 1
        for pid, qty in summary.items():
            name = self.products[self.products['product_id'] == pid].iloc[0]['name']
            text += f"{name} x {qty}\n"
        self.cart_label.setText(text)

    # ---------- Show Stock Summary ----------
    def show_stock_summary(self):
        low_stock = self.products[self.products['stock'] <= 5]
        msg = f"Total Products: {len(self.products)}\n"
        if not low_stock.empty:
            msg += "Low Stock Items:\n"
            for _, p in low_stock.iterrows():
                msg += f"- {p['name']} (ID: {p['product_id']}): {p['stock']} left\n"
        else:
            msg += "All products have sufficient stock."
        QMessageBox.information(self, "Stock Summary", msg)

    # ---------- Checkout ----------
    def checkout(self):
        if not self.cart:
            QMessageBox.information(self, "Empty Cart", "Your cart is empty!")
            return

        total = sum(float(self.products[self.products['product_id'] == pid].iloc[0]['price']) for pid in self.cart)
        payment, ok = QInputDialog.getDouble(
            self, "Payment",
            f"Total amount: ${total:.2f}\nEnter payment received:",
            decimals=2, min=0.0
        )
        if not ok or payment < total:
            QMessageBox.warning(self, "Payment Error", f"Payment must be at least ${total:.2f}.")
            return
        change = payment - total

        customer_name, ok = QInputDialog.getText(
            self, "Customer Name", "Enter customer name:", text="Customer"
        )
        if not ok or customer_name.strip() == "":
            customer_name = "Customer"

        # Reduce stock
        for pid in self.cart:
            idx = self.products[self.products['product_id'] == pid].index[0]
            self.products.at[idx, 'stock'] -= 1
        self.products.to_csv(os.path.join("data", "products.csv"), index=False)

        self.save_sales(customer_name)

        # Generate receipt
        receipt_text = generate_receipt_text(
            self.cart, self.products,
            customer_name=customer_name,
            payment_amount=payment,
            change_amount=change,
            cashier_name=self.cashier_name
        )
        self.receipt_display.setPlainText(receipt_text)

        # Reset cart
        self.cart = []
        self.update_cart_label()
        self.refresh_product_list()
        QMessageBox.information(self, "Checkout Complete",
                                f"Payment received: ${payment:.2f}\nChange: ${change:.2f}\nReceipt is ready to print!")

    # ---------- Print Receipt ----------
    def print_receipt(self):
        if self.receipt_display.toPlainText().strip() == "":
            QMessageBox.warning(self, "No Receipt", "No receipt to print.")
            return
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        if dialog.exec() == QPrintDialog.DialogCode.Accepted:
            self.receipt_display.print(printer)
        # Reset for next transaction
        self.cart = []
        self.update_cart_label()
        self.receipt_display.clear()
        self.refresh_product_list()
        QMessageBox.information(self, "Ready", "Transaction completed. Ready for next customer!")

    # ---------- Save Receipt to PDF ----------
    def print_receipt_to_pdf(self):
        if self.receipt_display.toPlainText().strip() == "":
            QMessageBox.warning(self, "No Receipt", "No receipt to save.")
            return
        printer = QPrinter()
        printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
        filename, _ = QFileDialog.getSaveFileName(self, "Save Receipt as PDF", "", "PDF Files (*.pdf)")
        if filename:
            printer.setOutputFileName(filename)
            self.receipt_display.print(printer)
            QMessageBox.information(self, "Saved", f"Receipt saved as PDF:\n{filename}")

    # ---------- Cancel Item ----------
    def cancel_item(self):
        if not self.cart:
            QMessageBox.information(self, "Cart Empty", "No items to cancel.")
            return

        summary = {}
        for pid in self.cart:
            summary[pid] = summary.get(pid, 0) + 1
        items_list = [f"{self.products[self.products['product_id']==pid].iloc[0]['name']} x {qty}" for pid, qty in summary.items()]

        item, ok = QInputDialog.getItem(self, "Cancel Item", "Select item to remove:", items_list, 0, False)
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
                QMessageBox.information(self, "Item Removed", f"{item} removed from cart.")

    # ---------- Save Sales ----------
    def save_sales(self, customer_name="Customer"):
        sales_path = os.path.join("data", "sales.csv")
        os.makedirs("data", exist_ok=True)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df_sale = pd.DataFrame([{
            'datetime': now,
            'customer_name': customer_name,
            'cashier_name': self.cashier_name,
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
    app = QApplication(sys.argv)
    win = AkbarCashier()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
