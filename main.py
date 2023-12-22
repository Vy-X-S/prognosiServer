from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os

import json

app = FastAPI()
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

sample_request = {
    "session_id": "123e4567-e89b-12d3-a456-426614174000",
    "clinic_id": "CL-1001", 
    "user_id": "USR-5002", 
    "patient_id": "PAT-3021",
    "patient_symptoms": [ 
      {
        "symptom_id": "SYM-001",
        "symptom_name": "Fever"
      },
      {
        "symptom_id": "SYM-002",
        "symptom_name": "Cough"
      }
    ],
    "doctor_id": "DR-2031",
    "date": "2023-12-19",
    "treatment": "Rest, increased fluid intake, and paracetamol for fever.",
    "tx_id": "TX-1010"
  }


@app.post("/call") # this will make call to OpenAI API
async def call_openai_api(data: dict):
  api_key = os.environ["OPENAI_API_KEY"]
  client = OpenAI(api_key = api_key)
  
  prompt = f"Generate a medical treatment proposal based on the following data: {data}"
  
  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages= [
      {"role": "system", "content": "You are a medical assistant. You create medical documents based on treatment proposal data. "},
      {"role": "user", "content": prompt}
    ]
  )
  
  return response.choices[0].message.content

@app.get("/")
def test():
  return {"Hello": "Test2"}