# ⚡ QUICK START GUIDE

**For users who want to get started immediately!**

---

## 🚀 FASTEST WAY TO START

### **Step 1: Double-Click This File**
```
RUN_IMPROVED.bat
```

### **Step 2: Choose Your Language**
Look at the **top-right corner** and click:
- 🇬🇧 **English** 
- 🇮🇩 **Indonesia**

### **Step 3: Select Your Mode**
Click one of these:
- **💳 Start as Cashier** - Process sales
- **📦 Update Stock** - Modify inventory
- **💰 Update Prices** - Change prices

### **Step 4: Login**
- **Employee ID**: Enter your ID (e.g., E001)
- **Name**: Enter your name

**New user?** The system will offer to register you!

### **Step 5: Start Working!**
You're ready to use the system!

---

## 💳 CASHIER MODE QUICK GUIDE

### **Making a Sale:**

1. **Browse Products**
   - Click catalog buttons (AJ, PK, OB)
   - Click products to add to cart

2. **Checkout**
   - Click green **"💳 CHECKOUT"** button
   - Enter payment amount
   - Enter customer name (optional)
   - Receipt appears automatically!

3. **Print Receipt**
   - Click blue **"🖨️ PRINT"** button
   - Or click purple **"📄 SAVE PDF"** button

4. **Start New Sale**
   - Cart clears automatically after checkout
   - Add new items and repeat!

### **Cancel Items:**
- Click red **"❌ CANCEL ITEM"** button
- Select item to remove

### **Generate Report:**
- Click orange **"📊 GENERATE REPORT"** button
- Select date range
- View or save as PDF

---

## 📦 STOCK MANAGEMENT QUICK GUIDE

### **Update Stock Levels:**

1. **Access Stock Manager**
   - Choose "📦 Update Stock" from welcome screen
   - Login with Employee/Manager/Supervisor role

2. **Update a Product**
   - Click **"✏️ Update"** next to product
   - Enter new stock amount
   - Confirm

3. **Check Stock Alerts**
   - Products with ≤5 items show in **red**
   - Restock these items soon!

---

## 💰 PRICE MANAGEMENT QUICK GUIDE

### **Update Prices:**

1. **Access Price Manager**
   - Choose "💰 Update Prices" from welcome screen
   - Login with Manager/Supervisor role

2. **Update a Price**
   - Click **"✏️ Update"** next to product
   - Enter new price
   - Confirm

3. **Review Changes**
   - All changes are logged automatically
   - Check logs in `logs/` folder

---

## 👥 USER ROLES QUICK REFERENCE

| What You Want to Do | Required Role |
|---------------------|---------------|
| Process sales | Cashier, Manager, Supervisor |
| Update stock | Employee, Manager, Supervisor |
| Update prices | Manager, Supervisor |
| Everything | Supervisor |

---

## 🆘 QUICK TROUBLESHOOTING

### **"Python is not recognized"**
1. Install Python from https://www.python.org/downloads/
2. Check "Add Python to PATH" during installation

### **"ModuleNotFoundError"**
```bash
pip install PyQt6 pandas
```

### **Buttons are not visible**
- Make sure you're using `main_prog_improved.py`
- Press F11 for fullscreen

### **Can't see language selector**
- Press F11 for fullscreen
- Check top-right corner of welcome screen

---

## 📱 KEYBOARD SHORTCUTS

None currently - use mouse/touch for all operations.

---

## 💡 TIPS FOR BEGINNERS

### **For Cashiers:**
- ✅ Browse catalog by clicking category buttons (AJ, PK, OB)
- ✅ Items show stock levels - red = low stock
- ✅ You can add same item multiple times
- ✅ Use "Cancel Item" to remove mistakes
- ✅ Always enter payment amount carefully

### **For Store Managers:**
- ✅ Check stock levels daily
- ✅ Reorder red-marked items (≤5 stock)
- ✅ Review logs regularly
- ✅ Generate weekly sales reports
- ✅ Backup `data/` folder regularly

### **For System Admins:**
- ✅ Create user accounts for all employees
- ✅ Assign appropriate roles
- ✅ Review activity logs for issues
- ✅ Keep backup of entire directory

---

## 📂 IMPORTANT FILES & FOLDERS

### **Don't Touch:**
- `data/products.csv` - Your inventory!
- `data/sales.csv` - Your sales records!
- `data/users.csv` - Your employee list!

### **Safe to Delete:**
- `receipts/*.pdf` - Old receipts (after backup)
- `logs/` - Old logs (after review)
- `archive/` - Old code versions

### **Need Help?**
- Read: `README.md`
- Detailed guide: `PROJECT_OVERVIEW.md`
- Architecture: `SYSTEM_ARCHITECTURE.md`
- All docs: `docs/` folder

---

## 🎯 COMMON WORKFLOWS

### **Daily Opening:**
```
1. Run RUN_IMPROVED.bat
2. Select language
3. Choose "Start as Cashier"
4. Login with your credentials
5. Check stock summary
6. Start processing sales
```

### **Daily Closing:**
```
1. Generate sales report (today's date)
2. Save report as PDF
3. Check stock levels
4. Note items needing restock
5. Close program
6. Optional: Backup data/ folder
```

### **Weekly Tasks:**
```
1. Generate weekly sales report
2. Review activity logs
3. Update prices if needed
4. Restock low items
5. Add new products if needed
```

### **Monthly Tasks:**
```
1. Generate monthly sales report
2. Review all activity logs
3. Backup entire directory
4. Check user accounts
5. Archive old receipts
```

---

## 🎉 YOU'RE READY!

**That's it! You now know enough to:**
- ✅ Process sales
- ✅ Manage inventory
- ✅ Update prices
- ✅ Generate reports
- ✅ Handle daily operations

**For more details, see:**
- `README.md` - Complete user manual
- `PROJECT_OVERVIEW.md` - Full system documentation
- `docs/` - Detailed guides

---

## 📞 NEED MORE HELP?

Check these files in order:

1. **`README.md`** - Main documentation
2. **`docs/BEGINNERS_GUIDE.md`** - Detailed beginner guide
3. **`docs/HOW_TO_RUN.md`** - Setup instructions
4. **`docs/IMPROVED_VERSION_GUIDE.md`** - Complete feature guide
5. **`PROJECT_OVERVIEW.md`** - Full system overview

---

## ✅ QUICK CHECKLIST

**Before First Use:**
- [ ] Python installed
- [ ] PyQt6 and Pandas installed
- [ ] Run RUN_IMPROVED.bat successfully
- [ ] Can see welcome screen
- [ ] Can switch languages

**For Daily Use:**
- [ ] Run program
- [ ] Select language
- [ ] Login with credentials
- [ ] Process sales / manage stock / update prices
- [ ] Generate reports
- [ ] Close program

**For Maintenance:**
- [ ] Check logs weekly
- [ ] Backup data monthly
- [ ] Review stock levels daily
- [ ] Generate weekly reports

---

**Happy Selling! 🎉**

---

**Document**: Quick Start Guide  
**Version**: 1.0  
**Created**: November 7, 2025  
**Purpose**: Get users started in 5 minutes  
**Status**: Complete ✅
