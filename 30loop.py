import random
secret_number = random.randint(1, 100)
count = 0
guess = 0

print("มาเล่นเกมทายตัวเลข 1-100 กันค่าาา")

while guess != secret_number:
    guess = int(input("ลองทายตัวเลขมาก่อน: "))
    count += 1

    if guess > secret_number:
     print("มากไปลองใหม่นะ")
    elif guess < secret_number:
     print("น้อยไปจ้าา")
    else:
     print(f"ถูกต้องแล้วค่า เลขที่ถูกต้องคือ {secret_number}")
     print(f"คุณใช้จำนวนทายไปทั้งหมด: {count} ครั้ง")

