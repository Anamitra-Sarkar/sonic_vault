#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                           SONIC-VAULT :: TONE GENERATOR                       ║
║                         Generate Test WAV Files for Testing                   ║
╚═══════════════════════════════════════════════════════════════════════════════╝

Generates a simple sine wave .wav file for testing the steganography tool.
"""

import wave
import struct
import math
import argparse
import sys


# Terminal colors for hacker aesthetic
class Colors:
    HEADER = '\033[95m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


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
║{Colors.YELLOW}                         [ TONE GENERATOR MODULE ]                             {Colors.CYAN}║
║{Colors.YELLOW}                    Audio Steganography Test File Creator                      {Colors.CYAN}║
╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.ENDC}
"""
    print(banner)


def print_progress(label: str, current: int, total: int, width: int = 40):
    """Print a hacker-style progress bar."""
    percent = current / total
    filled = int(width * percent)
    bar = '█' * filled + '░' * (width - filled)
    sys.stdout.write(f'\r{Colors.CYAN}[{label}]{Colors.ENDC} {Colors.GREEN}{bar}{Colors.ENDC} {Colors.YELLOW}{percent*100:.1f}%{Colors.ENDC}')
    sys.stdout.flush()
    if current == total:
        print()


def generate_wav(output_file: str, duration: float = 5.0, frequency: float = 440.0,
                 sample_rate: int = 44100, amplitude: int = 16000) -> dict:
    """
    Generate a sine wave WAV file.
    
    Args:
        output_file: Output WAV file path
        duration: Duration in seconds
        frequency: Frequency of the tone in Hz
        sample_rate: Sample rate in Hz
        amplitude: Wave amplitude (max 32767 for 16-bit)
    
    Returns:
        Dictionary with file statistics
    """
    num_samples = int(sample_rate * duration)
    
    print(f"\n{Colors.CYAN}[INIT]{Colors.ENDC} Generating audio parameters...")
    print(f"{Colors.CYAN}[FREQ]{Colors.ENDC} Frequency: {Colors.GREEN}{frequency} Hz{Colors.ENDC}")
    print(f"{Colors.CYAN}[RATE]{Colors.ENDC} Sample Rate: {Colors.GREEN}{sample_rate} Hz{Colors.ENDC}")
    print(f"{Colors.CYAN}[TIME]{Colors.ENDC} Duration: {Colors.GREEN}{duration} seconds{Colors.ENDC}")
    print(f"{Colors.CYAN}[DATA]{Colors.ENDC} Total Samples: {Colors.GREEN}{num_samples:,}{Colors.ENDC}")
    print()
    
    # Open WAV file for writing
    with wave.open(output_file, 'wb') as wav_file:
        # Set parameters: mono, 16-bit, specified sample rate
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)  # 2 bytes = 16 bits
        wav_file.setframerate(sample_rate)
        
        # Generate and write samples
        chunk_size = 1000
        samples_written = 0
        
        while samples_written < num_samples:
            chunk_end = min(samples_written + chunk_size, num_samples)
            frames = b''
            
            for i in range(samples_written, chunk_end):
                # Generate sine wave sample
                value = int(amplitude * math.sin(2 * math.pi * frequency * i / sample_rate))
                # Pack as signed 16-bit little-endian
                frames += struct.pack('<h', value)
            
            wav_file.writeframes(frames)
            samples_written = chunk_end
            print_progress("GENERATING", samples_written, num_samples)
    
    # Calculate file statistics
    file_size = num_samples * 2 + 44  # 2 bytes per sample + WAV header
    capacity_bits = num_samples * 2  # Each byte can hold 1 bit
    capacity_chars = capacity_bits // 8
    
    stats = {
        'file': output_file,
        'duration': duration,
        'frequency': frequency,
        'sample_rate': sample_rate,
        'samples': num_samples,
        'file_size': file_size,
        'stego_capacity_bits': capacity_bits,
        'stego_capacity_chars': capacity_chars
    }
    
    return stats


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='SONIC-VAULT Tone Generator - Create test WAV files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_tone.py -o cover.wav
  python generate_tone.py -o test.wav -d 10 -f 880
  python generate_tone.py -o long.wav -d 60 -f 440 -r 48000
        """
    )
    
    parser.add_argument('-o', '--output', type=str, default='cover.wav',
                        help='Output WAV file (default: cover.wav)')
    parser.add_argument('-d', '--duration', type=float, default=5.0,
                        help='Duration in seconds (default: 5.0)')
    parser.add_argument('-f', '--frequency', type=float, default=440.0,
                        help='Frequency in Hz (default: 440.0 - A4 note)')
    parser.add_argument('-r', '--rate', type=int, default=44100,
                        help='Sample rate in Hz (default: 44100)')
    parser.add_argument('-a', '--amplitude', type=int, default=16000,
                        help='Amplitude 0-32767 (default: 16000)')
    
    args = parser.parse_args()
    
    print_banner()
    
    try:
        stats = generate_wav(
            output_file=args.output,
            duration=args.duration,
            frequency=args.frequency,
            sample_rate=args.rate,
            amplitude=args.amplitude
        )
        
        print(f"\n{Colors.GREEN}{'═' * 75}{Colors.ENDC}")
        print(f"{Colors.GREEN}[SUCCESS]{Colors.ENDC} WAV file generated successfully!")
        print(f"{Colors.GREEN}{'═' * 75}{Colors.ENDC}")
        print(f"{Colors.CYAN}[FILE]{Colors.ENDC} Output: {Colors.YELLOW}{stats['file']}{Colors.ENDC}")
        print(f"{Colors.CYAN}[SIZE]{Colors.ENDC} File Size: {Colors.YELLOW}{stats['file_size']:,} bytes{Colors.ENDC}")
        print(f"{Colors.CYAN}[HIDE]{Colors.ENDC} Steganography Capacity: {Colors.YELLOW}{stats['stego_capacity_chars']:,} characters{Colors.ENDC}")
        print(f"{Colors.GREEN}{'═' * 75}{Colors.ENDC}")
        
    except Exception as e:
        print(f"\n{Colors.RED}[ERROR]{Colors.ENDC} Failed to generate WAV file: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
