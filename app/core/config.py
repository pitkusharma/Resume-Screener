import os
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

# Central configurations
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
MAX_FILE_SIZE_MB = 5

# Ensure upload folder exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initializing llm
llm = ChatGoogleGenerativeAI(
    model='gemini-2.0-flash',
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0
)

# Get IP list from env and split into set
WHITELISTED_IPS = set(os.getenv("WHITELISTED_IPS", "").split(","))