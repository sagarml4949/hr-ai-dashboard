from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from langchain_groq import ChatGroq
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import os 

app = FastAPI()

# Allow the HTML frontend to talk to this Python server securely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Load the Dataset
try:
    hr_data = pd.read_csv('HRMLprediction.csv')
    print(f"Data loaded successfully: {len(hr_data)} rows.")
except FileNotFoundError:
    print("Error: HRMLprediction.csv not found in the directory.")
    hr_data = pd.DataFrame()

# 2. Configure the AI Agent
# --- SECURITY UPDATE ---
# We use os.getenv so the cloud provider can securely inject the key.
# This prevents bots from stealing your key off GitHub.
GROQ_API_KEY = os.getenv("GROQ_API_KEY") 

try:
    llm = ChatGroq(model="mixtral-8x7b-32768", api_key=GROQ_API_KEY, temperature=0)
    agent = create_pandas_dataframe_agent(llm, hr_data, verbose=False, allow_dangerous_code=True, handle_parsing_errors=True)
except Exception as e:
    print("Agent setup failed. Check your API key.", e)
    agent = None

# 3. Define Communication Schemas & Memory Buffer
class ChatRequest(BaseModel):
    prompt: str

# This list acts as our AI's short-term memory
conversation_memory = []

# 4. API Endpoint 1: The Chat Agent with Conversational Memory and Error Fallback
@app.post("/chat")
def chat_with_agent(request: ChatRequest):
    global conversation_memory

    if not agent:
        return {"response": "Error: AI Agent is not initialized. Check the API key.", "status": "error"}
    
    try:
        # Step A: Build the context from our memory buffer
        context = "Previous Conversation History:\n"
        for turn in conversation_memory:
            context += f"User: {turn['user']}\nAI: {turn['ai']}\n"
        
        # Step B: Prompt with stricter formatting rules
        full_prompt = f"""
        {context}
        
        Current Question: {request.prompt}
        
        Instructions: Answer the Current Question using the pandas dataframe. 
        If the question uses pronouns, refer to the Conversation History.
        CRITICAL: When you are ready to answer, you MUST use the exact prefix "Final Answer: ".
        """
        
        # Step C: Ask the agent
        result = agent.invoke({"input": full_prompt})
        final_answer = str(result["output"])
        
    except Exception as e:
        error_msg = str(e)
        # THE FIX: Graceful Fallback for LLM Formatting Rebellions
        if "Could not parse LLM output:" in error_msg:
            try:
                # We manually extract the AI's thought process out of the crash log!
                extracted_answer = error_msg.split("`")[1]
                extracted_answer = extracted_answer.replace("Thought:", "").replace("Action: None", "").strip()
                final_answer = extracted_answer
            except IndexError:
                return {"response": "System Error: The AI returned an unreadable format. Please try rephrasing.", "status": "error"}
        else:
            return {"response": f"System Error: {error_msg}", "status": "error"}

    # Step D: Save this interaction to memory
    conversation_memory.append({"user": request.prompt, "ai": final_answer})
    
    # Keep memory clean: Only remember the last 3 interactions to preserve speed
    if len(conversation_memory) > 3:
        conversation_memory.pop(0)

    return {"response": final_answer, "status": "success"}

# 5. API Endpoint 2: The 3D Engine Data Feeder
@app.get("/data")
def get_3d_data():
    if hr_data.empty:
        return {"data": []}
    sample = hr_data.sample(n=min(3000, len(hr_data)), random_state=42)
    subset = sample[['satisfaction_level', 'last_evaluation', 'average_montly_hours', 'left']]
    return {"data": subset.to_dict(orient='records')}