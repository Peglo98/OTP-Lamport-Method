# OTP Lamport Method

Simple Python Flask application demonstrating Lamport's one-time password (OTP) method using hash chains.

## Project Structure

- `app.py`: Main Flask application.
- `templates/`: HTML templates for user interface.

## Requirements

- Python 3.6+
- Flask

## Installation

```bash
git clone https://github.com/Peglo98/OTP-Lamport-Method.git
cd OTP-Lamport-Method
pip install Flask
```

## Usage

```bash
python app.py
```

Then open your web browser and navigate to `http://127.0.0.1:5000/`.

1. Enter a secret seed and the desired number of one-time passwords.
2. The application will generate a chain of OTPs.
3. Use the OTPs in reverse order for secure authentication.

## Project Workflow

1. **Generate**: The server uses a hash function to create a sequence of passwords from an initial seed.
2. **Validate**: Clients present the next password in the chain; the server hashes it and compares it to the stored value.
3. **Consume**: Each password is used only once, ensuring one-time usage.


