import os

from flask import Flask, render_template, request

from util.preprocess import getText

from classifier.classifier import SVCmodel

app = Flask(__name__)

svc = SVCmodel("./classifier/SVC")

# Принятие файла с фронтенда и ответ классом документа
@app.route("/predict",  methods=['POST'])
def predict():

    # Проверка что файл был передан
    if 'file' not in request.files:
        return 'No file provided'
    
    # Ответ сервера
    output = "-"

    try:
        # Сохранение файла
        file = request.files['file']
        file.save("temp.pdf")

        # Является ли файл валидным pdf
        valid = True
        text = None
        try:
            text = getText("temp.pdf")
        except:
            valid = False
            output = "invalid file"

        # Если файл валидный то он классифицируется
        if valid:
            output = svc.transform(text)

    # Обработка иных ошибок
    except:
        output = "unexpected error"
    # Удаление файла в случае непредвиденной ошибки
    finally:
        os.remove("temp.pdf")

    return output

# Основная страница с формой для классификации документов
@app.route("/")
def mainpage():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, Debug=True)