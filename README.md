# AI Engineering Coursework

## Part A — Hosted API Call
`api_call.py` calls a Llama 3.1 8B model hosted via Hugging Face's Inference Providers (Featherless AI).

To run:
1. Get a free token from huggingface.co (Settings → Access Tokens), with "Make calls to Inference Providers" permission
2. Set it as an environment variable: `setx HF_TOKEN "your-token"`
3. `pip install huggingface_hub`
4. `python api_call.py`

See `part_a_output.png` for a successful run.

## Part B — Local Model (Ollama)
Ran `llama3.2:3b` locally via Ollama. See `part_b_output.png` for the session.