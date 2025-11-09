# 🎫 QUICK REFERENCE CARD - Role-Based Access

## 👥 User Roles & Permissions

### 🔑 SUPERVISOR (Highest Level)
```
✅ Cashier Operations
✅ Update Stock
✅ Update Prices
━━━━━━━━━━━━━━━━━━
FULL SYSTEM ACCESS
```

### 🔑 MANAGER
```
✅ Cashier Operations
✅ Update Stock
✅ Update Prices
━━━━━━━━━━━━━━━━━━
FULL SYSTEM ACCESS
```

### 📦 EMPLOYEE
```
❌ Cashier Operations
✅ Update Stock
❌ Update Prices
━━━━━━━━━━━━━━━━━━
STOCK MANAGEMENT ONLY
```

### 💳 CASHIER
```
✅ Cashier Operations
❌ Update Stock
❌ Update Prices
━━━━━━━━━━━━━━━━━━
SALES ONLY
```

---

## 🚀 Quick Start Guide

### First Time Login
1. Click desired action button
2. Enter NEW Employee ID
3. Enter your full name
4. Select your role from dropdown
5. Confirm registration
6. Start using the system!

### Returning User Login
1. Click desired action button
2. Enter your Employee ID
3. Press Login (name optional)
4. Start using the system!

---

## 📋 Common Actions

### As CASHIER
```
✅ CAN DO:
- Process sales
- Add items to cart
- Print receipts
- Generate reports

❌ CANNOT DO:
- Change stock levels
- Modify prices
```

### As EMPLOYEE
```
✅ CAN DO:
- Update stock quantities
- Add new inventory
- View stock levels

❌ CANNOT DO:
- Process sales
- Change prices
```

### As MANAGER/SUPERVISOR
```
✅ CAN DO:
- Everything! Full access
- Override restrictions
- View all logs
```

---

## 🔐 Security Features

### Activity Logging
✅ All actions are logged
✅ Logs stored by date
✅ Includes employee info
✅ Tracks all changes

### Access Control
✅ Role-based permissions
✅ Automatic access denial
✅ Denied attempts logged
✅ Audit trail maintained

---

## 📁 Log File Location

```
logs/
  └── 2025-11-04/
      ├── activity_09-30-15.log
      ├── activity_11-45-22.log
      └── activity_14-20-33.log
```

**Each folder = One day**
**Each file = One session**

---

## ❌ What If Access is Denied?

### You'll see:
```
⚠️ Insufficient Privileges!

Your role: [YOUR_ROLE]
Required: [NEEDED_ROLE]

Contact your supervisor for access.
```

### What to do:
1. Check your role
2. Verify you're using correct feature
3. Contact supervisor if you need access
4. Don't try repeatedly (it's logged!)

---

## 💡 Tips & Best Practices

### For All Users
- ✅ Use your own Employee ID
- ✅ Logout after each session
- ✅ Keep Employee ID secure
- ❌ Don't share credentials

### For Managers/Supervisors
- 📊 Review logs regularly
- 🔍 Check for unusual activity
- 👥 Verify employee roles
- 📝 Update roles as needed

---

## 🆘 Need Help?

### Common Issues

**Problem:** "Employee ID not found"
**Solution:** Register as new user with your name

**Problem:** "Access Denied"
**Solution:** Check your role - you may not have permission

**Problem:** "Can't update stock/price"
**Solution:** Verify your role is Employee+ for stock, Manager+ for price

---

## 📞 Support

**For Technical Issues:**
Contact IT Department

**For Access/Role Changes:**
Contact Store Supervisor

**For Training:**
Refer to full documentation in `docs/` folder

---

## 🎯 Remember

```
ROLE HIERARCHY:
Supervisor > Manager > Employee > Cashier

PERMISSION RULES:
Higher roles can do everything lower roles can do
PLUS their own special privileges
```

---

**Last Updated:** November 4, 2025
**System Version:** 2.0
**Document:** Quick Reference Card
