import sqlite3
import tkinter as tk
from datetime import datetime, timedelta
from tkinter import messagebox, ttk

# --- 1. ระบบจัดการฐานข้อมูล SQLite (Database) ---
def init_db():
    conn = sqlite3.connect("dueday.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            due_date TEXT NOT NULL,
            est_hours INTEGER NOT NULL,
            status TEXT DEFAULT 'Pending'
        )
    ''')
    conn.commit()
    conn.close()

# --- 2. ส่วนของหน้าต่างโปรแกรมหลัก (GUI) ---
class DueDayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DueDay - โปรแกรมจัดตารางงานและแจ้งเตือนเดดไลน์")
        self.root.geometry("750x600")
        
        init_db()
        self.show_login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # --- หน้า Login ---
    def show_login_screen(self):
        self.clear_screen()
        frame = ttk.Frame(self.root, padding="30")
        frame.pack(expand=True)

        ttk.Label(frame, text="DueDay Login", font=("Helvetica", 18, "bold")).grid(row=0, column=0, columnspan=2, pady=15)
        
        ttk.Label(frame, text="ชื่อผู้ใช้:").grid(row=1, column=0, sticky="e", pady=5)
        self.username_entry = ttk.Entry(frame)
        self.username_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(frame, text="รหัสผ่าน:").grid(row=2, column=0, sticky="e", pady=5)
        self.password_entry = ttk.Entry(frame, show="*")
        self.password_entry.grid(row=2, column=1, pady=5)
        
        ttk.Button(frame, text="เข้าสู่ระบบ", command=self.login).grid(row=3, column=0, columnspan=2, pady=15)

    def login(self):
        user = self.username_entry.get()
        pwd = self.password_entry.get()
        if user == "student" and pwd == "1234":
            self.show_main_screen()
        else:
            messagebox.showerror("ผิดพลาด", "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง (ลองใช้: student / 1234)")

    # --- หน้าหลักแสดงผลและเพิ่มงาน ---
    def show_main_screen(self):
        self.clear_screen()
        
        # Header
        header = ttk.Frame(self.root, padding="10")
        header.pack(fill="x")
        ttk.Label(header, text="📌 ตารางงานและการบ้านที่ต้องส่ง", font=("Helvetica", 14, "bold")).pack(side="left")
        ttk.Button(header, text="ออกจากระบบ", command=self.show_login_screen).pack(side="right")

        # Form กรอกข้อมูล
        form = ttk.LabelFrame(self.root, text=" เพิ่มการบ้านใหม่ ", padding="10")
        form.pack(fill="x", padx=10, pady=5)

        ttk.Label(form, text="ชื่องาน:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = ttk.Entry(form, width=18)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form, text="วันส่ง (YYYY-MM-DD):").grid(row=0, column=2, padx=5, pady=5)
        self.due_entry = ttk.Entry(form, width=12)
        self.due_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form, text="เวลาที่ใช้ (ชม.):").grid(row=0, column=4, padx=5, pady=5)
        self.hours_entry = ttk.Entry(form, width=5)
        self.hours_entry.grid(row=0, column=5, padx=5, pady=5)

        ttk.Button(form, text="+ เพิ่มงาน", command=self.add_task).grid(row=0, column=6, padx=10, pady=5)

        # ตารางแสดงรายการงาน
        table_frame = ttk.Frame(self.root, padding="10")
        table_frame.pack(fill="both", expand=True)

        columns = ("id", "name", "due", "start_by", "status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="ชื่องาน")
        self.tree.heading("due", text="วันส่ง (Deadline)")
        self.tree.heading("start_by", text="ควรเริ่มทำอย่างน้อย")
        self.tree.heading("status", text="สถานะ / ความด่วน")

        self.tree.column("id", width=30, anchor="center")
        self.tree.column("name", width=180)
        self.tree.column("due", width=110, anchor="center")
        self.tree.column("start_by", width=140, anchor="center")
        self.tree.column("status", width=180)
        
        self.tree.pack(fill="both", expand=True)

        # ตั้งค่าสีแบ่งระดับความด่วน
        self.tree.tag_configure("urgent", background="#FFCCCC") # สีแดง: งานด่วนมาก/เลยกำหนด
        self.tree.tag_configure("warning", background="#FFF2CC") # สีเหลือง: อีก 1-2 วัน
        self.tree.tag_configure("normal", background="#E2EFDA")  # สีเขียว: มีเวลาทำสบายๆ

        # ปุ่มจัดการสถานะ
        btn_frame = ttk.Frame(self.root, padding="10")
        btn_frame.pack(fill="x")
        ttk.Button(btn_frame, text="✅ ทำเสร็จแล้ว (ลบงาน)", command=self.delete_task).pack(side="left", padx=5)

        self.load_tasks()

    # --- ฟังก์ชันจัดการข้อมูล (CRUD) ---
    def add_task(self):
        name = self.name_entry.get()
        due_str = self.due_entry.get()
        hours = self.hours_entry.get()

        if not name or not due_str or not hours:
            messagebox.showwarning("เตือน", "กรุณากรอกข้อมูลให้ครบทุกช่อง")
            return

        try:
            datetime.strptime(due_str, "%Y-%m-%d")
            est_hours = int(hours)

            conn = sqlite3.connect("dueday.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tasks (name, due_date, est_hours) VALUES (?, ?, ?)", 
                           (name, due_str, est_hours))
            conn.commit()
            conn.close()

            self.name_entry.delete(0, tk.END)
            self.due_entry.delete(0, tk.END)
            self.hours_entry.delete(0, tk.END)
            self.load_tasks()

        except ValueError:
            messagebox.showerror("ผิดพลาด", "รูปแบบวันที่ต้องเป็น YYYY-MM-DD และเวลาที่ใช้ต้องเป็นตัวเลข")

    def load_tasks(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = sqlite3.connect("dueday.db")
        cursor = conn.cursor()
        # ดึงข้อมูลและจัดเรียงตามวันส่งให้อัตโนมัติ (Auto-Sorting)
        cursor.execute("SELECT id, name, due_date, est_hours FROM tasks WHERE status='Pending' ORDER BY due_date ASC")
        rows = cursor.fetchall()
        conn.close()

        today = datetime.now().date()

        for task in rows:
            task_id, name, due_str, hours = task
            due_date = datetime.strptime(due_str, "%Y-%m-%d").date()
            days_left = (due_date - today).days

            # คำนวณวันเริ่มทำล่วงหน้า
            start_date = due_date - timedelta(days=max(1, hours // 3))
            start_by_str = start_date.strftime("%d/%m/%Y")

            # วิเคราะห์สถานะและเลือกแท็กสี
            if days_left < 0:
                status = "❌ เลยกำหนดส่งแล้ว!"
                tag = "urgent"
            elif days_left == 0:
                status = "🔥 ต้องส่งวันนี้!"
                tag = "urgent"
            elif days_left <= 2:
                status = f"⚠️ เหลือ {days_left} วัน (รีบทำ!)"
                tag = "warning"
            else:
                status = f"🟢 เหลือ {days_left} วัน"
                tag = "normal"

            self.tree.insert("", tk.END, values=(task_id, name, due_str, start_by_str, status), tags=(tag,))

    def delete_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("แจ้งเตือน", "กรุณาคลิกเลือกรายการงานที่ทำเสร็จแล้วก่อนครับ")
            return

        item = self.tree.item(selected[0])
        task_id = item['values'][0]

        conn = sqlite3.connect("dueday.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
        conn.close()

        self.load_tasks()
        messagebox.showinfo("สำเร็จ", "เก่งมาก! ทำงานเสร็จไปอีกหนึ่งงานแล้ว 🎉")

if __name__ == "__main__":
    root = tk.Tk()
    app = DueDayApp(root)
    root.mainloop()