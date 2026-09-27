from pydantic import BaseModel
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate


# Define the structure we want from the AI
class WordResult(BaseModel):
    word: str
    meaning: str
    example: str


# Local Ollama model
llm = ChatOllama(
    model="qwen2.5-coder:7b",
    temperature=0.8,
)


# Prompt
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are a simple related word generator.

        The user will provide a word, topic, concept, or short prompt.

        Generate ONE word that is meaningfully related to the user's prompt.

        Rules:
        - Generate only one word.
        - The word should be related to the user's prompt.
        - Keep the meaning simple.
        - Give one short example sentence.
        """
    ),
    ("human", "{user_prompt}")
])


# Create LangChain chain
chain = prompt | llm.with_structured_output(WordResult)


def generate_word(user_prompt):
    response = chain.invoke({
        "user_prompt": user_prompt
    })

    return response


if __name__ == "__main__":
    print("=== LangChain Related Word Generator ===")
    print("Using local Qwen 2.5 Coder 7B")
    print("Type 'exit' to quit.\n")

    while True:
        user_prompt = input("Enter your prompt: ")

        if user_prompt.lower() == "exit":
            print("Goodbye!")
            break

        try:
            result = generate_word(user_prompt)

            print("\nResult:")
            print(f"Word: {result.word}")
            print(f"Meaning: {result.meaning}")
            print(f"Example: {result.example}")
            print()

        except Exception as e:
            print(f"\nError: {e}\n")