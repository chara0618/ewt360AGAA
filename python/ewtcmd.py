import pickle

import requests
import json
import streamlit as st
from streamlit.components.v1 import html

def testgood(cookies):
    #st.write("开始测试...")
    resp = requests.get(url_baseInfo, headers={'token':cookies.get('token')}, cookies=cookies)
    resp.raise_for_status()
    if not resp.json().get('success'):
        st.error("测试请求失败，错误信息："+resp.json().get('msg'))
        st.error("尝试重新登录。")
        st.stop()
    #st.write("测试成功")
def get_reportId(url_b, params_b, cookies):
    try:
        response_b = requests.get(url_b, params=params_b, cookies=cookies)
        if response_b.status_code == 200:
            response_b_json = response_b.json()
            if response_b_json.get('success'):
                if response_b_json.get('data') and 'reportId' in response_b_json['data']:
                    reportId = response_b_json["data"]["reportId"]
                    return reportId
                else:
                    st.error("解析的JSON数据中缺少必要的键或data为None")
                    st.stop()
            else:
                st.error("请求未成功，错误信息："+response_b_json.get('msg'))
                st.stop()
        else:
            st.error("请求失败，状态码："+str(response_b.status_code))
            st.stop()
    except json.JSONDecodeError:
        st.error("响应内容不是有效的JSON")
        st.stop()
    except Exception as e:
        st.error("发生错误："+str(e))
        st.error("请检查各项内容是否正确填写。")
        st.stop()

def get_sorted_question_ids(url_a, params, cookies):
    try:
        # 发起GET请求
        response_a = requests.get(url_a, params=params, cookies=cookies)

        # 检查响应状态码
        if response_a.status_code == 200:
            # 尝试解析响应内容
            response_a_json = response_a.json()

            # 首先检查success字段
            if response_a_json.get('success'):
                # 检查解析后的数据是否包含必要的键且data不为None
                if response_a_json.get('data') and 'questions' in response_a_json['data']:

                    # 提取题目id
                    questions = response_a_json["data"]["questions"]

                    # 按照questionNo排序
                    sorted_questions = sorted(questions, key=lambda x: x["questionNo"])

                    # 提取排序后的id列表
                    sorted_ids = [question["id"] for question in sorted_questions]

                    return sorted_ids
                else:
                    st.error("解析的JSON数据中缺少必要的键或data为None")
                    st.stop()
            else:
                st.error("请求未成功，错误信息："+response_a_json.get('msg'))
                st.stop()
        else:
            st.error("请求失败，状态码："+str(response_a.status_code))
            st.stop()
    except json.JSONDecodeError:
        st.error("响应内容不是有效的JSON")
        st.stop()
    except Exception as e:
        st.error("发生错误："+str(e))
        st.error("请检查各项内容是否正确填写。")
        st.stop()

def get_questions_list(url_c, params_c, cookies):
    try:
        response_c = requests.post(url_c, json=params_c, cookies=cookies)
        if response_c.status_code == 200:
            response_c_json = response_c.json()
            if response_c_json.get('success'):
                if response_c_json.get('data') and 'questionInfoList' in response_c_json['data']:
                    # 把题目pid以index大小顺序列为列表
                    questionInfoList = response_c_json["data"]["questionInfoList"]
                    #sorted_ql = sorted(questionInfoList, key=lambda x: x["questionNumber"])
                    sorted_ql = questionInfoList
                    sorted_subjective = [question["subjective"] for question in sorted_ql]
                    sorted_pids = [question["questionId"] for question in sorted_ql]
                    sorted_ppids = [question["parentQuestionId"] for question in sorted_ql]
                    return sorted_pids, sorted_ppids,sorted_subjective
                else:
                    st.error("解析的JSON数据中缺少必要的键或data为None")
                    st.stop()
            else:
                st.error("请求未成功，错误信息："+response_c_json.get('msg'))
                st.stop()
        else:
            st.error("请求失败，状态码："+str(response_c.status_code))
            st.stop()
    except json.JSONDecodeError:
        st.error("响应内容不是有效的JSON")
        st.stop()
    except Exception as e:
        st.error("发生错误："+str(e))
        st.error("请检查各项内容是否正确填写。")
        st.stop()


