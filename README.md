# Телеграм бот с нейросетью Ru-GPT3 от Сбера
Небольшой "тренировочный" кейс по прикручиванию NLP-нейронки Ru-GPT3 к боту в телеге.
<br>Весьма интересный опыт, который стоило получить :)

# Как это работает?
Пользователь пишет боту команду
<br> /gen !число_последовательномтей!начало_последовательности
<br>Например:
```
/gen !200!курочка убийца захватила город
```
И модель выводит сгенерированную последовательность.

<br>Загрузить нужную модель можно в строке:
``` python
tok, model = load_tokenizer_and_model("sberbank-ai/rugpt3medium_based_on_gpt2")
```
Для "игр" с ботом и отладки, его можно поднять в PyCharm.


# Ссылки
<br>[Репозиторий с моделями ru-GPT от Сбербанка](https://github.com/sberbank-ai/ru-gpts)
<br>[BotFather](https://telegram.me/BotFather)
<br>[telebot](https://github.com/eternnoir/pyTelegramBotAPI)
<br>[PyCharm](https://www.jetbrains.com/ru-ru/pycharm/)
