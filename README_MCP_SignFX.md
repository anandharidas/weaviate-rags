# SignFX MCP Tool

A Model Context Protocol (MCP) tool that provides comprehensive SignFX metrics functionality for signal analysis and monitoring.

## Features

- **Real-time Metrics Collection**: Add and track SignFX metrics including signal strength, noise levels, SNR, frequency, amplitude, phase, distortion, latency, throughput, and error rates
- **Quality Scoring**: Automatic calculation of quality scores based on multiple metrics
- **Time-based Analysis**: Get average metrics over configurable time windows
- **Data Simulation**: Generate realistic simulated SignFX data for testing
- **Comprehensive Reporting**: Detailed metrics summaries and statistics

## Installation

1. Install the required dependencies:
```bash
pip install -r mcp_requirements.txt
```

2. Make the tool executable:
```bash
chmod +x mcp_signfx_tool.py
```

## Configuration

The MCP tool can be configured using the `mcp_config.json` file:

```json
{
  "mcpServers": {
    "signfx-metrics": {
      "command": "python",
      "args": ["/path/to/mcp_signfx_tool.py"],
      "env": {
        "PYTHONPATH": "/path/to/your/project"
      }
    }
  }
}
```

## Available Tools

### 1. add_signfx_metrics
Add new SignFX metrics data point.

**Parameters:**
- `signal_strength` (number, required): Signal strength value
- `noise_level` (number, required): Noise level value
- `frequency` (number, required): Frequency in Hz
- `amplitude` (number, required): Amplitude value
- `phase` (number, optional): Phase in radians
- `distortion` (number, optional): Distortion level (0-1)
- `latency` (number, optional): Latency in seconds
- `throughput` (number, optional): Throughput value
- `error_rate` (number, optional): Error rate (0-1)

### 2. get_signfx_summary
Get comprehensive SignFX metrics summary.

**Parameters:**
- `time_window_minutes` (integer, optional): Time window for analysis in minutes (default: 5)

### 3. get_average_metrics
Get average SignFX metrics over time window.

**Parameters:**
- `time_window_minutes` (integer, optional): Time window for averaging in minutes (default: 5)

### 4. simulate_signfx_data
Generate simulated SignFX metrics for testing.

**Parameters:**
- `num_samples` (integer, optional): Number of samples to generate (default: 10)
- `base_frequency` (number, optional): Base frequency for simulation (default: 1000.0)

## Usage Examples

### Basic Usage

```python
import asyncio
from mcp.client import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["/path/to/mcp_signfx_tool.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Add metrics
            result = await session.call_tool(
                "add_signfx_metrics",
                {
                    "signal_strength": 1.5,
                    "noise_level": 0.1,
                    "frequency": 1000.0,
                    "amplitude": 1.2
                }
            )
            print(result.content[0].text)

asyncio.run(main())
```

### Running the Example

```bash
# Run the example script
python signfx_example.py

# Run in interactive mode
python signfx_example.py interactive
```

## Metrics Explained

### Signal-to-Noise Ratio (SNR)
Calculated as: `20 * log10(signal_strength / noise_level)`
- Higher values indicate better signal quality
- Measured in decibels (dB)

### Quality Score
A weighted composite score (0-100) based on:
- SNR (30% weight)
- Distortion (20% weight)
- Latency (15% weight)
- Error rate (15% weight)
- Throughput (10% weight)
- Amplitude (10% weight)

### Time Windows
- Metrics are stored with timestamps
- Analysis can be performed over configurable time windows
- Default time window is 5 minutes
- Maximum history: 1000 data points

## Error Handling

The tool includes comprehensive error handling:
- Input validation for all parameters
- Graceful handling of missing data
- Clear error messages for debugging
- Automatic data cleanup to prevent memory issues

## Performance Considerations

- Maximum 1000 metrics stored in memory
- Automatic cleanup of old data
- Efficient statistical calculations
- Minimal memory footprint

## Integration

This MCP tool can be integrated with:
- Signal processing applications
- Real-time monitoring systems
- Quality assurance tools
- Data analysis pipelines
- Machine learning workflows

## License

This tool is provided as-is for educational and development purposes.


