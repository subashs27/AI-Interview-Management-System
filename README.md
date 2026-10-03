                    AI Interview Management System

                             Candidate
                                 │
                                 ▼
                    Upload Resume (PDF)
                                 │
                                 ▼
                     Resume Parser (PyMuPDF)
                                 │
                                 ▼
                    Resume Analyzer (Gemini)
                                 │
                                 ▼
      Extract Candidate Information
      ───────────────────────────────────────────────
      • Name
      • Target Role
      • Skills
      • Projects
      • Certificates
      • Technologies
      ───────────────────────────────────────────────
                                 │
                                 ▼
                  Knowledge Retrieval Engine
                                 │
               Search SQLite Knowledge Database
                                 │
                ┌────────────────┴───────────────┐
                │                                │
                ▼                                ▼
          Topic Exists                     Topic Not Found
          in SQLite                           in SQLite
                │                                │
                ▼                                ▼
      Load Stored Knowledge            Generate using Gemini
      + Interview Questions                  + Questions
                │                                │
                └──────────────┬─────────────────┘
                               ▼
                     Save New Knowledge
                     into SQLite Database
                               │
                               ▼
                    Interview Question Pool
                               │
                               ▼
                   Adaptive Interview Engine
                               │
          Select Question Based on Candidate Level
                               │
                               ▼
                     Voice Recording
                               │
                               ▼
                     Speech-to-Text
                               │
                               ▼
                  Candidate Transcript
                               │
                               ▼
                  Evaluation Engine (Gemini)
                               │
                               ▼
        Technical • Communication • Confidence
                               │
                               ▼
                 Follow-up Question Engine
                               │
                               ▼
              Continue Until Interview Ends
                               │
                               ▼
               AI Interview Report (Memory Only)
                               │
                               ▼
                    Display to Candidate# AI-Interview-Management-System

## Deploy on Render

This repository is a Streamlit application. Deploy it on Render as a **Web Service** (not as a Vercel serverless function):

1. Connect this repository in Render and create a Web Service using the included `render.yaml` Blueprint.
2. Add `GOOGLE_API_KEY` in the service's environment settings.
3. Deploy. Render installs dependencies from `requirements.txt` and starts Streamlit on Render's assigned port.

The SQLite database is stored in `knowledge.db`. Render's local filesystem is not persistent by default, so database changes made at runtime may be lost when the service restarts or redeploys.
