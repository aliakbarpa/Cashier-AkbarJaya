# 🧪 TESTING GUIDE - Version 2.0 Features

## Testing Role-Based Access & Logging

---

## 📋 Pre-Test Setup

### 1. Ensure Clean Environment
```bash
# Navigate to project directory
cd C:\Users\Public\Documents\AkbarJAYACashier

# Check if logs folder exists (will be auto-created)
# Check if data/users.csv exists (will be auto-created with default supervisor)
```

### 2. Launch Application
```bash
python main_prog_improved.py
```

---

## 🧪 Test Suite 1: Role Registration

### Test 1.1: Register Supervisor
**Steps:**
1. Click "Start as Cashier"
2. Enter ID: `SUPER001`
3. Enter Name: `Test Supervisor`
4. Click Login
5. Select Role: `Supervisor`
6. Click Register

**Expected Result:**
✅ Registration successful
✅ Login granted
✅ Can proceed to cashier mode

**Verify Log:**
```bash
# Check: logs/[TODAY]/activity_[TIME].log
# Should contain: LOGIN entry for SUPER001
```

---

### Test 1.2: Register Manager
**Steps:**
1. Exit and restart application
2. Click "Update Prices"
3. Enter ID: `MGR001`
4. Enter Name: `Test Manager`
5. Select Role: `Manager`

**Expected Result:**
✅ Registration successful
✅ Access granted to price update
✅ Log entry created

---

### Test 1.3: Register Employee
**Steps:**
1. Click "Update Stock"
2. Enter ID: `EMP001`
3. Enter Name: `Test Employee`
4. Select Role: `Employee`

**Expected Result:**
✅ Registration successful
✅ Access granted to stock update
✅ Log entry created

---

### Test 1.4: Register Cashier
**Steps:**
1. Click "Start as Cashier"
2. Enter ID: `CASH001`
3. Enter Name: `Test Cashier`
4. Select Role: `Cashier`

**Expected Result:**
✅ Registration successful
✅ Access granted to cashier mode
✅ Log entry created

---

## 🧪 Test Suite 2: Access Control

### Test 2.1: Cashier Access Control
**Steps:**
1. Login as CASH001 (Cashier)
2. Try to access "Update Stock"

**Expected Result:**
❌ Access DENIED
📝 Error message shows insufficient privileges
📝 ACCESS_DENIED logged

**Verify Log:**
```
[TIME] ACCESS_DENIED
Employee: Test Cashier (ID: CASH001)
Employee Role: Cashier
Attempted Action: stock_update
Reason: Insufficient privileges
```

---

### Test 2.2: Employee Access Control - Stock (Should Pass)
**Steps:**
1. Login as EMP001 (Employee)
2. Click "Update Stock"

**Expected Result:**
✅ Access GRANTED
✅ Stock manager opens
✅ LOGIN logged

---

### Test 2.3: Employee Access Control - Price (Should Fail)
**Steps:**
1. Login as EMP001 (Employee)
2. Click "Update Prices"

**Expected Result:**
❌ Access DENIED
📝 ACCESS_DENIED logged

---

### Test 2.4: Manager Full Access
**Steps:**
1. Login as MGR001 (Manager)
2. Try "Start as Cashier" → Should work ✅
3. Try "Update Stock" → Should work ✅
4. Try "Update Prices" → Should work ✅

**Expected Result:**
✅ All three accesses granted
📝 All three LOGINs logged

---

### Test 2.5: Supervisor Full Access
**Steps:**
1. Login as SUPER001 (Supervisor)
2. Try all three functions

**Expected Result:**
✅ Full access to everything
📝 All activities logged

---

## 🧪 Test Suite 3: Activity Logging

### Test 3.1: Stock Update Logging
**Steps:**
1. Login as EMP001 or higher
2. Update any product stock
3. Change from 50 to 75

**Expected Result:**
✅ Stock updated successfully
📝 Log file created in logs/[TODAY]/

**Verify Log Contains:**
```
[TIME] STOCK_UPDATE
Employee: Test Employee (ID: EMP001)
Action: Stock Update
Product ID: [PRODUCT_ID]
Product Name: [PRODUCT_NAME]
Old Stock: 50
New Stock: 75
Change: +25
```

---

### Test 3.2: Price Update Logging
**Steps:**
1. Login as MGR001 or SUPER001
2. Update any product price
3. Change from $10.00 to $12.50

**Expected Result:**
✅ Price updated successfully
📝 Log entry created

