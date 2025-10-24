-- SauceMax Minimal - Stable Reaper Integration
-- Simplified version for reliable testing

-- Configuration
local SCRIPT_NAME = "SauceMax"
local SCRIPT_VERSION = "0.1.0"

-- Simple message display function
function showMessage(title, message)
    if reaper.ShowMessageBox then
        reaper.ShowMessageBox(message, title, 0)
    else
        -- Fallback for older Reaper versions
        reaper.ShowConsoleMsg(title .. ": " .. message .. "\n")
    end
end

-- Check if we have basic Reaper API access
function checkReaperAPI()
    if not reaper then
        return false, "Reaper API not available"
    end
    
    if not reaper.GetSelectedTrack then
        return false, "Reaper API incomplete"
    end
    
    return true, "Reaper API available"
end

-- Get track information
function getTrackInfo()
    local track = reaper.GetSelectedTrack(0, 0)
    local track_name = "Master"
    
    if track then
        local retval, name = reaper.GetSetMediaTrackInfo_String(track, "P_NAME", "", false)
        if name and name ~= "" then
            track_name = name
        else
            local track_num = reaper.GetMediaTrackInfo_Value(track, "IP_TRACKNUMBER")
            track_name = "Track " .. tostring(math.floor(track_num))
        end
    else
        track = reaper.GetMasterTrack(0)
    end
    
    return track, track_name
end

-- Simulate basic analysis (placeholder)
function performBasicAnalysis(track_name)
    local analysis_result = {
        track_name = track_name,
        confidence = 0.75,
        suggested_processing = "balanced",
        issues_found = {"Low frequency imbalance", "Needs compression"},
        timestamp = os.date("%Y-%m-%d %H:%M:%S")
    }
    
    return analysis_result
end

-- Apply simple EQ (using built-in ReaEQ if available)
function applySimpleEQ(track, eq_type)
    if not track then return false end
    
    local eq_name = "ReaEQ"
    local fx_index = reaper.TrackFX_AddByName(track, eq_name, false, -1)
    
    if fx_index >= 0 then
        -- Configure based on type
        if eq_type == "bright" then
            -- High shelf boost
            reaper.TrackFX_SetParam(track, fx_index, 2, 0.6)  -- High shelf gain
            showMessage("SauceMax", "Applied brightness EQ")
        elseif eq_type == "warm" then
            -- Low shelf boost  
            reaper.TrackFX_SetParam(track, fx_index, 8, 0.4)  -- Low shelf gain
            showMessage("SauceMax", "Applied warmth EQ")
        else
            -- Balanced - gentle adjustments
            reaper.TrackFX_SetParam(track, fx_index, 2, 0.3)  -- Slight high boost
            reaper.TrackFX_SetParam(track, fx_index, 8, 0.2)  -- Slight low boost
            showMessage("SauceMax", "Applied balanced EQ")
        end
        return true
    else
        showMessage("SauceMax Error", "Could not add EQ plugin")
        return false
    end
end

-- Apply simple compression (using ReaComp if available)
function applySimpleCompression(track)
    if not track then return false end
    
    local comp_name = "ReaComp"
    local fx_index = reaper.TrackFX_AddByName(track, comp_name, false, -1)
    
    if fx_index >= 0 then
        -- Gentle compression settings
        reaper.TrackFX_SetParam(track, fx_index, 0, 0.3)  -- Threshold
        reaper.TrackFX_SetParam(track, fx_index, 1, 0.6)  -- Ratio  
        reaper.TrackFX_SetParam(track, fx_index, 2, 0.1)  -- Attack
        reaper.TrackFX_SetParam(track, fx_index, 3, 0.3)  -- Release
        
        showMessage("SauceMax", "Applied gentle compression")
        return true
    else
        showMessage("SauceMax Error", "Could not add compression plugin")
        return false
    end
end

-- Main functions
function quickSauce()
    local api_ok, api_msg = checkReaperAPI()
    if not api_ok then
        showMessage("SauceMax Error", api_msg)
        return
    end
    
    local track, track_name = getTrackInfo()
    
    showMessage("SauceMax", "Analyzing: " .. track_name .. "\n\nApplying Quick Sauce...")
    
    -- Perform analysis (simulated)
    local analysis = performBasicAnalysis(track_name)
    
    -- Apply processing based on analysis
    local success = true
    
    -- Apply EQ
    if not applySimpleEQ(track, analysis.suggested_processing) then
        success = false
    end
    
    -- Apply compression if needed
    if success and analysis.confidence > 0.6 then
        applySimpleCompression(track)
    end
    
    if success then
        local result_msg = string.format(
            "✓ Quick Sauce applied to: %s\n\nProcessing: %s\nConfidence: %.0f%%\n\nA/B test with bypass to compare!",
            track_name,
            analysis.suggested_processing,
            analysis.confidence * 100
        )
        showMessage("SauceMax - Complete", result_msg)
    else
        showMessage("SauceMax", "Processing completed with some limitations")
    end
