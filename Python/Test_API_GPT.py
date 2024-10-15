import openai

openai.api_key = ''


nome_do_usuario = input("Por favor, digite seu nome: ")

# loop chatbot
while True:
    # usuário mensagem
    user_input = input(f"{nome_do_usuario}: ")

    # sair do loop
    if user_input.lower() == 'sair':
        break

    # array de mensagens
    messages = [
        {"role": "system", "content": "Você é um assistente útil."},
        {"role": "user", "content": user_input}
    ]

    # prompt para o GPT-4
    response = openai.ChatCompletion.create(
        model = 'gpt-4-turbo',
        messages=messages,
        max_tokens=50
    )

    # do chatbot da resposta do GPT-4 e a exibe
    chatbot_reply = response['choices'][0]['message']['content'].strip()
    print(f"ChatGPT: {chatbot_reply}")
