class CandidateProfileBuilder:

    @staticmethod
    def build(parsed_data):

        data = parsed_data.get(
            "ResumeParserData",
            {}
        )

        address = {}

        if data.get("Address"):

            address = data.get(
                "Address"
            )[0]

        email = None

        if data.get("Email"):

            if isinstance(
                data["Email"],
                list
            ):

                email = data["Email"][0].get(
                    "EmailAddress"
                )

            else:

                email = data.get("Email")

        phone = None

        if data.get("Mobile"):

            if isinstance(
                data["Mobile"],
                list
            ):

                phone = data["Mobile"][0].get(
                    "Number"
                )

            else:

                phone = data.get("Mobile")

        linkedin = None

        if data.get("WebSite"):

            websites = data.get(
                "WebSite"
            )

            if isinstance(
                websites,
                list
            ):

                for site in websites:

                    url = site.get(
                        "Url",
                        ""
                    )

                    if "linkedin" in url.lower():

                        linkedin = url

        skills = []

        if data.get("SkillKeywords"):

            if isinstance(
                data["SkillKeywords"],
                str
            ):

                skills = data[
                    "SkillKeywords"
                ].split(",")

            else:

                skills = data[
                    "SkillKeywords"
                ]

        candidate = {

            "full_name": data.get(
                "Name"
            ),

            "email": email,

            "phone": phone,

            "city": address.get(
                "City"
            ),

            "state": address.get(
                "State"
            ),

            "country": address.get(
                "Country"
            ),

            "skills": ",".join(skills),

            "experience_years": data.get(
                "ExperienceInYears"
            ),

            "current_company": data.get(
                "CurrentEmployer"
            ),

            "designation": data.get(
                "JobProfile"
            ),

            "linkedin": linkedin
        }

        return candidate