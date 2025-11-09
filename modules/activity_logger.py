"""
LOGGING UTILITY
Handles all logging activities for the cashier system
Creates organized log files by date
"""

import os
from datetime import datetime


class ActivityLogger:
    """Logger for tracking system activities"""
    
    def __init__(self):
        self.base_log_dir = "logs"
        self._ensure_log_directory()
    
    def _ensure_log_directory(self):
        """Ensure the logs directory exists"""
        if not os.path.exists(self.base_log_dir):
            os.makedirs(self.base_log_dir)
    
    def _get_date_folder(self):
        """Get the folder path for today's date"""
        today = datetime.now().strftime("%Y-%m-%d")
        date_folder = os.path.join(self.base_log_dir, today)
        
        # Create folder if it doesn't exist
        if not os.path.exists(date_folder):
            os.makedirs(date_folder)
        
        return date_folder
    
    def _get_log_file_path(self):
        """Get the current log file path with timestamp"""
        date_folder = self._get_date_folder()
        timestamp = datetime.now().strftime("%H-%M-%S")
        log_file = os.path.join(date_folder, f"activity_{timestamp}.log")
        return log_file
    
    def log_activity(self, activity_type, employee_id, employee_name, details):
        """
        Log an activity to file
        
        Args:
            activity_type: Type of activity (LOGIN, STOCK_UPDATE, PRICE_UPDATE, SALE, etc.)
            employee_id: Employee ID performing the action
            employee_name: Employee name
            details: Dictionary with activity details
        """
        log_file = self._get_log_file_path()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Format log entry
        log_entry = f"\n{'='*80}\n"
        log_entry += f"[{timestamp}] {activity_type}\n"
        log_entry += f"Employee: {employee_name} (ID: {employee_id})\n"
        log_entry += "-" * 80 + "\n"
        
        # Add details
        for key, value in details.items():
            log_entry += f"{key}: {value}\n"
        
        log_entry += "=" * 80 + "\n"
        
        # Write to file
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
            print(f"[LOG] Activity logged: {activity_type}")
        except Exception as e:
            print(f"[ERROR] Failed to write log: {e}")
    
    def log_login(self, employee_id, employee_name, role):
        """Log employee login"""
        details = {
            "Action": "Employee Login",
            "Role": role,
            "Status": "Success"
        }
        self.log_activity("LOGIN", employee_id, employee_name, details)
    
    def log_stock_update(self, employee_id, employee_name, product_id, product_name, old_stock, new_stock):
        """Log stock update"""
        details = {
            "Action": "Stock Update",
            "Product ID": product_id,
            "Product Name": product_name,
            "Old Stock": old_stock,
            "New Stock": new_stock,
            "Change": f"{new_stock - old_stock:+d}"
        }
        self.log_activity("STOCK_UPDATE", employee_id, employee_name, details)
    
    def log_price_update(self, employee_id, employee_name, product_id, product_name, old_price, new_price):
        """Log price update"""
        details = {
            "Action": "Price Update",
            "Product ID": product_id,
            "Product Name": product_name,
            "Old Price": f"${old_price:.2f}",
            "New Price": f"${new_price:.2f}",
            "Change": f"${new_price - old_price:+.2f}"
        }
        self.log_activity("PRICE_UPDATE", employee_id, employee_name, details)
    
    def log_sale(self, employee_id, employee_name, customer_name, total_amount, items_count):
        """Log sale transaction"""
        details = {
            "Action": "Sale Transaction",
            "Customer Name": customer_name,
            "Total Amount": f"${total_amount:.2f}",
            "Items Count": items_count,
            "Payment Status": "Completed"
        }
        self.log_activity("SALE", employee_id, employee_name, details)
    
    def log_access_denied(self, employee_id, employee_name, role, attempted_action):
        """Log access denied attempts"""
        details = {
            "Action": "Access Denied",
            "Employee Role": role,
            "Attempted Action": attempted_action,
            "Reason": "Insufficient privileges"
        }
        self.log_activity("ACCESS_DENIED", employee_id, employee_name, details)


# Create a global logger instance
activity_logger = ActivityLogger()
