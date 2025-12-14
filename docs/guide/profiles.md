# iTerm2 Profiles

Configure iTerm2 profiles for visual context switching.

## Required Profiles

| Profile Name | Purpose | Background Color |
|--------------|---------|------------------|
| Default | Fallback | Your preference |
| R-Dev | R packages | Green (#134F3C) |
| Python-Dev | Python projects | Green (#137746) |
| Node-Dev | Node.js projects | Dark (#121212) |
| AI-Session | Claude/Gemini | Purple |
| Production | Production warning | Red |

## Creating Profiles Manually

1. Open iTerm2 → Settings → Profiles
2. Select "Default" → Click "+" to duplicate
3. Rename to profile name (e.g., "R-Dev")
4. Customize colors under "Colors" tab

## Using Dynamic Profiles

Dynamic Profiles auto-load from JSON files.

### Install Profiles

Copy the included profiles:

```bash
cp profiles/context-switcher-profiles.json \
   ~/Library/Application\ Support/iTerm2/DynamicProfiles/
```

### Included Dynamic Profiles

- **Python-Dev** - Grass theme (green jungle)
- **Node-Dev** - Citruszest theme (dark with yellow accents)

### Creating Custom Dynamic Profiles

Create a JSON file in `~/Library/Application Support/iTerm2/DynamicProfiles/`:

```json
{
  "Profiles": [
    {
      "Name": "My-Profile",
      "Guid": "unique-id-here",
      "Dynamic Profile Parent Name": "Default",
      "Background Color": {
        "Red Component": 0.1,
        "Green Component": 0.1,
        "Blue Component": 0.1
      }
    }
  ]
}
```

## Profile Colors Reference

| Profile | Hex | RGB |
|---------|-----|-----|
| R-Dev (green) | #134F3C | 19, 79, 60 |
| Python-Dev | #137746 | 19, 119, 70 |
| Node-Dev | #121212 | 18, 18, 18 |
| Production | #8B0000 | 139, 0, 0 |
