import os
import time
from dotenv import load_dotenv
from google import genai


# ==========================================
# 1. LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()


# ==========================================
# 2. GET GEMINI API KEY
# ==========================================

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found. "
        "Please add it to the .env file."
    )


# ==========================================
# 3. CREATE GEMINI CLIENT
# ==========================================

client = genai.Client(
    api_key=api_key
)


# ==========================================
# 4. GENERATE ANSWER
# ==========================================

def generate_answer(question, context):

    prompt = f"""
You are a helpful assistant answering questions
using the provided context.

Use only the information given in the context.

If the answer is not present in the context,
say:

"I could not find the answer in the provided documents."

Do not make up information.

Context:
--------------------
{context}
--------------------

Question:
{question}

Answer:
"""

    try:

        print("\nCalling Gemini...")

        interaction = client.interactions.create(
            model="gemini-3.8-flash",
            input=prompt
        )

        return interaction.output_text

    except Exception as e:

        error_message = str(e)

        if "429" in error_message:
            print()
            print("=" * 60)
            print("GEMINI FREE TIER LIMIT REACHED")
            print("=" * 60)
            print()
            print(
                "The Gemini API daily request limit has been reached."
            )
            print(
                "Please wait for the limit to reset or use another"
                " available Gemini model/tier."
            )

        elif "503" in error_message:

            print()
            print(
                "Gemini is temporarily unavailable."
            )

        else:

            print()
            print("Gemini API error:")
            print(error_message)

        return None


# ==========================================
# 5. TEST THE LLM
# ==========================================

def main():

    print("=" * 60)
    print("              GEMINI LLM TEST")
    print("=" * 60)

    question = input(
        "\nEnter a question: "
    ).strip()

    # --------------------------------------
    # Temporary test context
    # --------------------------------------

    context = """
The CIA triad consists of three fundamental principles:
Confidentiality, Integrity, and Availability.

Confidentiality means protecting information from
unauthorized access.

Integrity means maintaining the accuracy and
consistency of information.

Availability means ensuring that authorized users
can access information when needed.
"""

    print("\nGenerating answer...")

    answer = generate_answer(
        question,
        context
    )

    print("\n" + "=" * 60)
    print("ANSWER")
    print("=" * 60)

    if answer:

        print(answer)

    else:

        print(
            "Could not generate an answer because "
            "the Gemini service is currently unavailable."
        )


# ==========================================
# 6. RUN PROGRAM
# ==========================================

if __name__ == "__main__":
    main()