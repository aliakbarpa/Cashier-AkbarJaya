# 🔧 TRANSLATION IMPLEMENTATION - COMPLETE CHANGES

**Status**: Ready to implement  
**File to modify**: `main_prog_improved.py`  
**Changes needed**: Add translation support throughout

---

## ✅ STEP 1: ADD IMPORTS (After line 28)

```python
# Add these imports after the WelcomeScreen import
from modules.translations.cashier_main_helper import tr_cashier
from modules.translations import LanguageManager
```

Complete imports section should look like:
```python
# Import our custom modules
from receipt_improved import generate_receipt_text
from report_improved import generate_sales_report
from modules.welcome_screen import WelcomeScreen
from modules.translations.cashier_main_helper import tr_cashier  # NEW
from modules.translations import LanguageManager  # NEW
```

---

## ✅ STEP 2: UPDATE LargePaymentDialog Class

### In `__init__` method (around line 32):

**FIND:**
```python
def __init__(self, parent, total_amount):
    super().__init__(parent)
    self.setWindowTitle("Payment")
    self.setGeometry(250, 150, 900, 700)
    self.setStyleSheet("QDialog { background-color: #f8fafc; }")
    self.setModal(True)
    
    self.total_amount = total_amount
    self.payment_amount = 0.0
    
    self.init_ui()
```

**REPLACE WITH:**
```python
def __init__(self, parent, total_amount):
    super().__init__(parent)
    self.setWindowTitle(tr_cashier('payment_title'))  # CHANGED
    self.setGeometry(250, 150, 900, 700)
    self.setStyleSheet("QDialog { background-color: #f8fafc; }")
    self.setModal(True)
    
    self.total_amount = total_amount
    self.payment_amount = 0.0
    
    # ADD THESE LINES
    self.ui_elements = {}
    LanguageManager.register_observer(self.update_translations)
    
    self.init_ui()
```

### In `init_ui` method (around line 44):

**FIND AND REPLACE each hardcoded string:**

1. Title label:
```python
# OLD:
title = QLabel("💳 PAYMENT")

# NEW:
self.title_label = QLabel(tr_cashier('payment_title'))
self.ui_elements['title'] = self.title_label
```

2. Total label:
```python
# OLD:
total_label = QLabel(f"TOTAL AMOUNT:")

# NEW:
self.total_label = QLabel(tr_cashier('payment_total_label'))
self.ui_elements['total_label'] = self.total_label
```

3. Payment label:
```python
# OLD:
payment_label = QLabel("💵 Enter Payment Received:")

# NEW:
self.payment_label = QLabel(tr_cashier('payment_enter_label'))
self.ui_elements['payment_label'] = self.payment_label
```

4. Placeholder text:
```python
# OLD:
self.payment_input.setPlaceholderText("0.00")

# NEW:
self.payment_input.setPlaceholderText(tr_cashier('payment_placeholder'))
self.ui_elements['payment_input'] = self.payment_input
```

5. Confirm button:
```python
# OLD:
confirm_btn = QPushButton("✅\nCONFIRM\nPAYMENT")

# NEW:
self.confirm_btn = QPushButton(tr_cashier('payment_confirm'))
self.ui_elements['confirm_btn'] = self.confirm_btn
```

6. Cancel button:
```python
# OLD:
cancel_btn = QPushButton("❌\nCANCEL")

# NEW:
self.cancel_btn = QPushButton(tr_cashier('payment_cancel'))
self.ui_elements['cancel_btn'] = self.cancel_btn
```

### In `validate_payment` method (around line 161):

**FIND:**
```python
error_msg.setWindowTitle("Insufficient Payment")
error_msg.setText(f"⚠️ INSUFFICIENT PAYMENT\n\n"
                f"Required: ${self.total_amount:.2f}\n"
                f"Received: ${payment:.2f}\n\n"
                f"Please enter at least ${self.total_amount:.2f}")
```

**REPLACE WITH:**
```python
error_msg.setWindowTitle(tr_cashier('payment_error_insufficient_title'))
error_msg.setText(tr_cashier('payment_error_insufficient', 
                             self.total_amount, payment, self.total_amount))
```

