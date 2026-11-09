from flask import Flask, render_template, request, redirect, url_for, flash
from detection import detect_blocking
from database import get_owner_by_vehicle
import os
import smtplib
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "your_secret_key"

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ============================================================
# GMAIL SETTINGS
# ============================================================

SENDER_EMAIL = "shashikanth1081@gmail.com"
SENDER_PASSWORD = "mrse yluz hows ioua"


# ============================================================
# SEND EMAIL
# ============================================================

def send_email_persistent(to_email, subject, body, image_path=None):

    try:

        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        from email.mime.base import MIMEBase
        from email import encoders

        msg = MIMEMultipart()

        msg["From"] = SENDER_EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(
            MIMEText(body, "plain")
        )


        # Attach image
        if image_path and os.path.exists(image_path):

            with open(image_path, "rb") as f:

                part = MIMEBase(
                    "application",
                    "octet-stream"
                )

                part.set_payload(
                    f.read()
                )

            encoders.encode_base64(part)

            part.add_header(
                "Content-Disposition",
                f"attachment; filename={os.path.basename(image_path)}"
            )

            msg.attach(part)


        # Connect to Gmail
        smtp_server = smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465
        )

        smtp_server.login(
            SENDER_EMAIL,
            SENDER_PASSWORD
        )

        smtp_server.send_message(msg)

        smtp_server.quit()

        print("Email sent successfully to:", to_email)

        return True


    except Exception as e:

        print("Email sending error:", e)

        return False


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/", methods=["GET"])
def index():

    return render_template(
        "index.html"
    )


# ============================================================
# DETECT PAGE
# ============================================================

@app.route("/detect", methods=["GET", "POST"])
def detect():

    if request.method == "POST":

        # ----------------------------------------------------
        # Get multiple uploaded images
        # ----------------------------------------------------

        files = request.files.getlist("images")


        # Remove empty files
        files = [
            file
            for file in files
            if file and file.filename != ""
        ]


        # ----------------------------------------------------
        # Check if at least one image was selected
        # ----------------------------------------------------

        if not files:

            flash(
                "No image selected.",
                "danger"
            )

            return redirect(
                request.url
            )


        # ----------------------------------------------------
        # Maximum 4 images
        # ----------------------------------------------------

        if len(files) > 4:

            flash(
                "Please upload a maximum of 4 images.",
                "danger"
            )

            return redirect(
                request.url
            )


        # ----------------------------------------------------
        # Process images
        # ----------------------------------------------------

        saved_images = []

        detection_results = []


        for index, file in enumerate(files):

            # Secure filename
            filename = secure_filename(
                file.filename
            )


            # Create unique filename
            name, extension = os.path.splitext(
                filename
            )

            filename = (
                f"vehicle_{index + 1}_{name}{extension}"
            )


            # Full path
            path = os.path.join(
                UPLOAD_FOLDER,
                filename
            )


            # Save image
            file.save(path)


            saved_images.append(
                filename
            )


            # ------------------------------------------------
            # YOLO blockage detection
            # ------------------------------------------------

            print(
                f"Processing image {index + 1}: {filename}"
            )


            result = detect_blocking(
                path
            )


            print(
                f"Image {index + 1} result: {result}"
            )


            detection_results.append(
                result
            )


        # ----------------------------------------------------
        # Combine results
        #
        # If ANY uploaded view shows blockage,
        # overall result is Blocked.
        # ----------------------------------------------------

        status = "Not Blocked"


        for result in detection_results:

            if str(result).lower() == "blocked":

                status = "Blocked"

                break


        # ----------------------------------------------------
        # GPS values
        # ----------------------------------------------------

        latitude = request.form.get(
            "latitude"
        )

        longitude = request.form.get(
            "longitude"
        )


        # ----------------------------------------------------
        # Display first image
        #
        # The existing detect.html expects `image`.
        # ----------------------------------------------------

        first_image = saved_images[0]


        print(
            "================================="
        )

        print(
            "Images uploaded:",
            len(saved_images)
        )

        print(
            "Detection results:",
            detection_results
        )

        print(
            "Final status:",
            status
        )

        print(
            "================================="
        )


        return render_template(
            "detect.html",

            image=first_image,

            images=saved_images,

            status=status,

            detection_results=detection_results,

            latitude=latitude,

            longitude=longitude
        )


    # --------------------------------------------------------
    # GET request
    # --------------------------------------------------------

    return render_template(
        "detect.html"
    )


# ============================================================
# NOTIFY OWNER
# ============================================================

@app.route("/notify", methods=["POST"])
def notify():

    vehicle_number = request.form.get(
        "vehicle_number"
    )


    # --------------------------------------------------------
    # Find vehicle owner in database
    # --------------------------------------------------------

    owner = get_owner_by_vehicle(
        vehicle_number
    )


    # --------------------------------------------------------
    # Image
    # --------------------------------------------------------

    image_name = request.form.get(
        "image_path"
    )


    image_path = (

        os.path.join(
            UPLOAD_FOLDER,
            image_name
        )

        if image_name

        else None
    )


    # --------------------------------------------------------
    # GPS
    # --------------------------------------------------------

    latitude = request.form.get(
        "latitude"
    )

    longitude = request.form.get(
        "longitude"
    )


    # --------------------------------------------------------
    # Owner found
    # --------------------------------------------------------

    if owner:

        # Create Google Maps location link
        if latitude and longitude:

            gps_link = (
                "https://www.google.com/maps"
                f"?q={latitude},{longitude}"
            )

        else:

            gps_link = (
                "Location not available"
            )


        # ----------------------------------------------------
        # Email body
        # ----------------------------------------------------

        body = f"""
Dear {owner['owner']},

Your vehicle ({vehicle_number}) is blocking another vehicle.

Please move your vehicle to unblock the other vehicle.

Location:
{gps_link}

This notification was generated by ParkAssist AI.

Thank you.
"""


        # ----------------------------------------------------
        # Send email
        # ----------------------------------------------------

        email_sent = send_email_persistent(

            owner["email"],

            "🚨 ParkAssist AI - Vehicle Blocking Alert",

            body,

            image_path
        )


        if email_sent:

            flash(
                "Notification sent successfully.",
                "success"
            )

        else:

            flash(
                "Failed to send notification.",
                "danger"
            )


    else:

        flash(
            "Owner not found in database.",
            "danger"
        )


    return redirect(
        url_for("detect")
    )


# ============================================================
# RUN FLASK
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )