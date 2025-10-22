#!/usr/bin/env python3
"""
MCP Tool with SignFX Metrics
A Model Context Protocol tool that provides SignFX metrics functionality.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
from datetime import datetime, timedelta
import statistics
import math

# MCP imports
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SignFXMetrics:
    """SignFX metrics data structure"""
    timestamp: datetime
    signal_strength: float
    noise_level: float
    signal_to_noise_ratio: float
    frequency: float
    amplitude: float
    phase: float
    distortion: float
    latency: float
    throughput: float
    error_rate: float
    quality_score: float

class SignFXMetricsCalculator:
    """Calculator for SignFX metrics"""
    
    def __init__(self):
        self.metrics_history: List[SignFXMetrics] = []
    
    def calculate_snr(self, signal_strength: float, noise_level: float) -> float:
        """Calculate Signal-to-Noise Ratio"""
        if noise_level == 0:
            return float('inf')
        return 20 * math.log10(signal_strength / noise_level)
    
    def calculate_quality_score(self, metrics: SignFXMetrics) -> float:
        """Calculate overall quality score based on multiple metrics"""
        # Weighted quality score (0-100)
        weights = {
            'snr': 0.3,
            'distortion': 0.2,
            'latency': 0.15,
            'error_rate': 0.15,
            'throughput': 0.1,
            'amplitude': 0.1
        }
        
        # Normalize metrics to 0-100 scale
        snr_score = min(100, max(0, (metrics.signal_to_noise_ratio + 20) * 2.5))  # -20dB to 20dB -> 0-100
        distortion_score = max(0, 100 - metrics.distortion * 100)  # Lower distortion = higher score
        latency_score = max(0, 100 - metrics.latency * 10)  # Lower latency = higher score
        error_rate_score = max(0, 100 - metrics.error_rate * 1000)  # Lower error rate = higher score
        throughput_score = min(100, metrics.throughput * 10)  # Higher throughput = higher score
        amplitude_score = min(100, abs(metrics.amplitude) * 50)  # Optimal amplitude range
        
        quality_score = (
            snr_score * weights['snr'] +
            distortion_score * weights['distortion'] +
            latency_score * weights['latency'] +
            error_rate_score * weights['error_rate'] +
            throughput_score * weights['throughput'] +
            amplitude_score * weights['amplitude']
        )
        
        return round(quality_score, 2)
    
    def add_metrics(self, metrics: SignFXMetrics) -> None:
        """Add new metrics to history"""
        metrics.quality_score = self.calculate_quality_score(metrics)
        self.metrics_history.append(metrics)
        
        # Keep only last 1000 entries to prevent memory issues
        if len(self.metrics_history) > 1000:
            self.metrics_history = self.metrics_history[-1000:]
    
    def get_average_metrics(self, time_window_minutes: int = 5) -> Optional[SignFXMetrics]:
        """Get average metrics over specified time window"""
        if not self.metrics_history:
            return None
            
        cutoff_time = datetime.now() - timedelta(minutes=time_window_minutes)
        recent_metrics = [m for m in self.metrics_history if m.timestamp >= cutoff_time]
        
        if not recent_metrics:
            return None
        
        return SignFXMetrics(
            timestamp=datetime.now(),
            signal_strength=statistics.mean([m.signal_strength for m in recent_metrics]),
            noise_level=statistics.mean([m.noise_level for m in recent_metrics]),
            signal_to_noise_ratio=statistics.mean([m.signal_to_noise_ratio for m in recent_metrics]),
            frequency=statistics.mean([m.frequency for m in recent_metrics]),
            amplitude=statistics.mean([m.amplitude for m in recent_metrics]),
            phase=statistics.mean([m.phase for m in recent_metrics]),
            distortion=statistics.mean([m.distortion for m in recent_metrics]),
            latency=statistics.mean([m.latency for m in recent_metrics]),
            throughput=statistics.mean([m.throughput for m in recent_metrics]),
            error_rate=statistics.mean([m.error_rate for m in recent_metrics]),
            quality_score=statistics.mean([m.quality_score for m in recent_metrics])
        )
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get comprehensive metrics summary"""
        if not self.metrics_history:
            return {"error": "No metrics data available"}
        
        recent_metrics = self.metrics_history[-100:]  # Last 100 entries
        
        return {
            "total_measurements": len(self.metrics_history),
            "recent_measurements": len(recent_metrics),
            "current_quality_score": recent_metrics[-1].quality_score if recent_metrics else 0,
            "average_quality_score": statistics.mean([m.quality_score for m in recent_metrics]),
            "min_quality_score": min([m.quality_score for m in recent_metrics]),
            "max_quality_score": max([m.quality_score for m in recent_metrics]),
            "average_snr": statistics.mean([m.signal_to_noise_ratio for m in recent_metrics]),
            "average_latency": statistics.mean([m.latency for m in recent_metrics]),
            "average_throughput": statistics.mean([m.throughput for m in recent_metrics]),
            "average_error_rate": statistics.mean([m.error_rate for m in recent_metrics]),
            "last_updated": recent_metrics[-1].timestamp.isoformat() if recent_metrics else None
        }