**FIND:**
```python
error_msg.setWindowTitle("Invalid Input")
error_msg.setText("⚠️ INVALID AMOUNT\n\nPlease enter a valid number!")
```

**REPLACE WITH:**
```python
error_msg.setWindowTitle(tr_cashier('payment_error_invalid_title'))
error_msg.setText(tr_cashier('payment_error_invalid'))
```

### ADD NEW METHODS to LargePaymentDialog class (before the class ends):

```python
def update_translations(self):
    """Update all text when language changes"""
    self.setWindowTitle(tr_cashier('payment_title'))
    self.ui_elements['title'].setText(tr_cashier('payment_title'))
    self.ui_elements['total_label'].setText(tr_cashier('payment_total_label'))
    self.ui_elements['payment_label'].setText(tr_cashier('payment_enter_label'))
    self.ui_elements['payment_input'].setPlaceholderText(tr_cashier('payment_placeholder'))
    self.ui_elements['confirm_btn'].setText(tr_cashier('payment_confirm'))
    self.ui_elements['cancel_btn'].setText(tr_cashier('payment_cancel'))

def closeEvent(self, event):
    """Clean up when closing"""
    LanguageManager.unregister_observer(self.update_translations)
    super().closeEvent(event)
```

---

## ✅ STEP 3: UPDATE LargeCompletionDialog Class

### In `__init__` method:

**FIND:**
```python
def __init__(self, parent, payment, change):
    super().__init__(parent)
    self.setWindowTitle("Transaction Complete")
```

**REPLACE WITH:**
```python
def __init__(self, parent, payment, change):
    super().__init__(parent)
    self.setWindowTitle(tr_cashier('completion_title'))  # CHANGED
    
    self.ui_elements = {}  # ADD
    LanguageManager.register_observer(self.update_translations)  # ADD
```

### In `init_ui` method, FIND AND REPLACE:

1. Success title:
```python
# OLD:
title = QLabel("✅ TRANSACTION\nCOMPLETE!")

# NEW:
self.title_label = QLabel(tr_cashier('completion_success'))
self.ui_elements['title'] = self.title_label
```

2. Payment label:
```python
# OLD:
payment_label = QLabel("💵 Payment Received:")

# NEW:
self.payment_label = QLabel(tr_cashier('completion_payment_label'))
self.ui_elements['payment_label'] = self.payment_label
```

3. Change label:
```python
# OLD:
change_label = QLabel("💰 Change to Return:")

# NEW:
self.change_label = QLabel(tr_cashier('completion_change_label'))
self.ui_elements['change_label'] = self.change_label
```

4. Thank you:
```python
# OLD:
thank_you = QLabel("🙏 Thank You!")

# NEW:
self.thank_you = QLabel(tr_cashier('completion_thank_you'))
self.ui_elements['thank_you'] = self.thank_you
```

5. OK button:
```python
# OLD:
ok_btn = QPushButton("✅\nOK")

# NEW:
self.ok_btn = QPushButton(tr_cashier('completion_ok'))
self.ui_elements['ok_btn'] = self.ok_btn
```

### ADD NEW METHODS to LargeCompletionDialog:

```python
def update_translations(self):
    """Update all text when language changes"""
    self.setWindowTitle(tr_cashier('completion_title'))
    self.ui_elements['title'].setText(tr_cashier('completion_success'))
    self.ui_elements['payment_label'].setText(tr_cashier('completion_payment_label'))
    self.ui_elements['change_label'].setText(tr_cashier('completion_change_label'))
    self.ui_elements['thank_you'].setText(tr_cashier('completion_thank_you'))
    self.ui_elements['ok_btn'].setText(tr_cashier('completion_ok'))

def closeEvent(self, event):
    """Clean up when closing"""
    LanguageManager.unregister_observer(self.update_translations)
    super().closeEvent(event)
```

---

## ✅ STEP 4: UPDATE LargeCustomerNameDialog Class

### In `__init__` method:

