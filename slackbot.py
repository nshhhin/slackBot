# -*- coding: utf-8 -*-
 
from slackbot.bot import Bot
from slackbot.bot import listen_to
from slackbot.bot import respond_to
import random
import slackbot_settings
import csv
import sqlite3
from datetime import datetime
import time
import threading
from slacker import Slacker
import sys
import urllib2
import json
import re
from requests_oauthlib import OAuth1Session
import json
from random import randint
import urllib
import urllib2

#	member : [0]:名前　[1]:twitterID [2]:slackID
member = [
		["XXX","xxx"],
		["YYY","yyy"],
		["ZZZ","zzz"]
]

# 名前,screenname

slack_member = {
	"XXX":"xxx",
	"YYY":"yyy",
	"ZZZ":"zzz"
}

b3_b4_m1 = {
	"XXX":"xxx",
	"YYY":"yyy",
	"ZZZ":"zzz"
}

b4_m1 = {
	"XXX":"xxx",
	"YYY":"yyy",
	"ZZZ":"zzz"
}

b3_b4 = {
	"XXX":"xxx",
	"YYY":"yyy",
	"ZZZ":"zzz"
}

AllMember = {
	"XXX":"xxx",
	"YYY":"yyy",
	"ZZZ":"zzz"
}


b1 = {
	"XXX":"xxx",
	"YYY":"yyy",
	"ZZZ":"zzz"
}

b2 = {
	"XXX":"xxx",
	"YYY":"yyy",
	"ZZZ":"zzz"
}

b3 = {
	"XXX":"xxx",
	"YYY":"yyy",
	"ZZZ":"zzz"
}

b4 = {
	"XXX":"xxx",
	"YYY":"yyy",
	"ZZZ":"zzz"
}

m1 = {
	"XXX":"xxx",
	"YYY":"yyy",
	"ZZZ":"zzz"
}


# オセロのための配列
init_ban = [
	[0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0],
	[0,0,0,1,2,0,0,0],
	[0,0,0,2,1,0,0,0],
	[0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0]
]

question_mode = False
selection_member = ""

APP_URL = 'https://api.apigw.smt.docomo.ne.jp/dialogue/v1/dialogue'

### Constants
oath_key_dict = {
    "consumer_key": "xxx",
    "consumer_secret": "xxx",
    "access_token": "xxx",
    "access_token_secret": "xxx"
}


class DocomoChat(object):
    u"""Docomoの雑談対話APIでチャット"""

    def __init__(self, api_key):
        super(DocomoChat, self).__init__()
        self.api_url = APP_URL + '?APIKEY=%s'%(api_key)
        self.context, self.mode = None, None

    def __send_message(self, input_message='', custom_dict=None):
        req_data = {'utt': input_message}
        if self.context:
            req_data['context'] = self.context
        if self.mode:
            req_data['mode'] = self.mode
        if custom_dict:
            req_data.update(custom_dict)
        request = urllib2.Request(self.api_url, json.dumps(req_data))
        request.add_header('Content-Type', 'application/json')
        try:
            response = urllib2.urlopen(request)
        except Exception as e:
            print e
            sys.exit()
        return response

    def __process_response(self, response):
        resp_json = json.load(response)
        self.context = resp_json['context'].encode('utf-8')
        self.mode    = resp_json['mode'].encode('utf-8')
        return resp_json['utt'].encode('utf-8')

    def send_and_get(self, input_message):
        response = self.__send_message(input_message)
        received_message = self.__process_response(response)
        return received_message

    def set_name(self, name, yomi):
        response = self.__send_message(custom_dict={'nickname': name, 'nickname_y': yomi})
        received_message = self.__process_response(response)
        return received_message



count_mode = False
calc_mode = False
shiritori_mode = False
chat_mode = False
myName = "ninoshin_bot"

api_key = 'xxxx'
chat = DocomoChat(api_key)
resp = chat.set_name('ninoshin_bot', 'にのしんぼっと')

"""
# data.db 
create table user (
	id integer PRIMARY KEY AUTOINCREMENT,
	user text,
	job text,
	LV integer,
	HP integer,
	AP integer,
	DP integer,
	SP integer
);
"""

