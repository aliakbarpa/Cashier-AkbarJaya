# 🔄 MAIN CASHIER TRANSLATION UPDATE GUIDE

## Overview

This document shows how to update `main_prog_improved.py` to use the centralized translation system.

---

## Step 1: Add Import at Top

**Add after existing imports:**
```python
# Import translation system
from modules.translations import LanguageManager, tr
```

---

## Step 2: Update LargePaymentDialog Class

**Replace hard-coded strings with tr() calls:**

### Init method:
```python
def __init__(self, parent, total_amount):
    super().__init__(parent)
    self.setWindowTitle(tr('payment_title'))  # Changed
    # ... rest of code
```

### UI elements to translate:
```python
# Title
title = QLabel(tr('payment_title'))

# Total label
total_label = QLabel(tr('payment_total_label'))

# Payment label
payment_label = QLabel(tr('payment_enter_label'))

# Placeholder
self.payment_input.setPlaceholderText(tr('payment_placeholder'))

# Confirm button
confirm_btn = QPushButton(tr('payment_confirm'))

# Cancel button
cancel_btn = QPushButton(tr('payment_cancel'))
```

### Error messages:
```python
# Insufficient payment error
error_msg.setWindowTitle(tr('payment_error_title'))
error_msg.setText(tr('payment_error_message').format(
    self.total_amount, payment, self.total_amount
))

# Invalid input error
error_msg.setWindowTitle(tr('payment_invalid_title'))
error_msg.setText(tr('payment_invalid_message'))
```

---

## Step 3: Update LargeCompletionDialog Class

```python
def __init__(self, parent, payment, change):
    super().__init__(parent)
    self.setWindowTitle(tr('completion_title'))
    # ... rest

# UI elements:
title = QLabel(tr('completion_success'))
payment_label = QLabel(tr('completion_payment_label'))
change_label = QLabel(tr('completion_change_label'))
thank_you = QLabel(tr('completion_thank_you'))
ok_btn = QPushButton(tr('completion_ok'))
```

---

## Step 4: Update LargeCustomerNameDialog Class

```python
def __init__(self, parent):
    super().__init__(parent)
    self.setWindowTitle(tr('customer_title'))
    self.customer_name = tr('customer_default')  # "Customer"
    # ... rest

# UI elements:
title = QLabel(tr('customer_title'))
instructions = QLabel(tr('customer_instructions'))
name_label = QLabel(tr('customer_name_label'))
self.name_input.setPlaceholderText(tr('customer_name_placeholder'))
self.name_input.setText(tr('customer_default'))
ok_btn = QPushButton(tr('customer_ok'))
skip_btn = QPushButton(tr('customer_skip'))
```

---

## Step 5: Update AkbarCashier Class

### Store UI elements that need updating:
```python
def __init__(self):
    super().__init__()
    # ... existing code
    
    # Store UI elements for translation updates
    self.ui_elements = {}
    
    # Register for language changes
    LanguageManager.register_observer(self.update_translations)
```

### Update labels:
```python
# Title
self.title_label = QLabel(tr('cashier_title'))
self.ui_elements['title'] = self.title_label

# Cashier label
self.cashier_label.setText(
    f"👤 {tr('cashier_label')}: {self.cashier_name} ({tr('id')}: {self.employee_id})"
)
self.ui_elements['cashier_label'] = self.cashier_label

# Catalog title
catalog_title = QLabel(tr('catalog_title'))
self.ui_elements['catalog_title'] = catalog_title

# Cart title
self.cart_label.setText(f"{tr('cart_title')}\n\n{tr('cart_empty')}")
self.ui_elements['cart_label'] = self.cart_label
```

### Update buttons:
```python
# Checkout button
self.checkout_btn = QPushButton(tr('checkout_button'))
self.ui_elements['checkout_btn'] = self.checkout_btn

# Cancel button
self.cancel_btn = QPushButton(tr('cancel_item_button'))
self.ui_elements['cancel_btn'] = self.cancel_btn

# Print button
self.print_btn = QPushButton(tr('print_button'))
self.ui_elements['print_btn'] = self.print_btn

# PDF button
self.pdf_btn = QPushButton(tr('save_pdf_button'))
self.ui_elements['pdf_btn'] = self.pdf_btn

# Report button
self.report_btn = QPushButton(tr('report_button'))
self.ui_elements['report_btn'] = self.report_btn
```