**FIND:**
```python
def __init__(self, parent):
    super().__init__(parent)
    self.setWindowTitle("Customer Name")
    self.resize(900, 600)
    self.setStyleSheet("QDialog { background-color: #f8fafc; }")
    self.setModal(True)
    
    self.customer_name = "Customer"
```

**REPLACE WITH:**
```python
def __init__(self, parent):
    super().__init__(parent)
    self.setWindowTitle(tr_cashier('customer_title'))  # CHANGED
    self.resize(900, 600)
    self.setStyleSheet("QDialog { background-color: #f8fafc; }")
    self.setModal(True)
    
    self.customer_name = tr_cashier('customer_default')  # CHANGED
    
    # ADD THESE LINES
    self.ui_elements = {}
    LanguageManager.register_observer(self.update_translations)
```

### In `init_ui` method, FIND AND REPLACE:

1. Title:
```python
# OLD:
title = QLabel("👤 CUSTOMER NAME")

# NEW:
self.title_label = QLabel(tr_cashier('customer_title'))
self.ui_elements['title'] = self.title_label
```

2. Instructions:
```python
# OLD:
instructions = QLabel("Please enter the customer's name:")

# NEW:
self.instructions = QLabel(tr_cashier('customer_instructions'))
self.ui_elements['instructions'] = self.instructions
```

3. Name label:
```python
# OLD:
name_label = QLabel("📝 Customer Name:")

# NEW:
self.name_label = QLabel(tr_cashier('customer_name_label'))
self.ui_elements['name_label'] = self.name_label
```

4. Name input:
```python
# OLD:
self.name_input.setPlaceholderText("Enter name here...")
self.name_input.setText("Customer")

# NEW:
self.name_input.setPlaceholderText(tr_cashier('customer_name_placeholder'))
self.name_input.setText(tr_cashier('customer_default'))
self.ui_elements['name_input'] = self.name_input
```

5. OK button:
```python
# OLD:
ok_btn = QPushButton("✅\nOK")

# NEW:
self.ok_btn = QPushButton(tr_cashier('customer_ok'))
self.ui_elements['ok_btn'] = self.ok_btn
```

6. Skip button:
```python
# OLD:
skip_btn = QPushButton("⏭️\nSKIP\n(Use 'Customer')")

# NEW:
self.skip_btn = QPushButton(tr_cashier('customer_skip'))
self.ui_elements['skip_btn'] = self.skip_btn
```

### Update `accept_name` method:

**FIND:**
```python
def accept_name(self):
    """Accept the entered name"""
    name = self.name_input.text().strip()
    if name:
        self.customer_name = name
    else:
        self.customer_name = "Customer"
    self.accept()
```

**REPLACE WITH:**
```python
def accept_name(self):
    """Accept the entered name"""
    name = self.name_input.text().strip()
    if name:
        self.customer_name = name
    else:
        self.customer_name = tr_cashier('customer_default')  # CHANGED
    self.accept()
```

### Update `skip_name` method:

**FIND:**
```python
def skip_name(self):
    """Skip and use default 'Customer'"""
    self.customer_name = "Customer"
    self.accept()
```

**REPLACE WITH:**
```python
def skip_name(self):
    """Skip and use default 'Customer'"""
    self.customer_name = tr_cashier('customer_default')  # CHANGED
    self.accept()
```

### ADD NEW METHODS to LargeCustomerNameDialog:

```python
def update_translations(self):
    """Update all text when language changes"""
    self.setWindowTitle(tr_cashier('customer_title'))
    self.ui_elements['title'].setText(tr_cashier('customer_title'))
    self.ui_elements['instructions'].setText(tr_cashier('customer_instructions'))
    self.ui_elements['name_label'].setText(tr_cashier('customer_name_label'))
    self.ui_elements['name_input'].setPlaceholderText(tr_cashier('customer_name_placeholder'))
    self.ui_elements['ok_btn'].setText(tr_cashier('customer_ok'))
    self.ui_elements['skip_btn'].setText(tr_cashier('customer_skip'))

def closeEvent(self, event):
    """Clean up when closing"""
    LanguageManager.unregister_observer(self.update_translations)
    super().closeEvent(event)
```

