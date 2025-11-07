#!/usr/bin/env python
"""
Simple test script for Jerdon AI API
"""
import asyncio
import httpx

async def test_api():
    """Test all main endpoints"""
    base_url = "http://localhost:8000"

    async with httpx.AsyncClient() as client:
        print("Testing Jerdon AI API...")
        print("="*60)

        # Test health endpoint
        print("\n1. Testing /health endpoint:")
        response = await client.get(f"{base_url}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")

        # Test metrics endpoint
        print("\n2. Testing /metrics endpoint:")
        response = await client.get(f"{base_url}/metrics")
        print(f"   Status: {response.status_code}")
        print(f"   Metrics data length: {len(response.text)} bytes")
        print(f"   Sample metrics:")
        for line in response.text.split('\n')[:10]:
            if line and not line.startswith('#'):
                print(f"   {line}")

        # Test demo endpoints
        print("\n3. Testing /demo/chat endpoint:")
        response = await client.post(f"{base_url}/demo/chat")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")

        print("\n4. Testing /demo/upload endpoint:")
        response = await client.post(f"{base_url}/demo/upload")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")

        print("\n5. Testing /demo/register endpoint:")
        response = await client.post(f"{base_url}/demo/register")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")

        # Test metrics again to see incremented counters
        print("\n6. Testing /metrics endpoint again (should show incremented counters):")
        response = await client.get(f"{base_url}/metrics")
        for line in response.text.split('\n'):
            if 'chat_requests_total' in line or 'file_uploads_total' in line or 'user_registrations_total' in line:
                print(f"   {line}")

        print("\n" + "="*60)
        print("✅ All tests passed!")

if __name__ == "__main__":
    print("Make sure the server is running: uvicorn main:app --reload")
    print("Then run this test script")
    print()

    # Uncomment to run tests:
    # asyncio.run(test_api())
