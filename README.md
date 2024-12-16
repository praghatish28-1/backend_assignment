# Email Rule Processor

This project is an email rule processing system that interacts with a Gmail account and a SQLite database to manage and process emails based on predefined rules.

## Project Structure
project_root/
├── src/
│   ├── config/
│   │   ├── __init__.py
│   │   ├── config.json
│   │   ├── credentials.json
│   │   ├── logging_config.json
│   │   ├── rules.json
│   │   └── token.pickle
│   └── services/
│       ├── __init__.py
│       ├── database_manager.py
│       ├── gmail_service.py
│       └── rule_processor.py
└── tests/
    ├── __init__.py
    ├── test_database_manager.py
    ├── test_gmail_service.py
    └── test_rule_processor.py



### Source Files

- **src/services/database_manager.py**: Manages the SQLite database operations.
- **src/services/gmail_service.py**: Handles interactions with the Gmail API.
- **src/services/rule_processor.py**: Processes rules and applies actions to emails.

### Test Files

- **test/test_database_manager.py**: Unit tests for `DatabaseManager`.
- **test/test_gmail_service.py**: Unit tests for `GmailService`.
- **test/test_rule_processor.py**: Unit tests for `RuleProcessor`.

## Setup

### Prerequisites

- Python 3.9+
- `pip` (Python package installer)
- SQLite3
- Google API credentials for Gmail API

### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/email-rule-processor.git
    cd email-rule-processor
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

4. Set up your Google API credentials:

    - Follow the instructions to create a project and enable the Gmail API: https://developers.google.com/gmail/api/quickstart/python
    - Download the `credentials.json` file and place it in the project root directory.

## Usage

### Running the Application

1. Ensure your SQLite database is set up and accessible.
2. Run the main application (if applicable):

    ```sh
    python src/main.py
    ```
   
## Obtaining and Storing Credentials

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing project.
3. In the sidebar, navigate to "APIs & Services" > "Credentials".
4. Click on "Create credentials" and select "OAuth client ID".
5. Select "Desktop app" as the application type.
6. Give your OAuth client a name and click "Create".
7. Click on the download icon next to your newly created OAuth client to download the `credentials.json` file.
8. Place the `credentials.json` file in your project directory.

   Update your `config.json` file to include the path to your `credentials.json` file:
   
      ```json
      {
        "db_path": "path/to/database.db",
        "credentials_path": "path/to/credentials.json",
        "token_path": "path/to/token.pickle",
        "rules_path": "path/to/rules.json",
        "scopes": [
          "https://www.googleapis.com/auth/gmail.modify"
        ],
        "log_file": "path/to/logfile.log"
      }

### Running Tests

To run the unit tests, use the following command:

sh
python -m unittest discover -s test


This will discover and run all the test cases in the `test` directory.

Alternatively, you can run each test file individually:

sh
python -m unittest test.test_database_manager
python -m unittest test.test_gmail_service
python -m unittest test.test_rule_processor


## Project Details

### DatabaseManager

Manages the SQLite database operations, including creating tables, storing emails, and retrieving emails.

### GmailService

Handles interactions with the Gmail API, including authentication, fetching emails, modifying email labels, and getting label IDs.

### RuleProcessor

Processes rules defined in a JSON file and applies actions to emails based on these rules. Supports various predicates and actions.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## Acknowledgments

- [Google Gmail API](https://developers.google.com/gmail/api)
- [SQLite](https://www.sqlite.org/index.html)
- [unittest](https://docs.python.org/3/library/unittest.html)
