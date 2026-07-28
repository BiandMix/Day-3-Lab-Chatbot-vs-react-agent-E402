"""Tool registry for the student course advisor agent."""

# Danh mục môn học mẫu để Agent tra cứu.
COURSE_CATALOG = {
    "CS101": {
        "name": "Introduction to Programming",
        "major": "computer science",
        "semester": "fall",
        "credits": 3,
        "schedule": ["Mon 09:00-10:30", "Wed 09:00-10:30"],
        "prerequisites": [],
        "tags": ["programming", "python", "foundation", "beginner"],
        "description": "Môn nhập môn lập trình với Python cho sinh viên năm nhất.",
    },
    "CS201": {
        "name": "Data Structures and Algorithms",
        "major": "computer science",
        "semester": "fall",
        "credits": 4,
        "schedule": ["Tue 09:00-11:00", "Thu 09:00-11:00"],
        "prerequisites": ["CS101"],
        "tags": ["algorithms", "data structures", "problem solving"],
        "description": "Môn cốt lõi về cấu trúc dữ liệu và giải thuật.",
    },
    "CS210": {
        "name": "Database Systems",
        "major": "computer science",
        "semester": "spring",
        "credits": 3,
        "schedule": ["Mon 13:00-14:30", "Wed 13:00-14:30"],
        "prerequisites": ["CS101"],
        "tags": ["database", "sql", "backend"],
        "description": "Thiết kế cơ sở dữ liệu quan hệ và truy vấn SQL.",
    },
    "AI301": {
        "name": "Introduction to Artificial Intelligence",
        "major": "computer science",
        "semester": "fall",
        "credits": 3,
        "schedule": ["Tue 13:00-14:30", "Thu 13:00-14:30"],
        "prerequisites": ["CS201"],
        "tags": ["ai", "machine learning", "intelligent systems"],
        "description": "Tổng quan về AI, tìm kiếm, biểu diễn tri thức và ML cơ bản.",
    },
    "AI210": {
        "name": "AI Foundations for Beginners",
        "major": "computer science",
        "semester": "fall",
        "credits": 4,
        "schedule": ["Fri 09:00-11:00"],
        "prerequisites": ["CS101"],
        "tags": ["ai", "foundation", "beginner", "intelligent systems"],
        "description": "Môn nhập môn AI dành cho sinh viên đã có nền tảng lập trình cơ bản.",
    },
    "DS220": {
        "name": "Business Data Analysis",
        "major": "business analytics",
        "semester": "fall",
        "credits": 3,
        "schedule": ["Mon 10:45-12:15", "Wed 10:45-12:15"],
        "prerequisites": [],
        "tags": ["analytics", "data", "business"],
        "description": "Nhập môn phân tích dữ liệu cho bài toán kinh doanh.",
    },
    "BUS105": {
        "name": "Principles of Marketing",
        "major": "business",
        "semester": "fall",
        "credits": 3,
        "schedule": ["Tue 15:00-16:30", "Thu 15:00-16:30"],
        "prerequisites": [],
        "tags": ["marketing", "business", "communication"],
        "description": "Nền tảng marketing và hành vi khách hàng.",
    },
}

# Lộ trình học mẫu theo mục tiêu nghề nghiệp.
STUDY_PLAN_LIBRARY = {
    "ai engineer": [
        "CS101 để xây nền tảng lập trình.",
        "CS201 để rèn giải thuật và tư duy kỹ thuật.",
        "AI301 để tiếp cận kiến thức AI cốt lõi.",
    ],
    "backend developer": [
        "CS101 để thành thạo code cơ bản.",
        "CS201 để tối ưu tư duy cấu trúc dữ liệu.",
        "CS210 để học thiết kế cơ sở dữ liệu và SQL.",
    ],
    "business analyst": [
        "DS220 để làm quen với dữ liệu kinh doanh.",
        "BUS105 để hiểu bối cảnh vận hành doanh nghiệp.",
        "CS210 nếu muốn tăng kỹ năng truy vấn dữ liệu.",
    ],
}


def _is_blank(value) -> bool:
    return value is None or str(value).strip() == ""


def _normalize_text(value: str) -> str:
    """
    Normalize text for case-insensitive matching.

    Args:
        value (str): Chuỗi đầu vào cần chuẩn hóa.
    """
    if value is None:
        return ""
    return str(value).strip().lower()


def _normalize_course_code(course_code) -> str:
    if course_code is None:
        return ""
    return str(course_code).strip().upper()


