import cv2
import pytesseract


def extract_text_from_image(image_path):

    image = cv2.imread(image_path)

    if image is None:
        raise Exception(
            f"Unable to read image: {image_path}"
        )

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    gray = cv2.GaussianBlur(
        gray,
        (3, 3),
        0
    )

    gray = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]
    cv2.imwrite(
        "debug_preprocessed.png",
        gray
)

    text = pytesseract.image_to_string(
        gray,
        lang="eng",
        config="--oem 3 --psm 11"
    )

    print("\n===== OCR OUTPUT =====\n")
    print(text)
    print("\n======================\n")

    return text