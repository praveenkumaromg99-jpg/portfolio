"""
Praveen's Portfolio — Full Backend
====================================
Database : SQLite (built into Python)
Storage  : Local uploads/ folder

APIs:
  Projects  → GET/POST/DELETE /api/projects
  Documents → GET/POST/DELETE /api/documents
  Blog      → GET/POST/DELETE /api/blog
  Files     → GET /api/files, POST /api/upload
  Messages  → GET/POST /api/contact
  Profile   → GET /api/profile

Run:     python app.py
Install: pip install flask flask-cors
"""

from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import sqlite3, os, datetime, uuid

app = Flask(__name__, static_folder=".")
CORS(app)

# =============================================
# CONFIG
# =============================================
YOUR_NAME      = "Praveen Kumar S"
YOUR_EMAIL     = "praveenkumaromg9@gmail.com"
YOUR_INSTAGRAM = "@1611_b.i.boof"
YOUR_GITHUB    = "https://github.com/praveenkumaromg99-jpg"
YOUR_LINKEDIN  = "https://www.linkedin.com/in/praveen-kumar-s-7a840032b"

DB_PATH        = "portfolio.db"
UPLOAD_FOLDER  = "uploads"
MAX_FILE_MB    = 50  # max upload size in MB

ALLOWED = {
    "pdf", "pptx", "ppt", "xlsx", "xls",
    "ipynb", "py", "pbix", "png", "jpg",
    "jpeg", "gif", "webp", "csv", "docx"
}

app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_MB * 1024 * 1024

# =============================================
# DATABASE SETUP
# =============================================
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Create all tables if they don't exist."""
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    for folder in ["projects","documents","presentations","excel","notebooks","powerbi","images","other"]:
        os.makedirs(f"{UPLOAD_FOLDER}/{folder}", exist_ok=True)

    conn = get_db()
    c = conn.cursor()

    # Projects table
    c.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT NOT NULL,
            description TEXT,
            category    TEXT DEFAULT 'General',
            tools       TEXT,
            link        TEXT DEFAULT '#',
            file_id     INTEGER,
            thumbnail   TEXT,
            created_at  TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Documents table (thesis, articles, reports)
    c.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT NOT NULL,
            description TEXT,
            doc_type    TEXT DEFAULT 'Article',
            file_id     INTEGER,
            created_at  TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Blog/Writing table
    c.execute("""
        CREATE TABLE IF NOT EXISTS blog (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT NOT NULL,
            content     TEXT,
            excerpt     TEXT,
            post_type   TEXT DEFAULT 'blog',
            tags        TEXT,
            created_at  TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Files table (all uploaded files)
    c.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            filename    TEXT NOT NULL,
            original    TEXT NOT NULL,
            file_type   TEXT,
            category    TEXT,
            size_kb     INTEGER,
            path        TEXT,
            uploaded_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Messages table
    c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            email       TEXT NOT NULL,
            message     TEXT NOT NULL,
            timestamp   TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    print("[DB] Database initialized ✅")

def row_to_dict(row):
    return dict(row) if row else None

def rows_to_list(rows):
    return [dict(r) for r in rows]

# =============================================
# HELPERS
# =============================================
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED

def get_category(ext):
    ext = ext.lower()
    if ext == "pdf":             return "documents"
    if ext in ("pptx","ppt"):   return "presentations"
    if ext in ("xlsx","xls"):   return "excel"
    if ext in ("ipynb","py"):   return "notebooks"
    if ext == "pbix":           return "powerbi"
    if ext in ("png","jpg","jpeg","gif","webp"): return "images"
    return "other"

# =============================================
# SERVE FRONTEND & ADMIN
# =============================================
@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/admin")
def admin():
    return send_from_directory(".", "admin.html")

@app.route("/uploads/<path:filename>")
def serve_upload(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# =============================================
# PROFILE
# =============================================
@app.route("/api/profile")
def profile():
    return jsonify({
        "name":      YOUR_NAME,
        "title":     "BSc Statistics Student",
        "college":   "Dr. Ambedkar Arts & Science College, Vyasarpadi, Chennai",
        "email":     YOUR_EMAIL,
        "instagram": YOUR_INSTAGRAM,
        "github":    YOUR_GITHUB,
        "linkedin":  YOUR_LINKEDIN,
        "skills":    ["Python", "SQL", "Power BI", "Statistics", "Excel", "PowerPoint"],
        "hobbies":   ["Football", "Gym", "Reading Books", "Writing Poetry"],
        "writing": {
            "books_published": 1,
            "genres": ["Poetry", "Short Stories"]
        }
    })

# =============================================
# FILE UPLOAD API
# =============================================
@app.route("/api/upload", methods=["POST"])
def upload_file():
    """
    Upload any file (PDF, PPTX, XLSX, IPYNB, PBIX, images).
    Form fields:
      file     - the file (required)
    Returns: file record with id, filename, path
    """
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    f = request.files["file"]
    if f.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not allowed_file(f.filename):
        return jsonify({"error": f"File type not allowed. Allowed: {', '.join(ALLOWED)}"}), 400

    ext      = f.filename.rsplit(".", 1)[1].lower()
    category = get_category(ext)
    unique   = str(uuid.uuid4())[:8]
    safe     = f.filename.replace(" ", "_")
    filename = f"{unique}_{safe}"
    rel_path = f"{category}/{filename}"
    abs_path = os.path.join(UPLOAD_FOLDER, rel_path)

    f.save(abs_path)
    size_kb = os.path.getsize(abs_path) // 1024

    conn = get_db()
    c    = conn.cursor()
    c.execute("""
        INSERT INTO files (filename, original, file_type, category, size_kb, path)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (filename, f.filename, ext, category, size_kb, rel_path))
    file_id = c.lastrowid
    conn.commit()

    result = row_to_dict(c.execute("SELECT * FROM files WHERE id=?", (file_id,)).fetchone())
    conn.close()

    print(f"[UPLOAD] {f.filename} → {rel_path} ({size_kb} KB)")
    return jsonify({"success": True, "file": result}), 201


