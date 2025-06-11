# app/utils/prompter.py

def create_prompt(question: str, context: str) -> str:
    return f"""You are a helpful assistant at Macquarie University.
Use the following context to answer the question as accurately as possible.

Context:
{context}

Question:
{question}

Answer:"""