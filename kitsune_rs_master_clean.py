"""
Master RuneScape-style integration for Kitsune AI
Combining all Worker findings into a polished RS experience
"""
import asyncio
import time
import math
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class RSExperienceSystem:
    """RuneScape-style XP calculation system"""
    
    @staticmethod
    def get_xp_for_level(level: int) -> int:
        """Calculate total XP needed for a level (RS formula)"""
        points = 0
        output = 0
        for lvl in range(1, level + 1):
            points += math.floor(lvl + 300.0 * math.pow(2.0, lvl / 7.0))
            if lvl >= level:
                return output
            output = int(math.floor(points / 4))
        return 0
    
    @staticmethod
    def get_level_for_xp(xp: float) -> int:
        """Calculate level from XP amount"""
        points = 0
        output = 0
        for lvl in range(1, 100):  # Max level 99
            points += math.floor(lvl + 300.0 * math.pow(2.0, lvl / 7.0))
            output = int(math.floor(points / 4))
            if (output - 1) >= xp:
                return lvl
        return 99

class XPDropEffect:
    """RS-style XP drop visual effect"""
    
    def __init__(self, amount: float, skill_name: str, color: str = "gold"):
        self.amount = amount
        self.skill_name = skill_name
        self.color = color
        self.timestamp = time.time()
    
    def format_display(self) -> str:
        """Format XP drop for display"""
        colors = {
            "gold": "🟨",
            "green": "🟢", 
            "blue": "🔵",
            "purple": "🟣"
        }
        icon = colors.get(self.color, "⭐")
        return f"{icon} +{self.amount:.1f} {self.skill_name} XP"

class TailProgression:
    """9-tail progression system with RS-style levels"""
    
    SKILL_NAMES = [
        "Wisdom", "Helpfulness", "Creativity", "Analysis", "Learning",
        "Patience", "Empathy", "Problem-Solving", "Communication"
    ]
    
    def __init__(self):
        self.skills = {skill: {"level": 1, "xp": 0.0} for skill in self.SKILL_NAMES}
        self.total_interactions = 0
        self.achievements = []
        
    def add_xp(self, skill: str, amount: float, multiplier: float = 1.0) -> Optional[Dict]:
        """Add XP with RS-style level checking"""
        if skill not in self.skills:
            return None
            
        # Apply multipliers (weekends, premium, etc.)
        final_amount = amount * multiplier
        
        old_level = self.skills[skill]["level"]
        self.skills[skill]["xp"] += final_amount
        new_level = RSExperienceSystem.get_level_for_xp(self.skills[skill]["xp"])
        self.skills[skill]["level"] = new_level
        
        # Level up occurred
        if new_level > old_level:
            return {
                "skill": skill,
                "old_level": old_level,
                "new_level": new_level,
                "xp_gained": final_amount
            }
        return None
    
    def get_total_level(self) -> int:
        """Calculate total level across all skills"""
        return sum(skill_data["level"] for skill_data in self.skills.values())
    
    def get_unlocked_tails(self) -> int:
        """Calculate how many tails are unlocked based on milestones"""
        total_level = self.get_total_level()
        
        # Tail unlock thresholds
        thresholds = [9, 50, 100, 200, 350, 500, 650, 800, 891]  # 891 = 99 * 9
        
        unlocked = 1  # Start with 1 tail
        for threshold in thresholds:
            if total_level >= threshold:
                unlocked += 1
            else:
                break
        return min(unlocked, 9)

