"""
Audio mix analysis tools for understanding mix characteristics.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import warnings
import os

# Safe imports with fallbacks
try:
    import librosa
    HAS_LIBROSA = True
except ImportError:
    HAS_LIBROSA = False
    warnings.warn("librosa not available - using basic analysis only")

try:
    import scipy.signal as signal
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False
    warnings.warn("scipy not available - some analysis features disabled")

@dataclass
class AudioFeatures:
    """Represents extracted audio features from a mix."""
    spectral_centroid: float
    spectral_rolloff: float
    rms_energy: float
    dynamic_range: float
    frequency_balance: Dict[str, float]  # bass, mids, highs
    stereo_width: float
    peak_frequency: float

@dataclass
class MixProfile:
    """Represents a complete mix analysis profile."""
    name: str
    features: AudioFeatures
    suggested_processing: Dict[str, any]
    confidence_score: float

class MixAnalyzer:
    """Analyzes audio mixes for balance and professional characteristics."""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.analysis_cache = {}
        self.frequency_bands = {
            'bass': (20, 250),
            'low_mids': (250, 500), 
            'mids': (500, 2000),
            'high_mids': (2000, 4000),
            'highs': (4000, 20000)
        }
        
        if not HAS_LIBROSA:
            warnings.warn("Librosa not available - analysis will be limited")
        
    def load_audio(self, file_path: str) -> Tuple[np.ndarray, int]:
        """Load audio file for analysis with robust error handling."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found: {file_path}")
        
        try:
            if HAS_LIBROSA:
                audio, sr = librosa.load(file_path, sr=self.sample_rate)
                if len(audio) == 0:
                    raise ValueError("Audio file is empty")
                return audio, sr
            else:
                # Fallback for when librosa is not available
                raise ImportError("librosa required for audio loading")
                
        except Exception as e:
            raise RuntimeError(f"Failed to load audio file {file_path}: {str(e)}")
        
    def extract_features(self, audio: np.ndarray) -> AudioFeatures:
        """
        Extract comprehensive audio features for mix analysis with error handling.
        
        Args:
            audio: Audio signal array
            
        Returns:
            AudioFeatures object with extracted characteristics
        """
        if audio is None or len(audio) == 0:
            raise ValueError("Invalid audio data provided")
        
        try:
            # Basic features that don't require librosa
            rms_energy = float(np.sqrt(np.mean(audio**2)))
            dynamic_range = float(np.max(audio) - np.min(audio))
            
            # Features requiring librosa
            if HAS_LIBROSA and len(audio) > 1024:  # Minimum length for analysis
                try:
                    spectral_centroids = librosa.feature.spectral_centroid(y=audio, sr=self.sample_rate)
                    spectral_centroid = float(np.mean(spectral_centroids))
                    
                    spectral_rolloff = librosa.feature.spectral_rolloff(y=audio, sr=self.sample_rate)
                    rolloff = float(np.mean(spectral_rolloff))
                except Exception as e:
                    warnings.warn(f"Spectral analysis failed: {e}")
                    spectral_centroid = 1000.0  # Default fallback
                    rolloff = 8000.0
            else:
                # Fallback values when librosa is not available
                spectral_centroid = 1000.0
                rolloff = 8000.0
            
            # Frequency balance analysis
            frequency_balance = self._analyze_frequency_balance(audio)
            
            # Stereo analysis (if stereo)
            if len(audio.shape) > 1 and audio.shape[0] > 1:
                stereo_width = self._calculate_stereo_width(audio)
            else:
                stereo_width = 0.0
                
            # Peak frequency detection with error handling
            try:
                peak_frequency = self._find_peak_frequency(audio)
            except Exception as e:
                warnings.warn(f"Peak frequency detection failed: {e}")
                peak_frequency = 440.0  # Default A4
            
            return AudioFeatures(
                spectral_centroid=spectral_centroid,
                spectral_rolloff=rolloff,
                rms_energy=rms_energy,
                dynamic_range=dynamic_range,
                frequency_balance=frequency_balance,
                stereo_width=stereo_width,
                peak_frequency=peak_frequency
            )
            
        except Exception as e:
            # Return safe defaults if analysis completely fails
            warnings.warn(f"Feature extraction failed, using defaults: {e}")
            return AudioFeatures(
                spectral_centroid=1000.0,
                spectral_rolloff=8000.0,
                rms_energy=0.1,
                dynamic_range=0.5,
                frequency_balance={'bass': 0.3, 'mids': 0.4, 'highs': 0.3},
                stereo_width=0.5,
                peak_frequency=440.0
            )
        
    def _analyze_frequency_balance(self, audio: np.ndarray) -> Dict[str, float]:
        """Analyze frequency balance with error handling."""
        try:
            if HAS_LIBROSA and len(audio) > 1024:
                stft = librosa.stft(audio)
                magnitude = np.abs(stft)
                freqs = librosa.fft_frequencies(sr=self.sample_rate)
                
                frequency_balance = {}
                total_energy = 0
                
                for band_name, (low_freq, high_freq) in self.frequency_bands.items():
                    band_mask = (freqs >= low_freq) & (freqs <= high_freq)
                    if np.any(band_mask):
                        band_energy = np.mean(magnitude[band_mask, :])
                        frequency_balance[band_name] = float(band_energy)
                        total_energy += band_energy
                    else:
                        frequency_balance[band_name] = 0.0
                
                # Normalize to ratios
                if total_energy > 0:
                    for band in frequency_balance:
                        frequency_balance[band] /= total_energy
                        
                return frequency_balance
            else:
                # Basic fallback analysis using simple FFT
                return self._basic_frequency_analysis(audio)
                
        except Exception as e:
            warnings.warn(f"Frequency analysis failed: {e}")
            return {'bass': 0.3, 'low_mids': 0.2, 'mids': 0.3, 'high_mids': 0.15, 'highs': 0.05}
    
    def _basic_frequency_analysis(self, audio: np.ndarray) -> Dict[str, float]:
        """Basic frequency analysis without librosa."""
        try:
            # Simple FFT-based analysis
            fft = np.fft.fft(audio[:min(len(audio), 8192)])  # Use first 8192 samples
            freqs = np.fft.fftfreq(len(fft), 1/self.sample_rate)
            magnitude = np.abs(fft)
            
            # Only use positive frequencies
            pos_mask = freqs > 0
            freqs = freqs[pos_mask]
            magnitude = magnitude[pos_mask]
            
            frequency_balance = {}
            total_energy = 0
            
            for band_name, (low_freq, high_freq) in self.frequency_bands.items():
                band_mask = (freqs >= low_freq) & (freqs <= high_freq)
                if np.any(band_mask):
                    band_energy = np.mean(magnitude[band_mask])
                    frequency_balance[band_name] = float(band_energy)
                    total_energy += band_energy
                else:
                    frequency_balance[band_name] = 0.0
            
            # Normalize
            if total_energy > 0:
                for band in frequency_balance:
                    frequency_balance[band] /= total_energy
            
            return frequency_balance
            
        except Exception as e:
            warnings.warn(f"Basic frequency analysis failed: {e}")
            return {'bass': 0.3, 'low_mids': 0.2, 'mids': 0.3, 'high_mids': 0.15, 'highs': 0.05}
    
    def _find_peak_frequency(self, audio: np.ndarray) -> float:
        """Find peak frequency with error handling."""
        try:
            fft = np.fft.fft(audio[:min(len(audio), 8192)])
            freqs = np.fft.fftfreq(len(fft), 1/self.sample_rate)
            
            # Only consider positive frequencies
            pos_mask = freqs > 0
            pos_freqs = freqs[pos_mask]
            pos_magnitude = np.abs(fft[pos_mask])
            
            if len(pos_magnitude) > 0:
                peak_idx = np.argmax(pos_magnitude)
                return float(abs(pos_freqs[peak_idx]))
            else:
                return 440.0
                
        except Exception as e:
            warnings.warn(f"Peak frequency detection failed: {e}")
            return 440.0
        
    def analyze_mix_balance(self, audio: np.ndarray) -> Dict[str, float]:
        """
        Analyze the frequency balance of a mix with error handling.
        
        Returns:
            Dict with balance scores for different frequency ranges
        """
        try:
            features = self.extract_features(audio)
            
            # Calculate balance scores (0-1, where 1 is perfectly balanced)
            balance_scores = {}
            ideal_ratios = {'bass': 0.25, 'low_mids': 0.20, 'mids': 0.30, 'high_mids': 0.15, 'highs': 0.10}
            
            for band_name in self.frequency_bands.keys():
                actual_ratio = features.frequency_balance.get(band_name, 0)
                ideal_ratio = ideal_ratios.get(band_name, 0.2)
                
                if ideal_ratio > 0:
                    # Score based on how close to ideal (higher is better)
                    balance_scores[band_name] = max(0.0, 1.0 - abs(actual_ratio - ideal_ratio) / ideal_ratio)
                else:
                    balance_scores[band_name] = 0.5  # Neutral score
                    
            return balance_scores
            
        except Exception as e:
            warnings.warn(f"Mix balance analysis failed: {e}")
            return {band: 0.5 for band in self.frequency_bands.keys()}
        
    def suggest_processing_chain(self, features: AudioFeatures) -> Dict[str, any]:
        """Suggest audio processing based on analysis with error handling."""
        try:
            suggestions = {
                'eq': {},
                'compression': {},
                'effects': [],
                'overall_confidence': 0.0
            }
            
            # EQ suggestions based on frequency balance
            balance = features.frequency_balance
            total_energy = sum(balance.values()) if balance else 1
            
            if total_energy > 0:
                bass_ratio = balance.get('bass', 0) / total_energy
                if bass_ratio < 0.15:  # Too little bass
                    suggestions['eq']['low_shelf'] = {'freq': 100, 'gain': 3.0, 'q': 0.7}
                elif bass_ratio > 0.35:  # Too much bass
                    suggestions['eq']['high_pass'] = {'freq': 40, 'q': 0.7}
                    
                highs_ratio = balance.get('highs', 0) / total_energy  
                if highs_ratio < 0.05:  # Needs brightness
                    suggestions['eq']['high_shelf'] = {'freq': 8000, 'gain': 2.0, 'q': 0.7}
                    
            # Compression suggestions based on dynamics
            if features.dynamic_range > 0.8:  # Too dynamic, needs compression
                suggestions['compression'] = {
                    'threshold': -12.0,
                    'ratio': 3.0,
                    'attack': 10.0,
                    'release': 100.0
                }
            elif features.dynamic_range < 0.2:  # Over-compressed, needs expansion
                suggestions['effects'].append('gentle_expansion')
                
            # Overall confidence based on analysis quality
            suggestions['overall_confidence'] = min(1.0, max(0.1, features.rms_energy * 10))
            
            return suggestions
            
        except Exception as e:
            warnings.warn(f"Processing chain suggestion failed: {e}")
            return {
                'eq': {},
                'compression': {},
                'effects': [],
                'overall_confidence': 0.5
            }
        
    def _calculate_stereo_width(self, stereo_audio: np.ndarray) -> float:
        """Calculate stereo width of audio signal with error handling."""
        try:
            if len(stereo_audio.shape) < 2 or stereo_audio.shape[0] < 2:
                return 0.0
                
            left = stereo_audio[0, :]
            right = stereo_audio[1, :]
            
            # Calculate correlation between channels
            if len(left) > 1 and len(right) > 1:
                correlation = np.corrcoef(left, right)[0, 1]
                
                # Handle NaN correlation (can happen with silence)
                if np.isnan(correlation):
                    return 0.5
                    
                # Width is inverse of correlation (high correlation = narrow, low = wide)
                width = 1.0 - abs(correlation)
                return float(np.clip(width, 0.0, 1.0))
            else:
                return 0.0
                
        except Exception as e:
            warnings.warn(f"Stereo width calculation failed: {e}")
            return 0.5
        
    def analyze_mix_balance(self, audio: np.ndarray) -> Dict[str, float]:
        """
        Analyze the frequency balance of a mix.
        
        Returns:
            Dict with balance scores for different frequency ranges
        """
        features = self.extract_features(audio)
        
        # Calculate balance scores (0-1, where 1 is perfectly balanced)
        total_energy = sum(features.frequency_balance.values())
        if total_energy == 0:
            return {band: 0.0 for band in self.frequency_bands.keys()}
            
        balance_scores = {}
        for band_name, energy in features.frequency_balance.items():
            # Ideal energy distribution varies by frequency band
            ideal_ratios = {'bass': 0.25, 'low_mids': 0.20, 'mids': 0.30, 'high_mids': 0.15, 'highs': 0.10}
            actual_ratio = energy / total_energy
            ideal_ratio = ideal_ratios.get(band_name, 0.2)
            
            # Score based on how close to ideal
            balance_scores[band_name] = 1.0 - abs(actual_ratio - ideal_ratio) / ideal_ratio
            
        return balance_scores
        
    def suggest_processing_chain(self, features: AudioFeatures) -> Dict[str, any]:
        """Suggest audio processing based on analysis."""
        suggestions = {
            'eq': {},
            'compression': {},
            'effects': [],
            'overall_confidence': 0.0
        }
        
        # EQ suggestions based on frequency balance
        balance = features.frequency_balance
        total_energy = sum(balance.values()) if balance else 1
        
        if total_energy > 0:
            bass_ratio = balance.get('bass', 0) / total_energy
            if bass_ratio < 0.15:  # Too little bass
                suggestions['eq']['low_shelf'] = {'freq': 100, 'gain': 3.0, 'q': 0.7}
            elif bass_ratio > 0.35:  # Too much bass
                suggestions['eq']['high_pass'] = {'freq': 40, 'q': 0.7}
                
            highs_ratio = balance.get('highs', 0) / total_energy  
            if highs_ratio < 0.05:  # Needs brightness
                suggestions['eq']['high_shelf'] = {'freq': 8000, 'gain': 2.0, 'q': 0.7}
                
        # Compression suggestions based on dynamics
        if features.dynamic_range > 0.8:  # Too dynamic, needs compression
            suggestions['compression'] = {
                'threshold': -12.0,
                'ratio': 3.0,
                'attack': 10.0,
                'release': 100.0
            }
        elif features.dynamic_range < 0.2:  # Over-compressed, needs expansion
            suggestions['effects'].append('gentle_expansion')
            
        # Overall confidence based on analysis quality
        suggestions['overall_confidence'] = min(1.0, features.rms_energy * 10)
        
        return suggestions
        
    def _calculate_stereo_width(self, stereo_audio: np.ndarray) -> float:
        """Calculate stereo width of audio signal."""
        if len(stereo_audio.shape) < 2:
            return 0.0
            
        left = stereo_audio[0, :]
        right = stereo_audio[1, :]
        
        # Calculate correlation between channels
        correlation = np.corrcoef(left, right)[0, 1]
        
        # Width is inverse of correlation (high correlation = narrow, low = wide)
        width = 1.0 - abs(correlation)
        return width