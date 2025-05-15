from flask import Flask, render_template, request
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
openai_api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=openai_api_key)
def translate(text, target_lang='en', src_lang='ko'):
    if not text.strip():
        return ''
    prompt = f'다음 문장을 {src_lang}에서 {target_lang}로 번역해 주세요.\n문장: {text}'
    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )
    return response.output_text.strip()

@app.route('/', methods=['GET', 'POST'])
def index():
    translated = ''
    text = ''
    src_lang = 'ko'
    lang = 'en'
    if request.method == 'POST':
        text = request.form['text']
        src_lang = request.form['src_lang']
        lang = request.form['lang']
        translated = translate(text, lang, src_lang)
    return render_template('index.html', translated=translated, text=text, src_lang=src_lang, lang=lang)

if __name__ == '__main__':
    app.run(debug=True) 