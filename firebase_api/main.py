import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from bs4 import BeautifulSoup
import urllib
from urllib.request import urlopen
from urllib.parse import urlencode, unquote, quote_plus



#Firebase database 인증 및 앱 초기화
cred = credentials.Certificate('myKey.json')
firebase_admin.initialize_app(cred,{
    'databaseURL' : '파이어베이스 주소'
})

# ref = db.reference() #db 위치 지정
# ref.update({'반원' : '고슴도치'}) #해당 변수가 없으면 생성한다.
#
# ref = db.reference('강좌/파이썬') #경로가 없으면 생성한다.
# ref.update({'파이썬 레시피 웹 활용' : 'complete'})
# ref.update({'파이썬 괴식 레시피' : 'Proceeding'})
#
# #리스트 전송시
# ref = db.reference() #db 위치 지정
# ref.update({'수강자' : ['구독자A','구독자B','구독자C','구독자D']}) #해당 변수가 없으면 생성한다.
#
# #데이터베이스 레퍼런스 생성 후 데이터 읽기
# ref = db.reference('없는 경로') #이 당시의 데이터가 확인된다.
# print(ref.get()) #특정값이 가져와지거나
#
# ref = db.reference('반원')
# print(ref.get())
#
# ref = db.reference('강좌/파이썬')
# print(ref.get()) #json형태로 받아와 진다.
#
# ref = db.reference('수강자')
# print(ref.get()) #list로 반환

def get_url():
    url = 'api url'
    return url

def request_url(url):
    result = requests.get(url)
    bs_obj = BeautifulSoup(result.content, "html.parser")
    return bs_obj

i = 0
bs_obj = request_url(get_url())
# totalCount = bs_obj.find('totalcount')
result = request_url(get_url())
# print(result)
# <create_date>2021/04/24 18:56:05</create_date>
# <location_id>188</location_id>
# <location_name>전라남도 무안군</location_name>
# <md101_sn>103221</md101_sn>
# <msg>[무안군청]4.25.(일)09:00~18:00 무안군보건소 및 남악복합주민센터, 오룡행복초등학교에서 임시선별검사소 운영 예정이오니 검사 받으시기 바랍니다.</msg>
# <send_platform>cbs</send_platform>
# print(result)



# for tag in result.findAll('row'):
#     ref = db.reference('Msg/DisasterMsg/row/' + str(i)) # db 위치 지정
#     i = i + 1
#     create_date = tag.create_date
#     location_id = tag.location_id
#     location_name = tag.location_name
#     md101_sn = tag.md101_sn
#     msg = tag.msg.string
#     send_platform = tag.send_platform
#     print(create_date.string)
#     print(location_id.string)
#     print(location_name.string)
#     print(md101_sn.string)
#     print(msg.string)
#     print(send_platform.string)
#     ref.update(
#         {"create_date": create_date.string, "location_id": location_id.string, "location_name": location_name.string,
#          "md101_sn": md101_sn.string, "msg": msg, "send_platform": send_platform.string})

ref = db.reference('Msg/DisasterMsg/row/' + str(0))
tmp = ref.get()
print(tmp is None)

if tmp is None:
    for tag in result.findAll('row'):
        ref = db.reference('Msg/DisasterMsg/row/' + str(i)) # db 위치 지정
        i = i + 1
        create_date = tag.create_date
        location_id = tag.location_id
        location_name = tag.location_name
        md101_sn = tag.md101_sn
        msg = tag.msg.string
        send_platform = tag.send_platform
        print(create_date.string)
        print(location_id.string)
        print(location_name.string)
        print(md101_sn.string)
        print(msg.string)
        print(send_platform.string)
        ref.update(
            {"create_date": create_date.string, "location_id": location_id.string, "location_name": location_name.string,
             "md101_sn": md101_sn.string, "msg": msg, "send_platform": send_platform.string})

else:
    for tag in result.findAll('row'):
        ref = db.reference('Msg/DisasterMsg/row/' + str(i)) # db 위치 지정


ref = db.reference('Msg/DisasterMsg/row/' + str(0))  # db 위치 지정
ref.update(
    {"create_date": "bc"})
# print(ref.get(0))

    # ref.update({"location_id":location_id.string})
    # ref.update({"location_name":location_name.string})
    # ref.update({"md101_sn":md101_sn.string})
    # ref.update({"msg": msg})
    # ref.update({"send_platform": send_platform.string})