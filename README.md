# 基于Tornado的一个带有登陆和注册功能的HTML页面
&nbsp;&nbsp;&nbsp;&nbsp;详细信息参见[这个链接](https://github.com/Iflier/TornadoLoginPage)。该`project`是由它衍生过来的，</br>
不同点在于保存用户登录的信息保存到`Sqlite3`。本想在Ubuntu容器内安装好MySQL数据库后，再打包成镜像上传出来的，</br>
然而实际操作时发现在ubuntu容器内安装MySQL着实有点耗费时间（实际上是懒吧 :-)）。分别启动两个容器，</br>
一个用来跑Ubuntu镜像，一个用来跑MySQL镜像，也想过。但是，这个不够`Python`化，不够 **简单、优雅和明确** （这个借口貌似很有道理的样子:-)）。</br>
</br>
</br>
# 开发环境
Python version: CPython 3.6.5</br>
Tornado version: 5.1</br>
Sqlite3</br>
# TODOS
把该应用打包到`ubuntu`镜像，从容器中运行。</br>
## UPDATE
**2017.07.27**</br>
</br>
历经多个业余时间，终于把一个完整的应用打包成一个镜像了 :-)</br>
镜像内`Tornado WEB Server`默认监听端口为`10000`，启动容器时，可以在外部`host`选择其他端口进行映射</br>
镜像内安装的Python3版本为 **Python 3.7**，`pip`包管理器为Version 18.0。</br>
在容器内的`/home/hap`目录下启动`server.py`脚本时，</br>
使用的启动命令为 **python3.7 server.py**</br>

# License
GPL V2.0</br>