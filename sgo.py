import requests
import json
import sys
import argparse
import hashlib
from http.cookies import SimpleCookie

# Get all data from command line
parser = argparse.ArgumentParser()
parser.add_argument('-n','--name', dest='name', action='store',
                   help='Inp the name of acc')
parser.add_argument('-p','--pwd', dest='pwd', action='store',
                   help='Inp the password of acc')

args = parser.parse_args()
print(args.name)
print(args.pwd)

print("\n", "-------- POST REQUEST (salt) --------", "\n")

#Get keys for hashing and get login cookies
cookiesLogin = dict(TTSLogin="SCID=1491&PID=-1&CID=2&SID=34&SFT=2&CN=89&BSP=0")

saltPost = requests.post("https://sgo.volganet.ru/webapi/auth/getdata", cookies=cookiesLogin)
#saltPost = '{"lt":"1024887778","ver":"652555995","salt":"122221295"}'
print(saltPost)
responseSalt = json.loads(str(saltPost.text))
cookiesGeted = saltPost.cookies.get_dict()
salt = str(responseSalt["salt"])
print("salt: ", salt)
print("lt: ", str(responseSalt["lt"]))
print("ver: ", str(responseSalt["ver"]))
print("cookies: ", str(cookiesGeted))
print("HEADERS: ", str(saltPost.headers))

cookiesLogin["NSSESSIONID"] = cookiesGeted["NSSESSIONID"]


#hashing and get two type of keys

print("\n", "-------- HASHING PASSWORD --------", "\n")


hash = hashlib.md5()
nhash = hashlib.md5((args.pwd).encode('utf-8')).hexdigest()
pwd2 = hashlib.md5((salt + nhash).encode('utf-8')).hexdigest()
print("pw2: " + pwd2)



loginHeaders = {
	"Accept": "application/json, text/javascript, */*; q=0.01",
	"Accept-Encoding": "gzip, deflate, br",
	"Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
	"Cache-Control": "no-cache",
	"Connection": "keep-alive",
	"Content-Length": "0",
	"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
	"Host": "sgo.volganet.ru",
	"Origin": "https://sgo.volganet.ru",
	"Pragma": "no-cache",
	"Referer": "https://sgo.volganet.ru/about.html",
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
	"X-Requested-With": "XMLHttpRequest"
}
logindata = {
	"LoginType": 1,
	"cid": 2,
	"sid": 34,
	"pid": -1,
	"cn": 89,
	"sft": 2,
	"scid": 1491,
	"UN": args.name,
	"PW": (pwd2)[0:len(args.pwd)],
	"lt": responseSalt["lt"],
	"pw2": pwd2,
	"ver": responseSalt["ver"]
}

print("\n", "-------- END LOGIN DATA --------", "\n")
print("Cookies: " + str(cookiesLogin))
print("\n Logindata text: " +json.dumps(logindata))
end_req = requests.post("https://sgo.volganet.ru/webapi/login", data=logindata, cookies=cookiesLogin, headers=loginHeaders)

print("\n Responce status: " + str(end_req) + "; Response text: " + end_req.text + "; Cookies: " + str(end_req.cookies.get_dict()))



if (end_req.status_code == 200):
	print("\n\n\n\n" + "auth succesful" + "\n\n\n\n")