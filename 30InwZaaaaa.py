print("คำนวนคะแนนรวม 3 วิชา และประเมินระดับคะแนน")
point1 = float(input("คะแนนวิชาที่ 1"))
point2 = float(input("คะแนนวิชาที่ 2"))
point3 = float(input("คะแนนวิชาที่ 3"))
total = (point1 + point2 + point3)
average = total/3
print("คะแนนรวมของคุณในครั้งนี้ \nคือ ", total, " คะแนน")
print("คะแนนเฉลี่ยของคุณในครั้งนี้ \nคือ ", average, " คะแนน")



if total < 60 : 
    total = float(input("คะแนนรวมของคุณ คือ:"))
    average = float(input("คะแนนเฉลี่ยของคุณ คือ:"))
    print("ควรปรับปรุง)") 
elif total < 80 :
    print("ดีเยี่ยม")
else:
    print("ดีเยี่ยม")