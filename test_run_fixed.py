from checker.whatsapp_checker import check_whatsapp_number

def test_single_number():
    """Test a single number with WhatsApp checker"""
    number = "+919943899583"  # Replace with a real number you want to check
    
    print("🚀 Starting WhatsApp number check...")
    
    try:
        # Check the number (driver will be created automatically)
        print(f"📞 Checking number: {number}")
        result = check_whatsapp_number(number)
        print(f"✅ Result: {number} is {'registered' if result else 'NOT registered'} on WhatsApp.")
        
    except Exception as e:
        print(f"❌ Error occurred: {e}")


if __name__ == "__main__":
    test_single_number()