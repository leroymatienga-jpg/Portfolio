"""
Portfolio Flask Application — Main Server
==========================================
Serves the portfolio frontend and provides API endpoints for:
- Contact form submission (with validation, rate limiting, DB storage, email notification)
- CV file download
- Admin endpoint to view all messages
"""

import os
import re
import html
from flask import Flask, request, jsonify, send_from_directory, send_file, abort
from flask_cors import CORS
from config import Config
from models import init_db, save_message, get_all_messages, count_recent_messages
from email_service import send_notification

# ─── App Initialization ───────────────────────────────────────────────
app = Flask(__name__, static_folder=".", static_url_path="")
app.secret_key = Config.SECRET_KEY
CORS(app)

# Initialize the database on startup
init_db()


# ─── Helper Functions ─────────────────────────────────────────────────

def sanitize_input(text):
    """Sanitize user input to prevent XSS attacks."""
    if not text:
        return ""
    return html.escape(text.strip())


def is_valid_email(email):
    """Validate email format using regex."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def get_client_ip():
    """Get the real client IP, accounting for proxies."""
    if request.headers.get("X-Forwarded-For"):
        return request.headers.get("X-Forwarded-For").split(",")[0].strip()
    return request.remote_addr


# ─── Static File Routes ──────────────────────────────────────────────

@app.route("/")
def serve_index():
    """Serve the main portfolio HTML page."""
    return send_from_directory(".", "index.html")


@app.route("/<path:filename>")
def serve_static(filename):
    """Serve static files (CSS, JS, images) from the project root."""
    # Security: prevent directory traversal
    if ".." in filename:
        abort(403)
    return send_from_directory(".", filename)


# ─── API: Contact Form ───────────────────────────────────────────────

@app.route("/api/contact", methods=["POST"])
def handle_contact():
    """
    Handle contact form submissions.

    Expects JSON body:
        { "name": str, "email": str, "subject": str, "message": str }

    Returns:
        201: Message saved successfully
        400: Validation error
        429: Rate limit exceeded
        500: Server error
    """
    # Rate limiting check
    client_ip = get_client_ip()
    recent_count = count_recent_messages(client_ip, Config.RATE_LIMIT_WINDOW_SECONDS)
    if recent_count >= Config.RATE_LIMIT_MAX_REQUESTS:
        return jsonify({
            "success": False,
            "error": "Too many messages. Please try again later."
        }), 429

    # Parse request data
    data = request.get_json()
    if not data:
        return jsonify({
            "success": False,
            "error": "Invalid request. Please send JSON data."
        }), 400

    # Extract and sanitize fields
    name = sanitize_input(data.get("name", ""))
    email = sanitize_input(data.get("email", ""))
    subject = sanitize_input(data.get("subject", ""))
    message = sanitize_input(data.get("message", ""))

    # Validation
    errors = []
    if not name or len(name) < 2:
        errors.append("Name is required (minimum 2 characters).")
    if not email:
        errors.append("Email is required.")
    elif not is_valid_email(email):
        errors.append("Please provide a valid email address.")
    if not subject or len(subject) < 2:
        errors.append("Subject is required (minimum 2 characters).")
    if not message or len(message) < 10:
        errors.append("Message is required (minimum 10 characters).")
    if len(name) > 100:
        errors.append("Name is too long (max 100 characters).")
    if len(subject) > 200:
        errors.append("Subject is too long (max 200 characters).")
    if len(message) > 5000:
        errors.append("Message is too long (max 5000 characters).")

    if errors:
        return jsonify({
            "success": False,
            "error": errors[0],
            "errors": errors
        }), 400

    # Save to database
    saved = save_message(name, email, subject, message, ip_address=client_ip)
    if not saved:
        return jsonify({
            "success": False,
            "error": "Failed to save your message. Please try again."
        }), 500

    # Send email notification (non-blocking — won't fail the request)
    email_sent = send_notification(name, email, subject, message)

    return jsonify({
        "success": True,
        "message": "Your message has been sent successfully!",
        "email_notified": email_sent
    }), 201


# ─── API: CV Download ────────────────────────────────────────────────

@app.route("/api/download-cv", methods=["GET"])
def download_cv():
    """
    Serve the CV file for download.
    Looks for the CV file in the project root directory.
    """
    cv_path = os.path.join(os.path.dirname(__file__), Config.CV_FILENAME)

    if not os.path.exists(cv_path):
        return jsonify({
            "success": False,
            "error": "CV file not found. Please check back later."
        }), 404

    return send_file(
        cv_path,
        as_attachment=True,
        download_name=Config.CV_FILENAME
    )


# ─── API: Admin — View Messages ──────────────────────────────────────

@app.route("/api/messages", methods=["GET"])
def get_messages():
    """
    Retrieve all contact messages (admin-only).
    Requires X-API-Key header matching ADMIN_API_KEY from .env.
    """
    api_key = request.headers.get("X-API-Key", "")

    if api_key != Config.ADMIN_API_KEY:
        return jsonify({
            "success": False,
            "error": "Unauthorized. Invalid API key."
        }), 401

    messages = get_all_messages()

    return jsonify({
        "success": True,
        "count": len(messages),
        "messages": messages
    }), 200


# ─── Error Handlers ──────────────────────────────────────────────────

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return jsonify({"success": False, "error": "Resource not found."}), 404


@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors."""
    return jsonify({"success": False, "error": "Internal server error."}), 500


# ─── Run the Server ──────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"""
    ==============================================
      Leroy Matienga Portfolio Server
      Running on http://localhost:{port}
    ==============================================
    """)
    app.run(host="0.0.0.0", port=port, debug=Config.DEBUG)
