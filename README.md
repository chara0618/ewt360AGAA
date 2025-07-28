# EWT360 Answer Getting & Automatic Answering

[下载](https://github.com/chara0618/ewt360AGAA/releases)

## 项目简介
`ewt360AGAA` 是[qzgeek/ewt360](https://github.com/qzgeek/ewt360)的一个分支，整合部分[GetEWTAnswers](https://github.com/zhicheng233/GetEWTAnswers)的功能，旨在提升原项目的使用体验。

## 功能特点
- **获取答案**：提供选择题与主观题的答案及解析。
- **自动回答**：工具能够自动完成题目，其中**选择题**提交正确答案，**主观题**提交[图片](http://file.ewt360.com/file/1918218053226168959)。

## 使用说明
1. **启动工具**：运行`run.exe` ，等待片刻后浏览器应自动弹出WEBUI，此时**不要关闭原来的黑窗**，继续进行下面的操作。初次运行可能要求输入email，直接回车即可。
2. **填写账密**：填写账号与密码，点击`登录`。
4. **选择课程**：点击`选择课程` ，选择需要获取答案的课程。
5. **调整设置**：点击`设置` ，按提示调整设置，然后点击`保存`。
7. **运行工具**：回到`主页`，点击`提交并处理信息` 。
8. **获取答案**：等待处理完毕，点击`答案`。

## 注意事项
1. 请仔细阅读所有说明和指南。 
2. 此程序仅用于给觉得E网通确实对自己无用的同学节约时间，不得滥用此程序，一切由滥用造成的后果由使用者自负。

## 疑难杂症
#### 什么是教辅？
- 详见[原项目](https://github.com/qzgeek/ewt360/tree/main#%E7%96%91%E9%9A%BE%E6%9D%82%E7%97%87)。
#### 在工具中填写账密后原来的E网通自动退出登录
- 工具会获取新的token,使得原token失效，导致E网通自动退出登录。
#### 未检测到已完成的试卷&未检测到已完成的课后习题
- 确保自己的账号有**已经完成的**试卷及课后习题，然后重新操作。

## 鸣谢
- [qzgeek/ewt360](https://github.com/qzgeek/ewt360)：大部分代码及WEBUI。
- [GetEWTAnswers](https://github.com/zhicheng233/GetEWTAnswers)：答案获取的相关API。
- [landuoguo/ewt360](https://github.com/landuoguo/ewt360)：关于E网通密码加密的研究。
- [DeepSeek](https://www.deepseek.com/)：部分代码生成。
