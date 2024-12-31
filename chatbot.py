import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests
import json

def chat_with_bot(api_url, api_key, user_message, model="grok-beta", temperature=0.7):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    messages = conversation + [{"role": "user", "content": user_message}]

    payload = {
        "messages": messages,
        "model": model,
        "temperature": temperature
    }

    response = requests.post(api_url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        result = response.json()
        reply = result.get("choices", [{}])[0].get("message", {}).get("content", "")
        return reply
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

def send_message():
    user_message = message_entry.get()
    if not user_message:
        messagebox.showerror("Error", "Please enter a message.")
        return

    try:
        chatbot_reply = chat_with_bot(API_URL, API_KEY, user_message)
        conversation.append({"role": "user", "content": user_message})
        conversation.append({"role": "assistant", "content": chatbot_reply})

        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, f"You: {user_message}\n", "user")
        chat_display.insert(tk.END, f"Bot: {chatbot_reply}\n\n", "bot")
        chat_display.config(state=tk.DISABLED)
        chat_display.yview(tk.END)
        message_entry.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to communicate with the bot: {e}")

# Constants
API_URL = "https://api.x.ai/v1/chat/completions"  # Replace with your API endpoint
API_KEY = "xai-deZJiuQEXJbLC6oYZRty61joqJ8J0xTmGdOLloh4bGoZAUan1lebvmlZtQ0BJxXmXuWE9V3pnAqM9Tcu"  # Replace with your API key

# Initialize conversation history
conversation = [{"role": "system", "content": "You are a helpful chatbot."}]

# Create the main window
root = tk.Tk()
root.title("Chatbot")
root.geometry("500x600")
root.config(bg="#2C3E50")

# Chat display area with scrollbar
chat_frame = tk.Frame(root, bg="#2C3E50")
chat_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

chat_display = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, width=60, height=20, state=tk.DISABLED, font=("Arial", 12), bg="#ECF0F1", fg="#2C3E50")
chat_display.tag_config("user", foreground="#2980B9", font=("Arial", 12, "bold"))
chat_display.tag_config("bot", foreground="#27AE60", font=("Arial", 12, "italic"))
chat_display.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Message entry field
entry_frame = tk.Frame(root, bg="#2C3E50")
entry_frame.pack(pady=5, padx=10, fill=tk.X)

message_entry = tk.Entry(entry_frame, width=40, font=("Arial", 14), bg="#ECF0F1", fg="#2C3E50")
message_entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

# Send button
send_button = tk.Button(entry_frame, text="Send", command=send_message, font=("Arial", 12, "bold"), bg="#3498DB", fg="white", relief=tk.FLAT, width=10)
send_button.pack(side=tk.RIGHT, padx=5, pady=5)

# Run the main event loop
root.mainloop()
