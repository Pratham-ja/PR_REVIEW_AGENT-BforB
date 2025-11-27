#!/usr/bin/env python3
"""
Example usage of Logic Analyzer Agent

This example shows how the Logic Analyzer Agent would detect
logical errors and bugs in code changes.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Note: This example requires LangChain dependencies to be installed


def example_logic_analysis():
    """Example of logic analysis on code changes"""
    
    print("Logic Analyzer Agent Example")
    print("=" * 40)
    
    try:
        from agents.logic_analyzer import LogicAnalyzerAgent
        from services.llm_client import LLMClientFactory
        from models import ReviewContext, FileChange, LineChange, ChangeType
        
        # Create LLM client (mock for demo)
        try:
            llm_client = LLMClientFactory.create_default_client()
            print("✓ LLM client created")
        except Exception:
            print("⚠ No LLM API key available - using mock client")
            from unittest.mock import Mock
            llm_client = Mock()
        
        # Create Logic Analyzer Agent
        agent = LogicAnalyzerAgent(llm_client)
        
        # Show agent information
        info = agent.get_agent_info()
        print(f"\nAgent: {info['name']}")
        print(f"Category: {info['category']}")
        print(f"Specialization: {info['specialization']}")
        print(f"Detects: {', '.join(info['detects'][:3])}...")
        
        # Example code changes with logical issues
        examples = [
            {
                "name": "Division by Zero",
                "file": "calculator.py",
                "language": "python",
                "changes": [
                    LineChange(10, "def divide(a, b):", ChangeType.ADD),
                    LineChange(11, "    return a / b", ChangeType.ADD),
                    LineChange(12, "", ChangeType.ADD),
                    LineChange(13, "result = divide(10, 0)", ChangeType.ADD)
                ]
            },
            {
                "name": "Null Pointer Dereference",
                "file": "user_service.js",
                "language": "javascript",
                "changes": [
                    LineChange(5, "function getUserName(user) {", ChangeType.ADD),
                    LineChange(6, "    return user.name.toUpperCase();", ChangeType.ADD),
                    LineChange(7, "}", ChangeType.ADD),
                    LineChange(8, "", ChangeType.ADD),
                    LineChange(9, "const name = getUserName(null);", ChangeType.ADD)
                ]
            },
            {
                "name": "Infinite Loop",
                "file": "processor.java",
                "language": "java",
                "changes": [
                    LineChange(15, "int i = 0;", ChangeType.ADD),
                    LineChange(16, "while (i < 10) {", ChangeType.ADD),
                    LineChange(17, "    System.out.println(i);", ChangeType.ADD),
                    LineChange(18, "    // Missing i++ increment", ChangeType.ADD),
                    LineChange(19, "}", ChangeType.ADD)
                ]
            },
            {
                "name": "Array Index Out of Bounds",
                "file": "data_processor.py",
                "language": "python",
                "changes": [
                    LineChange(20, "def process_data(items):", ChangeType.ADD),
                    LineChange(21, "    for i in range(len(items) + 1):", ChangeType.ADD),
                    LineChange(22, "        print(items[i])", ChangeType.ADD)
                ]
            }
        ]
        
        print(f"\nAnalyzing {len(examples)} code examples...")
        
        for i, example in enumerate(examples, 1):
            print(f"\n{i}. {example['name']} ({example['file']})")
            print("-" * 30)
            
            # Create file change
            file_change = FileChange(
                file_path=example["file"],
                language=example["language"],
                is_binary=False,
                additions=example["changes"],
                deletions=[],
                modifications=[]
            )
            
            # Show the code changes
            print("Code changes:")
            for line in example["changes"]:
                if line.content.strip():  # Skip empty lines
                    print(f"  +{line.line_number}: {line.content}")
            
            # Create review context
            context = ReviewContext(
                file_changes=[file_change],
                language=example["language"],
                config=Mock()
            )
            
            # Show what the agent would analyze
            print(f"\nLanguage: {example['language']}")
            
            # Get language-specific patterns
            patterns = agent.get_logic_patterns()
            if example["language"] in patterns:
                lang_patterns = patterns[example["language"]]
                print(f"Patterns to check: {', '.join(lang_patterns[:3])}...")
            
            # Show expected issues (since we can't run actual LLM)
            expected_issues = {
                "Division by Zero": "Critical: Division by zero on line 11 and 13",
                "Null Pointer Dereference": "High: Null pointer access on line 6",
                "Infinite Loop": "High: Missing loop increment on line 16-19",
                "Array Index Out of Bounds": "Medium: Index out of bounds on line 21-22"
            }
            
            if example["name"] in expected_issues:
                print(f"Expected finding: {expected_issues[example['name']]}")
        
        # Show system prompt excerpt
        print(f"\nSystem Prompt Excerpt:")
        print("-" * 30)
        prompt = agent.get_system_prompt()
        lines = prompt.split('\n')[:10]  # First 10 lines
        for line in lines:
            if line.strip():
                print(f"  {line.strip()}")
        print("  ...")
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("This example requires the full agent implementation")
        
        # Show basic logic patterns without full implementation
        print("\nLogic Analysis Patterns:")
        print("-" * 30)
        
        patterns = {
            "python": ["None checks", "Division by zero", "Index bounds"],
            "javascript": ["Null/undefined checks", "Type coercion", "Async issues"],
            "java": ["NullPointerException", "Array bounds", "Resource leaks"],
            "cpp": ["Null pointers", "Memory leaks", "Buffer overflows"]
        }
        
        for lang, pattern_list in patterns.items():
            print(f"{lang.upper()}: {', '.join(pattern_list)}")


def example_severity_levels():
    """Example of different severity levels for logic issues"""
    
    print("\nLogic Issue Severity Examples")
    print("=" * 40)
    
    severity_examples = [
        {
            "level": "CRITICAL",
            "description": "Will definitely cause crashes or data corruption",
            "examples": [
                "Dereferencing null pointer",
                "Division by zero",
                "Buffer overflow",
                "Use after free"
            ]
        },
        {
            "level": "HIGH", 
            "description": "Likely to cause runtime errors",
            "examples": [
                "Array index out of bounds",
                "Missing null checks",
                "Infinite loops",
                "Resource leaks"
            ]
        },
        {
            "level": "MEDIUM",
            "description": "Could cause issues under certain conditions", 
            "examples": [
                "Off-by-one errors",
                "Missing error handling",
                "Race conditions",
                "Type conversion issues"
            ]
        },
        {
            "level": "LOW",
            "description": "Minor logical inconsistencies",
            "examples": [
                "Unreachable code",
                "Redundant conditions",
                "Missing return statements",
                "Unused variables"
            ]
        }
    ]
    
    for severity in severity_examples:
        print(f"\n{severity['level']}:")
        print(f"  {severity['description']}")
        print("  Examples:")
        for example in severity['examples']:
            print(f"    • {example}")


if __name__ == "__main__":
    example_logic_analysis()
    example_severity_levels()
    
    print("\nLogic Analyzer Example completed!")
    print("\nTo run with real analysis:")
    print("1. Set OPENAI_API_KEY or ANTHROPIC_API_KEY")
    print("2. Install dependencies: pip install langchain-openai")
    print("3. The agent will analyze code and return JSON findings")