from ..extensions import db
from ..models import Grade, Student
from .gpa import calculate_summary


def list_grades():
    return Grade.query.order_by(Grade.updated_at.desc()).all()


def get_or_create_student(student_no, name, major="", class_name=""):
    student = Student.query.filter_by(student_no=student_no).first()
    if student:
        student.name = name or student.name
        student.major = major if major is not None else student.major
        student.class_name = class_name if class_name is not None else student.class_name
        return student

    student = Student(
        student_no=student_no,
        name=name,
        major=major or "",
        class_name=class_name or "",
    )
    db.session.add(student)
    return student


def create_grade(payload):
    student = get_or_create_student(
        payload["studentNo"],
        payload["studentName"],
        payload.get("major", ""),
        payload.get("className", ""),
    )
    grade = Grade(
        student=student,
        course_code=payload["courseCode"],
        course_name=payload["courseName"],
        credit=float(payload["credit"]),
        score=float(payload["score"]),
        semester=payload["semester"],
        teacher=payload["teacher"],
    )
    db.session.add(grade)
    db.session.commit()
    return grade


def update_grade(grade, payload):
    if "courseCode" in payload:
        grade.course_code = payload["courseCode"]
    if "courseName" in payload:
        grade.course_name = payload["courseName"]
    if "credit" in payload:
        grade.credit = float(payload["credit"])
    if "score" in payload:
        grade.score = float(payload["score"])
    if "semester" in payload:
        grade.semester = payload["semester"]
    if "teacher" in payload:
        grade.teacher = payload["teacher"]
    db.session.commit()
    return grade


def get_transcript(student_no):
    student = Student.query.filter_by(student_no=student_no).first()
    if not student:
        return None
    grades = Grade.query.filter_by(student_id=student.id).order_by(Grade.semester.desc(), Grade.course_code).all()
    return {
        "student": student.to_dict(),
        "summary": calculate_summary(grades),
        "grades": [grade.to_dict() for grade in grades],
    }


def analyze_grades():
    all_grades = Grade.query.all()
    if not all_grades:
        return []

    course_map = {}
    for grade in all_grades:
        key = (grade.course_code, grade.course_name, grade.semester, grade.teacher, grade.credit)
        if key not in course_map:
            course_map[key] = []
        course_map[key].append(grade)

    def count_in_range(scores, low, high):
        return sum(1 for s in scores if low <= s < high)

    result = []
    for (code, name, semester, teacher, credit), grades in course_map.items():
        scores = [g.score for g in grades]
        count = len(scores)
        avg = round(sum(scores) / count, 2) if count else 0
        max_score = round(max(scores), 2) if scores else 0
        min_score = round(min(scores), 2) if scores else 0
        pass_count = sum(1 for s in scores if s >= 60)
        pass_rate = round(pass_count / count * 100, 2) if count else 0

        distribution = {
            "range0_59": count_in_range(scores, 0, 60),
            "range60_69": count_in_range(scores, 60, 70),
            "range70_79": count_in_range(scores, 70, 80),
            "range80_89": count_in_range(scores, 80, 90),
            "range90_100": count_in_range(scores, 90, 101),
        }

        result.append({
            "courseCode": code,
            "courseName": name,
            "semester": semester,
            "teacher": teacher,
            "credit": credit,
            "studentCount": count,
            "average": avg,
            "maxScore": max_score,
            "minScore": min_score,
            "passRate": pass_rate,
            "distribution": distribution,
        })

    result.sort(key=lambda x: (x["semester"], x["courseCode"]), reverse=True)
    return result
