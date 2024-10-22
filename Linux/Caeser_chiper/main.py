import tkinter as tk
from tkinter import messagebox

# Caesar cipher functions


def encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            shift_amount = 65 if char.isupper() else 97
            encrypted_text += chr((ord(char) - shift_amount +
                                  shift) % 26 + shift_amount)
        else:
            encrypted_text += char
    return encrypted_text


def decrypt(text, shift):
    return encrypt(text, -shift)

# GUI Setup


def create_gui():
    def handle_encrypt():
        text = input_text.get("1.0", tk.END).strip()
        shift = int(shift_input.get())
        result = encrypt(text, shift)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, result)

    def handle_decrypt():
        text = input_text.get("1.0", tk.END).strip()
        shift = int(shift_input.get())
        result = decrypt(text, shift)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, result)

    def clear_text():
        input_text.delete("1.0", tk.END)
        output_text.delete("1.0", tk.END)
        shift_input.delete(0, tk.END)

    # Root window
    root = tk.Tk()
    root.title("Caesar Cipher Tool")
    root.configure(bg="#4B0082")  # Dark purple background

    # Labels
    tk.Label(root, text="Enter Text:", bg="#4B0082", fg="yellow").grid(
        row=0, column=0, padx=10, pady=10, sticky=tk.W)
    tk.Label(root, text="Shift:", bg="#4B0082", fg="yellow").grid(
        row=1, column=0, padx=10, pady=10, sticky=tk.W)
    tk.Label(root, text="Result:", bg="#4B0082", fg="yellow").grid(
        row=3, column=0, padx=10, pady=10, sticky=tk.W)

    # Text input for message
    input_text = tk.Text(root, height=5, width=50,
                         wrap=tk.WORD, bg="#EEE8AA", fg="#4B0082")
    input_text.grid(row=0, column=1, padx=10, pady=10)

    # Input for shift
    shift_input = tk.Entry(root, width=10, bg="#EEE8AA", fg="#4B0082")
    shift_input.grid(row=1, column=1, padx=10, pady=10)

    # Buttons
    tk.Button(root, text="Encrypt", command=handle_encrypt, bg="yellow",
              fg="#4B0082", width=15).grid(row=2, column=0, padx=10, pady=10)
    tk.Button(root, text="Decrypt", command=handle_decrypt, bg="yellow",
              fg="#4B0082", width=15).grid(row=2, column=1, padx=10, pady=10)
    tk.Button(root, text="Clear", command=clear_text, bg="yellow",
              fg="#4B0082", width=15).grid(row=2, column=2, padx=10, pady=10)

    # Output for result
    output_text = tk.Text(root, height=5, width=50,
                          wrap=tk.WORD, bg="#EEE8AA", fg="#4B0082")
    output_text.grid(row=3, column=1, padx=10, pady=10)

    # Main loop
    root.mainloop()


# Start GUI
create_gui()
