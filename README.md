![Todoify Logo](./landing/imgs/logo-no-background.png)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

**Todoify** is a powerful and user-friendly task management application designed to help users organize their daily tasks and enhance productivity. With an intuitive interface and robust features, Todoify is suitable for individuals and teams looking to stay organized and accomplish their goals.

## Features

- **Task Management:** Create, edit, and delete tasks effortlessly.
- **Due Dates:** Set due dates for tasks to stay on schedule.
- **Email Notifications:** Receive email reminders for upcoming tasks.
- **User-Friendly Interface:** Intuitive design for a seamless user experience.
- **Cross-Platform Compatibility:** Access Todoify from any device with internet connectivity.

## Getting Started

### Prerequisites

- Python 3.x
- SQLite (or another supported database)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/Todoify.git
    ```

2. Navigate to the project directory:

    ```bash
    cd Todoify
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1. Open `app.py` and configure the following settings:

    - `app.secret_key`: Set a secure secret key for the Flask app.
    - Mail Configuration:
        - `app.config['MAIL_SERVER']`: SMTP server.
        - `app.config['MAIL_PORT']`: Port number.
        - `app.config['MAIL_USE_TLS']`: Set to `True` if using TLS.
        - `app.config['MAIL_USE_SSL']`: Set to `True` if using SSL.
        - `app.config['MAIL_USERNAME']`: Your email address.
        - `app.config['MAIL_PASSWORD']`: Your email password.
        - `app.config['MAIL_DEFAULT_SENDER']`: Default sender email.

2. Create and apply the database migrations:

    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

### Usage

1. Run the application:

    ```bash
    python app.py
    ```

2. Open your web browser and go to [http://localhost:5000](http://localhost:5000).

3. Create an account, add tasks, and experience the simplicity of task management.

## Contributing

Contributions are welcome! Here's how you can contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/new-feature`.
3. Make your changes and commit them: `git commit -m 'Add new feature'`.
4. Push to the branch: `git push origin feature/new-feature`.
5. Submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/): Web framework used.
- [Bootstrap](https://getbootstrap.com/): Frontend framework for a responsive design.

---

**Author:** Divine Ezelibe
