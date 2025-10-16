import openai

# Display version
print("📦 Checking OpenAI package version...\n")

version = openai.__version__
print(f"✅ Installed OpenAI version: {version}")

# Check if it's new or old
from packaging import version as v

if v.parse(version) < v.parse("1.0.0"):
    print("\n⚠️ You are using an OLD version of OpenAI!")
    print("👉 Please upgrade by running:")
    print("   pip install --upgrade openai")
    print("\nAfter upgrading, restart your program.")
else:
    print("\n🎉 You are using the latest OpenAI SDK!")
    print("✅ You can safely use: from openai import OpenAI")
