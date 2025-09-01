import sqlite3
from flask import Flask, render_template, request, session
from chat_bot import get_categories, get_questions_by_category, add_new_question_answer, update_question, update_answer, update_category, get_answer_from_db

app = Flask(__name__)
app.secret_key = "12346789"

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'step' not in session:
        session['step'] = 1
    if 'action' not in session:
        session['action'] = None
    step = session['step']
    action = session['action']
    message = None
    categories = []
    questions = []
    answer = None
    
    if request.method == 'POST':
        user_input = request.form.get('user_input')

        # Если нажали кнопку "Назад"
        if 'back_button' in request.form:
            session['step'] -= 1
            if session['step'] < 1:
                session['step'] = 1
            # Очистка выбранной категории или вопроса
            session.pop('category_choice', None)
            session.pop('question_choice', None)

        # Первый шаг: выбор действия
        if step == 1:
            if user_input == "1":
                session['step'] = 2
                session['action'] = "1"
                categories = get_categories()  # Получаем список категорий
                message = "Выберите категорию для вашего вопроса."
            elif user_input == "2":
                session['step'] = 2
                session['action'] = "2"
                categories = get_categories()  # Список категорий для добавления нового вопроса
                message = "Выберите категорию для добавления нового вопроса."
            elif user_input == "3":
                session['step'] = 2
                session['action'] = "3"
                categories = get_categories()  # Список категорий для изменения вопроса
                message = "Выберите категорию для изменения вопроса."
            elif user_input == "4":
                session['step'] = 2
                session['action'] = "4"
                categories = get_categories()  # Список категорий для изменения ответа
                message = "Выберите категорию для изменения ответа."
            elif user_input == "5":
                session['step'] = 2
                session['action'] = "5"
                categories = get_categories()  # Список категорий для изменения категории вопроса
                message = "Выберите категорию для изменения категории."
            else:
                message = "Некорректный выбор. Попробуйте еще раз."

        # Шаг 2: Выбор категории для действия (задать вопрос, добавить новый вопрос и т.д.)
        elif step == 2:
            if action == "1":
                category_choice = request.form.get('category_choice')
                if category_choice:
                    session['step'] = 3
                    session['category_choice'] = category_choice
                    questions = get_questions_by_category(category_choice)
                    message = "Выберите вопрос из списка."
                else:
                    message = "Пожалуйста, выберите категорию."

            elif action == "2":
                category_choice = request.form.get('category_choice')
                if category_choice:
                    session['step'] = 7  # Переходим к шагу, где пользователь вводит новый вопрос и ответ
                    session['category_choice'] = category_choice
                    message = f"Вы выбрали категорию: {category_choice}. Введите новый вопрос и ответ."
                else:
                    message = "Пожалуйста, выберите категорию."

            elif action == "3":
                category_choice = request.form.get('category_choice')
                if category_choice:
                    session['step'] = 4  # Переходим к выбору вопроса для изменения
                    session['category_choice'] = category_choice
                    questions = get_questions_by_category(category_choice)
                    message = "Выберите вопрос для изменения."
                else:
                    message = "Пожалуйста, выберите категорию."

            elif action == "4":
                category_choice = request.form.get('category_choice')
                if category_choice:
                    session['step'] = 5  # Переходим к выбору вопроса для изменения ответа
                    session['category_choice'] = category_choice
                    questions = get_questions_by_category(category_choice)
                    message = "Выберите вопрос для изменения ответа."
                else:
                    message = "Пожалуйста, выберите категорию."

            elif action == "5":
                category_choice = request.form.get('category_choice')
                if category_choice:
                    session['step'] = 6  # Переходим к выбору вопроса для изменения категории
                    session['category_choice'] = category_choice
                    questions = get_questions_by_category(category_choice)
                    message = "Выберите вопрос для изменения категории."
                else:
                    message = "Пожалуйста, выберите категорию."

        # Шаг 3: Выбор вопроса для ответа
        elif step == 3:
            if action == "1":
                question_choice = request.form.get('question_choice')
                answer = get_answer_from_db(question_choice)
                message = f"Ответ на ваш вопрос: {answer}. Хотите задать еще вопрос или вернуться к действиям?"
                session['step'] = 1

        # Шаги 4-6: Изменение вопроса, ответа или категории
        elif step == 4:
            question_choice = request.form.get('question_choice')
            new_question = request.form.get('new_question')
            message = update_question(question_choice, new_question)
            session['step'] = 1

        elif step == 5:
            question_choice = request.form.get('question_choice')
            new_answer = request.form.get('new_answer')
            message = update_answer(question_choice, new_answer)
            session['step'] = 1

        elif step == 6:
            question_choice = request.form.get('question_choice')
            new_category = request.form.get('new_category')
            message = update_category(question_choice, new_category)
            session['step'] = 1

        # Шаг 7: Добавление нового вопроса и ответа
        elif step == 7:
            new_question = request.form.get('new_question')
            new_answer = request.form.get('new_answer')
            new_category = session.get('category_choice')
            if new_question and new_answer:
                message = add_new_question_answer(new_question, new_answer, new_category)
                session['step'] = 1  # Возвращаемся на шаг 1 после добавления вопроса
            else:
                message = "Пожалуйста, заполните все поля."

    return render_template('index.html', step=session.get('step'), action=session.get('action'), message=message, categories=categories, questions=questions, answer=answer)


# Функция добавления нового вопроса и ответа
def add_new_question_answer(new_question, new_answer, new_category):
    try:
        connection = sqlite3.connect('faq.db')  # Подключаемся к базе данных
        cursor = connection.cursor()

        # Проверяем, существует ли уже этот вопрос
        cursor.execute("SELECT 1 FROM questions_answers WHERE question = ?", (new_question,))
        if cursor.fetchone():
            return "Этот вопрос уже существует в базе данных."

        # Проверяем, существует ли категория
        cursor.execute("SELECT 1 FROM questions_answers WHERE category = ?", (new_category,))
        if not cursor.fetchone():
            # Если категории нет, создаем её
            cursor.execute("INSERT INTO questions_answers (category) VALUES (?)", (new_category,))
            connection.commit()  # Сохраняем изменения
            return f"Категория '{new_category}' добавлена в базу данных."

        # Добавляем вопрос, ответ и категорию в базу данных
        cursor.execute("INSERT INTO questions_answers (question, answer, category) VALUES (?, ?, ?)",
                       (new_question, new_answer, new_category))
        connection.commit()  # Сохраняем изменения
        return f"Вопрос '{new_question}' и ответ успешно добавлены в базу данных!"

    except Exception as e:
        return f"Произошла ошибка при добавлении данных: {str(e)}"
    finally:
        connection.close()

def update_category(question, new_category):
    try:
        connection = sqlite3.connect('faq.db')  # Подключаемся к базе данных
        cursor = connection.cursor()

        # Проверка, существует ли новая категория
        cursor.execute("SELECT 1 FROM questions_answers WHERE category = ?", (new_category,))
        if not cursor.fetchone():
            return f"Категория '{new_category}' не существует в базе данных."

        # Обновляем категорию вопроса
        cursor.execute("UPDATE questions_answers SET category = ? WHERE question = ?", (new_category, question))
        connection.commit()  # Сохраняем изменения

        return f"Категория для вопроса '{question}' успешно изменена на '{new_category}'."

    except Exception as e:
        return f"Произошла ошибка при изменении категории: {str(e)}"
    finally:
        connection.close()

if __name__ == "__main__":
    app.run(debug=True)









