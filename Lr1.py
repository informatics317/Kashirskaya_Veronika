from fuzzywuzzy import fuzz
from Levenshtein import ratio
import docx
from time import time
from logging import*
basicConfig(level=DEBUG,filename='Time.log',filemode='w',format="%(asctime)s %(levelname)s %(message)s")

def reader_docx(x):
    doc = docx.Document(x)
    text = []
    for paragraphs in doc.paragraphs:
        text.append(paragraphs.text)
    return '\n'.join(text)


text1 = reader_docx('Рыбалка1.docx')
text2 = reader_docx('Рыбалка2.docx')


def levenstein(str_1, str_2):
    n, m = len(str_1), len(str_2)
    if n > m:
        str_1, str_2 = str_2, str_1
        n, m = m, n

    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if str_1[j - 1] != str_2[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]


'''Библиотека fuzzywuzzy'''
start_fuzzywuzzy = time()
info('The beginning of fuzzywuzzy')
distance_fuzzywuzzy = fuzz.ratio(text1, text2)
print(f"Расстояние Левенштейна через библиотеку  fuzzywuzzy: {distance_fuzzywuzzy}")
finish_fuzzywuzzy = time()
info(f'The end of fuzzywuzzy. Time work = {finish_fuzzywuzzy-start_fuzzywuzzy}')

'''Библиотека Levenshtein'''
start_Levenshtein = time()
info('The beginning of Levenshtein')
distance_Levenshtein = ratio(text1, text2)
print(f"Расстояние Левенштейна через библиотеку Levenstein: {distance_Levenshtein}")
finish_Levenshtein = time()
info(f'The end of Levenshtein. Time work = {finish_Levenshtein-start_Levenshtein}')

'''Функция levenstein'''
start_levenshtein_f = time()
info('The beginning of levenstein')
print(f"Расстояние Левенштейна с помощью функции: {levenstein(text1, text2)}")
finish_levenshtein_f = time()
info(f'The end of levenstein . Time work = {finish_levenshtein_f-start_levenshtein_f}')
