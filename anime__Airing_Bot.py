import os, logging
import BotResources, requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Enable: logging
# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO      
# )
# logger = logging.getLogger(__name__)


#getting data from anime scheduleing
def animeSchedule():
    obj = BotResources.getData()
    data = obj.messageData()

    print("in anime Schedule")
    return data


# Define the command handler to send a message with an inline button
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message with an inline button that triggers a callback query."""
    await update.message.reply_text("Hold your horses 🐎, Searching 🔍 and Collecting ⬇️ today airing anime list, wait for a sec 🙏")
    animeData = animeSchedule()
    #updating message id
    await update.message.reply_text("Today Anime data collected successfully ✅✅✅, ready to send 🚀")
    #await update.message.reply_text("Today Anime data collected successfully,")
    for anime in animeData:
        replyMessage = BotResources.getData.message
        replyMessage = replyMessage.format(anime["titles"], anime["time"], anime["season"],anime["episode"],anime["synopsis"])
        IMAGE_URL = f'https://img.anili.st/media/{anime["posterId"]}'
        try:
        # Attempt to download the image from the URL
            response = requests.get(IMAGE_URL)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
            print("sending message : ", anime["titles"])
            # Send the photo with the user's message as a caption
            await context.bot.send_photo(
                chat_id=update.message.chat_id,
                photo=response.content,
                caption=replyMessage,
                parse_mode='MarkdownV2'
                #reply_to_message_id=update.message.message_id
        )
        except requests.exceptions.RequestException as e:
        # Handle any request exceptions
            await update.message.reply_text("An unexpected error occured")
    

#handling response
def handle_response(text:str)-> str:
  data:str=text.lower()
  if 'hello' in data:
    return 'hey there'
  return "i don't undestand your input"




async def handle_message(update:Update,context:ContextTypes.DEFAULT_TYPE):
  message_type:str=update.message.chat.type
  text:str=update.message.text
  print(f'user ({update.message.chat.id}) in {message_type}: {text}')

  #response 
  response:str = handle_response(text)
  print('Bot:', response)

  await update.message.reply_text(response)





# Main function to set up the bot
def main():
    """Start the bot."""
    load_dotenv()
    TOKEN_ID = os.getenv("TOKEN_ID")
    # print(TOKEN_ID)
    # Create the Application and pass it your bot's token.
    application = ApplicationBuilder().token(TOKEN_ID).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Start the Bot
    print("polling . . .")
    application.run_polling()

if __name__ == '__main__':
    main()
