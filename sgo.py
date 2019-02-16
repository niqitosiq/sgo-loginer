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

cookiesLogin["NSSESSIONID"] = cookiesGeted["NSSESSIONID"]


#hashing and get two type of keys

print("\n", "-------- HASHING PASSWORD --------", "\n")


hash = hashlib.md5()
nhash = hashlib.md5((args.pwd).encode('utf-8')).hexdigest()
pwd2 = hashlib.md5((salt + nhash).encode('utf-8')).hexdigest()
print("pw2: " + pwd2)

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
end_req = requests.post("https://sgo.volganet.ru/webapi/login", data=logindata, cookies=cookiesLogin)

print("\n Responce code: " + str(end_req) + "; Response text: " + end_req.text + "; Cookies: " + str(end_req.cookies.get_dict()))