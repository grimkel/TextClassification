import re

from functools import reduce
from collections.abc import Callable


from spellchecker import SpellChecker


target_names = ['alt.atheism',
                 'comp.graphics',
                 'comp.os.ms-windows.misc',
                 'comp.sys.ibm.pc.hardware',
                 'comp.sys.mac.hardware',
                 'comp.windows.x',
                 'misc.forsale',
                 'rec.autos',
                 'rec.motorcycles',
                 'rec.sport.baseball',
                 'rec.sport.hockey',
                 'sci.crypt',
                 'sci.electronics',
                 'sci.med',
                 'sci.space',
                 'soc.religion.christian',
                 'talk.politics.guns',
                 'talk.politics.mideast',
                 'talk.politics.misc',
                 'talk.religion.misc']


# Функция принимает:
# список полей fieldTitles - список ключевых слов с которых начинаются поля
# sep - сепаратор, символ окончания поля,
# в данном случае каждое поле в датасете заканчивается символом новой строки \n
# text - сам текст одного вхождения данных
def removeFields(text: str) -> str:

    # Выделение поля - набора символов алфоовита и цифр
    # а так же служебных символов . -
    regex = "[A-Za-z.-0-9]+:.*\n"
    # Удаление полдстроки/замена на пустую подстроку
    text = re.sub(regex, '', text)

    return text

# Функция принимает:
# text - текст одного вхождения данных
def specialCharacterCleaner(text: str) -> str:

    startText = text
    # Удаление апострофов используется для слов тиках как:
    # can't wouldn't и т.д.
    text = re.sub("'t", " not", text)
    text = re.sub("\'re", " are", text)
    text = re.sub("'s", " is", text)
    text = re.sub("'d", " would", text)
    text = re.sub("'ll", " will", text)
    text = re.sub("'ve", " have", text)
    text = re.sub("'m", " am", text)

    # Выделение переходов на новую строку и дубликатов пробелов
    regex = "[\r\n\t\\s]+"
    # Замена выделенных подстрок на единый символ разделения ' '
    text = re.sub(regex, ' ', text)

    # Выделение пробела в начале строки
    regex = "^\\s"
    # замена на пустую строку
    text = re.sub(regex, '', text)

    # Некоторые данные пустые или же крайне малы
    # Например:
    #
    # From: xchen@vax2.concordia.ca (CHEN, XIA)
    # Subject: how
    # News-Software: VAX/VMS VNEWS 1.41
    # Nntp-Posting-Host: vax2.concordia.ca
    # Organization: Concordia University
    # Lines: 0
    #
    if len(text) < 5:
        return None

    # Удаление спецсимволов внутри слов
    resText = text[0]  # Отфильтрованная строка
    for i in range(1, len(text)):

        match text[i]:

            # Удаление спецсимволов являющихся частью слова
            # (считаю что если точка не в конце слова,
            # то является его частью например -
            # .net или shelley.u.washington.edu)
            case '.' | '-':

                nextIsLetter = False
                # Является ли текущий символ не последним в строке
                if i < len(text) - 1:
                    # Является ли след символ частью слова
                    nextIsLetter = text[i+1].isalpha()

                # Находится ли точка внутри слова
                if nextIsLetter:
                    # замена точки на разделение слов
                    resText += ' '
                else:
                    resText += text[i]

            # Любые иные символы записываются без изменений
            case _:
                resText += text[i]

    # Присвоение нового тескта
    text = resText
    # Удаление дубликата
    del resText

    # Выделение спецсимволов не являющихся символами пунктуации
    regex = "[^\\w 0-9.!?,]"
    # Замена на пустую строку
    text = re.sub(regex, '', text)

    # Замена двух и более символов пунктуации одним
    # ... -> .
    regex = "[.]{2,}"  # Выделение подстрок из 2 и более точек
    text = re.sub(regex, '.', text)  # Замена на одну точку
    # !!! -> !
    regex = "[!]{2,}"
    text = re.sub(regex, '!', text)
    # ??? -> ?
    regex = "[?]{2,}"
    text = re.sub(regex, '?', text)
    # ,,, -> ,
    regex = "[,]{2,}"
    text = re.sub(regex, ',', text)

    # Обрамление символов пунктуации пробелами
    # для послдеющего выделения их как отдельных слов - токенов
    text = re.sub('[.]', " . ", text)
    text = re.sub('[!]', " ! ", text)
    text = re.sub('[?]', " ? ", text)
    text = re.sub('[,]', " , ", text)

    # Замена дублиактов пробелов

    # Выделение подстрок состоящих из двух и более пробелов
    regex = " {2,}"
    # Замена выделенных подстрок на единичные пробелы
    text = re.sub(regex, ' ', text)
    return text


# Примнимает лист слов words
# Лист слов с коррекциями если нужны
def spellCheck(words: list[str]) -> list[str]:

    # Загрузка спеллчекера
    spell = SpellChecker(language="en")

    # Корректировка слов
    # если слово распознано как несуществующее возвращается None
    correctedWords = [spell.correction(word) for word in words]
    # None исключается из текста
    correctedWords = [word for word in correctedWords if word is not None]
    return correctedWords


# Функция разбиения текста слова/токены
def splitText(text: str) -> list:
    return text.split()


# Объединение листа слов words в одну строку
# для последующей обработки tf-idf sklearn
# нужна при исользовании спеллчекера
def list2str(words: list[str]) -> str:
    return " ".join(words)


# Композиция нескольких функций
# fs - функции для составления композиции/пайплайна
def compose(*fs: tuple[Callable, ...]) -> Callable:

    # Композиция двух функций f, g
    # Возращаемый тип неизвестен, зависит от последней функции в композиции
    def compose2(f: Callable, g: Callable):
        return lambda x: f(g(x))

    # Построение самой композиции при помощи reduce
    composite_fn = reduce(compose2, fs, lambda x: x)
    return composite_fn


# Построение пайплайна без сплеллчека/проверки орфографии.
preprocess = compose(specialCharacterCleaner,
                     removeFields)


# Построение пайплайна с проверкой орфографии.
preprocessSpell = compose(list2str,
                          spellCheck,
                          splitText,
                          specialCharacterCleaner,
                          removeFields)