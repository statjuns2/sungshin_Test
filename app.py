from flask import Flask, render_template, request, session, redirect, url_for
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "your-secret-key")

def get_client():
    api_key = session.get("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)

def translate(text, target_lang='en', src_lang='ko'):
    if not text.strip():
        return ''
    client = get_client()
    if not client:
        return 'API 키가 필요합니다.'
    prompt = f'다음 문장을 {src_lang}에서 {target_lang}로 번역해 주세요. 번역결과만 출력해. \n문장: {text}, 번역결과: '
    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )
    return response.output_text.strip()

@app.route('/set_api_key', methods=['GET', 'POST'])
def set_api_key():
    if request.method == 'POST':
        session['OPENAI_API_KEY'] = request.form['api_key']
        return redirect(url_for('index'))
    return render_template('set_api_key.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if not session.get('OPENAI_API_KEY'):
        return redirect(url_for('set_api_key'))
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