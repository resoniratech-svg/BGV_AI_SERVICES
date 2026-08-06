from deepface import DeepFace


def compare_faces(image1_path, image2_path):

    try:
        result = DeepFace.verify(
            img1_path=image1_path, img2_path=image2_path, enforce_detection=False
        )

        return {
            "success": True,
            "matched": result["verified"],
            "distance": float(result["distance"]),
        }

    except Exception as e:
        return {"success": False, "message": str(e)}
