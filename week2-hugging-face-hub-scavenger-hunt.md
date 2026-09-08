# Week 2 Assignment: Hugging Face Hub Scavenger Hunt

## Overview

Same fields I walked through in Monday's demo: parameter count/size, architecture family, license, tokenizer/vocab size. Pick 3 models, record those fields, run a tokenizer comparison across languages, check context window against this week's reading, then write a short reflection tying it back to a real project decision.

*Same order I used in Monday's demo: parameter count/size near the top of the card, architecture family in the description, license in the metadata, tokenizer/vocab size in tokenizer_config.json (or just test the model directly in a tokenizer tool).*

## How to Submit

1. Fill out this file directly (replace the `_____` placeholders and bracketed instructions with your answers).
2. Commit this file to the same GitHub repo you created for Assignment 1, using this exact filename: `week2-tokenizer-model-comparison.md`.
3. Push your commit, then submit a link to the file as instructed for this course.

---

## Part 1: Choose 3 Models

1. Go to huggingface.co/models.
2. Pick 3 models that actually make a meaningful comparison — not three near-identical variants of the same model. At least 2 different organizations/families, ideally a mix of sizes (small under ~3B, mid-size, larger).
3. Pick based on your own interests. Got a project idea? Use models you'd actually consider for it.


I chose the character voice message generator as my project idea, so I picked three text-to-speech models that could work for it: Fish Speech V1.5 (Fish Audio), XTTS v2 (Coqui), and Kokoro-82M (Hexgrad). These are three different orgs, and the sizes vary a lot: Kokoro at 82M, XTTS v2 at 467M, and Fish Speech's exact parameter count isn't published on its own card, though it's commonly cited around 500M elsewhere.

## Part 2: Record Your Findings

Where to find each field, if you get stuck:
- **Parameter count / size** — near the top of the card, sometimes right in the model's name (e.g. "7B" = 7 billion parameters).
- **Architecture family** — in the description text, or config.json under "Files and Versions."
- **License** — shown as a tag near the top, and always in the YAML metadata block.
- **Tokenizer / vocab size** — check tokenizer_config.json or config.json under "Files and Versions" for vocab_size. Can't find it? Note "not published" — that's a useful observation on its own.


| Model | Link | Parameter count / size | Architecture family | License | Tokenizer / vocab size |
|---|---|---|---|---|---|
| Model 1: Fish Speech V1.5 | https://huggingface.co/fishaudio/fish-speech-1.5 | Not stated on its own card. ~500M is mentioned only in a competing model's README (Kokoro-82M), not Fish Speech's own documentation. | Dual-AR (dual autoregressive transformer) | CC-BY-NC-SA-4.0 | 102,048 (vocab_size in config.json). The repo also ships a tokenizer.tiktoken file, so it has a real token vocabulary, not just a phonemizer. |
| Model 2: XTTS v2 | https://huggingface.co/coqui/XTTS-v2 | 467M | GPT-2-style text encoder + DVAE + HiFi-GAN vocoder | coqui-public-model-license (non-commercial) | Has vocab.json on the repo, but no vocab_size number published on the card |
| Model 3: Kokoro-82M | https://huggingface.co/hexgrad/Kokoro-82M | 82M | StyleTTS 2 + ISTFTNet, decoder-only | Apache 2.0 | Not applicable. It does not use a conventional text tokenizer at all. It converts input text into phoneme representations using espeak-ng before speech generation. |

## Part 3: Tokenizer Comparison Exercise

Use a tokenizer tool that supports multiple model families (tiktokenizer.vercel.app works) and test all 3 models with the same three inputs:

- **Test sentence (use this exact sentence for all 3 models):** "I love learning about artificial intelligence."
- **Language A:** translate the test sentence into a Latin-script European language — Spanish, French, German, whatever. Same translation across all 3 models.
- **Language B:** translate it into a non-Latin-script language — Japanese, Arabic, Korean, Hindi, your call. Same translation across all 3 models.

I want to point out that I only used the Qwen/HunyuanOCR/PaddleOCR-VL models here to test out the tokenizer tool for the assignment. My actual project idea is still the character voice message generator (Fish Speech V1.5, XTTS v2, and Kokoro-82M), which is what I used for Parts 2 and the rest of this assignment. It makes sense that those three didn't show up as text tokens or had no vocab size listed, since they are speech models and not language models. They turn text into audio instead of turning text into more text.

**Sentences used for the test:**

- English: "I love learning about artificial intelligence."
- Spanish: "Me encanta aprender sobre inteligencia artificial."
- Japanese: "私は人工知能について学ぶのが大好きです。"

**Test run to confirm tiktokenizer's coverage (using Qwen, HunyuanOCR, PaddleOCR-VL as a check):**

| Model | Test sentence tokens | Language A used | Language A tokens | Language B used | Language B tokens |
|---|---|---|---|---|---|
| HunyuanOCR | N/A, not supported in tiktokenizer | Spanish | N/A | Japanese | N/A |
| PaddleOCR-VL | N/A, not supported in tiktokenizer | Spanish | N/A | Japanese | N/A |
| Qwen2-VL / Qwen3-VL (via Qwen2.5-72B tokenizer) | 7 | Spanish | 9 | Japanese | 12 |

