from customtkinter import CTkEntry

def add_entry(parent, placeholder="", default=""):
    entry = CTkEntry(parent, width=750, placeholder_text=placeholder)
    if default:
        entry.insert(0, default)
    entry.pack(pady=(10, 10))
    return entry