def _normalize_course_list(course_list):
    if not isinstance(course_list, list):
        return None
    return [_normalize_course_code(course) for course in course_list if not _is_blank(course)]


def _normalize_int(value):
    if value is None or value == "":
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.strip().isdigit():
        return int(value.strip())
    return None


def _course_exists(course_code: str) -> tuple[bool, str]:
    """
    Return whether a course code exists and its normalized form.

    Args:
        course_code (str): Mã môn cần kiểm tra.
    """
    normalized_code = _normalize_course_code(course_code)
    return normalized_code in COURSE_CATALOG, normalized_code


def search_courses(
    student_major: str = "",
    interest: str = "",
    semester: str = "fall",
    level: str = "",
    max_credits: int | None = None,
) -> str:
    """
    Suggest courses that match a student's major, interest, and semester.

    Args:
        student_major (str): Ngành học của sinh viên.
        interest (str): Sở thích hoặc hướng quan tâm học tập.
        semester (str): Học kỳ cần tra cứu.
        level (str): Trình độ mong muốn, ví dụ beginner hoặc advanced.
        max_credits (int | None): Giới hạn số tín chỉ tối đa cho mỗi môn.
    """
    desired_interest = _normalize_text(interest)
    major = _normalize_text(student_major)
    selected_semester = _normalize_text(semester)
    desired_level = _normalize_text(level)
    normalized_max_credits = _normalize_int(max_credits)

    if not desired_interest:
        return "LỖI: Cần cung cấp interest để gợi ý môn học."

    if max_credits not in (None, "") and normalized_max_credits is None:
        return "LỖI: max_credits phải là số nguyên hợp lệ."

    if major in {"all", "any", "*"}:
        major = ""
    if selected_semester in {"all", "all_semester", "any", "*"}:
        selected_semester = ""

    matches = []
    for course_code, course in COURSE_CATALOG.items():
        same_major = not major or course["major"] == major
        same_semester = not selected_semester or course["semester"] == selected_semester
        interest_matched = any(desired_interest in tag for tag in course["tags"])
        level_matched = not desired_level or any(desired_level in tag for tag in course["tags"])
        credit_matched = normalized_max_credits is None or course["credits"] <= normalized_max_credits
        if same_major and same_semester and interest_matched and level_matched and credit_matched:
            matches.append(
                f"- {course_code}: {course['name']} ({course['credits']} tín chỉ) | "
                f"Lịch: {', '.join(course['schedule'])} | "
                f"Tiên quyết: {', '.join(course['prerequisites']) if course['prerequisites'] else 'Không có'}"
            )

    if not matches:
        filters = [f"sở thích '{interest}'"]
        if major:
            filters.insert(0, f"ngành '{student_major}'")
        if selected_semester:
            filters.append(f"học kỳ '{semester}'")
        if desired_level:
            filters.append(f"trình độ '{level}'")
        if normalized_max_credits is not None:
            filters.append(f"tối đa {normalized_max_credits} tín chỉ")
        return "LỖI: Không tìm thấy môn phù hợp với " + ", ".join(filters) + "."

    return "Các môn phù hợp:\n" + "\n".join(matches)


def check_prerequisites(course_code: str, completed_courses: list[str]) -> str:
    """
    Check whether the student has completed the prerequisites for a course.

    Args:
        course_code (str): Mã môn cần kiểm tra tiên quyết.
        completed_courses (list[str]): Danh sách mã môn đã hoàn thành.
    """
    exists, normalized_code = _course_exists(course_code)
    if not normalized_code:
        return "LỖI: Cần cung cấp course_code hợp lệ."
    if not exists:
        return f"LỖI: Không tồn tại môn học với mã '{course_code}'."

    normalized_completed_courses = _normalize_course_list(completed_courses)
    if normalized_completed_courses is None:
        return "LỖI: completed_courses phải là danh sách mã môn."

    completed_set = set(normalized_completed_courses)
    prerequisites = COURSE_CATALOG[normalized_code]["prerequisites"]
    missing = [course for course in prerequisites if course not in completed_set]

    if not prerequisites:
        return f"Môn {normalized_code} không có môn tiên quyết. Sinh viên có thể đăng ký."

    if missing:
        return (
            f"CHƯA ĐỦ ĐIỀU KIỆN: Để học {normalized_code}, sinh viên còn thiếu "
            f"các môn tiên quyết: {', '.join(missing)}."
        )

    return f"ĐỦ ĐIỀU KIỆN: Sinh viên đã hoàn thành đầy đủ tiên quyết cho môn {normalized_code}."


