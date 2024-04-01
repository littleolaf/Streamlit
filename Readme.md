# Git学习记录
虽然这是我的某个项目的前端页面，但主要是被我用来学习git和github使用，以下是学习记录

**分支：**  
&emsp;&emsp;创建：```git checkout -b BranchName```  
&emsp;&emsp;&emsp;`git branch [NewName]`  
&emsp;&emsp;&emsp;`git checkout [branchName]`   
&emsp;&emsp;重命名：`git branch -m [OldName] [NewName]`  
&emsp;&emsp;删除本地分支：`git branch -d [branchname]`  
&emsp;&emsp;删除远程分支：`git push origin --delete [branchname]`  
&emsp;&emsp;合并：`git merge [branch][branch]`  
&emsp;&emsp;&emsp;执行合并命令会将指定分支合并到当前工作分支上  
&emsp;&emsp;解决冲突：vs code自带冲突解决  

**版本控制与回退：**`git reset --hard "CommitId"`  
**查看记录/状态：**`git log/status`  

**GitHub下载与上传：**`git push [remote] [branch]`


**gitignore使用：**
https://blog.csdn.net/qq_38259968/article/details/103711998