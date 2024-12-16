import unittest
from unittest.mock import patch, MagicMock
from src.services.rule_processor import RuleProcessor

class TestRuleProcessor(unittest.TestCase):
    @patch('src.services.rule_processor.open', new_callable=unittest.mock.mock_open, read_data='[{"description": "Test Rule", "if": "all", "conditions": [{"field_name": "subject", "predicate": "contains", "value": "test"}], "perform_actions": ["mark_as_read"]}]')
    def test_load_rules(self, mock_open):
        db_manager = MagicMock()
        gmail_service = MagicMock()
        rule_processor = RuleProcessor(db_manager, gmail_service, 'rules.json')
        rules = rule_processor.load_rules()
        self.assertEqual(len(rules), 1)
        self.assertEqual(rules[0]['description'], 'Test Rule')

    def test_validate_rules(self):
        db_manager = MagicMock()
        gmail_service = MagicMock()
        rule_processor = RuleProcessor(db_manager, gmail_service, 'rules.json')
        rules = [{"description": "Test Rule", "if": "all", "conditions": [{"field_name": "subject", "predicate": "contains", "value": "test"}], "perform_actions": ["mark_as_read"]}]
        rule_processor.validate_rules(rules)

    @patch('src.services.rule_processor.RuleProcessor.load_rules')
    def test_apply_rules(self, mock_load_rules):
        db_manager = MagicMock()
        gmail_service = MagicMock()
        rule_processor = RuleProcessor(db_manager, gmail_service, 'rules.json')
        mock_load_rules.return_value = [{"description": "Test Rule", "if": "all", "conditions": [{"field_name": "subject", "predicate": "contains", "value": "test"}], "perform_actions": ["mark_as_read"]}]
        db_manager.get_emails.return_value = [{'id': '1', 'From': 'sender@example.com', 'Subject': 'test subject', 'Body': 'Body', 'Date received': 1234567890}]
        rule_processor.apply_rules()
        gmail_service.modify_email_labels.assert_called_once_with('1', [], ['UNREAD'])

    def test_evaluate_rule(self):
        db_manager = MagicMock()
        gmail_service = MagicMock()
        rule_processor = RuleProcessor(db_manager, gmail_service, 'rules.json')
        rule = {"description": "Test Rule", "if": "all", "conditions": [{"field_name": "subject", "predicate": "contains", "value": "test"}], "perform_actions": ["mark_as_read"]}
        email = {'id': '1', 'From': 'sender@example.com', 'Subject': 'test subject', 'Body': 'Body', 'Date received': 1234567890}
        result = rule_processor.evaluate_rule(rule, email)
        self.assertTrue(result)

    @patch('src.services.rule_processor.RuleProcessor.evaluate_rule')
    def test_apply_actions(self, mock_evaluate_rule):
        db_manager = MagicMock()
        gmail_service = MagicMock()
        rule_processor = RuleProcessor(db_manager, gmail_service, 'rules.json')
        rule = {"description": "Test Rule", "if": "all", "conditions": [{"field_name": "subject", "predicate": "contains", "value": "test"}], "perform_actions": ["mark_as_read"]}
        email = {'id': '1', 'From': 'sender@example.com', 'Subject': 'test subject', 'Body': 'Body', 'Date received': 1234567890}
        mock_evaluate_rule.return_value = True
        rule_processor.apply_actions(rule, email)
        gmail_service.modify_email_labels.assert_called_once_with('1', [], ['UNREAD'])

if __name__ == '__main__':
    unittest.main()