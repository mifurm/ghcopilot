#!/usr/bin/env python3
"""
Interactive demo of the trip extraction feature
Run this to see real-time extraction examples
"""

from trip_extractor import TripDetailsExtractor, format_trip_summary
from colorama import Fore, Style, init

# Initialize colorama for colored output
try:
    init(autoreset=True)
    COLORS_AVAILABLE = True
except:
    COLORS_AVAILABLE = False


def print_header(text):
    """Print a colored header"""
    if COLORS_AVAILABLE:
        print(f"\n{Fore.CYAN}{'=' * 70}")
        print(f"{Fore.CYAN}{text:^70}")
        print(f"{Fore.CYAN}{'=' * 70}{Style.RESET_ALL}")
    else:
        print(f"\n{'=' * 70}")
        print(f"{text:^70}")
        print(f"{'=' * 70}")


def print_input(text):
    """Print user input"""
    if COLORS_AVAILABLE:
        print(f"{Fore.GREEN}👤 User: {text}{Style.RESET_ALL}")
    else:
        print(f"👤 User: {text}")


def print_output(text):
    """Print bot output"""
    if COLORS_AVAILABLE:
        print(f"{Fore.YELLOW}🤖 Bot: {text}{Style.RESET_ALL}")
    else:
        print(f"🤖 Bot: {text}")


def print_extracted(summary):
    """Print extracted details"""
    if COLORS_AVAILABLE:
        print(f"{Fore.MAGENTA}\n{summary}{Style.RESET_ALL}")
    else:
        print(f"\n{summary}")


def demo_conversation():
    """Run a demo conversation showing extraction in action"""
    print_header("TRIP DETAILS EXTRACTION - LIVE DEMO")
    
    extractor = TripDetailsExtractor()
    
    # Conversation flow
    conversations = [
        {
            "user": "Hi! I'm planning a family trip",
            "bot": "Hello! I'd be happy to help you plan your family trip. Where would you like to go, and when are you thinking of traveling?"
        },
        {
            "user": "We want to visit Paris in June with our 2 kids",
            "bot": "Paris in June is a wonderful choice! The weather is perfect and there are so many family-friendly activities. How old are your children?"
        },
        {
            "user": "They're 5 and 8 years old. We're thinking about going from June 15 to June 22",
            "bot": "Perfect! That gives you a full week to explore. Paris has amazing attractions for those ages - the Eiffel Tower, Luxembourg Gardens, and Disneyland Paris are all great options."
        },
        {
            "user": "Sounds great! So it's me, my wife, and the 2 kids for 7 days",
            "bot": "Excellent! I have all the details now. Let me help you plan some activities and find family-friendly accommodations."
        }
    ]
    
    print("\n🎭 Simulated Conversation:")
    print("Watch how trip details are extracted in real-time!\n")
    
    cumulative_details = {
        'destination': None,
        'dates': {},
        'travelers': {'adults': 0, 'children': 0, 'total': 0},
        'duration': None,
        'children': []
    }
    
    for i, conv in enumerate(conversations, 1):
        print(f"\n{'─' * 70}")
        print(f"Message {i}:")
        print(f"{'─' * 70}")
        
        print_input(conv['user'])
        print_output(conv['bot'])
        
        # Extract details from user message
        details = extractor.extract_all_details(conv['user'])
        
        # Update cumulative details
        if details['destination']:
            cumulative_details['destination'] = details['destination']
        if details['dates'].get('start_date'):
            cumulative_details['dates']['start_date'] = details['dates']['start_date']
        if details['dates'].get('end_date'):
            cumulative_details['dates']['end_date'] = details['dates']['end_date']
        if details['dates'].get('month'):
            cumulative_details['dates']['month'] = details['dates']['month']
        if details['travelers']['adults'] > 0:
            cumulative_details['travelers']['adults'] = details['travelers']['adults']
        if details['travelers']['children'] > 0:
            cumulative_details['travelers']['children'] = details['travelers']['children']
        if details['travelers']['total'] > 0:
            cumulative_details['travelers']['total'] = details['travelers']['total']
        if details['duration']:
            cumulative_details['duration'] = details['duration']
        if details['children']:
            cumulative_details['children'] = details['children']
        
        # Show what was extracted from this message
        if any([details['destination'], details['dates'].get('start_date'), 
                details['travelers']['total'] > 0, details['duration'], details['children']]):
            
            extracted_items = []
            if details['destination']:
                extracted_items.append(f"📍 Destination: {details['destination']}")
            if details['dates'].get('start_date'):
                extracted_items.append(f"📅 Start: {details['dates']['start_date']}")
            if details['dates'].get('end_date'):
                extracted_items.append(f"📅 End: {details['dates']['end_date']}")
            if details['dates'].get('month'):
                extracted_items.append(f"📅 Month: {details['dates']['month']}")
            if details['travelers']['adults'] > 0:
                extracted_items.append(f"👨👩 Adults: {details['travelers']['adults']}")
            if details['travelers']['children'] > 0:
                extracted_items.append(f"👶 Children: {details['travelers']['children']}")
            if details['duration']:
                extracted_items.append(f"⏱️ Duration: {details['duration']} days")
            if details['children']:
                ages = [str(c['age']) for c in details['children'] if 'age' in c]
                if ages:
                    extracted_items.append(f"🎈 Ages: {', '.join(ages)}")
            
            if COLORS_AVAILABLE:
                print(f"\n{Fore.BLUE}🔍 Extracted from this message:{Style.RESET_ALL}")
                for item in extracted_items:
                    print(f"{Fore.BLUE}   {item}{Style.RESET_ALL}")
            else:
                print(f"\n🔍 Extracted from this message:")
                for item in extracted_items:
                    print(f"   {item}")
    
    # Final summary
    print_header("COMPLETE TRIP SUMMARY")
    summary = format_trip_summary(cumulative_details)
    print_extracted(summary)
    
    print(f"\n{'=' * 70}")
    print("✅ All trip details successfully extracted!")
    print("🎯 Ready to provide personalized recommendations!")
    print(f"{'=' * 70}\n")


def interactive_mode():
    """Interactive mode - user can type their own messages"""
    print_header("INTERACTIVE EXTRACTION MODE")
    print("\n💡 Type trip-related messages and see what gets extracted!")
    print("💡 Type 'quit' or 'exit' to stop\n")
    
    extractor = TripDetailsExtractor()
    
    while True:
        try:
            user_input = input(f"\n👤 You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Thanks for trying the trip extractor!\n")
                break
            
            # Extract details
            details = extractor.extract_all_details(user_input)
            summary = format_trip_summary(details)
            
            print_extracted(summary)
            
        except KeyboardInterrupt:
            print("\n\n👋 Thanks for trying the trip extractor!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")


def main():
    """Main demo function"""
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║           🧳 TRIP DETAILS EXTRACTOR - INTERACTIVE DEMO            ║
║                                                                   ║
║   This demo shows how the trip extraction feature works in        ║
║   real-time. It can identify destinations, dates, travelers,      ║
║   and more from natural language messages.                        ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
    """)
    
    while True:
        print("\n📋 Choose a demo mode:")
        print("  1. Watch a simulated conversation")
        print("  2. Try interactive mode (type your own messages)")
        print("  3. Exit")
        
        choice = input("\nYour choice (1-3): ").strip()
        
        if choice == '1':
            demo_conversation()
        elif choice == '2':
            interactive_mode()
        elif choice == '3':
            print("\n👋 Goodbye! Happy trip planning!\n")
            break
        else:
            print("\n❌ Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
