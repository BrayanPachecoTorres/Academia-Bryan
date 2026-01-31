from django.shortcuts import render
from transformers import AutoModelForCausalLM, AutoTokenizer

# Cargar el modelo una sola vez
model_name = "distilgpt2"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

def chat_ia(request):
    respuesta = ""
    if request.method == "POST":
        pregunta = request.POST.get("pregunta")
        inputs = tokenizer(pregunta, return_tensors="pt")
        outputs = model.generate(**inputs, max_length=100, temperature=0.7)
        respuesta = tokenizer.decode(outputs[0])
    return render(request, "ia/chat.html", {"respuesta": respuesta})
