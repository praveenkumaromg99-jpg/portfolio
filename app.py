"""
Praveen's Portfolio — Python Flask Backend
==========================================
APIs:
  GET  /api/projects          → all projects
  GET  /api/projects/<id>     → single project
  POST /api/projects          → add a project  (admin)

  GET  /api/blog              → all blog posts
  GET  /api/blog/<id>         → single post
  POST /api/blog              → add a post     (admin)

  GET  /api/profile           → your profile info
  POST /api/contact           → contact form

Run:     python app.py
Install: pip install flask flask-cors
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import datetime, json, os

app = Flask(__name__, static_folder=".")
CORS(app)

# =============================================
# ✏️  CONFIG — edit these
# =============================================
YOUR_NAME      = "Praveen"
YOUR_INSTAGRAM = "@your_instagram"        # ✏️ update this
YOUR_GITHUB    = "https://github.com/yourusername"  # ✏️ update this
YOUR_EMAIL     = "your@email.com"         # ✏️ update this

PROJECTS_FILE  = "data/projects.json"
BLOG_FILE      = "data/blog.json"
MESSAGES_FILE  = "data/messages.json"


# =============================================
# HELPERS
# =============================================
def read_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def next_id(items):
    if not items:
        return 1
    return max(item.get("id", 0) for item in items) + 1


# =============================================
# SERVE FRONTEND
# =============================================
@app.route("/")
def index():
    return send_from_directory(".", "index.html")


# =============================================
# PROFILE
# =============================================
@app.route("/api/profile")
def profile():
    return jsonify({
        "name":      YOUR_NAME,
        "title":     "BSc Statistics Student",
        "instagram": YOUR_INSTAGRAM,
        "github":    YOUR_GITHUB,
        "email":     YOUR_EMAIL,
        "skills":    ["Python", "SQL", "Power BI", "Statistics"],
        "hobbies":   ["Football", "Gym", "Reading Books", "Writing Poetry"],
        "writing": {
            "books_published": 1,
            "genres": ["Poetry", "Short Stories"]
        }
    })


# =============================================
# PROJECTS API
# =============================================
@app.route("/api/projects", methods=["GET"])
def get_projects():
    """Return all projects, newest first."""
    projects = read_json(PROJECTS_FILE)
    return jsonify(projects[::-1])   # newest first


@app.route("/api/projects/<int:project_id>", methods=["GET"])
def get_project(project_id):
    """Return a single project by ID."""
    projects = read_json(PROJECTS_FILE)
    project = next((p for p in projects if p["id"] == project_id), None)
    if not project:
        return jsonify({"error": "Project not found"}), 404
    return jsonify(project)


@app.route("/api/projects", methods=["POST"])
def add_project():
    """
    Add a new project.
    Body (JSON):
      title        - required
      description  - required
      tools        - list, e.g. ["Python", "Pandas"]
      tag          - e.g. "Python" / "Power BI" / "SQL"
      link         - URL to project (optional)
      image        - image URL (optional)
    """
    data = request.get_json()
    title       = data.get("title", "").strip()
    description = data.get("description", "").strip()

    if not title or not description:
        return jsonify({"error": "title and description are required"}), 400

    projects = read_json(PROJECTS_FILE)
    new_project = {
        "id":          next_id(projects),
        "title":       title,
        "description": description,
        "tools":       data.get("tools", []),
        "tag":         data.get("tag", "Project"),
        "link":        data.get("link", "#"),
        "image":       data.get("image", ""),
        "created_at":  datetime.datetime.now().isoformat()
    }
    projects.append(new_project)
    write_json(PROJECTS_FILE, projects)
    print(f"[PROJECT ADDED] {title}")
    return jsonify(new_project), 201


@app.route("/api/projects/<int:project_id>", methods=["DELETE"])
def delete_project(project_id):
    """Delete a project by ID."""
    projects = read_json(PROJECTS_FILE)
    updated = [p for p in projects if p["id"] != project_id]
    if len(updated) == len(projects):
        return jsonify({"error": "Project not found"}), 404
    write_json(PROJECTS_FILE, updated)
    return jsonify({"success": True, "message": f"Project {project_id} deleted"})


# =============================================
# BLOG API
# =============================================
@app.route("/api/blog", methods=["GET"])
def get_posts():
    """Return all blog posts, newest first."""
    posts = read_json(BLOG_FILE)
    # Support ?tag= filter
    tag = request.args.get("tag", "").strip()
    if tag:
        posts = [p for p in posts if tag.lower() in [t.lower() for t in p.get("tags", [])]]
    return jsonify(posts[::-1])


@app.route("/api/blog/<int:post_id>", methods=["GET"])
def get_post(post_id):
    """Return a single blog post by ID."""
    posts = read_json(BLOG_FILE)
    post = next((p for p in posts if p["id"] == post_id), None)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    return jsonify(post)


@app.route("/api/blog", methods=["POST"])
def add_post():
    """
    Add a new blog/writing post.
    Body (JSON):
      title    - required
      content  - required (the full text of your post/poem/story)
      type     - "blog" / "poem" / "story" (default: "blog")
      tags     - list, e.g. ["statistics", "python"]
      excerpt  - short preview text (optional, auto-generated if missing)
    """
    data = request.get_json()
    title   = data.get("title", "").strip()
    content = data.get("content", "").strip()

    if not title or not content:
        return jsonify({"error": "title and content are required"}), 400

    # Auto-generate excerpt from first 150 chars of content
    excerpt = data.get("excerpt", "") or content[:150] + ("…" if len(content) > 150 else "")

    posts = read_json(BLOG_FILE)
    new_post = {
        "id":         next_id(posts),
        "title":      title,
        "content":    content,
        "excerpt":    excerpt,
        "type":       data.get("type", "blog"),
        "tags":       data.get("tags", []),
        "created_at": datetime.datetime.now().isoformat()
    }
    posts.append(new_post)
    write_json(BLOG_FILE, posts)
    print(f"[POST ADDED] {title}")
    return jsonify(new_post), 201


@app.route("/api/blog/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    """Delete a blog post by ID."""
    posts = read_json(BLOG_FILE)
    updated = [p for p in posts if p["id"] != post_id]
    if len(updated) == len(posts):
        return jsonify({"error": "Post not found"}), 404
    write_json(BLOG_FILE, updated)
    return jsonify({"success": True, "message": f"Post {post_id} deleted"})


# =============================================
# CONTACT FORM API
# =============================================
@app.route("/api/contact", methods=["POST"])
def contact():
    """
    Receive and save a contact form message.
    Body: { name, email, message }
    """
    data    = request.get_json()
    name    = data.get("name", "").strip()
    email   = data.get("email", "").strip()
    message = data.get("message", "").strip()

    if not name or not email or not message:
        return jsonify({"error": "All fields are required"}), 400

    messages = read_json(MESSAGES_FILE)
    messages.append({
        "id":        next_id(messages),
        "name":      name,
        "email":     email,
        "message":   message,
        "timestamp": datetime.datetime.now().isoformat()
    })
    write_json(MESSAGES_FILE, messages)
    print(f"[CONTACT] {name} <{email}>")
    return jsonify({"success": True, "reply": f"Thanks {name}! I'll get back to you soon."})


# =============================================
# SEED DEMO DATA  (run once to populate)
# =============================================
def seed_demo_data():
    """Creates sample projects and blog post if data folder is empty."""
    os.makedirs("data", exist_ok=True)

    if not os.path.exists(PROJECTS_FILE):
        demo_projects = [
            {
                "id": 1,
                "title": "Statistical Analysis Project",
                "description": "Real-world data analysis using Python and statistical methods.",
                "tools": ["Python", "Pandas", "Matplotlib"],
                "tag": "Python",
                "link": "#",
                "image": "",
                "created_at": datetime.datetime.now().isoformat()
            },
            {
                "id": 2,
                "title": "Power BI Dashboard",
                "description": "An interactive dashboard visualizing trends and insights.",
                "tools": ["Power BI", "Excel"],
                "tag": "Power BI",
                "link": "#",
                "image": "",
                "created_at": datetime.datetime.now().isoformat()
            },
            {
                "id": 3,
                "title": "SQL Database Project",
                "description": "Designing and querying a relational database.",
                "tools": ["SQL", "PostgreSQL"],
                "tag": "SQL",
                "link": "#",
                "image": "",
                "created_at": datetime.datetime.now().isoformat()
            }
        ]
        write_json(PROJECTS_FILE, demo_projects)
        print("[SEED] Sample projects created.")

    if not os.path.exists(BLOG_FILE):
        demo_posts = [
            {
                "id": 1,
                "title": "Why I Love Statistics",
                "content": "Statistics is the art of learning from data. Every dataset tells a story...",
                "excerpt": "Statistics is the art of learning from data. Every dataset tells a story…",
                "type": "blog",
                "tags": ["statistics", "learning"],
                "created_at": datetime.datetime.now().isoformat()
            },
            {
                "id": 2,
                "title": "A Poem About Numbers",
                "content": "Numbers dance in silence,\npatterns hide in plain sight,\neach data point a heartbeat\nin the rhythm of the night.",
                "excerpt": "Numbers dance in silence, patterns hide in plain sight…",
                "type": "poem",
                "tags": ["poetry", "statistics"],
                "created_at": datetime.datetime.now().isoformat()
            }
        ]
        write_json(BLOG_FILE, demo_posts)
        print("[SEED] Sample blog posts created.")


# =============================================
# START
# =============================================
if __name__ == "__main__":
    seed_demo_data()
    print("\n" + "=" * 45)
    print(f"  {YOUR_NAME}'s Portfolio Backend ✅")
    print("  http://localhost:5000")
    print("  API endpoints:")
    print("    GET  /api/profile")
    print("    GET  /api/projects")
    print("    POST /api/projects")
    print("    GET  /api/blog")
    print("    POST /api/blog")
    print("    POST /api/contact")
    print("=" * 45 + "\n")
    app.run(debug=True, port=5000)
