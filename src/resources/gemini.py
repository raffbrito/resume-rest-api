import os
import uuid
import boto3
import requests
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import request, jsonify
from flask_jwt_extended import jwt_required

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('RESUME_QUESTIONS_TABLE', 'resume_questions'))

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def get_resume_text():
    resume_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../resume.txt"))
    if not os.path.exists(resume_path):
        return "Resume not found."
    with open(resume_path, "r") as f:
        return f.read()

def gemini_api_call(question):
    resume_text = get_resume_text()
    prompt = f"Please answer the following question based only on the resume below. If question is not related to the resume, career, work experience, skills, please say 'I don't know'.\n\n{resume_text}\n\nQuestion: {question}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    print("Prompt sent to Gemini:", prompt)
    response = requests.post(
        f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
        headers=headers,
        json=payload
    )
    response.raise_for_status()
    data = response.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]

blp = Blueprint("AI", "ai", description="Resume Q&A with AI")

@blp.route("/ask-ai")
class ResumeQuestion(MethodView):
    @jwt_required()
    def post(self):
        data = request.get_json()
        question = data.get("question")
        if not question:
            abort(400, message="Question is required.")
        request_id = str(uuid.uuid4())
        try:
            answer = gemini_api_call(question)
        except Exception as e:
            abort(500, message=f"AI API error: {str(e)}")
        item = {
            "id": f"REQUEST#{request_id}",
            "question": question,
            "answer": answer,
            "status": "complete"
        }
        table.put_item(Item=item)
        return {"requestID": request_id}, 201

@blp.route("/ask-ai/<string:request_id>")
class ResumeQuestionResult(MethodView):
    @jwt_required()
    def get(self, request_id):
        response = table.get_item(Key={"id": f"REQUEST#{request_id}"})
        item = response.get("Item")
        if not item:
            abort(404, message="Request not found.")
        return {"question": item["question"], "answer": item["answer"], "status": item["status"]}
