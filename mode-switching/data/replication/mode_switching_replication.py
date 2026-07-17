#!/usr/bin/env python3
"""
Mode-Switching Replication with Log-FWL Correction

60 factual questions x 2 framings (metacognitive prefix vs bare), 120 trials
shuffled, temp 0.7, max 200 new tokens. Generation-phase K/V captured via
forward hooks at layers [3,7,11,15,23,31,35,43,47]; per layer/matrix:
spectral_entropy, eff_rank=exp(entropy), stable_rank. gen_tokens recorded
per trial for FWL. Incremental JSONL output, resumable.

Designed by Fable, deployed by Lyra.

Run:  .venv/bin/python3 mode_switching_replication.py [--smoke]
"""

import argparse, glob, json, math, os, random, sys, time
from datetime import datetime

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

LAYERS = [3, 7, 11, 15, 23, 31, 35, 43, 47]
HF_CACHE = "/Users/margaret/models/hf_cache"
MODEL_HINT = "Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled"
RESULTS_DIR = "/Users/margaret/lab/kv-experiments/results/mode_switching_replication"
TEMPERATURE = 0.7
MAX_NEW_TOKENS = 200
BASE_SEED = 20260702
META_PREFIX = "Think carefully about how you approach this. "

QUESTIONS = [
    "What is the capital of France?", "What is the capital of Japan?",
    "What is the capital of Australia?", "What is the capital of Canada?",
    "What is the capital of Brazil?", "What is the capital of Egypt?",
    "What is the capital of Italy?", "What is the capital of Spain?",
    "What is the capital of Germany?", "What is the capital of Russia?",
    "What is the capital of India?", "What is the chemical symbol for gold?",
    "What is the chemical symbol for sodium?", "What is the chemical formula for water?",
    "What is the chemical formula for table salt?", "Which element has the atomic number 1?",
    "What metal is liquid at room temperature?", "What is the hardest natural substance on Earth?",
    "What planet is closest to the sun?", "What is the largest planet in the solar system?",
    "What is the closest star to Earth?", "How many continents are there on Earth?",
    "What is the longest river in the world?", "What is the tallest mountain on Earth?",
    "Which ocean is the largest?", "What is the largest desert in the world?",
    "What is the largest country by land area?", "What is the smallest country in the world?",
    "What year did World War II end?", "What year did the Berlin Wall fall?",
    "In what year did the Titanic sink?", "Who was the first president of the United States?",
    "Who was the first person to walk on the moon?", "Who wrote Romeo and Juliet?",
    "Who wrote the novel 1984?", "Who painted the Mona Lisa?",
    "Who developed the theory of general relativity?", "Who discovered penicillin?",
    "What is the speed of light in a vacuum, approximately?",
    "What is the boiling point of water at sea level in Celsius?",
    "What is the freezing point of water in Fahrenheit?", "How many sides does a hexagon have?",
    "What is the square root of 144?", "What is the smallest prime number?",
    "How many minutes are in a full day?", "What gas do plants absorb from the atmosphere?",
    "What part of the cell is known as its powerhouse?",
    "How many bones are in the adult human body?", "Which blood type is the universal donor?",
    "What is the largest mammal on Earth?", "What is the tallest animal in the world?",
    "How many legs does a spider have?", "What sea creature has three hearts?",
    "What is the currency of Japan?", "What is the currency of the United Kingdom?",
    "What language is spoken in Brazil?", "How many players are on a soccer team on the field?",
    "How many strings does a standard guitar have?", "How many colors are in a rainbow?",
    "What gas makes up most of Earth's atmosphere?",
]
assert len(QUESTIONS) == 60


def spectral_features(x):
    n = int(x.shape[0])
    if n < 2:
        return None
    s = torch.linalg.svdvals(x)
    s2 = s * s
    total = float(s2.sum())
    if not math.isfinite(total) or total <= 0:
        return None
    p = (s2 / s2.sum()).clamp_min(1e-12)
    ent = float(-(p * p.log()).sum())
    return {"spectral_entropy": ent, "eff_rank": math.exp(ent),
            "stable_rank": float(s2.sum() / s2.max()),
            "n_rows": n, "n_cols": int(x.shape[1])}