**Verify Log Contains:**
```
[TIME] PRICE_UPDATE
Employee: Test Manager (ID: MGR001)
Action: Price Update
Product ID: [PRODUCT_ID]
Product Name: [PRODUCT_NAME]
Old Price: $10.00
New Price: $12.50
Change: +$2.50
```

---

### Test 3.3: Multiple Updates Same Session
**Steps:**
1. Login once
2. Update 3 different products
3. Check log file

**Expected Result:**
✅ All 3 updates in SAME log file
📝 Single LOGIN entry
📝 Three UPDATE entries

---

### Test 3.4: Log File Organization
**Steps:**
1. Perform activities today
2. Navigate to logs folder
3. Check structure

**Expected Result:**
```
logs/
└── 2025-11-04/
    ├── activity_10-30-15.log
    ├── activity_11-45-22.log
    └── activity_14-20-33.log
```

✅ Folder named with today's date
✅ Files named with time stamps
✅ Each file contains complete session info

---

## 🧪 Test Suite 4: Edge Cases

### Test 4.1: Existing User Login
**Steps:**
1. Login with existing ID: `SUPER001`
2. Leave name field EMPTY
3. Click Login

**Expected Result:**
✅ Auto-filled with registered name
✅ Login successful
✅ No duplicate registration

---

### Test 4.2: Wrong Name for Existing ID
**Steps:**
1. Enter ID: `SUPER001`
2. Enter Name: `Wrong Name`
3. Click Login

**Expected Result:**
⚠️ Name mismatch warning
💬 Prompt to login as registered name
✅ Option to proceed or re-enter

---

### Test 4.3: Register with Insufficient Role
**Steps:**
1. Click "Update Prices"
2. Try to register with role "Cashier"

**Expected Result:**
❌ Registration blocked
⚠️ Warning about insufficient privileges
💬 Prompt to select different role

---

### Test 4.4: Same Action Multiple Times
**Steps:**
1. Update same product stock 3 times
2. Check log file

**Expected Result:**
✅ All 3 updates logged separately
📝 Each with before/after values
📝 Each with timestamp

---

## 📊 Test Results Template

| Test ID | Description | Status | Notes |
|---------|-------------|--------|-------|
| 1.1 | Register Supervisor | ⬜ | |
| 1.2 | Register Manager | ⬜ | |
| 1.3 | Register Employee | ⬜ | |
| 1.4 | Register Cashier | ⬜ | |
| 2.1 | Cashier Denied Stock | ⬜ | |
| 2.2 | Employee Stock Access | ⬜ | |
| 2.3 | Employee Denied Price | ⬜ | |
| 2.4 | Manager Full Access | ⬜ | |
| 2.5 | Supervisor Full Access | ⬜ | |
| 3.1 | Stock Update Log | ⬜ | |
| 3.2 | Price Update Log | ⬜ | |
| 3.3 | Multiple Updates | ⬜ | |
| 3.4 | Log Organization | ⬜ | |
| 4.1 | Existing User Login | ⬜ | |
| 4.2 | Wrong Name Warning | ⬜ | |
| 4.3 | Insufficient Role Block | ⬜ | |
| 4.4 | Multiple Updates | ⬜ | |

**Legend:** ⬜ Not Tested | ✅ Passed | ❌ Failed

---

## 🐛 Common Issues & Solutions

### Issue: Log files not created
**Solution:** Check if `logs` folder exists, should auto-create

### Issue: Access always granted
**Solution:** Check employee_login.py `check_access_permission` function

### Issue: Log entries missing
**Solution:** Verify activity_logger is imported in stock/price managers

### Issue: Multiple folders created
**Solution:** Check system date/time format matches log folder naming

---

## ✅ Final Checklist

After completing all tests:

- [ ] All 4 roles can register
- [ ] Access control works correctly for each role
- [ ] Denied attempts are logged
- [ ] Stock updates are logged with details
- [ ] Price updates are logged with details
- [ ] Log files organized by date
- [ ] Log files named with timestamp
- [ ] Existing users can login
- [ ] Wrong credentials handled properly
- [ ] All activities traced to correct employee

---

## 📝 Report Issues

If any test fails:
1. Note the test ID
2. Record what happened vs. expected
3. Check relevant log files
4. Review employee role in data/users.csv
5. Verify all modules are updated

---

**Testing Date:** ___________________
**Tested By:** ___________________
**Overall Result:** ⬜ PASS | ⬜ FAIL | ⬜ PARTIAL
