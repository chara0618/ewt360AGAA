import streamlit as st
import re
import strtojs as stj
import ewtcmd as ewt

st.set_page_config(
    # 可恶的Streamlit, 为什么设置页面标题函数的一定要是第一行代码？！
    page_title="EWTcrackerGUI",  # 标签页标题
    page_icon="💯",  # 标签页图标，可以使用 Unicode 表情符号或图片路径
    layout="centered"  # 页面布局，可选 "wide" 或 "centered"
)

# def extract_cookies(json_text):
#     # 将JSON字符串解析为Python字典
#     data = json.loads(json_text)
#     # 提取"请求 Cookie"下的内容（如果键不存在则返回空字典）
#     cookies_dict = data.get("请求 Cookie", {})
#     return cookies_dict

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
st.caption("EWT360AGAA 1.0.0")
st.title("EWT360AGAA")
st.write("欢迎使用一网通教辅答案获取工具！")
st.write("GUI By Streamlit & Code_S96 | Program By Qzgeek | Fork By falseblocks")
cookie_area = st.text_area(label="在这里输入Cookies...")
# upfile = st.file_uploader("在这里上传二维码照片...(限大小10M以内)", type=["jpg", "png", "gif"])
paper_rid = st.text_area(label="已完成试卷的reportId...")
homework_rid = st.text_area(label="已完成课后习题的reportId...")
url = st.text_area(label="答题链接...")
auto_flag = st.checkbox(label="自动答题",value=True)
method_flag = st.checkbox(label="显示解析",value=False)
submit_button = st.button(label="提交并处理信息", key="process_button")
st.markdown("---")
#st.write("以下是程序自动生成日志↓（答案会生成在最底下）")

# if upfile is not None:
#     file_size = upfile.size
#     max_file_size_bytes = 10 * 1024 * 1024  # 10MB
#     if file_size > max_file_size_bytes:
#         st.error("文件大小不能超过10MB!")
#         st.stop()
#     st.write("开始尝试解析二维码图片...")
#     try:
#         # 使用Pillow打开图片
#         img = Image.open(upfile)
#         # 解码二维码
#         deobj = decode(img)
#         if deobj:
#             # 显示解码结果
#             st.write("二维码解析成功！")
#             for obj in deobj:
#                 furl = requests.get(deobj[0].data.decode("utf-8"), allow_redirects=True).url
#                 st.write(f"完整链接: {furl}")
#             st.write("开始提取ContentID字符串...")
#             match = re.search(r'contentid=([^&]+)', furl)
#             if match:
#                 contid = match.group(1)
#                 st.write(contid)
#                 st.write("ContentID已储存！")
#                 st.write(f"ContentID是: {contid}")
#             else:
#                 st.error("未解析到ContentID，也许你用的不是E网通的链接？AwA")
#         else:
#             st.error("未检测到二维码，请检查图片是否无遮挡，清晰有效。")
#     except Exception as e:
#         st.error(f"解析失败: {e}")
if submit_button:
    if (paper_rid == "") or (homework_rid == ""):
        st.error("请输入reportId!")
        st.stop()
    elif url == "":
        st.error("请输入答题链接!")
        st.stop()
    #st.write("开始处理信息...")
    #st.write("开始转换Cookies....")
    cookies = stj.store_data(cookie_area)
    if cookies is None:
        st.error("Cookies转换失败！请检查输入是否正确。")
        st.stop()
    #st.write("开始提取paperId,homeworkId,reportId,bizCode...")
    try:
        paperId = re.search(r'paperId=([^&]+)', url).group(1)
        bizCode = re.search(r'bizCode=([^&]+)', url).group(1)
        homeworkId = "0"
        reportId = re.search(r'reportId=([^&]+)', url).group(1)
    except Exception as e:
        st.error("请输入完整的链接!")
        st.stop()
    #st.write("开始获取答案...")
    ewt.genshin_launch(paperId,homeworkId,bizCode,reportId,paper_rid,homework_rid, cookies,auto_flag,method_flag)