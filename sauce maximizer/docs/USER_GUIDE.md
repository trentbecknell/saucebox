# SauceMax User Guide

This guide covers how to use SauceMax to enhance your mixes in Reaper and other DAWs.

## Getting Started

### What is SauceMax?

SauceMax is an intelligent audio plugin that analyzes your mixes and suggests the perfect "recipe" for professional-sounding results. It uses machine learning to detect what your mix needs and automatically applies the right processing.

**"Sauce"** in music production refers to that special something that makes a mix sound polished and professional - the sonic enhancement that takes a good mix and makes it great.

### First Launch

1. **Install SauceMax** following the installation guide
2. **Open Reaper** and load a project with audio
3. **Run SauceMax**: Actions → SauceMax → Launch SauceMax
4. **You'll see the SauceMax interface** with these main buttons:
   - 🎛️ **Quick Sauce** - One-click analysis and processing
   - 📊 **Analyze Mix** - Analysis only, no processing
   - Processing chains: **⚖️ Balanced**, **✨ Bright**, **🔥 Warm**

## Using SauceMax

### Quick Sauce (Recommended for Beginners)

The fastest way to improve your mix:

1. **Select the track** you want to enhance (or use none for master bus)
2. **Click "Quick Sauce"**
3. **Wait for analysis** (10-30 seconds depending on track length)
4. **SauceMax automatically applies** the best processing chain
5. **Listen to the result** and compare with bypass

**Quick Sauce** analyzes your audio and applies:
- EQ adjustments for frequency balance
- Compression for dynamics control
- Enhancement effects as needed

### Manual Analysis Workflow

For more control over the process:

1. **Click "Analyze Mix"** to run analysis without processing
2. **Review the analysis results** in the popup window
3. **Choose a processing chain** based on the suggestions:
   - **Balanced**: General-purpose enhancement
   - **Bright**: Adds clarity and high-frequency presence
   - **Warm**: Adds low-end warmth and vintage character

### Understanding Analysis Results

SauceMax provides detailed feedback about your mix:

```
SauceMax Analysis Results: Lead Vocal

OVERALL ASSESSMENT:
Recommended Processing: BRIGHT
Confidence: 78%

FREQUENCY ANALYSIS:
Spectral Centroid: 2400 Hz
RMS Energy: 0.182
Dynamic Range: 0.654
Stereo Width: 0.45

PROCESSING SUGGESTIONS:
EQ ADJUSTMENTS:
• High Shelf: +2.1dB @ 8000Hz
• Low Shelf: +1.2dB @ 100Hz

COMPRESSION:
• Threshold: -15.2dB
• Ratio: 3.2:1
• Attack: 12.5ms
• Release: 85.0ms
```

#### Key Metrics Explained

- **Confidence**: How sure SauceMax is about its suggestions (>70% is good)
- **Spectral Centroid**: Brightness measure (higher = brighter)
- **RMS Energy**: Overall level (0.1-0.5 is typical for individual tracks)
- **Dynamic Range**: How compressed the audio is (higher = more dynamic)
- **Stereo Width**: How wide the stereo image is (0.5 is centered)

## Processing Chains Explained

### ⚖️ Balanced Chain
**Best for**: General-purpose enhancement, full mixes, need overall improvement

**What it does**:
- Gentle EQ to balance frequency response
- Moderate compression to control dynamics
- Subtle enhancement for clarity

**Use when**:
- Your mix sounds "okay" but needs polish
- You want safe, professional-sounding results
- Working on the master bus

### ✨ Bright Chain
**Best for**: Dull mixes, vocals, acoustic instruments

**What it does**:
- High-frequency boost for clarity
- Presence enhancement around 2-4kHz
- Light compression to maintain dynamics

**Use when**:
- Mix sounds muffled or dark
- Vocals need to cut through
- Acoustic guitars lack sparkle
- Working with older recordings

### 🔥 Warm Chain
**Best for**: Digital/harsh mixes, electronic music, adding character

**What it does**:
- Low-frequency enhancement for body
- Subtle saturation for harmonic richness
- Gentle high-frequency roll-off

**Use when**:
- Mix sounds thin or harsh
- Digital sources need analog warmth
- Electronic music needs body
- Overly bright recordings

## Best Practices

### Track Selection