**My actual 3 models for this assignment:**

| Model | Test sentence tokens | Language A used | Language A tokens | Language B used | Language B tokens |
|---|---|---|---|---|---|
| Fish Speech V1.5 | N/A, not supported in tiktokenizer | Spanish | N/A | Japanese | N/A |
| XTTS v2 | N/A, not supported in tiktokenizer | Spanish | N/A | Japanese | N/A |
| Kokoro-82M | Not applicable, uses IPA phonemes via espeak-ng instead of a text token vocabulary | Spanish | Not applicable | Japanese | Not applicable |

*Fish Speech has a real tokenizer (tokenizer.tiktoken file, vocab_size 102,048 in config.json). It just isn't one of the models tiktokenizer supports. XTTS has a vocab.json file but no published vocab_size number. Kokoro does not use a text tokenizer at all. It converts text into phonemes instead. Based on the Qwen test above, the Japanese version used more tokens than the English or Spanish ones.*

## Part 4: Context Window Check

For each model, look up its context window — the max tokens it can handle in one request. Usually on the card or in the config file.

| Model | Context window (tokens) | Source (URL or where you found it) |
|---|---|---|
| Fish Speech V1.5 | 8,192 (max_seq_len in config.json) | huggingface.co/fishaudio/fish-speech-1.5/blob/main/config.json |
| XTTS v2 | 250 characters per synthesis call (roughly 40-50 words). Text longer than that gets a truncation warning unless automatic sentence-splitting is enabled, which just breaks it into multiple 250-character calls internally. | Coqui TTS GitHub repo (coqui-ai/TTS discussions/docs) |
| Kokoro-82M | ~500 tokens max, with the maintainers recommending 100-200 token chunks for best quality. | huggingface.co/nvidia/kokoro-82M-onnx-opt model card |


**Now do the math for at least one model:** Chapter 2 is roughly 62 pages. Using ~500–600 words/page and ~0.75 words/token, estimate the total token count. Would the whole reading fit in that model's context window in one API call, with room left for a response? Show your work and your conclusion.

> I'll do the math using both Kokoro and Fish Speech since they both have real published numbers.
>
> - Chapter 2 is about 62 pages x 550 words/page (midpoint of 500-600) = 34,100 words
> - 34,100 words / 0.75 words per token = about 45,467 tokens
>
> For Kokoro's ~500-token limit, that's about 91 separate calls minimum. For Fish Speech's 8,192-token limit, that's about 5.55, so at least 6 chunks. Neither model gets close to fitting the chapter in one call, but Fish Speech's larger context does mean noticeably fewer chunks than Kokoro would need. There is also no "room left for a response" concept here the way an LLM would need, since the output is just audio for whatever chunk you feed in, not a generated reply.
>
> This actually works out fine for my project though. A character voice message generator is not meant to read whole chapters out loud, it is meant to generate short encouraging clips for a kid, so a small per-call limit like this is not really a dealbreaker the way it would be for a model meant to summarize or read long documents.


## Part 5: Comparison Reflection (300–400 words)

Answer all four:

- What's the biggest difference between your 3 models — size, architecture, license, tokenizer, something else?
- If you had to pick one for a real project, which one and why? Don't just say "the biggest one" — factor in license restrictions and whether the project actually needs that much size.
- Would your pick change for a multilingual or cost-sensitive use case, based on what you found in Part 3? Why or why not?
- Would your pick change for a use case involving long documents (full reports, long transcripts), based on the context window math in Part 4? Why or why not?

> Thinking about my three models, the biggest difference isn't size, it's what they can actually do. Kokoro is small and has the easiest license, but it only works with preset voices, no cloning. Fish Speech and XTTS can both clone a voice from a short clip, which is the whole point of my project, but both have non-commercial licenses.
>
> For this project I'd go with Fish Speech V1.5. The main reason is language support. I want people anywhere to be able to use this, and Fish Speech covers 13 languages with real training hours behind each one: over 300k hours each for English and Chinese, over 100k for Japanese, and about 20k each for German, French, Spanish, Korean, Arabic, and Russian. XTTS clones from a shorter clip and documents its specs more clearly, but it doesn't have that same language depth, so it doesn't fit what I actually want to build.
>
> Long documents don't really change anything here. XTTS caps at 250 characters per call, Fish Speech at 8,192 tokens, Kokoro at about 500 tokens. None of them are meant for reading something long, but that's fine since a voice message is supposed to be short anyway.
>
> If the app ever took off, I'd want a conversational mode too. Fish Speech's Dual-AR setup is basically built like a normal LLM under the hood, and the newer S2 Pro version in that same family already has multi-turn conversation and multi-speaker support. So Fish Speech covers both things I care about long term, going multilingual and eventually going conversational, even with the messier documentation and the license I'd have to deal with later.
