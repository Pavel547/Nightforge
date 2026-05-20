# Nightforge - Dark Fantasy Gothic Clothing Shop
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-ff1709?logo=django&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?logo=django&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-38B2AC?logo=tailwind-css&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?logo=postgresql&logoColor=white)
![Stripe](https://img.shields.io/badge/Stripe-008CDD?logo=stripe&logoColor=white)
![Cloudinary](https://img.shields.io/badge/Cloudinary-3448C5?logo=cloudinary&logoColor=white)
![Deploy](https://img.shields.io/badge/Deploy-Render-purple)

---

## 📌 Description

Nightforge is a full-stack e-commerce application built with Django and Django REST Framework, 
focused on clean API design, database optimization, and secure order processing.

---

## 🚀 Features

- Custom user authentication (register, login, logout, profile management)
- REST API with filtering, search, ordering and pagination
- Product catalog with search, filtering and sorting
- Shopping cart system
- Order creation and management
- Stripe payment integration (with webhook handling)
- Email notifications after successful orders
- Image storage using Cloudinary

---

## ⚙️ API Features

- Pagination (LimitOffsetPagination)
- Filtering (DjangoFilterBackend, Custom filters)
- Search & Ordering
- Custom permissions (admin vs user)

---

## 🛠 Tech Stack

- **Backend:** Django, Python  
- **API:** Django REST Framework
- **Database:** PostgreSQL  
- **Frontend:** HTML, CSS (Tailwind CSS)  
- **Payments:** Stripe  
- **Media storage:** Cloudinary  
- **Email:** Resend / SMTP  
- **Deployment:** Render  

---

## 🎨 Design
UI design inspired by a free [Figma template](https://www.figma.com/design/Uz5XzkAousMHKxFudsJ5Mz/UX---clothing-E-shop---Streetwear-style--Community-?node-id=7-3&t=cs8DU3xKoSRnrt8k-0).

---

## 🌐 Live Demo
https://nightforge.onrender.com/

---

## 📂 Project Structure
```Markdown
Dark-fantasy-gothic-clothing-shop/
├── shop/ # Django project(settings, urls, wsgi)
├── main/ # Main app (homepage, catalog, product details)
├── users/ # Authentication and user profiles
├── cart/ # Shopping cart logiс
├── orders/ # Order management
├── payment/ # Stripe integration and webhooks
├── templates/ # HTML templates
├── static/ # Static files (CSS, JS, images)
├── media/ # Media files (Images)
├── manage.py
├── .env
└── requirements.txt
```

---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone <repo_url>
cd <project-folder>
```

### 2. Create virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup environment variables
Create '.env' and add:
```env
SC_KEY = your_secret_key
DEBUG = True or False

DB_NAME = your_postgresql_db_name
DB_USER = your_postgresql_user
PASSWORD = your_db_password
DB_HOST = your_db_host
DB_PORT = your_db_port

STRIPE_API_KEY = your_stripe_api_key
STRIPE_WEBHOOK = your_stripe_webhook

EMAIL_HOST_USER = your_gmail
EMAIL_HOST_PASSWORD = your_gmail_app_password

CLOUDINARY_CLOUD_NAME = your_cloud_name
CLOUDINARY_API_KEY = your_api_key
CLOUDINARY_API_SECRET = your_api_secret

RESEND_API_KEY = your_resend_api_key

# Optional
DJANGO_LOG_LEVEL = your_log_level
```

### 5. Apply migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Collect static files
```bash
python manage.py collectstatic
```

### 7. Run server
```bash
python manage.py runserver
```
---

## ⚠️ Notes
To send emails in production, you need a verified domain for Resend.
SMTP (Gmail) can be used for development purposes.

---

## 🔗 API Endpoints

### Products
GET /api/main/products/  
GET /api/main/products/{id}/  

Supports:
- search
- filtering
- ordering
- pagination

---

### Orders
GET /api/orders/orders/  
GET /api/orders/orders/{id}/  

- Authenticated users can view their own orders  
- Admin users can view all orders  

---

### Authentication
POST /api/users/register/  
POST /api-auth/login/  
POST /api-auth/logout/

Authentication is handled using Django session-based authentication,
which is suitable for server-rendered applications using Django templates.

### Profile
GET /api/users/profile/

---

## 📸 Screenshots
<img width="1915" height="920" alt="obrazek" src="https://github.com/user-attachments/assets/b11be553-e1ec-4918-80a8-80728c7580ed" />
<img width="1912" height="1079" alt="obrazek" src="https://github.com/user-attachments/assets/5b5b8b3f-f6e8-45d7-987f-fe79aa9d494b" />
<img width="1917" height="914" alt="obrazek" src="https://github.com/user-attachments/assets/ee61e3c6-4a23-4df4-8b37-e91061f7f599" />
<img width="1918" height="915" alt="obrazek" src="https://github.com/user-attachments/assets/e391885f-d824-4804-b645-0782297bc9d4" />

---

## 📄 License
This project is for CV.
