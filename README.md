# Git URL in Files 🔗

أداة Python لاستخراج كل الروابط (خصوصاً روابط Git) من أي ملف أو مجلد.

## 📦 التثبيت

### من GitHub (تطوير محلي)
```bash
git clone https://github.com/ibrahimkhacef5-del/guf-official
cd git-url-in-files
pip install -e .
```

### من PyPI (لو نشرتها)
```bash
pip install git-url-in-files
```

## 🚀 الاستخدام

### CLI
```bash
# استخرج كل الروابط من ملف
git-url-in-files README.md

# استخرج روابط Git فقط من مجلد (بشكل تكراري)
git-url-in-files ./my-project --only-git

# فلترة بامتدادات معينة
git-url-in-files ./src -e .py .md

# مخرجات JSON
git-url-in-files . --json

# من stdin
cat file.txt | git-url-in-files -
```

### Python API
```python
from git_url_in_files import extract_urls, extract_from_file, extract_from_directory

# من نص
print(extract_urls("شوف https://github.com/user/repo.git"))

# من ملف
print(extract_from_file("config.yaml"))

# من مجلد كامل
results = extract_from_directory("./project", extensions=[".py", ".md"])
for file, urls in results.items():
    print(file, "->", urls)
```

## ✅ المزايا
- يدعم `http`, `https`, `ftp`, `git://`, `ssh://`, و `git@host:user/repo.git`
- يعمل على ملف واحد أو مجلد كامل بشكل تكراري
- فلترة بالامتدادات
- تجاهل الملفات الكبيرة والمخفية (قابل للتعديل)
- مخرجات JSON جاهزة للـ CI/CD
- يدعم stdin

## 📄 الترخيص
MIT
