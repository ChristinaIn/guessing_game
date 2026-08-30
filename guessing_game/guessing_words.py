import emoji, random, tkinter as tk
import os, sys

def resource_path(filename):  # возвращает правильный путь к ресурсу
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__))
    )

    return os.path.join(base_path, filename)

root = tk.Tk()

screen_width = root.winfo_screenwidth()  # настройки размеров экрана
screen_height = root.winfo_screenheight()
window_width = 500
window_height = 500
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.geometry('500x500')
root.resizable(False, False)
root.title('Игра Угадайка')


background_image = tk.PhotoImage(file=resource_path('background_игра_угадайка.png'))  # создание бэкграунда
canvas = tk.Canvas(
    root,
    width=window_width,
    height=window_height,
    highlightthickness=0
)
canvas.pack(fill='both', expand=True)
canvas.create_image(
    0,
    0,
    anchor='nw',
    image=background_image
)

astronomy = [
    'астероид', 'астрономия', 'бетельгейзе', 'галактика', 'гравитация', 'комета',
    'космос', 'кратер', 'метеор', 'метеорит', 'млечный', 'нейтрон', 'орбита',
    'планета', 'планетарий', 'пульсар', 'радиотелескоп', 'сверхновая', 'светило',
    'солнце', 'спектр', 'спутник', 'туманность', 'фотон', 'хромосфера', 'черная',
    'экзопланета', 'эллипс', 'юпитер', 'ядро'
]

banking = [
    'аккредитив', 'активы', 'аннуитет', 'банк', 'банкомат', 'вклад', 'валюта',
    'гарантия', 'депозит', 'долг', 'залог', 'инкассо', 'ипотека', 'капитал',
    'капитализация', 'клиринг', 'комиссия', 'конвертация', 'кредит', 'ликвидность',
    'овердрафт', 'платёж', 'резервирование', 'рефинансирование', 'счёт', 'эквайринг',
    'экономика', 'эмитент', 'заёмщик', 'проценты'
]

history = [
    'абсолютизм', 'археология', 'вассал', 'восстание', 'генеалогия', 'государство',
    'деспотизм', 'империя', 'индустриализация', 'инквизиция', 'колонизация', 'конституция',
    'крестовый', 'монархия', 'наследование', 'наполеон', 'палеография', 'перепись', 'революция',
    'реформация', 'самодержавие', 'сословие', 'феодализм', 'хронология', 'цивилизация', 'эпоха',
    'архив', 'династия', 'летопись', 'реставрация'
]

psychology = [
    'агрессия', 'адаптация', 'апатия', 'бессознательное', 'восприятие', 'внимание', 'воображение',
    'галлюцинация', 'депрессия', 'интроверсия', 'когниция', 'мотивация', 'невроз', 'обучение',
    'память', 'перцепция', 'психика', 'рефлексия', 'самооценка', 'стресс', 'темперамент',
    'тревожность', 'фрустрация', 'эмпатия', 'экстраверсия', 'эксперимент', 'эмоция',
    'личность', 'мышление', 'сублимация'
]

programming = [
    'алгоритм', 'аргумент', 'библиотека', 'ветвление', 'выражение', 'дебаггер',
    'декомпозиция', 'интерфейс', 'компилятор', 'константа', 'контейнер', 'класс',
    'массив', 'метод', 'модуль', 'объект', 'оператор', 'параметр', 'переменная',
    'протокол', 'рекурсия', 'репозиторий', 'сервер', 'скрипт', 'синтаксис', 'функция',
    'цикл', 'экземпляр', 'эмулятор', 'исключение'
]

word = ''  # загаданное слово
guessed_letters = []  # список уже названных букв
guessed_words = []  # список уже названных слов
tries = 6  # количество попыток
current_widgets = []  # список элементов для удаления при переходе на другой экран

