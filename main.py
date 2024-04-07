from typing import Final
from telegram import Update
import json
from web3 import Web3
from jsonABI import function_signature_to_abi
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN: Final = '7132682756:AAFOv___QxCisyd7II9tBb1ABwOcATnbimQ'
BOT_USERNAME: Final = '@contract_command_bot'
# Connect to an Ethereum node
CONTRACT_ENDPOINT = Web3(Web3.HTTPProvider('https://eth.llamarpc.com'))
# Main commands


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi & Welcome to the Contract Command Bot! :D")


async def call_contract_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 3:
        await update.message.reply_text('To use this command do the following: /call <contract address> <function_signature> <arguments>')
        return
# store the user input
    contract_address = args[0]
    checksum_address = Web3.to_checksum_address(contract_address)
    print(contract_address)
    abi_ = function_signature_to_abi(args[1])
    print(abi_)
    function_signature = args[1]
    print(function_signature)
    arguments = args[2]
    acc_address = Web3.to_checksum_address(arguments)
    print(arguments)

    try:
        contrat = CONTRACT_ENDPOINT.eth.contract(
            address=checksum_address, abi=abi_)
        result = contrat.functions.balanceOf(acc_address).call()
        await update.message.reply_text(f"Result: {result}")
    except Exception as e:
        await update.message.reply_text(f"Failed to call smart contracr. Error: {e}")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Display a help message with instructions on how to use the bot and the available commands.")


# Responses
def handle_response(text: str) -> str:
    processed: str = text.lower()
    if 'hello' | 'hi' in text:
        return 'hi there!'
    if 'how are you' in text:
        return 'Good :)'
    if 'sup' in text:
        'nm rly'


async def handle_message(update: Update, contect: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User({update.message.chat.id}) in {message_type}: "{text}"')
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot: ', response)
    await update.message.reply_text(response)


async def error(update: Update, context:  ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('starting bot...')
    app = Application.builder().token(TOKEN).build()

    #  commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('call', call_contract_command))
    app.add_handler(CommandHandler('help', help_command))

    #  messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # error
    app.add_error_handler(error)
    print('polling..')
    app.run_polling(poll_interval=3)
