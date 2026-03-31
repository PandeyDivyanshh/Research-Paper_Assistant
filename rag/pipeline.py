import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_groq import ChatGroq
# NEW
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from vectorstore.store import search_chunks
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.2,
        max_tokens=1024,
    )
    return llm


def build_prompt():
    template = """
You are an intelligent research paper assistant.
Use ONLY the context below to answer the user's question.
If the answer is not found in the context, say "I couldn't find this in the paper."
Do NOT make up information.

Context from the paper:
{context}

User Question:
{question}

Answer:
"""
    return PromptTemplate(
        input_variables=["context", "question"],
        template=template
    )


def answer_question(question: str) -> str:
    relevant_chunks = search_chunks(question, top_k=3)
    context = "\n\n".join(relevant_chunks)
    prompt = build_prompt()
    llm = get_llm()
    parser = StrOutputParser()
    chain = prompt | llm | parser
    answer = chain.invoke({
        "context": context,
        "question": question
    })
    return answer


# ---- TEST BLOCK ----
if __name__ == "__main__":
    test_questions = [
        "What is the main contribution of this paper?",
        "What dataset was used in the experiments?",
        "What is scaled dot-product attention?"
    ]

    for question in test_questions:
        print(f"\n Question: {question}")
        print(f" Answer: {answer_question(question)}")
        print("-" * 60)