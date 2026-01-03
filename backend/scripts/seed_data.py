"""
Seed data script for TeachBetter application (Updated for Final Demo)
Context: ITSS Japanese Teacher (Nguyen Thi Diep)
"""
import asyncio
from datetime import datetime, timedelta
import random
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from bson import ObjectId

# Fix encoding issue on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Database settings
MONGODB_URL = "mongodb://localhost:27017"
MONGODB_DB_NAME = "teach_better_db"

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
DEFAULT_PASSWORD = "password123"

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# ============ 1. USERS DATA (PERSONAS) ============
USERS = [
    # --- MAIN CHARACTER (DEMO USER) ---
    {
        "id_ref": "diep",
        "name": "Nguyễn Thị Điệp",  # Tên hiển thị đầy đủ
        "email": "diep.nguyen@example.com", # Email đăng nhập
        "role": "user",
        "bio": "Giáo viên mới phụ trách môn ITSS. Đang tìm phương pháp dạy Agile hiệu quả cho sinh viên N4-N3.",
        "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Diep2"
    },
    # --- ADMINS ---
    {
        "id_ref": "admin1",
        "name": "Admin System",
        "email": "admin@teachbetter.com",
        "role": "admin",
        "bio": "System Administrator",
        "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Admin1"
    },
    # --- SUPPORTING CHARACTERS (SENSEIS) ---
    {
        "id_ref": "yorifuji",
        "name": "Yorifuji", # Chỉ để họ
        "email": "yorifuji@example.com",
        "role": "user",
        "bio": "ITSS担当。現場経験10年のベテラン。",
        "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Yorifuji"
    },
    {
        "id_ref": "kimura",
        "name": "Kimura", # Chỉ để họ
        "email": "kimura@example.com",
        "role": "user",
        "bio": "たとえ話が得意な先生。",
        "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Kimura"
    },
    {
        "id_ref": "diem",
        "name": "Diem", # Chỉ để tên
        "email": "diem@example.com",
        "role": "user",
        "bio": "N1保持者のベトナム人教師。",
        "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Diem"
    },
    {
        "id_ref": "giang",
        "name": "Lê Thị Giang",
        "email": "giang.le@example.com",
        "role": "user",
        "bio": "ベトナム人のITSS専門講師。実務経験豊富。",
        "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Giang"
    },
    {
        "id_ref": "tanaka",
        "name": "Tanaka",
        "email": "tanaka@example.com",
        "role": "user",
        "bio": "初級文法担当。",
        "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Tanaka"
    },
    # --- FILLER USERS (Để tạo bài viết rác cho xôm) ---
    { "id_ref": "sato", "name": "Sato", "email": "sato@ex.com", "role": "user", "bio": "漢字教育", "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Sato" },
    { "id_ref": "suzuki", "name": "Suzuki", "email": "suzuki@ex.com", "role": "user", "bio": "会話クラス", "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Suzuki" },
    { "id_ref": "yamada", "name": "Yamada", "email": "yamada@ex.com", "role": "user", "bio": "作文指導", "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Yamada" },
    { "id_ref": "takahashi", "name": "Takahashi", "email": "taka@ex.com", "role": "user", "bio": "JLPT対策", "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Taka" }
]

# ============ 2. CATEGORIES ============
CATEGORIES = [
    {"name": "IT日本語 (IT Nihongo)", "description": "ITSS, Thuật ngữ chuyên ngành, Quy trình phát triển"},
    {"name": "文法指導 (Grammar)", "description": "Phương pháp dạy ngữ pháp, Phân tích lỗi sai"},
    {"name": "授業運営 (Classroom)", "description": "Quản lý lớp học, Tạo động lực, Game"},
    {"name": "会話・聴解 (Kaiwa/Chokai)", "description": "Dạy hội thoại và nghe hiểu"},
    {"name": "キャリア支援 (Career)", "description": "Phỏng vấn, Viết CV, Business Manners"}
]

