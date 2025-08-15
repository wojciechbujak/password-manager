from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import pyperclip
import json
import random
import sys, os


LABEL_FONT = ("Helvetica", 12, "bold")
DATA_FILE = "data.json"


PRIMARY = "#0d47a1"
PRIMARY_LIGHT = "#5472d3"
PRIMARY_DARK = "#002171"
ACCENT = "#ffca28"
BG = "#f5f9ff"
SURFACE = "#ffffff"
TEXT = "#0a0a0a"
TEXT_MUTED = "#2d3b55"
NAVY = "#002b5c"

def resource_path(relative_path):

    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)



def setup_styles(root):
    root.configure(bg=BG)
    style = ttk.Style()
    try:
        style.theme_use('clam')
    except:
        pass

    default_font = ("Segoe UI", 10)
    root.option_add("*Font", default_font)


    style.configure(".", background=BG, foreground=TEXT)


    style.configure("TLabelframe", background=SURFACE, borderwidth=1, relief="solid",  bordercolor=NAVY)
    style.configure("TLabelframe.Label", background=SURFACE, foreground=PRIMARY_DARK,
                    font=("Segoe UI", 12, "bold"), anchor="center")


    style.configure("TLabel", background=SURFACE, foreground=TEXT)


    style.configure("TEntry",
        fieldbackground="#ffffff", background="#ffffff", foreground=TEXT,
        insertcolor=TEXT, bordercolor=PRIMARY, lightcolor=PRIMARY, padding=6
    )
    style.map("TEntry",
        bordercolor=[("focus", PRIMARY)], lightcolor=[("focus", PRIMARY)]
    )


    style.configure("TCombobox",
        fieldbackground="#ffffff", background="#ffffff", foreground=TEXT,
        arrowcolor=PRIMARY, padding=6
    )


    style.configure("Accent.TButton",
        background=PRIMARY, foreground="#ffffff",
        padding=(14, 10), borderwidth=0
    )
    style.map("Accent.TButton",
        background=[("active", PRIMARY_LIGHT), ("pressed", PRIMARY_DARK)]
    )




    try:
        root.tk.call('tk', 'scaling', 1.1)
    except:
        pass


def safe_load():
    import os, json
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}





def show_password_popup(website, email, password):
    popup = Toplevel()
    popup.title(f"Details for {website}")
    popup.resizable(False, False)

    Label(popup, text=f"Email:", font=LABEL_FONT).grid(row=0, column=0, sticky="w", padx=8, pady=6)
    email_entry = Entry(popup, width=40)
    email_entry.grid(row=0, column=1, padx=8, pady=6)
    email_entry.insert(0, email)
    email_entry.config(state="readonly")

    Label(popup, text=f"Password:", font=LABEL_FONT).grid(row=1, column=0, sticky="w", padx=8, pady=6)
    password_entry = Entry(popup, width=40)
    password_entry.grid(row=1, column=1, padx=8, pady=6)
    password_entry.insert(0, password)
    password_entry.config(state="readonly")

    def copy_pwd():
        popup.clipboard_clear()
        popup.clipboard_append(password)

    Button(popup, text="Copy Password", command=copy_pwd).grid(row=2, column=1, sticky="e", pady=10, padx=8)


def generate_password():
    letters = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    numbers = list('0123456789')
    symbols = list('!#$%&()*+')

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = (
        [random.choice(letters) for _ in range(nr_letters)] +
        [random.choice(symbols) for _ in range(nr_symbols)] +
        [random.choice(numbers) for _ in range(nr_numbers)]
    )
    random.shuffle(password_list)
    password = "".join(password_list)

    password_entry_add.delete(0, END)
    password_entry_add.insert(0, password)
    pyperclip.copy(password)


def find_password():
    website = website_combo.get().strip()
    if not website:
        messagebox.showerror(title="Error", message="Select or enter a page name.")
        return
    data = safe_load()
    credentials = data.get(website)

    credentials = data.get(website)
    if credentials:
        show_password_popup(website, credentials.get("email", ""), credentials.get("password", ""))
    else:
        messagebox.showerror(title="No entry", message="No details for the specified page.")


