#!/usr/bin/env python3
"""
Diagnose CSS loading issues for the AI chatbot
"""
import os
from pathlib import Path

def check_css_issues():
    """Check for common CSS loading issues"""
    
    print("🔍 Diagnosing AI Chatbot CSS Issues")
    print("=" * 50)
    
    # Check if static directory exists
    static_dir = Path("static")
    if not static_dir.exists():
        print("❌ static/ directory not found!")
        return
    print("✅ static/ directory exists")
    
    # Check if styles.css exists
    css_file = static_dir / "styles.css"
    if not css_file.exists():
        print("❌ static/styles.css not found!")
        return
    print("✅ static/styles.css exists")
    
    # Check CSS file size
    css_size = css_file.stat().st_size
    print(f"📊 CSS file size: {css_size} bytes")
    
    # Check for AI chatbot CSS classes
    with open(css_file, 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    required_classes = [
        ".ai-chat-container",
        ".ai-chat-header", 
        ".ai-chat-messages",
        ".ai-message",
        ".ai-toggle-btn"
    ]
    
    print("\n🎨 Checking for AI chatbot CSS classes:")
    for css_class in required_classes:
        if css_class in css_content:
            print(f"✅ {css_class} found in CSS")
        else:
            print(f"❌ {css_class} missing from CSS")
    
    # Check template file
    template_file = Path("templates/browse_movies.html")
    if not template_file.exists():
        print("❌ templates/browse_movies.html not found!")
        return
    print("\n✅ templates/browse_movies.html exists")
    
    # Check template for CSS link
    with open(template_file, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    print("\n🔗 Checking template CSS references:")
    if 'ai-chat-container' in template_content:
        print("✅ AI chatbot HTML structure found in template")
    else:
        print("❌ AI chatbot HTML structure missing from template")
    
    # Check base template for CSS link
    base_template = Path("templates/base.html")
    if base_template.exists():
        with open(base_template, 'r', encoding='utf-8') as f:
            base_content = f.read()
        
        if '/static/styles.css' in base_content:
            print("✅ CSS link found in base.html")
        else:
            print("❌ CSS link missing from base.html")
    
    print("\n💡 Potential Solutions:")
    print("1. Clear browser cache (Ctrl+F5)")
    print("2. Check browser developer tools for CSS loading errors")
    print("3. Verify the server is serving static files correctly")
    print("4. Ensure the CSS file has proper permissions")
    
    print("\n🌐 Test URL: http://localhost:8000/browse")
    print("📝 Open browser dev tools (F12) and check:")
    print("   - Network tab for CSS loading")
    print("   - Console for any errors")
    print("   - Elements tab to verify CSS classes are applied")

if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    check_css_issues()
