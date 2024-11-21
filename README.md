# Hamad - E-commerce Application

Hamad is a Django-based, Dockerized e-commerce application adhering to the M-V-T architecture. This application features user authentication, product management, a shopping cart, and order placement. With responsive design built using Tailwind CSS and an integrated DevOps pipeline, Hamad simplifies deployment and scalability.

## **Table of Contents**
1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Installation Options](#installation-options)
   - [Using Docker](#1-using-docker)
   - [Local Installation](#2-local-installation)
   - [Manual Installation](#3-manual-installation)
4. [Configuration](#configuration)
   - [Environment Variables](#environment-variables)
   - [Database Setup](#database-setup)
   - [Frontend Configuration](#frontend-configuration)
5. [Usage](#usage)
6. [Development Workflow](#development-workflow)
7. [Testing](#testing)
   - [Test Cases](#test-cases)
   - [Running Tests](#running-tests)
8. [Future Work](#future-work)
9. [Known Issues](#known-issues)
10. [Contributing](#contributing)
11. [License](#license)

## **Features**
- **Authentication**: Login and guest session support.
- **Product Management**: Organized products with categories.
- **Cart**: Persistent shopping cart for authenticated and unauthenticated users.
- **Order Management**: Secure order placement with summaries.
- **Responsive UI**: Designed with Tailwind CSS for a modern, mobile-friendly experience.
- **Database Seeding**: Automated seeding with data from an external API.
- **DevOps Ready**: CI/CD pipeline for deployment.

## **Prerequisites**
Before installation, ensure you have:
- **Docker** and **Docker Compose** (for containerized deployment)
- **Python 3.9+**, **pip**, and **virtualenv** (for local development)
- **Node.js** and **Yarn** (optional for manual frontend builds)

## **Installation Options**

### **1. Using Docker**
1. Clone the repository:
   ```bash
   git clone https://github.com/HamadMulti/hamad.git
   cd hamad
   ```

2. Build and run the Docker container:
   ```bash
   docker build -t hamad-app .
   docker run -p 4000:4000 hamad-app
   ```

3. Open the application at `http://127.0.0.1:4000`.

### **2. Local Installation**
1. Clone the repository:
   ```bash
   git clone https://github.com/HamadMulti/hamad.git
   cd hamad
   ```

2. Execute the installation script:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

3. Run the development server:
   ```bash
   python manage.py runserver
   ```

4. Open the application at `http://127.0.0.1:8000`.

### **3. Manual Installation**
1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install and configure Tailwind CSS:
   ```bash
   python manage.py tailwind install  # Installs Tailwind directly
   python manage.py tailwind start   # Starts the development server
   ```

4. Apply database migrations and seed data:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py seed_db_api
   ```

5. Collect static files:
   ```bash
   python manage.py collectstatic
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## **Configuration**

### **Environment Variables**
- Set `DJANGO_SETTINGS_MODULE=hamad.settings` for the environment.
- Ensure `PYTHONUNBUFFERED=1` for consistent logs.

### **Database Setup**
- Default: SQLite.
- For production, configure your database in `settings.py` or through environment variables.

### **Frontend Configuration**
- Install Tailwind CSS directly using:
  ```bash
  python manage.py tailwind install
  ```
- Start Tailwind CSS in development mode:
  ```bash
  python manage.py tailwind start
  ```

## **Usage**
- Access the app at `http://127.0.0.1:8000` (local) or `http://127.0.0.1:4000` (Docker).
- Login to manage your cart and place orders.
- View product details, categories, and your order history.

## **Development Workflow**
1. Modify Django models, views, or templates as needed.
2. Run database migrations for any model changes:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
3. Test the application locally using `runserver`.

## **Testing**
Testing ensures the integrity of the application and its features.

### **Test Cases**
The application includes tests for:
1. **Models**:
   - Validate product and category creation.
   - Check relationships like products belonging to categories.
2. **Views**:
   - Test endpoints for home, product details, cart, and order placement.
3. **Forms**:
   - Validate form submissions and error handling.
4. **Custom Commands**:
   - Verify database seeding functionality.
5. **URLs**:
   - Confirm correct URL mappings for all endpoints.

### **Running Tests**
To run tests locally:
```bash
python manage.py test
```

To measure code coverage:
```bash
coverage run manage.py test
coverage report -m
```

Generate an HTML report:
```bash
coverage html
open htmlcov/index.html
```

## **Future Work**
### **1. Analytics Integration**
- Add dashboards for admin users to track:
  - Sales data.
  - User activity.
  - Product performance.

### **2. Payment Gateway**
- Integrate popular payment providers such as:
  - **Stripe** for credit/debit cards.
  - **PayPal** for secure online transactions.

### **3. Improved Deployment**
- Transition hosting from **Render** to:
  - **DigitalOcean**: Cost-effective and scalable deployment.
  - **AWS**: Advanced cloud solutions for high scalability and reliability.

### **4. Enhanced Frontend**
- Build dynamic, user-friendly interfaces using advanced Tailwind components.

## **Known Issues**
- **Docker Permission Issues**: Ensure correct file permissions for `static` and `db.sqlite3`.
- **Tailwind Errors**: Rebuild assets after updating CSS:
  ```bash
  python manage.py tailwind build
  ```
- **Database Errors**: Verify migration status:
  ```bash
  python manage.py showmigrations
  ```

## **Contributing**
We welcome contributions! Fork the repository, create a feature branch, and submit a pull request. Ensure changes are tested locally.

## **License**
This project is licensed under the MIT License. See the `LICENSE` file for details.

Let me know if additional adjustments or details are needed!