"""
Utility functions for extracting trip details from user messages
"""

import re
from datetime import datetime
from typing import Dict, Optional, List
import json


class TripDetailsExtractor:
    """Extract trip planning details from natural language messages"""
    
    def __init__(self):
        """Initialize the extractor with patterns"""
        # Month patterns
        self.months = {
            'january': 1, 'jan': 1,
            'february': 2, 'feb': 2,
            'march': 3, 'mar': 3,
            'april': 4, 'apr': 4,
            'may': 5,
            'june': 6, 'jun': 6,
            'july': 7, 'jul': 7,
            'august': 8, 'aug': 8,
            'september': 9, 'sep': 9, 'sept': 9,
            'october': 10, 'oct': 10,
            'november': 11, 'nov': 11,
            'december': 12, 'dec': 12
        }
        
        # Common country and city names (expandable)
        self.destinations = [
            'paris', 'london', 'tokyo', 'new york', 'rome', 'barcelona',
            'amsterdam', 'berlin', 'prague', 'vienna', 'budapest',
            'france', 'uk', 'england', 'japan', 'italy', 'spain',
            'germany', 'netherlands', 'czech republic', 'austria', 'hungary',
            'usa', 'united states', 'canada', 'australia', 'thailand',
            'greece', 'portugal', 'switzerland', 'ireland', 'scotland'
        ]
    
    def extract_all_details(self, message: str) -> Dict:
        """
        Extract all trip details from a message
        
        Args:
            message: User's message text
            
        Returns:
            Dictionary with extracted details
        """
        message_lower = message.lower()
        
        return {
            'destination': self.extract_destination(message),
            'dates': self.extract_dates(message),
            'travelers': self.extract_travelers(message),
            'duration': self.extract_duration(message),
            'children': self.extract_children(message),
            'raw_message': message
        }
    
    def extract_destination(self, message: str) -> Optional[str]:
        """
        Extract destination (country or city) from message
        
        Examples:
            "I want to go to Paris" -> "Paris"
            "Planning a trip to Japan" -> "Japan"
            "Visit New York" -> "New York"
        """
        message_lower = message.lower()
        
        # Pattern 1: "to [destination]"
        pattern1 = r'to\s+([a-z\s]+?)(?:\s+(?:in|on|for|with|from)|[,.]|$)'
        match = re.search(pattern1, message_lower)
        if match:
            destination = match.group(1).strip()
            if destination in self.destinations:
                return destination.title()
        
        # Pattern 2: "visit [destination]"
        pattern2 = r'visit(?:ing)?\s+([a-z\s]+?)(?:\s+(?:in|on|for|with)|[,.]|$)'
        match = re.search(pattern2, message_lower)
        if match:
            destination = match.group(1).strip()
            if destination in self.destinations:
                return destination.title()
        
        # Pattern 3: "in [destination]"
        pattern3 = r'in\s+([a-z\s]+?)(?:\s+(?:in|on|for|with)|[,.]|$)'
        match = re.search(pattern3, message_lower)
        if match:
            destination = match.group(1).strip()
            if destination in self.destinations:
                return destination.title()
        
        # Pattern 4: Direct mention of known destinations
        for destination in sorted(self.destinations, key=len, reverse=True):
            if destination in message_lower:
                return destination.title()
        
        return None
    
    def extract_dates(self, message: str) -> Dict[str, Optional[str]]:
        """
        Extract travel dates from message
        
        Examples:
            "June 15 to June 20" -> {start: "2025-06-15", end: "2025-06-20"}
            "from July 1st" -> {start: "2025-07-01", end: None}
            "next summer" -> {season: "summer", year: 2025}
        """
        message_lower = message.lower()
        dates = {
            'start_date': None,
            'end_date': None,
            'season': None,
            'month': None,
            'year': None
        }
        
        # Pattern 1: Specific dates (e.g., "June 15", "15th of June")
        date_pattern = r'(\w+)\s+(\d{1,2})(?:st|nd|rd|th)?'
        matches = re.findall(date_pattern, message_lower)
        
        current_year = datetime.now().year
        
        for i, match in enumerate(matches):
            month_name, day = match
            if month_name in self.months:
                month = self.months[month_name]
                try:
                    date_str = f"{current_year}-{month:02d}-{int(day):02d}"
                    if i == 0:
                        dates['start_date'] = date_str
                    elif i == 1:
                        dates['end_date'] = date_str
                except ValueError:
                    pass
        
        # Pattern 2: Month mentions
        for month_name, month_num in self.months.items():
            if month_name in message_lower:
                dates['month'] = month_name.capitalize()
                break
        
        # Pattern 3: Season mentions
        seasons = ['summer', 'winter', 'spring', 'fall', 'autumn']
        for season in seasons:
            if season in message_lower:
                dates['season'] = season
                break
        
        # Pattern 4: Relative dates
        if 'next week' in message_lower:
            dates['relative'] = 'next_week'
        elif 'next month' in message_lower:
            dates['relative'] = 'next_month'
        elif 'next year' in message_lower:
            dates['relative'] = 'next_year'
            dates['year'] = current_year + 1
        
        return dates
    
    def extract_duration(self, message: str) -> Optional[int]:
        """
        Extract trip duration in days
        
        Examples:
            "5 days" -> 5
            "2 weeks" -> 14
            "one week" -> 7
        """
        message_lower = message.lower()
        
        # Pattern 1: X days
        pattern1 = r'(\d+)\s*(?:day|days)'
        match = re.search(pattern1, message_lower)
        if match:
            return int(match.group(1))
        
        # Pattern 2: X weeks
        pattern2 = r'(\d+)\s*(?:week|weeks)'
        match = re.search(pattern2, message_lower)
        if match:
            return int(match.group(1)) * 7
        
        # Pattern 3: Written numbers
        number_words = {
            'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
            'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10
        }
        
        for word, number in number_words.items():
            if f'{word} day' in message_lower:
                return number
            if f'{word} week' in message_lower:
                return number * 7
        
        return None
    
    def extract_travelers(self, message: str) -> Dict[str, int]:
        """
        Extract number of travelers
        
        Examples:
            "me and my wife" -> {adults: 2}
            "family of 4" -> {total: 4}
            "2 adults and 3 kids" -> {adults: 2, children: 3}
        """
        message_lower = message.lower()
        travelers = {
            'adults': 0,
            'children': 0,
            'total': 0
        }
        
        # Pattern 1: "X adults"
        adult_pattern = r'(\d+)\s*(?:adult|adults|grown-?up|grown-?ups)'
        match = re.search(adult_pattern, message_lower)
        if match:
            travelers['adults'] = int(match.group(1))
        
        # Pattern 2: "X children/kids"
        child_pattern = r'(\d+)\s*(?:child|children|kid|kids|toddler|toddlers)'
        match = re.search(child_pattern, message_lower)
        if match:
            travelers['children'] = int(match.group(1))
        
        # Pattern 3: "family of X"
        family_pattern = r'family of (\d+)'
        match = re.search(family_pattern, message_lower)
        if match:
            travelers['total'] = int(match.group(1))
        
        # Pattern 4: Implicit (me and my wife/husband)
        if 'me and my wife' in message_lower or 'my wife and i' in message_lower:
            travelers['adults'] = 2
        if 'me and my husband' in message_lower or 'my husband and i' in message_lower:
            travelers['adults'] = 2
        
        # Pattern 5: Solo traveler
        if any(word in message_lower for word in ['solo', 'alone', 'by myself', 'just me']):
            travelers['adults'] = 1
        
        # Calculate total if not explicitly stated
        if travelers['total'] == 0 and (travelers['adults'] > 0 or travelers['children'] > 0):
            travelers['total'] = travelers['adults'] + travelers['children']
        
        return travelers
    
    def extract_children(self, message: str) -> List[Dict]:
        """
        Extract detailed information about children (ages)
        
        Examples:
            "kids aged 5 and 8" -> [{age: 5}, {age: 8}]
            "6 year old daughter" -> [{age: 6, gender: "female"}]
        """
        message_lower = message.lower()
        children = []
        
        # Pattern 1: "aged X and Y"
        age_pattern1 = r'aged?\s+(\d+)(?:\s+and\s+(\d+))?'
        match = re.search(age_pattern1, message_lower)
        if match:
            for group in match.groups():
                if group:
                    children.append({'age': int(group)})
        
        # Pattern 2: "X year old" or "X-year-old"
        age_pattern2 = r'(\d+)[-\s]?year[-\s]?old'
        matches = re.findall(age_pattern2, message_lower)
        for age in matches:
            children.append({'age': int(age)})
        
        # Pattern 3: Age ranges
        if 'toddler' in message_lower:
            children.append({'age_range': '1-3', 'description': 'toddler'})
        if 'baby' in message_lower or 'infant' in message_lower:
            children.append({'age_range': '0-1', 'description': 'infant'})
        if 'teenager' in message_lower or 'teen' in message_lower:
            children.append({'age_range': '13-19', 'description': 'teenager'})
        
        return children
    
    def format_summary(self, details: Dict) -> str:
        """
        Format extracted details into a human-readable summary
        """
        lines = ["📋 Extracted Trip Details:"]
        
        if details.get('destination'):
            lines.append(f"📍 Destination: {details['destination']}")
        
        dates = details.get('dates', {})
        if dates.get('start_date'):
            lines.append(f"📅 Start Date: {dates['start_date']}")
        if dates.get('end_date'):
            lines.append(f"📅 End Date: {dates['end_date']}")
        if dates.get('month') and not dates.get('start_date'):
            lines.append(f"📅 Month: {dates['month']}")
        if dates.get('season'):
            lines.append(f"🌤️ Season: {dates['season'].capitalize()}")
        
        duration = details.get('duration')
        if duration:
            lines.append(f"⏱️ Duration: {duration} days")
        
        travelers = details.get('travelers', {})
        if travelers.get('total') > 0:
            lines.append(f"👥 Total Travelers: {travelers['total']}")
        if travelers.get('adults') > 0:
            lines.append(f"👨👩 Adults: {travelers['adults']}")
        if travelers.get('children') > 0:
            lines.append(f"👶 Children: {travelers['children']}")
        
        children = details.get('children', [])
        if children:
            ages = [str(c.get('age', c.get('description', '?'))) for c in children]
            lines.append(f"🎈 Children Ages: {', '.join(ages)}")
        
        if len(lines) == 1:
            lines.append("ℹ️ No specific details extracted yet. Please provide more information!")
        
        return "\n".join(lines)


