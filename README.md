# AI Explainer Backend

A FastAPI-based backend service that provides intelligent text explanation capabilities using Google's Gemini AI model. This service can explain complex concepts in different modes (simple, detailed, technical) and supports multiple languages.

## 🚀 Features

- **Multiple Explanation Modes**: Choose from simple, detailed, or technical explanations
- **Multi-language Support**: Get explanations in your preferred language
- **Customizable Length**: Control the length of explanations with token limits
- **RESTful API**: Clean and intuitive API endpoints
- **CORS Enabled**: Ready for frontend integration
- **Health Check**: Built-in health monitoring endpoint

## 🛠️ Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Google Gemini AI**: Advanced language model for intelligent explanations
- **LangChain**: Framework for building LLM-powered applications
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for running FastAPI applications

## 📋 Prerequisites

- Python 3.8 or higher
- Google AI API key (Gemini)

## 🔧 Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd AI-Explainer-Backend
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:

   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```

   To get a Google API key:

   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy the key to your `.env` file

## 🚀 Running the Application

### Development Mode

```bash
python main.py
```

The server will start at `http://localhost:8000`

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 📚 API Documentation

Once the server is running, you can access:

- **Interactive API Docs**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`

## 🔌 API Endpoints

### POST `/api/explain`

Explains the provided text according to specified parameters.

**Request Body:**

```json
{
  "text": "String to explain",
  "language": "english", // Optional, default: "english"
  "maxLen": 1024, // Optional, default: 1024
  "explanationMode": "simple" // Optional, default: "simple"
}
```

**Explanation Modes:**

- `simple`: Beginner-friendly explanations
- `detailed`: Comprehensive explanations with examples
- `technical`: In-depth technical analysis

**Response:**

```json
{
  "success": true,
  "content": {
    "explanation": "Generated explanation text"
  }
}
```

### GET `/health`

Health check endpoint to verify service status.

**Response:**

```json
{
  "status": "healthy"
}
```

## 💡 Usage Examples

### Using curl

**Simple explanation:**

```bash
curl -X POST "http://localhost:8000/api/explain" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "What is machine learning?",
    "explanationMode": "simple",
    "maxLen": 500
  }'
```

**Detailed explanation in Spanish:**

```bash
curl -X POST "http://localhost:8000/api/explain" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Explain quantum computing",
    "language": "spanish",
    "explanationMode": "detailed",
    "maxLen": 1024
  }'
```

### Using Python

```python
import requests

url = "http://localhost:8000/api/explain"
data = {
    "text": "What is blockchain technology?",
    "explanationMode": "technical",
    "maxLen": 800
}

response = requests.post(url, json=data)
result = response.json()
print(result["content"]["explanation"])
```

## 🔒 Environment Variables

| Variable         | Description                       | Required |
| ---------------- | --------------------------------- | -------- |
| `GOOGLE_API_KEY` | Your Google AI API key for Gemini | Yes      |

## 🏗️ Project Structure

```
AI-Explainer-Backend/
├── main.py              # FastAPI application and endpoints
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create this)
└── README.md           # This file
```
