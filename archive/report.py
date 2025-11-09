import os
import pandas as pd
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QMessageBox,
    QDateEdit, QHBoxLayout, QFileDialog
)
from PyQt6.QtCore import QDate

def generate_sales_report(parent):
    sales_path = os.path.join("data", "sales.csv")
    product_path = os.path.join("data", "products.csv")

    # Check if sales.csv exists
    if not os.path.exists(sales_path) or os.stat(sales_path).st_size == 0:
        QMessageBox.information(parent, "No Data", "No sales data available yet to generate report.")
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
    layout = QVBoxLayout()

    start_label = QLabel("Select start date:")
    start_date_edit = QDateEdit()
    start_date_edit.setCalendarPopup(True)
    start_date_edit.setDate(QDate.currentDate())
    layout.addWidget(start_label)
    layout.addWidget(start_date_edit)

    end_label = QLabel("Select end date:")
    end_date_edit = QDateEdit()
    end_date_edit.setCalendarPopup(True)
    end_date_edit.setDate(QDate.currentDate())
    layout.addWidget(end_label)
    layout.addWidget(end_date_edit)

    button_layout = QHBoxLayout()
    ok_btn = QPushButton("Generate Report")
    cancel_btn = QPushButton("Cancel")
    button_layout.addWidget(ok_btn)
    button_layout.addWidget(cancel_btn)
    layout.addLayout(button_layout)
    dialog.setLayout(layout)

    # --- Generate report ---
    def generate():
        start_date = start_date_edit.date().toPyDate()
        end_date = end_date_edit.date().toPyDate()
        if start_date > end_date:
            QMessageBox.warning(dialog, "Date Error", "Start date must be before end date.")
            return

        # Filter sales by date
        df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
        mask = (df['datetime'].dt.date >= start_date) & (df['datetime'].dt.date <= end_date)
        df_filtered = df.loc[mask]

        if df_filtered.empty:
            QMessageBox.information(dialog, "No Data", "No sales in the selected date range.")
            return

        # --- Handle missing cashier/customer names ---
        cashiers = df_filtered['cashier_name'].fillna("Unknown").astype(str).unique()
        customers = df_filtered['customer_name'].fillna("Unknown").astype(str).unique()

        # Summary per product, including stock
        product_summary = {}
        total_revenue = 0.0
        for idx, row in df_filtered.iterrows():
            items = str(row['products']).split(',')
            for pid in items:
                price = float(df_products.at[pid, 'price']) if pid in df_products.index else 0.0
                total_revenue += price
                if pid not in product_summary:
                    product_summary[pid] = {'qty': 1, 'total': price}
                else:
                    product_summary[pid]['qty'] += 1
                    product_summary[pid]['total'] += price

        # Generate report text
        report_text = f"Sales Report from {start_date} to {end_date}\n\n"
        report_text += f"Cashiers involved: {', '.join(cashiers)}\n"
        report_text += f"Customers: {', '.join(customers)}\n\n"

        report_text += f"{'Product ID':10} {'Qty Sold':>10} {'Revenue($)':>12} {'Stock Left':>12}\n"
        report_text += "-"*50 + "\n"
        for pid, data in product_summary.items():
            stock_left = df_products.at[pid, 'stock'] if pid in df_products.index else 'N/A'
            report_text += f"{pid:10} {data['qty']:>10} {data['total']:>12.2f} {stock_left:>12}\n"

        report_text += "-"*50 + "\n"
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
            filename, _ = QFileDialog.getSaveFileName(parent, "Save Report as PDF", "", "PDF Files (*.pdf)")
            if filename:
                try:
                    from fpdf import FPDF  # pip install fpdf
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Courier", size=10)
                    for line in report_text.split('\n'):
                        pdf.cell(0, 5, line, ln=True)
                    pdf.output(filename)
                    QMessageBox.information(parent, "Saved", f"Report saved as PDF:\n{filename}")
                except ImportError:
                    QMessageBox.warning(parent, "FPDF Missing", "Install 'fpdf' package to save PDF:\npip install fpdf")
                except Exception as e:
                    QMessageBox.warning(parent, "Error", f"Failed to save PDF:\n{e}")

        QMessageBox.information(dialog, "Sales Report", report_text)
        dialog.accept()

    ok_btn.clicked.connect(generate)
    cancel_btn.clicked.connect(dialog.reject)
    dialog.exec()
