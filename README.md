## Installation

+ "django-environ" = "==0.4.1"
+ "dj-database-url" = "==0.4.2"
+ "django-compressor" = "==1.6"
+ "python-dotenv"


## 需要檔案

1. 在 `settings/ ` 底下建立一個 local.env。
2. .env 檔案內包含下列變數環境：
    + DEBUG="True" 要運行的環境  # True or False
    + DATABASE_URL= 指定資料庫路徑。資料庫路徑資訊由 dj-database-url 管理，# syntax: DATABASE_URL=postgres://username:password@127.0.0.1:5432/database
    + SECRET_KEY= DJANGO_SECRET_KEY 指定 Django 需要的 secret key。 # 不需要 "" 包住。

