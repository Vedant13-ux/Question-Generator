from logging import debug
from flask import Flask, request, jsonify
from model import glossary, mcq, subjective, summary, true_false

# Initializing the Flask Application 
app=Flask(__name__)


@app.route('/summarize', methods=["POST"])
def get_summary(min_length=20, max_length=500, ratio=0.6):
    if request.form.get("params"):
        max_length=request.form['params']['max_length']
        min_length=request.form['params']['min_length']
        ratio=request.form['params']['ratio']

    summarized = summary.get_summary(request.form['text'], min_length, max_length, ratio)
    return jsonify({"summary": summarized})


@app.route('/glossary', methods=["POST"])
def get_glossary(numer_of_words=20):
    text=request.form['text']
    if(request.form.get("number_of_words")):
        numer_of_words=request.form["number_of_words"]

    glossary_data=glossary.get_glossary(text,numer_of_words )
    print(glossary_data)
    return jsonify({"glossary":glossary_data})


@app.route('/true_false', methods=["POST"])
def get_true_false(number_of_questions=10):
    text=request.form["text"]
    questions= true_false.generate_true_false(text, 10)
    return jsonify({"questions_true_false":questions})
    

@app.route('/mcq', methods=["POST"])
def get_mcq(number_of_questions=10):
    text=request.form["text"]
    questions= mcq.generate_questions(text,int(number_of_questions),True)
    return jsonify({"questions_mcq_fib":questions})
            

if __name__=="__main__":
    app.run(debug=True)


