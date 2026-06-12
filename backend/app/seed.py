from .extensions import db
from .models import Appeal, Grade, Student


def seed_demo_data():
    if Student.query.first():
        return

    students = [
        Student(student_no="20240101", name="张明", major="计算机科学与技术", class_name="计科2401"),
        Student(student_no="20240102", name="李华", major="计算机科学与技术", class_name="计科2401"),
        Student(student_no="20240103", name="王芳", major="计算机科学与技术", class_name="计科2401"),
        Student(student_no="20240104", name="赵强", major="计算机科学与技术", class_name="计科2401"),
        Student(student_no="20240105", name="陈静", major="计算机科学与技术", class_name="计科2401"),
        Student(student_no="20240106", name="刘伟", major="计算机科学与技术", class_name="计科2401"),
        Student(student_no="20240107", name="孙丽", major="计算机科学与技术", class_name="计科2401"),
        Student(student_no="20240108", name="周杰", major="计算机科学与技术", class_name="计科2401"),
        Student(student_no="20240109", name="吴敏", major="计算机科学与技术", class_name="计科2401"),
        Student(student_no="20240110", name="郑航", major="计算机科学与技术", class_name="计科2401"),

        Student(student_no="20240201", name="李雨", major="软件工程", class_name="软工2402"),
        Student(student_no="20240202", name="钱磊", major="软件工程", class_name="软工2402"),
        Student(student_no="20240203", name="孙悦", major="软件工程", class_name="软工2402"),
        Student(student_no="20240204", name="马涛", major="软件工程", class_name="软工2402"),
        Student(student_no="20240205", name="朱琳", major="软件工程", class_name="软工2402"),
        Student(student_no="20240206", name="胡军", major="软件工程", class_name="软工2402"),
        Student(student_no="20240207", name="林芳", major="软件工程", class_name="软工2402"),
        Student(student_no="20240208", name="何鑫", major="软件工程", class_name="软工2402"),

        Student(student_no="20240301", name="王佳", major="数据科学", class_name="数科2401"),
        Student(student_no="20240302", name="冯硕", major="数据科学", class_name="数科2401"),
        Student(student_no="20240303", name="丁宁", major="数据科学", class_name="数科2401"),
        Student(student_no="20240304", name="沈悦", major="数据科学", class_name="数科2401"),
        Student(student_no="20240305", name="韩冰", major="数据科学", class_name="数科2401"),
        Student(student_no="20240306", name="罗佳", major="数据科学", class_name="数科2401"),
        Student(student_no="20240307", name="唐凯", major="数据科学", class_name="数科2401"),
        Student(student_no="20240308", name="许阳", major="数据科学", class_name="数科2401"),

        Student(student_no="20240401", name="黄明", major="软件工程", class_name="软工2401"),
        Student(student_no="20240402", name="崔莹", major="软件工程", class_name="软工2401"),
        Student(student_no="20240403", name="邓辉", major="软件工程", class_name="软工2401"),
        Student(student_no="20240404", name="彭雪", major="软件工程", class_name="软工2401"),
        Student(student_no="20240405", name="曾磊", major="软件工程", class_name="软工2401"),
        Student(student_no="20240406", name="肖娜", major="软件工程", class_name="软工2401"),
        Student(student_no="20240407", name="曹阳", major="软件工程", class_name="软工2401"),
        Student(student_no="20240408", name="苏琪", major="软件工程", class_name="软工2401"),
    ]
    db.session.add_all(students)
    db.session.flush()

    def grades_for(course_code, course_name, credit, semester, teacher, students_scores):
        return [
            Grade(student=stu, course_code=course_code, course_name=course_name,
                  credit=credit, score=score, semester=semester, teacher=teacher)
            for stu, score in students_scores
        ]

    s_2401 = students[0:10]
    s_2402 = students[10:18]
    s_2401_ds = students[18:26]
    s_2401_se = students[26:34]

    all_grades = []

    all_grades += grades_for("CS101", "程序设计基础", 4, "2025-2026-1", "陈老师", [
        (s_2401[0], 92), (s_2401[1], 85), (s_2401[2], 78), (s_2401[3], 68), (s_2401[4], 95),
        (s_2401[5], 55), (s_2401[6], 82), (s_2401[7], 73), (s_2401[8], 64), (s_2401[9], 88),
    ])

    all_grades += grades_for("MA101", "高等数学", 5, "2025-2026-1", "周老师", [
        (s_2401[0], 86), (s_2401[1], 72), (s_2401[2], 90), (s_2401[3], 58), (s_2401[4], 81),
        (s_2401[5], 48), (s_2401[6], 93), (s_2401[7], 67), (s_2401[8], 76), (s_2401[9], 83),
    ])

    all_grades += grades_for("SE201", "软件工程导论", 3, "2025-2026-1", "刘老师", [
        (s_2402[0], 78), (s_2402[1], 65), (s_2402[2], 85), (s_2402[3], 92), (s_2402[4], 71),
        (s_2402[5], 52), (s_2402[6], 88), (s_2402[7], 69),
        (s_2401_se[0], 82), (s_2401_se[1], 74), (s_2401_se[2], 95), (s_2401_se[3], 61),
        (s_2401_se[4], 77), (s_2401_se[5], 56), (s_2401_se[6], 89), (s_2401_se[7], 83),
    ])

    all_grades += grades_for("DS101", "数据分析基础", 3, "2025-2026-1", "赵老师", [
        (s_2401_ds[0], 88), (s_2401_ds[1], 94), (s_2401_ds[2], 76), (s_2401_ds[3], 62),
        (s_2401_ds[4], 81), (s_2401_ds[5], 53), (s_2401_ds[6], 70), (s_2401_ds[7], 91),
    ])

    all_grades += grades_for("CS102", "数据结构", 4, "2025-2026-2", "陈老师", [
        (s_2401[0], 83), (s_2401[1], 91), (s_2401[2], 75), (s_2401[3], 66),
        (s_2401[4], 97), (s_2401[5], 54), (s_2401[6], 80), (s_2401[7], 71),
        (s_2401[8], 63), (s_2401[9], 87),
        (s_2402[0], 79), (s_2402[1], 85), (s_2402[2], 92), (s_2402[3], 68),
        (s_2402[4], 74), (s_2402[5], 59), (s_2402[6], 88), (s_2402[7], 76),
    ])

    all_grades += grades_for("CS201", "操作系统", 4, "2025-2026-2", "吴老师", [
        (s_2401[0], 85), (s_2401[1], 72), (s_2401[2], 90), (s_2401[3], 61),
        (s_2401[4], 94), (s_2401[5], 47), (s_2401[6], 78), (s_2401[7], 69),
        (s_2401[8], 56), (s_2401[9], 82),
    ])

    all_grades += grades_for("SE301", "软件测试", 3, "2025-2026-2", "郑老师", [
        (s_2402[0], 81), (s_2402[1], 74), (s_2402[2], 89), (s_2402[3], 95),
        (s_2402[4], 67), (s_2402[5], 53), (s_2402[6], 84), (s_2402[7], 77),
        (s_2401_se[0], 76), (s_2401_se[1], 91), (s_2401_se[2], 83), (s_2401_se[3], 64),
        (s_2401_se[4], 70), (s_2401_se[5], 58), (s_2401_se[6], 96), (s_2401_se[7], 87),
    ])

    db.session.add_all(all_grades)
    db.session.flush()

    db.session.add(
        Appeal(
            grade=all_grades[15],
            student_no=students[5].student_no,
            reason="期末大题第三题步骤分可能漏算，申请复核。",
            status="pending",
        )
    )
    db.session.commit()
