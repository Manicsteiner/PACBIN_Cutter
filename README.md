# PACBIN_Cutter
尝试通过暴力查找特定文件头来裁剪一些游戏的PAC.BIN，提取其中资源。  
查看图片请使用[GARbro-Unofficial-Release](https://github.com/Manicsteiner/GARbro/releases/tag/GARbro-Mod-1.0.1.5B1)（该功能暂未合并进入主线）。

适用游戏：
 - Lovedol - Lovely Idol SLPM-65968
 - W Wish SLPM-65671
 - Hokenshitsu e Youkoso SLPM-66439
 - 3LDK SLPM-65607
 - Iinazuke SLPM-66732 （LZS Audio？）
 - Final Approach 2 SLPM-66942
 - Nettai Teikiatsu Shoujo SLPM-66860
 - Magical Tale SLPM-65965
 - Yumemishi SLPM-66618
 - Yumemi Hakusho SLPM-55070

文件格式信息：
 - TM2
   vis*.tm2，“TIM2”Header，TIM2图片格式
 - LZS-TIM2
   il*.tm2，“LZS______TIM2”Header，使用LZSS Stream压缩的TIM2图片格式
 - PSS
   *.pss，没有明显的文件头，在0xB3附近会出现“TMPGEncode”字样，PSS视频文件
 - VGS
   *.vgs，“VGS”Header，VGS（Princess Soft VGS Header）音频文件，可能有额外压缩或加密，未输出
 - HBD
   *.HBD，“IECSsreV”Header，可能是音频文件，未输出

已知问题：
 - 当前方法递归次数过多，最后一个文件可能无法正常输出
 - 第一个文件（m0.pss）可能包含多个pss文件，请自行切分