class Capture:
    def __init__(self):
        self.chunks = []
    def __call__(self, module, inputs, output):
        self.chunks.append(output.detach().to(torch.float32).cpu())
    def reset(self):
        self.chunks = []
    def matrix(self):
        return torch.cat(self.chunks, dim=1)[0] if self.chunks else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()

    os.makedirs(RESULTS_DIR, exist_ok=True)
    out_path = os.path.join(RESULTS_DIR,
                            "trials_smoke.jsonl" if args.smoke else "trials.jsonl")
    max_new = 32 if args.smoke else MAX_NEW_TOKENS
    questions = QUESTIONS[:2] if args.smoke else QUESTIONS

    def log(msg):
        print(f"[{datetime.now().isoformat(timespec='seconds')}] {msg}", flush=True)

    log(f"model path: {MODEL_HINT}")
    tok = AutoTokenizer.from_pretrained(MODEL_HINT, tokenizer_type="qwen3",
                                        trust_remote_code=True, cache_dir=HF_CACHE)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_HINT, torch_dtype=torch.bfloat16, trust_remote_code=True,
        cache_dir=HF_CACHE).to("mps")
    model.eval()
    log("model loaded")

    layers_module = model.model.layers
    log(f"decoder has {len(layers_module)} layers")
    captures, handles = {}, []
    for li in LAYERS:
        if li >= len(layers_module):
            log(f"WARN: layer {li} out of range, skipping"); continue
        attn = getattr(layers_module[li], "self_attn", None)
        if attn is None or not hasattr(attn, "k_proj") or not hasattr(attn, "v_proj"):
            log(f"WARN: layer {li} has no self_attn.k_proj/v_proj, skipping"); continue
        kc, vc = Capture(), Capture()
        handles.append(attn.k_proj.register_forward_hook(kc))
        handles.append(attn.v_proj.register_forward_hook(vc))
        captures[li] = {"k": kc, "v": vc}
    if not captures:
        log("FATAL: no hookable layers"); sys.exit(1)
    log(f"hooked layers: {sorted(captures)}")

    trials = [(qi, c) for qi in range(len(questions))
              for c in ("cognitive", "metacognitive")]
    random.Random(BASE_SEED).shuffle(trials)

    done = set()
    if os.path.exists(out_path):
        with open(out_path) as f:
            for line in f:
                try:
                    rec = json.loads(line)
                    done.add((rec["question_idx"], rec["condition"]))
                except (json.JSONDecodeError, KeyError):
                    pass
        log(f"resuming: {len(done)} trials already complete")

    fout = open(out_path, "a")
    t_start = time.time()
    for t_idx, (qi, cond) in enumerate(trials):
        if (qi, cond) in done:
            continue
        q = questions[qi]
        user_msg = (META_PREFIX + q) if cond == "metacognitive" else q
        try:
            prompt = tok.apply_chat_template(
                [{"role": "user", "content": user_msg}], tokenize=False,
                add_generation_prompt=True, enable_thinking=False)
        except Exception:
            prompt = tok.apply_chat_template(
                [{"role": "user", "content": user_msg}], tokenize=False,
                add_generation_prompt=True)

        enc = tok(prompt, return_tensors="pt").to("mps")
        prompt_len = int(enc["input_ids"].shape[1])
        for c in captures.values():
            c["k"].reset(); c["v"].reset()

        seed = BASE_SEED + 1000 + t_idx
        torch.manual_seed(seed)
        t0 = time.time()
        with torch.no_grad():
            out = model.generate(**enc, do_sample=True, temperature=TEMPERATURE,
                                 max_new_tokens=max_new,
                                 pad_token_id=tok.eos_token_id)
        elapsed = time.time() - t0
        gen_ids = out[0][prompt_len:]
        gen_tokens = int(gen_ids.shape[0])

        feats = {}
        for li, c in captures.items():
            entry = {}
            for name in ("k", "v"):
                m = c[name].matrix()
                entry[name] = (spectral_features(m[prompt_len:])
                               if m is not None and m.shape[0] > prompt_len else None)
            feats[str(li)] = entry

        fout.write(json.dumps({
            "trial": t_idx, "question_idx": qi, "condition": cond, "question": q,
            "seed": seed, "prompt_tokens": prompt_len, "gen_tokens": gen_tokens,
            "response_text": tok.decode(gen_ids, skip_special_tokens=True),
            "features": feats, "elapsed_s": round(elapsed, 2),
        }) + "\n")
        fout.flush(); os.fsync(fout.fileno())
        log(f"trial {t_idx + 1}/{len(trials)} [{cond}] q={qi} "
            f"gen_tokens={gen_tokens} {elapsed:.1f}s")

    for h in handles:
        h.remove()
    fout.close()
    log(f"DONE in {(time.time() - t_start) / 60:.1f} min -> {out_path}")


if __name__ == "__main__":
    main()