**Individual Tracks**:
- Select the track before running SauceMax
- Best for vocals, lead instruments, drums
- Use different chains for different instruments

**Mix Bus**:
- Don't select any track (defaults to master)
- Best for overall mix enhancement
- Use Balanced chain for final polish

### When to Use SauceMax

**Good Candidates**:
- ✅ Home recordings that need professional polish
- ✅ Rough mixes that lack clarity or punch
- ✅ Tracks that sound "good" but not "great"
- ✅ Learning what professional processing sounds like

**Less Suitable**:
- ❌ Already well-mixed professional tracks
- ❌ Heavily damaged or distorted audio
- ❌ Extreme genres requiring specialized processing
- ❌ Creative/artistic mixing choices

### A/B Testing

Always compare your results:

1. **Apply SauceMax processing**
2. **Use Reaper's bypass** to toggle the effects on/off
3. **Listen on different speakers/headphones**
4. **Trust your ears** - SauceMax suggests, you decide

### Workflow Tips

**For Beginners**:
1. Get your raw tracks sounding balanced first
2. Use SauceMax on individual tracks needing help
3. Finish with SauceMax on the master bus
4. Don't over-process - less is often more

**For Experienced Users**:
1. Use SauceMax as a "second opinion"
2. Analyze before manual processing to identify issues
3. Use suggestions as starting points for manual tweaking
4. Compare SauceMax results with your manual processing

## Troubleshooting Common Issues

### "No Processing Needed"
**Meaning**: Your mix is already well-balanced
**Action**: This is good! Consider light master bus enhancement only

### Low Confidence Scores (<50%)
**Possible Causes**:
- Very short audio clips
- Unusual or experimental music
- Already heavily processed audio
**Action**: Trust your ears over the suggestions

### Processing Sounds Wrong
**Solutions**:
- Try different processing chains
- Reduce the intensity of effects manually
- Check if the source audio has issues
- Consider the genre and style context

### Analysis Fails
**Common Fixes**:
- Check audio file format (use WAV if possible)
- Ensure audio isn't silent or extremely quiet
- Try shorter audio clips (30-60 seconds)
- Restart Reaper and try again

## Advanced Techniques

### Genre-Specific Tips

**Hip-Hop/R&B**:
- Use Warm chain for body and low-end
- Bright chain for vocals that need to cut through
- Balanced for final master bus polish

**Rock/Metal**:
- Bright chain for guitars that need clarity
- Warm chain for bass and drums
- Be careful with compression on dynamic performances

**Electronic/EDM**:
- Warm chain to add analog character
- Bright chain for leads and vocals
- Balanced chain for full-mix enhancement

**Acoustic/Folk**:
- Bright chain for natural sparkle
- Light processing to maintain organic feel
- Use lower confidence threshold for subtle results

### Combining with Other Processing

SauceMax works well with other plugins:

**Before SauceMax**:
- Basic EQ cleanup (high-pass filters, notch filters)
- Noise reduction
- Pitch correction

**After SauceMax**:
- Creative effects (reverb, delay, modulation)
- Limiter/maximizer for loudness
- Stereo imaging tools

### Automation and Mixing

- **Don't automate SauceMax**: It's designed for static processing
- **Apply SauceMax early**: Before creative effects and automation
- **Bypass during arrangement**: Turn off when adding/removing tracks

## Getting Better Results

### Preparation

1. **Balance your raw tracks first**: Level, pan, basic EQ
2. **Fix obvious problems**: Noise, timing, tuning issues
3. **Get a rough mix**: Don't rely on SauceMax to fix everything

### Reference Tracks

- **Use professional references** in your genre
- **A/B with references** after applying SauceMax
- **Analyze references** with SauceMax to learn

### Learning from SauceMax

- **Study the suggestions**: What EQ moves does it suggest?
- **Try manual equivalent**: Can you achieve similar results by hand?
- **Understand the why**: Why does this track need brightness/warmth?

## Support and Community

- **GitHub Issues**: Report bugs and request features
- **GitHub Discussions**: Ask questions and share tips
- **Audio Forums**: Production techniques and mixing advice

Remember: SauceMax is a tool to help you learn and improve your mixes. The goal is to understand what makes mixes sound professional so you can eventually achieve great results on your own!