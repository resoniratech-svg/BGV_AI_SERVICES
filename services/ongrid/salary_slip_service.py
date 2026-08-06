import json

from services.ongrid.ongrid_client import (
    OnGridClient
)


class SalarySlipService:

    @staticmethod
    def salary_slip_ocr(

            base64_data

    ):

        ####################################################
        # GRIDLINES PAYLOAD
        ####################################################

        payload = {

            "base64_data": base64_data,

            "consent": "Y"

        }

        print("=" * 80)
        print("SALARY SLIP OCR REQUEST")
        print(json.dumps(payload, indent=4))
        print("=" * 80)

        ####################################################
        # GRIDLINES API
        ####################################################

        response = (

            OnGridClient.post(

                "/bank-api/salary-slip/ocr",

                payload

            )

        )

        print("=" * 80)
        print("SALARY SLIP OCR RESPONSE")
        print(json.dumps(response, indent=4))
        print("=" * 80)

        ####################################################
        # EMPTY RESPONSE
        ####################################################

        if not response:

            raise Exception(

                "Empty response received from Gridlines Salary Slip OCR API."

            )

        ####################################################
        # GRIDLINES FAILURE
        ####################################################

        if response.get("success") is False:

            status = response.get("status")

            raw_response = response.get("raw_response")

            if status == 429:

                raise Exception(

                    "Gridlines API rate limit exceeded. Please try again later."

                )

            if status == 403:

                raise Exception(

                    "Gridlines API access forbidden. Please verify API credentials."

                )

            if status == 400:

                raise Exception(

                    f"Invalid Salary Slip. Gridlines Response: {raw_response}"

                )

            if status == 404:

                raise Exception(

                    f"Gridlines endpoint not found. Response: {raw_response}"

                )

            raise Exception(

                f"Gridlines Salary Slip OCR failed. Status: {status}. Response: {raw_response}"

            )

        ####################################################
        # VALIDATE RESPONSE
        ####################################################

        if response.get("status") != 200:

            raise Exception(

                f"Unexpected Gridlines response status: {response.get('status')}"

            )

        ####################################################
        # SUCCESS
        ####################################################

        return response