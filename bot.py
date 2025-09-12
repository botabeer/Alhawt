#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, SourceGroup
from dotenv import load_dotenv

# تحميل القيم من ملف .env
load_dotenv()
CHANNEL_ACCESS_TOKEN = os.getenv("aErk1lTQiebIf/P1d8JQllkU1eebylaSAKQZTkYW3d50WeLncmTlIMyFX9rvttNg347TH6SsLwKSGZTKIxv+JmIFPeye/tK2us6/npBfeYkdkti5YhNz/wJzYszW12IikIDfi5NT1oMeXBRmAL8C0wdB04t89/1O/w1cDnyilFU=")
CHANNEL_SECRET = os.getenv("1841e7af13a02de5400ade57c3fb9bc1")
ADMIN_USER_ID = os.getenv("‏Ub0345b01633bbe470bb6ca45ed48a913")

app = Flask(__name__)
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text.strip()
    user_id = event.source.user_id
    group_id = getattr(event.source, "group_id", None)

    # فقط الأدمن الأساسي يقدر يتحكم
    if user_id != ADMIN_USER_ID:
        return

    # ✅ أوامر عامة
    if text == "!status":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="✅ البوت شغال"))
    elif text == "!settings":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="⚙️ إعدادات الحماية: (محاكاة)"))
    elif text == "!admins":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="👮 قائمة المشرفين: (محاكاة)"))

    # 🔐 أوامر الحماية
    elif text == "!protect on":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="🔐 تم تفعيل الحماية"))
    elif text == "!protect off":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="🔓 تم إيقاف الحماية"))
    elif text == "!antibot on":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="🤖🚫 منع دخول البوتات"))
    elif text == "!antibot off":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="🤖✅ السماح بدخول البوتات"))
    elif text == "!antilink on":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="🚫 تم منع الروابط"))
    elif text == "!antilink off":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="✅ تم السماح بالروابط"))
    elif text == "!autokick on":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="👢 تم تفعيل الطرد التلقائي"))
    elif text == "!autokick off":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="🛑 تم إيقاف الطرد التلقائي"))

    # 👮 أوامر الإدارة
    elif text.startswith("!kick "):
        if group_id:
            target_user = text.split(" ", 1)[1]
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"👢 محاولة طرد {target_user}"))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="❌ الأمر يعمل فقط في القروب"))
    elif text.startswith("!ban "):
        target_user = text.split(" ", 1)[1]
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"🚫 تم حظر {target_user}"))
    elif text.startswith("!unban "):
        target_user = text.split(" ", 1)[1]
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"✅ تم رفع الحظر عن {target_user}"))
    elif text == "!clearban":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="🗑️ تم مسح قائمة الحظر"))

    # ✅ أوامر القوائم
    elif text.startswith("!whitelist add "):
        target_user = text.split(" ", 2)[2]
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"✅ تمت إضافة {target_user} إلى القائمة البيضاء"))
    elif text.startswith("!whitelist remove "):
        target_user = text.split(" ", 2)[2]
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"❌ تمت إزالة {target_user} من القائمة البيضاء"))
    elif text == "!whitelist list":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="📜 القائمة البيضاء: (محاكاة)"))
    elif text == "!blacklist list":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="📜 القائمة السوداء: (محاكاة)"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
