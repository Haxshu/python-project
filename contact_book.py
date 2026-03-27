import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
import re

# ── Data file ──────────────────────────────────────────────────────────────────
DATA_FILE = "contacts.json"

def load_contacts():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_contacts(contacts):
    with open(DATA_FILE, "w") as f:
        json.dump(contacts, f, indent=2)

# ── Validation ─────────────────────────────────────────────────────────────────
def is_valid_phone(phone):
    return bool(re.match(r"^[\d\s\+\-\(\)]{7,20}$", phone.strip()))

def is_valid_email(email):
    if not email:
        return True  # optional
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email.strip()))

# ── Palette ────────────────────────────────────────────────────────────────────
BG        = "#0F0F13"
PANEL     = "#16161E"
CARD      = "#1E1E2A"
ACCENT    = "#7C6AF7"
ACCENT2   = "#A78BFA"
TEXT      = "#E8E8F0"
SUBTEXT   = "#8888AA"
RED       = "#F87171"
GREEN     = "#4ADE80"
BORDER    = "#2A2A3E"
ENTRY_BG  = "#12121A"

FONT_TITLE  = ("Georgia", 22, "bold")
FONT_HEADER = ("Courier New", 10, "bold")
FONT_BODY   = ("Courier New", 11)
FONT_SMALL  = ("Courier New", 9)
FONT_BTN    = ("Courier New", 10, "bold")

