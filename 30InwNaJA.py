print("โปรแกรมคำนวนคะแนนรวม \n")
Art = int(input("คะแนนวิชาศิลปะ: "))
History = int(input("คะแนนวิชาประวัติศาสตร์: "))
Math = int(input("คะแนนวิชาคณิตศาสตร์: "))
total = (Art + History + Math)
average = total/3
print("คะแนนรวมของคุณในครั้งนี้ \nคือ ", total, " คะแนน")
print("คะแนนเฉลี่ยของคุณในครั้งนี้ \nคือ ", average, " คะแนน")

if total < 60 : 
    total = int(input("คะแนนรวมของคุณ คือ:"))
    average = int(input("คะแนนเฉลี่ยของคุณ คือ:"))
    print("ควรปรับปรุง)") 
elif total > 80 :
    print("ดีเยี่ยม")
else:
    print("ดีเยี่ยม")

