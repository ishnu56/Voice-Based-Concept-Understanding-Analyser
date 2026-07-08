from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def evaluate_similarity(reference_text, student_text):
    ref_embedding = model.encode(reference_text, convert_to_tensor=True)
    stu_embedding = model.encode(student_text, convert_to_tensor=True)

    similarity = util.pytorch_cos_sim(ref_embedding, stu_embedding).item()
    score = round(similarity * 100, 2)

    if score >= 90:
        level = "Strong"
    elif score >= 70:
        level = "Moderate"
    else:
        level = "Poor"

    return score, level