def auto_do_homework(url_d, params_d, data_to_send, cookies):
    global response_d,response_d_a
    try:
        response_d = requests.get(url_d, params=params_d, cookies=cookies)
        response_d_a = requests.post(url_d_a, json=data_to_send, cookies=cookies)

        # if response_d.status_code == 200:
        #     if response_d_a.status_code == 200:
        #         st.write("请求成功，响应数据：", response_d_a.json())
        #     else:
        #         st.write("请求失败，状态码：", response_d_a.status_code)
        # else:
        #     st.write("请求失败，状态码：", response_d.status_code)

    except json.JSONDecodeError:
        st.error("响应内容不是有效的JSON")
        st.stop()
    except Exception as e:
        st.error("发生错误：", str(e))
        st.error("请检查各项内容是否正确填写。")
        st.stop()
    return None

def auto_submit_homework(url_e, data_get, cookies):
    try:
        response_e = requests.post(url_e, json=data_get, cookies=cookies)
        if response_e.status_code != 200:
            st.error("请求失败，状态码："+str(response_e.status_code))
            st.stop()
    except json.JSONDecodeError:
        st.error("响应内容不是有效的JSON")
        st.stop()
    except Exception as e:
        st.error("发生错误："+str(e))
        st.error("请检查各项内容是否正确填写。")
        st.stop()
    return None


def get_right_answer(data, qid, cookies):
    try:
        # 发起POST请求
        response = requests.post(url_f, json=data, cookies=cookies)
        response.raise_for_status()  # 检查HTTP错误状态
        # 解析响应内容
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            st.error("响应内容不是有效的JSON")
            st.stop()
        # 处理父问题和子问题逻辑
        response_data = response_json.get("data", {})
        # 如果是子问题，查找匹配的子问题ID
        if data.get("parentQuestionId") != "0":
            for cq in response_data.get("childQuestions", []):
                if cq.get("id") == qid:
                    return cq.get("rightAnswer", []),cq.get('method', '')
        # 返回主问题的正确答案
        return response_data.get('rightAnswer', []),response_data.get('method', '')
    except requests.exceptions.RequestException as e:
        st.error(f"请求失败: {str(e)}")
        st.stop()
    except Exception as e:
        st.error(f"发生错误: {str(e)}")
        st.error("请检查各项内容是否正确填写。")
        st.stop()

def get_schoolId(cookies):
    try:
        # 获取schoolId
        baseinfo = requests.get(url_baseInfo, cookies=cookies, headers={'token': cookies.get('token')})
        baseinfo.raise_for_status()
        baseinfo_json = baseinfo.json()
        if baseinfo_json.get('data'):
            return baseinfo_json.get('data').get('schoolId')
        else:
            st.error("解析的JSON数据中缺少必要的键或data为None")
            st.stop()
    except requests.exceptions.RequestException as e:
        st.error(f"请求失败: {str(e)}")
        st.stop()
    except Exception as e:
        st.error(f"发生错误: {str(e)}")
        st.error("请检查各项内容是否正确填写。")
        st.stop()