---

## ✅ STEP 5: UPDATE AkbarCashier Class

This is the main class with many changes.

### In `__init__` method, ADD AFTER `self.cart = []`:

```python
self.cart = []

# ADD THESE LINES:
self.ui_elements = {}
LanguageManager.register_observer(self.update_translations)
```

### FIND AND REPLACE window title:

**FIND:**
```python
self.setWindowTitle("Akbar Jaya Cashier System - Enhanced UI v1.8")
```

**REPLACE WITH:**
```python
self.setWindowTitle(tr_cashier('window_title'))
```

### FIND AND REPLACE title label:

**FIND:**
```python
# Title
self.title_label = QLabel("AKBAR JAYA")
```

**ADD AFTER creating the label:**
```python
self.title_label = QLabel(tr_cashier('title'))
self.ui_elements['title'] = self.title_label  # ADD THIS LINE
```

### FIND AND REPLACE cashier label:

**FIND:**
```python
self.cashier_label.setText(f"👤 Cashier: {self.cashier_name} (ID: {self.employee_id})")
```

**REPLACE WITH:**
```python
self.cashier_label.setText(f"👤 {tr_cashier('cashier_label')}: {self.cashier_name} ({tr_cashier('id_label')}: {self.employee_id})")
self.ui_elements['cashier'] = self.cashier_label  # ADD THIS LINE
```

### FIND AND REPLACE catalog title:

**FIND:**
```python
catalog_title = QLabel("📂 Product Catalog")
```

**REPLACE WITH:**
```python
self.catalog_title = QLabel(tr_cashier('catalog_title'))
self.ui_elements['catalog_title'] = self.catalog_title
```

(Then use `self.catalog_title` instead of `catalog_title` when adding to layout)

### FIND AND REPLACE cart label initialization:

**FIND:**
```python
self.cart_label = QLabel("🛒 Shopping Cart:\n\n  (Empty)")
```

**REPLACE WITH:**
```python
self.cart_label = QLabel(f"{tr_cashier('cart_title')}\n\n{tr_cashier('cart_empty')}")
self.ui_elements['cart_label'] = self.cart_label
```

### FIND AND REPLACE all buttons:

1. Checkout button:
```python
# OLD:
self.checkout_btn = QPushButton("💳\nCHECKOUT")

# NEW:
self.checkout_btn = QPushButton(tr_cashier('checkout_btn'))
self.ui_elements['checkout_btn'] = self.checkout_btn
```

2. Cancel button:
```python
# OLD:
self.cancel_btn = QPushButton("❌\nCANCEL")

# NEW:
self.cancel_btn = QPushButton(tr_cashier('cancel_btn'))
self.ui_elements['cancel_btn'] = self.cancel_btn
```

3. Print button:
```python
# OLD:
self.print_btn = QPushButton("🖨️\nPRINT")

# NEW:
self.print_btn = QPushButton(tr_cashier('print_btn'))
self.ui_elements['print_btn'] = self.print_btn
```

4. PDF button:
```python
# OLD:
self.pdf_btn = QPushButton("📄\nSAVE PDF")

# NEW:
self.pdf_btn = QPushButton(tr_cashier('save_pdf_btn'))
self.ui_elements['pdf_btn'] = self.pdf_btn
```

5. Report button:
```python
# OLD:
self.report_btn = QPushButton("📊\nREPORT")

# NEW:
self.report_btn = QPushButton(tr_cashier('report_btn'))
self.ui_elements['report_btn'] = self.report_btn
```

### In `update_cart_label` method:

**FIND:**
```python
def update_cart_label(self):
    text = "🛒 Shopping Cart:\n\n"
    summary = {}
    for pid in self.cart:
        summary[pid] = summary.get(pid, 0) + 1
    
    if not summary:
        text += "  (Empty)\n"
    else:
        # ... rest of code
        text += f"───────────────────\n"
        text += f"TOTAL: ${grand_total:.2f}\n"
```