end

function analyzeOnly()
    local api_ok, api_msg = checkReaperAPI()
    if not api_ok then
        showMessage("SauceMax Error", api_msg)
        return
    end
    
    local track, track_name = getTrackInfo()
    local analysis = performBasicAnalysis(track_name)
    
    local analysis_msg = string.format(
        "📊 Analysis Results: %s\n\nSuggested Processing: %s\nConfidence: %.0f%%\n\nIssues Found:\n• %s\n\nRecommendation: Use '%s' processing chain",
        track_name,
        analysis.suggested_processing,
        analysis.confidence * 100,
        table.concat(analysis.issues_found, "\n• "),
        analysis.suggested_processing
    )
    
    showMessage("SauceMax Analysis", analysis_msg)
end

function applyProcessingChain(chain_type)
    local api_ok, api_msg = checkReaperAPI()
    if not api_ok then
        showMessage("SauceMax Error", api_msg)
        return
    end
    
    local track, track_name = getTrackInfo()
    
    local success = applySimpleEQ(track, chain_type)
    if success then
        local msg = string.format("Applied %s processing to: %s", chain_type, track_name)
        showMessage("SauceMax", msg)
    end
end

-- Simple GUI (basic dialog-based interface)
function showMainDialog()
    local api_ok, api_msg = checkReaperAPI()
    if not api_ok then
        showMessage("SauceMax Error", api_msg)
        return
    end
    
    local track, track_name = getTrackInfo()
    
    local dialog_msg = string.format(
        "🎛️ SauceMax v%s\n\nSelected: %s\n\nChoose an action:",
        SCRIPT_VERSION,
        track_name
    )
    
    local choice = reaper.ShowMessageBox(
        dialog_msg,
        "SauceMax - Intelligent Mix Enhancement",
        4  -- Yes/No/Cancel
    )
    
    if choice == 6 then  -- Yes
        quickSauce()
    elseif choice == 7 then  -- No  
        analyzeOnly()
    else  -- Cancel
        showSubMenu()
    end
end

function showSubMenu()
    local choice = reaper.ShowMessageBox(
        "Choose processing type:\n\n• Yes = Balanced (general purpose)\n• No = Bright (clarity)\n• Cancel = Warm (character)",
        "SauceMax - Processing Chains",
        3  -- Yes/No/Cancel
    )
    
    if choice == 6 then      -- Yes
        applyProcessingChain("balanced")
    elseif choice == 7 then  -- No
        applyProcessingChain("bright") 
    else                     -- Cancel
        applyProcessingChain("warm")
    end
end

function showHelp()
    local help_text = string.format([[🎛️ SauceMax v%s - Help

QUICK START:
1. Select a track (or none for master)
2. Run SauceMax
3. Choose "Yes" for Quick Sauce
4. Listen and A/B test with bypass

PROCESSING TYPES:
• Balanced: General-purpose enhancement
• Bright: Adds clarity and presence  
• Warm: Adds character and body

TIPS:
• Works best on unprocessed audio
• Always A/B test results
• Trust your ears over automation
• Use as starting point for manual tweaking

TROUBLESHOOTING:
• Ensure ReaEQ/ReaComp plugins are available
• Check track selection
• Restart Reaper if issues persist]], SCRIPT_VERSION)
    
    showMessage("SauceMax Help", help_text)
end

-- Main entry point
function main()
    -- Check Reaper compatibility
    local api_ok, api_msg = checkReaperAPI()
    if not api_ok then
        showMessage("SauceMax Error", 
            "Reaper API not available.\n\nPlease run this script from within Reaper.")
        return
    end
    
    showMainDialog()
end

-- Menu registration (for Reaper's Actions menu)
function registerMenuItems()
    if reaper.AddRemoveReaScript then
        reaper.AddRemoveReaScript(true, 0, "", "SauceMax: Quick Sauce", quickSauce)
        reaper.AddRemoveReaScript(true, 0, "", "SauceMax: Analyze Mix", analyzeOnly)
        reaper.AddRemoveReaScript(true, 0, "", "SauceMax: Balanced Chain", function() applyProcessingChain("balanced") end)
        reaper.AddRemoveReaScript(true, 0, "", "SauceMax: Bright Chain", function() applyProcessingChain("bright") end)
        reaper.AddRemoveReaScript(true, 0, "", "SauceMax: Warm Chain", function() applyProcessingChain("warm") end)
        reaper.AddRemoveReaScript(true, 0, "", "SauceMax: Help", showHelp)
    end
end

-- Auto-run main function
if reaper then
    main()
end

-- Export functions for library use
return {
    quickSauce = quickSauce,
    analyzeOnly = analyzeOnly,
    applyProcessingChain = applyProcessingChain,
    showHelp = showHelp,
    main = main,
    version = SCRIPT_VERSION
}