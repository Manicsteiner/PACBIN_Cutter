# PACBIN_Cutter
尝试通过暴力查找特定文件头来裁剪一些游戏的PAC.BIN，提取其中资源。
适用游戏：
 - Lovedol - Lovely Idol SLPM-65968
 - W Wish SLPM-65671

已知问题：
 - 当前方法递归次数过多，最后一个文件无法正常输出
 - 第一个文件（m0.pss）可能包含多个pss文件