def save():
    website = website_entry_add.get().strip()
    email = email_entry_add.get().strip()
    password = password_entry_add.get().strip()
    new_data = {website: {"email": email, "password": password}}

    if not website or not email or not password:
        messagebox.showerror(title="Error", message="Please do not leave any fields blank in the Add section.")
        return

    wrote = False

    try:
        with open("data.json", "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):

        with open("data.json", "w", encoding="utf-8") as file:
            json.dump(new_data, file, indent=4, ensure_ascii=False)
        wrote = True
    else:

        if website in data:
            ok = messagebox.askyesno("Overwriting", f"An entry for '{website}' exists. Overwrite?")
            if not ok:
                return
        data.update(new_data)
        with open("data.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        wrote = True
    finally:

        if wrote:
            try:
                refresh_site_list()

                if 'website_combo' in globals() and website:
                    website_combo.set(website)
            except Exception:
                pass

        website_entry_add.delete(0, END)
        password_entry_add.delete(0, END)

def edit_password():
    website = website_combo.get().strip()
    if not website:
        messagebox.showerror("Error", "Select page to edit.")
        return
    data = safe_load()
    if website not in data:
        messagebox.showerror("Error", "Entry not found.")
        return

    creds = data[website]

    edit_win = Toplevel(window)
    edit_win.title(f"Edit entry: {website}")
    edit_win.resizable(False, False)

    ttk.Label(edit_win, text="Email/Username:").grid(row=0, column=0, padx=8, pady=6, sticky="w")
    email_edit = ttk.Entry(edit_win, width=40)
    email_edit.grid(row=0, column=1, padx=8, pady=6)
    email_edit.insert(0, creds.get("email", ""))

    ttk.Label(edit_win, text="Password:").grid(row=1, column=0, padx=8, pady=6, sticky="w")
    pass_edit = ttk.Entry(edit_win, width=40)
    pass_edit.grid(row=1, column=1, padx=8, pady=6)
    pass_edit.insert(0, creds.get("password", ""))

    def save_changes():
        new_email = email_edit.get().strip()
        new_pass = pass_edit.get().strip()
        if not new_email or not new_pass:
            messagebox.showerror("Error", "Fields cannot be empty.")
            return
        data[website] = {"email": new_email, "password": new_pass}
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        refresh_site_list()
        edit_win.destroy()
        messagebox.showinfo("Success", "The entry has been updated.")

    ttk.Button(edit_win, text="Save changes", style="Accent.TButton", command=save_changes).grid(row=2, column=0, columnspan=2, pady=10)


def delete_password():
    website = website_combo.get().strip()
    if not website:
        messagebox.showerror("Error", "Select the page to delete.")
        return
    data = safe_load()
    if website not in data:
        messagebox.showerror("Error", "Entry not found.")
        return
    confirm = messagebox.askyesno("Confirmation", f"'Are you sure you want to delete the entry {website}'?")
    if confirm:
        del data[website]
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        refresh_site_list()
        website_combo.set("")
        messagebox.showinfo("Success", "The entry has been deleted.")

def toggle_show():
    if password_entry_add.cget('show') == "•":
        password_entry_add.config(show="")
        show_chk.config(text="Hide")
    else:
        password_entry_add.config(show="•")
        show_chk.config(text="Show")


window = Tk()
window.title("Password Manager")
window.geometry("860x520")
setup_styles(window)


window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)

try:
    logo_img = PhotoImage(file=resource_path('logo.png'))
    canvas = Canvas(window, width=200, height=200, highlightthickness=0)
    canvas.create_image(100, 100, image=logo_img)
    canvas.grid(column=0, row=0, columnspan=2, pady=(0, 10))
except Exception as e:
    print("Logo loading error:", e)


left_frame = ttk.LabelFrame(window, text="Add new password", padding=(15, 12))
left_frame.grid(row=1, column=0, sticky="nsew", padx=20)
left_frame.columnconfigure(1, weight=1)

ttk.Label(left_frame, text="Website:").grid(row=0, column=0, sticky=W, pady=4)
website_entry_add = ttk.Entry(left_frame)
website_entry_add.grid(row=0, column=1, columnspan=2, sticky="ew", pady=4)

ttk.Label(left_frame, text="Email/Username:").grid(row=1, column=0, sticky=W, pady=4)
email_entry_add = ttk.Entry(left_frame)
email_entry_add.grid(row=1, column=1, columnspan=2, sticky="ew", pady=4)

ttk.Label(left_frame, text="Password:").grid(row=2, column=0, sticky=W, pady=4)
password_entry_add = ttk.Entry(left_frame, show="•")
password_entry_add.grid(row=2, column=1, columnspan=2, sticky="ew", pady=4)

show_chk = ttk.Checkbutton(left_frame, text="Show", command=toggle_show)
show_chk.grid(row=3, column=1, sticky=W, pady=(2,6))

# przyciski – ładniejsze style
generate_button = ttk.Button(left_frame, text="Generate Password", style="Accent.TButton", command=generate_password)
generate_button.grid(row=4, column=0, columnspan=3, pady=(4,2), sticky="ew")

add_button = ttk.Button(left_frame, text="Add to database", style="Accent.TButton", command=save)
add_button.grid(row=5, column=0, columnspan=3, pady=(2,0), sticky="ew")


right_frame = ttk.LabelFrame(window, text="Search for an existing entry", padding=(15,12))
right_frame.grid(row=1, column=1, sticky="nsew", padx=20)
right_frame.columnconfigure(0, weight=1)

ttk.Label(right_frame, text="Website:").grid(row=0, column=0, sticky=W, pady=4)
website_combo = ttk.Combobox(right_frame, width=30, state="normal")
website_combo.grid(row=1, column=0, sticky="ew", pady=4)

search_button = ttk.Button(right_frame, text="Search", style="Accent.TButton", command=find_password)
search_button.grid(row=2, column=0, pady=(4,0), sticky="ew")

edit_button = ttk.Button(right_frame, text="Edit", style="Accent.TButton", command=edit_password)
edit_button.grid(row=3, column=0, pady=(4,0), sticky="ew")

delete_button = ttk.Button(right_frame, text="Delete", style="Accent.TButton", command=delete_password)
delete_button.grid(row=4, column=0, pady=(4,0), sticky="ew")

def refresh_site_list():
    data = safe_load()
    sites = sorted(list(data.keys()))
    website_combo['values'] = sites

refresh_site_list()

window.bind("<Return>", lambda e: save())
window.bind("<Control-f>", lambda e: find_password())
window.iconphoto(False, PhotoImage(file=resource_path('logo.png')))
window.mainloop()
