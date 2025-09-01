import sqlite3
import spacy

nlp = spacy.load('ru_core_news_lg')  # модель для русского языка

def find_similar_question(question, cursor):  # функция для поиска схожих ответов
    question_doc = nlp(question)  # преобразует в Doc для читабельности
    cursor.execute("SELECT id, question FROM questions_answers")  # нахождение всех вопросов в базе данных
    rows = cursor.fetchall()  # сохраняет все строки в список rows, каждая строка кортеж с ключом и значением
    most_similar_question = None  # предотвращает ошибки, если переменная не установлена на конкретный вопрос, но если найдется похожий, то в дальнейшем будет обновлена
    highest_similarity = 0  # используется для нахождения наибольшей схожести

    for row in rows:  # цикл к.т перебирает вопросы и ответы
        db_question = row[1]  # извлекает элемент из кортежа, к.т является вопросом из базы данных
        db_question_doc = nlp(db_question)  # преобразует в Doc для читабельности spacy
        similarity = question_doc.similarity(db_question_doc)  # преобразуем вопрос из базы данных в Doc, чтобы работать с ним, как с текстом в spacy

        if similarity > highest_similarity:  # если текущая схожесть больше, чем наибольшая найденная до этого, то обновляем переменные
            highest_similarity = similarity  # обновляем наибольшую схожесть
            most_similar_question = row  # обновляем наибольшую схожесть

    if most_similar_question and highest_similarity > 0.7:  # Порог схожести
        return most_similar_question  # возврвщает наиболее подходящий вопрос
    else:
        return None  # если схожий вопрос не найден

def get_answer_from_db(question, category=None):  # получение ответа
    try:
        connection = sqlite3.connect('faq.db')  # Подключаемся к базе данных
        cursor = connection.cursor()  # для SQL запросов

        if category:
            cursor.execute("SELECT answer FROM questions_answers WHERE question = ? AND category = ?", (question, category))  # Ищем ответ в базе
        else:
            cursor.execute("SELECT answer FROM questions_answers WHERE question = ?", (question,))

        result = cursor.fetchone()  # Получаем первый результат

        if result:  # result это кортеж с ключом и значением
            return result[0]  # возвращаем только текст ответа
        else:
            similar_question = find_similar_question(question, cursor)  # Если точного ответа нет, ищем похожий вопрос в функции выше
            if similar_question:
                question_id, existing_question = similar_question
                cursor.execute("SELECT answer FROM questions_answers WHERE id = ?", (question_id,))
                similar_answer = cursor.fetchone()
                return f"Похожий вопрос: {existing_question}\nОтвет: {similar_answer[0]}"
            else:
                return None  # если не найден вопрос возвращаем none
    except Exception as e:
        return f"Произошла ошибка при подключении к базе данных:{str(e)} "
    finally:
        connection.close()

def add_new_question_answer():
    try:
        connection = sqlite3.connect('faq.db')  # Подключаемся к базе данных
        cursor = connection.cursor()

        # Запросить новый вопрос
        new_question = input("Бот: Введи новый вопрос: ").strip()

        # Проверяем, есть ли уже этот вопрос в базе
        cursor.execute("SELECT 1 FROM questions_answers WHERE question = ?", (new_question,))
        if cursor.fetchone():
            print("Бот: Этот вопрос уже существует в базе данных.")
            return

        # Запросить новый ответ
        new_answer = input("Бот: Введи ответ для этого вопроса: ").strip()

        # Запросить категорию
        new_category = input("Бот: Введи категорию для этого вопроса: ").strip()

        # Проверяем, существует ли категория
        cursor.execute("SELECT 1 FROM categories WHERE category_name = ?", (new_category,))
        if not cursor.fetchone():
            # Если категории нет, создаем её
            cursor.execute("INSERT INTO categories (category_name) VALUES (?)", (new_category,))
            print(f"Бот: Категория '{new_category}' добавлена в базу данных.")

        # Добавляем вопрос, ответ и категорию в базу данных
        cursor.execute("INSERT INTO questions_answers (question, answer, category) VALUES (?, ?, ?)",
                       (new_question, new_answer, new_category))

        connection.commit()  # Сохраняем изменения
        print(f"Бот: Вопрос '{new_question}' и ответ успешно добавлены в базу данных!")

    except Exception as e:
        print(f"Произошла ошибка при добавлении данных: {str(e)}")
    finally:
        connection.close()

