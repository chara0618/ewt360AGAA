import pickle
import time

import requests
import streamlit as st
import re

from PIL import Image
from pyzbar.pyzbar import decode
from urllib.parse import unquote

import strtojs as stj
import ewtcmd as ewt
from login import get_token
from ewtcmd import url_login

st.set_page_config(
    # 可恶的Streamlit, 为什么设置页面标题函数的一定要是第一行代码？！
    page_title="EWT360AGAA GUI",  # 标签页标题
    page_icon="💯",  # 标签页图标，可以使用 Unic
    # ode 表情符号或图片路径
    layout="centered"  # 页面布局，可选 "wide" 或 "centered"
)
try:
    with open('reportId.data', 'rb') as f:
        tup = pickle.load(f)
        homework_rid = tup[0]
        paper_rid = tup[1]
except OSError as e:
    paper_rid = '0'
    homework_rid = '0'
try:
    with open('token.data', 'rb') as f:
        tup = pickle.load(f)
        token_timestamp = tup[1]
        if int(time.time()) - token_timestamp < 600:
            cookie_area = tup[0]
        else:
            cookie_area = ''
except OSError as e:
    token_timestamp = 0
    cookie_area = ''
contid = None
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
    username = st.text_input(label='账号')
    password = st.text_input(label='密码', type='password')
    if st.button(label="登录", key="login_button"):
        res, token = get_token(username, password, url_login)
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
        with open('token.data', 'wb') as f:
            pickle.dump((cookie_area,int(time.time())), f)
        st.rerun()
    st.stop()



if int(time.time()) - token_timestamp > 600:
    login()
st.caption("EWT360AGAA 1.0.2")
st.title("EWT360AGAA")
st.write("欢迎使用E网通教辅答案获取工具！")
st.write("GUI By Streamlit & Code_S96 | Program By Qzgeek | Fork By 皆生函数")
url = st.text_area(label="答题链接...")
upfile = st.file_uploader("在这里上传二维码照片...(限大小10M以内)", type=["jpg", "png", "gif"],accept_multiple_files=False)
auto_flag = st.checkbox(label="自动答题",value=False)
method_flag = st.checkbox(label="显示解析",value=False)
submit_button = st.button(label="提交并处理信息", key="process_button")
if st.button(label='重新登录', key='relogin_button'):
    login()
st.markdown("---")
#st.write("以下是程序自动生成日志↓（答案会生成在最底下）")
if upfile is not None and url == '':
    file_size = upfile.size
    max_file_size_bytes = 10 * 1024 * 1024  # 10MB
    if file_size > max_file_size_bytes:
        st.error("文件大小不能超过10MB!")
        st.stop()
    #st.write("开始尝试解析二维码图片...")
    try:
        # 使用Pillow打开图片
        img = Image.open(upfile)
        # 解码二维码
        deobj = decode(img)
        if deobj:
            # 显示解码结果
            #st.write("二维码解析成功！")
            for obj in deobj:
                url = unquote(requests.get(deobj[0].data.decode("utf-8"), allow_redirects=True).url)
                st.info(f"✅二维码完整链接: {url}")
            # st.write("开始提取ContentID字符串...")
            # match = re.search(r'contentid=([^&]+)', url)
            # if match:
            #     contid = match.group(1)
            #     st.write(contid)
            #     st.write("ContentID已储存！")
            #     st.write(f"ContentID是: {contid}")
            # else:
            #     st.error("未解析到ContentID，也许你用的不是E网通的链接？AwA")
            #     st.stop()
        else:
            st.error("未检测到二维码，请检查图片是否无遮挡，清晰有效。")
            st.stop()
    except Exception as e:
        st.error(f"解析失败: {e}")
        st.stop()
if submit_button:
    if url == '':
        st.error("请输入答题链接!")
        st.stop()
    #st.write("开始处理信息...")
    #st.write("开始转换Cookies....")
    cookies = stj.store_data(cookie_area)
    #st.write(cookies)
    if cookies is None:
        st.error("Cookies转换失败！请检查输入是否正确。")
        st.stop()
    #st.write("开始提取paperId,homeworkId,reportId,bizCode...")
    try:
        paperId = re.search(r'paperId=([^&]+)', url).group(1)
        bizCode = re.search(r'bizCode=([^&]+)', url).group(1)
        homeworkId = "0"
        try:
            reportId = re.search(r'reportId=([^&]+)', url).group(1)
        except AttributeError as e:
            reportId = '0'
        except Exception as e:
            st.error(f"发生错误: {str(e)}")
            st.stop()
    except AttributeError as e:
        st.error("请输入完整的链接或使用E网通的二维码!")
        st.stop()
    except Exception as e:
        st.error(f"发生错误: {str(e)}")
        st.error("请检查各项内容是否正确填写。")
        st.stop()
    #st.write("开始获取答案...")
    ewt.genshin_launch(paperId,homeworkId,bizCode,reportId,paper_rid,homework_rid, cookies,auto_flag,method_flag)