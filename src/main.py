import logging
from src.config import config_manager, logging_config
from src.services import database_manager, gmail_service, rule_processor



def main():
    config_file = 'src/config.json'
    config = config_manager.ConfigManager(config_file)

    db_path = config.get('db_path')
    credentials_path = config.get('credentials_path')
    token_path = config.get('token_path')
    rules_path = config.get('rules_path')
    scopes = config.get('scopes')
    log_file = config.get('log_file')

    logging_config.setup_logging(log_file)

    db_manager = database_manager.DatabaseManager(db_path)
    db_manager.create_tables()
    gmail_service_obj = gmail_service.GmailService(credentials_path, token_path, scopes)

    logging.info('Fetching emails...')
    emails = gmail_service_obj.fetch_emails()
    logging.info('Emails fetched...')
    logging.info('Storing into db')
    for email in emails:
        db_manager.store_email(*email)
    logging.info('Successfully written into db')

    rule_processor_obj = rule_processor.RuleProcessor(db_manager, gmail_service_obj, rules_path)
    logging.info('Processing rules')
    rule_processor_obj.apply_rules()


if __name__ == '__main__':
    main()
