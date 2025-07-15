# AI Chatbot CSS Troubleshooting Guide

## Issue: AI Chatbot CSS Not Showing

### Quick Fixes to Try First:

1. **Hard Refresh Browser**
   - Press `Ctrl + F5` (Windows) or `Cmd + Shift + R` (Mac)
   - This forces the browser to reload all assets, bypassing cache

2. **Clear Browser Cache**
   - Open Dev Tools (F12)
   - Right-click the refresh button → "Empty Cache and Hard Reload"

3. **Check Browser Console**
   - Open Dev Tools (F12)
   - Go to Console tab
   - Look for any red errors related to CSS loading

### Diagnostic Steps:

#### Step 1: Verify Server is Running
```bash
# Start the server
python -m uvicorn main:app --reload --port 8000

# Or use the helper script
.\fix_css_and_start.ps1
```

#### Step 2: Test CSS Loading Directly
1. Open browser to: `http://localhost:8000/static/styles.css`
2. You should see the CSS file content
3. If you get 404 error, static files aren't being served correctly

#### Step 3: Check Network Tab
1. Open `http://localhost:8000/browse`
2. Open Dev Tools (F12) → Network tab
3. Refresh page
4. Look for `styles.css` request:
   - ✅ Status 200 = CSS loaded successfully
   - ❌ Status 404 = CSS file not found
   - ❌ Status 500 = Server error

#### Step 4: Inspect Elements
1. Right-click on the AI chat area
2. Select "Inspect Element"
3. Check if classes like `ai-chat-container` are present
4. In the Styles panel, verify CSS rules are applied

### Common Causes & Solutions:

#### 1. Browser Cache Issues
**Problem**: Old CSS is cached
**Solution**: 
- Hard refresh (Ctrl+F5)
- Clear browser cache
- Try incognito/private browsing mode

#### 2. Static File Path Issues
**Problem**: CSS not loading from `/static/styles.css`
**Check**: 
```python
# In main.py, verify this line exists:
app.mount("/static", StaticFiles(directory="static"), name="static")
```

#### 3. CSS Syntax Errors
**Problem**: Malformed CSS breaks loading
**Solution**: 
- Validate CSS syntax
- Check browser console for CSS parsing errors

#### 4. Missing CSS Classes
**Problem**: HTML uses classes not defined in CSS
**Check**: Template uses these classes:
- `.ai-chat-container`
- `.ai-chat-header`
- `.ai-chat-messages`
- `.ai-toggle-btn`

#### 5. CSS Specificity Issues
**Problem**: Other CSS rules override AI chatbot styles
**Solution**: Check for conflicting styles in Dev Tools

### Testing the Fix:

#### Test 1: Direct CSS Access
Visit: `http://localhost:8000/static/styles.css`
Expected: CSS file content displayed

#### Test 2: Browse Page Load
Visit: `http://localhost:8000/browse`
Expected: Page loads with styled AI chatbot toggle button

#### Test 3: AI Chatbot Styling
1. Click "Chat with AI" button
2. Chat container should appear with:
   - Dark background (#1a1a1a)
   - Gold header text (#f5c518)
   - Styled input and buttons

### Files to Check:

1. **`static/styles.css`** - Contains AI chatbot CSS (lines ~1140-1494)
2. **`templates/base.html`** - Has CSS link: `<link rel="stylesheet" href="/static/styles.css">`
3. **`templates/browse_movies.html`** - Uses AI chatbot classes
4. **`main.py`** - Mounts static files correctly

### Debug Commands:

```bash
# Check file exists
ls static/styles.css

# Check file size (should be ~1494 lines)
wc -l static/styles.css

# Search for AI CSS classes
grep -n "ai-chat-container" static/styles.css

# Start server with debug output
python -m uvicorn main:app --reload --log-level debug
```

### Still Not Working?

If CSS is still not showing after trying all above steps:

1. **Create minimal test**: Use `test_css_server.py` to isolate the issue
2. **Check file permissions**: Ensure `static/styles.css` is readable
3. **Try different browser**: Test in Chrome, Firefox, Edge
4. **Check antivirus/firewall**: May be blocking local server
5. **Restart server**: Kill all Python processes and restart

### Success Indicators:

✅ **CSS is working when you see:**
- AI toggle button has gold background (#f5c518)
- Chat container has dark background
- Messages have proper spacing and avatars
- Scrollbar is styled (dark theme)
- Hover effects work on buttons

❌ **CSS is not working when you see:**
- Plain white/unstyled buttons
- Basic HTML default styling
- No background colors or gradients
- Cramped text with default spacing

---

**Need More Help?**
1. Check browser console for specific error messages
2. Take screenshot of the unstyled chatbot
3. Run `diagnose_css.py` for automated checks
