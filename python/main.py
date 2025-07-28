import pickle
import time

import requests
import streamlit as st

import strtojs as stj
import ewtcmd as ewt
from login import get_token

#session_state:
#   username,password
#   chosen_list,chosen_title_list
#   flag_list:
#       auto_flag,only_choice,auto_submit,method_flag

st.set_page_config(
        # 可恶的Streamlit, 为什么设置页面标题函数的一定要是第一行代码？！
        page_title="EWT360AGAA GUI",  # 标签页标题
        page_icon="💯",  # 标签页图标，可以使用 Unic
        # ode 表情符号或图片路径
        layout="centered"  # 页面布局，可选 "wide" 或 "centered"
    )
try:
    with open('.reportId.data', 'rb') as f:
        tup = pickle.load(f)
        homework_rid = tup[0]
        paper_rid = tup[1]
except OSError as e:
    paper_rid = '0'
    homework_rid = '0'
try:
    with open('.token.data', 'rb') as f:
        tup = pickle.load(f)
        token_timestamp = tup[-1]
        if int(time.time()) - token_timestamp < 3600:
            st.session_state.username = tup[0]
            cookie_area = tup[1]
        else:
            cookie_area = ''
except OSError as e:
    token_timestamp = 0
    cookie_area = ''
try:
    with open('.settings.data', 'rb') as f:
        tup = pickle.load(f)
        st.session_state.settings_list = tup[0]
        settings_timestamp = tup[-1]
except OSError as e:
    settings_timestamp = 0
    st.session_state.settings_list = {}
st.markdown(
    """
    <style>
        /* 调整整个页面的行间距 */
        body {
            line-height: 1; /* 设置行间距为 1 倍 */
        }
    </style>
    """,
    unsafe_allow_html=True
)

@st.dialog('登录E网通')
def login():
    global cookie_area
    st.session_state.username = st.text_input(label='账号')
    st.session_state.password = st.text_input(label='密码', type='password')
    if st.button(label="登录", key="login_button"):
        res, token = get_token(st.session_state.username, st.session_state.password, ewt.url_login)
        if res == 1:
            st.error('请填写正确的账号和密码。')
            st.stop()
        elif res == 2:
            st.error('登录过于频繁，请稍后再试。')
            st.stop()
        elif res == 3:
            st.error('登录密码错误超限，请在E网通网站重新登录并进行安全验证。')
            st.stop()
        elif res == 4:
            st.error('账号和密码不能为空。')
            st.stop()
        elif res == -1:
            st.error(f'发生错误:{token}')
            st.stop()
        cookie_area = 'token=' + token
        with open('.token.data', 'wb') as f:
            pickle.dump((st.session_state.username,cookie_area,int(time.time())), f)
        st.session_state.chosen_list = []
        st.session_state.chosen_title_list = []
        st.rerun()

@st.dialog('选择课程',width='large')
def choose():
    titles = []
    all_homeworks = []
    st.session_state.chosen_list = []
    st.session_state.chosen_title_list = []
    st.write('只能选择未完成的课程')
    col1,col2 = st.columns([0.1,0.9],gap=None,)
    if col1.button(label='刷新'):
        testgood(cookies)
        st.cache_data.clear()
    with st.spinner("正在加载..."):
        for homework in ewt.get_all_homeworks(cookies):
            if homework.get('status') != 3:
                titles.append(homework.get('title'))
                all_homeworks.append(homework)
        for (tab, homework) in zip(st.tabs(titles), all_homeworks):
            days = ewt.get_all_dateStats(homework.get('homeworkId'), cookies)
            for day in days:
                with tab.expander(time.strftime('%Y年%m月%d日', time.localtime(day.get('date')/1000))):
                    for lesson in ewt.get_day_lessons(day.get('dateId'), homework.get('homeworkId'), cookies):
                        if len(lesson.get('contentId')) < 10:
                            finishStatus = ewt.get_practices([lesson.get('contentId')], cookies)[0].get("studyTest").get('finishStatus')
                            disable_flag = (finishStatus==1)
                        else:
                            disable_flag = lesson.get('finished')
                        if st.checkbox('**'+lesson.get('subjectName')+' '+lesson.get('contentTypeName')+'** '+lesson.get('title'),disabled=disable_flag):
                            st.session_state.chosen_list.append(lesson.get('contentId'))
                            st.session_state.chosen_title_list.append('**'+lesson.get('subjectName')+' '+lesson.get('contentTypeName')+'** '+lesson.get('title'))
    if col2.button("确定"):
        st.rerun()

def testgood(cookies):
    #st.write("开始测试...")
    resp = requests.get(ewt.url_baseInfo, headers={'token':cookies.get('token')}, cookies=cookies)
    resp.raise_for_status()
    if not resp.json().get('success'):
        # st.error("测试请求失败，错误信息："+resp.json().get('msg'))
        # st.error("尝试重新登录。")
        # if st.button(label='重新登录', key='relogin_button'):
        #     login()
        # st.stop()
        login()
    #st.write("测试成功")

# st.write("开始转换Cookies....")
cookies = stj.store_data(cookie_area)
# st.write(cookies)
if cookies is None:
    login()
testgood(cookies)