@listen_to(u'しりとり')
def startShiritori(message):
    message.send('しらとり')

@listen_to('fuck')
def reaction(message):
    message.react('+1')

@listen_to(u'ずんどこ')
def zun(message):
	generateZunDoko()

def generateZunDoko():
	array_zun = []
	for var in range(0, 5):
		i = random.randint(0,1)
		if( i == 0 ):
			array_zun.append("ずん".encode("utf-8"))
		elif( i == 1 ):
			array_zun.append("どこ".encode("utf-8"))
	print array_zun
	return array_zun

@listen_to(u'オセロ vs @(.*)')
def playOthello(message, params):
	array_num = [":zero:",":one:",":two:",":three:",":four:",":five:",":six:",":seven:",":eight:"]

	user1 = message.channel._client.users[message.body['user']][u'name']
	user1 = str(user1)

	user2 = params

	msg = "🔴：@" + user1 + "(2)"
	msg += "\n"
	msg += "🔵：@" + user2 + "(2)"


	message.send(msg)

	global init_ban

	sql_ban = ""
	for y in range(0,8):
		for x in range(0,8):
			sql_ban += str(init_ban[x][y])

	con = sqlite3.connect("data.db")
	con.execute("insert into othello values (null, '"+user1+"','"+user2+"','" + sql_ban +"')" )
	con.commit()
	con.close()




	msg = ""

	for y in range(0,9):
		for x in range(0,9):

			if x == 0:
				msg += array_num[y]
			elif y == 0:
				msg += array_num[x]
			elif x > 0 and y > 0:
				if init_ban[x-1][y-1] == 0:
					msg +=	"⚪️"
				elif init_ban[x-1][y-1] == 1:
					msg += "🔵"
				elif init_ban[x-1][y-1] == 2:
					msg += "🔴"

		msg += "\n"

	message.send(msg)

@listen_to(u'put (.*)')
def putStone(message,params):
	global init_ban
	print re.match(u"[1-8],[1-8]", params)
	if(re.match(u"[1-8],[1-8]", params) != None):
		args = params.split(",")
		positionX = int(args[0])
		positionY = int(args[1])
		init_ban[positionX-1][positionY-1] = 1
		message.reply(str(positionX) +","+str(positionY)+"におきました")
	else:
		message.reply("『put 1,1』のように置きたい場所を指定してください")

@respond_to(u'get_time')
def getTime(message):
	message.send("ただいまの時刻は"+datetime.now().strftime("%Y/%m/%d %H:%M:%S")+"です")

def dstJanken(message):
	response = ["fist","v","hand","open_hands"]
	i = random.randint(0,len(response)-1)
	message.send(":"+response[i]+":")

@listen_to(u'remind (.*)')
@respond_to(u'remind (.*)')
def setTime(message,params):
	args = params.split(" ")
	if len( args ) == 3:
		time = args[0] + " " + args[1]	# 日付
		msg = args[2]	# メッセージ

		set_datetime = datetime.strptime(time, '%Y/%m/%d %H:%M:%S')
		cur_datetime = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

		con = sqlite3.connect("data.db")
		con.execute("insert into othello values (null, '"+user1+"','"+user2+"','" + sql_ban +"')" )
		con.commit()
		con.close()

		message.send(time +" に \""+msg+ "\" をセットしました")


	else:
		message.send("『remind 年月日(YYYY/MM/DD) 時間(HH:mm:ss) メッセージ』で好きな時刻にメッセージをセットできます")


@listen_to(u'じゃんけん')
def startJanken(message):

	t=threading.Timer(10,dstJanken,[message])
	t.start()


	slack = Slacker(slackbot_settings.API_TOKEN)
	user = message.channel._client.users[message.body['user']][u'name']
	user = str(user)

	ret = slack.chat.post_message(
		message._body['channel'],
		'@'+user+': 下の3つから選んでください。10秒後だしますよ...',
		username=message._client.login_data['self']['name'],
		as_user=True
		)
	ts = ret.body['ts']

	EMOJIS = (
		'v',
		'fist',
		'hand'
		)
	for i in range(0,len(EMOJIS)):
		message._client.webapi.reactions.add(
		name=EMOJIS[i],
		channel=message._body['channel'],
		timestamp=ts
		)
		print message._client.webapi.reactions.get()


