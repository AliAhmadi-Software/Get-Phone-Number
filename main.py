"""INFO:    Get Id Gp-980422"""

from pyrogram import Client,Filters
from pyrogram.errors import UserAlreadyParticipant
import time,os,re
from pandas import DataFrame
from utils import *

app=Client("getId_app",
   api_id=1400416,
    api_hash='890c54c2f48c2d423550831c661d7e3a')

B_memberList="لیست شماره"
B_joinGroup="جوین "
B_help="راهنما"
Q_countMember="تعداد کل ممبر های گروه : {} 👥" \
              "\nتعداد کل شماره ها : {} 📞"
Q_gettingMember=" ♻در حال استخراج ... " \
                "{:.1f}% ♻"
Q_readyFile=" ♻در حال آماده سازی فایل ... "
Q_doneMember="✅✅✅Done✅✅✅"
Q_memberList="لیست ممبر گروه :" \
                   "\n\n{}"
Q_joinGroup="اکانت با موفقیت عضو گروه شد.✅"
W_joinGroup="هنگام عضو شدن در گروه خطا رخ داد.⚠"
Q_help="💬 جوین [لینک/ایدی]" \
       "\n<b>" \
       "♦️ انتخاب گروه برای استخراج شماره کاربران" \
       "\n『توجه : قبل از استفاده از دستور 'لیست شماره' باید از دستور جوین استفاده شود.』" \
       "</b>" \
       "\n\n💬 لیست شماره" \
       "\n<b>" \
       "♦️ دریافت لیست شماره اعضا به صورت فایل VCF" \
       "</b>" \
       "\n\n💬 راهنما" \
       "\n<b>" \
       "♦️ باز کردن لیست فعلی" \
       "</b>"
warn="خطا!⚠"

app.start()
Id_AdminDebug='asnbl'
Id_Admins=[Id_AdminDebug,"me",106909240,1193374705]
Id_group=0
app.send_message(Id_AdminDebug,'a')
@app.on_message(Filters.chat(Id_Admins) & Filters.text)
class get_id:

    def __init__(self, client, message):
        self.message=message
        self.client=client
        self.user_id=self.message.from_user.id
        try:
            self.run()
        except Exception as e:
            app.send_message(self.message.chat.id,repr(e))
        # self.run()

    def run(self):
        global Id_group
        if self.message.text==B_memberList:
            self.typing()
            total=0
            totalNumbers=0
            NumbersList=[]
            NameList=[]
            title=self.client.get_chat(Id_group).title
            try:
                totalMember=self.client.get_chat_members_count(chat_id=Id_group)
                members=self.client.iter_chat_members(chat_id=Id_group)
            except:return self.message.reply(warn)
            mssgId=self.message.reply(Q_gettingMember.format(0)).message_id

            for member in members:
                total+=1
                print(total)
                data=search_db_telegram(member.user.id)
                if data!=None:
                    totalNumbers+=1
                    NumbersList.append("+"+str(data[2]))
                    NameList.append(member.user.first_name)

                if total%600==0:
                    self.client.edit_message_text(
                    chat_id=self.message.chat.id,message_id=mssgId,text=Q_gettingMember.format(total*100/totalMember))
                elif total==totalMember:
                    break

            self.client.edit_message_text(
                    chat_id=self.message.chat.id,message_id=mssgId,
                    text=Q_doneMember)

            self.client.edit_message_text(
                    chat_id=self.message.chat.id,message_id=mssgId,
                    text=Q_readyFile)
            df = DataFrame({'TEL': NumbersList , "Name": NameList})
            print(df)
            df.to_excel('{}.xlsx'.format(title), sheet_name='sheet', index=False)
            self.client.send_chat_action(self.user_id,"upload_document")
            self.client.send_document(chat_id=self.message.chat.id,document="{}.xlsx".format(title),caption=Q_countMember.format(totalMember,totalNumbers))
            os.system('rm "{}.xlsx"'.format(title))

        elif self.message.text.startswith(B_joinGroup):
            self.typing()
            group=self.message.text.replace(B_joinGroup,'',1)
            chat_id=0
            try:
                chat_id=app.join_chat(chat_id=group).id
            except UserAlreadyParticipant:chat_id=app.get_chat(chat_id=group).id
            except:pass
            if chat_id==0:
                self.message.reply(W_joinGroup)
            else:
                Id_group=chat_id
                print(chat_id)
                self.message.reply(Q_joinGroup)

        elif self.message.text==B_help:
            self.message.reply(Q_help,parse_mode='html')

    def typing(self):
        self.client.send_chat_action(self.user_id,"typing")
        time.sleep(0.3)