def calculate_total_credits(selected_courses: list[str]) -> str:
    """
    Calculate the total credits for a list of selected courses.

    Args:
        selected_courses (list[str]): Danh sách mã môn đã chọn.
    """
    normalized_courses = _normalize_course_list(selected_courses)
    if normalized_courses is None:
        return "LỖI: selected_courses phải là danh sách mã môn."
    if not normalized_courses:
        return "LỖI: Danh sách selected_courses đang trống."

    total_credits = 0
    unknown_courses = []
    valid_courses = []

    for course_code in normalized_courses:
        exists, normalized_code = _course_exists(course_code)
        if not exists:
            unknown_courses.append(course_code)
            continue
        total_credits += COURSE_CATALOG[normalized_code]["credits"]
        valid_courses.append(normalized_code)

    if unknown_courses:
        return f"LỖI: Không tìm thấy các mã môn sau: {', '.join(unknown_courses)}."

    return f"Tổng số tín chỉ của {', '.join(valid_courses)} là {total_credits} tín chỉ."


def check_schedule_conflict(selected_courses: list[str]) -> str:
    """
    Check whether any selected courses have overlapping schedules.

    Args:
        selected_courses (list[str]): Danh sách mã môn cần kiểm tra trùng lịch.
    """
    normalized_courses = _normalize_course_list(selected_courses)
    if normalized_courses is None:
        return "LỖI: selected_courses phải là danh sách mã môn."
    if len(normalized_courses) < 2:
        return "LỖI: Cần ít nhất 2 môn để kiểm tra xung đột lịch."

    unknown_courses = []
    schedule_map = {}

    for course_code in normalized_courses:
        exists, normalized_code = _course_exists(course_code)
        if not exists:
            unknown_courses.append(course_code)
            continue
        schedule_map[normalized_code] = COURSE_CATALOG[normalized_code]["schedule"]

    if unknown_courses:
        return f"LỖI: Không tìm thấy các mã môn sau: {', '.join(unknown_courses)}."

    conflicts = []
    course_codes = list(schedule_map.keys())
    for index, first_code in enumerate(course_codes):
        for second_code in course_codes[index + 1 :]:
            overlap = set(schedule_map[first_code]) & set(schedule_map[second_code])
            if overlap:
                conflicts.append(
                    f"{first_code} trùng với {second_code} ở khung giờ: {', '.join(sorted(overlap))}"
                )

    if conflicts:
        return "PHÁT HIỆN XUNG ĐỘT LỊCH:\n" + "\n".join(f"- {item}" for item in conflicts)

    return "KHÔNG CÓ XUNG ĐỘT: Các môn đã chọn không bị trùng lịch."


def suggest_study_plan(goal: str, available_time: str) -> str:
    """
    Suggest a basic study plan based on a career goal and available time.

    Args:
        goal (str): Mục tiêu nghề nghiệp hoặc hướng phát triển.
        available_time (str): Mức thời gian có thể dành cho việc học.
    """
    normalized_goal = _normalize_text(goal)
    normalized_time = _normalize_text(available_time)

    if not normalized_goal:
        return "LỖI: Cần cung cấp goal để gợi ý lộ trình học."

    if normalized_goal not in STUDY_PLAN_LIBRARY:
        return f"LỖI: Chưa có lộ trình mẫu cho mục tiêu '{goal}'."

    workload_advice = {
        "cao": "Bạn có thể đăng ký 15-18 tín chỉ nếu đã quen nhịp học.",
        "vừa": "Bạn nên giữ mức 12-15 tín chỉ để cân bằng học và hoạt động khác.",
        "ít": "Bạn nên ưu tiên 9-12 tín chỉ và chọn các môn nền tảng trước.",
    }
    pacing = workload_advice.get(
        normalized_time,
        "Bạn nên xác nhận lại quỹ thời gian để chọn số tín chỉ phù hợp.",
    )

    recommended_steps = "\n".join(f"- {item}" for item in STUDY_PLAN_LIBRARY[normalized_goal])
    return (
        f"Gợi ý lộ trình cho mục tiêu '{goal}':\n"
        f"{recommended_steps}\n"
        f"Khuyến nghị tải học tập: {pacing}"
    )


# Registry các tool mà Agent được phép gọi.
AVAILABLE_TOOLS = {
    "search_courses": search_courses,
    "check_prerequisites": check_prerequisites,
    "calculate_total_credits": calculate_total_credits,
    "check_schedule_conflict": check_schedule_conflict,
    "suggest_study_plan": suggest_study_plan,
}