main,settings,answer = st.tabs(['主页','设置','答案'])
with settings:
    if settings_timestamp != 0:
        st.caption(f"上次保存时间:{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(settings_timestamp))}")
    else:
        st.caption(f"上次保存时间:无")
    st.session_state.settings_list['auto_flag'] = st.toggle(label="自动答题", value=st.session_state.settings_list.get('auto_flag'))
    if st.session_state.settings_list['auto_flag']:
        with st.container(border=True):
            st.session_state.settings_list['only_choice'] = st.toggle(label='只答选择题', value=st.session_state.settings_list.get('only_choice'))
            st.session_state.settings_list['auto_submit'] = st.toggle(label='自动提交', value=st.session_state.settings_list.get('auto_submit'), help='与只答选择题同时启用时，只提交只有选择题的习题')
    st.session_state.settings_list['method_flag'] = st.toggle(label="显示解析", value=st.session_state.settings_list.get('method_flag'))
    if st.button(label='保存'):
        with st.spinner('正在保存'):
            with open('.settings.data', 'wb') as f:
                pickle.dump((st.session_state.settings_list,int(time.time())), f)
            st.rerun()
    if 'username' in st.session_state and st.session_state.username != '':
        st.write('---')
        with st.container(border=True):
            st.write(f'E网通账号 {st.session_state.username}')
            if st.button(label='重新登录', key='relogin_button'):
                login()

with main:
    st.title("EWT360AGAA v1.0.3")
    st.write("欢迎使用E网通教辅答案获取工具！")
    st.write("GUI By Streamlit & Code_S96 | Program By Qzgeek | Fork By 皆生函数")
    #url = st.text_area(label="答题链接...")
    if st.button(label='选择课程', key='choose_button'):
        choose()
    if 'chosen_list' in st.session_state and st.session_state.chosen_list:
        with st.expander("已选课程",expanded=True):
            for title in st.session_state.chosen_title_list:
                st.write(title)
    # upfile = st.file_uploader("在这里上传二维码照片...(限大小10M以内)", type=["jpg", "png", "gif"],accept_multiple_files=False)
    st.markdown("---")
    #st.write("以下是程序自动生成日志↓（答案会生成在最底下）")
    # if upfile is not None and url == '':
    #     file_size = upfile.size
    #     max_file_size_bytes = 10 * 1024 * 1024  # 10MB
    #     if file_size > max_file_size_bytes:
    #         st.error("文件大小不能超过10MB!")
    #         st.stop()
    #     #st.write("开始尝试解析二维码图片...")
    #     try:
    #         # 使用Pillow打开图片
    #         img = Image.open(upfile)
    #         # 解码二维码
    #         deobj = decode(img)
    #         if deobj:
    #             # 显示解码结果
    #             #st.write("二维码解析成功！")
    #             for obj in deobj:
    #                 url = unquote(requests.get(deobj[0].data.decode("utf-8"), allow_redirects=True).url)
    #                 st.info(f"✅二维码完整链接: {url}")
    #             # st.write("开始提取ContentID字符串...")
    #             # match = re.search(r'contentid=([^&]+)', url)
    #             # if match:
    #             #     contid = match.group(1)
    #             #     st.write(contid)
    #             #     st.write("ContentID已储存！")
    #             #     st.write(f"ContentID是: {contid}")
    #             # else:
    #             #     st.error("未解析到ContentID，也许你用的不是E网通的链接？AwA")
    #             #     st.stop()
    #         else:
    #             st.error("未检测到二维码，请检查图片是否无遮挡，清晰有效。")
    #             st.stop()
    #     except Exception as e:
    #         st.error(f"解析失败: {e}")
    #         st.stop()
    submit_button = st.button(label="提交并处理信息", key="process_button")
    if submit_button:
        if 'chosen_list' not in st.session_state or st.session_state.chosen_list == []:
            st.error("请选择课程!")
            st.stop()
        #st.write("开始处理信息...")
        #st.write("开始提取paperId,homeworkId,reportId,bizCode...")
        # try:
        #     paperId = re.search(r'paperId=([^&]+)', url).group(1)
        #     bizCode = re.search(r'bizCode=([^&]+)', url).group(1)
        #     homeworkId = "0"
        #     try:
        #         reportId = re.search(r'reportId=([^&]+)', url).group(1)
        #     except AttributeError as e:
        #         reportId = '0'
        #     except Exception as e:
        #         st.error(f"发生错误: {str(e)}")
        #         st.stop()
        # except AttributeError as e:
        #     st.error("请输入完整的链接或使用E网通的二维码!")
        #     st.stop()
        # except Exception as e:
        #     st.error(f"发生错误: {str(e)}")
        #     st.error("请检查各项内容是否正确填写。")
        #     st.stop()
        #st.write("开始获取答案...")
        # ewt.genshin_launch(paperId,homeworkId,bizCode,reportId,paper_rid,homework_rid, cookies,auto_flag,method_flag)
        with st.spinner('请稍等...'):
            bar = st.progress(0)
            for progress,(chosen,title) in enumerate(zip(st.session_state.chosen_list,st.session_state.chosen_title_list),1):
                bar.progress(progress/len(st.session_state.chosen_list), f'正在处理 {progress}/{len(st.session_state.chosen_list)}')
                ewt.genshin_launch(chosen,title,paper_rid, homework_rid, cookies,answer)
            bar.empty()
