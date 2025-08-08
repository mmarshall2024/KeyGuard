
import openai, os
openai.api_key = os.getenv("OPENAI_API_KEY")
def omni_logic_core(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are OMNI, an immortal AI business empire assistant."},
                  {"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']
