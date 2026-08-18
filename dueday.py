import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

class HomeworkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DueDay - โปรแกรมจัดตารางงานและแจ้งเตือน")
        self.root.geometry("600x500")
        
        # คลังเก็บข้อมูลการบ้าน (Database จำลอง)
        self.tasks = []
        
        # เริ่มต้นด้วยหน้า Login
        self.show_login_screen()

    def show_login_screen(self):
        self.clear_screen()
        
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True)

        ttk.Label(frame, text="เข้าสู่ระบบ DueDay", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(frame, text="ชื่อผู้ใช้:").grid(row=1, column=0, sticky="e", pady=5)
        self.username_entry = ttk.Entry(frame)
        self.username_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(frame, text="รหัสผ่าน:").grid(row=2, column=0, sticky="e", pady=5)
        self.password_entry = ttk.Entry(frame, show="*")
        self.password_entry.grid(row=2, column=1, pady=5)
        
        login_btn = ttk.Button(frame, text="เข้าสู่ระบบ", command=self.login)
        login_btn.grid(row=3, column=0, columnspan=2, pady=15)

    def login(self):
        user = self.username_entry.get()
        pwd = self.password_entry.get()
        
        # กำหนด Username/Password เบื้องต้นสำหรับทดสอบ
        if user == "student" and pwd == "1234":
            self.show_main_screen()
        else:
            messagebox.showerror("ผิดพลาด", "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง (ลองใช้: student / 1234)")

    def show_main_screen(self):
        self.clear_screen()
        
        # ส่วนหัว
        header = ttk.Frame(self.root, padding="10")
        header.pack(fill="x")
        ttk.Label(header, text="ตารางงานและการบ้านที่ต้องส่ง", font=("Helvetica", 14, "bold")).pack(side="left")
        ttk.Button(header, text="ออกจากระบบ", command=self.show_login_screen).pack(side="right")

        # ฟอร์มเพิ่มการบ้าน
        form_frame = ttk.LabelFrame(self.root, text=" เพิ่มการบ้านใหม่ ", padding="10")
        form_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(form_frame, text="ชื่องาน:").grid(row=0, column=0, padx=5, pady=5)
        self.task_name_entry = ttk.Entry(form_frame, width=20)
        self.task_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="วันส่ง (YYYY-MM-DD):").grid(row=0, column=2, padx=5, pady=5)
        self.due_date_entry = ttk.Entry(form_frame, width=12)
        self.due_date_entry.grid(row=0, column=3, padx=5, pady=5)
        
        add_btn = ttk.Button(form_frame, text="+ เพิ่มงาน", command=self.add_task)
        add_btn.grid(row=0, column=4, padx=10, pady=5)

        # ตารางแสดงรายการงาน (จัดลำดับตามวันส่ง)
        table_frame = ttk.Frame(self.root, padding="10")
        table_frame.pack(fill="both", expand=True)

        columns = ("task", "due_date", "status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tree.heading("task", text="ชื่องาน/วิชา")
        self.tree.heading("due_date", text="วันกำหนดส่ง (Deadline)")
        self.tree.heading("status", text="สถานะการจัดตาราง")
        
        self.tree.column("task", width=200)
        self.tree.column("due_date", width=150)
        self.tree.column("status", width=150)
        self.tree.pack(fill="both", expand=True)

    def add_task(self):
        name = self.task_name_entry.get()
        due_str = self.due_date_entry.get()

        if not name or not due_str:
            messagebox.showwarning("แจ้งเตือน", "กรุณากรอกข้อมูลให้ครบถ้วน")
            return

        try:
            # ตรวจสอบรูปแบบวันที่
            due_date = datetime.strptime(due_str, "%Y-%m-%d").date()
            today = datetime.now().date()
            
            days_left = (due_date - today).days
            
            if days_left < 0:
                status = "เลยกำหนดส่งแล้ว!"
            elif days_left == 0:
                status = "🔥 ต้องส่งวันนี้!"
            elif days_left <= 2:
                status = "⚠️ งานเร่งด่วน (ทำทันที)"
            else:
                status = f"เหลือเวลา {days_left} วัน"

            # บันทึกและจัดเรียงตามวันส่งให้อัตโนมัติ
            self.tasks.append({"name": name, "due": due_date, "status": status})
            self.tasks.sort(key=lambda x: x["due"]) 
            
            self.update_task_table()
            self.task_name_entry.delete(0, tk.END)
            self.due_date_entry.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("ผิดพลาด", "กรุณากรอกวันที่ในรูปแบบ YYYY-MM-DD เช่น 2026-08-25")

    def update_task_table(self):
        # ล้างข้อมูลเก่าในตาราง
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # แสดงข้อมูลที่จัดเรียงใหม่
        for task in self.tasks:
            self.tree.insert("", tk.END, values=(task["name"], task["due"].strftime("%d/%m/%Y"), task["status"]))

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = HomeworkApp(root)
    root.mainloop()