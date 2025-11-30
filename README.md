# SONIC-VAULT 🔐🎵

> A powerful steganography tool to hide encrypted text inside Audio Files using LSB (Least Significant Bit) manipulation.

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║   ███████╗ ██████╗ ███╗   ██╗██╗ ██████╗    ██╗   ██╗ █████╗ ██╗   ██╗██╗  ████████╗║
║   ██╔════╝██╔═══██╗████╗  ██║██║██╔════╝    ██║   ██║██╔══██╗██║   ██║██║  ╚══██╔══╝║
║   ███████╗██║   ██║██╔██╗ ██║██║██║         ██║   ██║███████║██║   ██║██║     ██║   ║
║   ╚════██║██║   ██║██║╚██╗██║██║██║         ╚██╗ ██╔╝██╔══██║██║   ██║██║     ██║   ║
║   ███████║╚██████╔╝██║ ╚████║██║╚██████╗     ╚████╔╝ ██║  ██║╚██████╔╝███████╗██║   ║
║   ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝ ╚═════╝      ╚═══╝  ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝   ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

## 🎯 Overview

SONIC-VAULT injects secret payloads into `.wav` files by manipulating the Least Significant Bits (LSB) of audio frames. The modification is imperceptible to the human ear, making it perfect for covert communication.

## 📋 Requirements

- **Python:** 3.10+
- **Libraries:** `wave` (Native), `struct`, `math` (all built-in)

No external dependencies required! 🎉

## 🛠️ Modules

### 1. Tone Generator (`generate_tone.py`)
Creates simple sine wave `.wav` files for testing.

```bash
# Generate a 5-second 440Hz tone (default)
python generate_tone.py -o cover.wav

# Generate a 10-second 880Hz tone
python generate_tone.py -o test.wav -d 10 -f 880

# Custom sample rate
python generate_tone.py -o audio.wav -d 60 -f 440 -r 48000
```

**Options:**
| Flag | Description | Default |
|------|-------------|---------|
| `-o, --output` | Output WAV file | `cover.wav` |
| `-d, --duration` | Duration in seconds | `5.0` |
| `-f, --frequency` | Frequency in Hz | `440.0` |
| `-r, --rate` | Sample rate in Hz | `44100` |
| `-a, --amplitude` | Amplitude (0-32767) | `16000` |

### 2. Encoder (`inject.py`)
Hides secret messages inside audio files.

```bash
# Basic usage
python inject.py -c cover.wav -s secret.txt

# Specify output file
python inject.py -c cover.wav -s secret.txt -o hidden.wav
```

**Options:**
| Flag | Description | Default |
|------|-------------|---------|
| `-c, --cover` | Cover WAV file (required) | - |
| `-s, --secret` | Secret text file (required) | - |
| `-o, --output` | Output stego WAV file | `stego_song.wav` |

### 3. Decoder (`extract.py`)
Extracts hidden messages from stego audio files.

```bash
# Display extracted message
python extract.py -i stego_song.wav

# Save to file
python extract.py -i stego_song.wav -o recovered.txt
```

**Options:**
| Flag | Description | Default |
|------|-------------|---------|
| `-i, --input` | Input stego WAV file (required) | - |
| `-o, --output` | Output text file (optional) | - |

## 🚀 Quick Start

```bash
# Step 1: Generate a test audio file
python generate_tone.py -o cover.wav -d 5

# Step 2: Create your secret message
echo "This is a TOP SECRET message!" > secret.txt

# Step 3: Hide the message in the audio
python inject.py -c cover.wav -s secret.txt -o stego_song.wav

# Step 4: Extract the hidden message
python extract.py -i stego_song.wav
```

## 🔬 How It Works

### Encoding Process
1. **Convert to Binary:** Secret text → ASCII → Binary (01010101...)
2. **Append Delimiter:** Add `#####` to mark message end
3. **Read Audio Frames:** Load WAV file as byte array
4. **LSB Injection:** Replace the last bit of each audio byte with one bit of the secret message
5. **Write Output:** Save modified audio as new WAV file

### Decoding Process
1. **Read Audio Frames:** Load stego WAV file as byte array
2. **Extract LSBs:** Get the last bit of each byte
3. **Reconstruct Binary:** Combine bits into binary string
4. **Convert to Text:** Binary → ASCII → Text
5. **Find Delimiter:** Stop when `#####` is found

## 📊 Sample Output

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                            [ ENCODER MODULE ]                                 ║
╚═══════════════════════════════════════════════════════════════════════════════╝

[LOAD] Reading secret payload from: secret.txt
[DATA] Secret message length: 147 characters
[BITS] Total bits to inject: 1,216

[Injecting Payload] ████████████████████████████████████████ 100.0%

═══════════════════════════════════════════════════════════════════════════
[SUCCESS] Payload injected successfully!
═══════════════════════════════════════════════════════════════════════════
[FILE] Output saved to: stego_song.wav
[DIST] Distortion Level: 0.0001%
```

## ⚠️ Limitations

- Only works with `.wav` files (uncompressed audio)
- Message capacity depends on audio file size
- Each byte can store 1 bit of secret data
- Maximum message size = (audio bytes / 8) characters

## 🔒 Security Notes

- This is a steganography tool, not encryption
- For maximum security, encrypt your message before hiding
- The delimiter pattern (`#####`) could be detected by analysis
- Consider using larger audio files for better concealment

## 📜 License

Apache License 2.0 - See [LICENSE](LICENSE) for details.

---

*Built with ❤️ by a Cryptographer & DSP Engineer*
