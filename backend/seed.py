"""
Seed the database with initial data:
  - 1 admin user
  - 4 language education content sets (tips + quizzes)
Run: python seed.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.core.database import SessionLocal, init_db
from app.core.security import hash_password
from app.models.models import User, EducationContent

init_db()
db = SessionLocal()

# ── Admin user ──
admin_email = "admin@phishing-detector.com"
if not db.query(User).filter(User.email == admin_email).first():
    admin = User(
        email=admin_email,
        password_hash=hash_password("admin123"),
        name="System Admin",
        preferred_language="en",
        role="admin",
    )
    db.add(admin)
    print(f"[+] Admin created: {admin_email} / admin123")

# ── Demo user ──
demo_email = "demo@example.com"
if not db.query(User).filter(User.email == demo_email).first():
    demo = User(
        email=demo_email,
        password_hash=hash_password("demo123"),
        name="Demo User",
        preferred_language="en",
        role="user",
    )
    db.add(demo)
    print(f"[+] Demo user created: {demo_email} / demo123")

# ── Education content ──
contents = [
    # ── English Tips ──
    {
        "title": "How to Spot a Phishing Email",
        "content_type": "tip",
        "language": "en",
        "difficulty_level": "beginner",
        "content": {
            "body": """Phishing emails often have these red flags:

1. **Urgent language** — "Your account will be closed in 24 hours!"
2. **Generic greetings** — "Dear Customer" instead of your name
3. **Suspicious links** — Hover over links to see the real URL
4. **Grammar mistakes** — Professional companies proofread their emails
5. **Unexpected attachments** — Never open attachments from unknown senders
6. **Requests for personal info** — Legitimate companies never ask for passwords via email

**Golden rule:** When in doubt, go directly to the website by typing the URL yourself.""",
        },
    },
    {
        "title": "Visa & Immigration Scam Warning Signs",
        "content_type": "tip",
        "language": "en",
        "difficulty_level": "beginner",
        "content": {
            "body": """Scammers target immigrants and international students with fake visa threats:

**Common tactics:**
- "Your visa has been cancelled. Click here to reinstate."
- "Immigration officers will come to your address unless you pay a fine."
- "Your work permit is under review. Verify your identity now."

**How to protect yourself:**
1. Government agencies NEVER ask for payment via text message or email
2. Always verify through official government websites
3. Never share passport or visa details via messaging apps
4. Report suspicious messages to your local immigration office

**Remember:** Real immigration issues are communicated through official postal mail or verified phone calls.""",
        },
    },
    # ── Chinese Tips ──
    {
        "title": "如何识别钓鱼邮件",
        "content_type": "tip",
        "language": "zh",
        "difficulty_level": "beginner",
        "content": {
            "body": """钓鱼邮件通常有以下特征：

1. **紧急措辞** — "您的账户将在24小时内被关闭！"
2. **通用称呼** — "亲爱的客户"而不是你的名字
3. **可疑链接** — 将鼠标悬停在链接上查看真实URL
4. **语法错误** — 正规公司会校对邮件内容
5. **意外附件** — 不要打开未知发件人的附件
6. **索要个人信息** — 正规公司不会通过邮件索要密码

**黄金法则：** 如有疑问，请直接在浏览器中输入官网地址访问。""",
        },
    },
    {
        "title": "签证诈骗警告",
        "content_type": "tip",
        "language": "zh",
        "difficulty_level": "beginner",
        "content": {
            "body": """骗子针对移民和国际学生发送虚假签证威胁：

**常见手段：**
- "您的签证已被取消，点击此处恢复。"
- "移民局官员将上门，除非您支付罚款。"
- "您的工作许可正在审核中，请立即验证身份。"

**如何保护自己：**
1. 政府机构绝不会通过短信或邮件要求付款
2. 始终通过官方网站核实信息
3. 不要通过聊天软件分享护照或签证信息
4. 向当地移民局举报可疑消息

**记住：** 真正的移民问题通过官方邮件或确认电话通知。""",
        },
    },
    # ── Malay Tips ──
    {
        "title": "Cara Mengesan E-mel Phishing",
        "content_type": "tip",
        "language": "ms",
        "difficulty_level": "beginner",
        "content": {
            "body": """E-mel phishing biasanya mempunyai tanda-tanda ini:

1. **Bahasa mendesak** — "Akaun anda akan ditutup dalam 24 jam!"
2. **Salam umum** — "Pelanggan yang dihormati" dan bukan nama anda
3. **Pautan mencurigakan** — Tuding tetikus ke pautan untuk melihat URL sebenar
4. **Kesilapan tatabahasa** — Syarikat profesional menyemak e-mel mereka
5. **Lampiran tidak dijangka** — Jangan buka lampiran daripada pengirim yang tidak dikenali
6. **Maklumat peribadi** — Syarikat sah tidak akan minta kata laluan melalui e-mel

