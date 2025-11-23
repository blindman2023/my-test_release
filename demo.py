#!/usr/bin/env python3
"""
Demo script to showcase the Chinese Learning Platform functionality
This script demonstrates the API endpoints and exercise validation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.lesson_service import lesson_service

def demo_lesson_service():
    print("=== Chinese Learning Platform Demo ===\n")
    
    # Test curriculum loading
    print("1. Loading curriculum...")
    curriculum = lesson_service.get_curriculum()
    print(f"   Found {len(curriculum['lessons'])} lessons")
    for lesson in curriculum['lessons']:
        print(f"   - {lesson['title']} ({lesson['level']})")
    
    # Test lesson loading
    print("\n2. Loading first lesson...")
    lesson = lesson_service.get_lesson_by_id("lesson-1")
    if lesson:
        print(f"   Lesson: {lesson['title']}")
        print(f"   Vocabulary: {len(lesson['vocabulary'])} words")
        print(f"   Grammar points: {len(lesson['grammar'])}")
        print(f"   Exercises: {len(lesson['exercises'])}")
        
        # Show vocabulary
        print("\n   Vocabulary sample:")
        for word in lesson['vocabulary'][:2]:
            print(f"     {word['chinese']} ({word['pinyin']}) - {word['english']}")
    
    # Test exercise validation
    print("\n3. Testing exercise validation...")
    result = lesson_service.validate_exercise_answer("lesson-1", "ex-1-1", "0")
    print(f"   Multiple choice (correct): {result['correct']}")
    
    result = lesson_service.validate_exercise_answer("lesson-1", "ex-1-1", "1")
    print(f"   Multiple choice (incorrect): {result['correct']}")
    
    result = lesson_service.validate_exercise_answer("lesson-1", "ex-1-2", "谢谢")
    print(f"   Translation (correct): {result['correct']}")
    
    print("\n=== Demo completed successfully! ===")

if __name__ == "__main__":
    demo_lesson_service()