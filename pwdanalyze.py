import tkinter as tk
from tkinter import messagebox, scrolledtext
from crypto_utils import load_master_password
from password_utils import evaluate_password, generate_strong_password, load_common_passwords
from vault_utils import save_to_vault, load_vault, search_credentials, delete_credential


class PasswordManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Password Manager")
        self.geometry("800x600")
        self.resizable(False, False)
        self.master_key = None
        self.common_passwords = load_common_passwords()

        self.frames = {}
        for F in (MasterKeyScreen, MenuScreen, SaveCredentialsScreen, AnalyzerScreen, ViewCredentialsScreen):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MasterKeyScreen)

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()

class MasterKeyScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Enter Master Password", font=("Arial", 14)).pack(pady=20)
        self.entry = tk.Entry(self, show="*")
        self.entry.pack(pady=10)
        tk.Button(self, text="Login", command=self.verify_password).pack(pady=10)

    def verify_password(self):
        password = self.entry.get()
        key = load_master_password(password)
        if key:
            self.master.master_key = key
            self.master.show_frame(MenuScreen)
        else:
            messagebox.showerror("Error", "Incorrect Master Password")

class MenuScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Main Menu", font=("Arial", 16)).pack(pady=20)
        tk.Button(self, text="Save Credentials", command=lambda: master.show_frame(SaveCredentialsScreen), width=30).pack(pady=5)
        tk.Button(self, text="Analyze/Generate Password", command=lambda: master.show_frame(AnalyzerScreen), width=30).pack(pady=5)
        tk.Button(self, text="View Saved Credentials", command=lambda: master.show_frame(ViewCredentialsScreen), width=30).pack(pady=5)
        tk.Button(self, text="Exit", command=master.destroy, width=30).pack(pady=5)

class SaveCredentialsScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Save Credentials", font=("Arial", 14)).pack(pady=10)

        tk.Label(self, text="Website:").pack()
        self.website = tk.Entry(self, width=40)
        self.website.pack(pady=2)

        tk.Label(self, text="Username/Email:").pack()
        self.username = tk.Entry(self, width=40)
        self.username.pack(pady=2)

        tk.Label(self, text="Password:").pack()
        self.password = tk.Entry(self, width=40)
        self.password.pack(pady=2)

        tk.Button(self, text="Save", command=self.save_credentials).pack(pady=10)
        tk.Button(self, text="Back", command=lambda: master.show_frame(MenuScreen)).pack()

    def save_credentials(self):
        website = self.website.get()
        username = self.username.get()
        password = self.password.get()
        save_to_vault(website, username, password, self.master.master_key)
        messagebox.showinfo("Saved", "Credentials saved successfully")

class AnalyzerScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Password Analyzer / Generator", font=("Arial", 14)).pack(pady=10)

        tk.Label(self, text="Enter Password to Analyze:").pack()
        self.analyze_input = tk.Entry(self, width=40)
        self.analyze_input.pack(pady=5)
        tk.Button(self, text="Analyze", command=self.analyze).pack()

        self.result = tk.Label(self, text="", justify="left", fg="blue")
        self.result.pack(pady=10)

        tk.Label(self, text="Generate Strong Password:").pack(pady=5)
        self.gen_output = tk.Entry(self, width=40)
        self.gen_output.pack(pady=2)
        tk.Button(self, text="Generate", command=self.generate).pack()

        tk.Button(self, text="Back", command=lambda: master.show_frame(MenuScreen)).pack(pady=10)

    def analyze(self):
        password = self.analyze_input.get()
        result = evaluate_password(password, self.master.common_passwords)
        feedback = "\n".join(result["feedback"])
        text = f"Strength: {result['label']}\nScore: {result['score']}\nCrack Time: {result['time_to_crack']}\n{feedback}"
        self.result.config(text=text)

    def generate(self):
        pwd = generate_strong_password()
        self.gen_output.delete(0, tk.END)
        self.gen_output.insert(0, pwd)

class ViewCredentialsScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Saved Credentials", font=("Arial", 14)).pack(pady=10)

        self.search_entry = tk.Entry(self, width=40)
        self.search_entry.pack(pady=5)
        tk.Button(self, text="Search", command=self.search_credentials).pack(pady=2)

        self.output = scrolledtext.ScrolledText(self, width=50, height=15)
        self.output.pack(pady=5)

        tk.Button(self, text="Refresh", command=self.display_credentials).pack(pady=2)
        tk.Button(self, text="Delete by Website", command=self.delete_credential).pack(pady=2)
        tk.Button(self, text="Back", command=lambda: master.show_frame(MenuScreen)).pack(pady=5)

    def display_credentials(self):
        self.output.delete(1.0, tk.END)
        records = load_vault(self.master.master_key)
        if not records:
            self.output.insert(tk.END, "No credentials saved.")
        else:
            for item in records:
                self.output.insert(tk.END, f"Website: {item['website']}\nUsername: {item['username']}\nPassword: {item['password']}\n\n")

    def search_credentials(self):
        keyword = self.search_entry.get()
        if not keyword:
            messagebox.showwarning("Input Error", "Please enter a website to search.")
            return
        results = search_credentials(keyword, self.master.master_key)
        self.output.delete(1.0, tk.END)
        if results:
            for item in results:
                self.output.insert(tk.END, f"Website: {item['website']}\nUsername: {item['username']}\nPassword: {item['password']}\n\n")
        else:
            self.output.insert(tk.END, "No matching credentials found.")

    def delete_credential(self):
        website = self.search_entry.get()
        if not website:
            messagebox.showwarning("Input Error", "Please enter a website to delete.")
            return
        deleted = delete_credential(website, self.master.master_key)
        if deleted:
            messagebox.showinfo("Deleted", f"Credentials for '{website}' deleted.")
        else:
            messagebox.showinfo("Not Found", f"No credentials found for '{website}'.")
        self.display_credentials()

if __name__ == "__main__":
    app = PasswordManagerApp()
    app.mainloop()