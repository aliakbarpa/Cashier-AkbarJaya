"""
REPORT MODULE - ENHANCED DAILY REPORT
Includes top-selling products, frequent customers, and per-day summaries.
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
    """Generate detailed sales report with date range filter and daily breakdown."""
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

    # Load products for stock/price
    try:
        df_products = pd.read_csv(product_path)
        df_products.set_index("product_id", inplace=True)
    except:
        df_products = pd.DataFrame(columns=["product_id", "name", "price", "stock"])
        df_products.set_index("product_id", inplace=True)

    # --- Date selection dialog ---
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

    # --- Generate report logic ---
    def generate():
        start_date = start_date_edit.date().toPyDate()
        end_date = end_date_edit.date().toPyDate()
        if start_date > end_date:
            QMessageBox.warning(dialog, "Date Error", "Start date must be before end date.")
            return

        # Filter data
        df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
        mask = (df['datetime'].dt.date >= start_date) & (df['datetime'].dt.date <= end_date)
        df_filtered = df.loc[mask]

        if df_filtered.empty:
            QMessageBox.information(dialog, "No Data", "No sales in the selected range.")
            return

        # Prepare report text
        report_pages = []

        for day, day_data in df_filtered.groupby(df_filtered['datetime'].dt.date):
            cashiers = day_data['cashier_name'].fillna("Unknown").astype(str).unique()
            customers = day_data['customer_name'].fillna("Unknown").astype(str).unique()

            product_summary = {}
            for _, row in day_data.iterrows():
                items = str(row.get('products', '')).split(',')
                for pid in [i.strip() for i in items if i.strip()]:
                    if pid in df_products.index:
                        try:
                            price = float(df_products.at[pid, 'price'])
                        except (KeyError, ValueError):
                            price = 0.0
                    else:
                        price = 0.0

                    if pid not in product_summary:
                        product_summary[pid] = {'qty': 1, 'total': price}
                    else:
                        product_summary[pid]['qty'] += 1
                        product_summary[pid]['total'] += price

            # Top-selling products
            top_products = sorted(product_summary.items(), key=lambda x: x[1]['qty'], reverse=True)
            top5 = top_products[:5]

            # Frequent customers
            frequent_customers = (
                day_data['customer_name'].fillna("Unknown").value_counts().head(3)
            )

            total_revenue = sum(p['total'] for p in product_summary.values())
            total_transactions = len(day_data)

            page_text = f"📅 SALES REPORT - {day}\n"
            page_text += f"Cashiers: {', '.join(cashiers)}\n"
            page_text += f"Customers: {', '.join(customers)}\n"
            page_text += "-"*55 + "\n"
            page_text += f"{'Product ID':10} {'Qty Sold':>10} {'Revenue($)':>12} {'Stock Left':>12}\n"
            page_text += "-"*55 + "\n"
            for pid, data in product_summary.items():
                stock_left = df_products.at[pid, 'stock'] if pid in df_products.index else 'N/A'
                page_text += f"{pid:10} {data['qty']:>10} {data['total']:>12.2f} {str(stock_left):>12}\n"
            page_text += "-"*55 + "\n"
            page_text += f"Total Transactions: {total_transactions}\n"
            page_text += f"Total Revenue($): {total_revenue:.2f}\n\n"

            # --- Top 5 products ---
            page_text += "🏆 Top-Selling Products:\n"
            for pid, data in top5:
                pname = df_products.at[pid, 'name'] if pid in df_products.index else pid
                page_text += f"  - {pname} ({pid}): {data['qty']} sold\n"
            page_text += "\n"

            # --- Frequent customers ---
            page_text += "🙋 Frequent Customers:\n"
            for cust, count in frequent_customers.items():
                page_text += f"  - {cust}: {count} purchases\n"

            report_pages.append(page_text)

        # Ask to save as PDF
        save_pdf = QMessageBox.question(
            dialog,
            "Save Report",
            "Do you want to save this report as a PDF (1 page per day)?",
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
                    pdf.set_auto_page_break(auto=True, margin=15)
                    for page_text in report_pages:
                        pdf.add_page()
                        pdf.set_font("Courier", size=10)
                        for line in page_text.split("\n"):
                            # Encode as latin-1-safe
                            line_safe = line.encode('latin-1', 'replace').decode('latin-1')
                            pdf.cell(0, 5, line_safe, ln=True)
                    pdf.output(filename)
                    QMessageBox.information(parent, "Saved", f"Report saved:\n{filename}")
                except Exception as e:
                    QMessageBox.warning(parent, "Error", f"Failed to save PDF:\n{e}")

        # Show in popup summary
        QMessageBox.information(parent, "Report Generated", "\n\n".join(report_pages[:1]))
        dialog.accept()

    ok_btn.clicked.connect(generate)
    cancel_btn.clicked.connect(dialog.reject)
    dialog.exec()
