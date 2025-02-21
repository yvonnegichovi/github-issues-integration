import unittest
from src.main import fetch_issues

class TestGitHubIssues(unittest.TestCase):
    def test_fetch_issues(self):
        result = fetch_issues("octocat", "Hello-World", "invalid_token")
        self.assertIn("error", result)

if __name__ == "__main__":
    unittest.main()