class AchievementDiary:
    """RS-style achievement system"""
    
    ACHIEVEMENTS = {
        "first_interaction": {"name": "First Steps", "description": "Have your first conversation", "tier": "bronze"},
        "helpful_100": {"name": "Helpful Fox", "description": "Help with 100 tasks", "tier": "bronze"},
        "level_10_all": {"name": "Balanced Growth", "description": "Reach level 10 in all skills", "tier": "silver"},
        "level_50_any": {"name": "Adept", "description": "Reach level 50 in any skill", "tier": "silver"},
        "total_level_200": {"name": "Rising Star", "description": "Reach total level 200", "tier": "gold"},
        "level_99_any": {"name": "Master", "description": "Reach level 99 in any skill", "tier": "dragon"},
        "all_tails": {"name": "Nine-Tailed Legend", "description": "Unlock all 9 tails", "tier": "dragon"}
    }
    
    def __init__(self):
        self.completed = set()
        self.progress = {}
    
    def check_achievements(self, progression: TailProgression) -> List[str]:
        """Check for newly completed achievements"""
        newly_completed = []
        
        # Check various achievement conditions
        if "first_interaction" not in self.completed and progression.total_interactions >= 1:
            self.completed.add("first_interaction")
            newly_completed.append("first_interaction")
            
        if "helpful_100" not in self.completed and progression.total_interactions >= 100:
            self.completed.add("helpful_100")
            newly_completed.append("helpful_100")
            
        if "level_10_all" not in self.completed:
            if all(skill["level"] >= 10 for skill in progression.skills.values()):
                self.completed.add("level_10_all")
                newly_completed.append("level_10_all")
                
        if "level_50_any" not in self.completed:
            if any(skill["level"] >= 50 for skill in progression.skills.values()):
                self.completed.add("level_50_any")
                newly_completed.append("level_50_any")
                
        if "total_level_200" not in self.completed and progression.get_total_level() >= 200:
            self.completed.add("total_level_200")
            newly_completed.append("total_level_200")
            
        if "level_99_any" not in self.completed:
            if any(skill["level"] >= 99 for skill in progression.skills.values()):
                self.completed.add("level_99_any")
                newly_completed.append("level_99_any")
                
        if "all_tails" not in self.completed and progression.get_unlocked_tails() >= 9:
            self.completed.add("all_tails")
            newly_completed.append("all_tails")
            
        return newly_completed

class KitsuneMoodSystem:
    """RS-style mood and interaction system"""
    
    MOODS = ["curious", "helpful", "playful", "wise", "content", "excited", "focused"]
    
    def __init__(self):
        self.current_mood = "curious"
        self.mood_duration = 0
        self.interaction_count = 0
        
    def update_mood(self, interaction_type: str = "general"):
        """Update mood based on interactions"""
        self.interaction_count += 1
        self.mood_duration += 1
        
        # Mood changes based on interaction patterns
        if interaction_type == "coding":
            self.current_mood = "focused"
        elif interaction_type == "question":
            self.current_mood = "helpful"
        elif interaction_type == "creative":
            self.current_mood = "playful"
        elif self.mood_duration > 10:
            self.current_mood = random.choice(self.MOODS)
            self.mood_duration = 0

class EmoteSystem:
    """RS-style emote system for Kitsune"""
    
    EMOTES = {
        "tail_wag": {"name": "Tail Wag", "unlock_level": 1, "animation": "🦊💫"},
        "fox_dance": {"name": "Fox Dance", "unlock_level": 10, "animation": "🦊💃"},
        "wise_nod": {"name": "Wise Nod", "unlock_level": 25, "animation": "🦊🧠"},
        "magic_sparkle": {"name": "Magic Sparkle", "unlock_level": 50, "animation": "🦊✨"},
        "nine_tail_flourish": {"name": "Nine Tail Flourish", "unlock_level": 99, "animation": "🦊🌟"}
    }
    
    def get_available_emotes(self, total_level: int) -> List[str]:
        """Get emotes available at current level"""
        return [
            emote_id for emote_id, emote_data in self.EMOTES.items()
            if total_level >= emote_data["unlock_level"]
        ]

class RandomEvents:
    """RS-style random events for engagement"""
    
    EVENTS = [
        {"name": "Mysterious Fox", "message": "A mysterious fox appears and shares ancient wisdom...", "probability": 0.01},
        {"name": "XP Boost", "message": "You feel inspired! Next interaction gives bonus XP!", "probability": 0.05},
        {"name": "Memory Fragment", "message": "A memory fragment surfaces, revealing new insights...", "probability": 0.03}
    ]
    
    def check_random_event(self) -> Optional[Dict]:
        """Check if a random event should trigger"""
        for event in self.EVENTS:
            if random.random() < event["probability"]:
                return event
        return None