@listen_to(u'けいさん')
@listen_to(u'計算')
@listen_to('calc')
def onCalculate(message):
	global calc_mode
	user = message.channel._client.users[message.body['user']][u'name']
	user = str(user)
	message.send('@'+user+': 半角数字で「2+5」みたいに指定してね👇')
	calc_mode = True

@listen_to(u'文字数カウント')
def onCountWord(message):
	global count_mode
	user = message.channel._client.users[message.body['user']][u'name']
	user = str(user)
	message.send('@'+user+': 次にカウントしたい文を入力してね👇')
	count_mode = True


@respond_to(u'おしゃべり開始')
def onChatMode(message):
	global chat_mode
	chat_mode = True
	message.send('会話を終了させたいときは『おしゃべり終了』と声をかけてください')

@respond_to(u'おしゃべり終了')
def offChatMode(message):
	global chat_mode
	chat_mode = False
	message.send('おしゃべりを終了しました')


@listen_to(u'')
def calculate(message):
	countWord(message)
	global calc_mode
	if calc_mode == True :
		user = message.channel._client.users[message.body['user']][u'name']
		user = str(user)
		text = message.body[u'text']
		text2 = text.encode('utf-8')
		if text2.find('計算') == -1 :
			message.send('@'+user+': '+str(eval(text2)) +' だと思います')
			calc_mode = False

def countWord(message):
	global count_mode
	if count_mode == True :
		user = message.channel._client.users[message.body['user']][u'name']
		user = str(user)
		text = message.body[u'text']
		text2 = text.encode('utf-8')
		if text2.find('文字数カウント') == -1:
			message.send('@'+user+': '+str(len(text))+'字です')
			count_mode = False

@respond_to(u'(.*)')
def sendChat(message,params):
	pattern = r"おしゃべり終了"
	matchedList = re.findall(pattern,params)
	global question_mode
	if(question_mode):
		sendAnswer(message)
		question_mode = False



	if len(matchedList) == 0:
		if chat_mode == True:
			print "aaaa"
			global chat
			global resp
			resp = chat.send_and_get(params)
			message.send(resp)


@listen_to('processing')
def processing(message):
	message.send('SnippetでProcessingのコードうってね')


#	RPG風ゲーム
@listen_to('create status')
@listen_to('ステータス')
def crateStatus(message):

	user = message.channel._client.users[message.body['user']][u'name']
	user = str(user)

	msg = "@"+ user + ": のステータスは\n" 

	jobs = ['戦士','魔法使い','盗人','海賊','売人','格闘家','フードファイター','無職']
	u_job = jobs[random.randint(0,len(jobs)-1)]
	u_Lv = 1
	u_HP = random.randint(1,20)
	u_Attack = random.randint(1,20)
	u_Deffence = random.randint(1,20)
	u_Speed = random.randint(1,20)


	msg += "職業： " + u_job + "\n"
	msg += "Lv： 1 \n"
	msg += "HP： " + str(u_HP) + "\n"
	msg += "攻撃力： " + str(u_Attack) + "\n"
	msg += "防御力： " + str(u_Deffence) + "\n"
	msg += "スピード： " + str(u_Speed) + "\n"

	con = sqlite3.connect("data.db")
	con.execute("insert into user values (null, '"+user+"','"+u_job+"'," + str(u_Lv) + "," + str(u_HP) +"," + str(u_Attack) +","+ str(u_Deffence) +"," + str(u_Speed) +")" )
	con.commit()
	con.close()

	message.send(msg)


