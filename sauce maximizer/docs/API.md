# SauceMax API Documentation

This document describes the SauceMax API for programmatic access to audio analysis and processing functionality.

## Core Classes

### MixAnalyzer

The main class for analyzing audio mixes and extracting features.

```python
from sauce_maximizer import MixAnalyzer

analyzer = MixAnalyzer(sample_rate=44100)
```

#### Methods

##### `load_audio(file_path: str) -> Tuple[np.ndarray, int]`

Load an audio file for analysis.

**Parameters:**
- `file_path`: Path to audio file (WAV, MP3, AIFF, FLAC)

**Returns:**
- Tuple of (audio_data, sample_rate)

**Example:**
```python
audio, sr = analyzer.load_audio("mix.wav")
print(f"Loaded {len(audio)} samples at {sr}Hz")
```

##### `extract_features(audio: np.ndarray) -> AudioFeatures`

Extract comprehensive audio features from signal.

**Parameters:**
- `audio`: Audio signal array

**Returns:**
- `AudioFeatures` dataclass with:
  - `spectral_centroid`: Brightness measure (Hz)
  - `spectral_rolloff`: High-frequency rolloff point (Hz)  
  - `rms_energy`: RMS energy level (0-1)
  - `dynamic_range`: Peak-to-RMS ratio (0-1)
  - `frequency_balance`: Energy by band (dict)
  - `stereo_width`: Stereo image width (0-1)
  - `peak_frequency`: Dominant frequency (Hz)

**Example:**
```python
features = analyzer.extract_features(audio)
print(f"Brightness: {features.spectral_centroid:.0f}Hz")
print(f"Bass energy: {features.frequency_balance['bass']:.3f}")
```

##### `analyze_mix_balance(audio: np.ndarray) -> Dict[str, float]`

Analyze frequency balance and return scores.

**Returns:**
- Dict with balance scores (0-1) for each frequency band:
  - `bass`: 20-250Hz
  - `low_mids`: 250-500Hz
  - `mids`: 500-2000Hz
  - `high_mids`: 2000-4000Hz
  - `highs`: 4000-20000Hz

**Example:**
```python
balance = analyzer.analyze_mix_balance(audio)
if balance['bass'] < 0.5:
    print("Mix needs more bass")
```

##### `suggest_processing_chain(features: AudioFeatures) -> Dict[str, any]`

Generate processing suggestions based on analysis.

**Returns:**
- Dict with processing suggestions:
  - `eq`: EQ adjustments needed
  - `compression`: Compression parameters
  - `effects`: Additional effects list
  - `overall_confidence`: Confidence in suggestions (0-1)

### AudioProcessor

Applies audio processing based on analysis suggestions.

```python
from sauce_maximizer.core.optimizer import AudioProcessor

processor = AudioProcessor(sample_rate=44100)
```

#### Methods

##### `apply_eq(audio: np.ndarray, eq_params: Dict[str, Any]) -> np.ndarray`

Apply EQ processing to audio signal.

**Parameters:**
- `eq_params`: Dict with EQ settings:
  ```python
  {
      'high_shelf': {'freq': 8000, 'gain': 2.0, 'q': 0.7},
      'low_shelf': {'freq': 100, 'gain': 1.5, 'q': 0.7},
      'high_pass': {'freq': 80, 'q': 0.7}
  }
  ```

**Example:**
```python
eq_settings = {'high_shelf': {'freq': 10000, 'gain': 2.5, 'q': 0.6}}
processed = processor.apply_eq(audio, eq_settings)
```

##### `apply_compression(audio: np.ndarray, comp_params: Dict[str, float]) -> np.ndarray`

Apply dynamic range compression.

**Parameters:**
- `comp_params`: Compression settings:
  ```python
  {
      'threshold': -12.0,  # dB
      'ratio': 4.0,        # ratio
      'attack': 10.0,      # ms
      'release': 100.0     # ms
  }
  ```

##### `generate_adaptive_chain(audio_features: AudioFeatures, target_style: str) -> ProcessingChain`

Generate adaptive processing chain for target style.

**Parameters:**
- `target_style`: "balanced", "bright", "warm", or "vintage"

**Returns:**
- `ProcessingChain` object with optimized processing steps

### MixPredictor

Machine learning model for mix quality prediction.

```python
from sauce_maximizer import MixPredictor

predictor = MixPredictor(model_type="random_forest")
```

#### Methods

##### `predict_mix_quality(audio_features: Dict[str, float]) -> Dict[str, float]`

Predict mix quality and suggest improvements.

**Returns:**
- Dict with:
  - `overall_quality`: Quality score (0-1)
  - `confidence`: Prediction confidence (0-1)
  - `improvement_areas`: List of issues found
  - `predicted_rating`: Quality on 0-10 scale
  - `quality_category`: "professional", "good", "needs_work", etc.

**Example:**
```python
# Extract features as dict
feature_dict = {
    'spectral_centroid': features.spectral_centroid,
    'rms_energy': features.rms_energy,
    'bass_energy': features.frequency_balance['bass'],
    # ... other features
}

prediction = predictor.predict_mix_quality(feature_dict)
print(f"Quality: {prediction['quality_category']}")
print(f"Score: {prediction['predicted_rating']:.1f}/10")
```

