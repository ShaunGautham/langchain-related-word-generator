const promptInput = document.getElementById("prompt");
const generateButton = document.getElementById("generateButton");

const resultSection = document.getElementById("result");
const wordElement = document.getElementById("word");
const meaningElement = document.getElementById("meaning");
const exampleElement = document.getElementById("example");
const errorElement = document.getElementById("error");


async function generateWord() {

    const prompt = promptInput.value.trim();

    if (!prompt) {
        errorElement.textContent = "Please enter a word or topic.";
        return;
    }

    errorElement.textContent = "";

    generateButton.disabled = true;
    generateButton.textContent = "Generating...";

    try {

        const response = await fetch("/generate", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                prompt: prompt
            })

        });


        if (!response.ok) {
            throw new Error("Failed to generate word.");
        }


        const data = await response.json();


        wordElement.textContent = data.word;
        meaningElement.textContent = data.meaning;
        exampleElement.textContent = data.example;


        resultSection.classList.remove("hidden");


    } catch (error) {

        errorElement.textContent =
            "Something went wrong. Make sure Ollama is running.";

    } finally {

        generateButton.disabled = false;
        generateButton.textContent = "Generate";

    }
}


generateButton.addEventListener("click", generateWord);


promptInput.addEventListener("keydown", (event) => {

    if (event.key === "Enter") {
        generateWord();
    }

});