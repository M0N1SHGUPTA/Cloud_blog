# FastAPI Blog - Learning Notes

## Request-Response Cycle

### 1. Pure REST API Flow (`/api/posts`)
```
BROWSER / MOBILE / POSTMAN
         |
         | GET /api/posts
         |
         v
      FastAPI
         |
         |── validates request
         |── queries DATABASE
         |── converts DB data → JSON
         |
         v
      returns JSON
      {
        "posts": [...],
        "total": 10
      }
         |
         v
BROWSER / MOBILE / POSTMAN
(does whatever it wants with JSON)
```

---

### 2. Jinja2 HTML Flow (`/posts`)
```
BROWSER
   |
   | GET /posts
   |
   v
FastAPI
   |
   |── queries DATABASE
   |── puts data in Python dict
   |   {"posts": posts, "user": user}
   |
   v
Jinja2 Template
   |
   |── injects dict data into HTML
   |   <h1>{{ user.name }}</h1>
   |── renders complete HTML string
   |
   v
FastAPI
   |
   |── wraps HTML in HTTP response
   |
   v
BROWSER
(receives complete HTML page, displays it)
```

---

### 3. How Jinja2 Frontend calls REST API (the full picture)
```
BROWSER
   |
   |── 1. loads HTML page from /posts  (Jinja2 route)
   |
   v
HTML Page loads in browser
   |
   |── 2. JavaScript on the page runs
   |── 3. JS calls fetch("/api/posts")  (REST API route)
   |
   v
FastAPI /api/posts
   |
   |── returns JSON
   |
   v
JavaScript receives JSON
   |
   |── updates the HTML page dynamically
   |
   v
BROWSER shows updated content
```

---

### 4. Authenticated Request Flow (JWT)
```
BROWSER
   |
   | Request + JWT token in cookie/header
   |
   v
FastAPI
   |
   |── 1. extracts JWT token from request
   |── 2. verifies token → decodes user_id
   |── 3. queries DB for user data
   |── 4. processes request
   |
   v
returns response (JSON or HTML)
```

---

## Project Structure (Corey's Final Project)
```
FastAPI Project
├── /api/posts/*   → REST API → returns JSON  (usable by React/Mobile/anyone)
├── /api/users/*   → REST API → returns JSON
│
├── /              → Jinja2 → returns HTML (the frontend)
├── /login         → Jinja2 → returns HTML
└── /register      → Jinja2 → returns HTML
```

The Jinja2 frontend is just ONE consumer of the REST API.
React, mobile apps, or Postman can call the same `/api/` routes.

---

## Key Concepts

| Term | What it means |
|------|--------------|
| REST API | Returns JSON, usable by any client |
| Jinja2 | Server-side HTML rendering |
| JWT | Token stored in cookies for auth |
| Python dict | What FastAPI passes to Jinja2 |
| JSON | What FastAPI returns to REST clients |
| `request` object | Raw HTTP request (URL, cookies, headers) |
