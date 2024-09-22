import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3

# Database setup
conn = sqlite3.connect('bmi_data.db')
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS bmi_records (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    height REAL NOT NULL,
    weight REAL NOT NULL,
    bmi REAL NOT NULL,
    category TEXT NOT NULL
)
''')
conn.commit()

class BMICalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BMI Calculator")
        self.geometry("500x650")
        self.configure(bg='#e6f2ff')

        # Center window on screen
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

        # Initialize image label
        self.bmi_image_label = None

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self, text="BMI Calculator", font=("Arial", 26, "bold"), bg='#e6f2ff', fg="#333")
        title_label.pack(pady=20)

        # Name
        self.name_label = tk.Label(self, text="Name:", font=("Arial", 14), bg='#e6f2ff')
        self.name_label.pack()
        self.name_entry = tk.Entry(self, font=("Arial", 14), bd=2, relief="groove")
        self.name_entry.pack(pady=5)

        # Height
        self.height_label = tk.Label(self, text="Height (in meters):", font=("Arial", 14), bg='#e6f2ff')
        self.height_label.pack()
        self.height_entry = tk.Entry(self, font=("Arial", 14), bd=2, relief="groove")
        self.height_entry.pack(pady=5)

        # Weight
        self.weight_label = tk.Label(self, text="Weight (in kg):", font=("Arial", 14), bg='#e6f2ff')
        self.weight_label.pack()
        self.weight_entry = tk.Entry(self, font=("Arial", 14), bd=2, relief="groove")
        self.weight_entry.pack(pady=5)

        # Calculate Button
        self.calculate_button = tk.Button(self, text="Calculate BMI", font=("Arial", 14), bg="#4CAF50", fg="white", relief="raised", command=self.calculate_bmi)
        self.calculate_button.pack(pady=20)

        # Display Result
        self.result_label = tk.Label(self, text="", font=("Arial", 16), bg='#e6f2ff')
        self.result_label.pack(pady=20)

        # View History Button
        self.view_history_button = tk.Button(self, text="View History", font=("Arial", 14), bg="#2196F3", fg="white", relief="raised", command=self.view_history)
        self.view_history_button.pack(pady=10)

        # Graph Button
        self.view_graph_button = tk.Button(self, text="View BMI Trend", font=("Arial", 14), bg="#FF9800", fg="white", relief="raised", command=self.view_bmi_trend)
        self.view_graph_button.pack(pady=10)

    def calculate_bmi(self):
        name = self.name_entry.get().strip()
        try:
            height = float(self.height_entry.get())
            weight = float(self.weight_entry.get())

            # Validation of reasonable input ranges
            if height <= 0 or height > 3:
                raise ValueError("Height must be between 0 and 3 meters.")
            if weight <= 0 or weight > 500:
                raise ValueError("Weight must be between 0 and 500 kg.")
        except ValueError as e:
            messagebox.showerror("Invalid Input", f"Please enter valid values. Error: {str(e)}")
            return

        if not name:
            messagebox.showerror("Invalid Input", "Please enter your name.")
            return

        bmi = weight / (height ** 2)
        bmi_category = self.get_bmi_category(bmi)

        self.result_label.config(text=f"Your BMI is {bmi:.2f} ({bmi_category})")

        self.save_bmi_record(name, height, weight, bmi, bmi_category)
        

    def get_bmi_category(self, bmi):
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obese"

    def save_bmi_record(self, name, height, weight, bmi, category):
        c.execute('''
        INSERT INTO bmi_records (name, height, weight, bmi, category) 
        VALUES (?, ?, ?, ?, ?)''', (name, height, weight, bmi, category))
        conn.commit()

    def view_history(self):
        records_window = tk.Toplevel(self)
        records_window.title("BMI History")
        records_window.geometry("1200x500")
        records_window.configure(bg="#f9f9f9")

        columns = ("ID", "Name", "Height", "Weight", "BMI", "Category")

        self.tree = ttk.Treeview(records_window, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Fetch records from the database
        c.execute("SELECT id, name, height, weight, bmi, category FROM bmi_records")
        records = c.fetchall()
        for record in records:
            self.tree.insert("", tk.END, values=record)

        # Add Delete Record Button in the history window
        self.delete_button = tk.Button(records_window, text="Delete Selected Record", font=("Arial", 14), bg="#f44336", fg="white", relief="raised", command=self.delete_record)
        self.delete_button.pack(pady=10)

    def delete_record(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            record_id = item["values"][0]
            self.tree.delete(selected_item)
            c.execute("DELETE FROM bmi_records WHERE id=?", (record_id,))
            conn.commit()
            messagebox.showinfo("Deleted", "Record deleted successfully!")
        else:
            messagebox.showwarning("No Selection", "Please select a record to delete.")

    def view_bmi_trend(self):
        c.execute("SELECT name, bmi FROM bmi_records ORDER BY id")
        records = c.fetchall()
        if not records:
            messagebox.showerror("No Data", "No BMI records to display.")
            return

        names = [r[0] for r in records]
        bmis = [r[1] for r in records]

        fig, ax = plt.subplots()
        ax.plot(names, bmis, marker='o', linestyle='-', color='b')

        ax.set_xlabel('Name')
        ax.set_ylabel('BMI')
        ax.set_title('BMI Trend')
        ax.grid(True)

        graph_window = tk.Toplevel(self)
        graph_window.title("BMI Trend Graph")
        graph_window.geometry("600x400")

        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Running the app
if __name__ == "__main__":
    app = BMICalculatorApp()
    app.mainloop()
 