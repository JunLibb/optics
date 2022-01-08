
## 首先拉取远程仓库的文件，和本地同步一下
git pull origin main
## 然后本地改动
## 上传指定文件xx.py
git add xx.py
## 上传整个文件夹
git add .
## 删除文件xx.py
git rm -r --cached xx.py
## 备注本次改动
git commit -m 'test'
## 上传本次改动
git push -u origin main