**REPLACE WITH:**
```python
def update_cart_label(self):
    text = f"{tr_cashier('cart_title')}\n\n"  # CHANGED
    summary = {}
    for pid in self.cart:
        summary[pid] = summary.get(pid, 0) + 1
    
    if not summary:
        text += f"{tr_cashier('cart_empty')}\n"  # CHANGED
    else:
        # ... rest of code stays same
        text += f"───────────────────\n"
        text += f"{tr_cashier('cart_total')}: ${grand_total:.2f}\n"  # CHANGED
```

### In `refresh_product_list` method, FIND:

```python
btn = QPushButton(f"📁\n{prefix}\n({count} items)")
```

**REPLACE WITH:**
```python
btn = QPushButton(f"📁\n{prefix}\n({count} {tr_cashier('items_suffix')})")
```

### In `open_catalog_dialog` method:

**FIND:**
```python
dialog.setWindowTitle(f"Catalog: {catalog_prefix}")
```

**REPLACE WITH:**
```python
dialog.setWindowTitle(f"{tr_cashier('catalog_dialog_title')}: {catalog_prefix}")
```

**FIND:**
```python
title = QLabel(f"📂 {catalog_prefix} Products")
```

**REPLACE WITH:**
```python
title = QLabel(f"📂 {catalog_prefix} {tr_cashier('catalog_products')}")
```

**FIND:**
```python
close_btn = QPushButton("❌ Close")
```

**REPLACE WITH:**
```python
close_btn = QPushButton(tr_cashier('catalog_close'))
```

### In `add_to_cart` method:

**FIND:**
```python
QMessageBox.warning(self, "Out of Stock", 
                  f"{product['name']} has only {product['stock']} left in stock!")
```

**REPLACE WITH:**
```python
QMessageBox.warning(self, tr_cashier('out_of_stock_title'), 
                  tr_cashier('out_of_stock_msg', product['name'], product['stock']))
```

### In `show_stock_summary` method:

**FIND:**
```python
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
```

**REPLACE WITH:**
```python
def show_stock_summary(self):
    low_stock = self.products[self.products['stock'] <= 5]
    msg = f"{tr_cashier('stock_summary_total', len(self.products))}\n\n"
    
    if not low_stock.empty:
        msg += f"{tr_cashier('stock_summary_low')}\n\n"
        for _, p in low_stock.iterrows():
            msg += f"  • {p['name']}\n"
            msg += f"    {tr_cashier('stock_id')}: {p['product_id']}\n"
            msg += f"    {tr_cashier('stock_remaining', p['stock'])}\n\n"
    else:
        msg += tr_cashier('stock_summary_ok')
    
    QMessageBox.information(self, tr_cashier('stock_summary_title'), msg)
```

### In `checkout` method:

**FIND:**
```python
if not self.cart:
    QMessageBox.information(self, "Empty Cart", "Your cart is empty!")
    return
```

**REPLACE WITH:**
```python
if not self.cart:
    QMessageBox.information(self, tr_cashier('empty_cart_title'), 
                          tr_cashier('empty_cart_msg'))
    return
```

**FIND:**
```python
if not ok or payment < total:
    QMessageBox.warning(self, "Payment Error", 
                      f"Payment must be at least ${total:.2f}.")
    return
```

**REPLACE WITH:**
```python
if not ok or payment < total:
    QMessageBox.warning(self, tr_cashier('payment_error_title'), 
                      tr_cashier('payment_error_msg', total))
    return
```

**FIND:**
```python
else:
    customer_name = "Customer"
```

**REPLACE WITH:**
```python
else:
    customer_name = tr_cashier('customer_default')
```

### In `print_receipt` method:

**FIND:**
```python
if not self.receipt_display.toPlainText().strip():
    QMessageBox.warning(self, "No Receipt", "No receipt to print.")
    return
```

**REPLACE WITH:**
```python
if not self.receipt_display.toPlainText().strip():
    QMessageBox.warning(self, tr_cashier('no_receipt_title'), 
                      tr_cashier('no_receipt_print'))
    return
```

**FIND:**
```python
QMessageBox.information(self, "Ready", "✅ Transaction completed!")
```