def clear_screen():  # очищает текущий экран, но canvas и фоновая картинка не удаляются

    for item in current_widgets:
        if isinstance(item, int):  # если это объект бэкграунда, то удаляем его с бэк-м
            canvas.delete(item)

        else:
            item.destroy()  # если это обычный tkinter-виджет

    current_widgets.clear()

def display_hearts():  # возвращает строку с оставшимися жизнями
    return emoji.emojize(':red_heart:') * tries + emoji.emojize(':grey_heart:') * (6 - tries)

def get_word_completion():  # Создаёт строку с угаданными буквами
    completion = ''

    for letter in word:
        if letter in guessed_letters:
            completion += letter + ' '
        else:
            completion += '_ '

    return completion

def show_category_screen():  # экран выбора категории для игры
    clear_screen()
    title = canvas.create_text(
        250,
        50,
        text='Давай поиграем в угадайку слов!',
        font=('Arial', 16, 'bold'),
        fill='black'
    )

    current_widgets.append(title)  # запоминает объект Заголовок, чтобы потом удалить

    category_text = canvas.create_text(  # выбираем категорию для игры
        250,
        150,
        text=(
            'Введи обозначение области:\n\n'
            'а — астрономия\n'
            'б — банковское дело\n'
            'и — история\n'
            'пр — программирование\n'
            'пс — психология'
        ),
        font=('Arial', 12),
        fill='black',
        justify='center'
    )

    current_widgets.append(category_text)  # запоминает объект Категория, чтобы потом удалить

    category_entry = tk.Entry(  # поле ввода
        root,
        font=('Arial', 14),
        justify='center'
    )

    canvas_window = canvas.create_window( # размещение поля ввода поверх бэкграунда
        250,
        250,
        window=category_entry,
        width=100
    )

    current_widgets.append(category_entry)  # запоминает объекты Поле ввода
    current_widgets.append(canvas_window)  # и его же на сanvas (бэкграунде)
    category_entry.focus()  # установка курсора в поле

    error_label = tk.Label(  # сообщение об ошибке
        root,
        text='',
        font=('Arial', 11),
        bg='white'
    )

    error_window = canvas.create_window(  # сообщение об ошибке на бэк-е
        250,
        300,
        window=error_label
    )

    current_widgets.append(error_label)  # запоминает выше созданные объекты
    current_widgets.append(error_window)

    def choose_category(event=None):
        global word

        answer = category_entry.get().lower().strip()  # получение введенного текста

        categories = {  # словарь областей
            'а': astronomy,
            'б': banking,
            'и': history,
            'пр': programming,
            'пс': psychology
        }

        if answer not in categories:  # проверяет корректность ответа
            error_label.config(
                text='Введи корректный вариант'
            )

            category_entry.delete(0, tk.END)
            return

        word = random.choice(categories[answer]).upper()  # выбор случайного слова

        start_game()  # запуск новой игры

    category_entry.bind(  # Нажатие Enter вызывает функцию choose_category
        '<Return>',
        choose_category
    )

def start_game():  # начало игры
    global guessed_letters
    global guessed_words
    global tries

    guessed_letters = []  # очистка старых данных
    guessed_words = []
    tries = 6

    show_game_screen()  # показываем игровой экран