# Convenience functions for easy import
def extract_trip_details(message: str) -> Dict:
    """Extract all trip details from a message"""
    extractor = TripDetailsExtractor()
    return extractor.extract_all_details(message)


def extract_destination(message: str) -> Optional[str]:
    """Extract just the destination from a message"""
    extractor = TripDetailsExtractor()
    return extractor.extract_destination(message)


def extract_dates(message: str) -> Dict:
    """Extract just the dates from a message"""
    extractor = TripDetailsExtractor()
    return extractor.extract_dates(message)


def extract_travelers(message: str) -> Dict:
    """Extract just the traveler count from a message"""
    extractor = TripDetailsExtractor()
    return extractor.extract_travelers(message)


def format_trip_summary(details: Dict) -> str:
    """Format trip details into a readable summary"""
    extractor = TripDetailsExtractor()
    return extractor.format_summary(details)


# Example usage and testing
if __name__ == "__main__":
    # Test cases
    test_messages = [
        "I want to plan a trip to Paris with my wife and two kids aged 5 and 8",
        "Planning a family vacation to Tokyo from June 15 to June 22",
        "We're thinking about visiting London next summer, family of 4",
        "5-day trip to Barcelona with 2 adults and 3 children",
        "Solo trip to New York in December",
        "Me and my husband want to go to Italy for 2 weeks"
    ]
    
    extractor = TripDetailsExtractor()
    
    print("=" * 70)
    print("TRIP DETAILS EXTRACTOR - TEST SUITE")
    print("=" * 70)
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n{'='*70}")
        print(f"Test {i}: {message}")
        print(f"{'='*70}")
        
        details = extractor.extract_all_details(message)
        summary = extractor.format_summary(details)
        
        print(summary)
        print(f"\nRaw extracted data:")
        import json
        print(json.dumps(details, indent=2, default=str))
