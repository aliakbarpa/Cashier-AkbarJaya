"""
LANGUAGE MANAGER - CENTRALIZED TRANSLATION SYSTEM
Manages all translations for the entire Akbar Jaya Cashier System

Usage:
    from modules.translations.language_manager import LanguageManager, tr
    
    # Get translation
    text = tr('welcome_message')
    
    # Change language
    LanguageManager.set_language('id')  # or 'en'
"""

class LanguageManager:
    """Centralized language management for the entire application"""
    
    _current_language = 'en'  # Default language
    _observers = []  # Components that need to be notified of language changes
    
    @classmethod
    def get_language(cls):
        """Get current language code"""
        return cls._current_language
    
    @classmethod
    def set_language(cls, lang_code):
        """Set current language and notify observers"""
        if lang_code in TRANSLATIONS:
            cls._current_language = lang_code
            cls._notify_observers()
    
    @classmethod
    def register_observer(cls, callback):
        """Register a callback to be notified of language changes"""
        if callback not in cls._observers:
            cls._observers.append(callback)
    
    @classmethod
    def unregister_observer(cls, callback):
        """Unregister a callback"""
        if callback in cls._observers:
            cls._observers.remove(callback)
    
    @classmethod
    def _notify_observers(cls):
        """Notify all observers of language change"""
        for callback in cls._observers:
            try:
                callback()
            except Exception as e:
                print(f"Error notifying observer: {e}")


def tr(key, lang=None):
    """
    Translate a key to current language
    
    Args:
        key: Translation key (e.g., 'welcome_message')
        lang: Optional language override
        
    Returns:
        Translated text or key if not found
    """
    if lang is None:
        lang = LanguageManager.get_language()
    
    return TRANSLATIONS.get(lang, {}).get(key, key)


# ========================================
# COMPLETE TRANSLATIONS DATABASE
# ========================================

