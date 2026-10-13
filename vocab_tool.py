import csv

# =========配置区，改这里就可以=========
target_level = "4"          # 想要筛选的HSK等级，改成3就是HSK3
csv_file_path = "新建文本文档 (2).csv"   # 读取的生词表
output_file_path = "练习.txt"       # 输出练习题，生成在第三周文件夹
# ====================================

# 读取生词表
def load_words(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))

# 根据HSK等级筛选词汇（基础for循环，没有高级推导式）
def filter_by_level(words, level):
    result_list = []
    for w in words:
        if str(w["HSK等级"]) == str(level):
            result_list.append(w)
    return result_list

# 统计各个词性的数量
def count_by_pos(words):
    pos_dict = {}
    for w in words:
        pos = w["词性"]
        if pos in pos_dict:
            pos_dict[pos] = pos_dict[pos] + 1
        else:
            pos_dict[pos] = 1
    return pos_dict

# 生成练习题写入txt
def gen_exercises(words, out):
    with open(out, "w", encoding="utf-8") as f:
        pos_result = count_by_pos(words)
        f.write("==== HSK词汇练习题 ====\n")
        f.write(f"词性统计结果：{pos_result}\n\n")
        for w in words:
            f.write("用“%s”造一个句子。（%s）\n" % (w["词汇"], w["词性"]))


if __name__ == "__main__":
    words = load_words(csv_file_path)
    target_words = filter_by_level(words, target_level)
    pos_info = count_by_pos(target_words)

    print(f"全部生词一共 {len(words)} 个")
    print(f"筛选出HSK{target_level}词汇，一共有 {len(target_words)} 个")
    print(f"HSK{target_level}词汇词性统计：{pos_info}")

    gen_exercises(target_words, output_file_path)
    print(f"\n✅ 练习题已经生成：{output_file_path}")