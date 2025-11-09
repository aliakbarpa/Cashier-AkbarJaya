"""
REPORT MODULE - IMPROVED WITH COLORFUL BUTTONS
Generates sales reports with date range filtering (UTF-8 safe)
"""

import os
import pandas as pd
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QMessageBox,
    QDateEdit, QHBoxLayout, QFileDialog
)
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QFont


def generate_sales_report(parent):
    """Generate sales report with date range filter"""
    sales_path = os.path.join("data", "sales.csv")
    product_path = os.path.join("data", "products.csv")

    # Check if sales.csv exists
    if not os.path.exists(sales_path) or os.stat(sales_path).st_size == 0:
        QMessageBox.information(parent, "No Data", 
                               "No sales data available yet to generate report.")
        return

    try:
        df = pd.read_csv(sales_path)
    except Exception as e:
        QMessageBox.warning(parent, "Error", f"Failed to read sales data: {e}")
        return

    if df.empty or 'datetime' not in df.columns:
        QMessageBox.information(parent, "No Data", "No sales data in CSV.")
        return

    # Load products for price and stock info
    try:
        df_products = pd.read_csv(product_path)
        df_products.set_index("product_id", inplace=True)
    except:
        df_products = pd.DataFrame(columns=["product_id", "name", "price", "stock"])
        df_products.set_index("product_id", inplace=True)

    # --- Dialog for selecting date range ---
    dialog = QDialog(parent)
    dialog.setWindowTitle("Select Date Range")
    dialog.setMinimumWidth(400)
    layout = QVBoxLayout()

    start_label = QLabel("Select start date:")
    start_label.setFont(QFont("Arial", 12))
    start_date_edit = QDateEdit()
    start_date_edit.setCalendarPopup(True)
    start_date_edit.setDate(QDate.currentDate())
    start_date_edit.setFont(QFont("Arial", 12))
    layout.addWidget(start_label)
    layout.addWidget(start_date_edit)

    end_label = QLabel("Select end date:")
    end_label.setFont(QFont("Arial", 12))
    end_date_edit = QDateEdit()
    end_date_edit.setCalendarPopup(True)
    end_date_edit.setDate(QDate.currentDate())
    end_date_edit.setFont(QFont("Arial", 12))
    layout.addWidget(end_label)
    layout.addWidget(end_date_edit)

    button_layout = QHBoxLayout()
    
    # Generate button - GREEN
    ok_btn = QPushButton("✅ Generate Report")
    ok_btn.setFont(QFont("Arial", 12, QFont.Weight.Bold))
    ok_btn.setMinimumHeight(50)
    ok_btn.setStyleSheet("""
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
    
    # Cancel button - RED
    cancel_btn = QPushButton("❌ Cancel")
    cancel_btn.setFont(QFont("Arial", 12, QFont.Weight.Bold))
    cancel_btn.setMinimumHeight(50)
    cancel_btn.setStyleSheet("""
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
    
    button_layout.addWidget(ok_btn)
    button_layout.addWidget(cancel_btn)
    layout.addLayout(button_layout)
    dialog.setLayout(layout)

    # --- Generate report function ---
    def generate():
        start_date = start_date_edit.date().toPyDate()
        end_date = end_date_edit.date().toPyDate()
        
        if start_date > end_date:
            QMessageBox.warning(dialog, "Date Error", 
                              "Start date must be before end date.")
            return

        # Filter sales by date
        df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
        mask = (df['datetime'].dt.date >= start_date) & (df['datetime'].dt.date <= end_date)
        df_filtered = df.loc[mask]

        if df_filtered.empty:
            QMessageBox.information(dialog, "No Data", 
                                  "No sales in the selected date range.")
            return

        # Handle missing cashier/customer names safely
        cashiers = df_filtered['cashier_name'].fillna("Unknown").astype(str).unique()
        customers = df_filtered['customer_name'].fillna("Unknown").astype(str).unique()

        # Summary per product, including stock
        product_summary = {}
        total_revenue = 0.0
        
        for idx, row in df_filtered.iterrows():
            products_str = str(row.get('products', ''))
            if not products_str or products_str == 'nan':
                continue
                
            items = products_str.split(',')
            for pid in items:
                pid = pid.strip()
                if not pid:
                    continue
                    
                if pid in df_products.index:
                    try:
                        price = float(df_products.at[pid, 'price'])
                    except (KeyError, ValueError):
                        price = 0.0
                else:
                    price = 0.0
                
                total_revenue += price
                
                if pid not in product_summary:
                    product_summary[pid] = {'qty': 1, 'total': price}
                else:
                    product_summary[pid]['qty'] += 1
                    product_summary[pid]['total'] += price

        # --- Prepare report text ---
        report_text = (
            "SALES REPORT\n"
            f"From {start_date} to {end_date}\n\n"
            f"Cashiers: {', '.join(cashiers)}\n"
            f"Customers: {', '.join(customers)}\n\n"
            f"{'Product ID':10} {'Qty Sold':>10} {'Revenue($)':>12} {'Stock Left':>12}\n"
            + "-" * 50 + "\n"
        )

        for pid, data in product_summary.items():
            stock_left = int(df_products.at[pid, 'stock']) if pid in df_products.index else 'N/A'
            report_text += f"{pid:10} {data['qty']:>10} {data['total']:>12.2f} {str(stock_left):>12}\n"

        report_text += "-" * 50 + "\n"
        report_text += f"{'Total Transactions:':30} {len(df_filtered)}\n"
        report_text += f"{'Total Revenue($):':30} {total_revenue:.2f}\n"

        # --- Save as PDF option ---
        save_pdf = QMessageBox.question(
            dialog,
            "Save Report",
            "Do you want to save this report as a PDF?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if save_pdf == QMessageBox.StandardButton.Yes:
            filename, _ = QFileDialog.getSaveFileName(
                parent, "Save Report as PDF", "", "PDF Files (*.pdf)"
            )
            if filename:
                try:
                    from fpdf import FPDF
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Courier", size=10)
                    
                    # Replace emojis (FPDF can't encode them)
                    safe_text = (
                        report_text
                        .replace("📊", "")
                        .replace("👥", "")
                        .replace("🛍️", "")
                    )
                    
                    for line in safe_text.split("\n"):
                        # Encode safely to avoid Latin-1 error
                        pdf.cell(0, 5, line.encode('latin-1', 'replace').decode('latin-1'), ln=True)
                    
                    pdf.output(filename)
                    QMessageBox.information(parent, "Saved", f"Report saved as PDF:\n{filename}")
                except ImportError:
                    QMessageBox.warning(parent, "FPDF Missing", 
                                      "Install 'fpdf' package to save PDF:\npip install fpdf")
                except Exception as e:
                    QMessageBox.warning(parent, "Error", f"Failed to save PDF:\n{e}")

        QMessageBox.information(dialog, "Sales Report", report_text)
        dialog.accept()

    ok_btn.clicked.connect(generate)
    cancel_btn.clicked.connect(dialog.reject)
    dialog.exec()
"""
REPORT MODULE - IMPROVED WITH COLORFUL BUTTONS
Generates sales reports with date range filtering (UTF-8 safe)
"""

import os
import pandas as pd
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QMessageBox,
    QDateEdit, QHBoxLayout, QFileDialog
)
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QFont


def generate_sales_report(parent):
    """Generate sales report with date range filter"""
    sales_path = os.path.join("data", "sales.csv")
    product_path = os.path.join("data", "products.csv")

    # Check if sales.csv exists
    if not os.path.exists(sales_path) or os.stat(sales_path).st_size == 0:
        QMessageBox.information(parent, "No Data", 
                               "No sales data available yet to generate report.")
        return

    try:
        df = pd.read_csv(sales_path)
    except Exception as e:
        QMessageBox.warning(parent, "Error", f"Failed to read sales data: {e}")
        return

    if df.empty or 'datetime' not in df.columns:
        QMessageBox.information(parent, "No Data", "No sales data in CSV.")
        return

    # Load products for price and stock info
    try:
        df_products = pd.read_csv(product_path)
        df_products.set_index("product_id", inplace=True)
    except:
        df_products = pd.DataFrame(columns=["product_id", "name", "price", "stock"])
        df_products.set_index("product_id", inplace=True)

    # --- Dialog for selecting date range ---
    dialog = QDialog(parent)
    dialog.setWindowTitle("Select Date Range")
    dialog.setMinimumWidth(400)
    layout = QVBoxLayout()

    start_label = QLabel("Select start date:")
    start_label.setFont(QFont("Arial", 12))
    start_date_edit = QDateEdit()
    start_date_edit.setCalendarPopup(True)
    start_date_edit.setDate(QDate.currentDate())
    start_date_edit.setFont(QFont("Arial", 12))
    layout.addWidget(start_label)
    layout.addWidget(start_date_edit)

    end_label = QLabel("Select end date:")
    end_label.setFont(QFont("Arial", 12))
    end_date_edit = QDateEdit()
    end_date_edit.setCalendarPopup(True)
    end_date_edit.setDate(QDate.currentDate())
    end_date_edit.setFont(QFont("Arial", 12))
    layout.addWidget(end_label)
    layout.addWidget(end_date_edit)

    button_layout = QHBoxLayout()
    
    # Generate button - GREEN
    ok_btn = QPushButton("✅ Generate Report")
    ok_btn.setFont(QFont("Arial", 12, QFont.Weight.Bold))
    ok_btn.setMinimumHeight(50)
    ok_btn.setStyleSheet("""
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
    
    # Cancel button - RED
    cancel_btn = QPushButton("❌ Cancel")
    cancel_btn.setFont(QFont("Arial", 12, QFont.Weight.Bold))
    cancel_btn.setMinimumHeight(50)
    cancel_btn.setStyleSheet("""
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
    
    button_layout.addWidget(ok_btn)
    button_layout.addWidget(cancel_btn)
    layout.addLayout(button_layout)
    dialog.setLayout(layout)

    # --- Generate report function ---
    def generate():
        start_date = start_date_edit.date().toPyDate()
        end_date = end_date_edit.date().toPyDate()
        
        if start_date > end_date:
            QMessageBox.warning(dialog, "Date Error", 
                              "Start date must be before end date.")
            return

        # Filter sales by date
        df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
        mask = (df['datetime'].dt.date >= start_date) & (df['datetime'].dt.date <= end_date)
        df_filtered = df.loc[mask]

        if df_filtered.empty:
            QMessageBox.information(dialog, "No Data", 
                                  "No sales in the selected date range.")
            return

        # Handle missing cashier/customer names safely
        cashiers = df_filtered['cashier_name'].fillna("Unknown").astype(str).unique()
        customers = df_filtered['customer_name'].fillna("Unknown").astype(str).unique()

        # Summary per product, including stock
        product_summary = {}
        total_revenue = 0.0
        
        for idx, row in df_filtered.iterrows():
            products_str = str(row.get('products', ''))
            if not products_str or products_str == 'nan':
                continue
                
            items = products_str.split(',')
            for pid in items:
                pid = pid.strip()
                if not pid:
                    continue
                    
                if pid in df_products.index:
                    try:
                        price = float(df_products.at[pid, 'price'])
                    except (KeyError, ValueError):
                        price = 0.0
                else:
                    price = 0.0
                
                total_revenue += price
                
                if pid not in product_summary:
                    product_summary[pid] = {'qty': 1, 'total': price}
                else:
                    product_summary[pid]['qty'] += 1
                    product_summary[pid]['total'] += price

        # --- Prepare report text ---
        report_text = (
            "SALES REPORT\n"
            f"From {start_date} to {end_date}\n\n"
            f"Cashiers: {', '.join(cashiers)}\n"
            f"Customers: {', '.join(customers)}\n\n"
            f"{'Product ID':10} {'Qty Sold':>10} {'Revenue($)':>12} {'Stock Left':>12}\n"
            + "-" * 50 + "\n"
        )

        for pid, data in product_summary.items():
            stock_left = int(df_products.at[pid, 'stock']) if pid in df_products.index else 'N/A'
            report_text += f"{pid:10} {data['qty']:>10} {data['total']:>12.2f} {str(stock_left):>12}\n"

        report_text += "-" * 50 + "\n"
        report_text += f"{'Total Transactions:':30} {len(df_filtered)}\n"
        report_text += f"{'Total Revenue($):':30} {total_revenue:.2f}\n"

        # --- Save as PDF option ---
        save_pdf = QMessageBox.question(
            dialog,
            "Save Report",
            "Do you want to save this report as a PDF?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if save_pdf == QMessageBox.StandardButton.Yes:
            filename, _ = QFileDialog.getSaveFileName(
                parent, "Save Report as PDF", "", "PDF Files (*.pdf)"
            )
            if filename:
                try:
                    from fpdf import FPDF
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Courier", size=10)
                    
                    # Replace emojis (FPDF can't encode them)
                    safe_text = (
                        report_text
                        .replace("📊", "")
                        .replace("👥", "")
                        .replace("🛍️", "")
                    )
                    
                    for line in safe_text.split("\n"):
                        # Encode safely to avoid Latin-1 error
                        pdf.cell(0, 5, line.encode('latin-1', 'replace').decode('latin-1'), ln=True)
                    
                    pdf.output(filename)
                    QMessageBox.information(parent, "Saved", f"Report saved as PDF:\n{filename}")
                except ImportError:
                    QMessageBox.warning(parent, "FPDF Missing", 
                                      "Install 'fpdf' package to save PDF:\npip install fpdf")
                except Exception as e:
                    QMessageBox.warning(parent, "Error", f"Failed to save PDF:\n{e}")

        QMessageBox.information(dialog, "Sales Report", report_text)
        dialog.accept()

    ok_btn.clicked.connect(generate)
    cancel_btn.clicked.connect(dialog.reject)
    dialog.exec()
