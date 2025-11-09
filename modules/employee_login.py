"""
EMPLOYEE LOGIN DIALOG - WITH TRANSLATION SUPPORT
Handles employee authentication and registration with role-based access
"""

import os
import pandas as pd
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QInputDialog, QMessageBox, QWidget, QLineEdit, QFormLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from datetime import datetime

# Import translation system
from modules.translations import LanguageManager, tr


class EmployeeLoginDialog(QDialog):
    """Dialog for employee login with name and ID - now with user database and role-based access"""
    
    def __init__(self, parent=None, for_management=False, required_action=None):
        super().__init__(parent)
        self.setWindowTitle(tr('login_title'))
        self.resize(700, 550)  # Bigger window
        self.setMinimumSize(700, 550)
        self.setStyleSheet("QDialog { background-color: #f8fafc; }")
        self.setModal(True)
        
        self.employee_name = tr('cashier_label')
        self.employee_id = "000"
        self.employee_role = tr('role_cashier')
        self.for_management = for_management
        self.required_action = required_action
        
        # Store UI elements for translation updates
        self.ui_elements = {}
        
        # Register for language changes
        LanguageManager.register_observer(self.update_translations)
        
        self.users_df = self.load_users()
        self.init_ui()
        self.center_on_screen()  # Center dialog on screen
    
    def load_users(self):
        """Load users from CSV file"""
        users_path = os.path.join("data", "users.csv")
        os.makedirs("data", exist_ok=True)
        
        if not os.path.exists(users_path) or os.stat(users_path).st_size == 0:
            default_users = pd.DataFrame([{
                'employee_id': 'SUPER001',
                'name': 'Supervisor',
                'role': 'Supervisor',
                'date_registered': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'active': True
            }])
            default_users.to_csv(users_path, index=False)
            return default_users
        
        try:
            return pd.read_csv(users_path)
        except Exception as e:
            print(f"[ERROR] Failed to load users.csv: {e}")
            return pd.DataFrame(columns=['employee_id', 'name', 'role', 'date_registered', 'active'])
    
    def save_user(self, employee_id, name, role='Cashier'):
        """Save new user to CSV"""
        users_path = os.path.join("data", "users.csv")
        new_user = pd.DataFrame([{
            'employee_id': employee_id,
            'name': name,
            'role': role,
            'date_registered': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'active': True
        }])
        self.users_df = pd.concat([self.users_df, new_user], ignore_index=True)
        self.users_df.to_csv(users_path, index=False)
        print(f"[INFO] New user registered: {name} (ID: {employee_id}, Role: {role})")
    
    def user_exists(self, employee_id):
        """Check if user exists in database"""
        if self.users_df.empty:
            return False
        return employee_id in self.users_df['employee_id'].values
    
    def get_user_info(self, employee_id):
        """Get user info from employee ID"""
        user = self.users_df[self.users_df['employee_id'] == employee_id]
        if not user.empty:
            return {'name': user.iloc[0]['name'], 'role': user.iloc[0]['role']}
        return None
    
    def check_access_permission(self, role, action):
        """Check if a role has permission for an action"""
        permissions = {
            'Supervisor': ['cashier', 'stock_update', 'price_update'],
            'Manager': ['cashier', 'stock_update', 'price_update'],
            'Employee': ['stock_update'],
            'Cashier': ['cashier']
        }
        return action in permissions.get(role, [])
    
    def init_ui(self):
        """Initialize login dialog UI"""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        self.setLayout(layout)
        
        # Title - dynamic based on required action
        if self.required_action == "stock_update":
            title_text = f"📦 {tr('stock_manager_title')}"
            subtitle_text = tr('stock_option_desc')
        elif self.required_action == "price_update":
            title_text = f"💰 {tr('price_manager_title')}"
            subtitle_text = tr('price_option_desc')
        else:
            title_text = tr('login_title')
            subtitle_text = tr('login_subtitle')
        
        title = QLabel(title_text)
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            color: #1e40af;
            background-color: #dbeafe;
            padding: 20px;
            border-radius: 10px;
        """)
        layout.addWidget(title)
        self.ui_elements['title'] = title
        
        subtitle = QLabel(subtitle_text)
        subtitle.setFont(QFont("Arial", 14))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #64748b; margin: 10px;")
        layout.addWidget(subtitle)
        self.ui_elements['subtitle'] = subtitle
        
        # Form container
        form_container = QWidget()
        form_container.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_container.setLayout(form_layout)
        
        # Name input
        self.name_input = QLineEdit()
        self.name_input.setFont(QFont("Arial", 14))
        self.name_input.setPlaceholderText(tr('employee_name_placeholder'))
        self.name_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #cbd5e1;
                border-radius: 8px;
                font-size: 16px;
            }
            QLineEdit:focus {
                border: 2px solid #3b82f6;
            }
        """)
        
        name_label = QLabel(tr('employee_name_label'))
        name_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        name_label.setStyleSheet("color: #1e293b;")
        form_layout.addRow(name_label, self.name_input)
        self.ui_elements['name_label'] = name_label
        
        # ID input
        self.id_input = QLineEdit()
        self.id_input.setFont(QFont("Arial", 14))
        self.id_input.setPlaceholderText(tr('employee_id_placeholder'))
        self.id_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #cbd5e1;
                border-radius: 8px;
                font-size: 16px;
            }
            QLineEdit:focus {
                border: 2px solid #3b82f6;
            }
        """)
        
        id_label = QLabel(tr('employee_id_label'))
        id_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        id_label.setStyleSheet("color: #1e293b;")
        form_layout.addRow(id_label, self.id_input)
        self.ui_elements['id_label'] = id_label
        
        layout.addWidget(form_container)
        
        # Buttons
        buttons_container = QWidget()
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        buttons_container.setLayout(buttons_layout)
        
        # Login button
        login_btn = QPushButton(tr('login_button'))
        login_btn.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        login_btn.setMinimumHeight(60)
        login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: white;
                border-radius: 10px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        login_btn.clicked.connect(self.validate_and_accept)
        buttons_layout.addWidget(login_btn)
        self.ui_elements['login_btn'] = login_btn
        
        # Cancel button
        cancel_btn = QPushButton(tr('cancel_button'))
        cancel_btn.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        cancel_btn.setMinimumHeight(60)
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #ef4444;
                color: white;
                border-radius: 10px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #dc2626;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        self.ui_elements['cancel_btn'] = cancel_btn
        
        layout.addWidget(buttons_container)
        self.id_input.setFocus()
    
    def update_translations(self):
        """Update UI text when language changes"""
        # Update title based on context
        if self.required_action == "stock_update":
            self.ui_elements['title'].setText(f"📦 {tr('stock_manager_title')}")
            self.ui_elements['subtitle'].setText(tr('stock_option_desc'))
        elif self.required_action == "price_update":
            self.ui_elements['title'].setText(f"💰 {tr('price_manager_title')}")
            self.ui_elements['subtitle'].setText(tr('price_option_desc'))
        else:
            self.ui_elements['title'].setText(tr('login_title'))
            self.ui_elements['subtitle'].setText(tr('login_subtitle'))
        
        self.ui_elements['name_label'].setText(tr('employee_name_label'))
        self.ui_elements['id_label'].setText(tr('employee_id_label'))
        self.ui_elements['login_btn'].setText(tr('login_button'))
        self.ui_elements['cancel_btn'].setText(tr('cancel_button'))
        self.name_input.setPlaceholderText(tr('employee_name_placeholder'))
        self.id_input.setPlaceholderText(tr('employee_id_placeholder'))
        self.setWindowTitle(tr('login_title'))
    
    def validate_and_accept(self):
        """Validate inputs, check database, and accept or register"""
        name = self.name_input.text().strip()
        emp_id = self.id_input.text().strip()
        
        if not emp_id:
            QMessageBox.warning(self, tr('login_error_title'), tr('login_error_empty'))
            self.id_input.setFocus()
            return
        
        if self.user_exists(emp_id):
            user_info = self.get_user_info(emp_id)
            registered_name = user_info['name']
            user_role = user_info['role']
            
            if self.required_action:
                if not self.check_access_permission(user_role, self.required_action):
                    QMessageBox.warning(
                        self, tr('login_error_access_denied'),
                        f"{tr('login_error_access_denied')}\n\n"
                        f"{tr('role_' + user_role.lower())}: {user_role}"
                    )
                    return
            
            self.employee_name = registered_name
            self.employee_id = emp_id
            self.employee_role = user_role
            
            QMessageBox.information(
                self, tr('login_success'),
                f"✅ {tr('login_welcome')}, {registered_name}!\n\n"
                f"{tr('employee_id_label')} {emp_id}\n"
                f"{tr('register_role_label')} {tr('role_' + user_role.lower())}"
            )
            self.accept()
        else:
            if not name:
                QMessageBox.warning(
                    self, tr('register_title'),
                    f"{tr('login_error_not_found')}"
                )
                self.name_input.setFocus()
                return
            self.show_registration_dialog(emp_id, name)
    
    def show_registration_dialog(self, emp_id, name):
        """Show registration confirmation dialog"""
        msg = QMessageBox(self)
        msg.setWindowTitle(tr('register_title'))
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setText(f"🆕 {tr('register_title')}\n\n{tr('employee_id_label')} {emp_id}\n{tr('employee_name_label')} {name}")
        
        register_btn = msg.addButton(tr('register_button_submit'), QMessageBox.ButtonRole.AcceptRole)
        cancel_btn = msg.addButton(tr('cancel_button'), QMessageBox.ButtonRole.RejectRole)
        msg.exec()
        
        if msg.clickedButton() == register_btn:
            role_dialog = QInputDialog(self)
            role_dialog.setWindowTitle(tr('register_role_label'))
            role_dialog.setLabelText(tr('register_role_label'))
            role_dialog.setComboBoxItems([
                tr('role_cashier'), tr('role_employee'),
                tr('role_manager'), tr('role_supervisor')
            ])
            
            if role_dialog.exec() == QDialog.DialogCode.Accepted:
                role_text = role_dialog.textValue()
                # Map back to English for storage
                role_map = {
                    tr('role_cashier'): 'Cashier',
                    tr('role_employee'): 'Employee',
                    tr('role_manager'): 'Manager',
                    tr('role_supervisor'): 'Supervisor'
                }
                role = role_map.get(role_text, 'Cashier')
                
                self.save_user(emp_id, name, role)
                QMessageBox.information(
                    self, tr('register_success'),
                    f"✅ {tr('register_success_message')}!\n\n{name}\n{emp_id}\n{role_text}"
                )
                self.employee_name = name
                self.employee_id = emp_id
                self.employee_role = role
                self.accept()
    
    def center_on_screen(self):
        """Center the dialog on the current screen"""
        from PyQt6.QtWidgets import QApplication
        screen = QApplication.primaryScreen()
        if screen:
            screen_geometry = screen.availableGeometry()
            x = (screen_geometry.width() - self.width()) // 2
            y = (screen_geometry.height() - self.height()) // 2
            self.move(x, y)
    
    def closeEvent(self, event):
        """Clean up when closing"""
        LanguageManager.unregister_observer(self.update_translations)
        super().closeEvent(event)
