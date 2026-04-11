from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def semantic_score(student_text, teacher_text):

    if not student_text or not teacher_text:
        return 0

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(
        [student_text, teacher_text]
    )

    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0]

    return similarity * 20