# ============ 3. TAGS ============
TAGS_BY_CATEGORY = {
    "IT日本語 (IT Nihongo)": [
        {"name": "QA/QC", "description": "Chất lượng phần mềm"},
        {"name": "Agile/Scrum", "description": "Phương pháp phát triển"},
        {"name": "基本情報 (FE)", "description": "Luyện thi FE"},
        {"name": "要件定義", "description": "Định nghĩa yêu cầu"}
    ],
    "文法指導 (Grammar)": [
        {"name": "導入 (Introduction)", "description": "Cách vào bài"},
        {"name": "N3レベル", "description": "Trình độ Trung cấp"},
        {"name": "N4レベル", "description": "Trình độ Sơ cấp 2"},
        {"name": "受身形 (Passive)", "description": "Thể bị động"},
        {"name": "使役形 (Causative)", "description": "Thể sai khiến"}
    ],
    "授業運営 (Classroom)": [
        {"name": "Game", "description": "Trò chơi lớp học"},
        {"name": "Ice Break", "description": "Khuấy động không khí"},
        {"name": "Trouble", "description": "Xử lý sự cố"}
    ],
    "キャリア支援 (Career)": [
        {"name": "面接 (Interview)", "description": "Phỏng vấn xin việc"},
        {"name": "マナー (Manners)", "description": "Văn hóa công sở"}
    ]
}

