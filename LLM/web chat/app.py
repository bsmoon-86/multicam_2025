import os
from flask import Flask, request, jsonify, Response, render_template
from google import genai

app = Flask(__name__)
client = genai.Client(api_key='AIzaSyAztfQPjLw1Rdn8E6haeiQUtOS_xRELHAs')

MODEL = "gemini-2.5-flash"

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.post("/api/chat")
def chat():
    data = request.get_json(force=True)
    user_text = (data.get("message") or "").strip()

    # (선택) 간단한 시스템 지시문
    prompt = f"너는 친절한 한국어 챗봇이다.\n사용자: {user_text}\n답변:"

    resp = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )
    return jsonify({"text": resp.text})


@app.get("/api/stream")
def stream():
    # SSE: /api/stream?message=...
    user_text = (request.args.get("message") or "").strip()
    prompt = f"너는 친절한 한국어 챗봇이다.\n사용자: {user_text}\n답변:"

    def gen():
        # SSE 헤더는 Response에서 설정하고, 여기서는 data: 라인만 쏴줌
        for chunk in client.models.generate_content_stream(model=MODEL, contents=prompt):
            if getattr(chunk, "text", None):
                # SSE 규격: "data: ..." + "\n\n"
                yield f"data: {chunk.text}\n\n"
        yield "data: [DONE]\n\n"

    return Response(gen(), mimetype="text/event-stream")

app.run(debug=True)