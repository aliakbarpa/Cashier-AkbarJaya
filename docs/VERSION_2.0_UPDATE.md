# VERSION 2.0 UPDATE - Role-Based Access & Activity Logging

## Date: November 4, 2025
## New Features Added

---

## 🎯 Feature 1: Activity Logging System

### Overview
All system activities are now automatically logged to organized files by date.

### Log Structure
```
logs/
├── 2025-11-04/
│   ├── activity_10-30-15.log
│   ├── activity_11-45-22.log
│   └── activity_14-20-33.log
├── 2025-11-05/
│   ├── activity_09-15-10.log
│   └── activity_13-42-55.log
└── ...
```

### What Gets Logged
1. **Employee Login**
   - Employee ID and Name
   - Role
   - Login timestamp
   
2. **Stock Updates**
   - Product ID and Name
   - Old stock level
   - New stock level
   - Change amount (+/-)
   - Employee who made the change
   
3. **Price Updates**
   - Product ID and Name
   - Old price
   - New price
   - Change amount (+/-)
   - Employee who made the change
   
4. **Access Denied Attempts**
   - Employee ID and Name
   - Role
   - Attempted action
   - Timestamp

### Log File Format
```
================================================================================
[2025-11-04 10:30:15] STOCK_UPDATE
Employee: John Doe (ID: EMP001)
--------------------------------------------------------------------------------
Action: Stock Update
Product ID: AJ001
Product Name: Beras Premium 5kg
Old Stock: 50
New Stock: 75
Change: +25
================================================================================
```

---

## 🔐 Feature 2: Role-Based Access Control

### Role Hierarchy (Highest to Lowest)

#### 1. **Supervisor** 
- **Access Level:** FULL ACCESS
- **Can do:**
  - ✅ Cashier operations
  - ✅ Update stock
  - ✅ Update prices
- **Badge:** 🔑 Full Access

#### 2. **Manager**
- **Access Level:** FULL ACCESS
- **Can do:**
  - ✅ Cashier operations
  - ✅ Update stock
  - ✅ Update prices
- **Badge:** 🔑 Full Access

#### 3. **Employee**
- **Access Level:** LIMITED ACCESS
- **Can do:**
  - ❌ Cashier operations (DENIED)
  - ✅ Update stock
  - ❌ Update prices (DENIED)
- **Badge:** 📦 Stock Only

#### 4. **Cashier**
- **Access Level:** BASIC ACCESS
- **Can do:**
  - ✅ Cashier operations
  - ❌ Update stock (DENIED)
  - ❌ Update prices (DENIED)
- **Badge:** 💳 Cashier Only

### Access Control Matrix

| Action         | Cashier | Employee | Manager | Supervisor |
|----------------|---------|----------|---------|------------|
| Cashier Mode   | ✅      | ❌       | ✅      | ✅         |
| Update Stock   | ❌      | ✅       | ✅      | ✅         |
| Update Prices  | ❌      | ❌       | ✅      | ✅         |

---

## 📋 How to Use the New Features

### For Users

#### **Starting the System**
1. Launch the application
2. Select desired action (Cashier, Stock, or Price)
3. Login with your Employee ID
4. System checks your role and grants/denies access
5. If granted, proceed with your task

#### **If Access is Denied**
You'll see a message like:
```
⚠️ Insufficient Privileges!

Your role: Cashier
Required action: Stock Update

You do not have permission to perform this action.
Please contact your supervisor.
```

The denied attempt will be logged for security audit.

#### **Registering New Users**
1. Enter a new Employee ID
2. Enter your name
3. Select your role from dropdown:
   - Cashier
   - Employee
   - Manager
   - Supervisor
4. System validates role has permission for current action
5. User is registered and logged in

### For Administrators

#### **Viewing Logs**
Navigate to: `logs/YYYY-MM-DD/`

Each log file contains:
- Timestamp of activity
- Employee who performed it
- Details of what was changed
- Before and after values

#### **Checking Access Attempts**
Look for `ACCESS_DENIED` entries in logs:
```
[2025-11-04 14:30:00] ACCESS_DENIED
Employee: Jane Smith (ID: CASH002)
--------------------------------------------------------------------------------
Action: Access Denied
Employee Role: Cashier
Attempted Action: price_update
Reason: Insufficient privileges
```

---

## 🔧 Technical Implementation

### New Files Created

1. **`modules/activity_logger.py`**
   - Centralized logging utility
   - Automatic folder organization by date
   - Standardized log format

2. **Updated Files:**
   - `modules/employee_login.py` - Added role checking
   - `modules/welcome_screen.py` - Added role-based button descriptions
   - `modules/stock_manager.py` - Added logging calls
   - `modules/price_manager.py` - Added logging calls

### Key Functions

#### ActivityLogger Class
```python
# Log employee login
activity_logger.log_login(emp_id, name, role)

# Log stock update
activity_logger.log_stock_update(emp_id, name, product_id, 
                                  product_name, old_stock, new_stock)

# Log price update
activity_logger.log_price_update(emp_id, name, product_id, 
                                  product_name, old_price, new_price)

# Log access denied
activity_logger.log_access_denied(emp_id, name, role, attempted_action)
```

#### Role Checking
```python
def check_access_permission(role, action):
    permissions = {
        'Supervisor': ['cashier', 'stock_update', 'price_update'],
        'Manager': ['cashier', 'stock_update', 'price_update'],
        'Employee': ['stock_update'],
        'Cashier': ['cashier']
    }
    return action in permissions.get(role, [])
```

---

## 🎓 Security Benefits

### 1. **Accountability**
- Every change is tracked with employee ID
- Audit trail for all modifications
- Easy to find who changed what and when

### 2. **Access Control**
- Prevents unauthorized changes
- Role-based permissions
- Automatic denial logging

### 3. **Compliance**
- Organized log files by date
- Complete audit trail
- Easy to review historical data

### 4. **Fraud Prevention**
- Logs access denied attempts
- Tracks all price/stock changes
- Identifies suspicious patterns

---

## 📊 Example Usage Scenarios

### Scenario 1: Cashier Tries to Update Price
1. Cashier clicks "Update Prices"
2. System checks role: "Cashier"
3. Required permission: "price_update"
4. Access DENIED ❌
5. Attempt logged to file
6. User sees error message

### Scenario 2: Employee Updates Stock
1. Employee clicks "Update Stock"
2. System checks role: "Employee"
3. Required permission: "stock_update"
4. Access GRANTED ✅
5. Login logged to file
6. Employee updates stock
7. Change logged to file

### Scenario 3: Manager Performs All Operations
1. Manager can access all three modes
2. All actions are logged
3. Full audit trail created

---

## 🚀 Testing the Features

### Test Role-Based Access
1. Create user with role "Cashier"
2. Try to access "Update Stock" → Should be DENIED
3. Try to access "Start as Cashier" → Should be GRANTED

### Test Logging
1. Perform any stock/price update
2. Navigate to `logs/TODAY'S_DATE/`
3. Open the latest .log file
4. Verify all details are logged correctly

### Test Access Denied Logging
1. Login as "Cashier"
2. Try to update prices
3. Check log file for ACCESS_DENIED entry

---

## 📝 Summary

**Version 2.0 adds:**
- ✅ Complete activity logging system
- ✅ Role-based access control (4 roles)
- ✅ Automatic log organization by date
- ✅ Access denied tracking
- ✅ Employee role hierarchy
- ✅ Enhanced security and accountability

**All changes are backward compatible** - existing functionality remains unchanged!
