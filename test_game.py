#!/usr/bin/env python3
"""
Test script to identify what's causing the game to crash
"""

import sys
import traceback

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import pygame
        print("✓ pygame imported successfully")
    except ImportError as e:
        print(f"✗ pygame import failed: {e}")
        return False
    
    try:
        import moderngl
        print("✓ moderngl imported successfully")
    except ImportError as e:
        print(f"✗ moderngl import failed: {e}")
        return False
    
    try:
        import cv2
        print("✓ opencv-python imported successfully")
    except ImportError as e:
        print(f"✗ opencv-python import failed: {e}")
        return False
    
    try:
        import mediapipe as mp
        print("✓ mediapipe imported successfully")
    except ImportError as e:
        print(f"✗ mediapipe import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("✓ numpy imported successfully")
    except ImportError as e:
        print(f"✗ numpy import failed: {e}")
        return False
    
    return True

def test_pygame_init():
    """Test pygame initialization"""
    print("\nTesting pygame initialization...")
    try:
        import pygame
        pygame.init()
        print("✓ pygame initialized successfully")
        return True
    except Exception as e:
        print(f"✗ pygame initialization failed: {e}")
        return False

def test_opengl_context():
    """Test OpenGL context creation"""
    print("\nTesting OpenGL context...")
    try:
        import pygame
        import moderngl
        
        # Create a small test window
        pygame.display.set_mode((100, 100), pygame.OPENGL | pygame.DOUBLEBUF)
        ctx = moderngl.create_context()
        print("✓ OpenGL context created successfully")
        
        # Clean up
        pygame.quit()
        return True
    except Exception as e:
        print(f"✗ OpenGL context creation failed: {e}")
        return False

def test_camera():
    """Test camera access"""
    print("\nTesting camera access...")
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("✓ Camera opened successfully")
            cap.release()
            return True
        else:
            print("⚠ Camera not available (this is normal if no camera is connected)")
            return True
    except Exception as e:
        print(f"✗ Camera test failed: {e}")
        return False

def test_asset_loading():
    """Test asset loading"""
    print("\nTesting asset loading...")
    try:
        import pygame
        pygame.init()
        
        # Test font loading
        font = pygame.font.Font('asset/orbitron-bold.otf', 16)
        print("✓ Font loaded successfully")
        
        # Test image loading
        image = pygame.image.load('asset/ui/logo.png')
        print("✓ Logo image loaded successfully")
        
        pygame.quit()
        return True
    except Exception as e:
        print(f"✗ Asset loading failed: {e}")
        return False

def test_game_modules():
    """Test importing game modules"""
    print("\nTesting game module imports...")
    
    modules = [
        'scripts.core',
        'scripts.brand_config',
        'scripts.window',
        'scripts.asset',
        'scripts.entities',
        'scripts.player',
        'scripts.vfx',
        'scripts.gamedata',
        'scripts.menu',
        'scripts.gesture_controller',
        'scripts.circuit_pattern',
        'scripts.gui'
    ]
    
    for module_name in modules:
        try:
            __import__(module_name)
            print(f"✓ {module_name} imported successfully")
        except Exception as e:
            print(f"✗ {module_name} import failed: {e}")
            return False
    
    return True

def main():
    """Run all tests"""
    print("=== Asteroid Sprint Game Crash Diagnostic ===\n")
    
    tests = [
        ("Import Tests", test_imports),
        ("Pygame Init", test_pygame_init),
        ("OpenGL Context", test_opengl_context),
        ("Camera Access", test_camera),
        ("Asset Loading", test_asset_loading),
        ("Game Modules", test_game_modules)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {e}")
            print(traceback.format_exc())
            results.append((test_name, False))
    
    print("\n=== Test Results ===")
    all_passed = True
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n✓ All tests passed! The game should work.")
    else:
        print("\n✗ Some tests failed. Check the issues above.")
    
    return all_passed

if __name__ == "__main__":
    main() 