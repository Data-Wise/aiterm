# iTerm2 Profile Creation Guide

**Step-by-step instructions with screenshots guidance**

---

## Overview

You need to create 4 profiles. Each takes ~3-4 minutes.

**Profiles to create:**
1. R-Dev (blue theme)
2. AI-Session (purple theme)
3. Focus (minimal dark)
4. Production (red theme)

---

## Opening Profile Preferences

### Step 1: Open iTerm2 Preferences
- Click **iTerm2** in menu bar
- Select **Preferences...** (or press `⌘,`)

### Step 2: Navigate to Profiles
- Click **Profiles** tab at the top
- You'll see a list of existing profiles on the left

---

## Profile 1: R-Dev (Blue Theme)

### Step 1: Duplicate Default Profile
1. In the profiles list (left side), select **Default**
2. Click the **+** button at the bottom left
3. Select **Duplicate Profile** from dropdown
4. A new profile appears named "Default copy"

### Step 2: Rename Profile
1. Double-click "Default copy" in the list
2. Type: `R-Dev`
3. Press Enter

### Step 3: Set Colors (Blue Theme)
1. With "R-Dev" selected, click **Colors** tab
2. Click **Color Presets...** dropdown (bottom right)
3. Select **Solarized Dark**
4. Optional: Adjust for more blue:
   - Click on "Background" color square
   - Shift slightly toward blue (#001520 or similar)

### Step 4: Configure Badge
1. Click **General** tab
2. Find "Badge" field (in General tab)
3. Check ☑️ **Show badge**
4. In the text field, type: `📦`
5. Badge position: **Top Right** (default is fine)

### Step 5: Verify
- Profile name: `R-Dev` (exact spelling, case-sensitive)
- Colors: Blue/dark theme
- Badge: 📦 visible in preview

✅ **R-Dev profile complete!**

---

## Profile 2: AI-Session (Purple Theme)

### Step 1: Create New Profile
1. Click **+** button (bottom left)
2. Select **Duplicate Profile**
3. Rename to: `AI-Session`

### Step 2: Set Colors (Purple Theme)
1. Click **Colors** tab
2. Click **Color Presets...** dropdown
3. Select **Tango Dark** (has purple tones)
4. Alternative presets:
   - **Pastel (Dark Background)**
   - **Solarized Dark** (adjust toward purple)

### Step 3: Configure Badge
1. Click **General** tab
2. Check ☑️ **Show badge**
3. Badge text: `🤖`
4. Position: **Top Right**

### Step 4: Verify
- Profile name: `AI-Session` (exact spelling)
- Colors: Purple/dark theme
- Badge: 🤖

✅ **AI-Session profile complete!**

---

## Profile 3: Focus (Minimal Dark)

### Step 1: Create New Profile
1. Click **+** button
2. Select **Duplicate Profile**
3. Rename to: `Focus`

### Step 2: Set Colors (Minimal Dark)
1. Click **Colors** tab
2. Click **Color Presets...** dropdown
3. Select **Smoooooth** (very minimal)
4. Alternatives:
   - **Dark Background**
   - **Solarized Dark** (reduce contrast)

### Step 3: Configure Badge
1. Click **General** tab
2. Check ☑️ **Show badge**
3. Badge text: `🎯`
4. Position: **Top Right**

### Step 4: Optional - Minimize Distractions
1. Click **Window** tab
2. Check ☑️ **Hide scrollbar**
3. Transparency: Opaque (0% transparent)

### Step 5: Verify
- Profile name: `Focus` (exact spelling)
- Colors: Very dark, minimal
- Badge: 🎯
- Optional: No scrollbar

✅ **Focus profile complete!**

---

## Profile 4: Production (Red Theme)

### Step 1: Create New Profile
1. Click **+** button
2. Select **Duplicate Profile**
3. Rename to: `Production`

### Step 2: Set Colors (Red Theme)
1. Click **Colors** tab
2. Click **Color Presets...** dropdown
3. Select **Red Sands**
4. Alternatives:
   - **Red Alert** (if available)
   - Manually adjust: Click "Background" → shift toward red (#200000)

### Step 3: Configure Badge
1. Click **General** tab
2. Check ☑️ **Show badge**
3. Badge text: `🔴`
4. Position: **Top Right**

### Step 4: Make It Stand Out (Warning Colors)
1. Still in **Colors** tab
2. Consider making cursor red/bright
3. Bold text color: Bright red
4. Goal: Obvious "danger zone" feeling

### Step 5: Verify
- Profile name: `Production` (exact spelling)
- Colors: Red/warning theme
- Badge: 🔴
- Feels like "danger zone"

✅ **Production profile complete!**

---

## Verification Checklist

After creating all 4 profiles, verify:

- [ ] **R-Dev** exists (blue theme, 📦 badge)
- [ ] **AI-Session** exists (purple theme, 🤖 badge)
- [ ] **Focus** exists (minimal dark, 🎯 badge)
- [ ] **Production** exists (red theme, 🔴 badge)
- [ ] All names spelled exactly as shown (case-sensitive)
- [ ] All badges enabled and visible

---

## Testing Profiles Manually

### Test Profile Switching

1. Open new iTerm2 window
2. In menu bar: **Profiles** → Select **R-Dev**
3. Window should change to blue theme with 📦 badge
4. Repeat for other profiles

### Expected Results

| Profile | Theme Color | Badge | Feel |
|---------|-------------|-------|------|
| R-Dev | Blue/dark | 📦 | Calm, focused |
| AI-Session | Purple/dark | 🤖 | Creative, AI work |
| Focus | Very dark | 🎯 | Minimal, distraction-free |
| Production | Red/dark | 🔴 | Warning, careful! |

---

## Troubleshooting

### Badge Not Showing?
1. General tab → Check ☑️ **Show badge**
2. Make sure badge text field has emoji
3. Try different position (Top Right, Bottom Right)

### Colors Look Wrong?
1. Colors tab → Try different preset
2. Click **Color Presets...** → **Import...**
3. Download more themes from iTerm2 color schemes

### Profile Not Found Error?
- Verify exact spelling: `R-Dev`, `AI-Session`, `Focus`, `Production`
- Case-sensitive! `r-dev` won't work
- No extra spaces

---

## Color Preset Recommendations

If default presets don't work well:

### For R-Dev (Blue)
- **Solarized Dark** (classic)
- **Ocean** (if available)
- **Cobalt2** (bright blue)

### For AI-Session (Purple)
- **Tango Dark** (purple tones)
- **Pastel (Dark Background)**
- **Grape** (if available)

### For Focus (Minimal)
- **Smoooooth** (very clean)
- **Dark Background** (simple)
- **Minimal** (if available)

### For Production (Red)
- **Red Sands** (classic red)
- **Red Alert** (if available)
- Custom: Background #200000, Foreground #ff8888

---

## Next Steps

After creating all 4 profiles:

1. ✅ Close Preferences
2. ✅ Continue to [setup-guide.md](setup-guide.md) Step 2
3. ✅ Enable auto-switching by adding to `~/.config/zsh/.zshrc`

---

## Screenshots Reference

**Where to find things:**

```
iTerm2 Preferences Window
├── Profiles tab (top)
│   ├── Profile list (left sidebar)
│   │   ├── + button (bottom left) → Create new
│   │   └── Profile names (double-click to rename)
│   │
│   └── Profile settings (right side)
│       ├── General tab
│       ├── Colors tab ← Set theme here
│       │   └── Color Presets... (bottom right)
│       ├── Text tab
│       ├── Window tab
│       ├── Session tab ← Set badge here
│       │   └── Badge section (middle)
│       └── ...
```

---

**Time:** 15 minutes total (~3-4 min per profile)  
**Difficulty:** Easy (just clicking and typing)  
**Required:** Yes (auto-switching won't work without these)

---

## 🔄 Recent Update (2024-2025)

**Badge location changed in recent iTerm2 versions!**

**Old location (pre-3.4):** Session tab  
**New location (3.4+):** General tab

All instructions in this guide reflect the **current** location (General tab).

---

## Visual Guide

**Where to find Badge setting:**

```
iTerm2 Preferences
└── Profiles tab
    └── [Select your profile]
        └── General tab ← YOU ARE HERE
            ├── Name
            ├── Command
            ├── Working Directory
            ├── Badge ← SET BADGE TEXT HERE
            │   └── Edit... ← Configure appearance
            └── ...
```

**Badge field location:**
- In **General** tab (first tab when you select a profile)
- Scroll down if needed
- Look for text field labeled "Badge"
- Enter emoji or text directly

**Badge appearance settings (Edit... button):**
- Position: Top Right, Bottom Right, etc.
- Maximum size: Percentage of window
- Typeface: Font selection

---

**Last Updated:** 2025-12-13  
**iTerm2 Version:** 3.4+ (latest)
