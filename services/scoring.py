def evaluate(text):
    scores = {}

    words = text.split()
    word_count = len(words)

    # 🟢 Task Completion
    if word_count > 120:
        scores["task_completion"] = 9
    elif word_count > 80:
        scores["task_completion"] = 7
    elif word_count > 40:
        scores["task_completion"] = 5
    else:
        scores["task_completion"] = 3

    # 🟡 Communication
    fillers = ["um", "uh", "like", "you know", "actually"]
    filler_count = sum(text.count(f) for f in fillers)

    if filler_count == 0:
        scores["communication"] = 9
    elif filler_count < 3:
        scores["communication"] = 7
    elif filler_count < 6:
        scores["communication"] = 5
    else:
        scores["communication"] = 3

    # 🔵 Output Quality
    keywords = ["solution", "approach", "result", "because", "reason"]
    keyword_score = sum(1 for word in keywords if word in text)

    scores["output_quality"] = min(keyword_score * 2, 10)

    # 🟣 Judgement
    logic_words = ["if", "then", "else", "consider", "tradeoff"]
    logic_score = sum(1 for word in logic_words if word in text)

    scores["judgement"] = min(5 + logic_score, 10)

    return scores



def generate_feedback(text, scores):
    strengths = []
    improvements = []

    # Strengths
    if scores["task_completion"] >= 7:
        strengths.append("Good detailed answer")

    if scores["communication"] >= 7:
        strengths.append("Clear communication with minimal fillers")

    if scores["output_quality"] >= 6:
        strengths.append("Used relevant technical terms")

    if scores["judgement"] >= 7:
        strengths.append("Shows good logical reasoning")

    # Improvements
    if scores["task_completion"] < 5:
        improvements.append("Answer lacks depth")

    if scores["communication"] < 5:
        improvements.append("Reduce filler words")

    if scores["output_quality"] < 5:
        improvements.append("Include more structured explanation")

    if scores["judgement"] < 6:
        improvements.append("Add more logical reasoning")

    return {
        "strengths": strengths,
        "improvements": improvements
    }