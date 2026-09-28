from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate


# --------------------------------
# 1. Create FastAPI application
# --------------------------------

app = FastAPI(
    title="Semantic Word Generator",
    description="Generate a semantically related word using a local LLM.",
    version="1.0.0",
)


# --------------------------------
# 2. Configure frontend
# --------------------------------

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


# --------------------------------
# 3. Define AI response structure
# --------------------------------

class WordResult(BaseModel):
    word: str
    meaning: str
    example: str


# --------------------------------
# 4. Configure Ollama / Qwen
# --------------------------------

llm = ChatOllama(
    model="qwen2.5-coder:7b",
    temperature=0.8,
)


# --------------------------------
# 5. Create prompt
# --------------------------------

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are a semantic word generator.

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


# --------------------------------
# 6. Create LangChain chain
# --------------------------------

chain = prompt | llm.with_structured_output(WordResult)


# --------------------------------
# 7. Function to generate a word
# --------------------------------

def generate_word(user_prompt: str) -> WordResult:

    response = chain.invoke({
        "user_prompt": user_prompt
    })

    return response


# --------------------------------
# 8. Request model for API
# --------------------------------

class WordRequest(BaseModel):
    prompt: str


# --------------------------------
# 9. Homepage
# --------------------------------

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


# --------------------------------
# 10. API endpoint
# --------------------------------

@app.post("/generate", response_model=WordResult)
async def generate(request: WordRequest):

    result = generate_word(request.prompt)

    return result