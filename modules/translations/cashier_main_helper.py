"""
CASHIER MAIN TRANSLATION HELPER
Provides easy translation access for main_prog_improved.py
Integrates with the centralized LanguageManager
"""

from modules.translations.language_manager import LanguageManager, tr
from modules.translations.cashier_main_id import CASHIER_MAIN_ID


class CashierMainTranslations:
    """Helper class for cashier main window translations"""
    
    # Complete translation dictionary for cashier main
    TRANSLATIONS = {
        'en': {
            # Window title
            'window_title': 'Akbar Jaya Cashier System - Enhanced UI v2.2',
            
            # Main labels
            'title': 'AKBAR JAYA',
            'cashier_label': 'Cashier',
            'id_label': 'ID',
            
            # Date/Time
            'datetime_prefix': '🕒',
            
            # Product Catalog
            'catalog_title': '📂 Product Catalog',
            'catalog_dialog_title': 'Catalog',
            'catalog_products': 'Products',
            'catalog_close': '❌ Close',
            'items_suffix': 'items',
            
            # Shopping Cart
            'cart_title': '🛒 Shopping Cart:',
            'cart_empty': '  (Empty)',
            'cart_total': 'TOTAL',
            
            # Main Buttons
            'checkout_btn': '💳\nCHECKOUT',
            'cancel_btn': '❌\nCANCEL',
            'print_btn': '🖨️\nPRINT',
            'save_pdf_btn': '📄\nSAVE PDF',
            'report_btn': '📊\nREPORT',
            
            # Payment Dialog
            'payment_title': '💳 PAYMENT',
            'payment_total_label': 'TOTAL AMOUNT:',
            'payment_enter_label': '💵 Enter Payment Received:',
            'payment_placeholder': '0.00',
            'payment_confirm': '✅\nCONFIRM\nPAYMENT',
            'payment_cancel': '❌\nCANCEL',
            
            # Payment errors
            'payment_error_insufficient_title': 'Insufficient Payment',
            'payment_error_insufficient': '⚠️ INSUFFICIENT PAYMENT\n\nRequired: ${:.2f}\nReceived: ${:.2f}\n\nPlease enter at least ${:.2f}',
            'payment_error_invalid_title': 'Invalid Input',
            'payment_error_invalid': '⚠️ INVALID AMOUNT\n\nPlease enter a valid number!',
            
            # Completion Dialog
            'completion_title': 'Transaction Complete',
            'completion_success': '✅ TRANSACTION\nCOMPLETE!',
            'completion_payment_label': '💵 Payment Received:',
            'completion_change_label': '💰 Change to Return:',
            'completion_thank_you': '🙏 Thank You!',
            'completion_ok': '✅\nOK',
            
            # Customer Name Dialog
            'customer_title': '👤 CUSTOMER NAME',
            'customer_instructions': 'Please enter the customer\'s name:',
            'customer_name_label': '📝 Customer Name:',
            'customer_name_placeholder': 'Enter name here...',
            'customer_default': 'Customer',
            'customer_ok': '✅\nOK',
            'customer_skip': '⏭️\nSKIP\n(Use \'Customer\')',
            
            # Message boxes
            'empty_cart_title': 'Empty Cart',
            'empty_cart_msg': 'Your cart is empty!',
            
            'out_of_stock_title': 'Out of Stock',
            'out_of_stock_msg': '{} has only {} left in stock!',
            
            'payment_error_title': 'Payment Error',
            'payment_error_msg': 'Payment must be at least ${:.2f}.',
            
            'item_removed_title': 'Item Removed',
            'item_removed_msg': '✅ {} removed from cart.',
            
            'cancel_item_title': 'Cancel Item',
            'cancel_item_prompt': 'Select item to remove:',
            
            'no_items_title': 'Cart Empty',
            'no_items_msg': 'No items to cancel.',
            
            'ready_title': 'Ready',
            'ready_msg': '✅ Transaction completed!',
            
            'no_receipt_title': 'No Receipt',
            'no_receipt_print': 'No receipt to print.',
            'no_receipt_save': 'No receipt to save.',
            
            'receipt_saved_title': 'Saved',
            'receipt_saved_msg': '✅ Receipt saved as PDF:\n{}',
            
            'stock_summary_title': 'Stock Summary',
            'stock_summary_total': '📊 Total Products: {}',
            'stock_summary_low': '⚠️ LOW STOCK ALERT:',
            'stock_summary_ok': '✅ All products have sufficient stock.',
            'stock_id': 'ID',
            'stock_remaining': 'Stock: {} remaining',
        },
        'id': CASHIER_MAIN_ID
    }
    
    @staticmethod
    def get_text(key, *args):
        """
        Get translated text for current language
        
        Args:
            key: Translation key
            *args: Format arguments for string formatting
            
        Returns:
            Formatted translated string
        """
        lang = LanguageManager.get_language()
        text = CashierMainTranslations.TRANSLATIONS.get(lang, {}).get(key, key)
        
        # Apply formatting if args provided
        if args:
            try:
                return text.format(*args)
            except:
                return text
        
        return text
    
    @staticmethod
    def tr(key, *args):
        """Shorthand for get_text"""
        return CashierMainTranslations.get_text(key, *args)


# Create easy-to-use function
def tr_cashier(key, *args):
    """
    Quick translation function for cashier main window
    
    Usage:
        from modules.translations.cashier_main_helper import tr_cashier
        
        text = tr_cashier('window_title')
        msg = tr_cashier('out_of_stock_msg', product_name, stock_amount)
    
    Args:
        key: Translation key
        *args: Format arguments
        
    Returns:
        Translated and formatted string
    """
    return CashierMainTranslations.get_text(key, *args)


# Export for easy importing
__all__ = ['CashierMainTranslations', 'tr_cashier']
