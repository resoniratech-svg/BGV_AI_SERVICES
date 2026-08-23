import cv2


class ImagePreprocessing:

    @staticmethod
    def preprocess_image(

        image_path
    ):

        image = cv2.imread(
            image_path
        )

        gray = cv2.cvtColor(

            image,

            cv2.COLOR_BGR2GRAY
        )

        threshold = cv2.threshold(

            gray,

            150,

            255,

            cv2.THRESH_BINARY
        )[1]

        cv2.imwrite(

            image_path,

            threshold
        )

        return image_path