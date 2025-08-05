import os
import json
import openai

openai.api_key = os.environ['OPENAI_API_KEY']

SYSTEM_PROMPT = (
    "You are a helpful assistant for Ian Cahall's resume website. "
    "Only answer questions about Ian Cahall's professional experience, education, skills, and projects. "
    "If asked about anything else, politely decline."
)

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        user_message = body.get('message', '')

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            max_tokens=300,
            temperature=0.2
        )
        reply = response['choices'][0]['message']['content']
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': 'https://ian-cahall-resume.com',
                'Access-Control-Allow-Methods': 'POST,OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'reply': reply})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': 'https://ian-cahall-resume.com',
                'Access-Control-Allow-Methods': 'POST,OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'reply': "Sorry, I couldn't process that."})
        }