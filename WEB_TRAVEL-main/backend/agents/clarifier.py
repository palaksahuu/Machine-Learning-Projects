from langchain.prompts import ChatPromptTemplate
import google.generativeai as genai
import os

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

clarification_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a travel assistant. When user provides:
{draft_input}, identify missing/ambiguous info from: 
1. Exact dates 2. Budget range 3. Activity types 
Ask ONE most critical question to clarify."""),
])

async def clarify_inputs(request):
    if any(word in request.preferences.lower() for word in ["mix", "some", "variety"]):
        model = genai.GenerativeModel("gemini-1.5-pro-latest")  # ✅ Updated model

        formatted_prompt = clarification_prompt.format_messages(draft_input=request.preferences)  
        response = model.generate_content(formatted_prompt[0].content)  # ✅ Extract text from prompt

        return {"requires_clarification": getattr(response, "text", "No clarification needed")}
    
    return request