TRANSLATIONS = {
    'en': {
        # ===== WELCOME SCREEN =====
        'welcome_title': 'AKBAR JAYA',
        'welcome_subtitle': 'Point of Sale System v2.0 - Role-Based Access',
        'welcome_message': 'Welcome! Please select an option to continue:',
        'cashier_option_title': '💳 Start as Cashier',
        'cashier_option_desc': 'Process sales transactions, manage cart, print receipts\n🔑 Access: Cashier, Manager, Supervisor',
        'stock_option_title': '📦 Update Stock',
        'stock_option_desc': 'Add or modify product inventory levels\n🔑 Access: Employee, Manager, Supervisor',
        'price_option_title': '💰 Update Prices',
        'price_option_desc': 'Modify individual product prices\n🔑 Access: Manager, Supervisor only',
        'welcome_guidelines': """
📖 Role-Based Access Control:
• <b>Supervisor:</b> Full access (Cashier, Stock, Price)
• <b>Manager:</b> Full access (Cashier, Stock, Price)
• <b>Employee:</b> Stock updates only
• <b>Cashier:</b> Cashier operations only

💾 All activities are logged with date and time stamps
        """,
        'welcome_footer': '© 2025 Akbar Jaya Store • v2.1 with Role-Based Access & Activity Logging',
        'exit_button': '❌ Exit',
        'language_selector': '🌐 Language / Bahasa',
        
        # ===== EMPLOYEE LOGIN =====
        'login_title': '🔐 Employee Login',
        'login_subtitle': 'Please enter your credentials to continue',
        'employee_id_label': '👤 Employee ID:',
        'employee_id_placeholder': 'Enter your Employee ID',
        'employee_name_label': '📝 Employee Name:',
        'employee_name_placeholder': 'Enter your full name',
        'login_button': '✅\nLOGIN',
        'cancel_button': '❌\nCANCEL',
        'register_button': '📝 Register New Employee',
        'login_error_title': 'Login Error',
        'login_error_empty': '⚠️ ALL FIELDS REQUIRED\n\nPlease enter both Employee ID and Name!',
        'login_error_access_denied': '⚠️ ACCESS DENIED',
        'login_error_not_found': 'Employee not found. Would you like to register?',
        'login_success': 'Login Successful',
        'login_welcome': 'Welcome back',
        
        # ===== REGISTRATION =====
        'register_title': '📝 Register New Employee',
        'register_subtitle': 'Create a new employee account',
        'register_id_label': '🆔 Employee ID:',
        'register_id_placeholder': 'Enter unique ID (e.g., E001)',
        'register_name_label': '👤 Full Name:',
        'register_name_placeholder': 'Enter full name',
        'register_role_label': '👔 Role:',
        'register_button_submit': '✅\nREGISTER',
        'register_error_title': 'Registration Error',
        'register_error_empty': '⚠️ ALL FIELDS REQUIRED\n\nPlease fill in all fields!',
        'register_error_exists': '⚠️ EMPLOYEE ID EXISTS\n\nThis Employee ID is already registered!\nPlease use a different ID.',
        'register_success': 'Registration Successful',
        'register_success_message': 'Employee registered successfully',
        
        # ===== CASHIER MAIN WINDOW =====
        'cashier_title': 'AKBAR JAYA',
        'cashier_subtitle': 'Cashier System - Enhanced UI',
        'cashier_label': 'Cashier',
        'catalog_title': '📂 Product Catalog',
        'cart_title': '🛒 Shopping Cart:',
        'cart_empty': '  (Empty)',
        'cart_total': 'TOTAL',
        'checkout_button': '💳\nCHECKOUT',
        'cancel_item_button': '❌\nCANCEL',
        'print_button': '🖨️\nPRINT',
        'save_pdf_button': '📄\nSAVE PDF',
        'report_button': '📊\nREPORT',
        
        # ===== CATALOG DIALOG =====
        'catalog_dialog_title': 'Catalog',
        'catalog_products': 'Products',
        'catalog_close': '❌ Close',
        
        # ===== PAYMENT DIALOG =====
        'payment_title': '💳 PAYMENT',
        'payment_total_label': 'TOTAL AMOUNT:',
        'payment_enter_label': '💵 Enter Payment Received:',
        'payment_placeholder': '0.00',
        'payment_confirm': '✅\nCONFIRM\nPAYMENT',
        'payment_cancel': '❌\nCANCEL',
        'payment_error_title': 'Insufficient Payment',
        'payment_error_message': '⚠️ INSUFFICIENT PAYMENT\n\nRequired: ${:.2f}\nReceived: ${:.2f}\n\nPlease enter at least ${:.2f}',
        'payment_invalid_title': 'Invalid Input',
        'payment_invalid_message': '⚠️ INVALID AMOUNT\n\nPlease enter a valid number!',
        
        # ===== COMPLETION DIALOG =====
        'completion_title': 'Transaction Complete',
        'completion_success': '✅ TRANSACTION\nCOMPLETE!',
        'completion_payment_label': '💵 Payment Received:',
        'completion_change_label': '💰 Change to Return:',
        'completion_thank_you': '🙏 Thank You!',
        'completion_ok': '✅\nOK',
        
        # ===== CUSTOMER NAME DIALOG =====
        'customer_title': '👤 CUSTOMER NAME',
        'customer_instructions': 'Please enter the customer\'s name:',
        'customer_name_label': '📝 Customer Name:',
        'customer_name_placeholder': 'Enter name here...',
        'customer_ok': '✅\nOK',
        'customer_skip': '⏭️\nSKIP\n(Use \'Customer\')',
        'customer_default': 'Customer',
        
        # ===== MESSAGES & ALERTS =====
        'empty_cart_title': 'Empty Cart',
        'empty_cart_message': 'Your cart is empty!',
        'out_of_stock_title': 'Out of Stock',
        'out_of_stock_message': '{} has only {} left in stock!',
        'payment_error_title': 'Payment Error',
        'payment_error_message': 'Payment must be at least ${:.2f}.',
        'item_removed_title': 'Item Removed',
        'item_removed_message': '✅ {} removed from cart.',
        'cancel_item_title': 'Cancel Item',
        'cancel_item_prompt': 'Select item to remove:',
        'no_items_title': 'Cart Empty',
        'no_items_message': 'No items to cancel.',
        'ready_title': 'Ready',
        'ready_message': '✅ Transaction completed!',
        'no_receipt_title': 'No Receipt',
        'no_receipt_print': 'No receipt to print.',
        'no_receipt_save': 'No receipt to save.',
        'receipt_saved_title': 'Saved',
        'receipt_saved_message': '✅ Receipt saved as PDF:\n{}',
        'stock_summary_title': 'Stock Summary',
        'stock_summary_total': '📊 Total Products: {}',
        'stock_summary_low': '⚠️ LOW STOCK ALERT:',
        'stock_summary_ok': '✅ All products have sufficient stock.',
        'stock_remaining': 'Stock: {} remaining',
        
        # ===== STOCK MANAGER =====
        'stock_manager_title': 'Stock Management',
        'stock_manager_subtitle': 'Update Product Inventory',
        'stock_manager_instructions': 'Select a product to update its stock level:',
        'stock_manager_product_label': '📦 Product:',
        'stock_manager_current_label': '📊 Current Stock:',
        'stock_manager_new_label': '➕ New Stock Amount:',
        'stock_manager_update_button': '✅\nUPDATE\nSTOCK',
        'stock_manager_close_button': '❌\nCLOSE',
        'stock_update_success': 'Stock Updated',
        'stock_update_message': '✅ Stock updated successfully!\n\n{}\nOld Stock: {}\nNew Stock: {}',
        'stock_update_error': 'Update Error',
        'stock_update_invalid': '⚠️ INVALID AMOUNT\n\nPlease enter a valid number!',
        'stock_select_product': 'Select a product first',
        
        # ===== PRICE MANAGER =====
        'price_manager_title': 'Price Management',
        'price_manager_subtitle': 'Update Product Prices',
        'price_manager_instructions': 'Select a product to update its price:',
        'price_manager_product_label': '📦 Product:',
        'price_manager_current_label': '💰 Current Price:',
        'price_manager_new_label': '💵 New Price:',
        'price_manager_update_button': '✅\nUPDATE\nPRICE',
        'price_manager_close_button': '❌\nCLOSE',
        'price_update_success': 'Price Updated',
        'price_update_message': '✅ Price updated successfully!\n\n{}\nOld Price: ${:.2f}\nNew Price: ${:.2f}',
        'price_update_error': 'Update Error',
        'price_update_invalid': '⚠️ INVALID AMOUNT\n\nPlease enter a valid price!',
        'price_select_product': 'Select a product first',
        
        # ===== RECEIPT =====
        'receipt_header': 'AKBAR JAYA RECEIPT',
        'receipt_date': 'Date/Time',
        'receipt_cashier': 'Cashier',
        'receipt_customer': 'Customer',
        'receipt_item': 'ITEM',
        'receipt_qty': 'QTY',
        'receipt_price': 'PRICE',
        'receipt_total': 'TOTAL',
        'receipt_subtotal': 'SUBTOTAL:',
        'receipt_payment': 'PAYMENT:',
        'receipt_change': 'CHANGE:',
        'receipt_footer': 'Thank you for shopping at Akbar Jaya!',
        
        # ===== REPORT =====
        'report_title': '📊 Sales Report Generator',
        'report_instruction': 'Select date range for the report:',
        'report_from': 'From Date:',
        'report_to': 'To Date:',
        'report_generate': '📊\nGENERATE\nREPORT',
        'report_close': '❌\nCLOSE',
        'report_no_data': 'No Sales Data',
        'report_no_data_message': 'No sales found in the selected date range.',
        'report_header': 'SALES REPORT',
        'report_period': 'Period',
        'report_summary': 'SALES SUMMARY',
        'report_total_transactions': 'Total Transactions',
        'report_total_revenue': 'Total Revenue',
        'report_products_sold': 'Products Sold',
        'report_details': 'TRANSACTION DETAILS',
        'report_save_pdf': '📄 SAVE AS PDF',
        
        # ===== ROLES =====
        'role_supervisor': 'Supervisor',
        'role_manager': 'Manager',
        'role_employee': 'Employee',
        'role_cashier': 'Cashier',
        
        # ===== GENERAL =====
        'yes': 'Yes',
        'no': 'No',
        'ok': 'OK',
        'cancel': 'Cancel',
        'close': 'Close',
        'save': 'Save',
        'items': 'items',
        'id': 'ID',
    },
    
    'id': {
        # ===== WELCOME SCREEN =====
        'welcome_title': 'AKBAR JAYA',
        'welcome_subtitle': 'Sistem Point of Sale v2.0 - Akses Berbasis Peran',
        'welcome_message': 'Selamat datang! Silakan pilih opsi untuk melanjutkan:',
        'cashier_option_title': '💳 Mulai sebagai Kasir',
        'cashier_option_desc': 'Proses transaksi penjualan, kelola keranjang, cetak struk\n🔑 Akses: Kasir, Manajer, Supervisor',
        'stock_option_title': '📦 Perbarui Stok',
        'stock_option_desc': 'Tambah atau ubah tingkat persediaan produk\n🔑 Akses: Karyawan, Manajer, Supervisor',
        'price_option_title': '💰 Perbarui Harga',
        'price_option_desc': 'Ubah harga produk individual\n🔑 Akses: Manajer, Supervisor saja',
        'welcome_guidelines': """
📖 Kontrol Akses Berbasis Peran:
• <b>Supervisor:</b> Akses penuh (Kasir, Stok, Harga)
• <b>Manajer:</b> Akses penuh (Kasir, Stok, Harga)
• <b>Karyawan:</b> Pembaruan stok saja
• <b>Kasir:</b> Operasi kasir saja

💾 Semua aktivitas dicatat dengan tanggal dan waktu
        """,
        'welcome_footer': '© 2025 Toko Akbar Jaya • v2.1 dengan Akses Berbasis Peran & Pencatatan Aktivitas',
        'exit_button': '❌ Keluar',
        'language_selector': '🌐 Language / Bahasa',
        
        # ===== EMPLOYEE LOGIN =====
        'login_title': '🔐 Login Karyawan',
        'login_subtitle': 'Silakan masukkan kredensial Anda untuk melanjutkan',
        'employee_id_label': '👤 ID Karyawan:',
        'employee_id_placeholder': 'Masukkan ID Karyawan Anda',
        'employee_name_label': '📝 Nama Karyawan:',
        'employee_name_placeholder': 'Masukkan nama lengkap Anda',
        'login_button': '✅\nMASUK',
        'cancel_button': '❌\nBATAL',
        'register_button': '📝 Daftarkan Karyawan Baru',
        'login_error_title': 'Kesalahan Login',
        'login_error_empty': '⚠️ SEMUA BIDANG WAJIB DIISI\n\nSilakan masukkan ID Karyawan dan Nama!',
        'login_error_access_denied': '⚠️ AKSES DITOLAK',
        'login_error_not_found': 'Karyawan tidak ditemukan. Apakah Anda ingin mendaftar?',
        'login_success': 'Login Berhasil',
        'login_welcome': 'Selamat datang kembali',
        
        # ===== REGISTRATION =====
        'register_title': '📝 Daftarkan Karyawan Baru',
        'register_subtitle': 'Buat akun karyawan baru',
        'register_id_label': '🆔 ID Karyawan:',
        'register_id_placeholder': 'Masukkan ID unik (mis., E001)',
        'register_name_label': '👤 Nama Lengkap:',
        'register_name_placeholder': 'Masukkan nama lengkap',
        'register_role_label': '👔 Peran:',
        'register_button_submit': '✅\nDAFTAR',
        'register_error_title': 'Kesalahan Pendaftaran',
        'register_error_empty': '⚠️ SEMUA BIDANG WAJIB DIISI\n\nSilakan isi semua bidang!',
        'register_error_exists': '⚠️ ID KARYAWAN SUDAH ADA\n\nID Karyawan ini sudah terdaftar!\nSilakan gunakan ID yang berbeda.',
        'register_success': 'Pendaftaran Berhasil',
        'register_success_message': 'Karyawan berhasil didaftarkan',
        
        # ===== CASHIER MAIN WINDOW =====
        'cashier_title': 'AKBAR JAYA',
        'cashier_subtitle': 'Sistem Kasir - UI yang Ditingkatkan',
        'cashier_label': 'Kasir',
        'catalog_title': '📂 Katalog Produk',
        'cart_title': '🛒 Keranjang Belanja:',
        'cart_empty': '  (Kosong)',
        'cart_total': 'TOTAL',
        'checkout_button': '💳\nBAYAR',
        'cancel_item_button': '❌\nBATAL',
        'print_button': '🖨️\nCETAK',
        'save_pdf_button': '📄\nSIMPAN PDF',
        'report_button': '📊\nLAPORAN',
        
        # ===== CATALOG DIALOG =====
        'catalog_dialog_title': 'Katalog',
        'catalog_products': 'Produk',
        'catalog_close': '❌ Tutup',
        
        # ===== PAYMENT DIALOG =====
        'payment_title': '💳 PEMBAYARAN',
        'payment_total_label': 'JUMLAH TOTAL:',
        'payment_enter_label': '💵 Masukkan Pembayaran Diterima:',
        'payment_placeholder': '0.00',
        'payment_confirm': '✅\nKONFIRMASI\nPEMBAYARAN',
        'payment_cancel': '❌\nBATAL',
        'payment_error_title': 'Pembayaran Tidak Cukup',
        'payment_error_message': '⚠️ PEMBAYARAN TIDAK CUKUP\n\nDiperlukan: ${:.2f}\nDiterima: ${:.2f}\n\nSilakan masukkan minimal ${:.2f}',
        'payment_invalid_title': 'Input Tidak Valid',
        'payment_invalid_message': '⚠️ JUMLAH TIDAK VALID\n\nSilakan masukkan angka yang valid!',
        
        # ===== COMPLETION DIALOG =====
        'completion_title': 'Transaksi Selesai',
        'completion_success': '✅ TRANSAKSI\nSELESAI!',
        'completion_payment_label': '💵 Pembayaran Diterima:',
        'completion_change_label': '💰 Kembalian:',
        'completion_thank_you': '🙏 Terima Kasih!',
        'completion_ok': '✅\nOK',
        
        # ===== CUSTOMER NAME DIALOG =====
        'customer_title': '👤 NAMA PELANGGAN',
        'customer_instructions': 'Silakan masukkan nama pelanggan:',
        'customer_name_label': '📝 Nama Pelanggan:',
        'customer_name_placeholder': 'Masukkan nama di sini...',
        'customer_ok': '✅\nOK',
        'customer_skip': '⏭️\nLEWATI\n(Gunakan \'Pelanggan\')',
        'customer_default': 'Pelanggan',
        
        # ===== MESSAGES & ALERTS =====
        'empty_cart_title': 'Keranjang Kosong',
        'empty_cart_message': 'Keranjang Anda kosong!',
        'out_of_stock_title': 'Stok Habis',
        'out_of_stock_message': '{} hanya tersisa {} di stok!',
        'payment_error_title': 'Kesalahan Pembayaran',
        'payment_error_message': 'Pembayaran harus minimal ${:.2f}.',
        'item_removed_title': 'Item Dihapus',
        'item_removed_message': '✅ {} dihapus dari keranjang.',
        'cancel_item_title': 'Batalkan Item',
        'cancel_item_prompt': 'Pilih item untuk dihapus:',
        'no_items_title': 'Keranjang Kosong',
        'no_items_message': 'Tidak ada item untuk dibatalkan.',
        'ready_title': 'Siap',
        'ready_message': '✅ Transaksi selesai!',
        'no_receipt_title': 'Tidak Ada Struk',
        'no_receipt_print': 'Tidak ada struk untuk dicetak.',
        'no_receipt_save': 'Tidak ada struk untuk disimpan.',
        'receipt_saved_title': 'Tersimpan',
        'receipt_saved_message': '✅ Struk disimpan sebagai PDF:\n{}',
        'stock_summary_title': 'Ringkasan Stok',
        'stock_summary_total': '📊 Total Produk: {}',
        'stock_summary_low': '⚠️ PERINGATAN STOK RENDAH:',
        'stock_summary_ok': '✅ Semua produk memiliki stok yang cukup.',
        'stock_remaining': 'Stok: {} tersisa',
        
        # ===== STOCK MANAGER =====
        'stock_manager_title': 'Manajemen Stok',
        'stock_manager_subtitle': 'Perbarui Persediaan Produk',
        'stock_manager_instructions': 'Pilih produk untuk memperbarui tingkat stoknya:',
        'stock_manager_product_label': '📦 Produk:',
        'stock_manager_current_label': '📊 Stok Saat Ini:',
        'stock_manager_new_label': '➕ Jumlah Stok Baru:',
        'stock_manager_update_button': '✅\nPERBARUI\nSTOK',
        'stock_manager_close_button': '❌\nTUTUP',
        'stock_update_success': 'Stok Diperbarui',
        'stock_update_message': '✅ Stok berhasil diperbarui!\n\n{}\nStok Lama: {}\nStok Baru: {}',
        'stock_update_error': 'Kesalahan Pembaruan',
        'stock_update_invalid': '⚠️ JUMLAH TIDAK VALID\n\nSilakan masukkan angka yang valid!',
        'stock_select_product': 'Pilih produk terlebih dahulu',
        
        # ===== PRICE MANAGER =====
        'price_manager_title': 'Manajemen Harga',
        'price_manager_subtitle': 'Perbarui Harga Produk',
        'price_manager_instructions': 'Pilih produk untuk memperbarui harganya:',
        'price_manager_product_label': '📦 Produk:',
        'price_manager_current_label': '💰 Harga Saat Ini:',
        'price_manager_new_label': '💵 Harga Baru:',
        'price_manager_update_button': '✅\nPERBARUI\nHARGA',
        'price_manager_close_button': '❌\nTUTUP',
        'price_update_success': 'Harga Diperbarui',
        'price_update_message': '✅ Harga berhasil diperbarui!\n\n{}\nHarga Lama: ${:.2f}\nHarga Baru: ${:.2f}',
        'price_update_error': 'Kesalahan Pembaruan',
        'price_update_invalid': '⚠️ JUMLAH TIDAK VALID\n\nSilakan masukkan harga yang valid!',
        'price_select_product': 'Pilih produk terlebih dahulu',
        
        # ===== RECEIPT =====
        'receipt_header': 'STRUK AKBAR JAYA',
        'receipt_date': 'Tanggal/Waktu',
        'receipt_cashier': 'Kasir',
        'receipt_customer': 'Pelanggan',
        'receipt_item': 'ITEM',
        'receipt_qty': 'JML',
        'receipt_price': 'HARGA',
        'receipt_total': 'TOTAL',
        'receipt_subtotal': 'SUBTOTAL:',
        'receipt_payment': 'PEMBAYARAN:',
        'receipt_change': 'KEMBALIAN:',
        'receipt_footer': 'Terima kasih telah berbelanja di Akbar Jaya!',
        
        # ===== REPORT =====
        'report_title': '📊 Generator Laporan Penjualan',
        'report_instruction': 'Pilih rentang tanggal untuk laporan:',
        'report_from': 'Dari Tanggal:',
        'report_to': 'Sampai Tanggal:',
        'report_generate': '📊\nBUAT\nLAPORAN',
        'report_close': '❌\nTUTUP',
        'report_no_data': 'Tidak Ada Data Penjualan',
        'report_no_data_message': 'Tidak ada penjualan ditemukan dalam rentang tanggal yang dipilih.',
        'report_header': 'LAPORAN PENJUALAN',
        'report_period': 'Periode',
        'report_summary': 'RINGKASAN PENJUALAN',
        'report_total_transactions': 'Total Transaksi',
        'report_total_revenue': 'Total Pendapatan',
        'report_products_sold': 'Produk Terjual',
        'report_details': 'DETAIL TRANSAKSI',
        'report_save_pdf': '📄 SIMPAN SEBAGAI PDF',
        
        # ===== ROLES =====
        'role_supervisor': 'Supervisor',
        'role_manager': 'Manajer',
        'role_employee': 'Karyawan',
        'role_cashier': 'Kasir',
        
        # ===== GENERAL =====
        'yes': 'Ya',
        'no': 'Tidak',
        'ok': 'OK',
        'cancel': 'Batal',
        'close': 'Tutup',
        'save': 'Simpan',
        'items': 'item',
        'id': 'ID',
    }
}
