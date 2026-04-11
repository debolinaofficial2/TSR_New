def rule_score(student, teacher):

    score = 0
    reasons = []

    # Subject match
    if student["subject"].lower() in str(teacher["subject_specialization"]).lower():
        score += 40
        reasons.append("Subject match")

    # Board match (designation usually contains boards)
    if student["board"].lower() in str(teacher["designation"]).lower():
        score += 20
        reasons.append("Board familiarity")

    # Teaching goal alignment
    if student["goal"] == "Concept clarity":
        score += 15
        reasons.append("Conceptual learning support")

    # Availability placeholder (can be upgraded later)
    score += 10
    reasons.append("General availability compatibility")

    # Experience inference from designation keywords
    if "professor" in str(teacher["designation"]).lower():
        score += 10
        reasons.append("Senior teaching experience")

    return score, reasons