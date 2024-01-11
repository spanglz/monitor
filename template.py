""" Шаблоны для отображения на сервере """
BASE_TEMPLATE = '''
<!DOCTYPE html>
<html>
    <head>
        <meta charset='UTF-8'>
        <title>Telegram Bot</title>
    </head>
    <body>{{ content | safe }}</body>
</html>
'''