#!/usr/bin/env python3
"""
Example usage of GitHubAPIClient

This example shows how to use the GitHub API client to fetch PR data.
Note: Requires GitHub token to be set in environment variables.
"""
import asyncio
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from services.github_client import GitHubAPIClient, GitHubAPIError


async def example_fetch_pr_data():
    """Example of fetching PR data"""
    
    # Initialize client (will use GITHUB_TOKEN from environment)
    client = GitHubAPIClient()
    
    try:
        # Example PR URL
        pr_url = "https://github.com/octocat/Hello-World/pull/1"
        
        # Parse the URL
        repo, pr_number = client.parse_pr_url(pr_url)
        print(f"Repository: {repo}")
        print(f"PR Number: {pr_number}")
        
        # Validate token (optional)
        if await client.validate_token():
            print("✓ GitHub token is valid")
            
            # Fetch PR data
            pr_data = await client.fetch_pr_data(repo, pr_number)
            
            print(f"PR Title: {pr_data.metadata.title}")
            print(f"Author: {pr_data.metadata.author}")
            print(f"Commit SHA: {pr_data.metadata.commit_sha}")
            print(f"Files changed: {len(pr_data.files_changed)}")
            print(f"Diff size: {len(pr_data.diff_content)} characters")
            
        else:
            print("✗ GitHub token is invalid or not provided")
            print("Set GITHUB_TOKEN environment variable")
    
    except GitHubAPIError as e:
        print(f"GitHub API Error: {e}")
    
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    finally:
        # Clean up
        await client.close()


async def example_parse_urls():
    """Example of parsing various GitHub PR URLs"""
    
    client = GitHubAPIClient()
    
    test_urls = [
        "https://github.com/microsoft/vscode/pull/12345",
        "https://github.com/facebook/react/pull/67890",
        "github.com/google/tensorflow/pull/11111",
    ]
    
    print("Parsing GitHub PR URLs:")
    for url in test_urls:
        try:
            repo, pr_number = client.parse_pr_url(url)
            print(f"✓ {url}")
            print(f"  Repository: {repo}")
            print(f"  PR Number: {pr_number}")
        except GitHubAPIError as e:
            print(f"✗ {url}: {e}")


if __name__ == "__main__":
    print("GitHub API Client Examples")
    print("=" * 40)
    
    # Check if token is available
    if os.getenv("GITHUB_TOKEN"):
        print("Running full example with API calls...")
        asyncio.run(example_fetch_pr_data())
    else:
        print("GITHUB_TOKEN not set, running URL parsing example only...")
        asyncio.run(example_parse_urls())
    
    print("\nExample completed!")