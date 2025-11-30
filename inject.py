#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                           SONIC-VAULT :: ENCODER                              ║
║                    Inject Secret Payload into Audio Files                     ║
╚═══════════════════════════════════════════════════════════════════════════════╝

Encoder module that hides encrypted text inside WAV files using LSB steganography.
The secret message is embedded in the Least Significant Bits of audio samples.
"""

import wave
import argparse
import sys
import os


# Terminal colors for hacker aesthetic
class Colors:
    HEADER = '\033[95m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


# Delimiter to mark the end of the hidden message
DELIMITER = '#####'


def print_banner():
    """Print the hacker-style banner."""
    banner = f"""
{Colors.CYAN}╔═══════════════════════════════════════════════════════════════════════════════╗
║{Colors.GREEN}   ███████╗ ██████╗ ███╗   ██╗██╗ ██████╗    ██╗   ██╗ █████╗ ██╗   ██╗██╗  ████████╗{Colors.CYAN}║
║{Colors.GREEN}   ██╔════╝██╔═══██╗████╗  ██║██║██╔════╝    ██║   ██║██╔══██╗██║   ██║██║  ╚══██╔══╝{Colors.CYAN}║
║{Colors.GREEN}   ███████╗██║   ██║██╔██╗ ██║██║██║         ██║   ██║███████║██║   ██║██║     ██║   {Colors.CYAN}║
║{Colors.GREEN}   ╚════██║██║   ██║██║╚██╗██║██║██║         ╚██╗ ██╔╝██╔══██║██║   ██║██║     ██║   {Colors.CYAN}║
║{Colors.GREEN}   ███████║╚██████╔╝██║ ╚████║██║╚██████╗     ╚████╔╝ ██║  ██║╚██████╔╝███████╗██║   {Colors.CYAN}║
║{Colors.GREEN}   ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝ ╚═════╝      ╚═══╝  ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝   {Colors.CYAN}║
╠═══════════════════════════════════════════════════════════════════════════════╣
║{Colors.YELLOW}                            [ ENCODER MODULE ]                                 {Colors.CYAN}║
║{Colors.YELLOW}                       LSB Steganography Injection                             {Colors.CYAN}║
╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.ENDC}
"""
    print(banner)


def print_progress(label: str, current: int, total: int, width: int = 40):
    """Print a hacker-style progress bar."""
    percent = current / total if total > 0 else 1
    filled = int(width * percent)
    bar = '█' * filled + '░' * (width - filled)
    sys.stdout.write(f'\r{Colors.CYAN}[{label}]{Colors.ENDC} {Colors.GREEN}{bar}{Colors.ENDC} {Colors.YELLOW}{percent*100:.1f}%{Colors.ENDC}')
    sys.stdout.flush()
    if current == total:
        print()


def text_to_binary(text: str) -> str:
    """
    Convert text to binary string representation.
    
    Args:
        text: The text to convert
    
    Returns:
        Binary string representation of the text
    """
    binary = ''
    for char in text:
        # Convert each character to 8-bit binary
        binary += format(ord(char), '08b')
    return binary


def inject_payload(cover_file: str, secret_file: str, output_file: str) -> dict:
    """
    Inject secret message into cover audio file using LSB steganography.
    
    Args:
        cover_file: Path to the cover WAV file
        secret_file: Path to the secret text file
        output_file: Path for the output stego WAV file
    
    Returns:
        Dictionary with injection statistics
    """
    # Read the secret message
    print(f"\n{Colors.CYAN}[LOAD]{Colors.ENDC} Reading secret payload from: {Colors.YELLOW}{secret_file}{Colors.ENDC}")
    
    with open(secret_file, 'r', encoding='utf-8') as f:
        secret_message = f.read()
    
    # Append delimiter to mark end of message
    secret_with_delimiter = secret_message + DELIMITER
    
    print(f"{Colors.CYAN}[DATA]{Colors.ENDC} Secret message length: {Colors.GREEN}{len(secret_message)} characters{Colors.ENDC}")
    print(f"{Colors.CYAN}[DELM]{Colors.ENDC} Delimiter appended: {Colors.GREEN}{DELIMITER}{Colors.ENDC}")
    
    # Convert to binary
    print(f"{Colors.CYAN}[CONV]{Colors.ENDC} Converting payload to binary...")
    binary_message = text_to_binary(secret_with_delimiter)
    message_bits = len(binary_message)
    
    print(f"{Colors.CYAN}[BITS]{Colors.ENDC} Total bits to inject: {Colors.GREEN}{message_bits:,}{Colors.ENDC}")
    
    # Open the cover audio file
    print(f"\n{Colors.CYAN}[OPEN]{Colors.ENDC} Reading cover audio: {Colors.YELLOW}{cover_file}{Colors.ENDC}")
    
    with wave.open(cover_file, 'rb') as wav_in:
        # Get audio parameters
        n_channels = wav_in.getnchannels()
        sample_width = wav_in.getsampwidth()
        frame_rate = wav_in.getframerate()
        n_frames = wav_in.getnframes()
        
        print(f"{Colors.CYAN}[INFO]{Colors.ENDC} Channels: {Colors.GREEN}{n_channels}{Colors.ENDC}")
        print(f"{Colors.CYAN}[INFO]{Colors.ENDC} Sample Width: {Colors.GREEN}{sample_width} bytes{Colors.ENDC}")
        print(f"{Colors.CYAN}[INFO]{Colors.ENDC} Frame Rate: {Colors.GREEN}{frame_rate} Hz{Colors.ENDC}")
        print(f"{Colors.CYAN}[INFO]{Colors.ENDC} Total Frames: {Colors.GREEN}{n_frames:,}{Colors.ENDC}")
        
        # Read all audio frames
        frames = bytearray(wav_in.readframes(n_frames))
    
    # Check capacity
    capacity = len(frames)
    print(f"{Colors.CYAN}[CAP]{Colors.ENDC} Audio capacity: {Colors.GREEN}{capacity:,} bits{Colors.ENDC}")
    
    if message_bits > capacity:
        raise ValueError(
            f"Message too large! Need {message_bits:,} bits, but audio only has {capacity:,} bytes available."
        )
    
    usage_percent = (message_bits / capacity) * 100
    print(f"{Colors.CYAN}[USE]{Colors.ENDC} Capacity usage: {Colors.GREEN}{usage_percent:.4f}%{Colors.ENDC}")
    
    # Inject the message using LSB
    print(f"\n{Colors.CYAN}[HACK]{Colors.ENDC} Injecting payload into audio bytes...")
    
    original_bytes = bytes(frames[:message_bits])  # Store original for distortion calc
    
    for i, bit in enumerate(binary_message):
        # Clear the LSB and set it to our bit
        frames[i] = (frames[i] & 0xFE) | int(bit)
        
        if i % 10000 == 0 or i == message_bits - 1:
            print_progress("Injecting Payload", i + 1, message_bits)
    
    # Calculate distortion
    modified_bytes = bytes(frames[:message_bits])
    bits_changed = sum(
        bin(a ^ b).count('1') for a, b in zip(original_bytes, modified_bytes)
    )
    total_bits = len(original_bytes) * 8
    distortion = (bits_changed / total_bits) * 100 if total_bits > 0 else 0
    
    # Write the stego file
    print(f"\n{Colors.CYAN}[SAVE]{Colors.ENDC} Writing stego audio to: {Colors.YELLOW}{output_file}{Colors.ENDC}")
    
    with wave.open(output_file, 'wb') as wav_out:
        wav_out.setnchannels(n_channels)
        wav_out.setsampwidth(sample_width)
        wav_out.setframerate(frame_rate)
        wav_out.writeframes(bytes(frames))
    
    # Calculate file size
    file_size = os.path.getsize(output_file)
    
    stats = {
        'cover_file': cover_file,
        'secret_file': secret_file,
        'output_file': output_file,
        'message_length': len(secret_message),
        'bits_injected': message_bits,
        'audio_capacity': capacity,
        'usage_percent': usage_percent,
        'distortion_percent': distortion,
        'file_size': file_size
    }
    
    return stats


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='SONIC-VAULT Encoder - Inject secret payload into audio files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python inject.py -c cover.wav -s secret.txt
  python inject.py -c cover.wav -s secret.txt -o hidden.wav
  python inject.py --cover song.wav --secret message.txt --output stego.wav
        """
    )
    
    parser.add_argument('-c', '--cover', type=str, required=True,
                        help='Cover WAV file (the audio to hide message in)')
    parser.add_argument('-s', '--secret', type=str, required=True,
                        help='Secret text file (the message to hide)')
    parser.add_argument('-o', '--output', type=str, default='stego_song.wav',
                        help='Output stego WAV file (default: stego_song.wav)')
    
    args = parser.parse_args()
    
    print_banner()
    
    # Validate inputs
    if not os.path.exists(args.cover):
        print(f"{Colors.RED}[ERROR]{Colors.ENDC} Cover file not found: {args.cover}")
        sys.exit(1)
    
    if not os.path.exists(args.secret):
        print(f"{Colors.RED}[ERROR]{Colors.ENDC} Secret file not found: {args.secret}")
        sys.exit(1)
    
    try:
        stats = inject_payload(
            cover_file=args.cover,
            secret_file=args.secret,
            output_file=args.output
        )
        
        print(f"\n{Colors.GREEN}{'═' * 75}{Colors.ENDC}")
        print(f"{Colors.GREEN}[SUCCESS]{Colors.ENDC} Payload injected successfully!")
        print(f"{Colors.GREEN}{'═' * 75}{Colors.ENDC}")
        print(f"{Colors.CYAN}[FILE]{Colors.ENDC} Output saved to: {Colors.YELLOW}{stats['output_file']}{Colors.ENDC}")
        print(f"{Colors.CYAN}[SIZE]{Colors.ENDC} File Size: {Colors.YELLOW}{stats['file_size']:,} bytes{Colors.ENDC}")
        print(f"{Colors.CYAN}[DATA]{Colors.ENDC} Hidden: {Colors.YELLOW}{stats['message_length']:,} characters ({stats['bits_injected']:,} bits){Colors.ENDC}")
        print(f"{Colors.CYAN}[DIST]{Colors.ENDC} Distortion Level: {Colors.YELLOW}{stats['distortion_percent']:.4f}%{Colors.ENDC}")
        print(f"{Colors.GREEN}{'═' * 75}{Colors.ENDC}")
        print(f"\n{Colors.CYAN}[TIP]{Colors.ENDC} Use extract.py to retrieve the hidden message")
        
    except ValueError as e:
        print(f"\n{Colors.RED}[ERROR]{Colors.ENDC} {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}[ERROR]{Colors.ENDC} Failed to inject payload: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
