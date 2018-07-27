# 基于Tornado的一个带有登陆和注册功能的HTML页面
&nbsp;&nbsp;&nbsp;&nbsp;目前新版的Tornado（V5.1）函数有了较大的更新，为了在更新最新版的翻译文档时</br>
顺便加深一下印象和理解，由此产生该`project`。
</br>
## 功能描述
1.已经注册的用户可以直接登陆，登陆成功后来到`welcome`页面。该页面放置一首古筝曲：`《平湖秋月》`，希望大家喜欢 :-)</br>
2.新的用户，可以在登陆页面找到`注册`按钮，进行手动注册，成功后跳转到`welcome`页面。注意：会检查新的注册用户名是否存在</br>
## 启动命令
在该`project`目录下运行：</br>
`for Windows:`</br>
CMD ->>: python server.py</br>
将会打印该server监听的端口号，访问入口：`localhost:10000`，然后被重定向到登陆页面，然后自己玩耍去吧！
</br>
</br>
# 开发环境
Python version: CPython 3.6.5</br>
Tornado version: 5.1</br>
MySQL Server version：8.0.11</br>
# TODOS
把该应用打包到`ubuntu`镜像，从容器中运行。</br>
容器联网还有点问题</br>

# License
GPL V2.0</br>