def get_all_homeworkIds(cookies):
    try:
        homeworkIds = []
        schoolId = get_schoolId(cookies)
        # 获取所有任务
        for status in range(0, 3):
            finished_courses = requests.post(url_homeworkInfo, cookies=cookies,  headers={'token':cookies.get('token')},
                                            json={
                                                'schoolId': schoolId,
                                                'subject': None,
                                                "type": None,
                                                "status": status,
                                                "pageIndex": 1,
                                                "pageSize": 20
                                            })
            finished_courses.raise_for_status()
            finished_courses_json = finished_courses.json()
            if finished_courses_json.get('data') or finished_courses_json.get('data') == []:
                for course in finished_courses_json.get('data'):
                    homeworkIds.append(course.get('homeworkId'))
            else:
                st.error("解析的JSON数据中缺少必要的键或data为None")
                st.stop()
        return homeworkIds
    except requests.exceptions.RequestException as e:
        st.error(f"请求失败: {str(e)}")
        st.stop()
    except Exception as e:
        st.error(f"发生错误: {str(e)}")
        st.error("请检查各项内容是否正确填写。")
        st.stop()

def get_finishes_lessons(cookies):
    try:
        # 获取已完成课程
        schoolId = get_schoolId(cookies)
        homeworkIds = get_all_homeworkIds(cookies)
        lessons = requests.post(url_studyRecord, cookies=cookies,  headers={'token':cookies.get('token')}, json={
            "schoolId": schoolId,
            "sceneId": "0",
            "homeworkIds": homeworkIds,
            "sourceType": 2
        })
        lessons.raise_for_status()
        lessons_json = lessons.json()
        if lessons_json.get('data'):
            return lessons_json.get('data')
        else:
            st.error("解析的JSON数据中缺少必要的键或data为None")
            st.stop()
    except requests.exceptions.RequestException as e:
        st.error(f"请求失败: {str(e)}")
        st.stop()
    except Exception as e:
        st.error(f"发生错误: {str(e)}")
        st.error("请检查各项内容是否正确填写。")
        st.stop()

def get_finished_reportId(cookies):
    try:
        lessonIdList = []
        paperIdList = []
        paper_rid = '0'
        homework_rid = '0'
        finished_lessons = get_finishes_lessons(cookies)
        for lesson in finished_lessons:
            if len(lesson.get('contentId')) > 6:
                paperIdList.append(lesson.get('contentId'))
                continue
            lessonIdList.append(lesson.get('contentId'))
        #获取课后习题reportId
        practices = requests.post(url_practice, cookies=cookies, headers={'token':cookies.get('token')}, json={
            "schoolId": "0",
            "lessonIdList": lessonIdList,
            "taskIds": ["0"],
            "homeworkId": "0"
        })
        practices.raise_for_status()
        practices_json = practices.json()
        if practices_json.get('data'):
            for practice in practices_json.get('data'):
                if practice.get('studyTest').get('finishStatus') == 1: #未做课后习题的课程也可能出现在学习记录中
                    homework_rid = practice.get('studyTest').get('reportId')
                    break
            else:
                st.error("未检测到已完成的课后习题!")
                st.stop()
        else:
            st.error("解析的JSON数据中缺少必要的键或data为None")
            st.stop()
        #获取试卷reportId
        if not paperIdList:
            st.error('未检测到已完成的试卷!')
            st.stop()
        paper_rid = get_reportId(url_b, {
            "paperId":paperIdList[0],
            "reportId":"0",
            "platform":"1",
            "bizCode":'205',
            "isRepeat":"1",
            "homeworkId":"0",
            "token":cookies.get('token')
        }, cookies)
        return homework_rid, paper_rid
    except requests.exceptions.RequestException as e:
        st.error(f"请求失败: {str(e)}")
        st.stop()
    except Exception as e:
        st.error(f"发生错误: {str(e)}")
        st.error("请检查各项内容是否正确填写。")
        st.stop()