@app.route("/api/files", methods=["GET"])
def get_files():
    """Get all uploaded files. Filter by ?category=documents etc."""
    category = request.args.get("category", "")
    conn = get_db()
    if category:
        rows = conn.execute("SELECT * FROM files WHERE category=? ORDER BY uploaded_at DESC", (category,)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM files ORDER BY uploaded_at DESC").fetchall()
    conn.close()
    return jsonify(rows_to_list(rows))


@app.route("/api/files/<int:file_id>", methods=["DELETE"])
def delete_file(file_id):
    conn = get_db()
    row  = conn.execute("SELECT * FROM files WHERE id=?", (file_id,)).fetchone()
    if not row:
        conn.close()
        return jsonify({"error": "File not found"}), 404

    path = os.path.join(UPLOAD_FOLDER, row["path"])
    if os.path.exists(path):
        os.remove(path)

    conn.execute("DELETE FROM files WHERE id=?", (file_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": f"File {file_id} deleted"})

# =============================================
# PROJECTS API
# =============================================
@app.route("/api/projects", methods=["GET"])
def get_projects():
    conn  = get_db()
    rows  = conn.execute("SELECT * FROM projects ORDER BY created_at DESC").fetchall()
    conn.close()
    projects = []
    for r in rows:
        p = dict(r)
        p["tools"] = p["tools"].split(",") if p["tools"] else []
        projects.append(p)
    return jsonify(projects)


@app.route("/api/projects", methods=["POST"])
def add_project():
    """
    Add project. Send as multipart/form-data:
      title, description, category, tools (comma separated), link, file (optional)
    """
    title       = request.form.get("title","").strip()
    description = request.form.get("description","").strip()
    category    = request.form.get("category","General")
    tools       = request.form.get("tools","")
    link        = request.form.get("link","#")
    file_id     = None

    if not title:
        return jsonify({"error": "title is required"}), 400

    # Handle optional file upload
    if "file" in request.files and request.files["file"].filename:
        upload_resp = upload_file()
        if upload_resp[1] == 201:
            file_id = upload_resp[0].get_json()["file"]["id"]

    conn = get_db()
    c    = conn.cursor()
    c.execute("""
        INSERT INTO projects (title, description, category, tools, link, file_id)
        VALUES (?,?,?,?,?,?)
    """, (title, description, category, tools, link, file_id))
    project_id = c.lastrowid
    conn.commit()
    result = row_to_dict(c.execute("SELECT * FROM projects WHERE id=?", (project_id,)).fetchone())
    conn.close()
    print(f"[PROJECT] Added: {title}")
    return jsonify(result), 201


@app.route("/api/projects/<int:pid>", methods=["DELETE"])
def delete_project(pid):
    conn = get_db()
    conn.execute("DELETE FROM projects WHERE id=?", (pid,))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

# =============================================
# DOCUMENTS API (thesis, articles)
# =============================================
@app.route("/api/documents", methods=["GET"])
def get_documents():
    conn = get_db()
    rows = conn.execute("SELECT * FROM documents ORDER BY created_at DESC").fetchall()
    conn.close()
    return jsonify(rows_to_list(rows))


@app.route("/api/documents", methods=["POST"])
def add_document():
    """
    Add document. Send as multipart/form-data:
      title, description, doc_type (Thesis/Article/Report), file
    """
    title       = request.form.get("title","").strip()
    description = request.form.get("description","").strip()
    doc_type    = request.form.get("doc_type","Article")
    file_id     = None

    if not title:
        return jsonify({"error": "title is required"}), 400

    if "file" in request.files and request.files["file"].filename:
        upload_resp = upload_file()
        if upload_resp[1] == 201:
            file_id = upload_resp[0].get_json()["file"]["id"]

    conn = get_db()
    c    = conn.cursor()
    c.execute("""
        INSERT INTO documents (title, description, doc_type, file_id)
        VALUES (?,?,?,?)
    """, (title, description, doc_type, file_id))
    doc_id = c.lastrowid
    conn.commit()
    result = row_to_dict(c.execute("SELECT * FROM documents WHERE id=?", (doc_id,)).fetchone())
    conn.close()
    print(f"[DOCUMENT] Added: {title}")
    return jsonify(result), 201


@app.route("/api/documents/<int:did>", methods=["DELETE"])
def delete_document(did):
    conn = get_db()
    conn.execute("DELETE FROM documents WHERE id=?", (did,))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

# =============================================
# BLOG API
# =============================================
@app.route("/api/blog", methods=["GET"])
def get_blog():
    post_type = request.args.get("type","")
    conn = get_db()
    if post_type:
        rows = conn.execute("SELECT * FROM blog WHERE post_type=? ORDER BY created_at DESC",(post_type,)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM blog ORDER BY created_at DESC").fetchall()
    conn.close()
    posts = []
    for r in rows:
        p = dict(r)
        p["tags"] = p["tags"].split(",") if p["tags"] else []
        posts.append(p)
    return jsonify(posts)


@app.route("/api/blog", methods=["POST"])
def add_blog():
    data    = request.get_json()
    title   = data.get("title","").strip()
    content = data.get("content","").strip()
    if not title or not content:
        return jsonify({"error": "title and content required"}), 400
    excerpt   = data.get("excerpt","") or content[:150] + "…"
    post_type = data.get("post_type","blog")
    tags      = ",".join(data.get("tags",[]))
    conn = get_db()
    c    = conn.cursor()
    c.execute("""
        INSERT INTO blog (title, content, excerpt, post_type, tags)
        VALUES (?,?,?,?,?)
    """, (title, content, excerpt, post_type, tags))
    post_id = c.lastrowid
    conn.commit()
    result = row_to_dict(c.execute("SELECT * FROM blog WHERE id=?", (post_id,)).fetchone())
    conn.close()
    return jsonify(result), 201


@app.route("/api/blog/<int:bid>", methods=["DELETE"])
def delete_blog(bid):
    conn = get_db()
    conn.execute("DELETE FROM blog WHERE id=?", (bid,))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

# =============================================
# CONTACT API
# =============================================
@app.route("/api/contact", methods=["POST"])
def contact():
    data    = request.get_json()
    name    = data.get("name","").strip()
    email   = data.get("email","").strip()
    message = data.get("message","").strip()
    if not name or not email or not message:
        return jsonify({"error": "All fields required"}), 400
    conn = get_db()
    conn.execute("INSERT INTO messages (name,email,message) VALUES (?,?,?)", (name,email,message))
    conn.commit()
    conn.close()
    print(f"[MESSAGE] From {name} <{email}>")
    return jsonify({"success": True, "reply": f"Thanks {name}! I'll get back to you soon."})


@app.route("/api/messages", methods=["GET"])
def get_messages():
    conn = get_db()
    rows = conn.execute("SELECT * FROM messages ORDER BY timestamp DESC").fetchall()
    conn.close()
    return jsonify(rows_to_list(rows))

# =============================================
# STATS (dashboard summary)
# =============================================
@app.route("/api/stats")
def stats():
    conn = get_db()
    return jsonify({
        "projects":  conn.execute("SELECT COUNT(*) FROM projects").fetchone()[0],
        "documents": conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0],
        "blog":      conn.execute("SELECT COUNT(*) FROM blog").fetchone()[0],
        "files":     conn.execute("SELECT COUNT(*) FROM files").fetchone()[0],
        "messages":  conn.execute("SELECT COUNT(*) FROM messages").fetchone()[0],
    })

# =============================================
# START
# =============================================
if __name__ == "__main__":
    init_db()
    print("\n" + "="*48)
    print(f"  {YOUR_NAME}'s Portfolio Backend ✅")
    print("  Website  → http://localhost:5000")
    print("  Admin    → http://localhost:5000/admin")
    print("  API:")
    print("    GET  /api/profile")
    print("    GET  /api/projects    POST /api/projects")
    print("    GET  /api/documents   POST /api/documents")
    print("    GET  /api/blog        POST /api/blog")
    print("    POST /api/upload      GET  /api/files")
    print("    POST /api/contact     GET  /api/messages")
    print("    GET  /api/stats")
    print("="*48 + "\n")
    app.run(debug=True, port=5000)
