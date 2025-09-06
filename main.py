from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from kerensky import kerensky
from kollontai import kollontai
from kornilov import kornilov
from lenin import lenin
from martov import martov
from milyukov import milyukov
from ovseenko import ovseenko
from spiridonova import spiridonova
from trotsky import trotsky

active_scenarios = {
    "kerensky": kerensky(),
    "trotsky": trotsky(),
    "ovsenko": ovseenko(),
    "lenin": lenin(),
    "martov": martov(),
    "kollontai": kollontai(),
    "kornilov": kornilov(),
    "spiridonova": spiridonova(),
    "milyukov": milyukov()
}

user_scenarios = {}

async def choose_scenario(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """1917: Вихрь революции  
Ты стоишь на пороге истории. Ветер перемен рвёт старые флаги, улицы Петрограда гуляют под красными знамёнами, а в коридорах власти — шепот заговоров и лязг штыков.  

Кем ты будешь в этом хаосе?  
/kerensky — Временное правительство держится на твоих плечах. Ты пытаешься балансировать между Советами, генералами и народом, который требует хлеба и мира. Но долго ли продержится власть на краю пропасти?  

/trotsky — Ты — пламенный трибун революции. Твои речи воспламеняют толпы, а Ленин ждёт твоего решения: когда ударить? Вопрос не в том, будет ли восстание, а в том, кто его возглавит — и победит.  

/ovsenko — Ты среди матросов-балтийцев, тех, кто первым поднял красный флаг над "Авророй". Но что дальше? Стрелять по Зимнему или искать компромисс? Твой выбор решит судьбу переворота.  

/lenin — Ты — мозг революции. Каждый твой приказ — шаг к диктатуре пролетариата. Но даже среди своих есть предатели. Довериться ли Троцкому? Ждать ли Учредительного собрания? Время не ждёт.  

/martov — Ты веришь в демократическую революцию, но большевики рвутся к власти. Можно ли остановить Ленина без крови? Или твой идеализм погубит тебя?  

/kollontai — Ты борешься не только за революцию, но и за права женщин. Любовь, политика, забастовки — всё сплетено в один клубок. Сможешь ли ты изменить страну, не потеряв себя?  

/kornilov — Генерал, который мог спасти Россию. Но Керенский объявил тебя мятежником. Пойти на Петроград — значит развязать гражданскую войну. Отступить — предать честь.  

/spiridonova — Террористка, революционерка, мученица. Ты готова умереть за крестьянскую правду. Но что сильнее: твоя ненависть к старому миру или страх перед новым?  

/milyukov — Либерал в море радикалов. Ты верил в реформы, но теперь понимаешь: слова ничего не стоят. Поддержать Корнилова? Договориться с Лениным? Или бежать, пока не поздно?"""
    )

async def route_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    command = update.message.text.strip("/")

    if command in active_scenarios:
        user_scenarios[user_id] = command
        await active_scenarios[command].start(update, context)
    else:
        await update.message.reply_text("Сценарий не найден.")

async def route_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    scenario_key = user_scenarios.get(user_id)

    if scenario_key and scenario_key in active_scenarios:
        await active_scenarios[scenario_key].handle_message(update, context)
    else:
        await choose_scenario(update, context)

def main():
    TOKEN = ""
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", choose_scenario))

    app.add_handler(CommandHandler("kerensky", route_start))
    app.add_handler(CommandHandler("trotsky", route_start))
    app.add_handler(CommandHandler("ovsenko", route_start))
    app.add_handler(CommandHandler("lenin", route_start))
    app.add_handler(CommandHandler("martov", route_start))
    app.add_handler(CommandHandler("kollontai", route_start))
    app.add_handler(CommandHandler("kornilov", route_start))
    app.add_handler(CommandHandler("spiridonova", route_start))
    app.add_handler(CommandHandler("milyukov", route_start))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, route_message))
    print("Бот запущен.")
    app.run_polling()

if __name__ == "__main__":
    main()