# Global metrics calculator instance
metrics_calculator = SignFXMetricsCalculator()

# MCP Server setup
app = Server("signfx-metrics")

@app.list_tools()
async def handle_list_tools() -> ListToolsResult:
    """List available SignFX tools"""
    tools = [
        Tool(
            name="add_signfx_metrics",
            description="Add new SignFX metrics data point",
            inputSchema={
                "type": "object",
                "properties": {
                    "signal_strength": {"type": "number", "description": "Signal strength value"},
                    "noise_level": {"type": "number", "description": "Noise level value"},
                    "frequency": {"type": "number", "description": "Frequency in Hz"},
                    "amplitude": {"type": "number", "description": "Amplitude value"},
                    "phase": {"type": "number", "description": "Phase in radians"},
                    "distortion": {"type": "number", "description": "Distortion level (0-1)"},
                    "latency": {"type": "number", "description": "Latency in seconds"},
                    "throughput": {"type": "number", "description": "Throughput value"},
                    "error_rate": {"type": "number", "description": "Error rate (0-1)"}
                },
                "required": ["signal_strength", "noise_level", "frequency", "amplitude"]
            }
        ),
        Tool(
            name="get_signfx_summary",
            description="Get comprehensive SignFX metrics summary",
            inputSchema={
                "type": "object",
                "properties": {
                    "time_window_minutes": {"type": "integer", "description": "Time window for analysis in minutes", "default": 5}
                }
            }
        ),
        Tool(
            name="get_average_metrics",
            description="Get average SignFX metrics over time window",
            inputSchema={
                "type": "object",
                "properties": {
                    "time_window_minutes": {"type": "integer", "description": "Time window for averaging in minutes", "default": 5}
                }
            }
        ),
        Tool(
            name="simulate_signfx_data",
            description="Generate simulated SignFX metrics for testing",
            inputSchema={
                "type": "object",
                "properties": {
                    "num_samples": {"type": "integer", "description": "Number of samples to generate", "default": 10},
                    "base_frequency": {"type": "number", "description": "Base frequency for simulation", "default": 1000.0}
                }
            }
        )
    ]
    return ListToolsResult(tools=tools)

@app.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
    """Handle tool calls"""
    try:
        if name == "add_signfx_metrics":
            return await add_signfx_metrics(arguments)
        elif name == "get_signfx_summary":
            return await get_signfx_summary(arguments)
        elif name == "get_average_metrics":
            return await get_average_metrics(arguments)
        elif name == "simulate_signfx_data":
            return await simulate_signfx_data(arguments)
        else:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Unknown tool: {name}")]
            )
    except Exception as e:
        logger.error(f"Error handling tool {name}: {e}")
        return CallToolResult(
            content=[TextContent(type="text", text=f"Error: {str(e)}")]
        )

async def add_signfx_metrics(arguments: Dict[str, Any]) -> CallToolResult:
    """Add new SignFX metrics"""
    try:
        # Extract required parameters
        signal_strength = arguments.get("signal_strength", 0.0)
        noise_level = arguments.get("noise_level", 0.0)
        frequency = arguments.get("frequency", 1000.0)
        amplitude = arguments.get("amplitude", 1.0)
        phase = arguments.get("phase", 0.0)
        distortion = arguments.get("distortion", 0.0)
        latency = arguments.get("latency", 0.0)
        throughput = arguments.get("throughput", 0.0)
        error_rate = arguments.get("error_rate", 0.0)
        
        # Calculate SNR
        snr = metrics_calculator.calculate_snr(signal_strength, noise_level)
        
        # Create metrics object
        metrics = SignFXMetrics(
            timestamp=datetime.now(),
            signal_strength=signal_strength,
            noise_level=noise_level,
            signal_to_noise_ratio=snr,
            frequency=frequency,
            amplitude=amplitude,
            phase=phase,
            distortion=distortion,
            latency=latency,
            throughput=throughput,
            error_rate=error_rate,
            quality_score=0.0  # Will be calculated by add_metrics
        )
        
        # Add to calculator
        metrics_calculator.add_metrics(metrics)
        
        result = {
            "status": "success",
            "message": "SignFX metrics added successfully",
            "metrics": {
                "timestamp": metrics.timestamp.isoformat(),
                "signal_strength": metrics.signal_strength,
                "noise_level": metrics.noise_level,
                "signal_to_noise_ratio": round(metrics.signal_to_noise_ratio, 2),
                "frequency": metrics.frequency,
                "amplitude": metrics.amplitude,
                "phase": metrics.phase,
                "distortion": metrics.distortion,
                "latency": metrics.latency,
                "throughput": metrics.throughput,
                "error_rate": metrics.error_rate,
                "quality_score": metrics.quality_score
            }
        }
        
        return CallToolResult(
            content=[TextContent(type="text", text=json.dumps(result, indent=2))]
        )
        
    except Exception as e:
        return CallToolResult(
            content=[TextContent(type="text", text=f"Error adding metrics: {str(e)}")]
        )

