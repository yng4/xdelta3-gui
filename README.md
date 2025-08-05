# 使用方法
下载单文件的可以直接双击文件直接运行，由于是单文件和编写语言是python，所以启动会有些慢；下载压缩包的请运行压缩包中的xdelta3-gui.exe，打算直接使用py脚本的话需要自行下载xdelta3，xdelta3.exe可以在原作者提供的二进制文件里找到，[jmacd/xdelta](https://github.com/jmacd/xdelta-gpl)<br>
<img width="518" height="47" alt="Image" src="https://github.com/user-attachments/assets/930e3d0b-8911-4ec9-b07e-51a320df3118" /><br>
**以下是示例，实际使用请按自己的情况结合示例使用。**<br>
先新建两个文本文件，新建文本文档.txt里面写上123，新建文本文档(2).txt里面写上1234。模拟新建文本文档.txt是原先的文件，新建文本文档(2).txt是一段时间后经过了操作的文件。<br>
<img width="1604" height="898" alt="Image" src="https://github.com/user-attachments/assets/3082de08-671d-40d0-8786-6d5746446f4f" /><br>
<img width="1690" height="891" alt="Image" src="https://github.com/user-attachments/assets/3e1e12e3-d67e-4c22-8a93-cb53e98031b4" /><br>
<img width="1687" height="894" alt="Image" src="https://github.com/user-attachments/assets/f0d6c3ab-ce2c-4a84-a832-d043a8544e48" /><br>
点击下拉栏选择生成补丁模式，旧文件选择新建文本文档.txt，新文件选择新建文本文档(2).txt，然后选择补丁保存路径和补丁名称（为了省事这里命名为1），然后点击开始处理并等待处理完成。
<img width="1606" height="906" alt="Image" src="https://github.com/user-attachments/assets/9f80b113-b672-451c-9bbe-8c2a6d50bdfc" /><br>
<img width="1606" height="903" alt="Image" src="https://github.com/user-attachments/assets/b23be7d5-1fb4-4cc1-873d-fd281fe19efd" /><br>
然后是使用补丁<br>
点击下拉栏选择应用补丁模式，旧文件选择新建文本文档.txt，补丁文件选择1.delta，然后选择输出文件的保存路径和名称（这里命名为1.txt）。<br>
<img width="1600" height="912" alt="Image" src="https://github.com/user-attachments/assets/00098e3b-7333-435d-9024-64d7246f38dd" /><br>
打开1.txt，可以发现，内容和新建文本文档(2).txt一样。<br>
<img width="1702" height="902" alt="Image" src="https://github.com/user-attachments/assets/fbdb7b3d-d7b2-4637-a9d1-881bf852c025" />
