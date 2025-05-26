import os
import sys
import django

# Set Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# Initialize Django
django.setup()

from engageiq_app.models import EmailMessage

def get_prompt_inputs():
    """
    Retrieves and prints all stored prompt inputs from the EmailMessage table.
    """
    messages = EmailMessage.objects.all().values("id", "prompt_input", "created_at")

    if not messages:
        print("No prompt inputs found in the database.")
        return

    print("\nStored Prompt Inputs:\n")
    for msg in messages:
        print(f"ID: {msg['id']}")
        print(f"Created At: {msg['created_at']}")
        print(f"Prompt Input: {msg['prompt_input']}\n")
        print("=" * 50)

if __name__ == "__main__":
    get_prompt_inputs()