# Функция для изменения вопроса
def update_question(old_question, new_question):
    try:
        connection = sqlite3.connect('faq.db')  # Подключаемся к базе данных
        cursor = connection.cursor()

        # Проверка, существует ли уже новый вопрос в базе данных
        cursor.execute("SELECT 1 FROM questions_answers WHERE question = ?", (new_question,))
        if cursor.fetchone():
            return "Этот новый вопрос уже существует в базе данных."

        # Обновляем вопрос в базе данных
        cursor.execute("UPDATE questions_answers SET question = ? WHERE question = ?", (new_question, old_question))
        connection.commit()  # Сохраняем изменения
        return f"Вопрос '{old_question}' успешно изменен на '{new_question}'."

    except Exception as e:
        return f"Произошла ошибка при изменении вопроса: {str(e)}"
    finally:
        connection.close()

# Функция для изменения ответа
def update_answer(question, new_answer):
    try:
        connection = sqlite3.connect('faq.db')  # Подключаемся к базе данных
        cursor = connection.cursor()

        # Обновляем ответ в базе данных
        cursor.execute("UPDATE questions_answers SET answer = ? WHERE question = ?", (new_answer, question))
        connection.commit()  # Сохраняем изменения

        return f"Ответ на вопрос '{question}' успешно изменен."

    except Exception as e:
        return f"Произошла ошибка при изменении ответа: {str(e)}"
    finally:
        connection.close()

# Функция для изменения категории
def update_category(question, new_category):
    try:
        connection = sqlite3.connect('faq.db')  # Подключаемся к базе данных
        cursor = connection.cursor()

        # Проверка, существует ли новая категория
        cursor.execute("SELECT 1 FROM categories WHERE category_name = ?", (new_category,))
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

def get_categories():  # Функция для вывода категорий
    connection = sqlite3.connect('faq.db')
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT category FROM questions_answers")  # Получаем все уникальные категории
    categories = cursor.fetchall()
    connection.close()
    return [category[0] for category in categories]

def get_questions_by_category(category):
    connection = sqlite3.connect('faq.db')
    cursor = connection.cursor()
    cursor.execute("SELECT question FROM questions_answers WHERE category = ?", (category,))  # Получаем все вопросы по категории
    questions = cursor.fetchall()
    connection.close()
    return [question[0] for question in questions]  # Возвращаем список вопросов


def add_new_data():
    """Функция для добавления новых данных в базу (вопрос, ответ, категория)."""
    try:
        connection = sqlite3.connect('faq.db')
        cursor = connection.cursor()

        print("Бот: Вы добавляете новые данные в базу.")
        new_category = input("Бот: Введите новую категорию (или оставьте пустым для существующей): ").strip()

        if new_category:
            cursor.execute("SELECT 1 FROM categories WHERE category_name = ?", (new_category,))
            existing_category = cursor.fetchone()
            if not existing_category:
                cursor.execute("INSERT INTO categories (category_name) VALUES (?)", (new_category,))
                print(f"Бот: Категория '{new_category}' добавлена.")

        new_question = input("Бот: Введите новый вопрос: ").strip()
        cursor.execute("SELECT 1 FROM questions_answers WHERE question = ?", (new_question,))
        existing_question = cursor.fetchone()

        if existing_question:
            print("Бот: Такой вопрос уже существует в базе данных. Добавление отменено.")
            connection.close()
            return

        new_answer = input("Бот: Введите ответ для этого вопроса: ").strip()
        category_to_use = new_category if new_category else input("Бот: Укажите категорию для вопроса: ").strip()

        cursor.execute("INSERT INTO questions_answers (question, answer, category) VALUES (?, ?, ?)", 
                       (new_question, new_answer, category_to_use))

        connection.commit()
        print("Бот: Новый вопрос и ответ успешно добавлены в базу данных!")
    except Exception as e:
        print(f"Бот: Произошла ошибка при добавлении данных: {str(e)}")
    finally:
        connection.close()

