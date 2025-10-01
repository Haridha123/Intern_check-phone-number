#!/usr/bin/env python3
"""
Batch WhatsApp Number Checker
Reads numbers from .txt files and checks if they're registered on WhatsApp
"""

import sys
import os
import time
from whatsapp.selenium_checker import check_whatsapp_number
from whatsapp.utils import read_numbers_from_file, get_all_number_files, save_results, validate_phone_number

def batch_check_from_file(file_path: str):
    """Check all numbers from a single file"""
    print(f"\n=== Checking numbers from {file_path} ===")
    
    numbers = read_numbers_from_file(file_path)
    if not numbers:
        print("No valid numbers found in file.")
        return {}
    
    results = {}
    driver = None
    
    try:
        # Initialize browser once for all checks using persistent profile
        from whatsapp.selenium_checker import create_persistent_driver, initialize_whatsapp_session
        
        print("🚀 Initializing persistent WhatsApp session...")
        driver = create_persistent_driver()
        
        if not initialize_whatsapp_session(driver):
            print("❌ Failed to initialize WhatsApp session")
            return {}
        
        print("✅ WhatsApp session ready! Starting batch check...")
        
        for i, number in enumerate(numbers, 1):
            validated_number = validate_phone_number(number)
            if not validated_number:
                print(f"[{i}/{len(numbers)}] Skipping invalid number: {number}")
                continue
                
            print(f"\n[{i}/{len(numbers)}] Checking: {validated_number}")
            
            try:
                is_registered = check_whatsapp_number(validated_number, driver)
                results[validated_number] = is_registered
                
                status = "REGISTERED" if is_registered else "NOT REGISTERED"
                print(f"Result: {validated_number} is {status}")
                
                # Small delay between checks
                time.sleep(2)
                
            except Exception as e:
                print(f"Error checking {validated_number}: {e}")
                results[validated_number] = False
    
    except KeyboardInterrupt:
        print("\nStopped by user.")
    except Exception as e:
        print(f"Error during batch checking: {e}")
    finally:
        if driver:
            driver.quit()
    
    return results

def batch_check_all_files():
    """Check numbers from all .txt files in C:/num/"""
    print("=== Batch WhatsApp Number Checker ===")
    
    txt_files = get_all_number_files()
    if not txt_files:
        print("No .txt files found in C:/num/")
        return
    
    print(f"Found {len(txt_files)} file(s) to process:")
    for file in txt_files:
        print(f"  - {os.path.basename(file)}")
    
    choice = input("\nProcess all files? (y/n): ").lower().strip()
    if choice != 'y':
        print("Cancelled.")
        return
    
    all_results = {}
    
    for file_path in txt_files:
        file_results = batch_check_from_file(file_path)
        all_results.update(file_results)
        
        # Save intermediate results
        if file_results:
            filename = os.path.splitext(os.path.basename(file_path))[0]
            intermediate_file = f"C:/num/results_{filename}.txt"
            save_results(file_results, intermediate_file)
    
    # Save final combined results
    if all_results:
        save_results(all_results, "C:/num/final_results.txt")
        print(f"\n=== FINAL SUMMARY ===")
        registered_count = sum(1 for v in all_results.values() if v)
        total_count = len(all_results)
        print(f"Total numbers checked: {total_count}")
        print(f"Registered: {registered_count}")
        print(f"Not registered: {total_count - registered_count}")
        print(f"Results saved to: C:/num/final_results.txt")

def main():
    """Main function"""
    if len(sys.argv) > 1:
        # Check specific file
        file_path = sys.argv[1]
        if not os.path.exists(file_path):
            print(f"Error: File not found: {file_path}")
            return
        
        results = batch_check_from_file(file_path)
        if results:
            # Save results with file-specific name
            filename = os.path.splitext(os.path.basename(file_path))[0]
            output_file = f"C:/num/results_{filename}.txt"
            save_results(results, output_file)
    else:
        # Check all files in directory
        batch_check_all_files()

if __name__ == "__main__":
    main()