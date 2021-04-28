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


def getpageNo_url(pageNo):
    url = 'api_PageNo변수를 넣는 주소'
    return url

def getnumOfRows_url(numOfRows):
    url = 'api_numOfRows변수를 넣는 주소'
    return url

def request_url(url):
    result = requests.get(url)
    bs_obj = BeautifulSoup(result.content, "html.parser")
    return bs_obj


flag = db.reference('Msg/DisasterMsg/row/' + str(0)).get()
print(flag)


if flag is None:
    MsgCount = db.reference('Msg/DisasterMsg/MsgCount/')
    for i in range(0, 2000):
        result = request_url(getpageNo_url(2000 - i))

        for tag in result.findAll('row'):
            ref = db.reference('Msg/DisasterMsg/row/' + str(i)) # db 위치 지정
            create_date = tag.create_date
            location_id = tag.location_id
            location_name = tag.location_name
            md101_sn = tag.md101_sn
            msg = tag.msg.string
            send_platform = tag.send_platform
            print(str(2000-i) + '번째 메세지를 저장했습니다.')
            ref.update(
                {"create_date": create_date.string, "location_id": location_id.string, "location_name": location_name.string,
                 "md101_sn": md101_sn.string, "msg": msg, "send_platform": send_platform.string})
            MsgCount.update({'totalCount': str(i+1)})

# else:
#     MsgCount = db.reference('Msg/DisasterMsg/MsgCount/')    # totalCount를 저장하기 위한 참조
#     MsgCountref = db.reference('Msg/DisasterMsg/MsgCount/totalCount')   # totalCount 값 참조
#
#     Updatecount = 0  # 몇 개의 메시지가 추가로 들어왔는지 계산하기 위한 변수
#     totalCount = int(MsgCountref.get())  # 디비가 가지고 있는 메시지 갯수
#     lastindex = totalCount - 1 # totalCount - 1
#
#     endPoint = db.reference('Msg/DisasterMsg/row/' + str(lastindex) + '/md101_sn')  # 마지막 메세지 md101 저장
#     result = request_url(getnumOfRows_url(20)) # 메세지 100개 요청
#     # print(endPoint.get())
#     i = 0       # API에서 데이터를 받아올 때 인덱스로 쓸 변수
#     print("현재 저장된 토탈카운트: " + str(totalCount))
#
#     tmp = 0     # range 함수를 쓰기 위한 변수
#     index = 0   # firebase DB에서 인덱스 계산을 위한 변수
#     for tag in result.findAll('row'):
#         md101_sn = int(tag.md101_sn.string)     # 현재 저장하려는 메시지의 고유번호
#         Updatecount = md101_sn - int(endPoint.get())   # API에서 가장 최신에 갱신된 md101_sn 에서 firebase에 가장 마지막에 저장된 md101_sn을 빼서 차를 구함
#         print("받아와야 하는 메세지 갯수: " + str(Updatecount))
#         break                                   # -> DB에 메세지가 저장된 이후로 몇 개의 데이터가 들어왔는지 알 수 있음
#
#         # if md101_sn == endPoint.get():    # 현재 저장하려는 메시지의 고유번호가 이미 저장된 고유번호라면 멈춤, 그렇지 않으면 진행
#         #     print(count)
#         #     break
#         # count += 1  # 현재 저장하려는 메시지의 고유번호가 이미 저장된 고유번호가 아니라면 카운트 추가
#
#     if Updatecount != 0:    # 새로 들어온 메시지가 있으면,
#         for i in range(0, Updatecount):
#             result = request_url(getpageNo_url(Updatecount - i))    # Updatecount - 0,
#
#             for tag in result.findAll('row'):
#                 lastindex = lastindex + 1
#                 ref = db.reference('Msg/DisasterMsg/row/' + str(lastindex))  # db 위치 지정
#                 create_date = tag.create_date
#                 location_id = tag.location_id
#                 location_name = tag.location_name
#                 md101_sn = tag.md101_sn
#                 msg = tag.msg.string
#                 send_platform = tag.send_platform
#                 print(str(lastindex) + '번에 메세지를 저장했습니다.')
#                 ref.update(
#                     {"create_date": create_date.string, "location_id": location_id.string,
#                      "location_name": location_name.string,
#                      "md101_sn": md101_sn.string, "msg": msg, "send_platform": send_platform.string})
#                 MsgCount.update({'totalCount': str(lastindex+1)})



        # for tmp in range(0, totalCount):
        #     # 현재 index에 있는 "데이터"를 가져와서
        #     # 위 for문에서 계산한 Updatecount만큼 기존 데이터들의 인덱스를 뒤로 이동시킴
        #     ref = db.reference('Msg/DisasterMsg/row/' + str(index)).get()
        #     moveref = db.reference('Msg/DisasterMsg/row/' + str(index + Updatecount))
        #     print(index + Updatecount)
        #     moveref.update(ref)
        #     index = index + 1
        #     tmp += 1
        #
        # totalCount = totalCount + Updatecount
        # print("저장되는 토탈카운트: " + str(totalCount))
        # MsgCount.update({'totalCount': str(totalCount)})   # 추가되는 메시지 갯수만큼 디비가 가지고 있는 메시지 갯수 업데이트
        #
        # for tag in result.findAll('row'):
        #     # 인덱스 0번째부터 새로 들어온 데이터들을 저장하고
        #     # md101_sn 이 이미 저장된 번호라면 저장을 멈추고 종료.
        #     ref = db.reference('Msg/DisasterMsg/row/' + str(i))  # db 위치 지정
        #     md101_sn = tag.md101_sn.string
        #     if md101_sn == endPoint.get():    # 현재 저장하려는 메시지의 고유번호가 이미 저장된 고유번호라면 멈춤, 그렇지 않으면 진행
        #         break
        #
        #     create_date = tag.create_date
        #     location_id = tag.location_id
        #     location_name = tag.location_name
        #     msg = tag.msg.string
        #     send_platform = tag.send_platform
        #     print(create_date.string)
        #     print(location_id.string)
        #     print(location_name.string)
        #     print(md101_sn.string)
        #     print(msg.string)
        #     print(send_platform.string)
        #
        #     ref.update(
        #         {"create_date": create_date.string, "location_id": location_id.string,
        #          "location_name": location_name.string,
        #          "md101_sn": md101_sn.string, "msg": msg, "send_platform": send_platform.string})
        #     i = i + 1

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

