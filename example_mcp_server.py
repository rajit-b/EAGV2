# basic import 
from mcp.server.fastmcp import FastMCP, Image
from mcp.server.fastmcp.prompts import base
from mcp.types import TextContent
from mcp import types
from PIL import Image as PILImage
import math
import sys
import subprocess
import time
import platform

# Try to import Mac-specific libraries, fall back gracefully
try:
    import pyautogui
    MAC_AUTOMATION_AVAILABLE = True
except ImportError:
    MAC_AUTOMATION_AVAILABLE = False
    print("Warning: pyautogui not available. GUI automation features will be limited.")

# instantiate an MCP server client
mcp = FastMCP("Calculator")

# Global variable to track Preview app
preview_app = None

# DEFINE TOOLS

#addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    print("CALLED: add(a: int, b: int) -> int:")
    return int(a + b)

@mcp.tool()
def add_list(l: list) -> int:
    """Add all numbers in a list"""
    print("CALLED: add(l: list) -> int:")
    return sum(l)

# subtraction tool
@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    print("CALLED: subtract(a: int, b: int) -> int:")
    return int(a - b)

# multiplication tool
@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    print("CALLED: multiply(a: int, b: int) -> int:")
    return int(a * b)

#  division tool
@mcp.tool() 
def divide(a: int, b: int) -> float:
    """Divide two numbers"""
    print("CALLED: divide(a: int, b: int) -> float:")
    return float(a / b)

# power tool
@mcp.tool()
def power(a: int, b: int) -> int:
    """Power of two numbers"""
    print("CALLED: power(a: int, b: int) -> int:")
    return int(a ** b)

# square root tool
@mcp.tool()
def sqrt(a: int) -> float:
    """Square root of a number"""
    print("CALLED: sqrt(a: int) -> float:")
    return float(a ** 0.5)

# cube root tool
@mcp.tool()
def cbrt(a: int) -> float:
    """Cube root of a number"""
    print("CALLED: cbrt(a: int) -> float:")
    return float(a ** (1/3))

# factorial tool
@mcp.tool()
def factorial(a: int) -> int:
    """factorial of a number"""
    print("CALLED: factorial(a: int) -> int:")
    return int(math.factorial(a))

# log tool
@mcp.tool()
def log(a: int) -> float:
    """log of a number"""
    print("CALLED: log(a: int) -> float:")
    return float(math.log(a))

# remainder tool
@mcp.tool()
def remainder(a: int, b: int) -> int:
    """remainder of two numbers divison"""
    print("CALLED: remainder(a: int, b: int) -> int:")
    return int(a % b)

# sin tool
@mcp.tool()
def sin(a: int) -> float:
    """sin of a number"""
    print("CALLED: sin(a: int) -> float:")
    return float(math.sin(a))

# cos tool
@mcp.tool()
def cos(a: int) -> float:
    """cos of a number"""
    print("CALLED: cos(a: int) -> float:")
    return float(math.cos(a))

# tan tool
@mcp.tool()
def tan(a: int) -> float:
    """tan of a number"""
    print("CALLED: tan(a: int) -> float:")
    return float(math.tan(a))

# mine tool
@mcp.tool()
def mine(a: int, b: int) -> int:
    """special mining tool"""
    print("CALLED: mine(a: int, b: int) -> int:")
    return int(a - b - b)

@mcp.tool()
def create_thumbnail(image_path: str) -> Image:
    """Create a thumbnail from an image"""
    print("CALLED: create_thumbnail(image_path: str) -> Image:")
    img = PILImage.open(image_path)
    img.thumbnail((100, 100))
    return Image(data=img.tobytes(), format="png")

@mcp.tool()
def strings_to_chars_to_int(string: str) -> list[int]:
    """Return the ASCII values of the characters in a word"""
    print("CALLED: strings_to_chars_to_int(string: str) -> list[int]:")
    return [int(ord(char)) for char in string]

@mcp.tool()
def int_list_to_exponential_sum(int_list: list) -> float:
    """Return sum of exponentials of numbers in a list"""
    print("CALLED: int_list_to_exponential_sum(int_list: list) -> float:")
    return sum(math.exp(i) for i in int_list)

@mcp.tool()
def fibonacci_numbers(n: int) -> list:
    """Return the first n Fibonacci Numbers"""
    print("CALLED: fibonacci_numbers(n: int) -> list:")
    if n <= 0:
        return []
    fib_sequence = [0, 1]
    for _ in range(2, n):
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence[:n]