def show_game_screen():  # игровой экран
    clear_screen()

    title = canvas.create_text(  # заголовок
        250,
        40,
        text='Угадай слово',
        font=('Arial', 18, 'bold'),
        fill='black'
    )

    current_widgets.append(title)

    hearts_label = canvas.create_text(  # сердечки
        250,
        85,
        text=display_hearts(),
        font=('Arial', 20),
        fill='black'
    )

    current_widgets.append(hearts_label)

    word_label = canvas.create_text(  # загаданное слово
        250,
        150,
        text=get_word_completion(),
        font=('Arial', 24, 'bold'),
        fill='black'
    )

    current_widgets.append(word_label)

    instruction = canvas.create_text(  # инструкция для игры
        250,
        220,
        text='Введи букву или слово:',
        font=('Arial', 12),
        fill='black'
    )

    current_widgets.append(instruction)

    guess_entry = tk.Entry(  # поле ввода
        root,
        font=('Arial', 16),
        justify='center'
    )

    guess_window = canvas.create_window(
        250,
        260,
        window=guess_entry,
        width=200
    )

    current_widgets.append(guess_entry)
    current_widgets.append(guess_window)
    guess_entry.focus()

    message_label = tk.Label(  # сообщение игры
        root,
        text='',
        font=('Arial', 12),
        bg='white'
    )

    message_window = canvas.create_window(
        250,
        320,
        window=message_label
    )

    current_widgets.append(message_label)
    current_widgets.append(message_window)

    def check_guess(event=None):  # проверка ответа

        global tries

        guess = guess_entry.get().upper().strip()  # получение ответа пользователя

        guess_entry.delete(0, tk.END)  # очищение поля ввода

        if not guess.isalpha():  # проверка символов
            message_label.config(
                text='Введи букву или слово'
            )

            return

        if guess in guessed_letters or guess in guessed_words:  # проверка повтора вводы буквы
            message_label.config(
                text='Этот вариант уже был'
            )

            return

        if len(guess) > 1:  # если введено слово

            if guess == word:  # если угадали

                show_result_screen(True)  # показываем победу
                return

            else:  # ввод неправильного слова

                guessed_words.append(guess)  # пополняется список слов

                tries -= 1  # отнимается попытка

                message_label.config(  #  выводится сообщение
                    text=f'Неверно! Осталось попыток: {tries}'
                )

        else:  # если введена буква

            if guess in word:  # введенная буква есть в слове

                guessed_letters.append(guess)  # пополняется список угаданных букв

                message_label.config(  # выводится сообщение
                    text='Ты угадал букву!'
                )

            else:  # неверно угаданная буква

                guessed_letters.append(guess)  # пополняется список угаданных букв

                tries -= 1  # отнимается попытка

                message_label.config(  # выводится сообщение
                    text=f'Такой буквы нет. Осталось попыток: {tries}'
                )

        canvas.itemconfig(  # обновление сердечек
            hearts_label,
            text=display_hearts()
        )

        canvas.itemconfig(  # обновление слова
            word_label,
            text=get_word_completion()
        )

        if '_' not in get_word_completion():  # проверка победы
            show_result_screen(True)
            return

        if tries == 0:  # проверка проигрыша
            show_result_screen(False)

    guess_entry.bind(  # нажатие Enter запускает проверку ответа
        '<Return>',
        check_guess
    )

def show_result_screen(victory):  # экран результата
    clear_screen()

    if victory:

        result_text = '🎉 Ура! Ты угадал! 🎉'

    else:

        result_text = f'😢 Ты проиграл!\n\nЗагаданное слово:\n{word}'

    result = canvas.create_text(  # создание текста результата
        250,
        150,
        text=result_text,
        font=('Arial', 18, 'bold'),
        fill='black',
        justify='center'
    )

    current_widgets.append(result)

    question = canvas.create_text(  # вывод вопроса о новой игре
        250,
        250,
        text='Будем играть снова?',
        font=('Arial', 14),
        fill='black'
    )

    current_widgets.append(question)

    yes_button = tk.Button(  # кнопка ДА
        root,
        text='Да',
        font=('Arial', 12),
        width=10,
        command=show_category_screen  # возврат к выбору категории игры
    )

    yes_window = canvas.create_window(
        190,
        310,
        window=yes_button
    )

    current_widgets.append(yes_button)
    current_widgets.append(yes_window)

    no_button = tk.Button(  # кнопка НЕТ
        root,
        text='Нет',
        font=('Arial', 12),
        width=10,

        command=root.destroy  # закрытие программы
    )

    no_window = canvas.create_window(
        310,
        310,
        window=no_button
    )

    current_widgets.append(no_button)
    current_widgets.append(no_window)

show_category_screen()  # запуск программы

root.mainloop()  # Запуск главного цикла tkinter