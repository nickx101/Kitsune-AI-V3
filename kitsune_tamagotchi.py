#!/usr/bin/env python3
"""
🦊 Kitsune AI V3 - Simple Working Tamagotchi 🦊
FOUR CORE FEATURES:
1. Fox visual (actual fox, not particles)
2. Real chat with LLM 
3. XP system that works
4. Settings that actually work

NO PLACEHOLDERS. NO FEATURE CREEP. JUST WORKING CODE.
"""

import asyncio
import sys
import os
import json
import pickle
import time
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Import the working RuneScape systems
from kitsune_rs_master_clean import RuneScapeKitsuneAI, AchievementDiary, RSExperienceSystem

class KitsuneSettings:
    """Settings that actually work"""
    
    def __init__(self):
        self.settings_file = Path("kitsune_settings.json")
        self.load_settings()
    
    def load_settings(self):
        """Load settings from file"""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r') as f:
                    data = json.load(f)
                    self.llm_endpoint = data.get("llm_endpoint", "http://localhost:8000")
                    self.fox_color = data.get("fox_color", "orange")
                    self.sound_enabled = data.get("sound_enabled", True)
                    self.save_location = data.get("save_location", "./saves/")
            else:
                self.reset_to_defaults()
        except Exception as e:
            print(f"Settings load error: {e}")
            self.reset_to_defaults()
    
    def reset_to_defaults(self):
        """Reset to default settings"""
        self.llm_endpoint = "http://localhost:8000"
        self.fox_color = "orange"
        self.sound_enabled = True
        self.save_location = "./saves/"
    
    def save_settings(self):
        """Save settings to file"""
        try:
            data = {
                "llm_endpoint": self.llm_endpoint,
                "fox_color": self.fox_color,
                "sound_enabled": self.sound_enabled,
                "save_location": self.save_location
            }
            with open(self.settings_file, 'w') as f:
                json.dump(data, f, indent=2)
            print("✅ Settings saved!")
        except Exception as e:
            print(f"❌ Settings save error: {e}")

class KitsuneSaveSystem:
    """Save/load system that actually works"""
    
    def __init__(self, save_location: str = "./saves/"):
        self.save_dir = Path(save_location)
        self.save_dir.mkdir(exist_ok=True)
        self.save_file = self.save_dir / "kitsune_progress.pkl"
    
    def save_progress(self, kitsune_ai: RuneScapeKitsuneAI):
        """Save all progress to file"""
        try:
            save_data = {
                "version": "3.0",
                "timestamp": datetime.now().isoformat(),
                "skills": kitsune_ai.progression.skills,
                "total_interactions": kitsune_ai.progression.total_interactions,
                "achievements": list(kitsune_ai.achievements.completed),
                "current_mood": kitsune_ai.mood_system.current_mood,
                "session_start": kitsune_ai.session_start.isoformat()
            }
            
            with open(self.save_file, 'wb') as f:
                pickle.dump(save_data, f)
            print("💾 Progress saved!")
            return True
        except Exception as e:
            print(f"❌ Save error: {e}")
            return False
    
    def load_progress(self, kitsune_ai: RuneScapeKitsuneAI):
        """Load progress from file"""
        try:
            if not self.save_file.exists():
                print("📝 New save file - starting fresh!")
                return False
                
            with open(self.save_file, 'rb') as f:
                save_data = pickle.load(f)
            
            # Restore progress
            kitsune_ai.progression.skills = save_data.get("skills", kitsune_ai.progression.skills)
            kitsune_ai.progression.total_interactions = save_data.get("total_interactions", 0)
            kitsune_ai.achievements.completed = set(save_data.get("achievements", []))
            kitsune_ai.mood_system.current_mood = save_data.get("current_mood", "curious")
            
            print("📂 Progress loaded!")
            print(f"🦊 Welcome back! {kitsune_ai.progression.total_interactions} interactions completed")
            return True
        except Exception as e:
            print(f"❌ Load error: {e}")
            return False

