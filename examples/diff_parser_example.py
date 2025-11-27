#!/usr/bin/env python3
"""
Example usage of DiffParser

This example shows how to use the DiffParser to parse git diff content
into structured format for analysis.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Note: This example requires the unidiff dependency to be installed
# For demonstration, we'll show the expected usage

def example_diff_parsing():
    """Example of parsing diff content"""
    
    # Sample git diff content
    sample_diff = """diff --git a/calculator.py b/calculator.py
new file mode 100644
index 0000000..d00491f
--- /dev/null
+++ b/calculator.py
@@ -0,0 +1,8 @@
+def add(a, b):
+    return a + b
+
+def subtract(a, b):
+    return a - b
+
+def multiply(a, b):
+    return a * b

diff --git a/main.py b/main.py
index 1234567..abcdefg 100644
--- a/main.py
+++ b/main.py
@@ -1,3 +1,6 @@
+from calculator import add, subtract
+
 def main():
-    print("Hello World")
+    result = add(5, 3)
+    print(f"5 + 3 = {result}")
     return

diff --git a/image.png b/image.png
new file mode 100644
index 0000000..1234567
Binary files /dev/null and b/image.png differ
"""
    
    try:
        from services.diff_parser import DiffParser
        
        # Initialize parser
        parser = DiffParser()
        
        # Parse the diff
        parsed_diff = parser.parse(sample_diff)
        
        print("Diff Parsing Results:")
        print("=" * 40)
        
        # Show overall statistics
        stats = parser.get_file_stats(parsed_diff)
        print(f"Total files: {stats['total_files']}")
        print(f"Text files: {stats['text_files']}")
        print(f"Binary files: {stats['binary_files']}")
        print(f"Total additions: {stats['total_additions']}")
        print(f"Total deletions: {stats['total_deletions']}")
        print(f"Languages: {', '.join(stats['languages'].keys())}")
        print()
        
        # Show details for each file
        for i, file_change in enumerate(parsed_diff.files, 1):
            print(f"File {i}: {file_change.file_path}")
            print(f"  Language: {file_change.language}")
            print(f"  Binary: {file_change.is_binary}")
            
            if not file_change.is_binary:
                print(f"  Additions: {len(file_change.additions)}")
                print(f"  Deletions: {len(file_change.deletions)}")
                print(f"  Modifications: {len(file_change.modifications)}")
                
                # Show some addition content
                if file_change.additions:
                    print("  Added lines:")
                    for line in file_change.additions[:3]:  # Show first 3
                        print(f"    +{line.line_number}: {line.content}")
                    if len(file_change.additions) > 3:
                        print(f"    ... and {len(file_change.additions) - 3} more")
                
                # Show changed content
                changed_content = parser.get_changed_lines_content(file_change)
                if changed_content:
                    print(f"  Changed content ({len(changed_content)} lines):")
                    for content in changed_content[:2]:  # Show first 2
                        print(f"    {content}")
                    if len(changed_content) > 2:
                        print(f"    ... and {len(changed_content) - 2} more")
            
            print()
        
        # Demonstrate filtering by language
        python_files = parser.filter_by_language(parsed_diff, ["python"])
        print(f"Python files only: {len(python_files.files)} files")
        for file_change in python_files.files:
            print(f"  - {file_change.file_path}")
        
    except ImportError:
        print("DiffParser requires 'unidiff' dependency to be installed")
        print("This example shows the expected usage structure")
        
        # Show language detection without full parser
        from services.diff_parser import DiffParser
        parser = DiffParser()
        
        test_files = ["calculator.py", "main.py", "image.png", "style.css"]
        print("\nLanguage Detection Demo:")
        for file_path in test_files:
            language = parser.detect_language(file_path)
            is_binary = parser._is_binary_file(file_path)
            print(f"  {file_path}: {language} (binary: {is_binary})")


def example_language_detection():
    """Example of language detection capabilities"""
    
    try:
        from services.diff_parser import DiffParser
        parser = DiffParser()
        
        # Test various file types
        test_files = [
            "app.py", "main.js", "component.tsx", "style.css",
            "README.md", "Dockerfile", "config.json", "script.sh",
            "Main.java", "program.cpp", "image.jpg", "document.pdf"
        ]
        
        print("Language Detection Examples:")
        print("=" * 30)
        
        for file_path in test_files:
            language = parser.detect_language(file_path)
            is_binary = parser._is_binary_file(file_path)
            
            status = "📄" if not is_binary else "📁"
            print(f"{status} {file_path:<15} -> {language}")
        
    except ImportError:
        print("Language detection requires DiffParser to be available")


if __name__ == "__main__":
    print("Diff Parser Examples")
    print("=" * 50)
    
    print("\n1. Language Detection:")
    example_language_detection()
    
    print("\n2. Diff Parsing:")
    example_diff_parsing()
    
    print("\nExample completed!")