# 请求的URL
url_a = 'https://web.ewt360.com/api/answerprod/app/answer/summaryReport'
url_b = 'https://web.ewt360.com/api/answerprod/web/answer/report'
url_c = 'https://web.ewt360.com/api/answerprod/common/answer/answerSheetInfo'
url_d = 'https://web.ewt360.com/api/answerprod/app/answer/paper/questions'
url_d_a = 'https://web.ewt360.com/api/answerprod/web/answer/submitAnswer'
url_e = 'https://web.ewt360.com/api/answerprod/web/answer/submitpaper'
url_f = 'https://web.ewt360.com/api/answerprod/web/answer/simple/question/info'
url_baseInfo = 'https://web.ewt360.com/api/usercenter/user/baseinfo'
url_homeworkInfo = 'https://web.ewt360.com/api/homeworkprod/homework/student/getStudentHomeworkInfo'
url_studyRecord = 'https://web.ewt360.com/api/homeworkprod/homework/student/listStudyRecord'
url_practice = 'https://web.ewt360.com/api/homeworkprod/student/homework/task/queryStudentLessonStudyGuideAndPractice'
url_login = 'https://web.ewt360.com/api/authcenter/v2/oauth/login/account'

"""
将cookie填入下方
格式应该为：
cookies = {
    "xxx": "xxxxx",
    "xxx": "xxxxx",
    ………
    "xxx": "xxxxx"
}
"""


