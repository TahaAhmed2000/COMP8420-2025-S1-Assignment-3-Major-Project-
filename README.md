
# 📚 Macquarie University Custom QA System using RAG

> 🔍 A personalized, retrieval-augmented question-answering system for Macquarie University students, powered by **Gemini**, **FAISS**, and a sleek **React + FastAPI** interface.

---

## 🚀 Features

- 🤖 **RAG-based QA**: Combines search + generation for accurate answers
- 📄 **Over 2,000+ MQ Documents** indexed (unit guides, policies, support articles)
- 💬 **Natural Language Queries** supported
- ⚡️ **FAISS + MiniLM** for lightning-fast semantic search
- 🌐 **Modern Frontend** with React, TailwindCSS & MUI
- 🔒 **Context-linked answers** with source traceability

---

## 🛠️ Tech Stack

### 🧠 Backend:
- Gemini-2.0-Flash API 🌟
- FastAPI ⚡️
- FAISS 🔍
- all-MiniLM-L6-v2 🧬

### 💻 Frontend:
- React 19 ⚛️
- Vite ⚡
- TailwindCSS 🎨
- MUI + Emotion 🎭
- Axios 🌐

---

## 📂 Folder Structure

```bash
├── main.py              # FastAPI backend
├── embeddings/          # Document embeddings & chunking
├── data/                # Raw MQ documents (scraped & cleaned)
├── faiss_index/         # Vector store files
└── frontend/            # React-based frontend (Vite-powered)
````

---

## 🧪 How to Run Locally

> Make sure Python 🐍 and Node.js 🟢 are installed.

### 🔙 Start Backend (FastAPI)

```bash
uvicorn main:app --reload --log-level debug
```

*Run this command in the project **root folder**.*

---

### 🖥️ Start Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

*Run this command inside the **frontend** folder.*

---

## ⚠️ Note on Gemini API Key

> As we are using the **Gemini API (free)**, the API key may expire or get rate-limited.

If you see errors like:

* ❌ `500 Internal Server Error`
* ❌ `400 Bad Request`

🔑 Please **generate a new Gemini API key** from [https://ai.google.dev](https://ai.google.dev),
and update it in the `main.py` file under the API key section.

---

## 🧠 Sample Queries

* 🗓️ “What is the census date for Session 2 in 2025?” → `22 August 2025`
* 🖨️ “Where can I print on campus?” → `Library, MQBS Labs, Wally’s Walk`
* 📜 “What is the late drop policy?” → Relevant MQ policy explained with link

---

## ✍️ Authors

* 👨‍💻 Taha Ahmed Siddiqui — Embeddings, FAISS, Backend logic
* 👨‍💻 Muhammad Ahmad Butt — Gemini API, Prompting, Frontend UI

---

## 📚 References (APA 7)

* Lewis, P., et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. NeurIPS. [https://proceedings.neurips.cc/paper/2020/file/6b493230205f780e1bc26945df7481e5-Paper.pdf](https://proceedings.neurips.cc/paper/2020/file/6b493230205f780e1bc26945df7481e5-Paper.pdf)
* Google. (2024). *Gemini API Documentation*. [https://ai.google.dev/gemini-api/docs](https://ai.google.dev/gemini-api/docs)
* Facebook AI Research. (2019). *FAISS*. [https://github.com/facebookresearch/faiss](https://github.com/facebookresearch/faiss)
* Microsoft. (2020). *MiniLM*. [https://arxiv.org/abs/2002.10957](https://arxiv.org/abs/2002.10957)
* Tiangolo, S. (2023). *FastAPI Docs*. [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com)
* React. (2024). *React Docs*. [https://react.dev](https://react.dev)
* Tailwind Labs. (2024). *TailwindCSS Docs*. [https://tailwindcss.com/docs](https://tailwindcss.com/docs)

---

## 🌟 Star This Repo

If you found this project helpful, please ⭐ it and share it with your peers!

---

## 📬 Contact

For feedback, bug reports, or questions:

* Taha: [tahaahmed.siddiqui@students.mq.edu.au](mailto:tahaahmed.siddiqui@students.mq.edu.au)
* Ahmad: [muhammadahmad.butt@students.mq.edu.au](mailto:muhammadahmad.butt@students.mq.edu.au)


