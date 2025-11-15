# post.py
import os, json, random, time
import tweepy

# تحميل التغريدات من ملف
with open("posts.txt", "r", encoding="utf-8") as f:
    posts = [line.strip() for line in f if line.strip()]
if not posts:
    raise SystemExit("posts.txt is empty — add some tweets.")

# قراءة بيانات الحسابات من متغير البيئة ACCOUNTS_JSON
accounts_json = os.getenv("ACCOUNTS_JSON")
if not accounts_json:
    raise SystemExit("ACCOUNTS_JSON environment variable not set. Add it as a GitHub Secret.")

try:
    data = json.loads(accounts_json)
    accounts = data.get("accounts", [])
except Exception as e:
    raise SystemExit(f"Failed to parse ACCOUNTS_JSON: {e}")

if not accounts:
    raise SystemExit("No accounts found in ACCOUNTS_JSON (expected key 'accounts').")

# لكل حساب: إعداد auth ونشر تغريدة عشوائية
for idx, acct in enumerate(accounts, start=1):
    try:
        consumer_key = acct["consumer_key"]
        consumer_secret = acct["consumer_secret"]
        access_token = acct["access_token"]
        access_token_secret = acct["access_token_secret"]
    except KeyError as e:
        print(f"[Account {idx}] Missing key in ACCOUNTS_JSON: {e}")
        continue

    try:
        auth = tweepy.OAuth1UserHandler(
            consumer_key, consumer_secret,
            access_token, access_token_secret
        )
        api = tweepy.API(auth)
        tweet = random.choice(posts)
        # نشر التغريدة
        api.update_status(tweet)
        print(f"[Account {idx}] Tweet posted.")
        # تأخير قصير لتجنب spike requests
        time.sleep(2)
    except Exception as e:
        print(f"[Account {idx}] Failed to post: {e}")