# ============ 4. POSTS DATA (Nhiều bài để lướt mỏi tay) ============
POSTS_DATA = [
    # --- BÀI MỚI (Đẩy bài Yorifuji xuống) ---
    {
        "author_ref": "suzuki",
        "title": "オンライン授業での学生のモチベーション維持について",
        "content": """リモート授業が増えて、学生の集中力が続かない問題に直面しています。
カメラオフの学生も多く、本当に聞いているのか分からない状況です。

皆さんはどんな工夫をしていますか？
ブレイクアウトルームやクイズなど、効果的な方法があれば教えてください！""",
        "category": "授業運営 (Classroom)",
        "tags": ["Ice Break", "Trouble"],
        "views": 234,
        "days_ago": 0  # Posted today
    },
    {
        "author_ref": "kimura",
        "title": "N3文法「〜によって」の使い分けが難しい",
        "content": """「方法」「原因」「人によって違う」など、〜によっての用法が多すぎて学生が混乱しています。
一つ一つ例文を出しても、試験になると間違える学生が多いです。

効果的な導入方法や練習問題の作り方があれば共有していただけませんか？""",
        "category": "文法指導 (Grammar)",
        "tags": ["N3レベル", "導入 (Introduction)"],
        "views": 189,
        "days_ago": 1
    },
    {
        "author_ref": "diem",
        "title": "面接練習での「志望動機」の添削について",
        "content": """来月から就活が始まる学生の面接練習をしています。
志望動機を聞くと、みんな「日本語が好き」「日本の文化が好き」という答えばかりで、IT企業向けの志望動機になっていません。

どうやって具体的な志望動機を引き出せばいいでしょうか？""",
        "category": "キャリア支援 (Career)",
        "tags": ["面接 (Interview)"],
        "views": 445,
        "days_ago": 1
    },
    {
        "author_ref": "sato",
        "title": "Agileの「スクラムマスター」を日本語でどう説明する？",
        "content": """ITSSの授業でスクラムを教えていますが、「スクラムマスター」の役割を日本語で説明するのが難しいです。
「進行役」「調整役」「ファシリテーター」など色々な訳があって、学生も混乱しています。

実際の現場ではどう呼ばれているのでしょうか？""",
        "category": "IT日本語 (IT Nihongo)",
        "tags": ["Agile/Scrum"],
        "views": 312,
        "days_ago": 2
    },
    {
        "author_ref": "tanaka",
        "title": "JLPT N3の「〜たばかり」と「〜ばかり」の違い",
        "content": """「食べたばかり」（just ate）と「野菜ばかり食べる」（only eat）の違いを説明していますが、
学生は「ばかり」という同じ言葉が出てくると混乱するようです。

分かりやすい教え方のコツはありますか？""",
        "category": "文法指導 (Grammar)",
        "tags": ["N3レベル"],
        "views": 278,
        "days_ago": 3
    },

    # --- BÀI QUAN TRỌNG NHẤT (ĐỂ TÌM KIẾM TRONG DEMO) ---
    {
        "author_ref": "yorifuji",
        "title": "🆘 QAとQCの違い、どう教えれば伝わりますか？", # Tiêu đề đúng kịch bản
        "content": """毎年同じ説明をしているのに、期末テストでまた間違える学生が続出しています... 😓
「QAはプロセス、QCはプロダクト」と教科書通りに言っても、学生の反応はイマイチです。

ベトナム人の学生にとって、この概念は直感的に理解しにくいのでしょうか？
皆さん、学生が「あ！なるほど！」となるような、分かりやすい例え話（メタファー）を持っていませんか？""",
        "category": "IT日本語 (IT Nihongo)",
        "tags": ["QA/QC", "N3レベル"],
        "views": 1250,
        "is_qa_scenario": True, # Cờ để thêm comment
        "days_ago": 5  # Posted 5 days ago
    },

    # --- BÀI CỦA ĐIỆP (Để profile không trống) ---
    {
        "author_ref": "diep",
        "title": "【相談】ITSSの授業で「報連相」をロールプレイで行う際の設定について",
        "content": """新米教師のĐiệpです。来週、報連相（ホウレンソウ）の授業を行います。
単なる説明だけでなく、実際に学生に演じさせたいのですが、N4レベルでもできる簡単なシチュエーション設定はありますか？
今のところ「遅刻の連絡」くらいしか思いつかなくて...""",
        "category": "IT日本語 (IT Nihongo)",
        "tags": ["N4レベル", "Game"],
        "views": 45
    },

    # --- FILLER POSTS (BÀI RÁC CHO XÔM) ---
    {
        "author_ref": "sato",
        "title": "漢字が苦手なIT学生への指導法",
        "content": """コードは書けるのに、仕様書の漢字が読めない学生が多いです。「技術があれば日本語はいらない」と思っている学生に、どう動機づけしていますか？""",
        "category": "授業運営 (Classroom)",
        "tags": ["Trouble"],
        "views": 320
    },
    {
        "author_ref": "tanaka",
        "title": "「〜てもいいですか」と「〜てくれませんか」の使い分け",
        "content": """許可と依頼の違いですが、ベトナム語だと同じような訳になることがあり、混乱する学生がいます。良い図解があれば教えてください。""",
        "category": "文法指導 (Grammar)",
        "tags": ["N4レベル", "導入 (Introduction)"],
        "views": 210
    },
    {
        "author_ref": "suzuki",
        "title": "Agile開発の「スプリント」と「イテレーション」の違い",
        "content": """ITSSの教科書によって定義が曖昧な気がします。授業では厳密に分けるべきでしょうか？それとも「繰り返し」としてまとめて教えてもいいでしょうか？""",
        "category": "IT日本語 (IT Nihongo)",
        "tags": ["Agile/Scrum", "基本情報 (FE)"],
        "views": 89
    },
    {
        "author_ref": "kimura",
        "title": "面接練習でよくある「逆質問」のリスト",
        "content": """日本のIT企業の面接で、最後に「何か質問はありますか？」と聞かれた時、学生が沈黙してしまいます。効果的な逆質問リストを作りたいです。""",
        "category": "キャリア支援 (Career)",
        "tags": ["面接 (Interview)"],
        "views": 560
    },
    {
        "author_ref": "diem",
        "title": "N3文法「〜まま」と「〜っぱなし」の違い",
        "content": """「窓を開けたまま寝る」と「窓を開けっぱなしで寝る」。ニュアンスの違い（不満の有無など）をどう説明していますか？""",
        "category": "文法指導 (Grammar)",
        "tags": ["N3レベル", "誤用分析 (Error Analysis)"],
        "views": 150
    },
    {
        "author_ref": "yamada",
        "title": "授業中に寝ている学生への対応（ITクラス）",
        "content": """夜遅くまでコーディングのバイトをしているそうで、授業中爆睡しています。起こすべきか、寝かせておくべきか...皆さんのクラスではどういうルールですか？""",
        "category": "授業運営 (Classroom)",
        "tags": ["Trouble"],
        "views": 410
    },
    {
        "author_ref": "takahashi",
        "title": "基本情報技術者試験（FE）の日本語語彙リスト",
        "content": """今年の試験に出そうな単語リストを作成しました。欲しい方はコメントください！PDFで送ります。""",
        "category": "IT日本語 (IT Nihongo)",
        "tags": ["基本情報 (FE)"],
        "views": 890
    },
    {
        "author_ref": "yorifuji",
        "title": "ウォーターフォール開発のメリットをどう伝える？",
        "content": """最近はAgileばかり人気ですが、大規模システムでのウォーターフォールの重要性も教えたいです。良い事例はありますか？""",
        "category": "IT日本語 (IT Nihongo)",
        "tags": ["要件定義", "Agile/Scrum"],
        "views": 120
    },
    {
        "author_ref": "sato",
        "title": "「上流工程」と「下流工程」のイメージ図",
        "content": """川の流れに例えて説明していますが、他にいいアイデアはありますか？""",
        "category": "IT日本語 (IT Nihongo)",
        "tags": ["要件定義", "導入 (Introduction)"],
        "views": 230
    },
    {
        "author_ref": "tanaka",
        "title": "受身形（Ukemi）の導入ゲーム",
        "content": """「泥棒に財布を盗まれた」だと暗いので、もっと楽しい導入ゲームを探しています。""",
        "category": "文法指導 (Grammar)",
        "tags": ["受身形 (Passive)", "Game"],
        "views": 340
    },
    {
        "author_ref": "suzuki",
        "title": "日本人のPMとの飲み会マナー",
        "content": """インターンに行く学生向けに、飲み会での席次やお酒の注ぎ方を教える必要はありますか？最近は日本もフラットになってきていると聞きますが。""",
        "category": "キャリア支援 (Career)",
        "tags": ["マナー (Manners)"],
        "views": 670
    },
    {
        "author_ref": "diem",
        "title": "敬語「〜ていただく」の過剰使用について",
        "content": """「ご参加していただく」「お読みしていただく」のような二重敬語？変な日本語を使う学生が増えています。""",
        "category": "文法指導 (Grammar)",
        "tags": ["N3レベル", "誤用分析 (Error Analysis)"],
        "views": 180
    },
    {
        "author_ref": "kimura",
        "title": "Gitのコミットメッセージの日本語指導",
        "content": """「修正した」だけじゃなくて、「何を・なぜ」修正したか書くように指導したいです。良いテンプレートはありますか？""",
        "category": "IT日本語 (IT Nihongo)",
        "tags": ["QA/QC"],
        "views": 290
    },
    {
        "author_ref": "yamada",
        "title": "仕様書の読解練習に使えるサイト",
        "content": """実際の仕様書に近い日本語が読めるサイトを探しています。""",
        "category": "IT日本語 (IT Nihongo)",
        "tags": ["要件定義"],
        "views": 450
    },
    {
        "author_ref": "takahashi",
        "title": "JLPT N2の聴解とIT現場の聴解の違い",
        "content": """JLPTは綺麗すぎますよね。もっと早口で省略が多い現場の会話練習用教材を作りませんか？""",
        "category": "会話・聴解 (Kaiwa/Chokai)",
        "tags": ["N3レベル"],
        "views": 510
    }
]

