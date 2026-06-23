import tkinter as tk
from tkinter import messagebox
import TransactionalUserOps as Ops
import MxAdminOps as MxOps

def create_gui():
    # create a window without the native title bar so we can draw a custom dark title bar
    root = tk.Tk()
    root.overrideredirect(True)
    root.geometry("520x220")

    # close handler (keeps GUI alive after cleaning up driver)
    def on_close():
        try:
            Ops.quit_driver()
        except Exception:
            pass
        try:
            root.destroy()
        except Exception:
            pass

    # outer container with dark background
    container = tk.Frame(root, bg="#121212", bd=0)
    container.pack(expand=True, fill="both")

    # custom title bar (black)
    titlebar = tk.Frame(container, bg="#000000", relief="flat")
    titlebar.pack(fill="x")

    title_label = tk.Label(titlebar, text="Open Risk From Region", bg="#000000", fg="#ffffff")
    title_label.pack(side="left", padx=(8, 0))

    # a simple close button on the title bar
    close_btn = tk.Button(titlebar, text="✕", bg="#8B0000", fg="#ffffff", bd=0, activebackground="#330000",
                          activeforeground="#ffffff", command=on_close)
    close_btn.pack(side="right", padx=6, pady=2)

    # allow moving the window by dragging the title bar
    def _start_move(event):
        root._drag_x = event.x
        root._drag_y = event.y

    def _do_move(event):
        x = root.winfo_x() + (event.x - getattr(root, "_drag_x", 0))
        y = root.winfo_y() + (event.y - getattr(root, "_drag_y", 0))
        root.geometry(f"+{x}+{y}")

    titlebar.bind("<Button-1>", _start_move)
    titlebar.bind("<B1-Motion>", _do_move)
    title_label.bind("<Button-1>", _start_move)
    title_label.bind("<B1-Motion>", _do_move)

    # content area (dark)
    content = tk.Frame(container, bg="#121212")
    content.pack(fill="both", expand=True, padx=8, pady=(8, 12))
    # make the second column expand so entries/buttons use available space
    content.grid_columnconfigure(1, weight=1)

    lbl = tk.Label(content, text="Database Name:", bg="#121212", fg="#e0e0e0")
    lbl.grid(row=0, column=0, padx=6, pady=6, sticky='e')
    entry = tk.Entry(content, width=34, bg="#1e1e1e", fg="#ffffff", insertbackground="#ffffff", relief="flat")
    entry.grid(row=0, column=1, padx=6, pady=6)

    # Quote/Policy input
    quote_lbl = tk.Label(content, text="Quote/Policy number:", bg="#121212", fg="#e0e0e0")
    quote_lbl.grid(row=2, column=0, padx=6, pady=6, sticky='e')
    quote_entry = tk.Entry(content, width=34, bg="#1e1e1e", fg="#ffffff", insertbackground="#ffffff", relief="flat")
    quote_entry.grid(row=2, column=1, padx=6, pady=6)

    def _on_open():
        current_DB = entry.get().strip()
        if not current_DB:
            messagebox.showwarning("Input required", "Please enter a DB name")
            return  
        Ops.init(current_DB)

    #temporaneamente chiama uniqueid e non quotenumber/policynumber
    def _on_quote():
        input_number = quote_entry.get().strip()
        if not input_number:
            messagebox.showwarning("Input required", "Please enter a Quote/Policy number.")
            return
        try:
            #DE-COMMENTA QUANDO l'open with number è pronto e sostituisci la chiamata qua sotto Ops.open_with_number(input_number, root)
            Ops.open_with_uniqueid(input_number, root)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Quote/Policy: {e}")

    def _on_mxadmin():
        # ensure a webdriver session exists in TransactionalUserOps
        try:
            if Ops.defaultDriver is None:
                Ops.defaultDriver = Ops.webdriver.Chrome(options=Ops.options)
        except Exception as e:
            messagebox.showerror("Error", f"Could not start WebDriver: {e}")
            return
        try:
            MxOps.open_mxadmin_index(driver=Ops.defaultDriver)
        except Exception as e:
            messagebox.showerror("Error", f"MX Admin action failed: {e}")
    btn_connect = tk.Button(content, text="Connect to DB", command=_on_open, bg="#2b2b2b", fg="#ffffff", activebackground="#3a3a3a", relief="flat")
    btn_connect.grid(row=1, column=0, padx=6, pady=6, sticky='ew')
    btn_mx = tk.Button(content, text="MX Admin", command=_on_mxadmin, bg="#2b2b2b", fg="#ffffff", activebackground="#3a3a3a", relief="flat")
    btn_mx.grid(row=1, column=1, padx=6, pady=6, sticky='ew')
    # Open Quote button
    btn_quote = tk.Button(content, text="Open Quote (uniqueid temp)", command=_on_quote, bg="#2b2b2b", fg="#ffffff", 
                          activebackground="#3a3a3a", relief="flat")
    btn_quote.grid(row=3, column=0, columnspan=2, padx=6, pady=6, sticky='ew')
    # ensure webdriver quits when window is closed via protocol
    root.protocol("WM_DELETE_WINDOW", on_close)
    root.resizable(False, False)
    root.mainloop()
if __name__ == "__main__":
    create_gui()
