import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
import json
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class EmployeeManager:
    def __init__(self):
        self.data = pd.DataFrame(columns=["Employee_ID","Name","Pay","Report_Viewed","Customer_Satisfaction"])

    def add_employee(self, E_Id, Name, Pay, Report, CSRate):
        self.data.loc[len(self.data)] = [E_Id, Name, Pay, Report, CSRate]

    def save_csv(self, filename="Employee.csv"):
        self.data.to_csv(filename, index=False)

    def load_csv(self, filename="Employee.csv"):
        self.data = pd.read_csv(filename)

    def save_json(self, filename="Employee.json"):
        self.data.to_json(filename, orient="records", indent=4)

    def load_json(self, filename="Employee.json"):
        self.data = pd.read_json(filename)

    def analysis(self):
        if self.data.empty:
            return None 

        df = self.data.copy()

        # scale or cap each metric
        df["Pay_score"] = (df["Pay"] / 1000).clip(upper=100)              
        df["Reports_score"] = df["Report_Viewed"].clip(upper=100)       
        df["CS_score"] = df["Customer_Satisfaction"].clip(0, 100)         

        # weighted performance score
        df["Performance_Score"] = (
            0.2 * df["Pay_score"] +
            0.3 * df["Reports_score"] +
            0.5 * df["CS_score"]
        )

        return df[["Employee_ID", "Name", "Pay_score", "Reports_score", "CS_score", "Performance_Score"]].to_dict(orient="records")

class EmployeeApp:
    def __init__(self,root):
        self.root = root
        self.root.title("Employee Performance Management System")
        self.manager=EmployeeManager()

        tk.Label(root,text="Employee Id").grid(column=0,row=0,padx=5,pady=4)
        self.Id_entry = tk.Entry(root)
        self.Id_entry.grid(row=0,column=1)  

        tk.Label(root,text="Employee Name").grid(column=0,row=1,padx=5,pady=4)
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=1,column=1)  

        tk.Label(root,text="Employee Pay").grid(column=0,row=2,padx=5,pady=4)
        self.Pay_entry = tk.Entry(root)
        self.Pay_entry.grid(row=2,column=1)  

        tk.Label(root,text="No. of Reports Viewed: ").grid(column=2,row=0,padx=5,pady=4)
        self.Reports_entry = tk.Entry(root)
        self.Reports_entry.grid(row=0,column=3)  

        tk.Label(root,text="Customer Satisfaction Rate").grid(column=2,row=1,padx=5,pady=4)
        self.CSRate_entry = tk.Entry(root)
        self.CSRate_entry.grid(row=1,column=3,padx=10,pady=5)  

        self.Text_box = tk.Text(root,height=20,width=100)
        self.Text_box.grid(column=0,row=3,columnspan=4, padx=10, pady=10)

 
        tk.Button(root, text="Add Employee", command=self.add_employee).grid(row=4, column=0, pady=10)
        tk.Button(root, text="Show Data", command=self.show_data).grid(row=4, column=1)
        tk.Button(root, text="Analyze", command=self.show_analysis).grid(row=4, column=2, pady=10)
        tk.Button(root, text="Plot Chart", command=self.plot_chart).grid(row=4, column=3)
        tk.Button(root, text="Save CSV", command=self.save_csv).grid(row=5, column=0, pady=10)
        tk.Button(root, text="Load CSV", command=self.load_csv).grid(row=5, column=1)

    def add_employee(self):
      try:
        E_Id= int(self.Id_entry.get())
        Name = self.name_entry.get()
        Pay = int(self.Pay_entry.get())
        Report= int(self.Reports_entry.get())
        CSRate = int(self.CSRate_entry.get())
        
        self.manager.add_employee(E_Id,Name,Pay,Report,CSRate)
        messagebox.showinfo("Employee report is successfully added in database.")
        self.Id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.Pay_entry.delete(0, tk.END)
        self.CSRate_entry.delete(0,tk.END)
        self.Reports_entry.delete(0,tk.END)

      except ValueError:
        messagebox.showerror("Error, Value error id, pay,report,csrate should be numerical.")

    def show_data(self):
         self.Text_box.delete(1.0, tk.END)
         if not self.manager.data.empty:
            self.Text_box.insert(tk.END, str(self.manager.data))
         else:
            self.Text_box.insert(tk.END, "No data available.")

    def show_analysis(self):
        results = self.manager.analysis()
        self.Text_box.delete(1.0, tk.END)
        self.Text_box.insert(tk.END, json.dumps(results, indent=4))

    def plot_chart(self):
     if self.manager.data.empty:
        messagebox.showwarning("Warning", "No data to plot!")
        return
    
     fig = Figure(figsize=(5, 4), dpi=100)
     ax = fig.add_subplot(111)

     ax.scatter(
        self.manager.data["Report_Viewed"], 
        self.manager.data["Customer_Satisfaction"]
     )

     ax.set_xlabel("Reports Viewed")
     ax.set_ylabel("Customer Satisfaction")
     ax.set_title("Employee Performance - Reports vs Satisfaction")

    # Create popup window for chart
     chart_window = tk.Toplevel(self.root)
     chart_window.title("Employee Performance")
    
     canvas = FigureCanvasTkAgg(fig, master=chart_window)
     canvas.draw()
     canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

         
    def save_csv(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv")
        if filename:
            self.manager.save_csv(filename)
            messagebox.showinfo("Saved", f"Data saved to {filename}")
    def load_csv(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if filename:
            self.manager.load_csv(filename)
            messagebox.showinfo("Loaded", f"Data loaded from {filename}")


if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeApp(root)
    root.mainloop()