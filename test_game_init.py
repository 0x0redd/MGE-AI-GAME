#!/usr/bin/env python3
"""
Detailed game initialization test to identify the exact crash point
"""

import sys
import traceback
import pygame

def test_step_by_step():
    """Test game initialization step by step"""
    print("=== Step-by-Step Game Initialization Test ===\n")
    
    try:
        print("Step 1: Importing modules...")
        from scripts.core import WIN_SIZE
        from scripts.brand_config import GAME_TITLE
        print("✓ Core modules imported")
        
        print("\nStep 2: Initializing pygame...")
        pygame.init()
        print("✓ Pygame initialized")
        
        print("\nStep 3: Creating shader window...")
        from scripts.window import ShaderWindow
        window = ShaderWindow(WIN_SIZE, GAME_TITLE, 'shaders/')
        print("✓ Shader window created")
        
        print("\nStep 4: Loading loading screen...")
        window.loading_screen('asset/ui/loading.png')
        print("✓ Loading screen loaded")
        
        print("\nStep 5: Creating display surface...")
        display = pygame.Surface(WIN_SIZE, pygame.SRCALPHA)
        print("✓ Display surface created")
        
        print("\nStep 6: Initializing gesture controller...")
        from scripts.gesture_controller import GestureController
        # Create a dummy game object for testing
        print("\nStep 8: Initializing game data manager...")
        from scripts.gamedata import GameDataManager
        gd = GameDataManager(None)
        print("✓ Game data manager initialized")
        
        print("\nStep 9: Loading assets...")
        from scripts.asset import Asset
        asset = Asset()
        asset.load_assets()
        print("✓ Assets loaded")
        
        # Now create the dummy game object, after asset and gd are defined
        class DummyGame:
            def __init__(self):
                self.window = window
                self.asset = asset
                self.gd = gd
                # Add missing attributes that the Menu class expects
                self.magnet_power = gd.magnet_power
                self.credits = gd.credits
                self.dt = 0
                self.hud = None  # Will be set later
                self.menu = None  # Will be set later
                
            def purchase(self, price):
                self.credits -= price
                
            def switch_sound(self):
                pass  # Dummy implementation
                
            def set_volume(self, volume):
                pass  # Dummy implementation
                
            def reset(self):
                pass  # Dummy implementation
                
            def start_game(self):
                pass  # Dummy implementation
                
            def quit(self):
                pass  # Dummy implementation
        dummy_game = DummyGame()
        gesture_controller = GestureController(dummy_game)
        print("✓ Gesture controller initialized")
        
        print("\nStep 7: Initializing circuit patterns...")
        from scripts.circuit_pattern import CircuitPattern, GeometricPattern
        circuit_pattern = CircuitPattern(WIN_SIZE[0], WIN_SIZE[1])
        geometric_pattern = GeometricPattern(WIN_SIZE[0], WIN_SIZE[1])
        print("✓ Circuit patterns initialized")
        
        print("\nStep 10: Setting up UI...")
        from scripts.brand_config import FONT_PRIMARY, FONT_SIZE_MEDIUM
        font = FONT_PRIMARY
        time_font = pygame.font.Font(font, FONT_SIZE_MEDIUM)
        ui_surf = pygame.Surface(WIN_SIZE, pygame.SRCALPHA)
        print("✓ UI setup completed")
        
        print("\nStep 11: Setting up sound...")
        pygame.mixer.music.load('asset/Screen Saver.mp3')
        pygame.mixer.music.play(-1)
        print("✓ Sound setup completed")
        
        print("\nStep 12: Setting up shaders...")
        window.load_const_surface('noise_tex', asset.noise)
        window.load_const_var('res', WIN_SIZE)
        window.load_const_var('w', 1.0/WIN_SIZE[0])
        window.load_const_var('h', 1.0/WIN_SIZE[1])
        window.load_const_var('max_st', 5)  # MAX_STELLAR_CREDITS
        window.load_const_var('max_magnet', 7000)  # MAGNET_DURATION
        window.load_const_var('max_freeze', 2000)  # FREEZE_DURATION
        stars_surf = pygame.Surface(WIN_SIZE, pygame.SRCALPHA)
        print("✓ Shaders setup completed")
        
        print("\nStep 13: Initializing menu...")
        from scripts.menu import Menu
        menu = Menu(dummy_game)
        print("✓ Menu initialized")
        
        print("\nStep 14: Setting up GUI...")
        import scripts.gui as gui
        gui.game = dummy_game
        hud = gui.EffectsHud()
        print("✓ GUI setup completed")
        
        print("\nStep 15: Initializing player...")
        from scripts.player import Player
        player = Player(dummy_game)
        print("✓ Player initialized")
        
        print("\nStep 16: Setting up game variables...")
        # Initialize game lists
        asteroids = []
        points = []
        bonuses = []
        particles = []
        vfx_particles = []
        print("✓ Game variables initialized")
        
        print("\nStep 17: Setting up game state...")
        menu_active = True
        game_over = False
        score = 0
        current_credits = 0
        super_magnet = 0
        freeze = 0
        show_help = False
        print("✓ Game state initialized")
        
        print("\nStep 18: Setting up timers...")
        clock = pygame.time.Clock()
        dt = 0
        current_time = 0
        start_time = 0
        print("✓ Timers initialized")
        
        print("\nStep 19: Setting up input...")
        keys = None
        print("✓ Input setup completed")
        
        print("\nStep 20: Final cleanup...")
        pygame.mixer.music.stop()
        pygame.quit()
        print("✓ Cleanup completed")
        
        print("\n🎉 SUCCESS! All initialization steps completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n💥 CRASH! Error occurred: {e}")
        print(f"Error type: {type(e).__name__}")
        print("\nFull traceback:")
        traceback.print_exc()
        return False

def test_actual_game_class():
    """Test the actual Game class initialization"""
    print("\n=== Testing Actual Game Class ===\n")
    
    try:
        print("Attempting to create Game instance...")
        from asteroid_sprint import Game
        game = Game()
        print("✓ Game instance created successfully!")
        
        print("Attempting to run game...")
        # This would normally run the game loop, but we'll just test initialization
        print("✓ Game initialization completed!")
        
        # Clean up
        if hasattr(game, 'quit'):
            game.quit()
        
        return True
        
    except Exception as e:
        print(f"\n💥 CRASH! Error in Game class: {e}")
        print(f"Error type: {type(e).__name__}")
        print("\nFull traceback:")
        traceback.print_exc()
        return False

def main():
    """Run the detailed tests"""
    print("=== Asteroid Sprint Detailed Crash Analysis ===\n")
    
    # Test step by step initialization
    step_by_step_success = test_step_by_step()
    
    if step_by_step_success:
        # If step by step works, test the actual Game class
        game_class_success = test_actual_game_class()
        
        if game_class_success:
            print("\n🎉 All tests passed! The game should work properly.")
        else:
            print("\n⚠ Step-by-step initialization works, but Game class has issues.")
    else:
        print("\n💥 Step-by-step initialization failed. Check the error above.")
    
    return step_by_step_success

if __name__ == "__main__":
    main() 