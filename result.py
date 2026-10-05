student_name = input("Enter you name: ").strip()
try:
    marks = float(input(f"hello {student_name}, enter you marks in percentage: "))
    attendance = float(input("enter your attendance in percentage: "))

    if marks < 0 or marks > 100 and attendance < 0 or attendance > 100:
        print("please enter the marks and attendance between 0 to 100.")
    else:
        if marks >= 80:
            grade = "A+"
        elif marks >= 60:
            grade = "A"
        elif marks >= 40:
            grade = "B"
        else:
            grade = "C"

        if marks >= 85 and attendance >= 75:
            scholarship = "congratulations🙌, you got scholarship"
        else:
            scholarship = "you didn't got scholarship"

        print("student name: ", student_name.upper())
        print("grades: ", grade)
        print("scholarship: ", scholarship)
except ValueError:
    print("please enter numbers instead of words!")



def nameage(name, age):
    print(f"name: {name}, age: {age}")
a = input("enter you name: ").lower()
b = int(input("enter your age: "))
nameage(a, b)
