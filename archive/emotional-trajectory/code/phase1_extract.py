"""Phase 1: Activation extraction for emotion projection experiment.

Loads model, runs all stimuli, extracts per-layer:
  - Residual stream (pre-norm, last token)
  - Pre-RoPE K activations (per head, last token)
  - V activations (per head, last token)

Pipeline validation run — check shapes, ranges, NaN. No conclusions.

Usage:
  python phase1_extract.py --model-dir /path/to/model --stimuli stimuli.json --output activations.npz
  python phase1_extract.py --model-dir /path/to/model --stimuli stimuli.json --layers 1,5,11,23
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


def extract_activations(model, tokenizer, prompts, layer_indices, device="cpu"):
    """Run forward passes and extract residual, K, V at specified layers.

    Returns dict with keys like:
      residual_L3: (n_prompts, hidden_dim)
      k_pre_rope_L3_H0: (n_prompts, head_dim)
      v_L3_H0: (n_prompts, head_dim)
      token_counts: (n_prompts,)
    """
    results = {f"residual_L{l}": [] for l in layer_indices}
    for l in layer_indices:
        n_kv = model.config.num_key_value_heads
        for h in range(n_kv):
            results[f"k_pre_rope_L{l}_H{h}"] = []
            results[f"v_L{l}_H{h}"] = []
    results["token_counts"] = []

    hooks = []
    captured = {}

    def make_residual_hook(layer_idx):
        def hook_fn(module, args, kwargs):
            hidden = args[0] if args else kwargs.get("hidden_states")
            if hidden is not None:
                captured[f"residual_L{layer_idx}"] = hidden.detach()
            return None
        return hook_fn

    for l in layer_indices:
        layer = model.model.layers[l]
        hooks.append(layer.register_forward_pre_hook(
            make_residual_hook(l), with_kwargs=True
        ))

    # We need to intercept K and V AFTER projection but BEFORE RoPE
    # In Qwen2, self_attn computes:
    #   q = self.q_proj(hidden)
    #   k = self.k_proj(hidden)  <-- pre-RoPE K
    #   v = self.v_proj(hidden)
    #   Then applies rotary to q and k
    # We'll hook the projection weights directly

    kv_proj_hooks = []

    k_captures = {}
    v_captures = {}

    def make_k_proj_hook(layer_idx):
        def hook_fn(module, input, output):
            k_captures[layer_idx] = output.detach()
        return hook_fn

    def make_v_proj_hook(layer_idx):
        def hook_fn(module, input, output):
            v_captures[layer_idx] = output.detach()
        return hook_fn

    for l in layer_indices:
        layer = model.model.layers[l]
        kv_proj_hooks.append(layer.self_attn.k_proj.register_forward_hook(
            make_k_proj_hook(l)
        ))
        kv_proj_hooks.append(layer.self_attn.v_proj.register_forward_hook(
            make_v_proj_hook(l)
        ))

    print(f"Hooks registered on {len(layer_indices)} layers")

    for i, prompt in enumerate(prompts):
        if i % 20 == 0:
            print(f"  Processing {i}/{len(prompts)}...")

        inputs = tokenizer(prompt, return_tensors="pt", padding=False).to(device)
        seq_len = inputs["input_ids"].shape[1]
        results["token_counts"].append(seq_len)

        with torch.no_grad():
            model(**inputs)

        # Extract last-token activations
        for l in layer_indices:
            # Residual (pre-norm input to attention)
            res = captured[f"residual_L{l}"][0, -1, :].cpu().float().numpy()
            results[f"residual_L{l}"].append(res)

            # Pre-RoPE K (already captured by hook on k_proj)
            k_full = k_captures[l][0, -1, :].cpu().float().numpy()
            v_full = v_captures[l][0, -1, :].cpu().float().numpy()

            n_kv = model.config.num_key_value_heads
            head_dim = k_full.shape[0] // n_kv

            for h in range(n_kv):
                k_head = k_full[h * head_dim:(h + 1) * head_dim]
                v_head = v_full[h * head_dim:(h + 1) * head_dim]
                results[f"k_pre_rope_L{l}_H{h}"].append(k_head)
                results[f"v_L{l}_H{h}"].append(v_head)

        captured.clear()
        k_captures.clear()
        v_captures.clear()

    # Remove hooks
    for h in hooks + kv_proj_hooks:
        h.remove()

    # Convert to numpy arrays
    for key in results:
        results[key] = np.array(results[key])

    return results


def sanity_check(results, layer_indices, n_kv_heads):
    """Phase 1 sanity checks — shapes, ranges, NaN."""
    print(f"\n{'='*60}")
    print("SANITY CHECKS")
    print(f"{'='*60}")

    n_prompts = len(results["token_counts"])
    print(f"Prompts processed: {n_prompts}")
    print(f"Token counts: mean={results['token_counts'].mean():.1f}, "
          f"std={results['token_counts'].std():.1f}, "
          f"min={results['token_counts'].min()}, "
          f"max={results['token_counts'].max()}")

    all_ok = True
    for l in layer_indices:
        res = results[f"residual_L{l}"]
        print(f"\nLayer {l}:")
        print(f"  Residual: shape={res.shape}, "
              f"mean={res.mean():.4f}, std={res.std():.4f}, "
              f"nan={np.isnan(res).sum()}, inf={np.isinf(res).sum()}")

        if np.isnan(res).any() or np.isinf(res).any():
            print("  *** NaN/Inf DETECTED — STOP ***")
            all_ok = False

        for h in range(n_kv_heads):
            k = results[f"k_pre_rope_L{l}_H{h}"]
            v = results[f"v_L{l}_H{h}"]
            print(f"  K_H{h}: shape={k.shape}, mean={k.mean():.4f}, std={k.std():.4f}")
            print(f"  V_H{h}: shape={v.shape}, mean={v.mean():.4f}, std={v.std():.4f}")

            if np.isnan(k).any() or np.isnan(v).any():
                print(f"  *** NaN in K/V head {h} — STOP ***")
                all_ok = False

    if all_ok:
        print(f"\nAll checks PASSED. Pipeline is clean.")
    else:
        print(f"\nSANITY CHECKS FAILED. Do not proceed.")

    return all_ok


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-dir", required=True)
    parser.add_argument("--stimuli", required=True)
    parser.add_argument("--output", default="activations.npz")
    parser.add_argument("--layers", type=str, default=None,
                        help="Comma-separated layer indices (default: evenly spaced)")
    parser.add_argument("--device", default="cpu")
    args = parser.parse_args()

    stimuli = json.loads(Path(args.stimuli).read_text())
    prompts = [s["prompt"] for s in stimuli]
    categories = [s["category"] for s in stimuli]

    print(f"Loading model from {args.model_dir}...")
    try:
        tokenizer = AutoTokenizer.from_pretrained(args.model_dir, trust_remote_code=True)
    except (AttributeError, Exception):
        tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B", trust_remote_code=True)
        print("  (used fallback tokenizer)")
    model = AutoModelForCausalLM.from_pretrained(
        args.model_dir, dtype=torch.float32, trust_remote_code=True,
    )
    model.eval()

    n_layers = model.config.num_hidden_layers
    n_kv = model.config.num_key_value_heads

    if args.layers:
        layer_indices = [int(x) for x in args.layers.split(",")]
    else:
        layer_indices = [0, n_layers // 4, n_layers // 2, 3 * n_layers // 4, n_layers - 1]

    print(f"Model: {n_layers} layers, {model.config.hidden_size}d hidden, "
          f"{n_kv} KV heads, {model.config.hidden_size // model.config.num_attention_heads}d head")
    print(f"Extracting at layers: {layer_indices}")
    print(f"Stimuli: {len(prompts)} prompts")

    results = extract_activations(model, tokenizer, prompts, layer_indices, args.device)

    ok = sanity_check(results, layer_indices, n_kv)

    # Save activations and metadata
    outpath = Path(args.output)
    outpath.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        str(outpath),
        categories=np.array(categories),
        layer_indices=np.array(layer_indices),
        n_kv_heads=np.array(n_kv),
        **results,
    )
    print(f"\nSaved to {outpath} ({outpath.stat().st_size / 1024:.0f} KB)")

    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
