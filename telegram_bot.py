from telegram.ext import Updater

from data import label_menu_data
from menu_recommend import recommend_menu

import logging

from telegram.ext import MessageHandler, Filters

from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from telegram_bot_helper import build_menu
from train_data import store_training


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def recommend_message_handler(update, context):
    message = update.message.text
    context.chat_data['train_data'] = message

    label = recommend_menu(message)
    recommended_menu = label_menu_data[label]
    respond_message = f"메뉴로 {recommended_menu} 먹는 건 어떤가요?"
    context.bot.send_message(chat_id=update.effective_chat.id, text=respond_message)

    show_list = [InlineKeyboardButton('네', callback_data='네'), InlineKeyboardButton('아니요', callback_data='아니요')]
    show_markup = InlineKeyboardMarkup(build_menu(show_list, 2))  # make markup
    context.bot.send_message(chat_id=update.effective_chat.id, text="답이 마음에 드나요?", reply_markup=show_markup)


def train_handler(update, context):
    train_data = ' '.join(context.args)
    print(train_data)
    context.chat_data['train_data'] = train_data
    select_label(train_data, update, context)


def select_label(train_data, update, context):
    show_list = [InlineKeyboardButton(i, callback_data=f"음식, {i}") for i in label_menu_data.values()]
    show_markup = InlineKeyboardMarkup(build_menu(show_list, 2))  # make markup

    if train_data:
        context.bot.send_message(chat_id=update.effective_chat.id, text='어느 메뉴로 훈련시킬까요?', reply_markup=show_markup
                                 )


def callback_train(update, context):
    train_data = context.chat_data['train_data']
    label = ''.join(update.callback_query.data.split(', ')[1:])
    inv_label_menu_data = {v: k for k, v in label_menu_data.items()}
    store_training(train_data, inv_label_menu_data[label])
    context.bot.edit_message_text(f"{label}을/를 선택하였습니다.",
                                  chat_id=update.callback_query.message.chat_id,
                                  message_id=update.callback_query.message.message_id)


def callback_train_again(update, context):
    context.bot.edit_message_text("다른 메뉴를 원하시나요?",
                                  chat_id=update.callback_query.message.chat_id,
                                  message_id=update.callback_query.message.message_id)
    train_data = context.chat_data
    select_label(train_data, update, context)


def exit_conversation(update, context):
    context.bot.edit_message_text("감사합니다.",
                                  chat_id=update.callback_query.message.chat_id,
                                  message_id=update.callback_query.message.message_id)


if __name__ == "__main__":
    import json

    with open("secret.json", "r") as json_file:
        secret_data = json.load(json_file)
    token = secret_data['token']
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    echo_handler = MessageHandler(Filters.text & (~Filters.command), recommend_message_handler)
    dispatcher.add_handler(echo_handler)

    caps_handler = CommandHandler('train', train_handler)
    dispatcher.add_handler(caps_handler)
    dispatcher.add_handler(CallbackQueryHandler(callback_train, pattern='^음식'))
    dispatcher.add_handler(CallbackQueryHandler(callback_train_again, pattern='^아니요'))
    dispatcher.add_handler(CallbackQueryHandler(exit_conversation, pattern='^네'))

    updater.start_polling()
