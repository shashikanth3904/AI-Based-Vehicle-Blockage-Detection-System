# AI-Based Vehicle Blockage Detection & Notification
# 🚗 ParkAssist AI 

**Detect. Alert. Unblock.**

ParkAssist AI is a web-based vehicle blockage detection and notification system developed using Python, Flask, and YOLOv8. It helps users identify potential vehicle blockage from uploaded images and notify the owner of the blocking vehicle through email.

The system combines computer vision, spatial analysis, a vehicle-owner database, browser-based geolocation, and automated email notifications in one web application.

## 📌 Table of Contents

- [Overview](#-overview)
- [Problem Statement](#-problem-statement)
- [Objectives](#-objectives)
- [Features](#-features)
- [System Workflow](#-system-workflow)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Installation and Setup](#-installation-and-setup)
- [Email Configuration](#-email-configuration)
- [Database Setup](#-database-setup)
- [How to Run](#-how-to-run)
- [Limitations](#-limitations)
- [Future Enhancements](#-future-enhancements)
- [Privacy and Security](#-privacy-and-security)
- [Conclusion](#-conclusion)

## 📖 Overview

Vehicle blockage is a common problem in parking areas, residential communities, colleges, apartments, and other locations. A parked vehicle may prevent another vehicle from moving freely, and identifying and contacting the responsible owner can be inconvenient.

ParkAssist AI provides a prototype solution by allowing users to upload or capture vehicle images through a web interface. The system uses YOLOv8-based vehicle detection and blockage-analysis logic to evaluate the scene. When a blockage is identified, the user can enter the blocking vehicle's registration number to retrieve its owner information from a database.

The system can then send an email notification containing blockage information, an evidence image, and a Google Maps location link when location access is available.

## 🎯 Problem Statement

To develop a web-based system that uses computer vision to analyze user-provided vehicle images, identify potential vehicle blockage, retrieve the blocking vehicle owner's contact information, and send an automated email notification with location details.

## 🎯 Objectives

- Detect vehicles in user-uploaded images.
- Analyze the spatial relationship between vehicles to identify possible obstruction.
- Support single-image uploads and up to four images for multi-view analysis.
- Retrieve owner details using a manually entered vehicle registration number.
- Obtain location coordinates through the browser's Geolocation API, with user permission.
- Generate a Google Maps link from the available coordinates.
- Send email notifications through Gmail SMTP.

## ✨ Features

### 1. Vehicle Detection
Uses a YOLOv8 segmentation model to detect vehicles in uploaded images.

### 2. Vehicle Blockage Analysis
Analyzes detected vehicle positions using the project's blockage-detection logic to classify the scene as blocked or not blocked.

### 3. Multi-Image Upload
Supports uploading one image or up to four images for multi-view analysis. This does not represent true 360-degree reconstruction.

### 4. Vehicle Owner Lookup
Uses SQLite to store and retrieve vehicle registration numbers, owner names, and email addresses.

### 5. GPS Location
Requests location access through the browser and uses available latitude and longitude coordinates to generate a Google Maps link.

### 6. Email Notifications
Uses Gmail SMTP to send an email to the registered owner, including the blockage message, location link, and an evidence image when available.

### 7. Web Interface
Provides a browser-based interface for image uploads, analysis, and notification workflows.

## 🔄 System Workflow

1. The user opens the ParkAssist AI website.
2. The user uploads one or more vehicle images.
3. The Flask application receives and saves the images.
4. YOLOv8 detects vehicles in the images.
5. The blockage-analysis module evaluates the detected vehicle positions.
6. The system displays the detection result.
7. The user enters the blocking vehicle's registration number.
8. The application retrieves the corresponding owner details from SQLite.
9. The browser provides location coordinates if the user grants permission.
10. The application generates a Google Maps location link.
11. Gmail SMTP sends the notification email to the registered owner.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Flask | Backend web framework |
| YOLOv8 Segmentation | Vehicle detection |
| OpenCV | Computer vision and image processing support |
| HTML | Web page structure |
| CSS | Styling and layout |
| JavaScript | Browser-side interactions and geolocation |
| Bootstrap | Responsive interface components, where used |
| SQLite | Vehicle-owner database |
| Gmail SMTP | Email notifications |
| Google Maps | Location link |
| Visual Studio Code | Development environment |

## 📁 Project Structure

```text
AI-based-vehicle-blockage-detection/
│
├── app.py                  # Flask application and routes
├── database.py             # Database access functions
├── detection.py            # Vehicle detection and blockage logic
├── vehicles.py             # Vehicle-related functionality
├── vehicles.db             # SQLite database (created locally)
├── yolov8n-seg.pt          # YOLOv8 segmentation model weights
├── requirements.txt        # Python dependencies
│
├── templates/
│   ├── index.html          # Home page
│   └── detect.html         # Image upload and detection page
│
├── static/
│   └── uploads/            # Uploaded and processed images
│
└── README.md               # Project documentation
```

*Note: The exact contents of folders may vary depending on your current implementation.*

## ⚙️ Installation and Setup

### Prerequisites

Install the following:

- Python 3.10 or another version compatible with the installed dependencies.
- Visual Studio Code.
- Git (optional, for cloning the repository).
- A Gmail account for email notifications.

### Step 1: Clone the Repository

```bash
git clone https://github.com/Shailesh280/AI-based-vehicle-blockage-detection.git
```

Open the downloaded project folder in VS Code.

### Step 2: Create a Virtual Environment

Open the VS Code terminal inside the project folder and run:

```bash
python -m venv venv
```

### Step 3: Activate the Virtual Environment

**Windows Command Prompt:**

```bat
venv\Scripts\activate.bat
```

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt or follow the Python environment activation guidance for your system.

### Step 4: Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 5: Configure Email Credentials

Configure the sender's Gmail address and Google App Password securely before starting the application. See [Email Configuration](#-email-configuration).

### Step 6: Initialize the Database

Make sure the SQLite database has the required `vehicles` table and columns expected by `database.py`.

See [Database Setup](#-database-setup).

## 📧 Email Configuration

ParkAssist AI uses Gmail SMTP to send notifications.

SMTP settings:

- **SMTP server:** `smtp.gmail.com`
- **Port:** `465`
- **Security:** SSL

For Gmail authentication, enable 2-Step Verification and generate an App Password from your Google Account.

Google's official guide: https://support.google.com/mail/answer/185833

**Security recommendations:**

- Do not publish your Gmail password or App Password.
- Do not commit credentials to GitHub.
- Prefer environment variables or a local `.env` file for secrets.
- Add `.env`, `venv/`, and other local-only files to `.gitignore`.
- If an App Password has been exposed, revoke it and generate a replacement.

## 🗄️ Database Setup

The application uses SQLite to associate a vehicle registration number with its owner details.

The database contains these logical fields:

| Field | Description |
|---|---|
| `number` | Vehicle registration number |
| `owner_name` | Owner's name |
| `email` | Owner's email address |

**Important:** The actual table and column names must match the queries in your `database.py` file. Your current code may use `owner` rather than `owner_name` for the owner-name column or returned dictionary key.

For testing, use fictional vehicle registration numbers and test email addresses. Do not add real vehicle owners' private information without permission.

## ▶️ How to Run

Activate the virtual environment, ensure dependencies and email settings are configured, and run:

```bash
python app.py
```

Open the local website in your browser:

http://127.0.0.1:5000

Then:

1. Open the detection page.
2. Upload one image or up to four images.
3. Run the detection process.
4. Review the blockage result.
5. Enter the blocking vehicle's registration number when prompted.
6. Allow location access if you want to include the location.
7. Submit the notification and check the configured recipient's inbox.

Keep the terminal running while using the application.

## ⚠️ Limitations

- The current prototype analyzes images supplied by the user; it does not require or directly access CCTV.
- The number plate is entered manually. Automatic number-plate recognition/OCR is not currently implemented.
- Multi-image support provides multi-view analysis, not true 360-degree reconstruction.
- Blockage classification depends on the current detection and spatial-analysis logic and may not work reliably in every parking arrangement.
- The database may contain test entries rather than a verified real-world vehicle-owner registry.
- Location information depends on browser permission and device availability.
- Prototype testing with a small collection of images does not establish production-level accuracy.
- Email delivery depends on valid credentials, network access, and the recipient's email service.

## 🚀 Future Enhancements

- Integrate automatic number-plate detection and OCR.
- Improve blockage classification using a larger, labelled dataset.
- Add confidence scores and detailed evaluation metrics.
- Support more complex parking layouts and multiple blocking vehicles.
- Add SMS, push notifications, or other communication options.
- Develop a mobile application.
- Explore real-time camera integration where authorized.
- Add secure authentication and access controls.
- Deploy the application to a cloud platform.
- Improve logging, error handling, and notification status tracking.

## 🔒 Privacy and Security

- Use only images that you have permission to process.
- Use synthetic owner data for demonstrations and testing.
- Obtain consent before storing or sharing personal information.
- Protect SMTP credentials using environment variables or a secrets manager.
- Do not upload `.env`, App Passwords, database files containing private information, or unnecessary personal images to a public repository.
- Run Flask's debug mode only during local development; disable it before deployment.

## ✅ Conclusion

ParkAssist AI demonstrates a prototype approach to vehicle blockage detection and owner notification by combining computer vision, a Flask web application, SQLite database access, browser geolocation, and email communication.

The project illustrates how AI and web technologies can be combined to address a practical parking-related problem. Further improvements to blockage classification, automatic number-plate recognition, security, and testing can help move the prototype toward a more robust application.

---

**Project:** ParkAssist AI  
**Tagline:** Detect. Alert. Unblock.  
**Domain:** Artificial Intelligence, Computer Vision, and Web Development  
**Developed as:** B.Tech AI & Data Science Mini Project
