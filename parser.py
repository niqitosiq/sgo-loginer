import data
import requests
import json

class parser:
	data_array = data.getAuth.getData()
	data = {}
	def postdata(link, data):
		if (data == 0):
			data = {"at": parser.data_array[0]["at"]}
		else:
			data["at"] = parser.data_array[0]["at"]
		page = requests.post(link, headers=parser.data_array[1], data=data, cookies=parser.data_array[2])
		return(page.content.decode("utf-8"))
	def getpage(link):
		print(parser.data_array[0]["at"])
		data["at"] = parser.data_array[0]["at"]
		page = requests.post(link, headers=parser.data_array[1], data=data, cookies=parser.data_array[2])
		return(page.content.decode("utf-8"))


print(parser.getpage('https://sgo.volganet.ru/asp/Reports/Report.asp'))