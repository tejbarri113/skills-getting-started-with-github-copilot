"""
Shared pytest fixtures for FastAPI app tests
"""
import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add src directory to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app, activities


@pytest.fixture
def client():
    """Test client fixture for FastAPI app"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to initial state before each test"""
    # Store original state
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Soccer Team": {
            "description": "Team practices, matches, and seasonal tournaments",
            "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 25,
            "participants": ["liam@mergington.edu", "noah@mergington.edu"]
        },
        "Basketball Club": {
            "description": "Skill development, scrimmages, and intramural play",
            "schedule": "Wednesdays and Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 20,
            "participants": ["ava@mergington.edu", "isabella@mergington.edu"]
        },
        "Art Club": {
            "description": "Explore painting, drawing, sculpture, and mixed media",
            "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
            "max_participants": 15,
            "participants": ["mia@mergington.edu", "charlotte@mergington.edu"]
        },
        "Drama Club": {
            "description": "Rehearse plays, staging, and performance opportunities",
            "schedule": "Thursdays, 3:30 PM - 5:30 PM",
            "max_participants": 30,
            "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
        },
        "Math Olympiad": {
            "description": "Problem solving practice and competition prep",
            "schedule": "Mondays, 3:30 PM - 4:30 PM",
            "max_participants": 15,
            "participants": ["lucas@mergington.edu", "ethan@mergington.edu"]
        },
        "Science Club": {
            "description": "Hands-on experiments, projects, and science fair prep",
            "schedule": "Wednesdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["oliver@mergington.edu", "sophia2@mergington.edu"]
        }
    }
    
    # Clear and reset
    activities.clear()
    activities.update(original_activities)
    
    yield
    
    # After test, reset again
    activities.clear()
    activities.update(original_activities)


@pytest.fixture
def sample_email():
    """Sample email for testing"""
    return "test.student@mergington.edu"


@pytest.fixture
def sample_activity():
    """Sample activity name for testing"""
    return "Chess Club"