@listen_to('show status')
def showStatus(message):

	user = message.channel._client.users[message.body['user']][u'name']
	user = str(user)

	con = sqlite3.connect("data.db")

	c = con.execute(u"select count(*) from user where user = '"+user+"'")

	isExist = False

	for row in c:
		if( row[0] == 1 ):
			isExist = True

	if(isExist):
		c = con.execute(u"select * from user where user = '"+user+"'")

		for row in c:
			msg += "@"+row[1].encode('utf-8')+": のステータスは\n"
			msg += "職業： " + row[2].encode('utf-8') + "\n"
			msg += "Lv： " + str(row[3]) + "\n"
			msg += "HP： " + str(row[4]) + "\n"
			msg += "攻撃力： " + str(row[5]) + "\n"
			msg += "防御力： " + str(row[6]) + "\n"
			msg += "スピード： " + str(row[7]) + "\n"
			
		con.close()
		message.send(msg)

	else:
		message.send("@"+ user + ": のステータスは存在しません")

	
@listen_to('attack')
def attack(message):
	message.send('〜に◯◯ダメージ与えた！！')

@listen_to(u'スーパーヒューマン')
def shiratori(message):
	message.send('俺はスーパーヒューマンじゃねえ！！')

@respond_to(u'問題')
@respond_to(u'tweet')
def getTweet(message):
	global question_mode
	global selection_member
	question_mode = True

	msg = "Q. 誰のツイートでしょう？"
	msg += "\n"
	msg += "===================================="
	msg += "\n"

	i = random.randint(0,len(member)-1)
	selection_member = member[i][0]
	tweets = tweet_search(i, oath_key_dict) #複数検索ワードを指定可能

	
	text = tweets[u"status"][u'text']
	#print "tweet_id:", tweet_id


	msg += text.encode("utf-8")

	Choices_name = []
	
  	Choices_name.append(member[i][0])


  	while(Choices_name[0] == member[i][0]):
  		i = random.randint(0,len(member)-1)

  	Choices_name.append(member[i][0])

  	while(Choices_name[1] == member[i][0] or Choices_name[0] == member[i][0]):
  		i = random.randint(0,len(member)-1)
  	Choices_name.append(member[i][0])


  	random.shuffle(Choices_name)
  	Choices_id = []
  	for i in range(0,3):
  		for _i in range(0,len(member)):
  			if member[_i][0] == Choices_name[i]:
  				Choices_id.append(member[_i][1])

  	msg += "\n"
  	msg += "====================================\n"
  	msg += "{"
  	msg += str(Choices_name[0])
  	msg += ","
  	msg += str(Choices_name[1])
  	msg += ","
  	msg += str(Choices_name[2])
  	msg += "}"
	

	slack = Slacker(slackbot_settings.API_TOKEN)
	
	ret = slack.chat.post_message(
		message._body['channel'],
		msg,
		username=message._client.login_data['self']['name'],
		as_user=True
		)
	ts = ret.body['ts']

	EMOJIS = []
	for i in range(0,3):
		if(Choices_id[i] == "O0omatsuko0O"):
			EMOJIS.append("o0omatsuko0o")
		else:
			EMOJIS.append(Choices_id[i])


	for i in range(0,len(EMOJIS)):
		message._client.webapi.reactions.add(
		name=EMOJIS[i],
		channel=message._body['channel'],
		timestamp=ts
		)

	#print randNum

@respond_to(u'日記')
def sendDiary(message):
	wether = "晴れ"
	msg = ""
	msg += str(datetime.now().strftime("%Y年 %m月 %d日"))
	msg += "\n"
	msg += "天気：" + wether
	msg += "\n"
	msg += "今日もいろいろあった"
	msg += "\n"
	msg += "おしまい"
	message.send(msg)


