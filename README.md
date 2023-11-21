![SpringBoot-Scan](https://socialify.git.ci/AabyssZG/SpringBoot-Scan/image?description=1&descriptionEditable=Open%20source%20penetration%20framework%20for%20SpringBoot%20and%20high-risk%20vulnerability%20exploitation%20tools%20related%20to%20Spring&font=Rokkitt&forks=1&issues=1&language=1&logo=https%3A%2F%2Favatars.githubusercontent.com%2Fu%2F54609266%3Fv%3D4&name=1&owner=1&pattern=Circuit%20Board&stargazers=1&theme=Dark)

# ✈️ 一、工具概述
日常渗透过程中，经常会碰到Spring Boot搭建的微服务，于是就想做一个针对Spring Boot的开源渗透框架，主要用作扫描Spring Boot的敏感信息泄露端点，并可以直接测试Spring的相关高危漏洞。

于是，就写了这么一个工具：SpringBoot-Scan  【简称：“SB-Scan”（错乱】

**后期将加入更多漏洞利用内置模块（各位师傅能不能赏个Star嘛~码代码挺辛苦的哈哈）**

**我还整理了一篇SpringBoot的相关渗透姿势在我的个人博客，欢迎各位师傅前来交流哈哈：[https://blog.zgsec.cn/archives/129.html](https://blog.zgsec.cn/archives/129.html)**

# 📝 二、TODO

* [x] 添加支持2023 JeeSpringCloud 任意文件上传漏洞
* [x] 添加支持2021 SnakeYAML_RCE 漏洞
* [x] 添加支持2020 Jolokia配置不当导致RCE漏洞
* [x] 添加支持CVE-2021-21234 (任意文件读取漏洞)
* [x] 支持自动对Spring进行指纹识别
* [x] 在漏洞利用模块，对错误进行输出为 `error.log`
* [x] 支持使用带认证的HTTP代理节点，自动检测节点状态
* [x] 由 `13exp` 师傅友情制作GUI图形化版本
* [x] 添加支持CVE-2022-22947 (Spring Cloud Gateway SpELRCE漏洞)
* [x] 添加支持CVE-2022-22963 (Spring Cloud Function SpEL RCE漏洞)
* [x] 添加支持CVE-2022-22965 (Spring Core RCE漏洞)
* [x] 命令执行漏洞式支持交互式执行命令
* [x] 验证代理是否存活，并可以使用HTTP认证
* [x] 支持使用HTTP/HTTPS代理所有流量
* [x] 随机User-Agent请求头
* [x] 解决SSL证书问题 (自签名证书请改成 `http://` 即可)
* [x] 智能识别目标地址 (`example.com` 和`http://example.com/` 以及`http://example.com` 都不会报错)

**GUI图形化版本，由 [13exp](https://github.com/13exp/) 师傅友情制作，GUI地址：[https://github.com/13exp/SpringBoot-Scan-GUI](https://github.com/13exp/SpringBoot-Scan-GUI)**

**感觉好用，师傅们可以点个Star哈哈~**
![GUI](./pic/GUI.png)

# 🚨 三、安装Python依赖库
```
pip3 install -r requirements.txt
```

# 🐉 四、工具使用
```
# python3 SpringBoot-Scan.py
  ______                       __                      _______                        __
 /      \                     |  \                    |       \                      |  \
|  $$$$$$\  ______    ______   \$$ _______    ______  | $$$$$$$\  ______    ______  _| $$_
| $$___\$$ /      \  /      \ |  \|       \  /      \ | $$__/ $$ /      \  /      \|   $$ \
 \$$    \ |  $$$$$$\|  $$$$$$\| $$| $$$$$$$\|  $$$$$$\| $$    $$|  $$$$$$\|  $$$$$$\\$$$$$$
 _\$$$$$$\| $$  | $$| $$   \$$| $$| $$  | $$| $$  | $$| $$$$$$$\| $$  | $$| $$  | $$ | $$ __
|  \__| $$| $$__/ $$| $$      | $$| $$  | $$| $$__| $$| $$__/ $$| $$__/ $$| $$__/ $$ | $$|  \
 \$$    $$| $$    $$| $$      | $$| $$  | $$ \$$    $$| $$    $$ \$$    $$ \$$    $$  \$$  $$
  \$$$$$$ | $$$$$$$  \$$       \$$ \$$   \$$ _\$$$$$$$ \$$$$$$$   \$$$$$$   \$$$$$$    \$$$$
          | $$                              |  \__| $$
          | $$                               \$$    $$
           \$$                                \$$$$$$
            ______
           /      \
          |  $$$$$$\  _______  ______   _______      +-------------------------------------+
          | $$___\$$ /       \|      \ |       \     +                                     +
           \$$    \ |  $$$$$$$ \$$$$$$\| $$$$$$$\    + Version: 2.12                       +
           _\$$$$$$\| $$      /      $$| $$  | $$    + Author: 曾哥(@AabyssZG)             +
          |  \__| $$| $$_____|  $$$$$$$| $$  | $$    + Whoami: https://github.com/AabyssZG +
           \$$    $$ \$$     \\$$    $$| $$  | $$    +                                     +
            \$$$$$$   \$$$$$$$ \$$$$$$$ \$$   \$$    +-------------------------------------+


用法:
        对单一URL进行信息泄露扫描:         python3 SpringBoot-Scan.py -u example.com
        读取目标TXT进行批量信息泄露扫描:    python3 SpringBoot-Scan.py -f url.txt
        对单一URL进行漏洞利用:             python3 SpringBoot-Scan.py -v example.com
        扫描并下载SpringBoot敏感文件:      python3 SpringBoot-Scan.py -d example.com
        使用HTTP代理并自动进行连通性测试:    python3 SpringBoot-Scan.py -p <代理IP:端口>

参数:
        -u  --url       对单一URL进行信息泄露扫描
        -f  --file      读取目标TXT进行批量信息泄露扫描
        -v  --vul       对单一URL进行漏洞利用
        -d  --dump      扫描并下载SpringBoot敏感文件（可提取敏感信息）
        -p  --proxy     使用HTTP进行代理（默认连通性测试www.baidu.com）
```

**注意，本工具优化了使用者体验，不管是对单一URL扫描还是读取TXT进行批量扫描，`example.com` 和`http://example.com/` 以及`http://example.com` 都不会报错，程序会自行判断并识别**

**同时，解决了SSL证书问题，可以对采用SSL证书的Spring Boot框架进行扫描（自签名证书请改成 `http://` 即可）**

# 🛸 五、工具演示

### 0# 信息泄露字典

Dir.txt为内置的信息泄露端点字典，我基本收集齐了Spring Boot的相关敏感信息泄露端点

如果有遗漏，欢迎各位师傅跟我联系哈哈

### 1# 测试并使用代理

```
python3 SpringBoot-Scan.py -p <代理IP:端口>
python3 SpringBoot-Scan.py -p <HTTP认证账号:HTTP认证密码@代理IP:端口>
```

![测试代理](./pic/测试代理.png)

比如我想对单一URL进行信息泄露扫描并使用代理
```
python3 SpringBoot-Scan.py -u example.com -p <代理IP:端口>
python3 SpringBoot-Scan.py -p <HTTP认证账号:HTTP认证密码@代理IP:端口>
```
同样，其他参数（`-u` / `-f` / `-u` / `-d`）均可以配合代理使用

### 2# 对单一URL进行信息泄露扫描

```
python3 SpringBoot-Scan.py -u example.com
```

![扫描单一URL](./pic/扫描单一URL.png)

**注：扫描结束后，会把成功的结果导出为同目录下的urlout.txt**

### 3# 读取目标TXT进行批量信息泄露扫描

```
python3 SpringBoot-Scan.py -f url.txt
```

![读取TXT并批量扫描](./pic/读取TXT并批量扫描.png)

**注：扫描结束后，会把成功的结果导出为同目录下的output.txt**

### 4# 对单一URL进行漏洞利用

```
python3 SpringBoot-Scan.py -v example.com
```

![对单一URL进行漏洞利用](./pic/对单一URL进行漏洞利用.png)

默认执行 `id` Payload，只是证明漏洞存在即可，有需要可以提issue来添加一个命令自定义功能

**同时，后期将加入更多漏洞利用内置模块，请师傅们敬请期待~**

### 5# 扫描并下载SpringBoot敏感文件

```
python3 SpringBoot-Scan.py -d example.com
```

![扫描并下载SpringBoot敏感文件](./pic/扫描并下载SpringBoot敏感文件.png)

**注：扫描到的敏感文件，会自动下载到脚本的运行目录，有进度条可以看到实时下载进度**

目前敏感文件目录内置了5个，如下：

```
actuator/heapdump
gateway/actuator/heapdump
heapdump
heapdump.json
hystrix.stream
```

如果有师傅有其他敏感文件的目录，可以提交issues，谢谢！！！

# 🙏 六、感谢各位师傅

## Stargazers

[![Stargazers repo roster for @AabyssZG/SpringBoot-Scan](http://reporoster.com/stars/AabyssZG/SpringBoot-Scan)](https://github.com/AabyssZG/SpringBoot-Scan/stargazers)


## Forkers

[![Forkers repo roster for @AabyssZG/SpringBoot-Scan](http://reporoster.com/forks/AabyssZG/SpringBoot-Scan)](https://github.com/AabyssZG/SpringBoot-Scan/network/members)


## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=AabyssZG/SpringBoot-Scan&type=Date)](https://star-history.com/#AabyssZG/SpringBoot-Scan&Date)
