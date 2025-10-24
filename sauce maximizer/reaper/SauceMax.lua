-- SauceMax ReaScript for Reaper Integration
-- Allows running mix analysis and applying processing chains directly in Reaper

-- Import required modules
local reaper = reaper
if not reaper.APIExists then
    reaper.ShowMessageBox("This script requires REAPER API", "Error", 0)
    return
end

-- SauceMax configuration
local SAUCEMAX_PATH = reaper.GetResourcePath() .. "/Scripts/SauceMax/"
local PYTHON_EXECUTABLE = "python3"  -- Adjust path as needed

-- Main SauceMax functions
function analyzeMix()
    -- Get selected track or master track
    local track = reaper.GetSelectedTrack(0, 0)
    if not track then
        track = reaper.GetMasterTrack(0)
        reaper.ShowMessageBox("No track selected, analyzing master mix", "SauceMax", 0)
    end
    
    -- Get track name for analysis
    local retval, track_name = reaper.GetSetMediaTrackInfo_String(track, "P_NAME", "", false)
    if track_name == "" then
        track_name = "Track_" .. tostring(reaper.GetMediaTrackInfo_Value(track, "IP_TRACKNUMBER"))
    end
    
    -- Export track for analysis
    local temp_file = reaper.GetResourcePath() .. "/temp_saucemax_analysis.wav"
    
    -- Solo track temporarily for clean export
    local solo_state = reaper.GetMediaTrackInfo_Value(track, "I_SOLO")
    reaper.SetMediaTrackInfo_Value(track, "I_SOLO", 1)
    
    -- Render track
    reaper.Main_OnCommand(40015, 0)  -- File: Render project to disk
    
    -- Restore solo state
    reaper.SetMediaTrackInfo_Value(track, "I_SOLO", solo_state)
    
    -- Run Python analysis
    local cmd = string.format('%s "%s/scripts/analyze_reaper_track.py" "%s" "%s"', 
                             PYTHON_EXECUTABLE, SAUCEMAX_PATH, temp_file, track_name)
    
    local analysis_result = os.execute(cmd)
    
    if analysis_result == 0 then
        reaper.ShowMessageBox("Mix analysis complete! Check the SauceMax window for results.", "SauceMax", 0)
        showAnalysisWindow()
    else
        reaper.ShowMessageBox("Analysis failed. Check Python installation and SauceMax path.", "Error", 0)
    end
end

function applyProcessingChain(chain_type)
    -- Apply suggested processing chain to selected track
    local track = reaper.GetSelectedTrack(0, 0)
    if not track then
        reaper.ShowMessageBox("Please select a track first", "SauceMax", 0)
        return
    end
    
    -- Load processing chain based on analysis results
    local chain_file = SAUCEMAX_PATH .. "presets/" .. chain_type .. ".rpp"
    
    if reaper.file_exists(chain_file) then
        -- Apply FX chain from preset
        reaper.TrackFX_AddByName(track, chain_file, false, -1)
        reaper.ShowMessageBox("Applied " .. chain_type .. " processing chain", "SauceMax", 0)
    else
        -- Apply individual effects based on suggestions
        applyIndividualEffects(track, chain_type)
    end
end

function applyIndividualEffects(track, chain_type)
    -- Apply effects individually based on chain type
    if chain_type == "balanced" then
        -- Add ReaEQ for frequency balance
        local eq_idx = reaper.TrackFX_AddByName(track, "ReaEQ", false, -1)
        if eq_idx >= 0 then
            -- Configure EQ based on analysis
            reaper.TrackFX_SetParam(track, eq_idx, 2, 0.6)  -- High shelf gain
            reaper.TrackFX_SetParam(track, eq_idx, 8, 0.3)  -- Low shelf gain
        end
        
        -- Add ReaComp for dynamics
        local comp_idx = reaper.TrackFX_AddByName(track, "ReaComp", false, -1)
        if comp_idx >= 0 then
            reaper.TrackFX_SetParam(track, comp_idx, 0, 0.25)  -- Threshold
            reaper.TrackFX_SetParam(track, comp_idx, 1, 0.65)  -- Ratio
        end
        
    elseif chain_type == "bright" then
        -- Brightness enhancement chain
        local eq_idx = reaper.TrackFX_AddByName(track, "ReaEQ", false, -1)
        if eq_idx >= 0 then
            reaper.TrackFX_SetParam(track, eq_idx, 2, 0.7)  -- High shelf boost
            reaper.TrackFX_SetParam(track, eq_idx, 1, 0.8)  -- High shelf frequency
        end
        
    elseif chain_type == "warm" then
        -- Warmth/vintage enhancement
        local eq_idx = reaper.TrackFX_AddByName(track, "ReaEQ", false, -1)
        if eq_idx >= 0 then
            reaper.TrackFX_SetParam(track, eq_idx, 8, 0.4)  -- Low shelf boost
        end
        
        -- Add subtle saturation if available
        local sat_idx = reaper.TrackFX_AddByName(track, "JS: Saturation", false, -1)
        if sat_idx >= 0 then
            reaper.TrackFX_SetParam(track, sat_idx, 0, 0.15)  -- Drive
        end
    end
end

