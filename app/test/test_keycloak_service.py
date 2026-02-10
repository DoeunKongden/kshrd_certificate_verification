"""
Test script for KeycloakService
Run this to test if your Keycloak service is working correctly.

Usage:
    poetry run python app/test/test_keycloak_service.py <user-id> [--debug]
    
Options:
    --debug    Show full raw Keycloak data (JSON)
"""
import asyncio
import sys
import os
import json
from pathlib import Path

# Change to project root directory to find .env file
project_root = Path(__file__).parent.parent.parent
os.chdir(project_root)

# Now import after changing directory
from app.services.keycloak_service import KeycloakService


async def test_keycloak_service():
    """Test the KeycloakService.get_user_profile method"""
    
    # Check for debug flag
    debug_mode = "--debug" in sys.argv
    if debug_mode:
        sys.argv.remove("--debug")
    
    print("=" * 70)
    print("KeycloakService Test Script")
    if debug_mode:
        print("DEBUG MODE: Showing full raw Keycloak data")
    print("=" * 70)
    
    # Step 1: Initialize the service
    print("\n[1/4] Initializing KeycloakService...")
    try:
        service = KeycloakService()
        print("   ✓ KeycloakService initialized successfully")
    except Exception as e:
        print(f"   ✗ Failed to initialize KeycloakService: {str(e)}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 2: Get user ID
    print("\n[2/4] Getting user ID...")
    if len(sys.argv) > 1:
        user_id = sys.argv[1]
        print(f"   ✓ Using user ID from command line: {user_id}")
    else:
        print("   Please provide a Keycloak user ID (UUID)")
        user_id = input("   Enter user ID: ").strip()
        if not user_id:
            print("   ✗ No user ID provided. Exiting.")
            return
    
    # Step 3: Fetch raw user data (for debugging)
    raw_user_data = None
    if debug_mode:
        print("\n[2.5/4] Fetching raw Keycloak user data...")
        try:
            raw_user_data = service.admin.get_user(user_id=user_id)
            print("   ✓ Raw user data retrieved")
            print("\n   Full Raw Keycloak User Data (JSON):")
            print("   " + "-" * 66)
            print(json.dumps(raw_user_data, indent=4, default=str))
        except Exception as e:
            print(f"   ✗ Failed to fetch raw data: {str(e)}")
    
    # Step 4: Test the method
    print(f"\n[3/4] Testing get_user_profile with user_id: {user_id}")
    print("   " + "-" * 66)
    
    try:
        profile = await service.get_user_profile(user_id)
        
        if profile:
            print("\n   ✓ Successfully retrieved user profile!")
            print("\n   Basic Information:")
            print("   " + "-" * 66)
            print(f"     ID:          {profile.id}")
            print(f"     Username:    {profile.username}")
            print(f"     Email:       {profile.email}")
            print(f"     Full Name:   {profile.full_name_en}")
            print(f"     Photo URL:   {profile.photo_url or '(not set)'}")
            print(f"     Roles:       {profile.roles if profile.roles else '(none)'}")
            
            # Show all additional attributes
            print("\n   Additional Attributes:")
            print("   " + "-" * 66)
            attrs_to_show = [
                ("Phone Number", profile.phone_number),
                ("Address", profile.address),
                ("Gender", profile.gender),
                ("University", profile.university),
                ("Bacll Grade", profile.bacll_grade),
                ("Khmer Name", profile.khmer_name),
                ("Province", profile.province),
                ("Date of Birth", profile.dob),
                ("Education Level", profile.education_level),
            ]
            
            for label, value in attrs_to_show:
                display_value = value if value else "(not set)"
                print(f"     {label:.<20} {display_value}")
            
            print("\n[4/4] Test Results")
            print("   " + "-" * 66)
            print("   ✓ Test completed successfully!")
        else:
            print("\n   ✗ User profile not found")
            print("   (The user doesn't exist in Keycloak or was deleted)")
            
    except PermissionError as e:
        print(f"\n   ✗ PERMISSION ERROR:")
        print(f"   {str(e)}")
        print("\n   To fix this:")
        print("   1. Go to Keycloak Admin Console")
        print("   2. Navigate to: Clients → hrd-certificate → Service Account Roles")
        print("   3. Click 'Assign role'")
        print("   4. Filter by 'realm-management'")
        print("   5. Assign the 'view-users' role")
        print("   6. Save and try again")
    except Exception as e:
        print(f"\n   ✗ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    asyncio.run(test_keycloak_service())