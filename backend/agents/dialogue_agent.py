"""
Dialogue Agent - Handles dialogue, voice, and character interactions
Mock version for Day 1 testing
"""

class DialogueAgent:
    def __init__(self):
        self.agent_name = "DialogueAgent"
        self.specialty = "dialogue and character voice"
    
    def analyze_dialogue_style(self, story_data):
        """Suggest dialogue style based on genre and mood"""
        genre = story_data.get("genre", "").lower()
        mood = story_data.get("mood", "").lower()
        
        style_guide = {
            "fantasy": {
                "tone": "Elevated but accessible",
                "vocabulary": "Mix of modern and archaic terms",
                "rhythm": "Flowing, descriptive"
            },
            "sci-fi": {
                "tone": "Precise and technical when needed",
                "vocabulary": "Scientific terms balanced with emotion",
                "rhythm": "Efficient, purposeful"
            },
            "romance": {
                "tone": "Emotional and intimate",
                "vocabulary": "Expressive, metaphorical",
                "rhythm": "Varies with emotional intensity"
            },
            "mystery": {
                "tone": "Tense and revealing",
                "vocabulary": "Careful word choices, subtext",
                "rhythm": "Builds suspense through pacing"
            }
        }
        
        default_style = {
            "tone": "Natural and engaging",
            "vocabulary": "Clear and accessible",
            "rhythm": "Conversational flow"
        }
        
        style = style_guide.get(genre, default_style)
        
        return {
            "agent": self.agent_name,
            "dialogue_style": style,
            "guidelines": [
                "Each character should have a distinct voice",
                "Dialogue should reveal character and advance plot",
                "Balance exposition with natural conversation",
                "Use subtext to add depth"
            ],
            "mood_adjustments": self._adjust_for_mood(mood)
        }
    
    def create_sample_dialogue(self, story_data):
        """Create sample dialogue based on the story"""
        title = story_data.get("title", "Your Story")
        
        return {
            "agent": self.agent_name,
            "sample_scene": f"Opening dialogue for '{title}'",
            "dialogue": [
                {
                    "character": "Protagonist",
                    "line": "I never expected things to change so quickly."
                },
                {
                    "character": "Supporting Character", 
                    "line": "Change is the only constant. The question is: are you ready for what comes next?"
                },
                {
                    "character": "Protagonist",
                    "line": "I suppose I have to be."
                }
            ],
            "notes": "This establishes the protagonist's uncertainty and hints at upcoming challenges"
        }
    
    def _adjust_for_mood(self, mood):
        """Adjust dialogue suggestions based on mood"""
        mood_adjustments = {
            "dark": "Use shorter sentences, more pauses, underlying tension",
            "epic": "Grand language, inspirational moments, building speeches",
            "lighthearted": "Playful banter, humor, optimistic outlook",
            "mysterious": "Cryptic hints, things left unsaid, layered meanings"
        }
        
        return mood_adjustments.get(mood, "Match dialogue to the story's emotional tone")

# Global instance
dialogue_agent = DialogueAgent()
