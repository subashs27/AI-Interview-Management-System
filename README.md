## 🚀 Live Demo

Try the application: [Open AI Interview Management System](https://ai-interview-management-system-88qsa6qb2jvn2cibmb7zg7.streamlit.app/)

## Features
- Resume upload and analysis
- Candidate skills and project extraction
- AI-powered interview question generation
- Interview evaluation and feedback

## Tech Stack
Python · Streamlit · Gemini API · SQLite
                    
##  System Architecture 
### 1. Candidate Module Workflow
                    
                    
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

## 2 Admin Dashboard – How It Works

The Admin Dashboard allows administrators to generate and manage interview knowledge and questions for different technical roles and topics.

### Workflow
1. Select Topics: Provide roles, categories, and topics through a CSV file.
2. Generate Knowledge: Gemini API generates technical concepts, interview questions, ideal answers, and evaluation criteria.
3. Store Knowledge: Save generated content in the SQLite database.
4. Support Interviews: The Candidate Dashboard retrieves relevant knowledge and questions for AI-assisted interviews.

### Technologies Used
- Frontend:Streamlit
- AI:Google Gemini API
- Backend:Python
- Database:SQLite
- Input:CSV


## Run Locally
1. Clone this repository.
2. Install dependencies using `pip install -r requirements.txt`.
3. Configure your Gemini API key using Streamlit secrets or environment variables.
4. Run `streamlit run app.py`.

##  Deployment
The application is deployed on Streamlit Community Cloud.
The app may take a short time to start after a period of inactivity.

## Security Notes

- Store API keys securely using Streamlit Cloud Secrets or environment variables.
- Never commit API keys, passwords, or sensitive credentials to GitHub.
- Use sample or fictional resumes when testing the application.
- Handle candidate resumes and interview results responsibly to protect personal information.
- Avoid exposing sensitive information in application logs or error messages.

## Author

SUBASH S

GitHub: [subashs27](https://github.com/subashs27)
