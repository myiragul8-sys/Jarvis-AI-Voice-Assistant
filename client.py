from openai import OpenAI
client=OpenAI(api_key="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")
completion=client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role":"system","content":"you are virtual assistance named jarvis skilled in general tasks like alexa and google cloud"},
              {"role":"user","content":"what is coding"}]
)
print(completion.choices[0].message.content)