**REPLACE WITH:**
```python
QMessageBox.information(self, tr_cashier('ready_title'), 
                      tr_cashier('ready_msg'))
```

### In `print_receipt_to_pdf` method:

**FIND:**
```python
if not self.receipt_display.toPlainText().strip():
    QMessageBox.warning(self, "No Receipt", "No receipt to save.")
    return
```

**REPLACE WITH:**
```python
if not self.receipt_display.toPlainText().strip():
    QMessageBox.warning(self, tr_cashier('no_receipt_title'), 
                      tr_cashier('no_receipt_save'))
    return
```

**FIND:**
```python
QMessageBox.information(self, "Saved", f"✅ Receipt saved as PDF:\n{filename}")
```

**REPLACE WITH:**
```python
QMessageBox.information(self, tr_cashier('receipt_saved_title'), 
                      tr_cashier('receipt_saved_msg', filename))
```

### In `cancel_item` method:

**FIND:**
```python
if not self.cart:
    QMessageBox.information(self, "Cart Empty", "No items to cancel.")
    return
```

**REPLACE WITH:**
```python
if not self.cart:
    QMessageBox.information(self, tr_cashier('no_items_title'), 
                          tr_cashier('no_items_msg'))
    return
```

**FIND:**
```python
item, ok = QInputDialog.getItem(
    self, "Cancel Item", "Select item to remove:", items_list, 0, False
)
```

**REPLACE WITH:**
```python
item, ok = QInputDialog.getItem(
    self, tr_cashier('cancel_item_title'), tr_cashier('cancel_item_prompt'), 
    items_list, 0, False
)
```

**FIND:**
```python
QMessageBox.information(self, "Item Removed", f"✅ {item} removed from cart.")
```

**REPLACE WITH:**
```python
QMessageBox.information(self, tr_cashier('item_removed_title'), 
                      tr_cashier('item_removed_msg', item))
```

### ADD NEW METHOD to AkbarCashier class (before closing the class):

```python
def update_translations(self):
    """Update all translations when language changes"""
    self.setWindowTitle(tr_cashier('window_title'))
    self.ui_elements['title'].setText(tr_cashier('title'))
    self.ui_elements['cashier'].setText(
        f"👤 {tr_cashier('cashier_label')}: {self.cashier_name} "
        f"({tr_cashier('id_label')}: {self.employee_id})"
    )
    self.ui_elements['catalog_title'].setText(tr_cashier('catalog_title'))
    self.ui_elements['checkout_btn'].setText(tr_cashier('checkout_btn'))
    self.ui_elements['cancel_btn'].setText(tr_cashier('cancel_btn'))
    self.ui_elements['print_btn'].setText(tr_cashier('print_btn'))
    self.ui_elements['pdf_btn'].setText(tr_cashier('save_pdf_btn'))
    self.ui_elements['report_btn'].setText(tr_cashier('report_btn'))
    self.update_cart_label()
    self.refresh_product_list()

def closeEvent(self, event):
    """Clean up when closing"""
    LanguageManager.unregister_observer(self.update_translations)
    super().closeEvent(event)
```

---

## ✅ STEP 6: UPDATE main() function

**FIND the last line in main() that sets cashier label:**
```python
win.cashier_label.setText(f"👤 Cashier: {win.cashier_name} (ID: {win.employee_id})")
```

**REPLACE WITH:**
```python
win.cashier_label.setText(
    f"👤 {tr_cashier('cashier_label')}: {win.cashier_name} "
    f"({tr_cashier('id_label')}: {win.employee_id})"
)
win.ui_elements['cashier'] = win.cashier_label
```

---

## 🎉 DONE!

After making all these changes:
1. Save the file
2. Run: `python main_prog_improved.py`
3. Test in both English and Indonesian modes

**Total Changes**: ~80 locations updated
**Estimated Time**: 1-2 hours
**Result**: Complete bilingual support!

---

**Document**: Complete Change List  
**Created**: November 7, 2025  
**Purpose**: Step-by-step implementation guide  
**Status**: Ready to apply ✅
