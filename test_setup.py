"""
Test script to validate the Resume to Portfolio setup
"""
import os
from config import Config
from utils.resume_parser import ResumeParser
from utils.portfolio_generator import PortfolioGenerator

def test_configuration():
    """Test configuration loading"""
    print("Testing configuration...")
    try:
        Config.validate_config()
        print("✓ Configuration is valid")
        print(f"  - GitHub Client ID: {'*' * len(Config.GITHUB_CLIENT_ID)}")
        print(f"  - Perplexity API Key: {'*' * len(Config.PERPLEXITY_API_KEY)}")
        print(f"  - Available themes: {len(Config.COLOR_THEMES)}")
        return True
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        return False

def test_directories():
    """Test required directories"""
    print("\nTesting directories...")
    dirs = [Config.UPLOAD_FOLDER, Config.GENERATED_FOLDER]
    all_exist = True

    for dir_path in dirs:
        if os.path.exists(dir_path):
            print(f"✓ {dir_path} exists")
        else:
            print(f"✗ {dir_path} does not exist")
            all_exist = False

    return all_exist

def test_resume_parser():
    """Test resume parser initialization"""
    print("\nTesting resume parser...")
    try:
        # Test filter methods
        test_text = "Call me at 555-123-4567 or visit 123 Main Street"
        filtered = ResumeParser.filter_personal_data(test_text)

        if "555-123-4567" not in filtered and "123 Main Street" not in filtered:
            print("✓ Resume parser filters personal data correctly")
            return True
        else:
            print("✗ Resume parser did not filter personal data")
            return False
    except Exception as e:
        print(f"✗ Resume parser error: {e}")
        return False

def test_portfolio_generator():
    """Test portfolio generator initialization"""
    print("\nTesting portfolio generator...")
    try:
        generator = PortfolioGenerator(Config.PERPLEXITY_API_KEY)
        print("✓ Portfolio generator initialized")

        # Test HTML validation
        valid_html = "<!DOCTYPE html><html><head></head><body></body></html>"
        invalid_html = "<div>incomplete</div>"

        if generator._validate_html(valid_html) and not generator._validate_html(invalid_html):
            print("✓ HTML validation works correctly")
            return True
        else:
            print("✗ HTML validation not working")
            return False
    except Exception as e:
        print(f"✗ Portfolio generator error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Resume to Portfolio - Setup Validation")
    print("=" * 60)

    tests = [
        test_configuration,
        test_directories,
        test_resume_parser,
        test_portfolio_generator
    ]

    results = [test() for test in tests]

    print("\n" + "=" * 60)
    if all(results):
        print("✓ All tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Run: python app.py")
        print("2. Open: http://localhost:5000")
        print("3. Login with GitHub and start creating portfolios!")
    else:
        print("✗ Some tests failed. Please check the errors above.")
    print("=" * 60)

if __name__ == '__main__':
    main()