## Data Structures

### AudioFeatures

```python
@dataclass
class AudioFeatures:
    spectral_centroid: float      # Hz
    spectral_rolloff: float       # Hz
    rms_energy: float            # 0-1
    dynamic_range: float         # 0-1
    frequency_balance: Dict[str, float]  # Energy by band
    stereo_width: float          # 0-1
    peak_frequency: float        # Hz
```

### ProcessingChain

```python
@dataclass
class ProcessingChain:
    name: str                    # Chain identifier
    steps: List[Dict[str, Any]]  # Processing steps
    target_characteristics: Dict[str, float]  # Target goals
    estimated_improvement: float # Expected improvement (0-1)
```

## Flask API Endpoints

If running the optional web API:

### POST `/api/analyze`

Analyze uploaded audio file.

**Request:**
```json
{
  "audio_file": "base64_encoded_audio",
  "format": "wav",
  "sample_rate": 44100
}
```

**Response:**
```json
{
  "features": {
    "spectral_centroid": 2500.0,
    "rms_energy": 0.25,
    "frequency_balance": {
      "bass": 0.3,
      "mids": 0.4,
      "highs": 0.2
    }
  },
  "suggestions": {
    "eq": {...},
    "compression": {...},
    "confidence": 0.85
  }
}
```

### POST `/api/predict`

Get quality prediction for audio features.

### POST `/api/process`

Apply processing chain to audio.

## Usage Examples

### Complete Analysis Workflow

```python
from sauce_maximizer import MixAnalyzer, MixPredictor
from sauce_maximizer.core.optimizer import AudioProcessor

# Initialize components
analyzer = MixAnalyzer()
predictor = MixPredictor()
processor = AudioProcessor()

# Load and analyze audio
audio, sr = analyzer.load_audio("my_mix.wav")
features = analyzer.extract_features(audio)

# Get quality prediction
feature_dict = {
    'spectral_centroid': features.spectral_centroid,
    'rms_energy': features.rms_energy,
    'dynamic_range': features.dynamic_range,
    # Add other features...
}

prediction = predictor.predict_mix_quality(feature_dict)
print(f"Mix quality: {prediction['quality_category']}")

# Generate and apply processing
if prediction['overall_quality'] < 0.7:
    suggestions = analyzer.suggest_processing_chain(features)
    
    if suggestions['eq']:
        processed_audio = processor.apply_eq(audio, suggestions['eq'])
    
    if suggestions['compression']:
        processed_audio = processor.apply_compression(processed_audio, suggestions['compression'])
```

### Batch Processing

```python
import os
from pathlib import Path

def analyze_folder(folder_path):
    """Analyze all audio files in a folder."""
    analyzer = MixAnalyzer()
    results = {}
    
    for audio_file in Path(folder_path).glob("*.wav"):
        try:
            audio, sr = analyzer.load_audio(str(audio_file))
            features = analyzer.extract_features(audio)
            balance = analyzer.analyze_mix_balance(audio)
            
            results[audio_file.name] = {
                'features': features,
                'balance': balance,
                'needs_processing': any(score < 0.6 for score in balance.values())
            }
        except Exception as e:
            print(f"Error analyzing {audio_file}: {e}")
    
    return results

# Analyze all mixes
results = analyze_folder("./my_mixes/")
for filename, analysis in results.items():
    if analysis['needs_processing']:
        print(f"{filename}: Needs processing")
```

### Custom Processing Chain

```python
def create_vocal_chain(features):
    """Create processing chain optimized for vocals."""
    steps = []
    
    # High-pass filter for proximity effect
    steps.append({
        'type': 'eq',
        'params': {'high_pass': {'freq': 100, 'q': 0.7}}
    })
    
    # Presence boost if needed
    if features.frequency_balance.get('high_mids', 0) < 0.15:
        steps.append({
            'type': 'eq', 
            'params': {'bell': {'freq': 3000, 'gain': 2.0, 'q': 1.0}}
        })
    
    # Compression for consistency
    if features.dynamic_range > 0.6:
        steps.append({
            'type': 'compression',
            'params': {
                'threshold': -18.0,
                'ratio': 3.0,
                'attack': 5.0,
                'release': 50.0
            }
        })
    
    return ProcessingChain(
        name="vocal_enhancement",
        steps=steps,
        target_characteristics={'clarity': 0.8, 'presence': 0.7},
        estimated_improvement=0.3
    )
```

## Error Handling

All API functions can raise these exceptions:

- `ValueError`: Invalid parameters or audio data
- `FileNotFoundError`: Audio file not found
- `RuntimeError`: Processing errors or model issues
- `ImportError`: Missing dependencies

Always wrap API calls in try-catch blocks:

```python
try:
    audio, sr = analyzer.load_audio("nonexistent.wav")
except FileNotFoundError:
    print("Audio file not found")
except Exception as e:
    print(f"Unexpected error: {e}")
```