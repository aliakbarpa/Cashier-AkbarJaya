"""
RECEIPT MODULE - IMPROVED ALIGNMENT
Generates properly formatted receipts with correct spacing
"""

from datetime import datetime


def generate_receipt_text(cart, products_df, customer_name="Customer", 
                         payment_amount=None, change_amount=None, 
                         cashier_name="Cashier"):
    """Generate formatted receipt text with proper alignment"""
    if not cart:
        return "No items in cart."

    # Count quantities
    summary = {}
    for pid in cart:
        summary[pid] = summary.get(pid, 0) + 1

    lines = []
    lines.append("=" * 60)
    lines.append("          Toko: AKBAR JAYA")
    lines.append("          JLN. Poros Cabbenge,Soppeng, Sul-Sel")
    lines.append("          No. 218, Kode POS: 9999989")
    lines.append("          No. Telpon: 081355739968")
    lines.append("=" * 60)
    lines.append("")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines.append(f"Date/Time : {now}")
    lines.append(f"Cashier   : {cashier_name}")
    lines.append(f"Customer  : {customer_name}")
    lines.append("")
    lines.append("-" * 60)
    lines.append(f"{'ITEM':<28} {'QTY':>5} {'PRICE':>10} {'TOTAL':>12}")
    lines.append("-" * 60)

    total_amount = 0.0
    for pid, qty in summary.items():
        product = products_df[products_df['product_id'] == pid].iloc[0]
        name = product['name'][:28]  # Truncate long names
        price = float(product['price'])
        total = price * qty
        total_amount += total
        
        # Better aligned format
        lines.append(f"{name:<28} {qty:>5} ${price:>9.2f} ${total:>10.2f}")

    lines.append("-" * 60)
    lines.append("")
    
    # Right-aligned totals with proper spacing
    lines.append(f"{'SUBTOTAL:':>48} ${total_amount:>10.2f}")
    
    if payment_amount is not None:
        lines.append(f"{'PAYMENT:':>48} ${payment_amount:>10.2f}")
        lines.append(f"{'CHANGE:':>48} ${change_amount:>10.2f}")
    
    lines.append("")
    lines.append("=" * 60)
    lines.append("")
    lines.append("       Thank you for shopping at Akbar Jaya!")
    lines.append("")
    lines.append("-" * 60)
    lines.append("              TERMS & CONDITIONS")
    lines.append("-" * 60)
    lines.append("  1) All items sold are non-refundable")
    lines.append("  2) Change may not be provided for large bills")
    lines.append("  3) This receipt is valid proof of purchase")
    lines.append("=" * 60)
    
    return "\n".join(lines)