### Update cart display:
```python
def update_cart_label(self):
    text = f"{tr('cart_title')}\n\n"
    summary = {}
    for pid in self.cart:
        summary[pid] = summary.get(pid, 0) + 1
    
    if not summary:
        text += f"  {tr('cart_empty')}\n"
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
        text += f"{tr('cart_total')}: ${grand_total:.2f}\n"
    
    self.cart_label.setText(text)
```

### Update messages:
```python
# Empty cart
QMessageBox.information(self, tr('empty_cart_title'), tr('empty_cart_message'))

# Out of stock
QMessageBox.warning(self, tr('out_of_stock_title'), 
    tr('out_of_stock_message').format(product['name'], product['stock']))

# Payment error
QMessageBox.warning(self, tr('payment_error_title'), 
    tr('payment_error_message').format(total))

# Item removed
QMessageBox.information(self, tr('item_removed_title'), 
    tr('item_removed_message').format(item))

# Cancel item
item, ok = QInputDialog.getItem(
    self, tr('cancel_item_title'), tr('cancel_item_prompt'), 
    items_list, 0, False
)

# No items
QMessageBox.information(self, tr('no_items_title'), tr('no_items_message'))

# Ready
QMessageBox.information(self, tr('ready_title'), tr('ready_message'))

# No receipt to print
QMessageBox.warning(self, tr('no_receipt_title'), tr('no_receipt_print'))

# No receipt to save
QMessageBox.warning(self, tr('no_receipt_title'), tr('no_receipt_save'))

# Receipt saved
QMessageBox.information(self, tr('receipt_saved_title'), 
    tr('receipt_saved_message').format(filename))
```

### Update catalog dialog:
```python
def open_catalog_dialog(self, catalog_prefix):
    dialog = QDialog(self)
    dialog.setWindowTitle(f"{tr('catalog_dialog_title')}: {catalog_prefix}")
    
    # Title
    title = QLabel(f"📂 {catalog_prefix} {tr('catalog_products')}")
    
    # Close button
    close_btn = QPushButton(tr('catalog_close'))
```

### Add update_translations method:
```python
def update_translations(self):
    """Update all UI text when language changes"""
    self.ui_elements['title'].setText(tr('cashier_title'))
    self.ui_elements['catalog_title'].setText(tr('catalog_title'))
    self.ui_elements['checkout_btn'].setText(tr('checkout_button'))
    self.ui_elements['cancel_btn'].setText(tr('cancel_item_button'))
    self.ui_elements['print_btn'].setText(tr('print_button'))
    self.ui_elements['pdf_btn'].setText(tr('save_pdf_button'))
    self.ui_elements['report_btn'].setText(tr('report_button'))
    
    # Update cashier label
    self.cashier_label.setText(
        f"👤 {tr('cashier_label')}: {self.cashier_name} ({tr('id')}: {self.employee_id})"
    )
    
    # Update cart display
    self.update_cart_label()
```

### Add closeEvent:
```python
def closeEvent(self, event):
    """Clean up when closing"""
    LanguageManager.unregister_observer(self.update_translations)
    super().closeEvent(event)
```

---

## Summary of Changes

### Files to Modify:
1. `main_prog_improved.py` - Main cashier application

### Key Changes:
1. **Import translation system** at top of file
2. **Replace ALL hard-coded strings** with `tr('key')` calls
3. **Store UI elements** in `self.ui_elements` dictionary
4. **Register observer** for language changes
5. **Add `update_translations()` method**
6. **Add `closeEvent()` method** to clean up

### Translation Keys Used:
- Payment dialog: `payment_title`, `payment_total_label`, `payment_enter_label`, etc.
- Completion dialog: `completion_title`, `completion_success`, etc.
- Customer name dialog: `customer_title`, `customer_name_label`, etc.
- Main window: `cashier_title`, `cart_title`, `checkout_button`, etc.
- Messages: `empty_cart_title`, `out_of_stock_message`, etc.

---

## Testing

After making changes:

1. **Run the program:**
   ```bash
   python main_prog_improved.py
   ```

2. **Change language** on welcome screen

3. **Test all features:**
   - Add items to cart → Check if cart text updates
   - Checkout → Check payment dialog
   - Complete transaction → Check completion dialog
   - Try all buttons → Verify text is translated

4. **Switch language again** → All text should update

---

## Next: Receipt Module

After completing main_prog_improved.py, we'll update receipt_improved.py to use translations for receipt text.

---

**Note**: Due to the size of main_prog_improved.py (900+ lines), I recommend making these changes section by section and testing each part before proceeding to the next.

Would you like me to create the complete updated file, or would you prefer to implement these changes step by step?
