import google.generativeai as genai
API_KEY = ''

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

# nome do usuário
nome_do_usuario = input("Por favor, digite seu nome: ")

# loop de conversas
while True:
    # mensagem do usuário
    user_input = input(f"{nome_do_usuario}: ")

    # parada
    if user_input.lower() == 'sair':
        break

    # prompt Gemini
    prompt = f"""
     voce é assistente virtual inteligente.
    a pessoa se chama: {nome_do_usuario} e ela te perguntou: {user_input}
    responda de forma completa e informativa.
    """

    # gerando resposta do Gemini
    response = model.generate_content(prompt)

    # resposta
    print(f"Gemini: {response.text}")

