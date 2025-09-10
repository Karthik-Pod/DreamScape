"""
Character Agent - Handles character development, personalities, and relationships
Mock version for Day 1 testing
"""

class CharacterAgent:
    def __init__(self):
        self.agent_name = "CharacterAgent"
        self.specialty = "character development and relationships"
    
    def create_main_character(self, story_data):
        """Create a main character based on story requirements"""
        genre = story_data.get("genre", "").lower()
        mood = story_data.get("mood", "").lower()
        idea = story_data.get("idea", "")
        
        character_templates = {
            "fantasy": {
                "archetype": "The Reluctant Hero",
                "background": "From a humble background, discovers hidden power",
                "personality": ["brave", "curious", "initially uncertain"]
            },
            "sci-fi": {
                "archetype": "The Explorer", 
                "background": "Scientist or engineer facing unknown technology",
                "personality": ["analytical", "determined", "adaptable"]
            },
            "romance": {
                "archetype": "The Vulnerable Romantic",
                "background": "Guarded due to past experiences",
                "personality": ["passionate", "cautious", "empathetic"]
            }
        }
        
        template = character_templates.get(genre, {
            "archetype": "The Everyperson",
            "background": "Ordinary person in extraordinary circumstances", 
            "personality": ["relatable", "determined", "growing"]
        })
        
        return {
            "agent": self.agent_name,
            "main_character": {
                "name": "To be determined",
                "archetype": template["archetype"],
                "background": template["background"],
                "personality_traits": template["personality"],
                "character_arc": "Starts uncertain, grows into their role",
                "motivation": self._extract_motivation(idea),
                "strengths": ["quick learner", "loyal to friends"],
                "weaknesses": ["tends to doubt themselves", "acts impulsively"]
            },
            "development_notes": "Character should evolve significantly by story's end"
        }
    
    def suggest_supporting_cast(self, story_data):
        """Suggest supporting characters"""
        return {
            "agent": self.agent_name,
            "supporting_characters": [
                {
                    "role": "The Mentor",
                    "purpose": "Guide protagonist and provide wisdom",
                    "relationship": "Protective but allows growth"
                },
                {
                    "role": "The Ally",
                    "purpose": "Loyal companion who provides different skills",
                    "relationship": "Equal partnership, mutual respect"
                },
                {
                    "role": "The Antagonist", 
                    "purpose": "Primary obstacle to protagonist's goal",
                    "relationship": "Opposing force, may have valid motivations"
                }
            ],
            "relationship_dynamics": "Focus on how characters change each other"
        }
    
    def _extract_motivation(self, idea):
        """Extract character motivation from story idea"""
        if "save" in idea.lower():
            return "to protect what they love"
        elif "find" in idea.lower() or "discover" in idea.lower():
            return "to uncover the truth"
        elif "escape" in idea.lower():
            return "to break free from constraints"
        else:
            return "to overcome the central challenge"

# Global instance  
character_agent = CharacterAgent()
