"""
TRANSLATION INTEGRATION GUIDE FOR main_prog_improved.py

This document shows how to integrate translations into the main cashier program.
Follow these steps to add bilingual support to the cashier interface.
"""

# ==============================================================================
# STEP 1: Import the translation helper
# ==============================================================================

# Add this import at the top of main_prog_improved.py:
from modules.translations.cashier_main_helper import tr_cashier
from modules.translations import LanguageManager


# ==============================================================================
# STEP 2: Make dialogs translation-aware
# ==============================================================================

class LargePaymentDialog(QDialog):
    """Large payment dialog with translation support"""
    
    def __init__(self, parent, total_amount):
        super().__init__(parent)
        
        # Store UI elements that need translation
        self.ui_elements = {}
        
        # Register for language changes
        LanguageManager.register_observer(self.update_translations)
        
        self.setWindowTitle(tr_cashier('payment_title'))
        # ... rest of initialization
    
    def init_ui(self):
        """Initialize with translated text"""
        # Title
        self.title_label = QLabel(tr_cashier('payment_title'))
        self.ui_elements['title'] = self.title_label
        
        # Total amount label
        self.total_label = QLabel(tr_cashier('payment_total_label'))
        self.ui_elements['total_label'] = self.total_label
        
        # Payment input label
        self.payment_label = QLabel(tr_cashier('payment_enter_label'))
        self.ui_elements['payment_label'] = self.payment_label
        
        # Payment input placeholder
        self.payment_input = QLineEdit()
        self.payment_input.setPlaceholderText(tr_cashier('payment_placeholder'))
        self.ui_elements['payment_input'] = self.payment_input
        
        # Confirm button
        self.confirm_btn = QPushButton(tr_cashier('payment_confirm'))
        self.ui_elements['confirm_btn'] = self.confirm_btn
        
        # Cancel button
        self.cancel_btn = QPushButton(tr_cashier('payment_cancel'))
        self.ui_elements['cancel_btn'] = self.cancel_btn
    
    def update_translations(self):
        """Update all text when language changes"""
        self.setWindowTitle(tr_cashier('payment_title'))
        self.ui_elements['title'].setText(tr_cashier('payment_title'))
        self.ui_elements['total_label'].setText(tr_cashier('payment_total_label'))
        self.ui_elements['payment_label'].setText(tr_cashier('payment_enter_label'))
        self.ui_elements['payment_input'].setPlaceholderText(tr_cashier('payment_placeholder'))
        self.ui_elements['confirm_btn'].setText(tr_cashier('payment_confirm'))
        self.ui_elements['cancel_btn'].setText(tr_cashier('payment_cancel'))
    
    def validate_payment(self):
        """Validate with translated error messages"""
        try:
            payment = float(self.payment_input.text())
            
            if payment < self.total_amount:
                error_msg = QMessageBox(self)
                error_msg.setWindowTitle(tr_cashier('payment_error_insufficient_title'))
                error_msg.setText(tr_cashier('payment_error_insufficient', 
                                             self.total_amount, payment, self.total_amount))
                error_msg.exec()
                return
            
            self.payment_amount = payment
            self.accept()
            
        except ValueError:
            error_msg = QMessageBox(self)
            error_msg.setWindowTitle(tr_cashier('payment_error_invalid_title'))
            error_msg.setText(tr_cashier('payment_error_invalid'))
            error_msg.exec()
    
    def closeEvent(self, event):
        """Clean up when closing"""
        LanguageManager.unregister_observer(self.update_translations)
        super().closeEvent(event)


# ==============================================================================
# STEP 3: Update LargeCompletionDialog
# ==============================================================================

class LargeCompletionDialog(QDialog):
    """Completion dialog with translation support"""
    
    def __init__(self, parent, payment, change):
        super().__init__(parent)
        self.ui_elements = {}
        LanguageManager.register_observer(self.update_translations)
        
        self.setWindowTitle(tr_cashier('completion_title'))
        # ... initialization
    
    def init_ui(self):
        """Initialize with translations"""
        self.title_label = QLabel(tr_cashier('completion_success'))
        self.ui_elements['title'] = self.title_label
        
        self.payment_label = QLabel(tr_cashier('completion_payment_label'))
        self.ui_elements['payment_label'] = self.payment_label
        
        self.change_label = QLabel(tr_cashier('completion_change_label'))
        self.ui_elements['change_label'] = self.change_label
        
        self.thank_you = QLabel(tr_cashier('completion_thank_you'))
        self.ui_elements['thank_you'] = self.thank_you
        
        self.ok_btn = QPushButton(tr_cashier('completion_ok'))
        self.ui_elements['ok_btn'] = self.ok_btn
    
    def update_translations(self):
        """Update translations"""
        self.setWindowTitle(tr_cashier('completion_title'))
        self.ui_elements['title'].setText(tr_cashier('completion_success'))
        self.ui_elements['payment_label'].setText(tr_cashier('completion_payment_label'))
        self.ui_elements['change_label'].setText(tr_cashier('completion_change_label'))
        self.ui_elements['thank_you'].setText(tr_cashier('completion_thank_you'))
        self.ui_elements['ok_btn'].setText(tr_cashier('completion_ok'))
    
    def closeEvent(self, event):
        LanguageManager.unregister_observer(self.update_translations)
        super().closeEvent(event)


