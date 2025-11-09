from datetime import datetime

def generate_receipt_text(cart, products_df, customer_name="Customer", payment_amount=None, change_amount=None, cashier_name="Cashier"):
    if not cart:
        return "No items in cart."

    # Count quantities
    summary = {}
    for pid in cart:
        summary[pid] = summary.get(pid, 0) + 1

    lines = []
    lines.append("==== Akbar Jaya Receipt ====")
    lines.append("")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines.append(f"Date: {now}")
    lines.append(f"Cashier: {cashier_name}")
    lines.append(f"Customer: {customer_name}")
    lines.append("")
    lines.append(f"{'Item':25} {'Price x Qty':15} {'Total':>10}")
    lines.append("-"*50)

    total_amount = 0.0
    for pid, qty in summary.items():
        product = products_df[products_df['product_id'] == pid].iloc[0]
        name = product['name']
        price = float(product['price'])
        total = price * qty
        total_amount += total
        lines.append(f"{name:25} ${price:.2f} x {qty:<3} ${total:>7.2f}")

    lines.append("-"*50)
    lines.append(f"{'Total:':>42} ${total_amount:.2f}")
    if payment_amount is not None:
        lines.append(f"{'Payment:':>42} ${payment_amount:.2f}")
        lines.append(f"{'Change:':>42} ${change_amount:.2f}")
    lines.append("")
    lines.append("Thank you for shopping at Akbar Jaya!")
    lines.append("Terms & Conditions apply.")
    lines.append("\n--- Terms & Conditions ---\n1) Items sold is non-refundable!\n2) Change is not required \n3) This receipt is valid transaction as per date shown in this receipt!")
    lines.append("==================================")
    
    return "\n".join(lines)