# regulating_tool.py
import json

class ComplianceChecker:
    def __init__(self):
        self.regulations = self.load_regulations()

    def load_regulations(self):
        with open('regulations.json') as f:
            return json.load(f)

    def check_compliance(self, game_data):
        issues = []
        for regulation in self.regulations:
            if not self.validate_game(game_data, regulation):
                issues.append(f"Compliance issue with: {regulation['description']}")
        return issues or ["Game is compliant"]

    def validate_game(self, game_data, regulation):
        # Basic validation logic (can be expanded)
        return game_data.get('category') == regulation['category']

if __name__ == '__main__':
    checker = ComplianceChecker()
    game_data = {'name': 'Fantasy League', 'category': 'skill'}
    print(checker.check_compliance(game_data))
