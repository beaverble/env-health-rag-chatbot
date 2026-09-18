from openai import OpenAI
client = OpenAI(api_key="foobar", base_url="http://HOST:PORT/v1/")

def pred_data(system_prompt, input_prompt):
    messages = []
    messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": input_prompt})

    completion = client.chat.completions.create(
        model="llama3.3",
        messages=messages,
        max_tokens=500,
        frequency_penalty=0.5,
        top_p=0.2,
        temperature=0.1,
    )
    resp = completion.to_json()
    return resp