@mcp.tool()
async def draw_rectangle() -> dict:
    """Draw a rectangle in Preview's markup tools"""
    global preview_app
    try:
        if not MAC_AUTOMATION_AVAILABLE:
            return {
                # "content": [
                #     TextContent(
                #         type="text",
                #         text="GUI automation not available. Please install: pip install pyautogui"
                #     )
                # ]
                "GUI automation not available. Please install: pip install pyautogui"
            }
        
        if not preview_app:
            return {
                "content": [
                    TextContent(
                        type="text",
                        text="Preview is not open. Please call open_preview first."
                    )
                ]
            }

        # Activate Preview
        subprocess.run(['osascript', '-e', 'tell application "Preview" to activate'], check=True)
        time.sleep(0.5)
        
        # Enable markup toolbar (Cmd+Shift+A)
        pyautogui.hotkey('command', 'shift', 'A')
        time.sleep(0.5)

        print("RAJIT: Adding Cmd+Shift+A for the 2nd time")
        
        # Enable markup toolbar (Cmd+Shift+A)
        pyautogui.hotkey('command', 'shift', 'A')
        time.sleep(0.5)
        
        # Click on Shapes tool
        pyautogui.click(x=441, y=108)
        time.sleep(0.5)

        # Click on Rectangle shape - this automatically adds the rectangle
        pyautogui.click(x=415, y=173)
        time.sleep(0.5)
        
        return {
            # "content": [
            #     TextContent(
            #         type="text",
            #         text=f"Rectangle added to canvas"
            #     )
            # ]
            "Rectangle added to canvas"
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error drawing rectangle: {str(e)}"
                )
            ]
        }

@mcp.tool()
async def draw_rectangle_and_text(text: str) -> dict:
    """Draw a rectangle and add text in Preview at specified position"""
    global preview_app
    try:
        if not MAC_AUTOMATION_AVAILABLE:
            return {
                "content": [
                    TextContent(
                        type="text",
                        text="GUI automation not available. Please install: pip install pyautogui"
                    )
                ]
            }
        
        if not preview_app:
            return {
                "content": [
                    TextContent(
                        type="text",
                        text="Preview is not open. Please call open_preview first."
                    )
                ]
            }
        
        # Activate Preview
        subprocess.run(['osascript', '-e', 'tell application "Preview" to activate'], check=True)
        time.sleep(0.5)


        pyautogui.hotkey('command', 'control', 't')
        time.sleep(0.5)
        
        # Type the text
        pyautogui.write(text, interval=0.05)
        time.sleep(0.5)
        
        # Click elsewhere to deselect
        pyautogui.press('escape')
        
        return {
            # "content": [
            #     TextContent(
            #         type="text",
            #         text=f"Text '{text}' added successfully at ({x}, {y})"
            #     )
            # ]
            "Text '"+text+"' added successfully"
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )
            ]
        }


@mcp.tool()
async def open_preview() -> dict:
    """Open Preview app with a new blank document"""
    global preview_app
    try:
        # Create a temporary blank image
        temp_image_path = "/tmp/blank_canvas.png"
        blank_img = PILImage.new('RGB', (800, 600), color='white')
        blank_img.save(temp_image_path)
        
        # Open Preview with the blank image
        subprocess.run(['open', '-a', 'Preview', temp_image_path], check=True)
        preview_app = True
        time.sleep(0.5)
        
        # Try to maximize using AppleScript (simpler approach without NSScreen)
        try:
            # Get display info using system_profiler
            result = subprocess.run(
                ['system_profiler', 'SPDisplaysDataType'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            # Simple approach: just activate and try to maximize
            script = '''
            tell application "Preview"
                activate
            end tell
            tell application "System Events"
                tell process "Preview"
                    set frontmost to true
                    -- Try to maximize (green button or full screen)
                    -- keystroke "f" using {control down, command down}
                end tell
            end tell
            '''
            subprocess.run(['osascript', '-e', script], check=True)
        except Exception as script_error:
            print(f"Warning: Could not maximize window: {script_error}")
            # Just activate Preview if maximizing fails
            subprocess.run(['osascript', '-e', 'tell application "Preview" to activate'], check=True)
        
        time.sleep(0.3)
        
        return {
            # "content": [
            #     TextContent(
            #         type="text",
            #         text="Preview opened successfully with blank canvas"
            #     )
            # ]
            "Preview opened successfully with blank canvas"
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error opening Preview: {str(e)}"
                )
            ]
        }

# DEFINE RESOURCES

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    print("CALLED: get_greeting(name: str) -> str:")
    return f"Hello, {name}!"


# DEFINE AVAILABLE PROMPTS
@mcp.prompt()
def review_code(code: str) -> str:
    print("CALLED: review_code(code: str) -> str:")
    return f"Please review this code:\n\n{code}"


@mcp.prompt()
def debug_error(error: str) -> list[base.Message]:
    return [
        base.UserMessage("I'm seeing this error:"),
        base.UserMessage(error),
        base.AssistantMessage("I'll help debug that. What have you tried so far?"),
    ]

if __name__ == "__main__":
    # Check if running with mcp dev command
    print("STARTING")
    if len(sys.argv) > 1 and sys.argv[1] == "dev":
        mcp.run()  # Run without transport for dev server
    else:
        mcp.run(transport="stdio")  # Run with stdio for direct execution