def genshin_launch(paperId, homeworkId,bizCode,reportId,paper_rid,homework_rid,cookies,auto_flag,method_flag):
    global sorted_pids, sorted_subjective, index,do_e,do_d,right_answer
    testgood(cookies)
    #st.write("开始分配变量...")
    paperId = paperId
    homeworkId = homeworkId
    bizCode = bizCode
    reportId = reportId
    paper_rid = paper_rid
    homework_rid = homework_rid
    cookies = cookies
    token = cookies.get('token')
    if paper_rid == '0' and homework_rid == '0':
        homework_rid, paper_rid = get_finished_reportId(cookies)
        st.info(f'✅已完成试卷reportId:{homework_rid},已完成课后习题reportId:{paper_rid}')
    with open('reportId.data', 'wb') as f:
        pickle.dump((homework_rid,paper_rid), f)
    if reportId == '0':
        params_b = {
            "paperId":paperId,
            "reportId":"0",
            "platform":"1",
            "bizCode":bizCode,
            "isRepeat":"1",
            "homeworkId":homeworkId,
            "token":token
        }
        #st.write("调用 get_reportId 函数获取 reportId...")
        reportId = get_reportId(url_b, params_b, cookies)
    params_c = {
        "paperId": paperId,
        "reportId": "",
        "platform": "1",
        "bizCode": bizCode,
        "homeworkId": homeworkId,
        "client": "1",
        "token": token,
    }
    if bizCode == '204':
        st.info("✅目标为课后习题")
        params_c['reportId'] = homework_rid
    elif bizCode == '205':
        st.info("✅目标为试卷")
        params_c['reportId'] = paper_rid
    elif bizCode == '201':
        st.warning("⚠️未知目标，按试卷处理")
        params_c['reportId'] = paper_rid
    else:
        st.error("bizCode不正确,请输入完整的链接!")
        st.stop()
    #st.write("调用get_questions_list 函数获取题目列表...")
    sorted_pids, sorted_ppids,sorted_subjective = get_questions_list(url_c, params_c, cookies)

    index = 0
    #st.write("调用for循环，调用auto_do_homework 函数做题...")
    for index, (question_pid,question_ppid,subjective_flag) in enumerate(zip(sorted_pids,sorted_ppids,sorted_subjective), start=1):
        params_d = {
            "paperId": paperId,
            "reportId": params_c['reportId'],
            "platform": "1",
            "questionId":question_pid,
            "parentQuestionId":question_ppid,
            "bizCode": params_c['bizCode']
            # "homeworkId": "0",
            # "token": token
        }
        qid = question_pid
        if question_ppid != "0":
            params_d["questionId"] = question_ppid
        right_answer,method = get_right_answer(params_d,qid, cookies)
        # 检查答案是否为主观题
        if subjective_flag:
            st.success(f"问题{index}: 如下")
            answer_all = '<div style="background-color:White;">'
            for answer_content in right_answer:
                answer_all = answer_all + answer_content + '&nbsp&nbsp&nbsp&nbsp'
            answer_all = answer_all.replace('</div>', '')
            answer_all = answer_all + '</div>'
            html(answer_all,scrolling=True,height=100)
            #     # 提取文本内容和图片URL
            #     text_content = re.sub('<.*?>', '', answer_content)
            #     # 移除所有HTML标签
            #     text_content = unescape(text_content)  # 将HTML实体转换为对应的字符
            #     text_all = text_all + text_content + ' '
            #     image_urls = re.findall('src="([^"]+)"', answer_content)
            #     image_urls_all.extend(image_urls)
            # st.success(f"问题{index}: {text_all}")
            # for i, img_url in enumerate(image_urls_all, start=1):
            #     st.write(f"  图片{i}: {img_url}")
        else:
            answer_all = ''
            for answer_content in right_answer:
                answer_all = answer_all + answer_content + ' '
            st.success(f"问题{index}: {answer_all} ")
        if method_flag:
            html('<div style="background-color:White;">'+method+'</div>',scrolling=True,height=300)
        # 自动答题
        if auto_flag:
            if subjective_flag:
                data_to_send = {
                    "paperId": paperId,
                    "reportId": reportId,
                    "platform": "1",
                    "questionList": [
                        {
                            "id": question_pid,
                            "attachmentImages":[
                                "https://img2.ewt360.com/1028%2F8911%2F0-4808d706-3b0c-433c-9873-e5b45553059e.png"
                            ],
                            "totalSeconds": 14,
                            "questionNo": 1,
                            "cateId": 1,
                            "assignPoints": False
                        }
                    ],
                    "bizCode": params_c['bizCode'],
                    "homeworkId": homeworkId,
                    "assignPoints": False
                }
            else:
                data_to_send = {
                    "paperId": paperId,
                    "reportId": reportId,
                    "platform": "1",
                    "questionList": [
                        {
                            "id": question_pid,
                            "myAnswers": right_answer,
                            "totalSeconds": 14,
                            "questionNo": 1,
                            "cateId": 1,
                            "assignPoints": False
                        }
                    ],
                    "bizCode": params_c['bizCode'],
                    "homeworkId": homeworkId,
                    "assignPoints": False
                }
            params_d["questionId"] = question_pid
            auto_do_homework(url_d, params_d, data_to_send, cookies)
    # 自动提交
    if auto_flag:
        data_get = {
            "paperPackageId": 0,
            "paperId": paperId,
            "reportId": reportId,
            "bizCode": params_c['bizCode'],
            "platform": "1",
            "totalSeconds": 14 * index,
            "homeworkId": homeworkId
        }
        auto_submit_homework(url_e, data_get, cookies)
        st.success(f'自动作答完成。')
    # 要发送的数据（将作为查询字符串附加到URL上）
    # params = {
    #     "bizCode": "204",
    #     "chapterId": "0",
    #     "classId": "0",
    #     "homeworkId": "0",
    #     "paperId": contentid,
    #     "platform": "1",
    #     "reportId": reportId,
    #     "resourceBizType": "0",
    #     "scheduleId": "0",
    #     "token": token
    # }
    #
    # # 调用函数并获取ID列表
    # st.write("调用get_sorted_question_ids 函数获取ID列表...")
    # id_list = get_sorted_question_ids(url_a, params, cookies)
    #
    # # 初始化结果列表
    # right_answers = []
    # # 对每个ID分别发起POST请求
    # for index, question_id in enumerate(id_list, start=1):
    # # 更新数据中的questionId
    #     data = {
    #     "paperId": contentid,
    #     "reportId": reportId,
    #     "platform": "2",
    #     "questionId": question_id,
    #     "bizCode": "204",
    #     "homeworkId": "0"
    #     }
    #
    #     # 获取rightAnswer的值
    #     right_answer = get_right_answer(url, data, cookies)