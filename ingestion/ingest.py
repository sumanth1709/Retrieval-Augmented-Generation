import pymupdf
import os


# Get the RAG Project folder
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

# Define folders
DATA_FOLDER = os.path.join(
    BASE_DIR,
    "data"
)

OUTPUT_FOLDER = os.path.join(
    BASE_DIR,
    "output"
)


def extract_text_from_pdf(pdf_path):

    document = pymupdf.open(pdf_path)

    full_text = ""

    for page_number, page in enumerate(
        document,
        start=1
    ):

        print(f"Reading page {page_number}")

        text = page.get_text("text")

        full_text += text
        full_text += "\n"

    document.close()

    return full_text


def main():

    # Check whether data folder exists
    if not os.path.exists(DATA_FOLDER):

        print("ERROR: Data folder not found!")
        print("Expected location:")
        print(DATA_FOLDER)

        return

    # Create output folder
    os.makedirs(
        OUTPUT_FOLDER,
        exist_ok=True
    )

    # Find PDFs
    for filename in os.listdir(DATA_FOLDER):

        if filename.lower().endswith(".pdf"):

            pdf_path = os.path.join(
                DATA_FOLDER,
                filename
            )

            print()
            print("==============================")
            print("Processing:", filename)
            print("==============================")

            text = extract_text_from_pdf(
                pdf_path
            )

            # Create TXT filename
            output_filename = (
                os.path.splitext(filename)[0]
                + ".txt"
            )

            output_path = os.path.join(
                OUTPUT_FOLDER,
                output_filename
            )

            # Save extracted text
            with open(
                output_path,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(text)

            print(
                "Saved:",
                output_path
            )


if __name__ == "__main__":
    main()