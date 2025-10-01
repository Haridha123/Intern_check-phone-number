
import os
from django.core.management.base import BaseCommand
from whatsapp.selenium_checker import check_whatsapp_number, create_persistent_driver, initialize_whatsapp_session
from whatsapp.utils import read_numbers_from_file, get_all_number_files, save_results, validate_phone_number


class Command(BaseCommand):

    help = 'Check if a phone number or numbers in a file are registered on WhatsApp (without sending messages)'

    def add_arguments(self, parser):
        parser.add_argument('--number', type=str, help='Phone number in international format (e.g., +1234567890)')
        parser.add_argument('--file', type=str, help='Path to .txt file with numbers (default: all .txt in C:/num/)')

    def handle(self, *args, **options):
        number = options.get('number')
        file_path = options.get('file')

        if number:
            self.stdout.write(f'Checking WhatsApp registration for: {number}')
            driver = create_persistent_driver()
            try:
                if not initialize_whatsapp_session(driver):
                    self.stdout.write(self.style.ERROR('Failed to initialize WhatsApp session.'))
                    return
                result = check_whatsapp_number(number, driver)
                if result:
                    self.stdout.write(self.style.SUCCESS(f'{number} is registered on WhatsApp.'))
                else:
                    self.stdout.write(self.style.WARNING(f'{number} is NOT registered on WhatsApp.'))
            finally:
                driver.quit()
            return

        # Batch mode
        if file_path:
            files = [file_path]
        else:
            files = get_all_number_files()
            if not files:
                self.stdout.write(self.style.ERROR('No .txt files found in C:/num/'))
                return

        driver = create_persistent_driver()
        try:
            if not initialize_whatsapp_session(driver):
                self.stdout.write(self.style.ERROR('Failed to initialize WhatsApp session.'))
                return
            for file in files:
                self.stdout.write(f'Checking numbers from: {file}')
                numbers = read_numbers_from_file(file)
                results = {}
                for n in numbers:
                    valid = validate_phone_number(n)
                    if not valid:
                        self.stdout.write(self.style.WARNING(f'Skipping invalid number: {n}'))
                        continue
                    is_registered = check_whatsapp_number(valid, driver)
                    results[valid] = is_registered
                    status = 'REGISTERED' if is_registered else 'NOT REGISTERED'
                    self.stdout.write(f'{valid}: {status}')
                # Save results for this file
                out_file = f'C:/num/results_{os.path.splitext(os.path.basename(file))[0]}.txt'
                save_results(results, out_file)
                self.stdout.write(self.style.SUCCESS(f'Results saved to: {out_file}'))
        finally:
            driver.quit()