class LLMConnector:
    """Real LLM connection that actually works"""
    
    def __init__(self, endpoint: str = "http://localhost:8000"):
        self.endpoint = endpoint
        self.timeout = 150
    
    def update_endpoint(self, new_endpoint: str):
        """Update LLM endpoint"""
        self.endpoint = new_endpoint
        print(f"🔗 LLM endpoint updated to: {new_endpoint}")
    
    def test_connection(self) -> bool:
        """Test if LLM is reachable"""
        try:
            response = requests.get(f"{self.endpoint}/health", timeout=5)
            print(f"Health check status: {response.status_code}")
            return response.status_code == 200
        except Exception as e:
            print(f"Connection error: {e}")
            return False
    
    async def chat(self, message: str) -> str:
        """Send message to LLM and get response"""
        try:
            # First test connection
            if not self.test_connection():
                return "❌ LLM connection failed. Check that the server is running on " + self.endpoint
            
            # Send chat request
            payload = {
                "message": message,
                "max_tokens": 500,
                "temperature": 0.7
            }
            
            response = requests.post(
                f"{self.endpoint}/chat", 
                json=payload, 
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("response", "No response from LLM")
            else:
                return f"❌ LLM error: {response.status_code}"
                
        except requests.exceptions.Timeout:
            return "⏰ LLM request timed out"
        except requests.exceptions.ConnectionError:
            return "🔌 Cannot connect to LLM server"
        except Exception as e:
            return f"❌ LLM error: {str(e)}"

class FoxVisual:
    """Simple fox visual that actually works"""
    
    def __init__(self, color: str = "orange"):
        self.color = color
        self.mood = "curious"
        self.tails = 1
    
    def update_color(self, new_color: str):
        """Update fox color"""
        self.color = new_color
        print(f"🎨 Fox color changed to: {new_color}")
    
    def update_mood(self, mood: str):
        """Update fox mood"""
        self.mood = mood
    
    def update_tails(self, tail_count: int):
        """Update tail count"""
        self.tails = tail_count
    
    def get_fox_display(self) -> str:
        """Get current fox visual"""
        # Color mapping
        color_emojis = {
            "orange": "🦊",
            "white": "🤍🦊",
            "black": "🖤🦊", 
            "golden": "💛🦊",
            "silver": "🤍✨🦊"
        }
        
        fox_emoji = color_emojis.get(self.color, "🦊")
        
        # Mood animations
        mood_effects = {
            "happy": "😊",
            "excited": "🤩", 
            "curious": "🤔",
            "wise": "🧠",
            "playful": "😄",
            "content": "😌",
            "focused": "🎯"
        }
        
        mood_emoji = mood_effects.get(self.mood, "😐")
        
        # Tail display
        tail_display = "🌟" * (self.tails - 1) if self.tails > 1 else ""
        
        return f"{fox_emoji}{mood_emoji}{tail_display}"

class KitsuneTamagotchi:
    """Main Kitsune Tamagotchi application"""
    
    def __init__(self):
        print("🚀 Initializing Kitsune AI V3...")
        
        # Core systems
        self.settings = KitsuneSettings()
        self.save_system = KitsuneSaveSystem(self.settings.save_location)
        self.llm = LLMConnector(self.settings.llm_endpoint)
        self.fox = FoxVisual(self.settings.fox_color)
        self.kitsune_ai = RuneScapeKitsuneAI()
        
        # Load saved progress
        self.save_system.load_progress(self.kitsune_ai)
        
        print("✅ Kitsune AI V3 ready!")
    
    def show_status(self):
        """Show current status"""
        print("\n" + "="*60)
        print(f"🦊 KITSUNE STATUS")
        print("="*60)
        
        # Fox display
        fox_display = self.fox.get_fox_display()
        print(f"Fox: {fox_display}")
        
        # Stats
        tails = self.kitsune_ai.progression.get_unlocked_tails()
        total_level = self.kitsune_ai.progression.get_total_level()
        total_interactions = self.kitsune_ai.progression.total_interactions
        achievements = len(self.kitsune_ai.achievements.completed)
        
        print(f"Tails: {tails}/9")
        print(f"Total Level: {total_level}")
        print(f"Interactions: {total_interactions}")
        print(f"Achievements: {achievements}")
        print(f"Mood: {self.kitsune_ai.mood_system.current_mood.title()}")
        
        # Next tail progress
        if tails < 9:
            thresholds = [9, 50, 100, 200, 350, 500, 650, 800, 891]
            next_threshold = thresholds[tails - 1]
            print(f"Next tail at level: {next_threshold}")
        
        # Show skill levels
        self.show_skills()
        
        print("="*60)
    
    def show_skills(self):
        """Show skill levels with progress bars"""
        print("\n📊 SKILL LEVELS")
        print("-" * 50)
        
        for skill_name, skill_data in self.kitsune_ai.progression.skills.items():
            level = skill_data["level"]
            xp = skill_data["xp"]
            
            # Calculate progress to next level
            next_level_xp = RSExperienceSystem.get_xp_for_level(level + 1) if level < 99 else 0
            
            if next_level_xp > 0:
                progress = (xp / next_level_xp) * 100
                progress_bar = "█" * int(progress / 10) + "░" * (10 - int(progress / 10))
                print(f"{skill_name:15} | Lv.{level:2} | {progress_bar} | {xp:6.0f}/{next_level_xp} XP")
            else:
                print(f"{skill_name:15} | Lv.{level:2} | ██████████ | MAX LEVEL!")
    
    def show_settings(self):
        """Show settings menu"""
        print("\n" + "="*50)
        print("⚙️  SETTINGS")
        print("="*50)
        print(f"1. LLM Endpoint: {self.settings.llm_endpoint}")
        print(f"2. Fox Color: {self.settings.fox_color}")
        print(f"3. Sound: {'On' if self.settings.sound_enabled else 'Off'}")
        print(f"4. Save Location: {self.settings.save_location}")
        print("5. Test LLM Connection")
        print("6. Reset to Defaults")
        print("7. Back to Main Menu")
        
        choice = input("\nSelect setting to change (1-7): ").strip()
        
        if choice == "1":
            new_endpoint = input(f"New LLM endpoint [{self.settings.llm_endpoint}]: ").strip()
            if new_endpoint:
                self.settings.llm_endpoint = new_endpoint
                self.llm.update_endpoint(new_endpoint)
                self.settings.save_settings()
        
        elif choice == "2":
            print("Available colors: orange, white, black, golden, silver")
            new_color = input(f"New fox color [{self.settings.fox_color}]: ").strip()
            if new_color in ["orange", "white", "black", "golden", "silver"]:
                self.settings.fox_color = new_color
                self.fox.update_color(new_color)
                self.settings.save_settings()
            else:
                print("❌ Invalid color")
        
        elif choice == "3":
            self.settings.sound_enabled = not self.settings.sound_enabled
            self.settings.save_settings()
            print(f"🔊 Sound {'enabled' if self.settings.sound_enabled else 'disabled'}")
        
        elif choice == "4":
            new_location = input(f"New save location [{self.settings.save_location}]: ").strip()
            if new_location:
                self.settings.save_location = new_location
                self.save_system = KitsuneSaveSystem(new_location)
                self.settings.save_settings()
        
        elif choice == "5":
            print("🔍 Testing LLM connection...")
            if self.llm.test_connection():
                print("✅ LLM connection successful!")
            else:
                print("❌ LLM connection failed")
        
        elif choice == "6":
            confirm = input("Reset all settings to defaults? (y/N): ").strip().lower()
            if confirm == 'y':
                self.settings.reset_to_defaults()
                self.settings.save_settings()
                print("🔄 Settings reset to defaults")
        
        elif choice == "7":
            return
        else:
            print("❌ Invalid choice")
    
    async def chat_with_kitsune(self):
        """Real chat with LLM integration"""
        print("\n💬 CHAT WITH KITSUNE")
        print("Type your message (or 'back' to return)")
        print("-" * 40)
        
        while True:
            # Show fox
            fox_display = self.fox.get_fox_display()
            user_input = input(f"\n{fox_display} You: ").strip()
            
            if user_input.lower() == 'back':
                break
            
            if not user_input:
                continue
            
            # Classify interaction type for XP
            interaction_type = self.classify_interaction(user_input)
            
            # Process with RuneScape AI system (gets XP)
            result = await self.kitsune_ai.process_interaction(interaction_type, user_input)
            
            # Update fox visual state
            self.fox.update_mood(result["mood"])
            self.fox.update_tails(result["current_tails"])
            
            # Show multiple XP drops
            if result.get("xp_drops"):
                for xp_drop in result["xp_drops"]:
                    print(f"✨ {xp_drop.format_display()}")
            
            # Show multiple level ups
            if result.get("level_ups"):
                for level_up in result["level_ups"]:
                    celebration = await self.kitsune_ai.tail_unlock_ceremony(level_up)
                    print(f"🎉 {celebration['message']}")
                
                # Check for new tail
                new_tails = result["current_tails"]
                if new_tails > getattr(self, '_last_tail_count', 1):
                    print(f"🌟 NEW TAIL UNLOCKED! You now have {new_tails} tails! 🌟")
                    self._last_tail_count = new_tails
            
            # Show achievements
            if result["new_achievements"]:
                for ach_id in result["new_achievements"]:
                    ach_data = AchievementDiary.ACHIEVEMENTS[ach_id]
                    print(f"🏆 ACHIEVEMENT: {ach_data['name']}")
            
            # Get LLM response
            print(f"{fox_display} Kitsune: Thinking...")
            llm_response = await self.llm.chat(user_input)
            print(f"{fox_display} Kitsune: {llm_response}")
            
            # Auto-save progress every 5 interactions
            if self.kitsune_ai.progression.total_interactions % 5 == 0:
                self.save_system.save_progress(self.kitsune_ai)
    
    def classify_interaction(self, text: str) -> str:
        """Classify user input for XP calculation"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['code', 'program', 'debug', 'function', 'python']):
            return "coding"
        elif any(word in text_lower for word in ['story', 'write', 'creative', 'poem']):
            return "creative"
        elif any(word in text_lower for word in ['analyze', 'data', 'pattern', 'study']):
            return "analysis"
        elif any(word in text_lower for word in ['learn', 'teach', 'explain']):
            return "learning"
        elif '?' in text:
            return "question"
        else:
            return "general"
    
    async def main_menu(self):
        """Main application loop"""
        self._last_tail_count = self.kitsune_ai.progression.get_unlocked_tails()
        
        while True:
            fox_display = self.fox.get_fox_display()
            print(f"\n{fox_display} KITSUNE AI V3 - SIMPLE & WORKING")
            print("="*50)
            print("1. 💬 Chat with Kitsune (Real LLM)")
            print("2. 📊 View Status & Progress")
            print("3. ⚙️  Settings")
            print("4. 💾 Save Progress")
            print("5. 🚪 Exit")
            
            choice = input("\nChoose (1-5): ").strip()
            
            if choice == "1":
                await self.chat_with_kitsune()
            elif choice == "2":
                self.show_status()
            elif choice == "3":
                self.show_settings()
            elif choice == "4":
                self.save_system.save_progress(self.kitsune_ai)
            elif choice == "5":
                print("💾 Saving progress...")
                self.save_system.save_progress(self.kitsune_ai)
                print("👋 Goodbye! Your progress has been saved.")
                break
            else:
                print("❌ Invalid choice")

async def main():
    """Application entry point"""
    print("🦊 Starting Kitsune AI V3...")
    print("🎯 SIMPLE. WORKING. NO PLACEHOLDERS.")
    
    try:
        app = KitsuneTamagotchi()
        await app.main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())