# 📋 QUICK REFERENCE CARD - Akbar Jaya Cashier v1.7

---

## 🚀 STARTING THE PROGRAM

**Double-click:** `RUN_IMPROVED.bat`

**OR via command line:**
```
python main_prog_improved.py
```

---

## 🔐 EMPLOYEE LOGIN

**When prompted, enter:**
1. Your full name
2. Your employee ID (e.g., "EMP001")

**⚠️ Both fields required - cannot proceed without them!**

---

## 💳 CASHIER MODE - DAILY USE

### **Adding Products:**
```
1. Click catalog button (AJ, PK, OB, etc.)
2. Click desired product
3. Product added to cart
4. Repeat for all items
```

### **Checking Out:**
```
1. Click "💳 CHECKOUT" button
2. Large payment window appears
3. Read total amount (shown in HUGE text)
4. Enter payment from customer
5. Click "✅ CONFIRM PAYMENT"
6. Enter customer name (optional)
7. View payment and change in large text
8. Click "OK" to finish
9. Receipt is ready
```

### **Printing Receipt:**
```
• Click "🖨️ PRINT" → Send to printer
• Click "📄 SAVE PDF" → Save as PDF file
```

### **Canceling Items:**
```
1. Click "❌ CANCEL ITEM"
2. Select item from list
3. Item removed from cart
```

### **Viewing Reports:**
```
1. Click "📊 REPORT"
2. Select date range
3. View sales summary
```

---

## 📦 UPDATING STOCK

**From Welcome Screen:**
```
1. Click "📦 Update Stock"
2. Enter employee credentials
3. Click product to update
4. Enter new stock level
5. Click "Update"
6. Click "Done" when finished
```

**Stock Alerts:**
- Products with ≤5 items show in RED
- Update stock before it runs out!

---

## 💰 UPDATING PRICES

**From Welcome Screen:**
```
1. Click "💰 Update Prices"
2. Enter employee credentials
3. Click product to update
4. Enter new price
5. Click "Update"
6. Click "Done" when finished
```

---

## 🎨 BUTTON COLORS GUIDE

| Button | Color | Purpose |
|--------|-------|---------|
| 💳 CHECKOUT | Green | Process payment |
| ❌ CANCEL | Red | Remove items |
| 🖨️ PRINT | Blue | Print receipt |
| 📄 SAVE PDF | Purple | Save as PDF |
| 📊 REPORT | Orange | Generate report |

---

## 🔴 PRODUCT COLORS

| Color | Meaning |
|-------|---------|
| 🔵 Blue | Drinks |
| 🟢 Green | Food |
| 🟠 Orange | Electronics |
| 🔴 Red | LOW STOCK (≤5) |

---

## 👁️ LARGE CHECKOUT FEATURES

