# AI辅助编程实录
## 1. 项目任务描述
编写Python脚本 vocab_tool.py，读取生词表CSV文件，实现：读取词汇、按HSK等级筛选词汇、统计不同词性的词汇数量，自动生成词汇造句练习题并输出到txt文本文件。
项目文件全部放在桌面【第三周】文件夹，仅使用Python自带csv标准库，不依赖额外第三方模块。

## 2. 原始初始代码（课程提供的原版代码）
```python
import os
import csv
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import weekpath

DATA = weekpath.data_path("生词表.csv")

def load_words(path=DATA):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))

def filter_by_level(words, level="4"):
    return [w for w in words if str(w["HSK等级"]) == str(level)]

def count_by_pos(words):
    d = {}
    for w in words:
        d[w["词性"]] = d.get(w["词性"], 0) + 1
    return d

def gen_exercises(words, out=None):
    out = out or weekpath.root_path("练习.txt")
    with open(out, "w", encoding="utf-8") as f:
        for w in words:
            f.write("用“%s”造一个句子。（%s）\n" % (w["词汇"], w["词性"]))

if __name__ == "__main__":
    words = load_words()
    lv4 = filter_by_level(words, "4")
    print("总词汇 %d 个，其中 HSK4 词汇 %d 个，词性分布：%s"
          % (len(words), len(lv4), count_by_pos(lv4)))
    out = weekpath.root_path("练习.txt")
    gen_exercises(lv4, out)
    print("已生成：%s" % out)