# -*- coding: utf-8 -*-
"""
week5_local_fallback.py
=======================
W5 本地部署备选方案: 当 Ollama / LM Studio / llama-cpp-server 都用不了时，
直接用 transformers + Qwen2.5-0.5B-Instruct 跑本地推理。

和 W4 的 week4_api_bot.py 接口完全一样: 仅暴露一个 ask(q, sys=None) 函数。
替换方式: 把 week4_api_bot.py 里的 `from openai import OpenAI` + `client = OpenAI(...)` + `resp = client.chat.completions.create(...)`
    from week5_local_fallback import ask
    print(ask("你好，介绍下你自己"))

依赖:
    pip install transformers torch --index-url https://download.pytorch.org/whl/cpu
(CPU 即可，不需要 GPU；首次运行自动从 Hugging Face 下载 Qwen2.5-0.5B-Instruct，约 1GB)

镜像 (连不上 huggingface.co 时把下面这一行取消注释):
    os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
"""
import os

# 中国大陆机房常连不上 huggingface.co; 如需镜像，把下行注释去掉
# os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

MODEL_NAME = os.environ.get("LOCAL_MODEL", "Qwen/Qwen2.5-0.5B-Instruct")
_pipe = None  # 全局单例，避免重复加载

def _load():
    """懒加载: 第一次调用时加载模型（约 1-3 GB 内存，CPU 推理）"""
    global _pipe
    if _pipe is not None:
        return _pipe
    from transformers import AutoTokenizer, AutoModelForCausalLM
    import torch
    print(f"[week5-fallback] 首次运行，加载 {MODEL_NAME} ...(CPU, 首次需 30-90 秒)")
    tok = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
    mdl = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.float32,      # CPU 推理用 fp32 最稳
        device_map="cpu",
        trust_remote_code=True,
    )
    mdl.eval()

    def _gen(messages, max_new_tokens=256, temperature=0.7):
        prompt = tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = tok(prompt, return_tensors="pt").to(mdl.device)
        with torch.no_grad():
            out = mdl.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=temperature > 0,
                temperature=temperature,
                top_p=0.9,
                pad_token_id=tok.eos_token_id,
            )
        text = tok.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)
        return text.strip()

    _pipe = _gen
    print("[week5-fallback] 模型就绪，可以开始问答。")
    return _pipe


def ask(q: str, sys: str | None = None, max_tokens: int = 256) -> str:
    """
    与 week4_api_bot.py 兼容的 ask(q) 接口。
    q: 用户问题
    sys: 可选系统提示词
    max_tokens: 最大生成长度（默认 256）
    """
    messages = []
    if sys:
        messages.append({"role": "system", "content": sys})
    messages.append({"role": "user", "content": q})
    return _load()(messages, max_new_tokens=max_tokens)


# ----- 极简自测 -----
if __name__ == "__main__":
    print(ask("用一句话介绍你自己。", sys="你是一个中文教学助手。"))
