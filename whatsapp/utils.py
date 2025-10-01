"""
Utility functions for WhatsApp number checking
"""
import os
from typing import List, Optional

def read_numbers_from_file(file_path: str) -> List[str]:
    """
    Read phone numbers from a text file.
    
    Args:
        file_path (str): Path to the text file containing phone numbers
        
    Returns:
        List[str]: List of phone numbers
    """
    numbers = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                number = line.strip()
                if number and not number.startswith('#'):  # Skip empty lines and comments
                    # Ensure number starts with +
                    if not number.startswith('+'):
                        number = '+' + number
                    numbers.append(number)
        print(f"[INFO] Read {len(numbers)} numbers from {file_path}")
    except FileNotFoundError:
        print(f"[ERROR] File not found: {file_path}")
    except Exception as e:
        print(f"[ERROR] Error reading file {file_path}: {e}")
    
    return numbers

def get_all_number_files(directory: str = "C:/num") -> List[str]:
    """
    Get all .txt files in the specified directory.
    
    Args:
        directory (str): Directory to search for .txt files
        
    Returns:
        List[str]: List of .txt file paths
    """
    txt_files = []
    try:
        for file in os.listdir(directory):
            if file.endswith('.txt'):
                txt_files.append(os.path.join(directory, file))
        print(f"[INFO] Found {len(txt_files)} .txt files in {directory}")
    except Exception as e:
        print(f"[ERROR] Error listing files in {directory}: {e}")
    
    return txt_files

def save_results(results: dict, output_file: str = "C:/num/results.txt") -> None:
    """
    Save checking results to a file.
    
    Args:
        results (dict): Dictionary with numbers as keys and True/False as values
        output_file (str): Path to output file
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write("WhatsApp Number Check Results\n")
            file.write("=" * 40 + "\n\n")
            
            registered = []
            not_registered = []
            
            for number, is_registered in results.items():
                if is_registered:
                    registered.append(number)
                else:
                    not_registered.append(number)
            
            file.write(f"REGISTERED NUMBERS ({len(registered)}):\n")
            file.write("-" * 30 + "\n")
            for number in registered:
                file.write(f"✓ {number}\n")
            
            file.write(f"\nNOT REGISTERED NUMBERS ({len(not_registered)}):\n")
            file.write("-" * 30 + "\n")
            for number in not_registered:
                file.write(f"✗ {number}\n")
            
            file.write(f"\nSUMMARY:\n")
            file.write(f"Total checked: {len(results)}\n")
            file.write(f"Registered: {len(registered)}\n")
            file.write(f"Not registered: {len(not_registered)}\n")
        
        print(f"[INFO] Results saved to {output_file}")
    except Exception as e:
        print(f"[ERROR] Error saving results to {output_file}: {e}")

def validate_phone_number(number: str) -> Optional[str]:
    """
    Validate and format phone number.
    
    Args:
        number (str): Phone number to validate
        
    Returns:
        Optional[str]: Formatted number or None if invalid
    """
    if not number:
        return None
    
    # Remove all non-digit characters except +
    cleaned = ''.join(c for c in number if c.isdigit() or c == '+')
    
    # Must start with + and have at least 10 digits
    if not cleaned.startswith('+'):
        cleaned = '+' + cleaned
    
    # Remove + for digit counting
    digits_only = cleaned[1:]
    
    if len(digits_only) < 10 or len(digits_only) > 15:
        print(f"[WARNING] Invalid number length: {number}")
        return None
    
    return cleaned
