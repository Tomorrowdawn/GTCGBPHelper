# GTCGBPHelper
a helper for ban-pick in GeniusInvokation TCG tournaments

仅适用于**征服赛制**

## 使用

在`FastRollout/helper.ipy`中已经有一个示例. 简单来说, 只需要提供一个对战胜率表($N\times N$), 输入给picker或者banner, 随后调用`picker.pick()`或者`banner.predict()`即可输出一个概率向量,表明pick或者ban该卡组的概率.

对战胜率表中,$t_{i,j}$表示$i$对阵$j$的胜率, 需要强调的是这通常不是一个对称矩阵. 

## 未来

可能考虑引入RL算法. 本项目有一个RM实现, 由于征服赛制的博弈树过于庞大, 运行时间缓慢而未披露. 目前仅提供基于纯rollout的实现.