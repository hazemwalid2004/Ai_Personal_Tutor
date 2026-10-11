import requests
import streamlit as st
import re
# =========================
# API Configuration
# =========================
API_URL = "ADD_YOUR_NGROK_URL_HERE"

HEADERS = {"ngrok-skip-browser-warning": "true"}
TIMEOUT = 600  # the model can take a while on Kaggle

st.set_page_config(page_title="AI Personal Tutor", page_icon="🎓", layout="centered")

# =========================
# Session state
# =========================
for key, default in {
    "pdf_ready": False,
    "generated": None,     # response of /generate
    "result": None,        # response of /submit-quiz
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


def api_post(path, **kwargs):
    """POST to the API and return (data, error_message)."""
    try:
        r = requests.post(API_URL + path, headers=HEADERS, timeout=TIMEOUT, **kwargs)
        data = r.json()
    except requests.exceptions.ConnectionError:
        return None, "Cannot reach the server. Check API_URL and that the Kaggle notebook is still running."
    except requests.exceptions.Timeout:
        return None, "The server took too long to answer. Try again."
    except Exception as e:
        return None, f"Unexpected error: {e}"

    if r.status_code != 200:
        return None, data.get("detail", f"Server error ({r.status_code})")
    if isinstance(data, dict) and "error" in data:
        return None, data["error"]
    return data, None


# =========================
# Header
# =========================
st.title("🎓 AI Personal Tutor")
st.caption("Upload a book or lecture notes, pick a topic, learn it, take a quiz and get feedback.")

# =========================
# Step 1: Upload PDF
# =========================
st.header("1. Upload your material")
uploaded = st.file_uploader("Choose a PDF (book chapter or lecture notes)", type=["pdf"])

if uploaded is not None and st.button("Process PDF", type="primary"):
    with st.spinner("Reading and indexing the PDF..."):
        data, err = api_post(
            "/upload",
            files={"file": (uploaded.name, uploaded.getvalue(), "application/pdf")},
        )
    if err:
        st.error(err)
    else:
        st.session_state.pdf_ready = True
        st.session_state.generated = None
        st.session_state.result = None
        st.success(data.get("message", "PDF processed"))

if not st.session_state.pdf_ready:
    st.info("If the book is already loaded on the server, you can skip this step.")
    if st.checkbox("The PDF is already loaded on the server"):
        st.session_state.pdf_ready = True

# =========================
# Step 2: Topic -> explanation + quiz
# =========================
if st.session_state.pdf_ready:
    st.header("2. Choose a topic")
    topic = st.text_input("Topic", placeholder="e.g. Wide Area Networks")

    if st.button("Explain topic and generate quiz", type="primary", disabled=not topic.strip()):
        st.session_state.result = None
        with st.spinner("The tutor is preparing the explanation and the quiz..."):
            data, err = api_post("/generate", json={"topic": topic.strip()})
        if err:
            st.error(err)
        else:
            st.session_state.generated = data

# =========================
# Show explanation + quiz
# =========================
gen = st.session_state.generated
if gen:
    st.divider()
    st.header(f"📘 {gen['topic']}")

    st.subheader("Explanation")
    st.text(gen["explanation"])  # keeps the Definition / Key Points / Example layout

    st.divider()
    st.header("3. Quiz")

    if st.session_state.result is None:
        with st.form("quiz_form"):
            answers = []
            for i, q in enumerate(gen["quiz"], start=1):
                st.markdown(f"**Question {i}: {q['question']}**")
                letters = list(q["options"].keys())
                choice = st.radio(
                    f"Answer {i}",
                    options=letters,
                    format_func=lambda l, opts=q["options"]: f"{l}) {opts[l]}",
                    index=None,
                    key=f"q_{i}",
                    label_visibility="collapsed",
                )
                answers.append(choice or "")
                st.write("")

            submitted = st.form_submit_button("Submit answers", type="primary")

        if submitted:
            if "" in answers:
                st.warning("Please answer all the questions.")
            else:
                with st.spinner("Checking your answers..."):
                    data, err = api_post("/submit-quiz", json={"answers": answers})
                if err:
                    st.error(err)
                else:
                    st.session_state.result = data
                    st.session_state.my_answers = answers
                    st.rerun()

# =========================
# Results
# =========================
res = st.session_state.result
if res:
    score = res["student_score"]["score"]
    total = res["student_score"]["total"]

    st.header("🏆 Your result")
    st.metric("Score", f"{score} / {total}")
    st.progress(score / total if total else 0)

    mine = st.session_state.get("my_answers", [])
    for i, q in enumerate(res["quiz"]["questions"], start=1):
        correct = q["correct_answer"]
        given = mine[i - 1] if i - 1 < len(mine) else ""
        ok = given == correct
        icon = "✅" if ok else "❌"
        with st.expander(f"{icon} Question {i}: {q['question']}", expanded=not ok):
            for letter, text in q["options"].items():
                tag = ""
                if letter == correct:
                    tag = "  ← correct answer"
                elif letter == given:
                    tag = "  ← your answer"
                st.write(f"{letter}) {text}{tag}")

    st.subheader("Feedback")
    st.text(res["feedback"])

    if st.button("Try another topic"):
        st.session_state.generated = None
        st.session_state.result = None
        st.rerun()
