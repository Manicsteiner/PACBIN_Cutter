# PACBIN_Cutter
尝试通过暴力查找特定文件头来裁剪一些游戏的PAC.BIN，提取其中资源。  
查看图片请使用[GARbro-Unofficial-Release](https://github.com/Manicsteiner/GARbro/releases/tag/GARbro-Mod-1.0.1.5B1)（该功能暂未合并进入主线）。

适用游戏：
 - Lovedol - Lovely Idol SLPM-65968
 - W Wish SLPM-65671
 - Hokenshitsu e Youkoso SLPM-66439
 - 3LDK SLPM-65607
 - Iinazuke SLPM-66732 （LZS Audio？）

已知问题：
 - 当前方法递归次数过多，最后一个文件可能无法正常输出
 - 第一个文件（m0.pss）可能包含多个pss文件