import google.generativeai as genai

genai.configure(api_key="AIzaSyCGWY9swGxwkpdlnYupvVWs2VOdMhpoD38")

models = genai.list_models()

for model in models:
    print(model.name, "-", model.supported_generation_methods)
