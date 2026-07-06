print("โปรแกรมคำนวนแม่สูตรคูณ")
num1 = int(input("ตัวเลขเริ่มต้น: "))
num2 = int(input("ตัวเลขสุดท้าย: "))

for m  in range(num1, num2 + 1):
   print(f"\n[สูตรคูณแม่ {m}]")
   for i in range(1,13):
      print(m,"x",i,"=",m*i)