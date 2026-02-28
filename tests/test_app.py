"""
Comprehensive FastAPI tests using AAA (Arrange-Act-Assert) pattern
Tests for the Mergington High School Activities API
"""
import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint"""
    
    def test_get_activities_success(self, client):
        """Test successfully retrieving all activities"""
        # Arrange
        # (no setup needed - activities pre-populated in fixture)
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Soccer Team" in data
    
    def test_get_activities_contains_required_fields(self, client):
        """Test that activities have all required fields"""
        # Arrange
        # (no setup needed)
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        chess_club = activities["Chess Club"]
        
        # Assert
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        assert isinstance(chess_club["participants"], list)
    
    def test_get_activities_count(self, client):
        """Test that all 9 activities are returned"""
        # Arrange
        # (no setup needed)
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert len(activities) == 9


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_success(self, client, sample_email, sample_activity):
        """Test successful signup for an activity"""
        # Arrange
        email = sample_email
        activity_name = sample_activity
        initial_count = len(client.get("/activities").json()[activity_name]["participants"])
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]
        
        # Verify participant was added
        updated_activity = client.get("/activities").json()[activity_name]
        assert email in updated_activity["participants"]
        assert len(updated_activity["participants"]) == initial_count + 1
    
    def test_signup_duplicate_email(self, client, sample_activity):
        """Test that duplicate signup returns 400 error"""
        # Arrange
        email = "michael@mergington.edu"  # Already in Chess Club
        activity_name = sample_activity
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"].lower()
    
    def test_signup_activity_not_found(self, client, sample_email):
        """Test signup for non-existent activity returns 404"""
        # Arrange
        email = sample_email
        activity_name = "Nonexistent Activity"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"].lower()
    
    def test_signup_activity_full(self, client):
        """Test signup when activity is at max capacity"""
        # Arrange
        # Create a new activity that's almost full
        email = "new.student@mergington.edu"
        
        # Use Art Club which has max 15 participants and currently has 2
        activity_name = "Art Club"
        activities_data = client.get("/activities").json()
        art_club = activities_data[activity_name]
        
        # Fill the activity to capacity
        for i in range(art_club["max_participants"] - art_club["participants"].__len__()):
            test_email = f"filler{i}@mergington.edu"
            client.post(
                f"/activities/{activity_name}/signup",
                params={"email": test_email}
            )
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "full" in data["detail"].lower()
    
    def test_signup_multiple_different_activities(self, client):
        """Test signing up same student for multiple different activities"""
        # Arrange
        email = "multi.student@mergington.edu"
        activity1 = "Chess Club"
        activity2 = "Soccer Team"
        
        # Act
        response1 = client.post(
            f"/activities/{activity1}/signup",
            params={"email": email}
        )
        response2 = client.post(
            f"/activities/{activity2}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        activities_data = client.get("/activities").json()
        assert email in activities_data[activity1]["participants"]
        assert email in activities_data[activity2]["participants"]


class TestUnregisterFromActivity:
    """Tests for DELETE /activities/{activity_name}/unregister endpoint"""
    
    def test_unregister_success(self, client, sample_activity):
        """Test successful unregistration from activity"""
        # Arrange
        email = "michael@mergington.edu"  # Already in Chess Club
        activity_name = sample_activity
        initial_count = len(client.get("/activities").json()[activity_name]["participants"])
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "unregistered" in data["message"].lower()
        assert email in data["message"]
        
        # Verify participant was removed
        updated_activity = client.get("/activities").json()[activity_name]
        assert email not in updated_activity["participants"]
        assert len(updated_activity["participants"]) == initial_count - 1
    
    def test_unregister_not_signed_up(self, client, sample_email, sample_activity):
        """Test unregistration for student not signed up returns 400"""
        # Arrange
        email = sample_email  # Not signed up anywhere
        activity_name = sample_activity
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "not signed up" in data["detail"].lower()
    
    def test_unregister_activity_not_found(self, client, sample_email):
        """Test unregister from non-existent activity returns 404"""
        # Arrange
        email = sample_email
        activity_name = "Nonexistent Activity"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"].lower()
    
    def test_unregister_then_signup_again(self, client, sample_email, sample_activity):
        """Test that student can signup again after unregistering"""
        # Arrange
        email = sample_email
        activity_name = sample_activity
        
        # First signup
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response1.status_code == 200
        
        # Act - Unregister
        response2 = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        assert response2.status_code == 200
        
        # Try to signup again
        response3 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response3.status_code == 200
        activities_data = client.get("/activities").json()
        assert email in activities_data[activity_name]["participants"]


class TestEdgeCases:
    """Tests for edge cases and state transitions"""
    
    def test_signup_and_unregister_multiple_times(self, client):
        """Test signup/unregister cycles multiple times"""
        # Arrange
        email = "cycle.student@mergington.edu"
        activity = "Math Olympiad"
        
        # Act & Assert - Multiple cycles
        for i in range(3):
            # Signup
            response1 = client.post(
                f"/activities/{activity}/signup",
                params={"email": email}
            )
            assert response1.status_code == 200
            
            activities_data = client.get("/activities").json()
            assert email in activities_data[activity]["participants"]
            
            # Unregister
            response2 = client.delete(
                f"/activities/{activity}/unregister",
                params={"email": email}
            )
            assert response2.status_code == 200
            
            activities_data = client.get("/activities").json()
            assert email not in activities_data[activity]["participants"]
    
    def test_activity_capacity_calculation(self, client):
        """Test that capacity is correctly enforced"""
        # Arrange
        activity = "Drama Club"  # max_participants: 30, currently has 2
        activities_data = client.get("/activities").json()
        max_cap = activities_data[activity]["max_participants"]
        current_count = len(activities_data[activity]["participants"])
        
        # Act - Fill to capacity
        for i in range(max_cap - current_count):
            email = f"capacity_test_{i}@mergington.edu"
            response = client.post(
                f"/activities/{activity}/signup",
                params={"email": email}
            )
            assert response.status_code == 200
        
        # Try to signup one more (should fail)
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": "over_capacity@mergington.edu"}
        )
        
        # Assert
        assert response.status_code == 400
        assert "full" in response.json()["detail"].lower()
    
    def test_special_characters_in_email(self, client, sample_activity):
        """Test signup with special characters in email"""
        # Arrange
        email = "test+tag@mergington.edu"
        activity_name = sample_activity
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        activities_data = client.get("/activities").json()
        assert email in activities_data[activity_name]["participants"]
    
    def test_activity_name_with_spaces(self, client):
        """Test signup for activities with spaces in names"""
        # Arrange
        email = "space_test@mergington.edu"
        
        # Act - Test activities with spaces: "Chess Club", "Programming Class", etc.
        response = client.post(
            f"/activities/Chess Club/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        activities_data = client.get("/activities").json()
        assert email in activities_data["Chess Club"]["participants"]