@listen_to(u'プロバスケットボール、bjリーグ所属のアルビレックスBBの背中スポンサーになっている会社は？')
@listen_to(u'切り餅のＣＭと言えば？')
@listen_to(u'正解')
def sendEtigo(message):
	#	message.send("越後製菓！！！！！！！！！！！！")
	msg = "\n"
	msg+="．　　　　　 　 　　　　　　　　　　　　　　　　 ,.へ \n"
	msg+="　___ 　　　　　　　 　 　 　 　 　　　　　　　　　　　　ﾑ　　i \n"
	msg+="「 ﾋ_i〉　　　 　 　　　　　　 　 　　　　　　　　　　　　 ゝ　〈 \n"
	msg+="ﾄ　ノ 　　　　　　　　　　　　　　　　　　　　　　　　　　iニ(() \n"
	msg+="		i 　{ 　 　　　　　　　 　　　＿＿＿_ 　 　　　　　　　　| 　ヽ \n"
	msg+="　i　　i　　　 　　　　　　　／__,　 , ‐-＼ 　 　 　 　 　　i 　　} \n"
	msg+="	　|　　 i　　　　　　 　　／（●) 　 ( ● )＼　　　　　　 {､　 λ \n"
	msg+="　ト－┤.　　　　　　／ 　 　（__人__） 　　　＼　　　 ,ノ　￣ ,! \n"
	msg+="　i　　　ゝ､_ 　　　　|　　　　　´￣` 　 　　　　|　,. '´ﾊ　　　,! \n"
	msg+=".　ヽ、 　　　｀`　､,__＼ 　　 　 　　　　　 　 ／　＼ 　ヽ／ \n"
	msg+="　　　＼ノ　ﾉ　　　ﾊ￣r/:::r―--―/::７　　 ﾉ　　　　／ \n"
	msg+="　 　　 　 ヽ.　　　　　　ヽ::〈； . '::. :' |::/　　 /　　　,.  \n"
	msg+="　　　　　 `ｰ ､　　　　＼ヽ::. ;::：|/　　　　　ｒ' \n"
	msg+="　　　／￣二二二二二二二二二二二二二二二二ヽ \n"
	msg+="　　　| 答 |　　　　　コ　ロ　ン　ビ　ア　　　　　　　│| \n"
	msg+="　　　　＼＿二二二二二二二二二二二二二二二二ノ \n"



	message.send(msg)


@listen_to(u'答え')
def sendAnswer(message):
	global selection_member
	for i in range(0,len(member)):
		if( member[i][0] == selection_member ):
			id = i

	message.send("正解は"+selection_member+":"+member[id][1]+":")


def create_oath_session(oath_key_dict):
    oath = OAuth1Session(
    oath_key_dict["consumer_key"],
    oath_key_dict["consumer_secret"],
    oath_key_dict["access_token"],
    oath_key_dict["access_token_secret"]
    )
    return oath

def tweet_search(id, oath_key_dict):
    # url = "https://api.twitter.com/1.1/search/tweets.json?"
    url = "https://api.twitter.com/1.1/users/show.json?"
   
    params = {
        "screen_name": member[id][1]
        }

    oath = create_oath_session(oath_key_dict)
    responce = oath.get(url, params = params)
    if responce.status_code != 200:
        print "Error code: %d" %(responce.status_code)
        return None
    tweets = json.loads(responce.text)
    return tweets

@respond_to(u'help')
def return_help(message):
	msg = "コマンド一覧"
	msg += "\n"
	msg += "\n"
	msg += "respond_to機能"
	msg += "\n"
	msg += "・remind YYYY:MM:DD hh:mm:ss 要件" + "→" + "(要件)を指定時間に通知する"
	msg += "\n"
	msg += "・get_time" + "→" + "現在時刻を取得する"
	msg += "\n"
	msg += "・put [1-8],[1-8]" + "→" + "オセロのコマを置く"
	msg += "\n"
	msg += "・問題" + "→" + "ツイート誰でしょうクイズをする"
	msg += "\n"
	msg += "\n"
	msg += "listen_to機能"
	msg += "\n"
	msg += "・計算" + "→" + "計算モードにする"
	msg += "\n"
	msg += "・文字数カウント" + "→" + "文字数カウントモードにする"
	msg += "\n"
	msg += "・日記" + "→" + "botの日記を確認する"
	message.send(msg)

def setTime(message,params):
	args = params.split(" ")
	if len( args ) == 3:
		time = args[0] + " " + args[1]	# 日付
		msg = args[2]	# メッセージ

		set_datetime = datetime.strptime(time, '%Y/%m/%d %H:%M:%S')
		cur_datetime = datetime.now().strftime("%Y/%m/%d %H:%M:%S")