# ==============================================================================
# STEP 4: Update LargeCustomerNameDialog
# ==============================================================================

class LargeCustomerNameDialog(QDialog):
    """Customer name dialog with translation support"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.ui_elements = {}
        LanguageManager.register_observer(self.update_translations)
        
        self.customer_name = tr_cashier('customer_default')
        self.setWindowTitle(tr_cashier('customer_title'))
        # ... initialization
    
    def init_ui(self):
        """Initialize with translations"""
        self.title_label = QLabel(tr_cashier('customer_title'))
        self.ui_elements['title'] = self.title_label
        
        self.instructions = QLabel(tr_cashier('customer_instructions'))
        self.ui_elements['instructions'] = self.instructions
        
        self.name_label = QLabel(tr_cashier('customer_name_label'))
        self.ui_elements['name_label'] = self.name_label
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText(tr_cashier('customer_name_placeholder'))
        self.name_input.setText(tr_cashier('customer_default'))
        self.ui_elements['name_input'] = self.name_input
        
        self.ok_btn = QPushButton(tr_cashier('customer_ok'))
        self.ui_elements['ok_btn'] = self.ok_btn
        
        self.skip_btn = QPushButton(tr_cashier('customer_skip'))
        self.ui_elements['skip_btn'] = self.skip_btn
    
    def update_translations(self):
        """Update translations"""
        self.setWindowTitle(tr_cashier('customer_title'))
        self.ui_elements['title'].setText(tr_cashier('customer_title'))
        self.ui_elements['instructions'].setText(tr_cashier('customer_instructions'))
        self.ui_elements['name_label'].setText(tr_cashier('customer_name_label'))
        self.ui_elements['name_input'].setPlaceholderText(tr_cashier('customer_name_placeholder'))
        self.ui_elements['ok_btn'].setText(tr_cashier('customer_ok'))
        self.ui_elements['skip_btn'].setText(tr_cashier('customer_skip'))
    
    def skip_name(self):
        """Skip with translated default"""
        self.customer_name = tr_cashier('customer_default')
        self.accept()
    
    def closeEvent(self, event):
        LanguageManager.unregister_observer(self.update_translations)
        super().closeEvent(event)


# ==============================================================================
# STEP 5: Update AkbarCashier Main Window
# ==============================================================================

class AkbarCashier(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Store UI elements
        self.ui_elements = {}
        
        # Register for language changes
        LanguageManager.register_observer(self.update_translations)
        
        self.setWindowTitle(tr_cashier('window_title'))
        # ... rest of initialization
    
    def init_ui(self):
        """Initialize UI with translations"""
        
        # Title
        self.title_label = QLabel(tr_cashier('title'))
        self.ui_elements['title'] = self.title_label
        
        # Cashier label
        self.cashier_label = QLabel(f"👤 {tr_cashier('cashier_label')}: {self.cashier_name} ({tr_cashier('id_label')}: {self.employee_id})")
        self.ui_elements['cashier_label'] = self.cashier_label
        
        # Catalog title
        catalog_title = QLabel(tr_cashier('catalog_title'))
        self.ui_elements['catalog_title'] = catalog_title
        
        # Cart title
        self.cart_label = QLabel(f"{tr_cashier('cart_title')}\n\n{tr_cashier('cart_empty')}")
        self.ui_elements['cart_label'] = self.cart_label
        
        # Buttons
        self.checkout_btn = QPushButton(tr_cashier('checkout_btn'))
        self.ui_elements['checkout_btn'] = self.checkout_btn
        
        self.cancel_btn = QPushButton(tr_cashier('cancel_btn'))
        self.ui_elements['cancel_btn'] = self.cancel_btn
        
        self.print_btn = QPushButton(tr_cashier('print_btn'))
        self.ui_elements['print_btn'] = self.print_btn
        
        self.pdf_btn = QPushButton(tr_cashier('save_pdf_btn'))
        self.ui_elements['pdf_btn'] = self.pdf_btn
        
        self.report_btn = QPushButton(tr_cashier('report_btn'))
        self.ui_elements['report_btn'] = self.report_btn
    
    def update_translations(self):
        """Update all translations when language changes"""
        self.setWindowTitle(tr_cashier('window_title'))
        self.ui_elements['title'].setText(tr_cashier('title'))
        self.ui_elements['cashier_label'].setText(f"👤 {tr_cashier('cashier_label')}: {self.cashier_name} ({tr_cashier('id_label')}: {self.employee_id})")
        self.ui_elements['catalog_title'].setText(tr_cashier('catalog_title'))
        self.ui_elements['checkout_btn'].setText(tr_cashier('checkout_btn'))
        self.ui_elements['cancel_btn'].setText(tr_cashier('cancel_btn'))
        self.ui_elements['print_btn'].setText(tr_cashier('print_btn'))
        self.ui_elements['pdf_btn'].setText(tr_cashier('save_pdf_btn'))
        self.ui_elements['report_btn'].setText(tr_cashier('report_btn'))
        
        # Update cart display
        self.update_cart_label()
    
    def update_cart_label(self):
        """Update cart with translated text"""
        text = f"{tr_cashier('cart_title')}\n\n"
        summary = {}
        for pid in self.cart:
            summary[pid] = summary.get(pid, 0) + 1
        
        if not summary:
            text += tr_cashier('cart_empty') + "\n"
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
            text += f"{tr_cashier('cart_total')}: ${grand_total:.2f}\n"
        
        self.cart_label.setText(text)
    
    def open_catalog_dialog(self, catalog_prefix):
        """Open catalog with translated text"""
        dialog = QDialog(self)
        dialog.setWindowTitle(f"{tr_cashier('catalog_dialog_title')}: {catalog_prefix}")
        
        # Title
        title = QLabel(f"📂 {catalog_prefix} {tr_cashier('catalog_products')}")
        # ... rest of dialog
        
        # Close button
        close_btn = QPushButton(tr_cashier('catalog_close'))
        # ... rest of setup
    
    def add_to_cart(self, product_id):
        """Add to cart with translated messages"""
        product = self.products[self.products['product_id'] == product_id].iloc[0]
        current_qty_in_cart = self.cart.count(product_id)
        
        if product['stock'] <= current_qty_in_cart:
            QMessageBox.warning(self, tr_cashier('out_of_stock_title'), 
                              tr_cashier('out_of_stock_msg', product['name'], product['stock']))
            return
        
        self.cart.append(product_id)
        self.update_cart_label()
    
    def checkout(self):
        """Checkout with translated messages"""
        if not self.cart:
            QMessageBox.information(self, tr_cashier('empty_cart_title'), 
                                  tr_cashier('empty_cart_msg'))
            return
        
        # ... rest of checkout process
    
    def cancel_item(self):
        """Cancel item with translated messages"""
        if not self.cart:
            QMessageBox.information(self, tr_cashier('no_items_title'), 
                                  tr_cashier('no_items_msg'))
            return
        # ... rest of cancel logic
    
    def print_receipt(self):
        """Print with translated messages"""
        if not self.receipt_display.toPlainText().strip():
            QMessageBox.warning(self, tr_cashier('no_receipt_title'), 
                              tr_cashier('no_receipt_print'))
            return
        # ... rest of print logic
        
        QMessageBox.information(self, tr_cashier('ready_title'), 
                              tr_cashier('ready_msg'))
    
    def print_receipt_to_pdf(self):
        """Save PDF with translated messages"""
        if not self.receipt_display.toPlainText().strip():
            QMessageBox.warning(self, tr_cashier('no_receipt_title'), 
                              tr_cashier('no_receipt_save'))
            return
        # ... save logic
        
        if filename:
            QMessageBox.information(self, tr_cashier('receipt_saved_title'), 
                                  tr_cashier('receipt_saved_msg', filename))
    
    def show_stock_summary(self):
        """Show stock with translated messages"""
        low_stock = self.products[self.products['stock'] <= 5]
        msg = tr_cashier('stock_summary_total', len(self.products)) + "\n\n"
        
        if not low_stock.empty:
            msg += tr_cashier('stock_summary_low') + "\n\n"
            for _, p in low_stock.iterrows():
                msg += f"  • {p['name']}\n"
                msg += f"    {tr_cashier('stock_id')}: {p['product_id']}\n"
                msg += f"    {tr_cashier('stock_remaining', p['stock'])}\n\n"
        else:
            msg += tr_cashier('stock_summary_ok')
        
        QMessageBox.information(self, tr_cashier('stock_summary_title'), msg)
    
    def closeEvent(self, event):
        """Clean up when closing"""
        LanguageManager.unregister_observer(self.update_translations)
        super().closeEvent(event)


# ==============================================================================
# SUMMARY OF CHANGES NEEDED
# ==============================================================================

"""
1. Add imports at top:
   - from modules.translations.cashier_main_helper import tr_cashier
   - from modules.translations import LanguageManager

2. For each dialog class:
   - Add self.ui_elements = {} in __init__
   - Register observer: LanguageManager.register_observer(self.update_translations)
   - Store all QLabel and QPushButton widgets in self.ui_elements
   - Add update_translations() method
   - Unregister in closeEvent()

3. For AkbarCashier main window:
   - Add self.ui_elements = {}
   - Register observer
   - Replace all hardcoded strings with tr_cashier('key')
   - Add update_translations() method
   - Unregister in closeEvent()

4. Replace all message box strings:
   - QMessageBox.information(self, tr_cashier('title'), tr_cashier('message'))
   - QMessageBox.warning(self, tr_cashier('title'), tr_cashier('message'))

5. Update dialog titles:
   - dialog.setWindowTitle(tr_cashier('dialog_title'))

6. Catalog button text:
   - For "X items": f"📁\n{prefix}\n({count} {tr_cashier('items_suffix')})"

This provides complete bilingual support with instant language switching!
"""