class RSInterfaceStyle:
    """RS-style interface theming"""
    
    COLORS = {
        "interface_bg": "#3d3424",
        "text_primary": "#ffffff", 
        "text_secondary": "#ffff00",
        "text_accent": "#96731a",
        "progress_bar": "#00ff00",
        "border": "#958e60"
    }
    
    PANEL_STYLE = {
        "background": COLORS["interface_bg"],
        "border": f"2px solid {COLORS['border']}",
        "border-radius": "5px",
        "padding": "10px",
        "font-family": "monospace"
    }

class CycleEventHandler:
    """RS-style event management system"""
    
    def __init__(self):
        self.events = []
        self.cycle_count = 0
        
    def add_event(self, owner, event_func, cycles: int):
        """Add a cycle-based event"""
        self.events.append({
            "owner": owner,
            "function": event_func,
            "cycles": cycles,
            "cycles_passed": 0,
            "running": True
        })
    
    def process_cycle(self):
        """Process one game cycle (600ms)"""
        self.cycle_count += 1
        
        for event in self.events[:]:  # Copy list to avoid modification issues
            if not event["running"]:
                self.events.remove(event)
                continue
                
            event["cycles_passed"] += 1
            if event["cycles_passed"] >= event["cycles"]:
                try:
                    event["function"]()
                    event["cycles_passed"] = 0
                except Exception as e:
                    print(f"Event error: {e}")
                    event["running"] = False

