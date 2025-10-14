import sys
sys.path.append('.')

from components.vault import vault
from vault_login_gui import show_login_gui

def main():
    print("=" * 50)
    print("VAULT LOGIN GUI TEST")
    print("=" * 50)
    print("\nThis is a standalone test of the vault login system.")
    print("\nDefault credentials:")
    print("  Password: secure123")
    print("\nFeatures:")
    print("  • 3 login attempts maximum")
    print("  • Show/hide password option")
    print("  • Visual feedback for success/failure")
    print("  • System lockout after max attempts")
    print("\n" + "=" * 50)
    print("\nOpening login window...")
    print("(Close the window or click Cancel to exit)")
    print("=" * 50 + "\n")
    
    # Create vault instance
    test_vault = vault()
    
    # Show login GUI
    authenticated = show_login_gui(test_vault)
    
    # Display results
    print("\n" + "=" * 50)
    print("AUTHENTICATION RESULT")
    print("=" * 50)
    
    if authenticated:
        print("✓ SUCCESS: Vault access granted!")
        print(f"  Vault status: {'UNLOCKED' if test_vault.is_authenticated() else 'LOCKED'}")
        print(f"  Login attempts used: {test_vault.login_attempts}")
        print("\nThe processor would now start normally...")
    else:
        print("✗ FAILED: Authentication unsuccessful")
        print(f"  Vault status: {'UNLOCKED' if test_vault.is_authenticated() else 'LOCKED'}")
        print(f"  Login attempts: {test_vault.login_attempts}/{test_vault.max_attempts}")
        print("\nThe processor cannot start without authentication.")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
