const API_URL = "http://127.0.0.1:8000/translate";

const form = document.querySelector("#translation-form");
const input = document.querySelector("#sanskrit-input");
const findButton = document.querySelector("#find-button");
const clearButton = document.querySelector("#clear-button");
const formMessage = document.querySelector("#form-message");
const resultPanel = document.querySelector("#result-panel");
const emptyState = document.querySelector("#empty-state");
const exampleButtons = document.querySelectorAll(".example-chip");
const themeToggle = document.querySelector(".theme-toggle");

const resultSource = document.querySelector("#result-source");
const resultSanskrit = document.querySelector("#result-sanskrit");
const resultEnglish = document.querySelector("#result-english");
const resultMeaning = document.querySelector("#result-meaning");

function setMessage(message = "") {
  formMessage.textContent = message;
}

function clearResult() {
  resultPanel.hidden = true;
  emptyState.hidden = false;
  resultSource.textContent = "";
  resultSource.classList.remove("ai-source");
  resultSanskrit.textContent = "";
  resultEnglish.textContent = "";
  resultMeaning.textContent = "";
}

function showResult(data) {
  if (!data.sanskrit || !data.english || !data.meaning || !data.source) {
    throw new Error("The translation service returned an incomplete result.");
  }
  resultSanskrit.textContent = data.sanskrit;
  resultEnglish.textContent = data.english;
  resultMeaning.textContent = data.meaning;
  resultSource.textContent = data.source;
  resultSource.classList.toggle("ai-source", data.source === "AI Translation Model");
  resultPanel.hidden = false;
  emptyState.hidden = true;
  resultPanel.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

async function findMeaning(event) {
  event.preventDefault();
  const text = input.value.trim();

  setMessage();
  if (!text) {
    clearResult();
    setMessage("Please enter a Sanskrit word or text first.");
    input.focus();
    return;
  }

  findButton.disabled = true;
  findButton.classList.add("is-loading");
  findButton.querySelector("span:first-child").textContent = "Analyzing Sanskrit...";
  clearResult();

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "The translation service could not process this request.");
    }

    showResult(data);
  } catch (error) {
    setMessage(error.message.includes("Failed to fetch")
      ? "The API is unavailable. Please start the FastAPI backend and try again."
      : error.message);
  } finally {
    findButton.disabled = false;
    findButton.classList.remove("is-loading");
    findButton.querySelector("span:first-child").textContent = "Find Meaning";
  }
}

form.addEventListener("submit", findMeaning);

clearButton.addEventListener("click", () => {
  input.value = "";
  setMessage();
  clearResult();
  input.focus();
});

exampleButtons.forEach((button) => {
  button.addEventListener("click", () => {
    input.value = button.textContent.trim();
    setMessage();
    input.focus();
  });
});

themeToggle.addEventListener("click", () => {
  document.body.classList.toggle("soft-theme");
  themeToggle.querySelector("span").textContent = document.body.classList.contains("soft-theme") ? "☀" : "☾";
});
