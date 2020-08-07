# -*- coding: utf-8 -*-
import re
from transliterate import translit as _translit


ALPHABET = 'абвгдеёжзийклмнпорстуфхцчшщъыьэюя'
VOWELS = 'аеёиоуыэюя'
VOWELS_YOTIZED = {'е': 'э', 'и': 'ы', 'ё': 'о', 'ю': 'у', 'я': 'а'}
SONANTS = 'бвгджзлмнр'
CONSONANTS_VOICED = {'б': 'п', 'в': 'ф', 'г': 'к', 'д': 'т', 'ж': 'ш', 'з': 'с'}
CONSONANTS_VOICED_REV = {y: x for x, y in CONSONANTS_VOICED.items()}
CONSONANTS_UNVOICED = 'кпстфхцчшщ'
NOSOFT = 'йцчшщ'
NOPHO = 'ъь'
SND_REPLACE = {
    r'й[ая]': r'я',
    r'й[эе]': r'е',
    r'й[оё]': r'ё',
    r'й[ую]': r'ю',
    r'вств': r'ств',
    r'дск': r'цк',
    r'здн': r'зн',
    r'зч': r'щ',
    r'лнц': r'нц',
    r'ндц': r'нц',
    r'нтск': r'нск',
    r'рдц': r'рц',
    r'cдн': r'cн',
    r'стск': r'сцк',
    r'стьд': r'зд',
    r'стьс': r'сс',
    r'сч': r'щ',
    r'т\ь?ся\b': r'ца',
    r'((?!\b.).)гого\b': r'\1гово',
    r'((?!(?:\b|на|не|пре|при|супер|мега|квази)м).+)ного\b': r'\1ново',
    r'([ежносцчшщь])его\b': r'\1ево',
    r'([вкмптсхш])ого\b': r'\1ово',
    r'что\b': r'што',
    r'\bего\b': r'ево'
}

re_latin_chars = re.compile(r'[A-Za-z]')

def translit(text):
    if re_latin_chars.search(text):
        text = _translit(text, 'ru') 
    return text

def get_syllables(text, lower=True):
    if lower:
        text = text.lower()
    text = translit(text)
    syls = []
    syl = ''
    next_syl = ''
    has_vowel = False
    for c in text:
        if c == "'":
            if next_syl and next_syl[-1] != "'":
                next_syl += c
        elif c.lower() in NOPHO or c.lower() not in ALPHABET:
            if syl:
                syl += next_syl
                if c.lower() in NOPHO:
                    syl += c
                syls.append(syl)
                syl = next_syl = ''
                has_vowel = False
        elif c.lower() in VOWELS:
            if has_vowel:
                i_ = -2 if next_syl.endswith("'") else -1
                syl += next_syl[:i_]
                syls.append(syl)
                syl = next_syl[i_:] + c
                next_syl = ''
            else:
                syl += c
                has_vowel = True
        else:
            if has_vowel:
                syl += next_syl
                next_syl = c
            else:
                syl += c
    if syl:
        syls.append(syl + next_syl)
    return syls

def phonetize(text, syllables=True):
    text = translit(text)
    text = text.lower().replace("'", 'ъ')
    for snd, rep in SND_REPLACE.items():
        text = re.sub(snd, rep, text)
    text = get_syllables(re.sub('[^{}]'.format(ALPHABET), '', text),
                         lower=False)
    text_pho = []
    prev_c = ''
    for syl in text:
        syl_pho = ''
        if prev_c:
            if syl[0] in CONSONANTS_UNVOICED:
                for c_ in prev_c:
                    syl_pho += CONSONANTS_VOICED.get(c_, c_)
            else:
                syl_pho = prev_c
            text_pho[-1] += syl_pho
            prev_c = syl_pho = ''
        for c in syl:
            # новый слог
            if not prev_c:
                # выставляем предыдущий символ; слог пока пустой
                if c not in NOPHO:
                    prev_c = c
            # если гласная [еёиюя]
            elif c in VOWELS_YOTIZED:
                # добавляем предыдущей согласной мягкость и помещаем
                # предыдущие согласные в слог
                if prev_c[-1] not in NOSOFT:
                    prev_c += "'"
                syl_pho += prev_c
                # меняем пришедшую гласную на [эоыуа] и помещаем
                # в предыдущий символ
                prev_c = VOWELS_YOTIZED[c]
            # если другая гласная
            elif c in VOWELS:
                # помещаем предыдущие согласные в слог, а пришедшую
                # гласную - в предыдущий символ
                syl_pho += prev_c
                prev_c = c
            # если звонкая согласная
            elif c in SONANTS:
                # помещаем предыдущую гласную в слог, а пришедшую
                # согласную - в предыдущий символ
                if prev_c[-1] in VOWELS:
                    syl_pho += prev_c
                    prev_c = ''
                elif c != 'в' and c in CONSONANTS_VOICED:
                    prev_c = prev_c[:-1] \
                           + CONSONANTS_VOICED_REV.get(prev_c[-1], prev_c[-1])
                prev_c += c
            # если [ъь]
            elif c in NOPHO:
                # если мягкий знак, то смягчаем все глухие звуки
                # перед ним
                if c == 'ь' and prev_c[-1] not in VOWELS:
                    prev_c_, need_soft = '', True
                    for c_ in reversed(prev_c):
                        if c_ in NOSOFT or c_ == "'":
                            prev_c_ += c_
                        elif need_soft and c_ in CONSONANTS_UNVOICED:
                            prev_c_ += "'" + c_
                        else:
                            prev_c_ += c_
                            need_soft = False
                    prev_c = ''.join(reversed(prev_c_))
                    if prev_c[-1] in SONANTS:
                        prev_c += "'"
            # если глухая согласная
            else:
                if prev_c[-1] in VOWELS:
                    syl_pho += prev_c
                    prev_c = ''
                else:
                    prev_c_ = ''
                    for c_ in prev_c:
                        prev_c_ += CONSONANTS_VOICED.get(c_, c_)
                    prev_c = prev_c_
                prev_c += c
        text_pho.append(syl_pho)
    if not text_pho:
        text_pho.append('')
    for c_ in prev_c:
        text_pho[-1] += CONSONANTS_VOICED.get(c_, c_)
    return text_pho if syllables else ''.join(text_pho)

def phonetize2(text, level=3, syllables=False):
    assert level >= 0 and level <= 5, \
           'ERROR: level can be between 0 and 5. Default is 3'
    text = translit(text)
    if level == 0:
        text = re.sub('\s+', ' ', text.strip())
    elif level == 1:
        text = re.sub('\s', '', text)
    else:
        text = phonetize(text, syllables=False)
        if level == 2:
            text = text.replace('е', 'йэ').replace('ё', 'йо') \
                       .replace('ю', 'йу').replace('я', 'йа') \
                       .replace("'ы", 'и')
        elif level == 3:
            pass
        elif level == 4:
            for x, y in dict(CONSONANTS_VOICED,
                             **{'о': 'а', 'э': 'ы', 'и': 'ы'}).items():
                text = text.replace(x, y)
        elif level == 5:
            for x, y in dict(CONSONANTS_VOICED,
                             **{x: 'о' for x in VOWELS}).items():
                text = text.replace(x, y)
    return get_syllables(text) if syllables else text
