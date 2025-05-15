import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Dict, Any, Optional

# Set the Google API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyA7e3kHqlBC6Liec9wRunVhlkL-OJEGJNQ"

# Create the FastAPI app
app = FastAPI(title="AI Text Explainer API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Define request model with the new fields


class ExplanationRequest(BaseModel):
    text: str
    language: Optional[str] = "english"  # Default language
    maxLen: Optional[int] = 1024  # Default max length
    explanationMode: Optional[str] = "simple"  # Default explanation mode

# Define response model


class ExplanationResponse(BaseModel):
    success: bool
    content: Dict[str, Any]


# Initialize the Gemini model
model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.3,
)


@app.post("/api/explain", response_model=ExplanationResponse)
async def explain_text(request: ExplanationRequest):
    try:
        # Create a prompt for the model based on the explanation mode
        from langchain_core.messages import SystemMessage, HumanMessage

        # Adjust the system prompt based on explanationMode
        system_content = "You are an educational AI assistant that explains complex concepts."

        if request.explanationMode == "simple":
            system_content = "You are an educational AI assistant that explains complex concepts in simple terms, as if explaining to a beginner."
        elif request.explanationMode == "detailed":
            system_content = "You are an educational AI assistant that provides detailed explanations with examples and context."
        elif request.explanationMode == "technical":
            system_content = "You are an educational AI assistant that explains concepts technically, using proper terminology and in-depth analysis."

        # Add language instruction and token length guidance
        max_len_guidance = ""
        if request.maxLen and request.maxLen < 500:
            max_len_guidance = (
                f" Your response should be concise and around {request.maxLen} tokens in length, "
                f"but ALWAYS complete your sentences. It's better to be slightly under the token limit "
                f"with complete sentences than to be cut off mid-sentence. If the token limit is very small, "
                f"provide a brief but complete explanation."
            )

        language_instruction = f"Respond in {request.language}.{max_len_guidance}"
        system_content += " " + language_instruction

        messages = [
            SystemMessage(content=system_content),
            HumanMessage(
                content=f"Please explain the following text according to the requested mode. Focus on making the key ideas accessible within approximately {request.maxLen} tokens, ensuring you complete all sentences: {request.text}")
        ]

        # Configure model with max tokens (with a small buffer to complete sentences)
        # Adding a small buffer to allow for sentence completion
        # 15% buffer or max 100 tokens
        buffer = min(100, int(request.maxLen * 0.15))
        model.max_output_tokens = request.maxLen + buffer

        # Get explanation from the model
        response = model.invoke(messages)

        # Return the response
        return ExplanationResponse(
            success=True,
            content={
                "explanation": response.content
            }
        )
    except Exception as e:
        # Print the error for debugging
        import traceback
        print(f"Error: {str(e)}")
        print(traceback.format_exc())

        raise HTTPException(
            status_code=500, detail=f"Error generating explanation: {str(e)}")

# Health check endpoint


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
