import os
import requests

def download_file(url, local_filename):
    print(f"Downloading {url} to {local_filename}...", flush=True)
    temp_filename = local_filename + ".tmp"
    
    # Retry configuration
    max_retries = 5
    for attempt in range(1, max_retries + 1):
        try:
            r = requests.get(url, stream=True, timeout=(30, 60))
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))
            print(f"Connection established. Content size: {total_size / (1024*1024):.2f} MB", flush=True)
            
            downloaded = 0
            # Download in 1MB chunks
            with open(temp_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size:
                            percent = (downloaded / total_size) * 100
                            print(f"Progress: {downloaded / (1024*1024):.2f} MB / {total_size / (1024*1024):.2f} MB ({percent:.2f}%)", flush=True)
                        else:
                            print(f"Progress: {downloaded / (1024*1024):.2f} MB", flush=True)
            
            # Rename temp file to destination
            if os.path.exists(local_filename):
                os.remove(local_filename)
            os.rename(temp_filename, local_filename)
            print(f"Successfully downloaded to {local_filename}", flush=True)
            return True
        except Exception as e:
            print(f"Attempt {attempt}/{max_retries} failed with error: {e}", flush=True)
            if attempt == max_retries:
                raise e
            print("Retrying in 5 seconds...", flush=True)
            import time
            time.sleep(5)
    return False

def main():
    target_dir = r"C:\Users\buvan\.cache\huggingface\hub\models--cross-encoder--mmarco-mMiniLMv2-L12-H384-v1\snapshots\1427fd652930e4ba29e8149678df786c240d8825"
    os.makedirs(target_dir, exist_ok=True)
    
    files = {
        "config.json": "https://huggingface.co/cross-encoder/mmarco-mMiniLMv2-L12-H384-v1/resolve/main/config.json",
        "tokenizer_config.json": "https://huggingface.co/cross-encoder/mmarco-mMiniLMv2-L12-H384-v1/resolve/main/tokenizer_config.json",
        "special_tokens_map.json": "https://huggingface.co/cross-encoder/mmarco-mMiniLMv2-L12-H384-v1/resolve/main/special_tokens_map.json",
        "sentencepiece.bpe.model": "https://huggingface.co/cross-encoder/mmarco-mMiniLMv2-L12-H384-v1/resolve/main/sentencepiece.bpe.model",
        "tokenizer.json": "https://huggingface.co/cross-encoder/mmarco-mMiniLMv2-L12-H384-v1/resolve/main/tokenizer.json",
        "model.safetensors": "https://huggingface.co/cross-encoder/mmarco-mMiniLMv2-L12-H384-v1/resolve/main/model.safetensors"
    }
    
    for filename, url in files.items():
        local_path = os.path.join(target_dir, filename)
        # Skip download if file already exists and is not 0 bytes
        if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
            print(f"{filename} already exists and is valid. Skipping...", flush=True)
            continue
        download_file(url, local_path)
        
    print("All model files downloaded successfully!", flush=True)

if __name__ == "__main__":
    main()
