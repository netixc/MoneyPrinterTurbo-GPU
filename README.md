# MoneyPrinterTurbo GPU

AI-powered automated video generation with GPU acceleration (NVENC + CUDA Whisper). Optimized for NVIDIA RTX GPUs.

## Features

- NVIDIA NVENC hardware video encoding (5-10x faster than CPU)
- CUDA-accelerated Whisper for subtitle generation (10x faster)
- FFmpeg 7.1 with full GPU support
- Multiple LLM providers (OpenAI, Pollinations, Moonshot, DeepSeek, etc.)
- Multiple TTS providers (Azure, SiliconFlow, OpenAI TTS)
- Free video materials from Pexels/Pixabay
- Automatic script generation, voiceover, and subtitle timing

## Installation

### Prerequisites

- Docker and Docker Compose
- NVIDIA GPU with driver 580.95.05 or newer
- NVIDIA Container Toolkit v1.17.8+

### Quick Start

```bash
# Clone the repository
git clone https://github.com/netixc/MoneyPrinterTurbo-GPU.git
cd MoneyPrinterTurbo-GPU

# Build and start containers
docker compose up --build -d

# Access Web UI
http://localhost:8501

# Access API
http://localhost:8080
```

## Configuration

Edit `config.toml` before starting:

### Video Materials

```toml
[app]
video_source = "pexels"  # or "pixabay"
pexels_api_keys = ["YOUR_API_KEY"]  # Register at https://www.pexels.com/api/
pixabay_api_keys = []  # Register at https://pixabay.com/api/docs/
```

### LLM Provider

Choose one provider and configure:

```toml
llm_provider = "pollinations"  # Options: openai, moonshot, deepseek, pollinations, ollama, etc.

# Pollinations (Free)
pollinations_api_key = ""
pollinations_base_url = "https://text.pollinations.ai/openai"
pollinations_model_name = "openai-fast"

# OpenAI
openai_api_key = "YOUR_API_KEY"
openai_base_url = "https://api.openai.com/v1"
openai_model_name = "gpt-4o-mini"

# DeepSeek
deepseek_api_key = "YOUR_API_KEY"
deepseek_base_url = "https://api.deepseek.com"
deepseek_model_name = "deepseek-chat"
```

### TTS Provider

Configure in WebUI or `config.toml`:

```toml
[azure]
# Azure TTS (Free tier available)
speech_key = "YOUR_KEY"
speech_region = "eastus"

[siliconflow]
# SiliconFlow TTS
api_key = "YOUR_KEY"

[openai_tts]
# OpenAI TTS or compatible endpoints
api_key = "YOUR_KEY"
base_url = "https://api.openai.com/v1"
model = "tts-1"  # or "tts-1-hd"
voice = "alloy"  # alloy, echo, fable, onyx, nova, shimmer
speed = 1.0      # Range: 0.25 to 4.0
```

### Subtitle Generation

```toml
subtitle_provider = "edge"  # Options: "edge" (free) or "whisper" (GPU-accelerated)

[whisper]
# Only effective when subtitle_provider = "whisper"
model_size = "large-v3"
device = "cuda"           # GPU acceleration
compute_type = "float16"  # FP16 for better performance
```

### GPU Settings

```toml
[whisper]
device = "cuda"           # Enable GPU for Whisper
compute_type = "float16"  # Use FP16 for RTX GPUs
```

Video encoding automatically uses `h264_nvenc` (GPU encoder) instead of CPU encoding.

### Redis (Optional)

```toml
enable_redis = false  # Set to true for task management
redis_host = "localhost"
redis_port = 6379
redis_db = 0
redis_password = ""
```

### Advanced Options

```toml
max_concurrent_tasks = 5      # Number of parallel video generation tasks
material_directory = ""       # Custom video materials folder
endpoint = ""                 # Custom API endpoint for external access

[proxy]
# http = "http://user:pass@proxy:1234"
# https = "http://user:pass@proxy:1234"
```

## Usage

### Web Interface

1. Open http://localhost:8501
2. Select TTS Server and configure API keys
3. Enter video subject/topic
4. Click "Generate Video"
5. Download from `./storage/tasks/<task_id>/final-1.mp4`

### API

```bash
# Generate video via API
curl -X POST http://localhost:8080/api/v1/video \
  -H "Content-Type: application/json" \
  -d '{
    "video_subject": "The future of AI",
    "video_aspect": "9:16"
  }'
```

## Performance

With RTX 3090 GPU:
- Video encoding: 5-10x faster (NVENC vs CPU)
- Subtitle generation: 10x faster (CUDA Whisper vs CPU)
- Overall pipeline: 2-3x faster end-to-end

## Hardware Requirements

- NVIDIA GPU with NVENC support (GTX 10 series or newer)
- 8GB+ GPU VRAM recommended
- 16GB+ system RAM
- SSD for faster video processing

## License

See [LICENSE](LICENSE) file for details.

## Credits

Based on [MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo) by harry0703

GPU optimizations and OpenAI TTS integration by Claude Code