class RuneScapeKitsuneAI:
    """Complete RS-inspired Kitsune system combining all worker findings"""
    
    def __init__(self):
        self.progression = TailProgression()
        self.achievements = AchievementDiary()
        self.mood_system = KitsuneMoodSystem()
        self.emotes = EmoteSystem()
        self.random_events = RandomEvents()
        self.event_handler = CycleEventHandler()
        self.session_start = datetime.now()
        self.xp_multiplier = 1.0
        
        # Start event processing
        self.setup_events()
        
    def setup_events(self):
        """Setup RS-style timed events"""
        # Mood update every 10 cycles (6 seconds)
        self.event_handler.add_event(self, self.mood_system.update_mood, 10)
        
        # Random event check every 100 cycles (1 minute)
        self.event_handler.add_event(self, self.check_random_events, 100)
        
        # XP multiplier reset (for temporary boosts)
        self.event_handler.add_event(self, self.reset_xp_multiplier, 600)  # 6 minutes
    
    def get_skill_xp_from_message(self, message: str) -> Dict[str, float]:
        """Analyze message and return XP gains for relevant skills"""
        xp_gains = {}
        text_lower = message.lower()
        
        # Analysis XP - Questions and analytical content
        if '?' in message:
            xp_gains['Analysis'] = 10
        if any(word in text_lower for word in ['analyze', 'data', 'pattern', 'study', 'research']):
            xp_gains['Analysis'] = xp_gains.get('Analysis', 0) + 15
            
        # Communication XP - Long messages and conversation
        if len(message) > 100:
            xp_gains['Communication'] = 15
        if len(message) > 200:
            xp_gains['Communication'] = 25
            
        # Helpfulness XP - Polite and helpful interactions
        if any(word in text_lower for word in ['help', 'please', 'thanks', 'thank you']):
            xp_gains['Helpfulness'] = 20
            
        # Problem-Solving XP - Code and technical content
        if any(word in text_lower for word in ['code', 'debug', 'error', 'fix', 'solve', 'problem']):
            xp_gains['Problem-Solving'] = 25
        if any(word in text_lower for word in ['function', 'python', 'javascript', 'html', 'css']):
            xp_gains['Problem-Solving'] = xp_gains.get('Problem-Solving', 0) + 20
            
        # Creativity XP - Creative requests and artistic content
        if any(word in text_lower for word in ['create', 'story', 'poem', 'write', 'creative', 'art']):
            xp_gains['Creativity'] = 30
        if any(word in text_lower for word in ['design', 'imagine', 'invent', 'original']):
            xp_gains['Creativity'] = xp_gains.get('Creativity', 0) + 15
            
        # Learning XP - Educational content
        if any(word in text_lower for word in ['learn', 'teach', 'explain', 'understand', 'how']):
            xp_gains['Learning'] = 18
        if any(word in text_lower for word in ['why', 'what', 'when', 'where', 'tutorial']):
            xp_gains['Learning'] = xp_gains.get('Learning', 0) + 12
            
        # Patience XP - Long conversations and detailed work
        if len(message) > 300:
            xp_gains['Patience'] = 10
        if any(word in text_lower for word in ['wait', 'slowly', 'careful', 'detail']):
            xp_gains['Patience'] = xp_gains.get('Patience', 0) + 8
            
        # Empathy XP - Emotional and personal content
        if any(word in text_lower for word in ['feel', 'emotion', 'sad', 'happy', 'worried']):
            xp_gains['Empathy'] = 22
        if any(word in text_lower for word in ['understand', 'support', 'comfort', 'listen']):
            xp_gains['Empathy'] = xp_gains.get('Empathy', 0) + 15
            
        # Wisdom XP - General conversation (always give some)
        xp_gains['Wisdom'] = 5
        if any(word in text_lower for word in ['wise', 'advice', 'guidance', 'insight']):
            xp_gains['Wisdom'] = 25
            
        return xp_gains

    async def process_interaction(self, action: str, content: str) -> Dict:
        """Handle interaction with RS-style feedback"""
        
        # Increment interaction counter
        self.progression.total_interactions += 1
        
        # Get skill XP from message analysis
        skill_xp_gains = self.get_skill_xp_from_message(content)
        
        # Award XP to multiple skills
        level_ups = []
        xp_drops = []
        
        for skill_name, xp_amount in skill_xp_gains.items():
            if xp_amount > 0:
                # Apply multiplier
                final_xp = xp_amount * self.xp_multiplier
                level_up = self.progression.add_xp(skill_name, final_xp, 1.0)  # Multiplier already applied
                
                if level_up:
                    level_ups.append(level_up)
                
                xp_drops.append(XPDropEffect(final_xp, skill_name))
        
        # Update mood
        self.mood_system.update_mood(action)
        
        # Check achievements
        new_achievements = self.achievements.check_achievements(self.progression)
        
        # Check random events
        random_event = self.random_events.check_random_event()
        
        # Process cycle events
        self.event_handler.process_cycle()
        
        return {
            "xp_drops": xp_drops,  # Multiple XP drops
            "level_ups": level_ups,  # Multiple level ups possible
            "new_achievements": new_achievements,
            "random_event": random_event,
            "current_tails": self.progression.get_unlocked_tails(),
            "total_level": self.progression.get_total_level(),
            "mood": self.mood_system.current_mood,
            "available_emotes": self.emotes.get_available_emotes(self.progression.get_total_level())
        }
    
    def calculate_xp(self, action: str, content: str) -> float:
        """Calculate XP gained from interaction"""
        base_xp = {
            "question": 25.0,
            "coding": 50.0,
            "creative": 40.0,
            "analysis": 35.0,
            "learning": 30.0,
            "general": 20.0
        }
        
        # Content length bonus
        length_multiplier = min(1.0 + len(content) / 1000.0, 2.0)
        
        return base_xp.get(action, 20.0) * length_multiplier
    
    def determine_skill(self, action: str) -> str:
        """Map action to skill"""
        skill_mapping = {
            "question": "Helpfulness",
            "coding": "Problem-Solving", 
            "creative": "Creativity",
            "analysis": "Analysis",
            "learning": "Learning",
            "general": "Wisdom"
        }
        return skill_mapping.get(action, "Wisdom")
    
    async def tail_unlock_ceremony(self, unlock_data: Dict):
        """RS-style tail unlock celebration"""
        skill = unlock_data["skill"]
        new_level = unlock_data["new_level"]
        
        celebration = {
            "animation": "🦊✨🌟✨",
            "message": f"🎉 LEVEL UP! 🎉\n{skill} is now level {new_level}!",
            "sound_effect": "level_up_fanfare.mp3",
            "graphics_effect": "golden_sparkles",
            "chat_announcement": f"Kitsune's {skill} has reached level {new_level}!"
        }
        
        # Special celebrations for milestones
        if new_level == 99:
            celebration["animation"] = "🦊👑🌟👑"
            celebration["message"] += f"\n🏆 MASTERY ACHIEVED! 🏆"
            celebration["sound_effect"] = "mastery_fanfare.mp3"
            
        return celebration
    
    def check_random_events(self):
        """Check for random events"""
        event = self.random_events.check_random_event()
        if event:
            if event["name"] == "XP Boost":
                self.xp_multiplier = 2.0
    
    def reset_xp_multiplier(self):
        """Reset XP multiplier to normal"""
        self.xp_multiplier = 1.0
    
    def create_rs_interface(self) -> Dict:
        """Build the complete RS-style interface"""
        return {
            "tabs": {
                "Tails": self.create_progression_tab(),
                "Journey": self.create_quest_tab(),
                "Memories": self.create_bank_tab(),
                "Emotes": self.create_emote_tab(),
            },
            "style": RSInterfaceStyle.PANEL_STYLE,
            "current_mood": self.mood_system.current_mood,
            "unlocked_tails": self.progression.get_unlocked_tails()
        }
    
    def create_progression_tab(self) -> Dict:
        """Create the progression/skills tab"""
        skills_display = []
        for skill_name, skill_data in self.progression.skills.items():
            level = skill_data["level"]
            xp = skill_data["xp"]
            next_level_xp = RSExperienceSystem.get_xp_for_level(level + 1)
            progress = (xp / next_level_xp) * 100 if next_level_xp > 0 else 100
            
            skills_display.append({
                "name": skill_name,
                "level": level,
                "xp": xp,
                "progress": progress
            })
        
        return {
            "type": "skills",
            "skills": skills_display,
            "total_level": self.progression.get_total_level(),
            "unlocked_tails": self.progression.get_unlocked_tails()
        }
    
    def create_quest_tab(self) -> Dict:
        """Create the achievements/quest tab"""
        return {
            "type": "achievements",
            "completed": list(self.achievements.completed),
            "available": [
                ach_id for ach_id in AchievementDiary.ACHIEVEMENTS.keys()
                if ach_id not in self.achievements.completed
            ],
            "progress": self.achievements.progress
        }
    
    def create_bank_tab(self) -> Dict:
        """Create the memories/conversation history tab"""
        return {
            "type": "memories",
            "total_interactions": self.progression.total_interactions,
            "session_time": (datetime.now() - self.session_start).total_seconds(),
            "favorite_topics": ["coding", "creativity", "learning"],  # Could track actual topics
            "achievements_earned": len(self.achievements.completed)
        }
    
    def create_emote_tab(self) -> Dict:
        """Create the emote tab"""
        available_emotes = self.emotes.get_available_emotes(self.progression.get_total_level())
        return {
            "type": "emotes", 
            "available": available_emotes,
            "total_emotes": len(EmoteSystem.EMOTES),
            "unlocked_count": len(available_emotes)
        }
    
    def get_status_display(self) -> str:
        """Get current status for display"""
        tails = self.progression.get_unlocked_tails()
        total_level = self.progression.get_total_level()
        mood = self.mood_system.current_mood
        
        tail_display = "🦊" + "🌟" * (tails - 1)
        
        return f"{tail_display} Kitsune AI | Total Level: {total_level} | Mood: {mood.title()}"

