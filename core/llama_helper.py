import os
import subprocess
import time

from data_logger import log_interaction


def ask_llama(
    prompt: str,
    model_name: str | None = None,
    timeout: int = 120,
    retries: int = 2,
) -> str:
    """
    Send a prompt to a local Ollama model and return the cleaned response.
    Includes retry logic for empty output, model errors, and timeouts.
    """

    model_name = model_name or os.getenv("JARVIS_LLM_MODEL", "llama3")
    print("Thinking... please wait.")

    for attempt in range(retries + 1):
        try:
            proc = subprocess.run(
                ["ollama", "run", model_name, prompt],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="ignore",
                timeout=timeout,
            )

            out = (proc.stdout or "").strip()
            err = (proc.stderr or "").strip()

            if out:
                cleaned = (
                    out.replace("**", "")
                    .replace("*", "")
                    .replace("_", "")
                    .replace("#", "")
                    .replace("`", "")
                    .replace("###", "")
                ).strip()

                bad_responses = [
                    "provided a series of individual letters",
                    "please provide the actual headlines",
                    "it seems like you provided",
                ]
                if any(bad in cleaned.lower() for bad in bad_responses):
                    print("Model misunderstood the input, retrying...")
                    if attempt < retries:
                        time.sleep(2)
                        continue
                    return "Sorry, I could not summarize the text properly."

                log_interaction("llama_response", {"prompt": prompt, "response": cleaned})
                return cleaned

            if err:
                print(f"Model error on attempt {attempt + 1}: {err}")
                if attempt < retries:
                    time.sleep(2)
                    continue
                return "Sorry, the model returned an error."

            if attempt < retries:
                print("Empty response, retrying...")
                time.sleep(2)
                continue

            return "Sorry, the model returned an empty response."

        except subprocess.TimeoutExpired:
            print(f"Model timed out on attempt {attempt + 1}.")
            if attempt < retries:
                time.sleep(2)
                continue
            return "Sorry, the model took too long to respond."

        except FileNotFoundError:
            return "LLaMA (Ollama) is not installed or not found."

        except Exception as e:
            print(f"ask_llama error: {e}")
            if attempt < retries:
                print("Retrying...")
                time.sleep(2)
                continue
            return "Sorry, I could not get a response from the model."