def chat_bot():
    # Ввод пользователя
    print("Бот: Привет! Я чат-бот VAO. Я больше похож на блокнот, в котором можно хранить нужную информацию. Я пока еще новая программа, но все же, с чем то я могу справиться. Не суди строго :).")
    
    while True:
        try:
            print("\nВыбери действие:")
            print("1. Задать вопрос")
            print("2. Показать список вопросов из категории")
            print("3. Добавить новый вопрос и ответ")
            print("4. Изменить вопрос")
            print("5. Изменить ответ")
            print("6. Изменить категорию вопроса")
            
            action = input("Твой выбор: ").strip()
            
            if action == '1':
                categories = get_categories()
                if not categories:
                    print("Бот: В базе данных нет категорий.")
                    continue

                print("Бот: Доступные категории:")
                for index, category in enumerate(categories, 1):
                    print(f"{index}. {category}")

                category_choice = input("Бот: Выберите категорию (введите номер): ").strip()

                if category_choice.lower() in ('выход', 'exit', 'quit'):
                    print("Бот: До свидания! Хорошего дня!")
                    return

                try:
                    category_index = int(category_choice)
                    if 1 <= category_index <= len(categories):
                        category = categories[category_index - 1]
                    else:
                        print("Бот: Некорректный выбор категории.")
                        continue
                except ValueError:
                    print("Бот: Введите корректный номер категории.")
                    continue

                # Показать вопросы в выбранной категории
                print(f"Бот: Вопросы в категории '{category}':")
                questions = get_questions_by_category(category)
                if questions:
                    for idx, question in enumerate(questions, 1):
                        print(f"{idx}. {question}")
                else:
                    print(f"Бот: В категории '{category}' пока нет вопросов.")

                question_choice = input(f"Вы ({category}): Введи номер вопроса или напиши свой вопрос: ").strip()
                if question_choice.lower() in ('выход', 'exit', 'quit'):
                    print("Бот: До свидания! Хорошего дня!")
                    break

                if question_choice.isdigit():
                    question_index = int(question_choice) - 1
                    if 0 <= question_index < len(questions):
                        question = questions[question_index]
                        result = get_answer_from_db(question, category)
                        if result:
                            print(f"Бот: Ответ: {result}")
                        else:
                            print("Бот: Извини, я не нашел ответа на твой вопрос, но ты можешь найти информацию тут https://www.w3schools.com/")
                    else:
                        print("Бот: Некорректный номер вопроса.")
                else:
                    result = get_answer_from_db(question_choice, category)
                    if result:
                        print(f"Бот: Ответ: {result}")
                    else:
                        print("Бот: Извини, я не нашел ответа на твой вопрос.")
            
            elif action == '2':
                # Показать вопросы в выбранной категории
                categories = get_categories()
                if not categories:
                    print("Бот: В базе данных нет категорий.")
                    continue

                print("Бот: Доступные категории:")
                for index, category in enumerate(categories, 1):
                    print(f"{index}. {category}")

                category_choice = input("Бот: Выберите категорию (введите номер): ").strip()
                try:
                    category_index = int(category_choice)
                    if 1 <= category_index <= len(categories):
                        category = categories[category_index - 1]
                        questions = get_questions_by_category(category)
                        if questions:
                            print(f"Бот: Вопросы в категории '{category}':")
                            for idx, question in enumerate(questions, 1):
                                print(f"{idx}. {question}")
                        else:
                            print(f"Бот: В категории '{category}' пока нет вопросов.")
                    else:
                        print("Бот: Некорректный выбор категории.")
                except ValueError:
                    print("Бот: Введи корректный номер категории.")
                    continue

            elif action == '3':
                add_new_data()

            elif action == '4':
                old_question = input("Бот: Введите вопрос, который хотите изменить: ").strip()
                new_question = input("Бот: Введите новый текст вопроса: ").strip()
                confirmation = update_question(old_question, new_question)
                print(f"Бот: {confirmation}")

            elif action == '5':
                question = input("Бот: Введите вопрос, для которого хотите изменить ответ: ").strip()
                new_answer = input("Бот: Введите новый ответ для этого вопроса: ").strip()
                confirmation = update_answer(question, new_answer)
                print(f"Бот: {confirmation}")

            elif action == '6':
                question = input("Бот: Введите вопрос, для которого хотите изменить категорию: ").strip()
                new_category = input("Бот: Введите новую категорию для этого вопроса: ").strip()
                confirmation = update_category(question, new_category)
                print(f"Бот: {confirmation}")
            
            else:
                print("Бот: Некорректный выбор. Попробуй еще раз.")
        except ValueError:
            print("Бот: Введи корректный номер действия.")
        except Exception as e:
            print(f"Бот: Произошла ошибка: {str(e)}")

# Запуск бота
if __name__ == "__main__":  # гарантирует, что функция chat_bot будет выполнена тогда, когда скрипт запускается напрямую, а не импортируется как модуль
    chat_bot()
