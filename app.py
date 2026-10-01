import re
from typing import Iterable, Optional

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Example dataset of known Amazon-associated US numbers.
# Replace this with your own trusted source if you need production behavior.
AMAZON_REGISTERED_NUMBERS = {
    "2065550100",
    "4255550199",
    "4155550132",
    "2125550111",
}

# بيانات الكورسات (يمكنك تعديل الأسماء أو الروابط لاحقاً)
COURSES = [
    {
        "id": 1,
        "title": "احتراف إدارة الدومينات والربح منها",
        "description": (
            "دورة شاملة تعلمك كيفية استثمار وبيع أسماء النطاقات التجارية"
            " باحترافية."
        ),
        "price": "$49",
        "checkout_url": (
            "https://your-lemon-squeezy-or-paypal-link.com"  # ضع رابط الدفع الخاص بك هنا
        ),
    },
    {
        "id": 2,
        "title": "استراتيجيات التسويق الرقمي وحركة المرور",
        "description": (
            "دليل عملي لإدارة الحملات الإعلانية وجلب الزيارات المربحة للمواقع"
            " ومتاجر التجارة الإلكترونية."
        ),
        "price": "$29",
        "checkout_url": "https://your-lemon-squeezy-or-paypal-link.com",
    },
]


def normalize_us_phone_number(phone_number: str) -> str:
    """Normalize a US phone number to a standard 10-digit format."""
    if phone_number is None:
        raise ValueError("Phone number is required.")

    digits = re.sub(r"\D+", "", str(phone_number).strip())

    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]

    if len(digits) != 10 or not digits.isdigit():
        raise ValueError("Enter a valid US phone number (10 digits).")

    area_code, exchange, line_number = digits[:3], digits[3:6], digits[6:]
    return f"({area_code}) {exchange}-{line_number}"


def normalize_phone_for_lookup(phone_number: str) -> str:
    """Return the canonical 10-digit number used for comparisons."""
    if phone_number is None:
        return ""

    digits = re.sub(r"\D+", "", str(phone_number).strip())

    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]

    return digits if len(digits) == 10 and digits.isdigit() else ""


def is_valid_us_phone_number(phone_number: str) -> bool:
    try:
        normalize_us_phone_number(phone_number)
        return True
    except ValueError:
        return False


def is_amazon_registered_phone(
    phone_number: str,
    known_registered_numbers: Optional[Iterable[str]] = None,
) -> bool:
    """Check whether a US phone number matches a known Amazon-associated number."""
    lookup_numbers = {
        normalize_phone_for_lookup(number)
        for number in (known_registered_numbers or AMAZON_REGISTERED_NUMBERS)
    }
    normalized = normalize_phone_for_lookup(phone_number)
    return bool(normalized) and normalized in lookup_numbers


def check_amazon_registration(
    phone_number: str,
    known_registered_numbers: Optional[Iterable[str]] = None,
) -> dict:
    """Return a structured result for a phone number lookup."""
    normalized = normalize_phone_for_lookup(phone_number)
    if not normalized:
        return {
            "input": phone_number,
            "is_valid_us_number": False,
            "normalized_number": None,
            "is_registered_with_amazon": False,
            "message": "Please enter a valid US phone number.",
        }

    formatted = normalize_us_phone_number(normalized)
    is_registered = is_amazon_registered_phone(
        normalized,
        known_registered_numbers=known_registered_numbers,
    )

    return {
        "input": str(phone_number),
        "is_valid_us_number": True,
        "normalized_number": formatted,
        "is_registered_with_amazon": is_registered,
        "message": (
            "This phone number is associated with an Amazon account."
            if is_registered
            else "This phone number does not appear to be associated with an Amazon account."
        ),
    }


@app.route("/")
def home():
    return render_template("index.html", courses=COURSES)


@app.route("/api/check-phone", methods=["GET", "POST"])
def check_phone():
    data = request.get_json(silent=True) or {}
    phone_number = request.args.get("phone_number")
    if phone_number is None:
        phone_number = data.get("phone_number")

    if phone_number is None:
        return jsonify({
            "is_valid_us_number": False,
            "normalized_number": None,
            "is_registered_with_amazon": False,
            "message": "Missing phone_number input.",
        }), 400

    return jsonify(check_amazon_registration(phone_number))


if __name__ == "__main__":
    app.run(debug=False)