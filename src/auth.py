def check_student_id(student_id: str) -> bool:
    if not student_id.isdigit():
        return False

    member_id_list = [
        # B4
        '21122015',
        '21122017',
        '21122020',
        '21122038',
        # M1
        '24622017',
        '24622033',
        '24622044',
        # M2
        '23622010',
        '23622026',
        '23622047',
        # D2
        '23821004',
    ]

    return student_id in member_id_list
