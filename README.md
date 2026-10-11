# 🚀 [Tips Hindawi](https://www.tipshindawi.com/) Internship (August–October) 2026

> 🎓 This project was built during the [ **Tips Hindawi** ](https://www.tipshindawi.com/) **Internship (August–October) 2026**.

## 👤 Participant

| Field            | Value                                |
| ---------------- | ------------------------------------ |
| Full Name        | Hazem Walid Fawzy                    |
| Project Name     | AI Personal Tutor                    |
| GitHub Username  | hazemwalid2004                       |
| Internship Batch | August–October 2026                  |
| Training Program | Large Language Models (LLMs) Program |
| Organization     | [**Edrak for Ai**](https://edrak4ai.com/en)                         |

---

# 📖 Project Overview

**AI Personal Tutor** is a study assistant that teaches students from their own books and lecture notes. The student uploads a PDF (a full book or a single chapter), types a topic, and the tutor:

1. finds the most relevant parts of the PDF (**RAG**),
2. explains the topic using only what the material says,
3. generates a multiple-choice quiz about it,
4. scores the student's answers, and
5. explains every mistake with feedback taken from the same material.

The project combines **Retrieval-Augmented Generation (RAG)** with an **Output Parser**, so the quiz always comes back as clean, structured data. The AI is told to use *only* the uploaded material, which keeps explanations grounded in the student's own book and reduces made-up answers. Scoring is done in plain Python, not by the model, so the score is always correct.

The project has two parts:

* **Back end** (`ai-personal-tutor-simple.ipynb`): a FastAPI server that runs on Kaggle with a GPU and is exposed to the internet through ngrok.
* **Front end** (`app.py`): a Streamlit web app that talks to the back end.

---

# ✨ Features

* 📄 **Upload any PDF**: books or lecture notes, processed and indexed on upload.
* 🔎 **RAG retrieval**: the text is split into chunks, embedded, and stored in a FAISS vector database. The tutor retrieves the chunks closest to the topic.
* 📘 **Topic explanation**: a definition, a detailed explanation, key points, and an example when the material gives one.
* ❓ **Quiz generation**: 3 multiple-choice questions (A–D) per topic, written only from the retrieved material.
* 🧾 **Structured output parsing**: a Pydantic output parser turns the model's answer into a validated quiz, with automatic retries if the model returns bad JSON.
* ✅ **Reliable scoring**: the score is calculated by Python and cannot be changed by the model.
* 💬 **Personalized feedback**: for each wrong answer, the tutor explains the difference between the student's answer and the correct one, and says what to review.
* 🔒 **Answers hidden until submission**: the correct answers are not sent to the student before they submit.
* 🖥️ **Simple web interface**: upload, choose a topic, read, take the quiz, and see results in one page.

---

# 🛠️ Technologies Used

| Area | Tools |
| --- | --- |
| Language | Python 3 |
| LLM | Qwen2.5-3B-Instruct (Hugging Face Transformers); Mistral-7B-Instruct can be used instead |
| RAG framework | LangChain (`langchain`, `langchain-community`, `langchain-text-splitters`, `langchain-huggingface`) |
| PDF loading | PyPDF (`PyPDFLoader`) |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` |
| Vector database | FAISS (CPU) |
| Output parsing | Pydantic + LangChain `PydanticOutputParser` |
| Back end API | FastAPI + Uvicorn |
| Public tunnel | pyngrok (ngrok) |
| Front end | Streamlit + Requests |
| Platform | Kaggle Notebooks (GPU) |

---

# ⚙️ Installation

The project has two parts that run separately: the **back end** on Kaggle (it needs a GPU) and the **front end** on your own computer.

## Requirements

* A [Kaggle](https://www.kaggle.com/) account (free) with phone verification, so that **GPU** and **Internet** can be turned on
* A free [ngrok](https://ngrok.com/) account and its auth token
* Python 3.9 or newer and Git on your computer

## 1. Clone the repository

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY_NAME.git
cd YOUR_REPOSITORY_NAME
```

## 2. Run the back end on Kaggle

1. Go to Kaggle → **Create → New Notebook → File → Import Notebook**, and upload `ai-personal-tutor-simple.ipynb` from the cloned folder.
2. In the notebook settings, set **Accelerator** to **GPU (T4 x2 or P100)** and turn **Internet** **ON**.
3. *(Optional)* To test with a book, add your PDF as a Kaggle dataset and change `pdf_path` in the "Document loading" cell. If you skip this step, you can upload any PDF later from the front end.
4. Open the last code cell and replace `PUT_YOUR_NGROK_TOKEN_HERE` with your own ngrok auth token (get it from the ngrok dashboard → *Your Authtoken*).
5. Click **Run All**. The first run downloads the models, so it takes a few minutes.
6. When it finishes, the last cell prints two links:

   ```
   Your public URL: https://xxxx-xxxx.ngrok-free.dev
   
   ```

   Copy the **public URL**. You can open the Swagger link to test the API directly.

> ⚠️ Never publish your ngrok token on GitHub. If you share your notebook, remove the token first. The free ngrok plan gives a **new URL each time** you run the notebook.

## 3. Run the front end on your computer

Install the dependencies:

```bash
pip install -r requirements.txt
```

Open `app.py` and paste the public URL from step 2:

```python
# API Configuration
API_URL = "https://xxxx-xxxx.ngrok-free.dev"
```

Start the app:

```bash
streamlit run app.py
```

Streamlit opens the app in your browser, usually at `http://localhost:8501`.

---

# 🚀 Usage

1. **Upload**: choose a PDF (a book or lecture notes) and click **Process PDF**. If the book is already loaded on the server, tick the checkbox to skip this step.
2. **Choose a topic**: type a topic from the book, for example `Wide Area Networks`, then click **Explain topic and generate quiz**.
3. **Learn**: read the explanation: definition, key points, and example.
4. **Take the quiz**: answer the 3 multiple-choice questions and click **Submit answers**.
5. **Review**: see your score, which questions were right or wrong, the correct answers, and the tutor's feedback on each mistake.
6. Click **Try another topic** to continue studying.

### API endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/upload` | Upload a PDF and build the vector store |
| POST | `/generate` | Get the explanation and quiz for a topic |
| POST | `/submit-quiz` | Submit answers and get the score and feedback |

> 💡 For a very large book, load only one chapter (for example `loader.load()[100:200]`) to make processing faster.

---

# 📈 Results

* Built a complete working pipeline: **PDF → chunks → embeddings → FAISS → LLM → structured quiz → scoring → feedback**.
* Tested on a large university textbook (*Computer Networks*, 5th Edition, A. Tanenbaum) with the topic *Wide Area Networks*, producing a grounded explanation, a parsed 3-question quiz, a score, and feedback on the wrong answers.
* The score is computed in Python, so it is always accurate, and the model is only used to explain mistakes.
* Deployed the back end as an API with FastAPI and ngrok, and connected it to a Streamlit front end for end-to-end use.

---

# 🔮 Future Improvements

* 🎤 **Voice input for topics**: let students say the topic out loud instead of typing it. The speech is converted to text with a speech-to-text model (such as Whisper) and sent to the same RAG pipeline.
* 🗣️ **Voice answers with analysis**: let students answer quiz questions by speaking. The system transcribes the voice, understands the answer (for example "I think it is option B" or the answer text itself), maps it to the right choice, submits it, and gives feedback. This would also allow spoken feedback with text-to-speech.
* ➗ **Math equation support**: detect math questions and equations in the material and in student questions, solve them (for example with SymPy or an LLM with a calculator tool), and explain each step in simple language. Equations would be displayed in clean LaTeX in the interface, and the final result would be verified by code instead of trusting the model alone.
* 🧠 **Learning memory**: remember each student's topics, scores, and weak points, so quizzes avoid repeated questions and focus on what the student struggles with.
* 📚 **Multiple documents and chapters**: let students upload several books at once, pick a chapter, and see the page numbers used as sources for every explanation.
* 🎚️ **Difficulty levels and question types**: easy, medium, and hard quizzes, plus true/false and short-answer questions, with the AI grading written answers.
* 🌍 **Arabic and multilingual support**: use multilingual embeddings and models so the tutor works with Arabic books and explains in the student's language.
* 🖼️ **OCR for scanned PDFs**: read scanned books and images of handwritten notes.
* 📊 **Progress dashboard and export**: charts of the student's scores over time, and exporting summaries and quizzes to PDF.
* 🔐 **Accounts and permanent hosting**: user login and a fixed deployment (instead of a temporary ngrok link) so the project is always online.

---

# 📚 About the Internship

This project was developed as part of the [**Tips Hindawi**](https://www.tipshindawi.com/) **Internship (August–October) 2026**, and it will be showcased on the official [Tips Hindawi](https://www.tipshindawi.com/) website.

[Tips Hindawi](https://www.tipshindawi.com/) is the internships department of [**Edrak for Ai**](https://edrak4ai.com/en), and the internship encourages participants to build real-world projects, apply practical skills, and showcase their work through GitHub.

For more information about the internship, training programs, and upcoming batches, visit the official [Tips Hindawi](https://www.tipshindawi.com/) website.

---

# 📄 License

This project is shared for educational and portfolio purposes.
