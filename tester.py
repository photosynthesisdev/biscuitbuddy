from vertexai.generative_models import GenerativeModel

model = GenerativeModel(
    "gemini-1.0-pro-002",
    system_instruction=[
        "Don't use technical terms in your response",
    ],
    api_key = ''
)
print(model.generate_content("Explain gravity"))