# ============ 5. ANSWERS (COMMENTS) ============
# Comment cho bài QA/QC của Yorifuji (chỉ có Yorifuji, Kimura, Diem, Giang tương tác)
QA_ANSWERS = [
    {
        "author_ref": "diem",
        "content": """🏥 医療に例えるのが鉄板ですよ！

私はいつもこう説明しています：
• QA = 「病気にならないように生活習慣を整える（予防）」
• QC = 「病気を見つけて治す（治療）」

これで私のクラスは全員正解しました✨ 試してみてください！""",
        "upvote_count": 15,
        "downvote_count": 0,
        "comments": [
            {
                "author_ref": "yorifuji",
                "content": "素晴らしいアイデアですね！医療の例えは学生にも伝わりやすそうです。"
            },
            {
                "author_ref": "giang",
                "content": "この例えは本当に分かりやすいです！実際の現場でも使えそうですね。"
            }
        ]
    },
    {
        "author_ref": "kimura",
        "content": """🍳 僕はいつも「料理」で説明します。

• QA = 「レシピや手順のチェック」（調理前の確認）
• QC = 「味見（テイスティング）」（完成品の確認）

レシピが間違っていたら、何度作り直してもマズい料理しかできませんからね（笑）
学生には「料理を作る前に確認するのがQAだよ」と言うと伝わりやすいです。""",
        "upvote_count": 23,
        "downvote_count": 1,
        "comments": [
            {
                "author_ref": "yorifuji",
                "content": "料理の例えも分かりやすいですね！次の授業で使わせていただきます。"
            },
            {
                "author_ref": "diem",
                "content": "学生が喜びそうな例えですね。面白いアプローチです！"
            },
            {
                "author_ref": "giang",
                "content": "料理に例えると学生が食いつきますね（笑）明日から使います！"
            }
        ]
    },
    {
        "author_ref": "giang",
        "content": """🏗️ 私は「家を建てる」に例えています。

• QA = 「設計図や建築計画のチェック」（建てる前の品質保証）
• QC = 「完成した家の検査」（建てた後の品質検査）

設計がダメだと、何度建て直しても欠陥住宅になりますからね。
ITSSの学生には、実際のソフトウェア開発に近いイメージで伝わりやすいです。""",
        "upvote_count": 18,
        "downvote_count": 0,
        "comments": [
            {
                "author_ref": "yorifuji",
                "content": "建築の例えもいいですね！ウォーターフォールの説明にも使えそうです。"
            },
            {
                "author_ref": "kimura",
                "content": "実務に近い例えで、学生もイメージしやすいと思います。"
            }
        ]
    }
]


