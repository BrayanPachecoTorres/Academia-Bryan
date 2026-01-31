from transformers import AutoModelForCausalLM, AutoTokenizer

# Modelo ligero
model_name = "distilgpt2"

# Descargar y cargar el modelo + tokenizer
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Texto de prueba
inputs = tokenizer("Hola Brayan, dame un consejo de ajedrez:", return_tensors="pt")

# Generar respuesta
outputs = model.generate(**inputs, max_length=100, temperature=0.7)
print(tokenizer.decode(outputs[0]))
