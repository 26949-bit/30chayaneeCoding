import sqlite3
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk


# --- 1. ระบบจัดการฐานข้อมูล SQLite (Database) ---
def init_db():
  conn = sqlite3.connect("dueday.db")
  cursor = conn.cursor()

  cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            due_date TEXT NOT NULL,
            est_hours INTEGER DEFAULT 0,
            est_minutes INTEGER DEFAULT 0,
            created_at TEXT,
            completed_at TEXT,
            status TEXT DEFAULT 'Pending'
        )
    """)

  # ตรวจสอบและอัปเดตคอลัมน์เดิมหากเคยสร้างตารางไว้แล้ว
  cursor.execute("PRAGMA table_info(tasks)")
  columns = [column[1] for column in cursor.fetchall()]

  if "est_minutes" not in columns:
    cursor.execute(
        "ALTER TABLE tasks ADD COLUMN est_minutes INTEGER DEFAULT 0"
    )
  if "created_at" not in columns:
    cursor.execute("ALTER TABLE tasks ADD COLUMN created_at TEXT")
  if "completed_at" not in columns:
    cursor.execute("ALTER TABLE tasks ADD COLUMN completed_at TEXT")

  conn.commit()
  conn.close()


# --- 2. ส่วนของหน้าต่างโปรแกรมหลัก (GUI) ---
class DueDayApp:

  def __init__(self, root):
    self.root = root
    self.root.title("DueDay - โปรแกรมจัดตารางงานและแจ้งเตือนเดดไลน์")
    self.root.geometry("850x650")

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

    ttk.Label(
        frame, text="DueDay Login", font=("Helvetica", 18, "bold")
    ).grid(row=0, column=0, columnspan=2, pady=15)

    ttk.Label(frame, text="ชื่อผู้ใช้:").grid(row=1, column=0, sticky="e", pady=5)
    self.username_entry = ttk.Entry(frame)
    self.username_entry.grid(row=1, column=1, pady=5)

    ttk.Label(frame, text="รหัสผ่าน:").grid(
        row=2, column=0, sticky="e", pady=5
    )
    self.password_entry = ttk.Entry(frame, show="*")
    self.password_entry.grid(row=2, column=1, pady=5)

    ttk.Button(frame, text="เข้าสู่ระบบ", command=self.login).grid(
        row=3, column=0, columnspan=2, pady=15
    )

  def login(self):
    user = self.username_entry.get()
    pwd = self.password_entry.get()
    if user == "student" and pwd == "1234":
      self.show_main_screen()
    else:
      messagebox.showerror(
          "ผิดพลาด",
          "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง (ลองใช้: student / 1234)",
      )

  # --- หน้าหลักแสดงผลและเพิ่มงาน ---
  def show_main_screen(self):
    self.clear_screen()

    # Header
    header = ttk.Frame(self.root, padding="10")
    header.pack(fill="x")
    ttk.Label(
        header,
        text="📌 ตารางงานและการบ้านที่ต้องส่ง",
        font=("Helvetica", 14, "bold"),
    ).pack(side="left")
    ttk.Button(
        header, text="ออกจากระบบ", command=self.show_login_screen
    ).pack(side="right")

    # Form กรอกข้อมูล
    form = ttk.LabelFrame(
        self.root, text=" เพิ่มการบ้านใหม่ (กรุณาใช้ปี ค.ศ.) ", padding="10"
    )
    form.pack(fill="x", padx=10, pady=5)

    # แถวที่ 1: ชื่องาน & วันส่ง
    ttk.Label(form, text="ชื่องาน:").grid(
        row=0, column=0, padx=5, pady=5, sticky="e"
    )
    self.name_entry = ttk.Entry(form, width=18)
    self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    ttk.Label(
        form, text="วันส่ง (ค.ศ. เช่น 2026-09-30):", font=("Helvetica", 9, "bold")
    ).grid(row=0, column=2, padx=5, pady=5, sticky="e")
    self.due_entry = ttk.Entry(form, width=12)
    self.due_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w")

    # แถวที่ 2: เวลาที่ใช้ทำ (ชั่วโมง / นาที)
    ttk.Label(form, text="เวลาที่ใช้ทำ:").grid(
        row=1, column=0, padx=5, pady=5, sticky="e"
    )

    time_frame = ttk.Frame(form)
    time_frame.grid(row=1, column=1, columnspan=3, sticky="w")

    self.hours_entry = ttk.Entry(time_frame, width=5)
    self.hours_entry.pack(side="left", padx=(5, 2))
    ttk.Label(time_frame, text="ชม.").pack(side="left", padx=(0, 10))

    self.mins_entry = ttk.Entry(time_frame, width=5)
    self.mins_entry.pack(side="left", padx=(5, 2))
    ttk.Label(time_frame, text="นาที").pack(side="left", padx=(0, 15))

    ttk.Button(time_frame, text="+ เพิ่มงาน", command=self.add_task).pack(
        side="left", padx=10
    )

    # ตารางแสดงรายการงาน
    table_frame = ttk.Frame(self.root, padding="10")
    table_frame.pack(fill="both", expand=True)

    columns = ("id", "name", "due", "est_time", "created_at", "status")
    self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

    self.tree.heading("id", text="ID")
    self.tree.heading("name", text="ชื่องาน")
    self.tree.heading("due", text="วันส่ง (ค.ศ.)")
    self.tree.heading("est_time", text="เวลาที่ใช้ทำ")
    self.tree.heading("created_at", text="เวลาที่ลงข้อมูล")
    self.tree.heading("status", text="สถานะ / ความด่วน")

    self.tree.column("id", width=30, anchor="center")
    self.tree.column("name", width=160)
    self.tree.column("due", width=100, anchor="center")
    self.tree.column("est_time", width=100, anchor="center")
    self.tree.column("created_at", width=140, anchor="center")
    self.tree.column("status", width=180)

    self.tree.pack(fill="both", expand=True)

    # สีแสดงความด่วน
    self.tree.tag_configure("urgent", background="#FFCCCC")  # สีแดง
    self.tree.tag_configure("warning", background="#FFF2CC")  # สีเหลือง
    self.tree.tag_configure("normal", background="#E2EFDA")  # สีเขียว

    # ปุ่มจัดการงาน
    btn_frame = ttk.Frame(self.root, padding="10")
    btn_frame.pack(fill="x")
    ttk.Button(
        btn_frame, text="✅ ทำเสร็จแล้ว (ลบงาน)", command=self.delete_task
    ).pack(side="left", padx=5)

    self.load_tasks()

  # --- ฟังก์ชันจัดการข้อมูล (CRUD) ---
  def add_task(self):
    name = self.name_entry.get().strip()
    due_str = self.due_entry.get().strip()
    hours_str = self.hours_entry.get().strip()
    mins_str = self.mins_entry.get().strip()

    if not name or not due_str:
      messagebox.showwarning("เตือน", "กรุณากรอกชื่องานและวันกำหนดส่ง")
      return

    # ตรวจสอบรูปแบบวันที่ (YYYY-MM-DD)
    try:
      datetime.strptime(due_str, "%Y-%m-%d")
    except ValueError:
      messagebox.showerror(
          "ผิดพลาด",
          "รูปแบบวันที่ไม่ถูกต้อง! กรุณาพิมพ์เป็น ค.ศ. เช่น 2026-09-30",
      )
      return

    # จัดการกรณีผู้ใช้กรอกชั่วโมง/นาทีอย่างใดอย่างหนึ่ง หรือทั้งคู่
    try:
      hours = int(hours_str) if hours_str else 0
      mins = int(mins_str) if mins_str else 0

      if hours == 0 and mins == 0:
        messagebox.showwarning(
            "เตือน", "กรุณาใส่เวลาที่คาดว่าจะใช้ทำ (ชั่วโมง หรือ นาที)"
        )
        return
    except ValueError:
      messagebox.showerror(
          "ผิดพลาด", "จำนวนชั่วโมงและนาทีต้องเป็นตัวเลขเท่านั้น"
      )
      return

    # เวลาปัจจุบันขณะกดลงข้อมูล
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    conn = sqlite3.connect("dueday.db")
    cursor = conn.cursor()
    cursor.execute(
        """
            INSERT INTO tasks (name, due_date, est_hours, est_minutes, created_at) 
            VALUES (?, ?, ?, ?, ?)
        """,
        (name, due_str, hours, mins, created_at),
    )
    conn.commit()
    conn.close()

    # เคลียร์ฟอร์ม
    self.name_entry.delete(0, tk.END)
    self.due_entry.delete(0, tk.END)
    self.hours_entry.delete(0, tk.END)
    self.mins_entry.delete(0, tk.END)

    self.load_tasks()

  def load_tasks(self):
    for row in self.tree.get_children():
      self.tree.delete(row)

    conn = sqlite3.connect("dueday.db")
    cursor = conn.cursor()
    cursor.execute("""
            SELECT id, name, due_date, est_hours, est_minutes, created_at 
            FROM tasks 
            WHERE status='Pending' 
            ORDER BY due_date ASC
        """)
    rows = cursor.fetchall()
    conn.close()

    today = datetime.now().date()

    for task in rows:
      task_id, name, due_str, hours, mins, created_at = task
      due_date = datetime.strptime(due_str, "%Y-%m-%d").date()
      days_left = (due_date - today).days

      # จัดรูปแบบการแสดงผลเวลา
      time_parts = []
      if hours > 0:
        time_parts.append(f"{hours} ชม.")
      if mins > 0:
        time_parts.append(f"{mins} นาที")
      est_time_display = " ".join(time_parts)

      # วิเคราะห์ระดับความด่วน
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

      created_display = created_at if created_at else "-"

      self.tree.insert(
          "",
          tk.END,
          values=(
              task_id,
              name,
              due_str,
              est_time_display,
              created_display,
              status,
          ),
          tags=(tag,),
      )

  def delete_task(self):
    selected = self.tree.selection()
    if not selected:
      messagebox.showwarning(
          "แจ้งเตือน", "กรุณาคลิกเลือกรายการงานที่ทำเสร็จแล้วก่อนครับ"
      )
      return

    item = self.tree.item(selected[0])
    task_id = item["values"][0]

    # บันทึกเวลาที่กดทำเสร็จแล้ว
    completed_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    conn = sqlite3.connect("dueday.db")
    cursor = conn.cursor()
    cursor.execute(
        """
            UPDATE tasks 
            SET status='Completed', completed_at=? 
            WHERE id=?
        """,
        (completed_at, task_id),
    )
    conn.commit()
    conn.close()

    self.load_tasks()
    messagebox.showinfo(
        "สำเร็จ",
        f"เก่งมาก! ทำงานเสร็จเมื่อ {completed_at}\nลบรายการงานเรียบร้อยแล้ว 🎉",
    )


if __name__ == "__main__":
  root = tk.Tk()
  app = DueDayApp(root)
  root.mainloop()