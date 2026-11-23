# ExcuseGPT 💬

> **Because Every Situation Deserves an Exceptionally Creative Explanation.**

ExcuseGPT is an AI-powered application for generating and refining context-grounded explanations for professional, academic, personal, and social situations.

Instead of relying on generic or fabricated excuses, it takes the circumstances supplied by the user and generates **three distinct responses** that aim to preserve the original facts while varying the way they are communicated.

## 🚀 Live Demo

[Launch ExcuseGPT](https://excusegpt-fmfp6khenoigrsxkedx9ez.streamlit.app/)

---

## 🛡️ Core Philosophy: Contextual Grounding

ExcuseGPT follows one central principle:

> **Creativity changes expression, not reality.**

- **Fact preservation:** Responses are designed to retain the circumstances provided by the user.
- **Grounding checks:** A custom validator checks for common forms of unsupported details, such as unreported actions, locations, time references, and commitments.
- **Natural communication:** Responses vary in wording, tone, and communication approach without needing to invent an emergency or an unverified reason.
- **User responsibility:** Generated and refined responses should be reviewed before being used or sent.

---

## 🎯 Available Response Approaches

ExcuseGPT has five available communication approaches. Each generation returns three responses using different approaches.

1. **Direct Acknowledgement:** Clearly states what happened with honesty and transparency.
2. **Alternative Framing:** Presents genuine circumstances from a constructive perspective.
3. **Accountability & Recovery:** Takes ownership and focuses on a practical way forward.
4. **Light Humour:** Uses mild, situation-appropriate humour where suitable.
5. **Emotional Expression:** Communicates sincere regret and personal sentiment.

---

## 🚀 Application Features

ExcuseGPT has four main sections:

### ✨ Create
- Enter the situation and provide genuine context.
- Customize the response using category, tone, creativity, formality, and length.
- Generate three distinct responses.
- Refine an individual response using a written instruction.
- Save responses to Favourites.

### 📚 History
- Browse previous generations.
- Search previous situations by keyword.
- Filter generations by category.
- Review the responses associated with each generation.
- Refine previous responses and save useful results.

### ⭐ Favourites
- View saved responses.
- Keep useful original and refined responses together.
- Remove saved responses when they are no longer needed.

### ℹ️ About
- Read about the product philosophy and grounding principles.
- Review the five available response approaches.
- Explore the application's technology and architecture.
- Read the data and privacy information.

---

## ⚙️ Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend** | Streamlit, Python 3.12 | User interface, navigation, and interactive workflows |
| **Styling** | Custom HTML and CSS | Application visual design |
| **Backend** | FastAPI | API endpoints for generation and refinement |
| **Server** | Uvicorn | Runs the FastAPI application |
| **AI Integration** | Google Gemini Developer API | Generates and refines responses |
| **Validation** | Pydantic | Validates request and response data |
| **Grounding** | Custom Python validator | Checks generated content for common unsupported details |
| **Persistence** | SQLite | Stores application history and favourites locally |
| **Testing** | Pytest | Automated unit and integration tests |

---

## 🔒 Data & Privacy

- **Local application storage:** Generation history and saved favourites are stored in the application's local SQLite database (`data/excusegpt.db`).
- **External AI processing:** When a user requests generation or refinement, the relevant situation details and instructions are sent to Google's Gemini Developer API.
- **API availability:** Requests are subject to the API provider's availability, rate limits, quotas, and applicable terms. These may change over time.
- **Sensitive information:** Avoid entering passwords, confidential information, or sensitive personal details into the application.

---

## 🛠️ Quick Start Guide

### 1. Prerequisites

- Python 3.12
- A Google Gemini API key from [Google AI Studio](https://aistudio.google.com/)

### 2. Clone the Repository

```powershell
git clone https://github.com/AyushVishwakarma19/ExcuseGPT.git
cd ExcuseGPT
```

### 3. Create and Activate a Virtual Environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 5. Configure the API Key

Create a `.env` file in the project root and add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Keep your actual `.env` file private. Do not commit API keys or other credentials to GitHub.

### 6. Run the Application

Open two terminal sessions from the project root.

**Terminal 1 — Start the FastAPI backend:**

```powershell
uvicorn backend.main:app --port 8000 --reload
```

The backend runs at `http://127.0.0.1:8000`.

**Terminal 2 — Start the Streamlit frontend:**

```powershell
python -m streamlit run frontend/app.py
```

Streamlit will provide the local application URL, normally `http://localhost:8501`.

---

## 🧪 Running Automated Tests

Run the test suite from the project root:

```powershell
python -m pytest -v .\tests
```

**Latest verified result:** 42 tests passed.

The test suite covers API behaviour, grounding validation, AI service handling, prompt construction, Pydantic schemas, and SQLite storage.

---

## ⚠️ Important Notes

- A working Gemini API key and available API quota are required for live generation and refinement.
- The AI provider may temporarily return service-unavailable or rate-limit errors. These are external service conditions and do not necessarily indicate a problem with the local application.
- Review generated responses for accuracy and suitability before using them.

---

**ExcuseGPT** · Context-Grounded AI Studio · Built with Python, Streamlit, FastAPI, Pydantic, SQLite, and Google Gemini.
