import vertexai
from vertexai.generative_models import GenerativeModel
  
def generate():
  vertexai.init(project="gen-lang-client-0259041665", location="us-central1")
  model = GenerativeModel(
    "gemini-1.5-flash-001",
  )
  responses = model.generate_content(
      ["""what is the capital of india"""],
      generation_config=generation_config,
      stream=True
  )

  for response in responses:
    print(response.text, end="")


generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}
 

generate()
