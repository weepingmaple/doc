import time
import interception

# Direct Input / DirectX Hardware Scan Codes
SCANCODES = {
    'W': 0x11,
    'A': 0x1E,
    'S': 0x1F,
    'D': 0x20,
    'SPACE': 0x39
}

def run_macro():
    print("Initializing Interception context...")
    
    print("Waiting for game window focus... Switch to the game now (5s countdown).")
    time.sleep(5)
    
    # In this package version, we check for a valid keyboard device context directly
    # Keyboard device IDs typically start at index 1 up to 10
    keyboard_device = 1
    
    print(f"Sending hardware-level inputs to Keyboard Device [{keyboard_device}]...")
    
    # --- SIMULATE HOLDING 'W' FOR 2 SECONDS ---
    print("Moving forward...")
    
    # State 0 = KEY_DOWN (Press and hold)
    interception.press(keyboard_device, SCANCODES['W'])
    
    # Hold the key for a realistic duration so the game engine registers it
    time.sleep(2.0)
    
    # State 1 = KEY_UP (Release key)
    interception.release(keyboard_device, SCANCODES['W'])
    
    print("Movement sequence completed successfully.")

if __name__ == "__main__":
    try:
        run_macro()
    except Exception as e:
        print(f"\nExecution Failed: {e}")
        print("Ensure:")
        print("1. The Interception driver is installed via command prompt.")
        print("2. You restarted your PC after installation.")
        print("3. You are running this Python script explicitly AS AN ADMINISTRATOR.")
