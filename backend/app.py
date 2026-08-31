import os
import re
from urllib.parse import urlparse

from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv


# ==========================================
# CONFIGURATION
# ==========================================

load_dotenv()

app = Flask(__name__)

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": "*"
        }
    }
)

MAX_URL_LENGTH = 2048

INSTAGRAM_HOSTS = {
    "instagram.com",
    "www.instagram.com"
}


# ==========================================
# SECURITY HEADERS
# ==========================================

@app.after_request
def add_security_headers(response):

    response.headers["X-Content-Type-Options"] = "nosniff"

    response.headers["X-Frame-Options"] = "SAMEORIGIN"

    response.headers[
        "Referrer-Policy"
    ] = "strict-origin-when-cross-origin"

    response.headers[
        "Permissions-Policy"
    ] = "camera=(), microphone=(), geolocation=()"

    return response


# ==========================================
# URL VALIDATION
# ==========================================

def is_instagram_url(url):

    try:

        parsed = urlparse(url)

        hostname = (
            parsed.hostname or ""
        ).lower()

        return hostname in INSTAGRAM_HOSTS

    except Exception:

        return False


def validate_instagram_url(url):

    if not url:

        return False, "Instagram URL is required."

    if len(url) > MAX_URL_LENGTH:

        return False, "The URL is too long."

    if not is_instagram_url(url):

        return False, "Only Instagram URLs are supported."

    return True, None


# ==========================================
# CONTENT TYPE DETECTION
# ==========================================

def detect_content_type(url):

    parsed = urlparse(url)

    path = parsed.path.lower().strip("/")


    if path.startswith("reel/"):

        return "reel"


    if path.startswith("reels/"):

        return "reel"


    if path.startswith("stories/"):

        return "story"


    if path.startswith("p/"):

        return "post"


    if path.startswith("tv/"):

        return "video"


    return "unknown"


# ==========================================
# CONTENT ID EXTRACTION
# ==========================================

def extract_content_id(url):

    parsed = urlparse(url)

    path = parsed.path.strip("/")


    patterns = [
        r"^reel/([^/]+)",
        r"^reels/([^/]+)",
        r"^p/([^/]+)",
        r"^tv/([^/]+)",
        r"^stories/([^/]+)"
    ]


    for pattern in patterns:

        match = re.search(
            pattern,
            path,
            re.IGNORECASE
        )

        if match:

            return match.group(1)


    return None


# ==========================================
# NORMALIZED MEDIA RESPONSE
# ==========================================

def normalized_response(
    content_type,
    title=None,
    description=None,
    thumbnail=None,
    media=None
):

    return {

        "success": True,

        "type": content_type,

        "title": title or "Instagram Media",

        "description": description or "",

        "thumbnail": thumbnail,

        "media": media or []

    }


# ==========================================
# PUBLIC CONTENT RETRIEVAL LAYER
# ==========================================

def retrieve_public_media(url):

    """
    This is the retrieval layer.

    It is intentionally designed for publicly
    accessible content only.

    It does not bypass:

    - Instagram login
    - Private accounts
    - Access controls
    - DRM
    - Security mechanisms
    - Rate limits
    """

    content_type = detect_content_type(url)

    content_id = extract_content_id(url)


    if not content_id:

        return {

            "success": False,

            "error":
                "Unable to identify the Instagram content."

        }


    # The actual public-content retrieval provider
    # will be connected here.

    return {

        "success": False,

        "error":
            "The public-content retrieval provider "
            "has not been configured yet.",

        "type": content_type,

        "content_id": content_id

    }


# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/api/health")
def health():

    return jsonify({

        "success": True,

        "service": "InstaFetch API",

        "status": "online",

        "version": "1.0.0"

    })


# ==========================================
# INSTAGRAM API
# ==========================================

@app.post("/api/instagram/fetch")
def fetch_instagram():

    if not request.is_json:

        return jsonify({

            "success": False,

            "error":
                "Request must contain JSON."

        }), 400


    data = request.get_json(
        silent=True
    ) or {}


    url = str(
        data.get("url", "")
    ).strip()


    # Validate URL

    valid, error = validate_instagram_url(url)


    if not valid:

        return jsonify({

            "success": False,

            "error": error

        }), 400


    # Detect content

    content_type = detect_content_type(url)


    # Retrieve content

    result = retrieve_public_media(url)


    # Retrieval failed

    if not result.get("success"):

        return jsonify({

            "success": False,

            "error":
                result.get(
                    "error",
                    "Unable to retrieve media."
                ),

            "type": content_type

        }), 501


    # Successful response

    return jsonify(
        normalized_response(

            content_type=result.get(
                "type",
                content_type
            ),

            title=result.get(
                "title"
            ),

            description=result.get(
                "description"
            ),

            thumbnail=result.get(
                "thumbnail"
            ),

            media=result.get(
                "media",
                []
            )

        )
    )


# ==========================================
# ERROR HANDLERS
# ==========================================

@app.errorhandler(404)
def not_found(error):

    return jsonify({

        "success": False,

        "error":
            "API endpoint not found."

    }), 404


@app.errorhandler(405)
def method_not_allowed(error):

    return jsonify({

        "success": False,

        "error":
            "HTTP method not allowed."

    }), 405


@app.errorhandler(413)
def request_too_large(error):

    return jsonify({

        "success": False,

        "error":
            "Request is too large."

    }), 413


@app.errorhandler(500)
def internal_server_error(error):

    return jsonify({

        "success": False,

        "error":
            "Internal server error."

    }), 500


# ==========================================
# START SERVER
# ==========================================

if __name__ == "__main__":

    port = int(
        os.getenv(
            "PORT",
            "5000"
        )
    )

    debug = (
        os.getenv(
            "FLASK_DEBUG",
            "false"
        ).lower() == "true"
    )


    app.run(

        host="0.0.0.0",

        port=port,

        debug=debug

)
