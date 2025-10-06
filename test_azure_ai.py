#!/usr/bin/env python3
"""
Test script for Azure AI Foundry integration
Run this to verify your Azure OpenAI configuration is working
"""

from azure_ai import get_azure_ai_response, get_ai_status
import json


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def test_ai_status():
    """Test 1: Check Azure AI configuration status"""
    print_section("Test 1: Azure AI Configuration Status")
    
    status = get_ai_status()
    print(json.dumps(status, indent=2))
    
    if status['configured']:
        print("\n✅ Azure AI is properly configured!")
    else:
        print("\n❌ Azure AI is NOT configured properly.")
        print("Please check your .env file and ensure all credentials are set.")
        print("See AZURE_SETUP.md for instructions.")
    
    return status['configured']


def test_simple_response():
    """Test 2: Get a simple response from Azure AI"""
    print_section("Test 2: Simple AI Response")
    
    test_message = "Hello! Can you help me plan a family trip?"
    print(f"User: {test_message}\n")
    
    response = get_azure_ai_response(test_message)
    print(f"AI Assistant: {response}")
    
    if len(response) > 50 and "configure" not in response.lower():
        print("\n✅ AI response looks good!")
        return True
    else:
        print("\n⚠️ AI response seems like a fallback. Check configuration.")
        return False


def test_trip_planning_response():
    """Test 3: Test trip planning specific response"""
    print_section("Test 3: Trip Planning Response")
    
    test_message = "I want to plan a 5-day trip to Tokyo with my wife and two kids (ages 5 and 8)"
    print(f"User: {test_message}\n")
    
    response = get_azure_ai_response(test_message)
    print(f"AI Assistant: {response}")
    
    # Check if response contains relevant keywords
    keywords = ['tokyo', 'kids', 'children', 'family', 'activities', 'recommend']
    found_keywords = [kw for kw in keywords if kw in response.lower()]
    
    print(f"\n📊 Found relevant keywords: {found_keywords}")
    
    if len(found_keywords) >= 2:
        print("✅ AI response is contextual and relevant!")
        return True
    else:
        print("⚠️ AI response may not be contextual enough.")
        return False


def test_conversation_context():
    """Test 4: Test conversation context handling"""
    print_section("Test 4: Conversation Context")
    
    # Simulate a conversation
    conversation = [
        {"role": "user", "message": "I want to visit Paris"},
        {"role": "assistant", "message": "Paris is a wonderful destination! When are you planning to visit?"}
    ]
    
    test_message = "We're thinking about going in summer with our 6-year-old"
    print("Previous conversation:")
    for msg in conversation:
        print(f"  {msg['role']}: {msg['message']}")
    
    print(f"\nUser: {test_message}\n")
    
    response = get_azure_ai_response(test_message, conversation)
    print(f"AI Assistant: {response}")
    
    # Check if response references Paris or summer
    context_keywords = ['paris', 'summer', '6', 'child', 'kid']
    found_context = [kw for kw in context_keywords if kw in response.lower()]
    
    print(f"\n📊 Context awareness - found: {found_context}")
    
    if len(found_context) >= 1:
        print("✅ AI maintains conversation context!")
        return True
    else:
        print("⚠️ AI may not be using conversation context properly.")
        return False


def main():
    """Run all tests"""
    print("\n" + "🚀" * 30)
    print("  AZURE AI FOUNDRY INTEGRATION TEST SUITE")
    print("🚀" * 30)
    
    results = []
    
    # Test 1: Configuration
    configured = test_ai_status()
    results.append(("Configuration", configured))
    
    if not configured:
        print("\n" + "❌" * 30)
        print("⚠️  Cannot proceed with further tests.")
        print("⚠️  Please configure Azure AI credentials first.")
        print("⚠️  See AZURE_SETUP.md for instructions.")
        print("❌" * 30)
        return
    
    # Test 2: Simple response
    results.append(("Simple Response", test_simple_response()))
    
    # Test 3: Trip planning
    results.append(("Trip Planning", test_trip_planning_response()))
    
    # Test 4: Context
    results.append(("Conversation Context", test_conversation_context()))
    
    # Summary
    print_section("TEST SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Azure AI integration is working perfectly!")
    elif passed > 0:
        print("\n⚠️  Some tests passed. Check failed tests above.")
    else:
        print("\n❌ All tests failed. Please check your Azure AI configuration.")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
