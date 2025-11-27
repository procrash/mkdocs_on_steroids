"""
Test n8n webhook connectivity without processing documents.
"""

import sys
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv('.env.windows')
load_dotenv('.env')

def test_n8n_connection():
    """Test connectivity to n8n webhook."""
    webhook_url = os.getenv('N8N_WEBHOOK_URL', 'http://192.168.0.72:5678/webhook/upload_data')

    print("\n" + "="*80)
    print("  Testing n8n Webhook Connection")
    print("="*80 + "\n")

    print(f"Webhook URL: {webhook_url}\n")

    # Create a minimal test payload
    test_payload = {
        'file_name': 'test.txt',
        'file_path': 'Z:\\mkdocs\\test.txt',
        'file_type': '.txt',
        'total_chunks': 1,
        'chunks': ['This is a test chunk to verify n8n connectivity.'],
        'metadata': {'test': True}
    }

    try:
        print("[1/2] Sending test request to n8n...")
        response = requests.post(
            webhook_url,
            json=test_payload,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )

        print(f"      Status Code: {response.status_code}")

        if response.status_code == 200:
            print("      [OK] Connection successful!\n")

            print("[2/2] Response from n8n:")
            try:
                response_data = response.json()
                print(f"      {response_data}\n")
            except:
                print(f"      {response.text[:200]}\n")

            print("="*80)
            print("  SUCCESS: n8n webhook is accessible!")
            print("="*80)
            print("\nYou can now use:")
            print("  - test_upload.bat to upload sample files")
            print("  - upload_document.bat to upload your documents")
            print("\n" + "="*80 + "\n")
            return 0
        else:
            print(f"      [WARNING] Unexpected status code: {response.status_code}\n")
            print(f"Response: {response.text[:500]}\n")
            print("="*80)
            print("  n8n responded but with unexpected status code")
            print("="*80)
            print("\nPlease check:")
            print("  1. Is your n8n workflow configured correctly?")
            print("  2. Does the webhook expect a different data format?")
            print("\n" + "="*80 + "\n")
            return 1

    except requests.exceptions.ConnectionError as e:
        print(f"      [ERROR] Connection failed!\n")
        print("="*80)
        print("  FAILED: Cannot connect to n8n")
        print("="*80)
        print(f"\nError: {e}\n")
        print("Please check:")
        print(f"  1. Is n8n running at {webhook_url}?")
        print("  2. Can you ping 192.168.0.72?")
        print("  3. Is there a firewall blocking the connection?")
        print("  4. Is the webhook URL correct in .env?\n")
        print("="*80 + "\n")
        return 1

    except requests.exceptions.Timeout:
        print(f"      [ERROR] Request timed out!\n")
        print("="*80)
        print("  FAILED: Request timed out")
        print("="*80)
        print("\nThe server is taking too long to respond.")
        print("Please check if n8n is running properly.\n")
        print("="*80 + "\n")
        return 1

    except Exception as e:
        print(f"      [ERROR] Unexpected error!\n")
        print("="*80)
        print("  FAILED: Unexpected error")
        print("="*80)
        print(f"\nError: {e}\n")
        print("="*80 + "\n")
        return 1

if __name__ == '__main__':
    sys.exit(test_n8n_connection())
