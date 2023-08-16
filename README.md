# The Web Armory | Web武器库

欢迎使用Web武器库，本知识库内容非原创，为方便搭建搜索，特意收集能找到的知识库并统一生成至一个gitbook中，如有侵权请联系删除。

## 使用方法

### Docker(推荐)

```bash
docker pull timlzh/webarmory:latest
docker run -it -dp 8000:80 timlzh/webarmory:latest
```

打开浏览器访问`http://127.0.0.1:8000`即可。

### Mkdocs-Material Docker镜像编译运行

```bash
docker pull squidfunk/mkdocs-material
docker run -t -v ${PWD}:/docs squidfunk/mkdocs-material serve
```

打开浏览器访问`http://127.0.0.1:8000`即可。

### 本地编译运行

运行环境：Python3

```bash
pip install mkdocs mkdocs-material
mkdocs serve
```

打开浏览器访问`http://127.0.0.1:8000`即可。

## Organized by

- @[Timlzh](https://github.com/timlzh)

## Contents Origins

- [BaizeSec/bylibrary](https://github.com/BaizeSec/bylibrary/)
- [PeiQi0/Peiqi-WIKI-Book](https://github.com/PeiQi0/PeiQi-WIKI-Book/)
- [xiaoy-sec/Pentest_Note](https://github.com/xiaoy-sec/Pentest_Note/)
- [DawnFlame/POChouse](https://github.com/DawnFlame/POChouse)
- [wgpsec/wiki](https://github.com/wgpsec/wiki)
- [cckuailong/vulbase](https://github.com/cckuailong/vulbase)
- Qingy
- Edge-Security-Team
