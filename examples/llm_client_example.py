#!/usr/bin/env python3
"""
Example usage of LLM Client

This example shows how to use the LLM client to interact with different
language model providers (OpenAI and Anthropic).
"""
import asyncio
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Note: This example requires LangChain dependencies to be installed


async def example_openai_client():
    """Example using OpenAI client"""
    try:
        from services.llm_client import LLMClientFactory, LLMProvider
        from langchain.schema import HumanMessage, SystemMessage
        
        print("OpenAI Client Example")
        print("=" * 30)
        
        # Create OpenAI client
        client = LLMClientFactory.create_openai_client(
            model="gpt-4",
            api_key=os.getenv("OPENAI_API_KEY", "demo_key")
        )
        
        # Show client info
        info = client.get_model_info()
        print(f"Provider: {info['provider']}")
        print(f"Model: {info['model']}")
        print(f"Has API Key: {info['has_api_key']}")
        
        if info['has_api_key'] and os.getenv("OPENAI_API_KEY"):
            # Test connection
            print("\nTesting connection...")
            connected = await client.test_connection()
            print(f"Connection successful: {connected}")
            
            if connected:
                # Example analysis request
                messages = [
                    SystemMessage(content="You are a code review assistant. Analyze code for potential issues."),
                    HumanMessage(content="""
Please analyze this Python code:

def divide(a, b):
    return a / b

result = divide(10, 0)
print(result)
""")
                ]
                
                print("\nSending analysis request...")
                response = await client.ainvoke(messages, max_tokens=200)
                print(f"Response: {response}")
        else:
            print("No API key provided - skipping actual API calls")
            
    except ImportError:
        print("LLM client requires LangChain dependencies")
        print("This example shows the expected usage structure")


async def example_anthropic_client():
    """Example using Anthropic client"""
    try:
        from services.llm_client import LLMClientFactory
        from langchain.schema import HumanMessage
        
        print("\nAnthropic Client Example")
        print("=" * 30)
        
        # Create Anthropic client
        client = LLMClientFactory.create_anthropic_client(
            api_key=os.getenv("ANTHROPIC_API_KEY", "demo_key")
        )
        
        # Show client info
        info = client.get_model_info()
        print(f"Provider: {info['provider']}")
        print(f"Model: {info['model']}")
        print(f"Has API Key: {info['has_api_key']}")
        
        if info['has_api_key'] and os.getenv("ANTHROPIC_API_KEY"):
            # Test simple request
            messages = [
                HumanMessage(content="What are the key principles of clean code? Please be concise.")
            ]
            
            print("\nSending request...")
            response = await client.ainvoke(messages, max_tokens=150)
            print(f"Response: {response}")
        else:
            print("No API key provided - skipping actual API calls")
            
    except ImportError:
        print("Anthropic client requires LangChain dependencies")


async def example_default_client():
    """Example using default client selection"""
    try:
        from services.llm_client import LLMClientFactory
        
        print("\nDefault Client Example")
        print("=" * 30)
        
        # Try to create default client based on available keys
        try:
            client = LLMClientFactory.create_default_client()
            info = client.get_model_info()
            print(f"Default client created: {info['provider']} ({info['model']})")
            
        except Exception as e:
            print(f"Could not create default client: {e}")
            print("Set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variable")
            
    except ImportError:
        print("Default client requires LangChain dependencies")


async def example_retry_mechanism():
    """Example of retry mechanism"""
    try:
        from services.llm_client import with_retry
        
        print("\nRetry Mechanism Example")
        print("=" * 30)
        
        # Simulate flaky operation
        attempt_count = 0
        
        async def flaky_operation():
            nonlocal attempt_count
            attempt_count += 1
            print(f"Attempt {attempt_count}")
            
            if attempt_count < 3:
                raise Exception("Temporary failure")
            return "Success!"
        
        # Use retry wrapper
        result = await with_retry(
            flaky_operation,
            max_retries=3,
            delay=0.1,  # Short delay for demo
            backoff_factor=1.5
        )
        
        print(f"Final result: {result}")
        
    except Exception as e:
        print(f"Retry example failed: {e}")


def example_client_configuration():
    """Example of different client configurations"""
    try:
        from services.llm_client import LLMClient, LLMProvider
        
        print("\nClient Configuration Examples")
        print("=" * 30)
        
        # Different OpenAI configurations
        configs = [
            {
                "name": "GPT-4 High Creativity",
                "provider": LLMProvider.OPENAI,
                "model": "gpt-4",
                "temperature": 0.8,
                "max_tokens": 1000
            },
            {
                "name": "GPT-3.5 Fast Response",
                "provider": LLMProvider.OPENAI,
                "model": "gpt-3.5-turbo",
                "temperature": 0.1,
                "max_tokens": 500
            },
            {
                "name": "Claude Sonnet Balanced",
                "provider": LLMProvider.ANTHROPIC,
                "model": "claude-3-sonnet-20240229",
                "temperature": 0.3,
                "max_tokens": 1500
            }
        ]
        
        for config in configs:
            client = LLMClient(
                provider=config["provider"],
                model=config["model"],
                api_key="demo_key",
                temperature=config["temperature"],
                max_tokens=config["max_tokens"]
            )
            
            info = client.get_model_info()
            print(f"✓ {config['name']}: {info['provider']} - {info['model']}")
            
    except ImportError:
        print("Configuration examples require LLM client imports")


if __name__ == "__main__":
    print("LLM Client Examples")
    print("=" * 50)
    
    # Check for API keys
    has_openai = bool(os.getenv("OPENAI_API_KEY"))
    has_anthropic = bool(os.getenv("ANTHROPIC_API_KEY"))
    
    print(f"OpenAI API Key available: {has_openai}")
    print(f"Anthropic API Key available: {has_anthropic}")
    print()
    
    # Run examples
    asyncio.run(example_openai_client())
    asyncio.run(example_anthropic_client())
    asyncio.run(example_default_client())
    asyncio.run(example_retry_mechanism())
    example_client_configuration()
    
    print("\nExamples completed!")
    print("\nTo test with real API calls:")
    print("1. Set OPENAI_API_KEY environment variable")
    print("2. Or set ANTHROPIC_API_KEY environment variable")
    print("3. Install dependencies: pip install langchain-openai langchain-anthropic")