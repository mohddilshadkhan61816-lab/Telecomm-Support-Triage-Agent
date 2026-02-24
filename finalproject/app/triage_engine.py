import yaml
import re

class TriageEngine:
    def __init__(self, config_path: str = "config/settings.yaml"):
        with open(config_path, "r") as file:
            self.config = yaml.safe_load(file)
            
        self.priority_scores = {
            "critical": 100,
            "high": 75,
            "medium": 50,
            "low": 25,
            "unclassified": 10
        }

    def _clean_text(self, text: str) -> str:
        return re.sub(r'[^\w\s]', '', text.lower())

    def determine_category(self, text: str) -> str:
        cleaned_text = self._clean_text(text)
        for category, keywords in self.config['categories'].items():
            if any(keyword in cleaned_text for keyword in keywords):
                return category
        return "general_inquiry"

    def determine_priority(self, text: str) -> tuple[str, int]:
        cleaned_text = self._clean_text(text)
        
        # Check from highest to lowest priority
        for priority_level in ["critical", "high", "medium", "low"]:
            keywords = self.config['priority_keywords'].get(priority_level, [])
            if any(keyword in cleaned_text for keyword in keywords):
                return priority_level, self.priority_scores[priority_level]
                
        return "unclassified", self.priority_scores["unclassified"]

    def get_auto_response(self, priority: str) -> str:
        return self.config['automated_responses'].get(
            priority, 
            self.config['automated_responses']['default']
        )

    def analyze_query(self, query_text: str) -> dict:
        category = self.determine_category(query_text)
        priority, score = self.determine_priority(query_text)
        response = self.get_auto_response(priority)
        
        return {
            "category": category,
            "priority": priority,
            "priority_score": score,
            "automated_response": response
        }