async def get_signfx_summary(arguments: Dict[str, Any]) -> CallToolResult:
    """Get SignFX metrics summary"""
    try:
        summary = metrics_calculator.get_metrics_summary()
        return CallToolResult(
            content=[TextContent(type="text", text=json.dumps(summary, indent=2))]
        )
    except Exception as e:
        return CallToolResult(
            content=[TextContent(type="text", text=f"Error getting summary: {str(e)}")]
        )

async def get_average_metrics(arguments: Dict[str, Any]) -> CallToolResult:
    """Get average metrics over time window"""
    try:
        time_window = arguments.get("time_window_minutes", 5)
        avg_metrics = metrics_calculator.get_average_metrics(time_window)
        
        if avg_metrics is None:
            return CallToolResult(
                content=[TextContent(type="text", text="No metrics data available for the specified time window")]
            )
        
        result = {
            "time_window_minutes": time_window,
            "average_metrics": {
                "timestamp": avg_metrics.timestamp.isoformat(),
                "signal_strength": round(avg_metrics.signal_strength, 4),
                "noise_level": round(avg_metrics.noise_level, 4),
                "signal_to_noise_ratio": round(avg_metrics.signal_to_noise_ratio, 2),
                "frequency": round(avg_metrics.frequency, 2),
                "amplitude": round(avg_metrics.amplitude, 4),
                "phase": round(avg_metrics.phase, 4),
                "distortion": round(avg_metrics.distortion, 4),
                "latency": round(avg_metrics.latency, 4),
                "throughput": round(avg_metrics.throughput, 4),
                "error_rate": round(avg_metrics.error_rate, 4),
                "quality_score": avg_metrics.quality_score
            }
        }
        
        return CallToolResult(
            content=[TextContent(type="text", text=json.dumps(result, indent=2))]
        )
    except Exception as e:
        return CallToolResult(
            content=[TextContent(type="text", text=f"Error getting average metrics: {str(e)}")]
        )

async def simulate_signfx_data(arguments: Dict[str, Any]) -> CallToolResult:
    """Generate simulated SignFX data for testing"""
    try:
        import random
        import math
        
        num_samples = arguments.get("num_samples", 10)
        base_frequency = arguments.get("base_frequency", 1000.0)
        
        generated_samples = []
        
        for i in range(num_samples):
            # Generate realistic simulated data
            signal_strength = random.uniform(0.5, 2.0)
            noise_level = random.uniform(0.01, 0.2)
            frequency = base_frequency + random.uniform(-50, 50)
            amplitude = random.uniform(0.1, 2.0)
            phase = random.uniform(0, 2 * math.pi)
            distortion = random.uniform(0.0, 0.1)
            latency = random.uniform(0.001, 0.1)
            throughput = random.uniform(0.5, 2.0)
            error_rate = random.uniform(0.0, 0.05)
            
            # Calculate SNR
            snr = metrics_calculator.calculate_snr(signal_strength, noise_level)
            
            # Create metrics
            metrics = SignFXMetrics(
                timestamp=datetime.now() - timedelta(seconds=i*10),  # Spread over time
                signal_strength=signal_strength,
                noise_level=noise_level,
                signal_to_noise_ratio=snr,
                frequency=frequency,
                amplitude=amplitude,
                phase=phase,
                distortion=distortion,
                latency=latency,
                throughput=throughput,
                error_rate=error_rate,
                quality_score=0.0
            )
            
            metrics_calculator.add_metrics(metrics)
            generated_samples.append({
                "sample": i + 1,
                "timestamp": metrics.timestamp.isoformat(),
                "signal_strength": round(signal_strength, 4),
                "noise_level": round(noise_level, 4),
                "signal_to_noise_ratio": round(snr, 2),
                "frequency": round(frequency, 2),
                "amplitude": round(amplitude, 4),
                "quality_score": round(metrics.quality_score, 2)
            })
        
        result = {
            "status": "success",
            "message": f"Generated {num_samples} simulated SignFX samples",
            "samples": generated_samples
        }
        
        return CallToolResult(
            content=[TextContent(type="text", text=json.dumps(result, indent=2))]
        )
        
    except Exception as e:
        return CallToolResult(
            content=[TextContent(type="text", text=f"Error generating simulated data: {str(e)}")]
        )

async def main():
    """Main function to run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="signfx-metrics",
                server_version="1.0.0",
                capabilities=app.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None,
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())