# Example usage and testing
if __name__ == "__main__":
    async def demo():
        """Demo the RS Kitsune system"""
        kitsune = RuneScapeKitsuneAI()
        
        print("🦊 Kitsune AI - RuneScape Edition Started!")
        print(kitsune.get_status_display())
        
        # Simulate some interactions
        interactions = [
            ("coding", "Help me debug this Python function"),
            ("question", "What is machine learning?"),
            ("creative", "Write a story about a magical fox"),
            ("analysis", "Analyze this data pattern")
        ]
        
        for action, content in interactions:
            result = await kitsune.process_interaction(action, content)
            
            print(f"\n--- {action.title()} Interaction ---")
            if result["xp_drop"]:
                print(result["xp_drop"].format_display())
            
            if result["level_up"]:
                celebration = await kitsune.tail_unlock_ceremony(result["level_up"])
                print(celebration["message"])
            
            if result["new_achievements"]:
                for ach in result["new_achievements"]:
                    ach_data = AchievementDiary.ACHIEVEMENTS[ach]
                    print(f"🏆 Achievement Unlocked: {ach_data['name']}")
            
            if result["random_event"]:
                print(f"🎲 {result['random_event']['message']}")
            
            print(kitsune.get_status_display())
    
    # Run demo
    asyncio.run(demo())