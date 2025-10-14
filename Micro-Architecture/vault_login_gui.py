"""
Vault Login GUI - Graphical interface for secure vault authentication
This module provides a tkinter-based login window for the processor vault system.
"""

import tkinter as tk
from tkinter import messagebox, ttk
import sys


class VaultLoginGUI:
    def __init__(self, vault_instance):
        """
        Initialize the login GUI.
        
        Args:
            vault_instance: The vault object that manages authentication
        """
        self.vault = vault_instance
        self.authenticated = False
        self.root = tk.Tk()
        self.root.title("LEG Processor - Vault Login")
        self.root.geometry("450x350")
        self.root.resizable(False, False)
        
        # Center window on screen
        self.center_window()
        
        # Configure colors and style
        self.bg_color = "#2C3E50"
        self.fg_color = "#ECF0F1"
        self.accent_color = "#3498DB"
        self.error_color = "#E74C3C"
        self.success_color = "#2ECC71"
        
        self.root.configure(bg=self.bg_color)
        
        # Create GUI elements
        self.create_widgets()
        
        # Bind Enter key to login
        self.root.bind('<Return>', lambda event: self.attempt_login())
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Create all GUI widgets."""
        # Header Frame
        header_frame = tk.Frame(self.root, bg=self.bg_color)
        header_frame.pack(pady=20)
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="🔒 VAULT ACCESS CONTROL",
            font=("Helvetica", 18, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        )
        title_label.pack()
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="LEG Processor Security System",
            font=("Helvetica", 10),
            bg=self.bg_color,
            fg=self.accent_color
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Login Frame
        login_frame = tk.Frame(self.root, bg=self.bg_color)
        login_frame.pack(pady=20, padx=40, fill="both", expand=True)
        
        # Password Label
        password_label = tk.Label(
            login_frame,
            text="Password:",
            font=("Helvetica", 12),
            bg=self.bg_color,
            fg=self.fg_color
        )
        password_label.pack(anchor="w", pady=(10, 5))
        
        # Password Entry
        self.password_entry = tk.Entry(
            login_frame,
            font=("Helvetica", 12),
            show="●",
            bg="#34495E",
            fg=self.fg_color,
            insertbackground=self.fg_color,
            relief="flat",
            bd=0
        )
        self.password_entry.pack(fill="x", ipady=8, pady=(0, 5))
        self.password_entry.focus()
        
        # Show/Hide Password Checkbox
        self.show_password_var = tk.BooleanVar()
        show_password_check = tk.Checkbutton(
            login_frame,
            text="Show password",
            variable=self.show_password_var,
            command=self.toggle_password,
            bg=self.bg_color,
            fg=self.fg_color,
            selectcolor="#34495E",
            activebackground=self.bg_color,
            activeforeground=self.fg_color,
            font=("Helvetica", 9)
        )
        show_password_check.pack(anchor="w", pady=(0, 15))
        
        # Status Label
        self.status_label = tk.Label(
            login_frame,
            text="",
            font=("Helvetica", 10),
            bg=self.bg_color,
            fg=self.error_color,
            wraplength=350
        )
        self.status_label.pack(pady=(0, 10))
        
        # Buttons Frame
        buttons_frame = tk.Frame(login_frame, bg=self.bg_color)
        buttons_frame.pack(fill="x")
        
        # Login Button
        self.login_button = tk.Button(
            buttons_frame,
            text="LOGIN",
            font=("Helvetica", 12, "bold"),
            bg=self.accent_color,
            fg="white",
            activebackground="#2980B9",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.attempt_login,
            padx=20,
            pady=10
        )
        self.login_button.pack(side="left", expand=True, fill="x", padx=(0, 5))
        
        # Cancel Button
        cancel_button = tk.Button(
            buttons_frame,
            text="CANCEL",
            font=("Helvetica", 12, "bold"),
            bg="#95A5A6",
            fg="white",
            activebackground="#7F8C8D",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.on_closing,
            padx=20,
            pady=10
        )
        cancel_button.pack(side="right", expand=True, fill="x", padx=(5, 0))
        
        # Footer
        footer_frame = tk.Frame(self.root, bg=self.bg_color)
        footer_frame.pack(side="bottom", pady=10)
        
        footer_label = tk.Label(
            footer_frame,
            text="Unauthorized access is prohibited",
            font=("Helvetica", 8, "italic"),
            bg=self.bg_color,
            fg="#7F8C8D"
        )
        footer_label.pack()
        
        # Attempt counter
        attempts_text = f"Attempts remaining: {self.vault.max_attempts - self.vault.login_attempts}"
        self.attempts_label = tk.Label(
            footer_frame,
            text=attempts_text,
            font=("Helvetica", 8),
            bg=self.bg_color,
            fg=self.fg_color
        )
        self.attempts_label.pack()
    
    def toggle_password(self):
        """Toggle password visibility."""
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="●")
    
    def attempt_login(self):
        """Attempt to login with the entered password."""
        password = self.password_entry.get()
        
        if not password:
            self.show_status("Please enter a password", self.error_color)
            return
        
        # Attempt login
        success, message = self.vault.login(password)
        
        if success:
            self.show_status(message, self.success_color)
            self.authenticated = True
            self.root.after(1000, self.root.destroy)  # Close after 1 second
        else:
            self.show_status(message, self.error_color)
            self.password_entry.delete(0, tk.END)
            self.update_attempts()
            
            # If max attempts reached, disable login
            if self.vault.login_attempts >= self.vault.max_attempts:
                self.login_button.config(state="disabled")
                self.password_entry.config(state="disabled")
    
    def show_status(self, message, color):
        """Display a status message."""
        self.status_label.config(text=message, fg=color)
    
    def update_attempts(self):
        """Update the attempts counter display."""
        remaining = self.vault.max_attempts - self.vault.login_attempts
        self.attempts_label.config(
            text=f"Attempts remaining: {remaining}",
            fg=self.error_color if remaining <= 1 else self.fg_color
        )
    
    def on_closing(self):
        """Handle window close event."""
        if not self.authenticated:
            result = messagebox.askyesno(
                "Exit",
                "Are you sure you want to exit?\nThe processor will not start without authentication."
            )
            if result:
                self.root.destroy()
                sys.exit(0)
        else:
            self.root.destroy()
    
    def run(self):
        """Run the GUI main loop."""
        self.root.mainloop()
        return self.authenticated


def show_login_gui(vault_instance):
    """
    Show the login GUI and return authentication status.
    
    Args:
        vault_instance: The vault object to authenticate against
        
    Returns:
        bool: True if authentication successful, False otherwise
    """
    gui = VaultLoginGUI(vault_instance)
    return gui.run()


# For standalone testing
if __name__ == "__main__":
    # Create a test vault instance
    from components.vault import vault
    test_vault = vault()
    
    print("Testing Vault Login GUI")
    print("Default password: secure123")
    print("-" * 40)
    
    authenticated = show_login_gui(test_vault)
    
    if authenticated:
        print("\n✓ Authentication successful!")
        print(f"Vault status: {'Unlocked' if test_vault.is_authenticated() else 'Locked'}")
    else:
        print("\n✗ Authentication failed!")
        print("Processor cannot start without vault access.")
