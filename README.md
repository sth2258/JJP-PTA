# JJP-PTA

Repository created for the various scripts supporting JJP PTA initiatives.

- BirthdayBox - obtains a token, queries the GiveBacks API, and uploads orders for Birthday Boxes into a Google Sheet


Notes:
    - Modules utilizing the Google Sheets API are done using a "service account" generated by the Google Developers console with Google Sheets API access. 
    - Service Account credentials are done using a flat-file json key - thus a mount is required for run:
        - `docker build . -t sth2258/jjppta-birthdaybox:v1.3;docker run -it --mount src="$(pwd)/mount",target=/usr/src/app/mount,type=bind sth2258/jjppta-birthdaybox:v1.3`