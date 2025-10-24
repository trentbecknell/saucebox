"""
Core audio processing engine for mix enhancement.

This module contains the main audio processing algorithms that apply
suggested enhancements to achieve professional-sounding mixes.
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from scipy import signal
import librosa

@dataclass  
class ProcessingChain:
    """Represents a chain of audio processing steps."""
    name: str
    steps: List[Dict[str, Any]]  # List of processing step configs
    target_characteristics: Dict[str, float]
    estimated_improvement: float

@dataclass
class AudioProcessor:
    """Main audio processing engine for mix enhancement."""
    
    def __init__(self, sample_rate: int = 44100):
        """Initialize processor with sample rate."""
        self.sample_rate = sample_rate
        self.processing_history = []
        self.presets_db = {}
        
    def load_presets(self, presets_path: str) -> None:
        """Load processing chain presets from file."""
        pass
        
    def apply_eq(self, audio: np.ndarray, eq_params: Dict[str, Any]) -> np.ndarray:
        """
        Apply EQ processing to audio signal.
        
        Args:
            audio: Input audio signal
            eq_params: EQ parameters (freq, gain, q, type)
            
        Returns:
            Processed audio signal
        """
        if not eq_params:
            return audio
            
        processed = audio.copy()
        
        # Apply different EQ types
        for eq_type, params in eq_params.items():
            if eq_type == 'high_shelf':
                processed = self._apply_high_shelf(processed, params)
            elif eq_type == 'low_shelf': 
                processed = self._apply_low_shelf(processed, params)
            elif eq_type == 'high_pass':
                processed = self._apply_high_pass(processed, params)
            elif eq_type == 'bell':
                processed = self._apply_bell_filter(processed, params)
                
        return processed
        
    def apply_compression(self, audio: np.ndarray, 
                         comp_params: Dict[str, float]) -> np.ndarray:
        """
        Apply dynamic range compression.
        
        Args:
            audio: Input audio signal
            comp_params: Compression parameters (threshold, ratio, attack, release)
            
        Returns:
            Compressed audio signal
        """
        if not comp_params:
            return audio
            
        threshold = comp_params.get('threshold', -12.0)
        ratio = comp_params.get('ratio', 4.0)
        attack_ms = comp_params.get('attack', 10.0)
        release_ms = comp_params.get('release', 100.0)
        
        # Convert time constants to samples
        attack_samples = int(attack_ms * self.sample_rate / 1000)
        release_samples = int(release_ms * self.sample_rate / 1000)
        
        # Simple peak detection and gain reduction
        envelope = self._calculate_envelope(audio, attack_samples, release_samples)
        threshold_linear = 10**(threshold/20)
        
        # Calculate gain reduction
        gain_reduction = np.ones_like(envelope)
        over_threshold = envelope > threshold_linear
        
        if np.any(over_threshold):
            excess = envelope[over_threshold] / threshold_linear
            gain_reduction[over_threshold] = 1.0 / (1.0 + (excess - 1.0) * (ratio - 1.0) / ratio)
        
        return audio * gain_reduction
        
    def apply_processing_chain(self, audio: np.ndarray, 
                              chain: ProcessingChain) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Apply a complete processing chain to audio.
        
        Args:
            audio: Input audio signal
            chain: ProcessingChain object with steps to apply
            
        Returns:
            Tuple of (processed_audio, processing_report)
        """
        processed = audio.copy()
        report = {
            'chain_name': chain.name,
            'steps_applied': [],
            'before_rms': np.sqrt(np.mean(audio**2)),
            'after_rms': 0.0,
            'processing_artifacts': []
        }
        
        for step in chain.steps:
            step_type = step.get('type')
            step_params = step.get('params', {})
            
            try:
                if step_type == 'eq':
                    processed = self.apply_eq(processed, step_params)
                elif step_type == 'compression':
                    processed = self.apply_compression(processed, step_params)
                elif step_type == 'saturation':
                    processed = self._apply_saturation(processed, step_params)
                    
                report['steps_applied'].append(step_type)
                
            except Exception as e:
                report['processing_artifacts'].append(f"Error in {step_type}: {str(e)}")
                
        report['after_rms'] = np.sqrt(np.mean(processed**2))
        
        # Store processing history
        self.processing_history.append({
            'chain': chain,
            'input_characteristics': self._analyze_audio_characteristics(audio),
            'output_characteristics': self._analyze_audio_characteristics(processed),
            'report': report
        })
        
        return processed, report
        
    def generate_adaptive_chain(self, audio_features, target_style: str = "balanced") -> ProcessingChain:
        """
        Generate an adaptive processing chain based on audio analysis.
        
        Args:
            audio_features: AudioFeatures from analyzer
            target_style: Target mix style ("balanced", "bright", "warm", etc.)
            
        Returns:
            Custom ProcessingChain for the audio
        """
        steps = []
        
        # Analyze frequency balance and suggest EQ
        balance = audio_features.frequency_balance
        total_energy = sum(balance.values()) if balance else 1
        
        eq_needed = {}
        if total_energy > 0:
            # Check bass balance
            bass_ratio = balance.get('bass', 0) / total_energy
            if bass_ratio < 0.15:
                eq_needed['low_shelf'] = {'freq': 100, 'gain': 2.5, 'q': 0.7}
            elif bass_ratio > 0.35:
                eq_needed['high_pass'] = {'freq': 60, 'q': 0.7}
                
            # Check high frequency content
            highs_ratio = balance.get('highs', 0) / total_energy
            if highs_ratio < 0.08 and target_style in ['bright', 'balanced']:
                eq_needed['high_shelf'] = {'freq': 10000, 'gain': 1.8, 'q': 0.7}
                
        if eq_needed:
            steps.append({'type': 'eq', 'params': eq_needed})
            
        # Add compression if needed
        if audio_features.dynamic_range > 0.7:
            comp_params = {
                'threshold': -15.0,
                'ratio': 3.5,
                'attack': 15.0,
                'release': 120.0
            }
            steps.append({'type': 'compression', 'params': comp_params})
            
        # Add subtle saturation for warmth
        if target_style in ['warm', 'vintage']:
            steps.append({'type': 'saturation', 'params': {'drive': 0.15, 'type': 'tape'}})
            
        estimated_improvement = min(0.8, len(steps) * 0.2)
        
        return ProcessingChain(
            name=f"adaptive_{target_style}",
            steps=steps,
            target_characteristics={
                'brightness': 0.7 if target_style == 'bright' else 0.5,
                'warmth': 0.8 if target_style == 'warm' else 0.4,
                'punch': 0.6,
                'clarity': 0.8
            },
            estimated_improvement=estimated_improvement
        )
        
    def _apply_high_shelf(self, audio: np.ndarray, params: Dict[str, float]) -> np.ndarray:
        """Apply high shelf EQ filter."""
        freq = params.get('freq', 8000)
        gain_db = params.get('gain', 0)
        q = params.get('q', 0.707)
        
        # Convert to linear gain
        gain = 10**(gain_db/20)
        
        # Design filter coefficients
        nyquist = self.sample_rate / 2
        normalized_freq = freq / nyquist
        
        if normalized_freq >= 1.0:
            return audio
            
        # Simple high shelf implementation
        sos = signal.butter(2, normalized_freq, btype='high', output='sos')
        filtered = signal.sosfilt(sos, audio)
        
        # Apply gain to high frequency content
        return audio + (filtered - audio) * (gain - 1)
        
    def _apply_low_shelf(self, audio: np.ndarray, params: Dict[str, float]) -> np.ndarray:
        """Apply low shelf EQ filter.""" 
        freq = params.get('freq', 200)
        gain_db = params.get('gain', 0)
        
        gain = 10**(gain_db/20)
        nyquist = self.sample_rate / 2
        normalized_freq = freq / nyquist
        
        if normalized_freq >= 1.0:
            return audio * gain
            
        sos = signal.butter(2, normalized_freq, btype='low', output='sos')
        filtered = signal.sosfilt(sos, audio)
        
        return audio + (filtered - audio) * (gain - 1)
        
    def _apply_high_pass(self, audio: np.ndarray, params: Dict[str, float]) -> np.ndarray:
        """Apply high pass filter."""
        freq = params.get('freq', 80)
        q = params.get('q', 0.707)
        
        nyquist = self.sample_rate / 2
        normalized_freq = freq / nyquist
        
        if normalized_freq >= 1.0:
            return np.zeros_like(audio)
        if normalized_freq <= 0:
            return audio
            
        sos = signal.butter(2, normalized_freq, btype='high', output='sos')
        return signal.sosfilt(sos, audio)
        
    def _apply_bell_filter(self, audio: np.ndarray, params: Dict[str, float]) -> np.ndarray:
        """Apply bell (peaking) EQ filter."""
        # Simplified bell filter implementation
        return audio
        
    def _apply_saturation(self, audio: np.ndarray, params: Dict[str, float]) -> np.ndarray:
        """Apply harmonic saturation."""
        drive = params.get('drive', 0.1)
        sat_type = params.get('type', 'soft')
        
        if sat_type == 'soft':
            # Soft saturation using tanh
            return np.tanh(audio * (1 + drive))
        else:
            # Hard clipping saturation
            threshold = 1.0 - drive
            return np.clip(audio, -threshold, threshold)
            
    def _calculate_envelope(self, audio: np.ndarray, 
                           attack_samples: int, release_samples: int) -> np.ndarray:
        """Calculate audio envelope for compression."""
        envelope = np.abs(audio)
        
        # Simple peak detector with attack/release
        output = np.zeros_like(envelope)
        current_level = 0.0
        
        for i, sample in enumerate(envelope):
            if sample > current_level:
                # Attack
                attack_coeff = 1.0 - np.exp(-1.0 / max(1, attack_samples))
                current_level += (sample - current_level) * attack_coeff
            else:
                # Release  
                release_coeff = 1.0 - np.exp(-1.0 / max(1, release_samples))
                current_level += (sample - current_level) * release_coeff
                
            output[i] = current_level
            
        return output
        
    def _analyze_audio_characteristics(self, audio: np.ndarray) -> Dict[str, float]:
        """Quick analysis of audio characteristics."""
        return {
            'rms': float(np.sqrt(np.mean(audio**2))),
            'peak': float(np.max(np.abs(audio))),
            'dynamic_range': float(np.max(audio) - np.min(audio)),
            'spectral_centroid': float(np.mean(librosa.feature.spectral_centroid(y=audio, sr=self.sample_rate)))
        }