**For Elderly Customers:**
- **Total Amount:** 72pt font (HUGE red numbers)
- **Payment Input:** 64pt font (very large)
- **Buttons:** 350-400px wide (can't miss them)
- **Change Display:** 72pt font (bright green)

**Why this helps:**
- Easy to read from 2 meters away
- Hard to make mistakes
- Less stressful for customers
- Faster checkout

---

## 📊 DAILY CHECKLIST

**Start of Day:**
- [ ] Login with your credentials
- [ ] Check stock levels (Report button)
- [ ] Note any low stock items
- [ ] Test receipt printer

**During Operations:**
- [ ] Login before each shift
- [ ] Process checkouts normally
- [ ] Watch for low stock alerts
- [ ] Help elderly customers with large screens

**End of Day:**
- [ ] Generate daily sales report
- [ ] Check total sales
- [ ] Note items to restock
- [ ] Logout

---

## 🆘 COMMON ISSUES

### **"Please enter employee ID"**
→ Fill in BOTH name and ID fields

### **"Out of Stock"**
→ Item has 0 in inventory, update stock first

### **"Payment must be at least $X"**
→ Enter amount ≥ total, cannot be less

### **"Invalid ID Format"**
→ Use only letters, numbers, or hyphens (A-Z, 0-9, -)

### **Can't see receipt**
→ Click CHECKOUT first, receipt shows after payment

### **Buttons disappeared**
→ Shouldn't happen in v1.7! Restart if it does

---

## 📱 KEYBOARD SHORTCUTS

| Key | Action |
|-----|--------|
| Enter | Confirm in dialogs |
| Esc | Cancel dialogs |
| Tab | Move between fields |

---

## 💾 FILE LOCATIONS

**Data Files:**
- Products: `data/products.csv`
- Sales: `data/sales.csv`

**Receipts:**
- PDF receipts: `receipts/` folder

**Reports:**
- Sales reports: `reports/` folder

**Documentation:**
- All guides: `docs/` folder

---

## 🔢 EMPLOYEE ID FORMAT

**Valid formats:**
- EMP001
- CASHIER-001
- JD2024
- STAFF123

**Invalid formats:**
- EMP 001 (no spaces)
- EMP/001 (no slashes)
- EMP"001 (no quotes)

---

## 📞 GETTING HELP

**For Technical Issues:**
1. Check `docs/` folder for guides
2. Read EMPLOYEE_LOGIN_UPDATE.md
3. Review BEGINNERS_GUIDE.md for understanding

**For Program Features:**
1. Check README.md
2. Review IMPROVED_VERSION_GUIDE.md

**For Learning:**
1. Study BEGINNERS_GUIDE.md
2. Experiment with test data
3. Read code comments

---

## 🎯 TIPS FOR EFFICIENCY

1. **Learn product IDs** - Faster than browsing catalog
2. **Use large screen mode** - Helps all customers
3. **Keep login info ready** - Don't waste time searching
4. **Check stock regularly** - Prevent out-of-stock situations
5. **Generate reports daily** - Track your performance
6. **Be patient with elderly** - Large screens are designed for them
7. **Update prices carefully** - Double-check before confirming
8. **Save receipts as backup** - PDF copies are important

---

## 📈 PERFORMANCE TRACKING

**Your sales are tracked by:**
- Employee ID
- Date and time
- Products sold
- Customer names

**View your performance:**
1. Click "📊 REPORT"
2. Filter by date range
3. Check total sales
4. Identify best-selling products

---

## ⭐ BEST PRACTICES

**Do:**
- ✅ Login with correct credentials
- ✅ Verify amounts before confirming
- ✅ Update stock when low
- ✅ Help customers with large screen
- ✅ Generate daily reports
- ✅ Double-check prices

**Don't:**
- ❌ Share your employee ID
- ❌ Skip login process
- ❌ Update prices without verification
- ❌ Ignore low stock warnings
- ❌ Rush elderly customers
- ❌ Forget to print receipts

---

## 🎓 QUICK TRAINING NOTES

**For New Employees:**

**Day 1:** Learn login process, basic checkout
**Day 2:** Practice with elderly customers, large screens
**Day 3:** Learn stock management
**Day 4:** Learn price updates, reports
**Day 5:** Full operations, troubleshooting

**Training Checklist:**
- [ ] Can login successfully
- [ ] Can add products to cart
- [ ] Can process checkout
- [ ] Can use large payment screen
- [ ] Can read change amount to customer
- [ ] Can print/save receipts
- [ ] Can cancel items
- [ ] Can generate reports
- [ ] Can update stock (with permission)
- [ ] Can update prices (with permission)
- [ ] Understands color coding
- [ ] Can help elderly customers

---

## 🌟 VERSION 1.7 NEW FEATURES

**What's New:**
1. **Employee Login Required** - Name + ID before use
2. **Management Security** - Login needed for stock/price changes
3. **HUGE Payment Window** - 900x700px, 72pt font
4. **LARGE Completion Screen** - Clear payment/change display
5. **Employee Tracking** - All sales linked to employee ID

**Why It Matters:**
- Better accountability
- Easier for elderly customers
- More secure inventory management
- Better sales tracking
- Professional appearance

---

## 📋 PRINT THIS PAGE

**Keep this reference card near your cash register!**

Cut along the dotted lines and laminate for durability.

---

**Version 1.7 • November 3, 2025**  
**© Akbar Jaya Store**  
**Made with ❤️ by Claude AI**
