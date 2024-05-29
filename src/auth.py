def check_student_id(student_id: str) -> bool:
    if not student_id.isdigit():
        return False
    
    student_id1 = int(student_id)

    with open('student_id.txt', 'r') as file:
        for line in file:
            student_id2 = int(line.strip())
            if student_id1 == student_id2:
                return True

    return False

