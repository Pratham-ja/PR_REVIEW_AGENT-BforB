#!/usr/bin/env python3
"""
Example usage of Readability Analyzer Agent

This example shows how the Readability Analyzer Agent would evaluate
code clarity and maintainability in code changes.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Note: This example requires LangChain dependencies to be installed


def example_readability_analysis():
    """Example of readability analysis on code changes"""
    
    print("Readability Analyzer Agent Example")
    print("=" * 40)
    
    try:
        from agents.readability_analyzer import ReadabilityAnalyzerAgent
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
        
        # Create Readability Analyzer Agent
        agent = ReadabilityAnalyzerAgent(llm_client)
        
        # Show agent information
        info = agent.get_agent_info()
        print(f"\nAgent: {info['name']}")
        print(f"Category: {info['category']}")
        print(f"Specialization: {info['specialization']}")
        print(f"Evaluates: {', '.join(info['evaluates'][:3])}...")
        print(f"Requires suggestions: {info['requires_suggestions']}")
        
        # Example code changes with readability issues
        examples = [
            {
                "name": "Poor Variable Names",
                "file": "data_processor.py",
                "language": "python",
                "changes": [
                    LineChange(5, "def process(d):", ChangeType.ADD),
                    LineChange(6, "    x = d['items']", ChangeType.ADD),
                    LineChange(7, "    temp = []", ChangeType.ADD),
                    LineChange(8, "    for i in x:", ChangeType.ADD),
                    LineChange(9, "        temp.append(i * 2)", ChangeType.ADD),
                    LineChange(10, "    return temp", ChangeType.ADD)
                ]
            },
            {
                "name": "Deep Nesting",
                "file": "validator.js",
                "language": "javascript",
                "changes": [
                    LineChange(10, "function validateUser(user) {", ChangeType.ADD),
                    LineChange(11, "    if (user) {", ChangeType.ADD),
                    LineChange(12, "        if (user.name) {", ChangeType.ADD),
                    LineChange(13, "            if (user.name.length > 0) {", ChangeType.ADD),
                    LineChange(14, "                if (user.email) {", ChangeType.ADD),
                    LineChange(15, "                    if (user.email.includes('@')) {", ChangeType.ADD),
                    LineChange(16, "                        return true;", ChangeType.ADD),
                    LineChange(17, "                    }", ChangeType.ADD),
                    LineChange(18, "                }", ChangeType.ADD),
                    LineChange(19, "            }", ChangeType.ADD),
                    LineChange(20, "        }", ChangeType.ADD),
                    LineChange(21, "    }", ChangeType.ADD),
                    LineChange(22, "    return false;", ChangeType.ADD),
                    LineChange(23, "}", ChangeType.ADD)
                ]
            },
            {
                "name": "Long Parameter List",
                "file": "calculator.java",
                "language": "java",
                "changes": [
                    LineChange(15, "public double calculate(double a, double b, double c, double d, double e, double f, String operation, boolean useCache) {", ChangeType.ADD),
                    LineChange(16, "    // Complex calculation logic", ChangeType.ADD),
                    LineChange(17, "    return a + b + c + d + e + f;", ChangeType.ADD),
                    LineChange(18, "}", ChangeType.ADD)
                ]
            },
            {
                "name": "Magic Numbers",
                "file": "config.py",
                "language": "python",
                "changes": [
                    LineChange(20, "def setup_connection():", ChangeType.ADD),
                    LineChange(21, "    timeout = 30000", ChangeType.ADD),
                    LineChange(22, "    max_retries = 5", ChangeType.ADD),
                    LineChange(23, "    buffer_size = 8192", ChangeType.ADD),
                    LineChange(24, "    if response_time > 2500:", ChangeType.ADD),
                    LineChange(25, "        return False", ChangeType.ADD)
                ]
            },
            {
                "name": "Missing Documentation",
                "file": "utils.py",
                "language": "python",
                "changes": [
                    LineChange(30, "def complex_algorithm(data, threshold, weights):", ChangeType.ADD),
                    LineChange(31, "    result = []", ChangeType.ADD),
                    LineChange(32, "    for item in data:", ChangeType.ADD),
                    LineChange(33, "        score = sum(w * item[i] for i, w in enumerate(weights))", ChangeType.ADD),
                    LineChange(34, "        if score > threshold:", ChangeType.ADD),
                    LineChange(35, "            result.append((item, score))", ChangeType.ADD),
                    LineChange(36, "    return sorted(result, key=lambda x: x[1], reverse=True)", ChangeType.ADD)
                ]
            }
        ]
        
        print(f"\nAnalyzing {len(examples)} readability examples...")
        
        for i, example in enumerate(examples, 1):
            print(f"\n{i}. {example['name']} ({example['file']})")
            print("-" * 40)
            
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
            
            # Analyze complexity
            try:
                complexity_insights = agent._analyze_complexity(context)
                
                print(f"\nComplexity Analysis:")
                if complexity_insights["deep_nesting"]:
                    print(f"  • Deep nesting: {len(complexity_insights['deep_nesting'])} instances")
                if complexity_insights["magic_numbers"]:
                    print(f"  • Magic numbers: {len(complexity_insights['magic_numbers'])} found")
                if complexity_insights["poor_names"]:
                    print(f"  • Poor names: {len(complexity_insights['poor_names'])} found")
                if complexity_insights["long_parameter_lists"]:
                    print(f"  • Long parameter lists: {len(complexity_insights['long_parameter_lists'])} found")
                
                if not any(complexity_insights.values()):
                    print("  • No complexity issues detected in pre-analysis")
                
            except Exception as e:
                print(f"  • Complexity analysis error: {e}")
            
            # Show language-specific patterns
            patterns = agent.get_readability_patterns()
            if example["language"] in patterns:
                lang_patterns = patterns[example["language"]]
                print(f"\nLanguage patterns ({example['language']}):")
                for pattern in lang_patterns[:3]:
                    print(f"  • {pattern}")
            
            # Show expected readability issues
            expected_issues = {
                "Poor Variable Names": "Variables 'd', 'x', 'temp', 'i' are not descriptive",
                "Deep Nesting": "5 levels of nesting make code hard to follow",
                "Long Parameter List": "8 parameters exceed recommended limit of 5-7",
                "Magic Numbers": "Numbers 30000, 5, 8192, 2500 should be named constants",
                "Missing Documentation": "Complex algorithm lacks docstring and comments"
            }
            
            if example["name"] in expected_issues:
                print(f"\nExpected issues: {expected_issues[example['name']]}")
                
                # Show suggested improvements
                suggestions = {
                    "Poor Variable Names": "Rename to: process_data(data_dict), items=data_dict['items'], processed_items=[], item",
                    "Deep Nesting": "Use early returns: if (!user?.name?.length) return false; if (!user?.email?.includes('@')) return false;",
                    "Long Parameter List": "Create a CalculationConfig class to group related parameters",
                    "Magic Numbers": "Define constants: TIMEOUT_MS=30000, MAX_RETRIES=5, BUFFER_SIZE=8192",
                    "Missing Documentation": "Add docstring explaining algorithm purpose, parameters, and return value"
                }
                
                if example["name"] in suggestions:
                    print(f"Suggested fix: {suggestions[example['name']]}")
        
        # Show readability patterns by language
        print(f"\nReadability Patterns by Language:")
        print("-" * 40)
        patterns = agent.get_readability_patterns()
        for lang, pattern_list in patterns.items():
            print(f"\n{lang.upper()}:")
            for pattern in pattern_list:
                print(f"  • {pattern}")
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("This example requires the full agent implementation")
        
        # Show basic readability concepts
        print("\nReadability Analysis Concepts:")
        print("-" * 40)
        
        concepts = {
            "Function Complexity": ["Cyclomatic complexity", "Function length", "Single responsibility"],
            "Naming": ["Descriptive names", "Consistent conventions", "Avoid abbreviations"],
            "Structure": ["Avoid deep nesting", "Limit parameters", "Clear organization"],
            "Documentation": ["Docstrings", "Inline comments", "Type hints"],
        }
        
        for category, items in concepts.items():
            print(f"{category}: {', '.join(items)}")


def example_readability_metrics():
    """Example of readability metrics and thresholds"""
    
    print("\nReadability Metrics and Thresholds")
    print("=" * 40)
    
    metrics = [
        {
            "metric": "Function Length",
            "threshold": "< 50 lines (Python), < 30 lines (JavaScript)",
            "rationale": "Shorter functions are easier to understand and test"
        },
        {
            "metric": "Cyclomatic Complexity",
            "threshold": "< 10 (ideally < 5)",
            "rationale": "Lower complexity reduces cognitive load"
        },
        {
            "metric": "Nesting Depth",
            "threshold": "< 4 levels",
            "rationale": "Deep nesting hurts readability and maintainability"
        },
        {
            "metric": "Parameter Count",
            "threshold": "< 5-7 parameters",
            "rationale": "Too many parameters indicate design issues"
        },
        {
            "metric": "Variable Name Length",
            "threshold": "> 3 characters (except loop counters)",
            "rationale": "Descriptive names improve code clarity"
        }
    ]
    
    for metric in metrics:
        print(f"\n{metric['metric']}:")
        print(f"  Threshold: {metric['threshold']}")
        print(f"  Why: {metric['rationale']}")


if __name__ == "__main__":
    example_readability_analysis()
    example_readability_metrics()
    
    print("\nReadability Analyzer Example completed!")
    print("\nKey Benefits:")
    print("• Improves code maintainability")
    print("• Reduces onboarding time for new developers")
    print("• Prevents technical debt accumulation")
    print("• Enhances team collaboration")
    print("\nTo run with real analysis:")
    print("1. Set OPENAI_API_KEY or ANTHROPIC_API_KEY")
    print("2. Install dependencies: pip install langchain-openai")
    print("3. The agent will provide specific improvement suggestions")