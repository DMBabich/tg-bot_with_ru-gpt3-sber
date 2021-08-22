from passport import password
import telebot
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import numpy as np
import torch

bot = telebot.TeleBot(password)
np.random.seed(42)
torch.manual_seed(42)


def load_tokenizer_and_model(model_name_or_path):
	return GPT2Tokenizer.from_pretrained(model_name_or_path), GPT2LMHeadModel.from_pretrained(model_name_or_path).cuda()


def generate(
		model, tok, text,
		do_sample=True, max_length=50, repetition_penalty=5.0,
		top_k=5, top_p=0.95, temperature=1,
		num_beams=None,
		no_repeat_ngram_size=3
):
	input_ids = tok.encode(text, return_tensors="pt").cuda()
	out = model.generate(
		input_ids.cuda(),
		max_length=max_length,
		repetition_penalty=repetition_penalty,
		do_sample=do_sample,
		top_k=top_k, top_p=top_p, temperature=temperature,
		num_beams=num_beams, no_repeat_ngram_size=no_repeat_ngram_size
	)
	return list(map(tok.decode, out))


tok, model = load_tokenizer_and_model("sberbank-ai/rugpt3medium_based_on_gpt2")

# user_text = "Александр Сергеевич Пушкин родился в "
# user_length = 100
# generated = generate(model, tok, text=user_text, num_beams=20, max_length=user_length)
# print(generated[0])


print('MODEL_GPT SUCCESSFUL')


@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message,
				 f'Я бот, генерирующий текст по GPT модели от Сбербанка. Категорически приветствую, {message.from_user.first_name}')
	bot.send_message(message.chat.id, 'Используй команды:\n/gen для генерации текста\n/help для ознакомления')
	bot.send_message(message.chat.id, 'ОБЯЗАТЕЛЬНО СПЕРВА ПОСМОТРИ ИНФОРМАЦИЮ (/help)')


@bot.message_handler(commands=['gen'], content_types=['text'])
def send_message(message):
	try:
		user = message.text
		user = user.split('!')
		user_length = int(user[1])
		if user_length < 10 or user_length > 900:
			bot.send_message(message.chat.id, 'количество слов НЕ МЕНЬШЕ 10 и НЕ БОЛЬШЕ 900')
			return 'lose'
		user_text = user[2]
		generator = generate(model, tok, text=user_text, num_beams=10, max_length=user_length)
		# print(f'user: {message.from_user.first_name} \nmessage:\n {user}\ngenerated text:\n{generator[0]}\n') # IT'S FOR ME
		# print(user)
		# bot.send_message(message.chat.id, f'слов:{next_words}')
		# bot.send_message(message.chat.id, f'seed: {seed_text}')
		bot.send_message(message.chat.id, text=generator[0])
	except:
		bot.send_message(message.chat.id, 'неправильный ввод! смотри /help')


@bot.message_handler(commands=['help'])
def send_info(message):
	bot.send_message(message.chat.id, 'Тебе необходимо передать мне три вещи\n'
									  'самой первой идет команда /gen\n'
									  'после команды идет число с восклицательным знаком - это количество слов для генерации\n'
									  'затем восклицательный знак и начать последовательность, чтобы я смог продолжить\n'
									  'восклицательный знак я использую как разделитель\n'
									  'однако, число слов должно быть ОТ 10 ДО 900, т.к. я трачу время на вычисления\n'
									  'ну и конечно, если выберешь малое число (например 10), то много слов писать не нужно\n'
									  'чем больше количество слов для генерации, тем больше слов я от тебя жду\n'
									  'но не увлекайся, ведь генератор тут я :D\n\n'
									  'я покажу пример, как это должно выглядеть:\n'
									  '/gen !20 !я пошел в лес и встретил\n\n'
									  'после чего, я за тебя продолжу\n'
									  'среднее время ожидания ~ 3 минуты\n\n'
									  'прочитать про меня можно тут:\n'
									  'https://github.com/sberbank-ai/ru-gpts')


bot.polling()
