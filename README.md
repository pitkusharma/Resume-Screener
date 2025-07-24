# AI-Powered Resume Screener

A backend microservice that accepts candidate resumes in PDF format, parses them, stores structured data, and allows querying for the best matches based on a job description using Gemini embeddings and Pinecone vector search.

---

## ✅ Features  

- ✅ Upload and parse resumes in PDF format
- ✅ Extract structured data (name, email, phone, skills, experience, education)
- ✅ Store resume details in MongoDB
- ✅ Generate embeddings using LangChain + Gemini
- ✅ Store embeddings in Pinecone
- ✅ Perform similarity search for job descriptions
- ✅ Asynchronous architecture for smooth performance
- ✅ IP Whitelisting Middleware for security

---
### **Tech Stack**
- **FastAPI** – Async API framework  
- **MongoDB** – Primary database for structured data  
- **Pinecone** – Vector DB for embeddings and similarity search  
- **LangChain + Gemini** – For metadata extraction and embedding generation  
- **PyMuPDF** – For PDF text parsing
---
## ✅ Installation & Setup  

```bash
# 1 Clone the repository:
git clone https://github.com/pitkusharma/Resume-Screener.git
cd Resume-Screener

# 2 Create and activate a virtual environment:
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# 3 Install dependencies:
pip install -r requirements.txt

# 4 Configure environment variables:
Create a .env file in the root directory, .env.example file as reference:
  DB_NAME=resume_screener
  MONGO_URI=mongo_uri_string
  PINECONE_API_KEY=your_pinecone_api_key
  GOOGLE_API_KEY=your_gemini_api_key
  WHITELISTED_IPS=127.0.0.1

# 5 Run the application:
uvicorn app.main:app --reload
```

## API Endpoints Details

### 1) Upload Resume

POST /api/upload-resume

Content-Type: multipart/form-data

Body:
  file: PDF file of resume

Response:
```json
{
    "status": true,
    "message": "Resume uploaded and processing started.",
    "data": {
        "id": "68826b28a2b7c4d2a9062b06",
        "filename": "1753377576_chef resume 1.pdf"
    }
}
```

### 2) Search Resume

POST /api/search

Content-Type: application/json

Body:
```json
{
  "description": "JOB TITLE: CHEF\n\nLocation: [Specify Location]\nEmployment: Full-Time, Permanent\nPosition:\nExperience: 2+ Years\nSalary:\n\nWHAT WILL YOU DO IN YOUR NEW ROLE?\n• Prepare and cook dishes according to recipes and quality standards.\n• Plan menus and create new recipes.\n• Manage kitchen inventory and order supplies.\n• Ensure food hygiene and safety compliance.\n• Supervise and train kitchen staff.\n• Maintain a clean and organized kitchen.\n\nWHAT WE ARE LOOKING FOR?\n• 2+ years of experience as a Chef or Cook.\n• Strong knowledge of culinary techniques and food safety regulations.\n• Creativity in developing new dishes and menus.\n• Excellent time management and organizational skills.\n• Ability to lead a team and work in a fast-paced environment.\n\nWHAT WE OFFER?\n- Supportive and employee-friendly work environment.\n- Opportunities for career growth and skill development.\n- Competitive salary and performance-based incentives.\n- Staff meals and discounts.\n- Work-life balance and flexible scheduling.",
  "top_k": 5
}
```  

Response:
```json
{
    "status": true,
    "message": "Similar resumes fetched successfully.",
    "data": [
        {
            "resume_id": "68826757680c1dad4857d016",
            "filename": "1753376599_chef resume 6.pdf",
            "score": 82.34
        },
        {
            "resume_id": "68826781680c1dad4857d019",
            "filename": "1753376641_chef resume 3.pdf",
            "score": 81.68
        },
        {
            "resume_id": "68826776680c1dad4857d018",
            "filename": "1753376630_chef resume 4.pdf",
            "score": 80.81
        },
        {
            "resume_id": "68826795680c1dad4857d01b",
            "filename": "1753376661_chef resume 1.pdf",
            "score": 77.7
        },
        {
            "resume_id": "6882676c680c1dad4857d017",
            "filename": "1753376620_chef resume 5.pdf",
            "score": 77.7
        }
    ]
}
```

### 3) Get Resume

GET /api/resumes/{id}

Response:
```json
{
    "status": true,
    "message": "Resume details fetched successfully.",
    "data": {
        "id": "68826e63a2b7c4d2a9062b07",
        "filename": "1753378403_Arun Sharma 19-07-2025.pdf",
        "metadata": {
            "name": "Arun Sharma",
            "email": "xyz@gmail.com",
            "phone": "+91 1234567891",
            "skills": [
                "Python",
                "SQL",
                "Machine Learning",
                "Java",
                "JavaScript",
                "Linux",
                "Backend Development",
                "Data Analysis",
                "DevOps",
                "Linux Shell Scripting",
                "Nginx",
                "Data Analysis",
            ],
            "experience": [
                {
                    "company": "X Technologies",
                    "role": "Software Engineer",
                    "duration": "[Feb 2023 – Present]"
                },
                {
                    "company": "Y Tech",
                    "role": "Programmer Trainee",
                    "duration": "[Sep 2022 – Jan 2023]"
                }
            ],
            "education": [
                {
                    "degree": "BCA",
                    "institution": "Top College (Autonomous)",
                    "year": "2019-2022"
                }
            ]
        },
        "uploaded_at": "2025-07-24T23:03:23.934000"
    }
}
```

## Security
IP Whitelisting Middleware: Only requests from specified IPs in WHITELISTED_IPS will be allowed.

## License
MIT License