async def clear_collections(db):
    print("🧹 Clearing existing data...")
    await db.users.delete_many({})
    await db.categories.delete_many({})
    await db.tags.delete_many({})
    await db.posts.delete_many({})
    await db.answers.delete_many({})
    print("✅ Collections cleared!")

async def seed_users(db):
    print("\n👤 Seeding users...")
    hashed_password = get_password_hash(DEFAULT_PASSWORD)
    user_map = {} 
    
    for user in USERS:
        user_doc = {
            "name": user["name"],
            "email": user["email"],
            "hashed_password": hashed_password,
            "avatar_url": user["avatar_url"],
            "bio": user["bio"],
            "role": user["role"],
            "status": "active",
            "violation_count": 0,
            "bookmarks": [],
            "created_at": datetime.utcnow() - timedelta(days=random.randint(1, 90)),
            "updated_at": datetime.utcnow()
        }
        result = await db.users.insert_one(user_doc)
        user_map[user["id_ref"]] = result.inserted_id
        print(f"  ✓ Created user: {user['name']}")
    
    return user_map

async def seed_categories(db):
    print("\n📁 Seeding categories...")
    category_map = {}
    
    for category in CATEGORIES:
        category_doc = {
            "name": category["name"],
            "description": category["description"],
            "post_count": 0,
            "is_active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        result = await db.categories.insert_one(category_doc)
        category_map[category["name"]] = result.inserted_id
    
    return category_map

async def seed_tags(db, user_map):
    print("\n🏷️  Seeding tags...")
    tag_map = {}
    admin_id = user_map["admin1"]
    
    for category_name, tags in TAGS_BY_CATEGORY.items():
        for tag in tags:
            tag_doc = {
                "name": tag["name"],
                "description": tag["description"],
                "post_count": 0,
                "is_active": True,
                "created_by": admin_id,
                "created_at": datetime.utcnow()
            }
            result = await db.tags.insert_one(tag_doc)
            tag_map[tag["name"]] = result.inserted_id
            
    return tag_map

async def seed_posts_and_answers(db, user_map, tag_map):
    print("\n📝 Seeding posts and answers...")
    
    for post_data in POSTS_DATA:
        author_id = user_map[post_data["author_ref"]]
        
        # Lấy tag IDs, bỏ qua nếu tag không tồn tại
        post_tag_ids = []
        if "tags" in post_data:
            post_tag_ids = [tag_map[t] for t in post_data["tags"] if t in tag_map]
        
        # Sử dụng days_ago nếu có, nếu không thì random
        days_ago = post_data.get("days_ago", random.randint(1, 30))

        post_doc = {
            "title": post_data["title"],
            "content": post_data["content"],
            "author_id": author_id,
            "category": post_data["category"],
            "tag_ids": post_tag_ids,
            "answer_count": 0,
            "view_count": post_data.get("views", 0),
            "is_deleted": False,
            "created_at": datetime.utcnow() - timedelta(days=days_ago),
            "updated_at": datetime.utcnow()
        }
        
        result = await db.posts.insert_one(post_doc)
        post_id = result.inserted_id
        
        # Cập nhật số lượng bài viết
        await db.categories.update_one({"name": post_data["category"]}, {"$inc": {"post_count": 1}})
        for tag_id in post_tag_ids:
            await db.tags.update_one({"_id": tag_id}, {"$inc": {"post_count": 1}})

        # Nếu là bài QA/QC Scenario thì thêm comment mẫu
        if post_data.get("is_qa_scenario"):
            print(f"    ↳ Adding QA/QC specific answers to post: {post_data['title'][:20]}...")
            for ans in QA_ANSWERS:
                ans_author_id = user_map[ans["author_ref"]]

                # Tạo comments cho answer này
                comments_list = []
                if "comments" in ans and len(ans["comments"]) > 0:
                    for comment in ans["comments"]:
                        comment_author_id = user_map[comment["author_ref"]]
                        comment_doc = {
                            "id": str(ObjectId()),
                            "author_id": comment_author_id,
                            "content": comment["content"],
                            "created_at": datetime.utcnow() - timedelta(minutes=random.randint(5, 60))
                        }
                        comments_list.append(comment_doc)

                # Tạo fake upvotes/downvotes
                upvote_count = ans.get("upvote_count", random.randint(3, 15))
                downvote_count = ans.get("downvote_count", 0)

                # Tạo danh sách fake user IDs cho votes (loại bỏ Điệp - chỉ có sensei vote)
                # Chỉ cho phép Yorifuji, Kimura, Diem, Giang và các sensei khác vote
                allowed_voters = [user_map[ref] for ref in ["yorifuji", "kimura", "diem", "giang", "tanaka", "sato", "suzuki", "yamada", "takahashi"]]
                upvote_user_ids = random.sample(allowed_voters, min(upvote_count, len(allowed_voters)))
                downvote_user_ids = random.sample(
                    [uid for uid in allowed_voters if uid not in upvote_user_ids],
                    min(downvote_count, len(allowed_voters) - len(upvote_user_ids))
                ) if downvote_count > 0 else []

                answer_doc = {
                    "content": ans["content"],
                    "post_id": post_id,
                    "author_id": ans_author_id,
                    "is_accepted_solution": False,
                    "votes": {
                        "upvoted_by": upvote_user_ids,
                        "downvoted_by": downvote_user_ids,
                        "score": upvote_count - downvote_count
                    },
                    "comments": comments_list,
                    "is_deleted": False,
                    "created_at": datetime.utcnow() - timedelta(hours=random.randint(1, 5)),
                    "updated_at": datetime.utcnow()
                }
                await db.answers.insert_one(answer_doc)
                await db.posts.update_one({"_id": post_id}, {"$inc": {"answer_count": 1}})
            print(f"    ✅ Added {len(QA_ANSWERS)} answers with {sum(ans.get('upvote_count', 0) for ans in QA_ANSWERS)} total upvotes.")

async def main():
    print("=" * 60)
    print("🌱 TEACH BETTER - FINAL DEMO DATA SEEDING")
    print("   User: Nguyễn Thị Điệp | Context: ITSS & Agile")
    print("=" * 60)
    
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[MONGODB_DB_NAME]
    
    try:
        await client.admin.command('ping')
        print("✅ Connected to MongoDB!")
        
        await clear_collections(db)
        user_map = await seed_users(db)
        category_map = await seed_categories(db)
        tag_map = await seed_tags(db, user_map)
        await seed_posts_and_answers(db, user_map, tag_map)
        
        print("\n" + "=" * 60)
        print("🎉 SEEDING COMPLETE! READY FOR DEMO.")
        print("=" * 60)
        print(f"  Login User: diep.nguyen@example.com")
        print(f"  Password:   {DEFAULT_PASSWORD}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(main())