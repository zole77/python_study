#-*-coding:utf-8-*-
import json
import xmltodict
import requests

URL = 'http://apis.data.go.kr/1741000/DisasterMsg3/getDisasterMsg1List?serviceKey=RFGquavKPUrcCE%2BLmZyFZ02tx6tq7lgkoevDFqgSuH%2FrZMZsdI8akZUk5Qe7tO%2FDFrAV%2FhJbr1ABTxX%2BgnBZmA%3D%3D&pageNo=1&numOfRows=1000&type=json'
response = requests.get(URL)
text = response.text

# with open("xml_to_json.xml", 'r', encoding='UTF-8') as f:
xmlString = text

print("xml input (xml_to_json.xml):")
print(xmlString)

jsonString = json.dumps(xmltodict.parse(xmlString), indent=4)

print("\nJSON output(output.json):")
print(jsonString)

with open("xml_to_json.json", 'w', encoding='UTF-8') as f:
    f.write(jsonString)