from flask import Flask, render_template

app = Flask(__name__)

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


@app.route("/")
def home():
  return render_template("index.html", courses=COURSES)


if __name__ == "__main__":
  app.run(debug=True)