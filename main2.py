import standard.content as st
import telegram_bot.test_bot as tg

my_content = st.get_content()

for item in my_content:
    tg.send_message(item)
