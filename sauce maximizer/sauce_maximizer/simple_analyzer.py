"""
Simple, stable audio analyzer using only standard libraries and numpy.
"""

import numpy as np
import wave
import struct
from typing import Dict, Tuple, Optional

class SimpleAnalyzer:
    """Minimal audio analyzer that actually works."""
    
    def __init__(self):
        """Initialize the analyzer."""
        self.last_analysis = None
        
    def load_wav_file(self, file_path: str) -> Tuple[np.ndarray, int]:
        """
        Load a WAV file using only standard library.
        
        Args:
            file_path: Path to WAV file
            
        Returns:
            Tuple of (audio_data, sample_rate)
        """
        try:
            with wave.open(file_path, 'rb') as wav_file:
                # Get basic info
                frames = wav_file.getnframes()
                sample_rate = wav_file.getframerate()
                channels = wav_file.getnchannels()
                sample_width = wav_file.getsampwidth()
                
                # Read raw audio data
                raw_audio = wav_file.readframes(frames)
                
                # Convert to numpy array
                if sample_width == 1:
                    dtype = np.uint8
                elif sample_width == 2:
                    dtype = np.int16
                elif sample_width == 4:
                    dtype = np.int32
                else:
                    raise ValueError(f"Unsupported sample width: {sample_width}")
                
                audio_data = np.frombuffer(raw_audio, dtype=dtype)
                
                # Handle stereo by taking left channel
                if channels == 2:
                    audio_data = audio_data[::2]
                
                # Normalize to [-1, 1]
                if dtype == np.uint8:
                    audio_data = (audio_data.astype(np.float32) - 128) / 128
                else:
                    max_val = 2**(8 * sample_width - 1)
                    audio_data = audio_data.astype(np.float32) / max_val
                
                return audio_data, sample_rate
                
        except Exception as e:
            raise RuntimeError(f"Failed to load WAV file {file_path}: {e}")
    
    def analyze_basic_stats(self, audio_data: np.ndarray, sample_rate: int) -> Dict[str, float]:
        """
        Analyze basic audio statistics.
        
        Args:
            audio_data: Audio signal array
            sample_rate: Sample rate in Hz
            
        Returns:
            Dict with basic audio statistics
        """
        try:
            # Basic statistics
            duration = len(audio_data) / sample_rate
            rms = np.sqrt(np.mean(audio_data**2))
            peak = np.max(np.abs(audio_data))
            
            # Dynamic range (simple version)
            dynamic_range = peak / (rms + 1e-10)  # Avoid division by zero
            
            # Frequency analysis using simple FFT
            fft = np.fft.fft(audio_data[:min(len(audio_data), sample_rate)])  # 1 second max
            fft_magnitude = np.abs(fft)
            freqs = np.fft.fftfreq(len(fft), 1/sample_rate)
            
            # Find dominant frequency
            positive_freqs = freqs[:len(freqs)//2]
            positive_magnitude = fft_magnitude[:len(fft_magnitude)//2]
            dominant_freq_idx = np.argmax(positive_magnitude)
            dominant_frequency = positive_freqs[dominant_freq_idx]
            
            # Simple frequency bands
            bass_band = np.sum(positive_magnitude[(positive_freqs >= 20) & (positive_freqs <= 250)])
            mid_band = np.sum(positive_magnitude[(positive_freqs >= 250) & (positive_freqs <= 4000)])
            high_band = np.sum(positive_magnitude[(positive_freqs >= 4000) & (positive_freqs <= 20000)])
            
            total_energy = bass_band + mid_band + high_band
            if total_energy > 0:
                bass_ratio = bass_band / total_energy
                mid_ratio = mid_band / total_energy
                high_ratio = high_band / total_energy
            else:
                bass_ratio = mid_ratio = high_ratio = 0.0
            
            results = {
                'duration_seconds': duration,
                'rms_level': float(rms),
                'peak_level': float(peak),
                'dynamic_range': float(dynamic_range),
                'dominant_frequency_hz': float(abs(dominant_frequency)),
                'bass_ratio': float(bass_ratio),
                'mid_ratio': float(mid_ratio),
                'high_ratio': float(high_ratio),
                'sample_rate': sample_rate,
                'total_samples': len(audio_data)
            }
            
            self.last_analysis = results
            return results
            
        except Exception as e:
            raise RuntimeError(f"Analysis failed: {e}")
    
    def suggest_simple_processing(self, analysis: Dict[str, float]) -> Dict[str, str]:
        """
        Suggest basic processing based on analysis.
        
        Args:
            analysis: Results from analyze_basic_stats
            
        Returns:
            Dict with simple processing suggestions
        """
        suggestions = []
        
        # Check levels
        if analysis['rms_level'] < 0.1:
            suggestions.append("Track seems quiet - consider raising the level")
        elif analysis['rms_level'] > 0.7:
            suggestions.append("Track seems loud - consider lowering the level")
        
        # Check frequency balance
        if analysis['bass_ratio'] < 0.1:
            suggestions.append("Low bass content - consider bass boost")
        elif analysis['bass_ratio'] > 0.5:
            suggestions.append("Heavy bass content - consider high-pass filter")
        
        if analysis['high_ratio'] < 0.05:
            suggestions.append("Limited high frequencies - consider brightness enhancement")
        elif analysis['high_ratio'] > 0.3:
            suggestions.append("Bright mix - might be harsh")
        
        # Check dynamics
        if analysis['dynamic_range'] < 2.0:
            suggestions.append("Heavily compressed - consider adding dynamics")
        elif analysis['dynamic_range'] > 10.0:
            suggestions.append("Very dynamic - might need compression for consistency")
        
        return {
            'suggestions': suggestions,
            'overall_assessment': self._get_overall_assessment(analysis)
        }
    
    def _get_overall_assessment(self, analysis: Dict[str, float]) -> str:
        """Get overall assessment of the mix."""
        issues = 0
        
        # Count potential issues
        if analysis['rms_level'] < 0.05 or analysis['rms_level'] > 0.8:
            issues += 1
        if analysis['bass_ratio'] < 0.08 or analysis['bass_ratio'] > 0.6:
            issues += 1
        if analysis['high_ratio'] < 0.03 or analysis['high_ratio'] > 0.4:
            issues += 1
        if analysis['dynamic_range'] < 1.5 or analysis['dynamic_range'] > 15.0:
            issues += 1
        
        if issues == 0:
            return "Mix sounds well-balanced"
        elif issues <= 2:
            return "Mix has minor issues that could be improved"
        else:
            return "Mix needs significant improvement"