# ── Main App ───────────────────────────────────────────────────────────────────
class ContactBook(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Contact Book")
        self.geometry("980x660")
        self.minsize(820, 560)
        self.configure(bg=BG)
        self.contacts = load_contacts()
        self.selected_index = None   # index into self.filtered
        self.filtered = list(self.contacts)
        self._build_ui()
        self.refresh_list()

    # ── UI Construction ────────────────────────────────────────────────────────
    def _build_ui(self):
        # ── Left sidebar ──────────────────────────────────────────────────────
        sidebar = tk.Frame(self, bg=PANEL, width=300)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Logo
        logo_frame = tk.Frame(sidebar, bg=PANEL)
        logo_frame.pack(fill="x", padx=20, pady=(24, 0))
        tk.Label(logo_frame, text="◈", font=("Georgia", 20), fg=ACCENT, bg=PANEL).pack(side="left")
        tk.Label(logo_frame, text=" Contact Book", font=("Georgia", 15, "bold"),
                 fg=TEXT, bg=PANEL).pack(side="left")

        tk.Frame(sidebar, bg=BORDER, height=1).pack(fill="x", padx=20, pady=16)

        # Search
        search_frame = tk.Frame(sidebar, bg=CARD, bd=0, highlightthickness=1,
                                highlightbackground=BORDER)
        search_frame.pack(fill="x", padx=16, pady=(0, 10))
        tk.Label(search_frame, text="⌕", font=("Courier New", 13), fg=SUBTEXT,
                 bg=CARD).pack(side="left", padx=(10, 4), pady=8)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self.do_search())
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                                     font=FONT_BODY, fg=TEXT, bg=CARD,
                                     insertbackground=ACCENT, relief="flat", bd=0)
        self.search_entry.pack(side="left", fill="x", expand=True, pady=8, padx=(0, 8))
        tk.Label(search_frame, text="search", font=FONT_SMALL, fg=SUBTEXT,
                 bg=CARD).pack(side="right", padx=8)

        # Contact list
        list_outer = tk.Frame(sidebar, bg=PANEL)
        list_outer.pack(fill="both", expand=True, padx=16)

        self.count_label = tk.Label(sidebar, text="", font=FONT_SMALL,
                                    fg=SUBTEXT, bg=PANEL)
        self.count_label.pack(pady=(4, 0))

        scrollbar = ttk.Scrollbar(list_outer, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        self.listbox = tk.Listbox(list_outer,
                                  yscrollcommand=scrollbar.set,
                                  font=FONT_BODY,
                                  bg=CARD, fg=TEXT,
                                  selectbackground=ACCENT,
                                  selectforeground="#FFFFFF",
                                  activestyle="none",
                                  relief="flat", bd=0,
                                  highlightthickness=0,
                                  cursor="hand2")
        self.listbox.pack(fill="both", expand=True)
        scrollbar.config(command=self.listbox.yview)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)
        self.listbox.bind("<Double-Button-1>", lambda e: self.edit_contact())

        # ── Right panel ───────────────────────────────────────────────────────
        right = tk.Frame(self, bg=BG)
        right.pack(side="right", fill="both", expand=True)

        # Toolbar
        toolbar = tk.Frame(right, bg=PANEL, height=56)
        toolbar.pack(fill="x")
        toolbar.pack_propagate(False)

        self._btn(toolbar, "＋ New",    self.new_contact,    ACCENT).pack(side="left", padx=(16, 6), pady=10)
        self._btn(toolbar, "✎  Edit",   self.edit_contact,   CARD,  ACCENT2).pack(side="left", padx=6, pady=10)
        self._btn(toolbar, "✕ Delete",  self.delete_contact, CARD,  RED).pack(side="left", padx=6, pady=10)

        self.sort_var = tk.StringVar(value="Name ↑")
        sort_menu = ttk.OptionMenu(toolbar, self.sort_var,
                                   "Name ↑", "Name ↑", "Name ↓", "Newest", "Oldest",
                                   command=lambda _: self.do_search())
        sort_menu.configure(width=10)
        sort_menu.pack(side="right", padx=16, pady=12)
        tk.Label(toolbar, text="Sort:", font=FONT_SMALL, fg=SUBTEXT, bg=PANEL).pack(side="right")

        tk.Frame(right, bg=BORDER, height=1).pack(fill="x")

        # Detail area
        self.detail_frame = tk.Frame(right, bg=BG)
        self.detail_frame.pack(fill="both", expand=True, padx=40, pady=30)
        self._show_empty_state()

    def _btn(self, parent, text, cmd, bg=CARD, fg=TEXT):
        b = tk.Button(parent, text=text, command=cmd,
                      font=FONT_BTN, fg=fg, bg=bg,
                      activebackground=ACCENT, activeforeground="#FFF",
                      relief="flat", bd=0, padx=16, pady=6,
                      cursor="hand2")
        b.bind("<Enter>", lambda e: b.configure(bg=ACCENT if bg == ACCENT else BORDER))
        b.bind("<Leave>", lambda e: b.configure(bg=bg))
        return b

    # ── Empty / Detail states ──────────────────────────────────────────────────
    def _clear_detail(self):
        for w in self.detail_frame.winfo_children():
            w.destroy()

    def _show_empty_state(self):
        self._clear_detail()
        tk.Label(self.detail_frame, text="◈", font=("Georgia", 48),
                 fg=BORDER, bg=BG).pack(pady=(80, 8))
        tk.Label(self.detail_frame,
                 text="Select a contact to view details\nor click ＋ New to add one",
                 font=FONT_BODY, fg=SUBTEXT, bg=BG, justify="center").pack()

    def _show_detail(self, contact):
        self._clear_detail()
        f = self.detail_frame

        # Avatar circle (canvas)
        initials = "".join(p[0].upper() for p in contact["name"].split()[:2])
        canvas = tk.Canvas(f, width=72, height=72, bg=BG, highlightthickness=0)
        canvas.pack(pady=(0, 12))
        canvas.create_oval(4, 4, 68, 68, fill=ACCENT, outline="")
        canvas.create_text(36, 36, text=initials, fill="#FFF",
                           font=("Georgia", 22, "bold"))

        tk.Label(f, text=contact["name"], font=("Georgia", 20, "bold"),
                 fg=TEXT, bg=BG).pack()

        if contact.get("company"):
            tk.Label(f, text=contact["company"], font=FONT_BODY,
                     fg=SUBTEXT, bg=BG).pack(pady=(2, 0))

        tk.Frame(f, bg=BORDER, height=1).pack(fill="x", pady=18)

        fields = [
            ("☎  Phone",   contact.get("phone",   "")),
            ("✉  Email",   contact.get("email",   "")),
            ("⌂  Address", contact.get("address", "")),
            ("✎  Notes",   contact.get("notes",   "")),
        ]
        for label, value in fields:
            if not value:
                continue
            row = tk.Frame(f, bg=CARD, padx=16, pady=10,
                           highlightthickness=1, highlightbackground=BORDER)
            row.pack(fill="x", pady=4)
            tk.Label(row, text=label, font=FONT_HEADER, fg=ACCENT2,
                     bg=CARD, width=12, anchor="w").pack(side="left")
            tk.Label(row, text=value, font=FONT_BODY, fg=TEXT,
                     bg=CARD, anchor="w", wraplength=480, justify="left").pack(side="left")

    # ── Listbox helpers ────────────────────────────────────────────────────────
    def refresh_list(self):
        q = self.search_var.get().lower() if hasattr(self, "search_var") else ""
        self.filtered = [c for c in self.contacts
                         if q in c["name"].lower()
                         or q in c.get("phone", "").lower()
                         or q in c.get("email", "").lower()]

        sort = self.sort_var.get() if hasattr(self, "sort_var") else "Name ↑"
        if sort == "Name ↑":
            self.filtered.sort(key=lambda c: c["name"].lower())
        elif sort == "Name ↓":
            self.filtered.sort(key=lambda c: c["name"].lower(), reverse=True)
        elif sort == "Newest":
            self.filtered = list(reversed(self.filtered))

        self.listbox.delete(0, "end")
        for c in self.filtered:
            self.listbox.insert("end", f"  {c['name']}")

        total = len(self.contacts)
        shown = len(self.filtered)
        label = f"{total} contact{'s' if total != 1 else ''}"
        if shown != total:
            label += f"  ·  {shown} shown"
        self.count_label.configure(text=label)

        # Restore selection if possible
        if self.selected_index is not None and self.selected_index < len(self.filtered):
            self.listbox.selection_set(self.selected_index)
            self._show_detail(self.filtered[self.selected_index])
        else:
            self.selected_index = None
            self._show_empty_state()

    def do_search(self):
        self.selected_index = None
        self.refresh_list()

    def on_select(self, _event=None):
        sel = self.listbox.curselection()
        if not sel:
            return
        self.selected_index = sel[0]
        self._show_detail(self.filtered[self.selected_index])

    # ── CRUD Dialog ────────────────────────────────────────────────────────────
    def _contact_dialog(self, title, contact=None):
        """Opens a modal dialog and returns a filled dict or None."""
        dlg = tk.Toplevel(self)
        dlg.title(title)
        dlg.configure(bg=BG)
        dlg.resizable(False, False)
        dlg.grab_set()

        # Center on parent
        self.update_idletasks()
        x = self.winfo_x() + (self.winfo_width()  - 480) // 2
        y = self.winfo_y() + (self.winfo_height() - 500) // 2
        dlg.geometry(f"480x500+{x}+{y}")

        result = {}

        tk.Label(dlg, text=title, font=("Georgia", 15, "bold"),
                 fg=TEXT, bg=BG).pack(pady=(24, 4))
        tk.Frame(dlg, bg=BORDER, height=1).pack(fill="x", padx=24, pady=(0, 16))

        form = tk.Frame(dlg, bg=BG)
        form.pack(fill="both", expand=True, padx=28)

        entries = {}
        fields = [
            ("name",    "Full Name *"),
            ("phone",   "Phone *"),
            ("email",   "Email"),
            ("company", "Company"),
            ("address", "Address"),
            ("notes",   "Notes"),
        ]

        for key, label in fields:
            tk.Label(form, text=label, font=FONT_HEADER, fg=ACCENT2,
                     bg=BG, anchor="w").pack(fill="x", pady=(6, 2))
            e = tk.Entry(form, font=FONT_BODY, fg=TEXT, bg=ENTRY_BG,
                         insertbackground=ACCENT, relief="flat",
                         highlightthickness=1, highlightbackground=BORDER,
                         highlightcolor=ACCENT)
            e.pack(fill="x", ipady=7, padx=1)
            if contact:
                e.insert(0, contact.get(key, ""))
            entries[key] = e

        entries["name"].focus_set()

        err_label = tk.Label(dlg, text="", font=FONT_SMALL, fg=RED, bg=BG)
        err_label.pack(pady=(6, 0))

        def submit():
            data = {k: v.get().strip() for k, v in entries.items()}
            if not data["name"]:
                err_label.configure(text="⚠  Full name is required.")
                return
            if not data["phone"]:
                err_label.configure(text="⚠  Phone number is required.")
                return
            if not is_valid_phone(data["phone"]):
                err_label.configure(text="⚠  Phone number looks invalid.")
                return
            if data["email"] and not is_valid_email(data["email"]):
                err_label.configure(text="⚠  Email address looks invalid.")
                return
            result.update(data)
            dlg.destroy()

        btn_row = tk.Frame(dlg, bg=BG)
        btn_row.pack(pady=16)
        self._btn(btn_row, "Cancel", dlg.destroy, CARD, SUBTEXT).pack(side="left", padx=6)
        self._btn(btn_row, "Save", submit, ACCENT, "#FFF").pack(side="left", padx=6)

        dlg.bind("<Return>", lambda e: submit())
        dlg.bind("<Escape>", lambda e: dlg.destroy())
        self.wait_window(dlg)
        return result if result else None

    # ── CRUD Actions ───────────────────────────────────────────────────────────
    def new_contact(self):
        data = self._contact_dialog("New Contact")
        if data:
            self.contacts.append(data)
            save_contacts(self.contacts)
            self.selected_index = None
            self.refresh_list()
            # Auto-select new contact
            name = data["name"].lower()
            for i, c in enumerate(self.filtered):
                if c["name"].lower() == name:
                    self.listbox.selection_set(i)
                    self.selected_index = i
                    self._show_detail(c)
                    break

    def edit_contact(self):
        if self.selected_index is None:
            messagebox.showinfo("Edit", "Please select a contact first.")
            return
        contact = self.filtered[self.selected_index]
        data = self._contact_dialog("Edit Contact", contact)
        if data:
            # Find in master list and update
            idx = self.contacts.index(contact)
            self.contacts[idx] = data
            save_contacts(self.contacts)
            self.refresh_list()
            # Re-select
            for i, c in enumerate(self.filtered):
                if c is self.contacts[idx]:
                    self.listbox.selection_set(i)
                    self.selected_index = i
                    self._show_detail(c)
                    break

    def delete_contact(self):
        if self.selected_index is None:
            messagebox.showinfo("Delete", "Please select a contact first.")
            return
        contact = self.filtered[self.selected_index]
        if messagebox.askyesno("Delete Contact",
                               f"Delete '{contact['name']}'?\nThis cannot be undone.",
                               icon="warning"):
            self.contacts.remove(contact)
            save_contacts(self.contacts)
            self.selected_index = None
            self.refresh_list()
            self._show_empty_state()


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = ContactBook()
    app.mainloop()