**Peraturan emas:** Jika ragu-ragu, pergi terus ke laman web dengan menaip URL sendiri.""",
        },
    },
    # ── Tamil Tips ──
    {
        "title": "ஃபிஷிங் மின்னஞ்சலை எவ்வாறு கண்டறிவது",
        "content_type": "tip",
        "language": "ta",
        "difficulty_level": "beginner",
        "content": {
            "body": """ஃபிஷிங் மின்னஞ்சல்களில் பொதுவாக இந்த எச்சரிக்கை அறிகுறிகள் இருக்கும்:

1. **அவசர மொழி** — "உங்கள் கணக்கு 24 மணி நேரத்தில் மூடப்படும்!"
2. **பொதுவான வாழ்த்துகள்** — "அன்புள்ள வாடிக்கையாளர்"
3. **சந்தேகத்திற்குரிய இணைப்புகள்** — உண்மையான URL-ஐ காண இணைப்புகள் மீது சுட்டிக்காட்டவும்
4. **இலக்கண தவறுகள்** — தொழில்முறை நிறுவனங்கள் தங்கள் மின்னஞ்சல்களை சரிபார்க்கும்
5. **எதிர்பாராத இணைப்புகள்** — தெரியான அனுப்புநர்களிடமிருந்து இணைப்புகளைத் திறக்க வேண்டாம்

**தங்க விதி:** சந்தேகம் இருந்தால், நீங்களே URL-ஐ தட்டச்சு செய்து இணையதளத்தை நேரடியாக அணுகவும்.""",
        },
    },
    # ── Quizzes ──
    {
        "title": "Phishing Detection Quiz",
        "content_type": "quiz",
        "language": "en",
        "difficulty_level": "beginner",
        "content": {
            "questions": [
                {
                    "id": "q1",
                    "question": "Which of these is a sign of a phishing email?",
                    "options": {
                        "a": "The email uses your full name",
                        "b": "The email asks you to click a link to verify your account urgently",
                        "c": "The email comes from a known company domain",
                        "d": "The email has proper grammar and formatting",
                    },
                },
                {
                    "id": "q2",
                    "question": "What should you do if you receive a suspicious email from your bank?",
                    "options": {
                        "a": "Click the link to check if it's real",
                        "b": "Reply asking if it's legitimate",
                        "c": "Go to the bank's website directly by typing the URL",
                        "d": "Forward it to all your contacts",
                    },
                },
                {
                    "id": "q3",
                    "question": "Government immigration agencies communicate visa issues through:",
                    "options": {
                        "a": "WhatsApp messages with payment links",
                        "b": "Emails asking for passport photos",
                        "c": "Official postal mail or verified phone calls",
                        "d": "Social media direct messages",
                    },
                },
            ],
            "correct_answers": {
                "q1": "b",
                "q2": "c",
                "q3": "c",
            },
        },
    },
    {
        "title": "防钓鱼测验",
        "content_type": "quiz",
        "language": "zh",
        "difficulty_level": "beginner",
        "content": {
            "questions": [
                {
                    "id": "q1",
                    "question": "以下哪项是钓鱼邮件的特征？",
                    "options": {
                        "a": "邮件使用了你的全名",
                        "b": "邮件要求你紧急点击链接验证账户",
                        "c": "邮件来自已知公司域名",
                        "d": "邮件语法正确、格式规范",
                    },
                },
                {
                    "id": "q2",
                    "question": "收到可疑的银行邮件应该怎么做？",
                    "options": {
                        "a": "点击链接检查是否真实",
                        "b": "回复邮件询问是否合法",
                        "c": "直接在浏览器输入银行官网地址访问",
                        "d": "转发给所有联系人",
                    },
                },
                {
                    "id": "q3",
                    "question": "政府移民机构通过什么方式通知签证问题？",
                    "options": {
                        "a": "WhatsApp消息附带付款链接",
                        "b": "邮件要求发送护照照片",
                        "c": "官方信件或已确认的电话",
                        "d": "社交媒体私信",
                    },
                },
            ],
            "correct_answers": {
                "q1": "b",
                "q2": "c",
                "q3": "c",
            },
        },
    },
]

for item in contents:
    existing = (
        db.query(EducationContent)
        .filter(
            EducationContent.title == item["title"],
            EducationContent.language == item["language"],
        )
        .first()
    )
    if not existing:
        db.add(EducationContent(**item))
        print(f"[+] Education: {item['language'].upper()} — {item['title']}")

db.commit()
db.close()
print("\n[✓] Seed complete!")
