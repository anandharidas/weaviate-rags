#!/usr/bin/env python3
"""
SignFX MCP Tool Example Usage
Demonstrates how to use the SignFX metrics MCP tool.
"""

import asyncio
import json
from mcp.client import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def example_usage():
    """Example of using the SignFX MCP tool"""
    
    # Connect to the MCP server
    server_params = StdioServerParameters(
        command="python",
        args=["/Users/anandharidas/python/weaviate-rags/mcp_signfx_tool.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()
            
            print("🚀 SignFX MCP Tool Example")
            print("=" * 50)
            
            # 1. Generate some simulated data
            print("\n1. Generating simulated SignFX data...")
            simulate_result = await session.call_tool(
                "simulate_signfx_data",
                {"num_samples": 5, "base_frequency": 1000.0}
            )
            print("Simulation result:")
            print(json.dumps(json.loads(simulate_result.content[0].text), indent=2))
            
            # 2. Add a real metrics data point
            print("\n2. Adding real SignFX metrics...")
            add_result = await session.call_tool(
                "add_signfx_metrics",
                {
                    "signal_strength": 1.5,
                    "noise_level": 0.1,
                    "frequency": 1000.0,
                    "amplitude": 1.2,
                    "phase": 0.5,
                    "distortion": 0.02,
                    "latency": 0.05,
                    "throughput": 1.8,
                    "error_rate": 0.01
                }
            )
            print("Add metrics result:")
            print(json.dumps(json.loads(add_result.content[0].text), indent=2))
            
            # 3. Get metrics summary
            print("\n3. Getting SignFX metrics summary...")
            summary_result = await session.call_tool(
                "get_signfx_summary",
                {}
            )
            print("Summary result:")
            print(json.dumps(json.loads(summary_result.content[0].text), indent=2))
            
            # 4. Get average metrics
            print("\n4. Getting average metrics over 10 minutes...")
            avg_result = await session.call_tool(
                "get_average_metrics",
                {"time_window_minutes": 10}
            )
            print("Average metrics result:")
            print(json.dumps(json.loads(avg_result.content[0].text), indent=2))
            
            print("\n✅ Example completed successfully!")

async def interactive_mode():
    """Interactive mode for testing the SignFX tool"""
    
    server_params = StdioServerParameters(
        command="python",
        args=["/Users/anandharidas/python/weaviate-rags/mcp_signfx_tool.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("🔧 SignFX MCP Tool - Interactive Mode")
            print("=" * 50)
            print("Available commands:")
            print("1. add - Add new metrics")
            print("2. summary - Get metrics summary")
            print("3. average - Get average metrics")
            print("4. simulate - Generate simulated data")
            print("5. quit - Exit")
            
            while True:
                try:
                    command = input("\nEnter command (1-5): ").strip()
                    
                    if command == "1":
                        # Add metrics
                        signal_strength = float(input("Signal strength: "))
                        noise_level = float(input("Noise level: "))
                        frequency = float(input("Frequency: "))
                        amplitude = float(input("Amplitude: "))
                        
                        result = await session.call_tool(
                            "add_signfx_metrics",
                            {
                                "signal_strength": signal_strength,
                                "noise_level": noise_level,
                                "frequency": frequency,
                                "amplitude": amplitude
                            }
                        )
                        print("Result:", json.loads(result.content[0].text))
                        
                    elif command == "2":
                        # Get summary
                        result = await session.call_tool("get_signfx_summary", {})
                        print("Summary:", json.loads(result.content[0].text))
                        
                    elif command == "3":
                        # Get average
                        time_window = int(input("Time window (minutes): ") or "5")
                        result = await session.call_tool(
                            "get_average_metrics",
                            {"time_window_minutes": time_window}
                        )
                        print("Average:", json.loads(result.content[0].text))
                        
                    elif command == "4":
                        # Simulate data
                        num_samples = int(input("Number of samples: ") or "5")
                        result = await session.call_tool(
                            "simulate_signfx_data",
                            {"num_samples": num_samples}
                        )
                        print("Simulation:", json.loads(result.content[0].text))
                        
                    elif command == "5":
                        print("Goodbye!")
                        break
                        
                    else:
                        print("Invalid command. Please enter 1-5.")
                        
                except KeyboardInterrupt:
                    print("\nGoodbye!")
                    break
                except Exception as e:
                    print(f"Error: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        asyncio.run(interactive_mode())
    else:
        asyncio.run(example_usage())