@respond_to(u'チェックしてないのは誰？ (.*)')
@listen_to(u'チェックしてないのは誰？ (.*)')
@respond_to(u'チェックしていないのは誰？ (.*)')
@listen_to(u'チェックしていないのは誰？ (.*)')
@respond_to(u'チェック (.*)')
@listen_to(u'チェック (.*)')
@respond_to(u'check (.*)')
@listen_to(u'check (.*)')
@respond_to(u'checkReaction (.*)')
@listen_to(u'checkReaction (.*)')
def checkReaction(message,params):

	
	args = params.split(" ")

	if ( len(args) == 2 ):
		slack = Slacker("xxx")

		url = args[0] #確認したいメンションのリンク
		mesId = url.split("/p")[1] # messageIDの取得 p以下
		mesId = mesId[0:len(mesId)-1]
		url = url [1:len(url)-1]
		
		mesId_bef = mesId[0:10] # XXXXXX.XXXXの形にする
		mesId_aft = mesId[10:len(mesId)]
		mesId = mesId_bef + "." + mesId_aft

		group = args[1] #対象とするグループ

		msgChannel = message.body["channel"]

		reactions = slack.reactions.get(channel= msgChannel, timestamp=mesId).body["message"]["reactions"]
		for t in range(0,len(reactions)):
			raw_data = slack.reactions.get(channel= msgChannel, timestamp=mesId).body["message"]["reactions"][t]["users"]
			for row in raw_data:
				if( group == "b1" ):
					forcus = b1
					person = b1.get(slack.users.info(user=row).body["user"]["name"])
				elif( group == "b2" ):
					forcus = b2
					person = b2.get(slack.users.info(user=row).body["user"]["name"])
				elif( group == "b3" ):
					forcus = b3
					person = b3.get(slack.users.info(user=row).body["user"]["name"])
				elif( group == "b4" ):
					forcus = b4
					person = b4.get(slack.users.info(user=row).body["user"]["name"])
				elif( group == "m1" ):
					forcus = m1
					person = m1.get(slack.users.info(user=row).body["user"]["name"])
				elif( group == "b4_m1" ):
					forcus = b4_m1
					person = b4_m1.get(slack.users.info(user=row).body["user"]["name"])
				elif( group == "b3_b4" ):
					forcus = b3_b4
					person = b3_b4.get(slack.users.info(user=row).body["user"]["name"])
				elif( group == "b3_b4_m1" ):
					forcus = b3_b4_m1
					person = b3_b4_m1.get(slack.users.info(user=row).body["user"]["name"])
				elif( group == "all" ):
					forcus = AllMember
					person = AllMember.get(slack.users.info(user=row).body["user"]["name"])

				if person != None:
					print slack.users.info(user=row).body["user"]["name"] + ":" + row
					del forcus[slack.users.info(user=row).body["user"]["name"]]

		text = "" # 返信する内容
		for row in forcus:
			text += "@" + row +" , "

		text = url + "\n" + "⬇️チェックしていない人たちはこの人たちですよ⬇️" + "\n"+ text

		message.send( text )


@respond_to(u'なりすまし (.*)')
@listen_to(u'なりすまし (.*)')
def narisumashi(message,params):
	args = params.split(" ")
	if len( args ) == 3:
		channel = args[0] # チャンネル名
		userName = args[1]	# メッセージ
		text = args[2]

		channel_name = "#" + channel
		slack = Slacker("xxx")
        slack.chat.post_message(channel_name,text, username = userName, icon_emoji=':bust_in_silhouette:')

@respond_to(u'今日の議事録')
@listen_to(u'今日の議事録')
def todayMeeting(message):
	today = datetime.now().strftime("%Y.%m.%d")
	message.send("https://scrapbox.io/nkmr-lab/" + today)

@listen_to(u'グループ (.*)')
def group(message,params):
	url = "https://slack.com/api/usergroups.list"
	args = params.split(" ")
	query = {
		'token':'xxx'
		}

	query = urllib.urlencode(query)
	req = urllib2.Request(url)
	# ヘッダ追加
	req.add_header('Content-Type', 'application/x-www-form-urlencoded')
	# パラメータ追加
	req.add_data(params)
	res = urllib2.urlopen(req)
	# レスポンス取得
	body = res.read()
	print body
	groupName = args[0]
	slack = Slacker("xxx")
	message.send("グループ名:" + groupName)


def main():

	bot = Bot()
	bot.run()

if __name__ == "__main__":

    main()


