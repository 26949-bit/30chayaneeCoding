print("โปรแกรมคำนวน bmi")
wieght = (float(input("น้ำหนักของคุณ: ")))
higth = (float(input("ส่วนสูงของคุณ: ")))
total =  higth * higth
bmi = wieght/total
print("ค่า bmi ของคุณคือ" ,bmi)

if bmi <18.5 :
    print("น้ำหนักน้อย")

elif bmi >18.6 - 22.9 :
    print("ปกติ")

elif bmi >23 - 24.9 :
    print("น้ำหนักเกิน")
    
else :
    print("อ้วน")

