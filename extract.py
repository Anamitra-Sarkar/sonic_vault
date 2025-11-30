#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                           SONIC-VAULT :: DECODER                              ║
║                    Extract Hidden Payload from Audio Files                    ║
╚═══════════════════════════════════════════════════════════════════════════════╝

Decoder module that extracts hidden text from WAV files using LSB steganography.
The secret message is retrieved from the Least Significant Bits of audio samples.
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

# Maximum bytes to scan for hidden message (prevent hanging on large files)
MAX_SEARCH_BYTES = 10000000


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
║{Colors.YELLOW}                            [ DECODER MODULE ]                                 {Colors.CYAN}║
║{Colors.YELLOW}                       LSB Steganography Extraction                            {Colors.CYAN}║
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


def binary_to_text(binary: str) -> str:
    """
    Convert binary string to text.
    
    Args:
        binary: Binary string representation
    
    Returns:
        Decoded text string
    """
    text = ''
    # Process 8 bits at a time
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        if len(byte) == 8:
            char_code = int(byte, 2)
            # Only add printable characters or common whitespace
            if 32 <= char_code <= 126 or char_code in [9, 10, 13]:
                text += chr(char_code)
    return text


def extract_payload(stego_file: str, output_file: str = None) -> dict:
    """
    Extract hidden message from stego audio file using LSB steganography.
    
    Args:
        stego_file: Path to the stego WAV file containing hidden message
        output_file: Optional path to save extracted message
    
    Returns:
        Dictionary with extraction statistics and the message
    """
    print(f"\n{Colors.CYAN}[OPEN]{Colors.ENDC} Reading stego audio: {Colors.YELLOW}{stego_file}{Colors.ENDC}")
    
    with wave.open(stego_file, 'rb') as wav_in:
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
        frames = wav_in.readframes(n_frames)
    
    total_bytes = len(frames)
    print(f"{Colors.CYAN}[DATA]{Colors.ENDC} Total bytes to scan: {Colors.GREEN}{total_bytes:,}{Colors.ENDC}")
    
    # Extract LSBs
    print(f"\n{Colors.CYAN}[SCAN]{Colors.ENDC} Extracting LSBs from audio bytes...")
    
    binary_message = ''
    extracted_text = ''
    delimiter_found = False
    
    # We process in chunks for efficiency and progress display
    chunk_size = 8  # Process 8 bits (1 character) at a time
    max_search = min(total_bytes, MAX_SEARCH_BYTES)  # Limit search to prevent hanging on large files
    
    for i in range(0, max_search, chunk_size):
        # Extract 8 LSBs to form one character
        byte_chunk = ''
        for j in range(chunk_size):
            if i + j < len(frames):
                byte_chunk += str(frames[i + j] & 1)
        
        if len(byte_chunk) == 8:
            char_code = int(byte_chunk, 2)
            # Check for valid printable character or whitespace
            if 32 <= char_code <= 126 or char_code in [9, 10, 13]:
                extracted_text += chr(char_code)
                
                # Check for delimiter
                if extracted_text.endswith(DELIMITER):
                    delimiter_found = True
                    # Remove delimiter from message
                    extracted_text = extracted_text[:-len(DELIMITER)]
                    print_progress("Extracting Payload", max_search, max_search)
                    break
        
        if i % 80000 == 0:
            print_progress("Extracting Payload", min(i + chunk_size, max_search), max_search)
    
    if not delimiter_found:
        print(f"\n{Colors.YELLOW}[WARN]{Colors.ENDC} Delimiter not found - message may be incomplete or no hidden data")
    
    # Save to file if output specified
    if output_file and extracted_text:
        print(f"\n{Colors.CYAN}[SAVE]{Colors.ENDC} Saving extracted message to: {Colors.YELLOW}{output_file}{Colors.ENDC}")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(extracted_text)
    
    stats = {
        'stego_file': stego_file,
        'output_file': output_file,
        'message_length': len(extracted_text),
        'delimiter_found': delimiter_found,
        'message': extracted_text
    }
    
    return stats


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='SONIC-VAULT Decoder - Extract hidden payload from audio files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python extract.py -i stego_song.wav
  python extract.py -i stego_song.wav -o recovered.txt
  python extract.py --input hidden.wav --output message.txt
        """
    )
    
    parser.add_argument('-i', '--input', type=str, required=True,
                        help='Input stego WAV file (containing hidden message)')
    parser.add_argument('-o', '--output', type=str, default=None,
                        help='Optional output text file to save extracted message')
    
    args = parser.parse_args()
    
    print_banner()
    
    # Validate inputs
    if not os.path.exists(args.input):
        print(f"{Colors.RED}[ERROR]{Colors.ENDC} Input file not found: {args.input}")
        sys.exit(1)
    
    try:
        stats = extract_payload(
            stego_file=args.input,
            output_file=args.output
        )
        
        print(f"\n{Colors.GREEN}{'═' * 75}{Colors.ENDC}")
        print(f"{Colors.GREEN}[SUCCESS]{Colors.ENDC} Payload extracted successfully!")
        print(f"{Colors.GREEN}{'═' * 75}{Colors.ENDC}")
        
        if stats['delimiter_found']:
            print(f"{Colors.CYAN}[STATUS]{Colors.ENDC} Delimiter: {Colors.GREEN}FOUND{Colors.ENDC}")
        else:
            print(f"{Colors.CYAN}[STATUS]{Colors.ENDC} Delimiter: {Colors.YELLOW}NOT FOUND{Colors.ENDC}")
        
        print(f"{Colors.CYAN}[LENGTH]{Colors.ENDC} Message length: {Colors.YELLOW}{stats['message_length']:,} characters{Colors.ENDC}")
        
        if stats['output_file']:
            print(f"{Colors.CYAN}[FILE]{Colors.ENDC} Saved to: {Colors.YELLOW}{stats['output_file']}{Colors.ENDC}")
        
        print(f"\n{Colors.CYAN}╔═══════════════════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
        print(f"{Colors.CYAN}║{Colors.ENDC} {Colors.YELLOW}EXTRACTED SECRET MESSAGE:{Colors.ENDC}")
        print(f"{Colors.CYAN}╠═══════════════════════════════════════════════════════════════════════════════╣{Colors.ENDC}")
        
        # Print message with box formatting
        message = stats['message']
        if message:
            # Split by lines and print each line
            lines = message.split('\n')
            for line in lines:
                # Wrap long lines
                while len(line) > 75:
                    print(f"{Colors.CYAN}║{Colors.ENDC} {Colors.GREEN}{line[:75]}{Colors.ENDC}")
                    line = line[75:]
                print(f"{Colors.CYAN}║{Colors.ENDC} {Colors.GREEN}{line}{Colors.ENDC}")
        else:
            print(f"{Colors.CYAN}║{Colors.ENDC} {Colors.RED}(No message found){Colors.ENDC}")
        
        print(f"{Colors.CYAN}╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.ENDC}")
        
    except Exception as e:
        print(f"\n{Colors.RED}[ERROR]{Colors.ENDC} Failed to extract payload: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
