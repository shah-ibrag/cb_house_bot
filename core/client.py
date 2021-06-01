from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler

app = Client("my_account")

async def invite_link(x):
	chat = await app.get_chat(f"{x}")
	print(chat)

async def log(e, id, link):
	text = f" ошибка - {e} \n \
	id = {id} - {link}"
	await app.send_message("self", text)


async def reg(id, link):
	text = f" клаб открыт пользователем - {link} - {id}"
	await app.send_message("self", text)


async def create_group(message, group_name: str, admin_id: int):
	try:
		await app.create_group(f"{message.from_user.first_name}", message.chat.id)
		#await invite_link(message.from_user.first_name)
		await reg(message.chat.id, message.from_user.mention)
		await app.send_message(message.chat.id, "клаб создан")

	except Exception as e:
		await app.send_message(message.chat.id, "У вас в настройках приватности проблема")
		await log(e, message.chat.id, message.from_user.mention)


@app.on_message(filters.group_chat_created)
async def getChat(client, message):
	await app.send_message(message.chat.id, message.chat.id)
	chat = await app.get_chat(message.chat.id)
	await app.send_message("self", message.chat.id)


@app.on_message(filters.private)
async def hello(client, message):
	text = f"Привет, {message.from_user.mention} \n \
	Доступные команды: \n \
	/cclub - создать клаб"
	await message.reply_text(text)

