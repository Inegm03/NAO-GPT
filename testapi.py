import openai

openai.api_key = ""

def generate_response(user_input):
    messages = [
        {"role": "system", "content": "Answer in one sentence of 3 words"},
        {"role": "user", "content": user_input},
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=60,
        temperature=0.7
    )

    reply = response['choices'][0]['message']['content']
    return reply


file_path3 = "text1.txt"  # Replace 'path_to_save' with the correct directory

# Open the file in read mode and read its content
with open(file_path3, "r") as file:
    transcription_content = file.read()

# Display or use the retrieved transcription content
text2=generate_response(transcription_content)

file_path4 = "text2.txt"  # Replace 'path_to_save' with your desired directory

# Open a file in write mode and save the transcription
with open(file_path4, "w") as file:
    file.write(text2)