# endPoint = db.reference('Msg/DisasterMsg/row/0/md101_sn')   # 0번째 메시지에 재난문자 고유값 저장해둠
# flag = db.reference('Msg/DisasterMsg/row/' + str(0)).get()
# print(flag)
#
#
# if flag is None:
#     MsgCount = db.reference('Msg/DisasterMsg/MsgCount/')
#
#     for tag in result.findAll('row'):
#         ref = db.reference('Msg/DisasterMsg/row/' + str(i)) # db 위치 지정
#         create_date = tag.create_date
#         location_id = tag.location_id
#         location_name = tag.location_name
#         md101_sn = tag.md101_sn
#         msg = tag.msg.string
#         send_platform = tag.send_platform
#         print(create_date.string)
#         print(location_id.string)
#         print(location_name.string)
#         print(md101_sn.string)
#         print(msg.string)
#         print(send_platform.string)
#         ref.update(
#             {"create_date": create_date.string, "location_id": location_id.string, "location_name": location_name.string,
#              "md101_sn": md101_sn.string, "msg": msg, "send_platform": send_platform.string})
#         i = i + 1
#         MsgCount.update({'totalCount': str(i)})  # 해당 변수가 없으면 생성한다.
#
# else:
#     MsgCount = db.reference('Msg/DisasterMsg/MsgCount/')
#     MsgCountref = db.reference('Msg/DisasterMsg/MsgCount/totalCount')
#     endPoint = db.reference('Msg/DisasterMsg/row/0/md101_sn')  # 0번째 메시지에 재난문자 고유값 저장해둠
#     # print(endPoint.get())
#
#     i = 0       # API에서 데이터를 받아올 때 인덱스로 쓸 변수
#     Updatecount = 0   # 몇 개의 메시지가 추가로 들어왔는지 계산하기 위한 변수
#     totalCount = int(MsgCountref.get()) # 디비가 가지고 있는 메시지 갯수
#     print("토탈카운트: " + str(totalCount))
#
#     tmp = 0     # range 함수를 쓰기 위한 변수
#     index = 0   # firebase DB에서 인덱스 계산을 위한 변수
#     for tag in result.findAll('row'):
#         md101_sn = int(tag.md101_sn.string)     # 현재 저장하려는 메시지의 고유번호
#         Updatecount = md101_sn - int(endPoint.get())   # API에서 가장 최신에 갱신된 md101_sn 에서 firebase에 가장 최근에 저장된 md101_sn을 빼서 차를 구함
#         print("업데이트 카운트: " + str(Updatecount))
#         break                                   # -> DB에 메세지가 저장된 이후로 몇 개의 데이터가 들어왔는지 알 수 있음
#
#
#         # if md101_sn == endPoint.get():    # 현재 저장하려는 메시지의 고유번호가 이미 저장된 고유번호라면 멈춤, 그렇지 않으면 진행
#         #     print(count)
#         #     break
#         # count += 1  # 현재 저장하려는 메시지의 고유번호가 이미 저장된 고유번호가 아니라면 카운트 추가
#
#     if Updatecount != 0:    # 새로 들어온 메시지가 있으면,
#
#         for tmp in range(0, totalCount):
#             # 현재 index에 있는 "데이터"를 가져와서
#             # 위 for문에서 계산한 Updatecount만큼 기존 데이터들의 인덱스를 뒤로 이동시킴
#             ref = db.reference('Msg/DisasterMsg/row/' + str(index)).get()
#             moveref = db.reference('Msg/DisasterMsg/row/' + str(index + Updatecount))
#             print(index + Updatecount)
#             moveref.update(ref)
#             index = index + 1
#             tmp += 1
#
#         totalCount = totalCount + Updatecount
#         print("저장되는 토탈카운트: " + str(totalCount))
#         MsgCount.update({'totalCount': str(totalCount)})   # 추가되는 메시지 갯수만큼 디비가 가지고 있는 메시지 갯수 업데이트
#
#         for tag in result.findAll('row'):
#             # 인덱스 0번째부터 새로 들어온 데이터들을 저장하고
#             # md101_sn 이 이미 저장된 번호라면 저장을 멈추고 종료.
#             ref = db.reference('Msg/DisasterMsg/row/' + str(i))  # db 위치 지정
#             md101_sn = tag.md101_sn.string
#             if md101_sn == endPoint.get():    # 현재 저장하려는 메시지의 고유번호가 이미 저장된 고유번호라면 멈춤, 그렇지 않으면 진행
#                 break
#
#             create_date = tag.create_date
#             location_id = tag.location_id
#             location_name = tag.location_name
#             msg = tag.msg.string
#             send_platform = tag.send_platform
#             print(create_date.string)
#             print(location_id.string)
#             print(location_name.string)
#             print(md101_sn.string)
#             print(msg.string)
#             print(send_platform.string)
#
#             ref.update(
#                 {"create_date": create_date.string, "location_id": location_id.string,
#                  "location_name": location_name.string,
#                  "md101_sn": md101_sn.string, "msg": msg, "send_platform": send_platform.string})
#             i = i + 1
#
#
#
#         # create_date = tag.create_date
#         # location_id = tag.location_id
#         # location_name = tag.location_name
#         # msg = tag.msg.string
#         # send_platform = tag.send_platform
#         # ref.update(
#         #     {"create_date": create_date.string, "location_id": location_id.string,
#         #      "location_name": location_name.string,
#         #      "md101_sn": md101_sn.string, "msg": msg, "send_platform": send_platform.string})
#         #
#         # i = i+1
# #
# #
# #
# # # ref = db.reference('Msg/DisasterMsg/row/' + str(0))  # db 위치 지정
# # # ref.update(
# # #     {"create_date": "bc"})
# # # print(ref.get(0))
# #
# #     # ref.update({"location_id":location_id.string})
# #     # ref.update({"location_name":location_name.string})
# #     # ref.update({"md101_sn":md101_sn.string})
# #     # ref.update({"msg": msg})
# #     # ref.update({"send_platform": send_platform.string})