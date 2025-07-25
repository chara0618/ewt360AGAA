# EWT360 Answer Getting & Automatic Answering

[下载](https://github.com/chara0618/ewt360AGAA/releases)

## 项目简介
`ewt360AGAA` 是[ewt360](https://github.com/qzgeek/ewt360)的一个分支，整合部分[GetEWTAnswers](https://github.com/zhicheng233/GetEWTAnswers)的功能，旨在提升原项目的使用体验。

## 功能特点
- **获取答案**：提供选择题与主观题的答案及解析。
- **自动回答**：工具能够自动完成题目，其中**选择题**提交正确答案，**主观题**提交[图片](http://file.ewt360.com/file/1918218053226168959)。

## 使用说明
1. **启动工具**：运行`run.bat`(Windows)或`run.sh`(Linux)，等待片刻后浏览器应自动弹出WEBUI，此时**不要关闭原来的黑窗**，继续进行下面的操作。
1. **获取Cookie**：手动抓包并根据指示填写`cookie`，所抓包请求URL中的域名应为web.ewt360.com，格式应保持HTTP请求头中`Cookies:`后的默认格式。
2. **获取ReportId**：分别选择**已经完成的**试卷及课后习题,复制并填写网址上reportId的值（详见[如何获得](https://github.com/zhicheng233/GetEWTAnswers?tab=readme-ov-file#%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8)）。
3. **获取答题链接**：打开需要获取答案的试卷或课后习题，复制并填写整个网址。
5. **运行工具**：按照工具的提示进行操作。

## 注意事项
1. 请仔细阅读所有说明和指南。 
2. 此程序仅用于给觉得E网通确实对自己无用的同学节约时间，不得滥用此程序，一切由滥用造成的后果由使用者自负。

## 疑难杂症
#### 什么是教辅？&如何获取cookie？
- 详见[原项目](https://github.com/chara0618/ewt360AGAA?tab=readme-ov-file#%E7%96%91%E9%9A%BE%E6%9D%82%E7%97%87)。

## 鸣谢
- [ewt360](https://github.com/qzgeek/ewt360)：大部分代码及WEBUI。
- [GetEWTAnswers](https://github.com/zhicheng233/GetEWTAnswers)：答案获取的相关API。