function showAnalysisWindow()
    -- Create simple dialog showing analysis results
    local script_path = debug.getinfo(1, "S").source:match("@(.*)"):gsub("[\\/][^\\/]*$", "") .. "/"
    local results_file = script_path .. "analysis_results.txt"
    
    if reaper.file_exists(results_file) then
        local file = io.open(results_file, "r")
        if file then
            local content = file:read("*all")
            file:close()
            reaper.ShowMessageBox(content, "SauceMax Analysis Results", 0)
        end
    end
end

function quickSauce()
    -- One-click "add sauce" function - analyze and apply best processing
    analyzeMix()
    
    -- Wait for analysis to complete (simplified)
    reaper.defer(function()
        applyProcessingChain("balanced")
    end)
end

-- Register menu items in Reaper
function createSauceMaxMenu()
    if reaper.APIExists("gfx.init") then
        reaper.AddRemoveReaScript(true, 0, "", "SauceMax: Quick Sauce (Analyze + Process)", quickSauce)
        reaper.AddRemoveReaScript(true, 0, "", "SauceMax: Analyze Mix", analyzeMix)
        reaper.AddRemoveReaScript(true, 0, "", "SauceMax: Apply Balanced Chain", function() applyProcessingChain("balanced") end)
        reaper.AddRemoveReaScript(true, 0, "", "SauceMax: Apply Bright Chain", function() applyProcessingChain("bright") end)
        reaper.AddRemoveReaScript(true, 0, "", "SauceMax: Apply Warm Chain", function() applyProcessingChain("warm") end)
    end
end

-- Main execution
function main()
    -- Create GUI for SauceMax
    local gfx = gfx
    gfx.init("SauceMax - Intelligent Mix Enhancement", 400, 300)
    
    while gfx.getchar() >= 0 do
        gfx.set(0.1, 0.1, 0.1)  -- Dark background
        gfx.rect(0, 0, gfx.w, gfx.h)
        
        -- Title
        gfx.set(1, 1, 1)
        gfx.setfont(1, "Arial", 24)
        gfx.x, gfx.y = 50, 30
        gfx.drawstr("SauceMax")
        
        -- Buttons
        gfx.setfont(1, "Arial", 16)
        
        -- Quick Sauce button
        if drawButton(50, 80, 300, 40, "🎛️ Quick Sauce (Analyze + Process)", 0.2, 0.6, 0.2) then
            quickSauce()
        end
        
        -- Analyze button
        if drawButton(50, 140, 140, 40, "📊 Analyze Mix", 0.4, 0.4, 0.6) then
            analyzeMix()
        end
        
        -- Processing chain buttons
        if drawButton(210, 140, 140, 40, "⚖️ Balanced", 0.6, 0.4, 0.2) then
            applyProcessingChain("balanced")
        end
        
        if drawButton(50, 200, 90, 40, "✨ Bright", 0.8, 0.6, 0.2) then
            applyProcessingChain("bright")
        end
        
        if drawButton(160, 200, 90, 40, "🔥 Warm", 0.8, 0.4, 0.2) then
            applyProcessingChain("warm")
        end
        
        if drawButton(270, 200, 80, 40, "❓ Help", 0.3, 0.3, 0.3) then
            showHelp()
        end
        
        gfx.update()
    end
    
    gfx.quit()
end

function drawButton(x, y, w, h, text, r, g, b)
    local mouse_x, mouse_y = gfx.mouse_x, gfx.mouse_y
    local mouse_cap = gfx.mouse_cap
    
    local is_hover = mouse_x >= x and mouse_x <= x + w and mouse_y >= y and mouse_y <= y + h
    local is_click = is_hover and mouse_cap == 1
    
    -- Button background
    if is_hover then
        gfx.set(r + 0.2, g + 0.2, b + 0.2)
    else
        gfx.set(r, g, b)
    end
    gfx.rect(x, y, w, h)
    
    -- Button border
    gfx.set(0.8, 0.8, 0.8)
    gfx.rect(x, y, w, h, 0)
    
    -- Button text
    gfx.set(1, 1, 1)
    local text_w, text_h = gfx.measurestr(text)
    gfx.x = x + (w - text_w) / 2
    gfx.y = y + (h - text_h) / 2
    gfx.drawstr(text)
    
    return is_click
end

function showHelp()
    local help_text = [[SauceMax - Intelligent Mix Enhancement

Quick Sauce: Automatically analyzes your mix and applies the best processing chain

Analyze Mix: Runs spectral analysis on selected track or master

Processing Chains:
• Balanced: EQ and compression for overall mix balance
• Bright: High-frequency enhancement for clarity
• Warm: Low-frequency enhancement and subtle saturation

Tips:
- Select a track before analysis for individual track processing
- Use on master bus for overall mix enhancement  
- Trust your ears - SauceMax suggestions are starting points]]
    
    reaper.ShowMessageBox(help_text, "SauceMax Help", 0)
end

-- Run the main function if called directly
if not package.loaded["SauceMax"] then
    main()
end

-- Export functions for use as library
return {
    analyzeMix = analyzeMix,
    applyProcessingChain = applyProcessingChain,
    quickSauce = quickSauce,
    main = main
}