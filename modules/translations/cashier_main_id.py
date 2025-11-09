"""
INDONESIAN TRANSLATIONS FOR MAIN CASHIER WINDOW
Separate module to optimize token usage
Contains only Indonesian translations for UI text in main_prog_improved.py
"""

# Main window translations
CASHIER_MAIN_ID = {
    # Window title
    'window_title': 'Sistem Kasir Akbar Jaya - UI yang Ditingkatkan v2.2',
    
    # Main labels
    'title': 'AKBAR JAYA',
    'cashier_label': 'Kasir',
    'id_label': 'ID',
    
    # Date/Time (keep emoji, translate text)
    'datetime_prefix': '🕒',  # Just emoji, time shown as is
    
    # Product Catalog
    'catalog_title': '📂 Katalog Produk',
    'catalog_dialog_title': 'Katalog',
    'catalog_products': 'Produk',
    'catalog_close': '❌ Tutup',
    'items_suffix': 'item',  # "5 item"
    
    # Shopping Cart
    'cart_title': '🛒 Keranjang Belanja:',
    'cart_empty': '  (Kosong)',
    'cart_total': 'TOTAL',
    
    # Main Buttons
    'checkout_btn': '💳\nBAYAR',
    'cancel_btn': '❌\nBATAL',
    'print_btn': '🖨️\nCETAK',
    'save_pdf_btn': '📄\nSIMPAN PDF',
    'report_btn': '📊\nLAPORAN',
    
    # Payment Dialog
    'payment_title': '💳 PEMBAYARAN',
    'payment_total_label': 'JUMLAH TOTAL:',
    'payment_enter_label': '💵 Masukkan Pembayaran Diterima:',
    'payment_placeholder': '0.00',
    'payment_confirm': '✅\nKONFIRMASI\nPEMBAYARAN',
    'payment_cancel': '❌\nBATAL',
    
    # Payment errors
    'payment_error_insufficient_title': 'Pembayaran Tidak Cukup',
    'payment_error_insufficient': '⚠️ PEMBAYARAN TIDAK CUKUP\n\nDiperlukan: ${:.2f}\nDiterima: ${:.2f}\n\nSilakan masukkan minimal ${:.2f}',
    'payment_error_invalid_title': 'Input Tidak Valid',
    'payment_error_invalid': '⚠️ JUMLAH TIDAK VALID\n\nSilakan masukkan angka yang valid!',
    
    # Completion Dialog
    'completion_title': 'Transaksi Selesai',
    'completion_success': '✅ TRANSAKSI\nSELESAI!',
    'completion_payment_label': '💵 Pembayaran Diterima:',
    'completion_change_label': '💰 Kembalian:',
    'completion_thank_you': '🙏 Terima Kasih!',
    'completion_ok': '✅\nOK',
    
    # Customer Name Dialog
    'customer_title': '👤 NAMA PELANGGAN',
    'customer_instructions': 'Silakan masukkan nama pelanggan:',
    'customer_name_label': '📝 Nama Pelanggan:',
    'customer_name_placeholder': 'Masukkan nama di sini...',
    'customer_default': 'Pelanggan',
    'customer_ok': '✅\nOK',
    'customer_skip': '⏭️\nLEWATI\n(Gunakan \'Pelanggan\')',
    
    # Message boxes
    'empty_cart_title': 'Keranjang Kosong',
    'empty_cart_msg': 'Keranjang Anda kosong!',
    
    'out_of_stock_title': 'Stok Habis',
    'out_of_stock_msg': '{} hanya tersisa {} di stok!',
    
    'payment_error_title': 'Kesalahan Pembayaran',
    'payment_error_msg': 'Pembayaran harus minimal ${:.2f}.',
    
    'item_removed_title': 'Item Dihapus',
    'item_removed_msg': '✅ {} dihapus dari keranjang.',
    
    'cancel_item_title': 'Batalkan Item',
    'cancel_item_prompt': 'Pilih item untuk dihapus:',
    
    'no_items_title': 'Keranjang Kosong',
    'no_items_msg': 'Tidak ada item untuk dibatalkan.',
    
    'ready_title': 'Siap',
    'ready_msg': '✅ Transaksi selesai!',
    
    'no_receipt_title': 'Tidak Ada Struk',
    'no_receipt_print': 'Tidak ada struk untuk dicetak.',
    'no_receipt_save': 'Tidak ada struk untuk disimpan.',
    
    'receipt_saved_title': 'Tersimpan',
    'receipt_saved_msg': '✅ Struk disimpan sebagai PDF:\n{}',
    
    'stock_summary_title': 'Ringkasan Stok',
    'stock_summary_total': '📊 Total Produk: {}',
    'stock_summary_low': '⚠️ PERINGATAN STOK RENDAH:',
    'stock_summary_ok': '✅ Semua produk memiliki stok yang cukup.',
    'stock_id': 'ID',
    'stock_remaining': 'Stok: {} tersisa',
}


def get_text(key, *args):
    """
    Get translated text from dictionary
    
    Args:
        key: Translation key
        *args: Format arguments for string formatting
        
    Returns:
        Formatted translated string
    """
    text = CASHIER_MAIN_ID.get(key, key)
    
    # Apply formatting if args provided
    if args:
        try:
            return text.format(*args)
        except:
            return text
    
    return text


# Quick access function
def tr_id(key, *args):
    """Shorthand for get_text"""
    return get_text(key, *args)
