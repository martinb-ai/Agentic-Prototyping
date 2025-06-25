# Developer Quickstart

The OpenAI API provides a simple interface to state-of-the-art AI models for text generation, natural language processing, computer vision, and more. This example generates text output from a prompt, as you might using ChatGPT.

```python
# Initalize Openai Client library and Setup API keys
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize the client with API key from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```

## Text Creation

```python
response = client.responses.create(
    model="gpt-4.1",
    input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)
```
Output
```bash
Under a silver moon, a gentle unicorn named Luna tiptoed through a sparkling forest, leaving trails of twinkling stardust and sweet dreams for all the sleeping creatures.
```

## Analyze Image Inputs

You can provide image inputs to the model as well. Scan receipts, analyze screenshots, or find objects in the real world with computer vision.

```python
response = client.responses.create(
    model="gpt-4.1",
    input=[
        {"role": "user", "content": "What two dogs are in this image?"},
        {
            "role": "user",
            "content": [
                {
                    "type": "input_image",
                    "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Comparison_of_a_wolf_and_a_pug.png/1920px-Comparison_of_a_wolf_and_a_pug.png"
                }
            ]
        }
    ]
)

print(response.output_text)
```

Passing a Base64 encoded Image (local images)
```python
import base64

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Path to your image
image_path = "images/multi_agent_orchestration.png"

# Getting the Base64 string
base64_image = encode_image(image_path)


response = client.responses.create(
    model="gpt-4.1",
    input=[
        {
            "role": "user",
            "content": [
                { "type": "input_text", "text": "what's in this image?" },
                {
                    "type": "input_image",
                    "image_url": f"data:image/jpeg;base64,{base64_image}",
                },
            ],
        }
    ],
)

print(response.output_text)
```

Output:
```bash
This image is a flowchart illustrating a "manager-agent" system for translating the word "hello" into Spanish, French, and Italian.

Here's a breakdown of what's depicted:

1. **Input (Left Side):**
    - A request: "Translate 'hello' to Spanish, French and Italian for me!" 
    - Another unspecified input indicated by "..."

2. **Manager (Center):**
    - The "Manager" box receives the input requests.
    - The manager breaks down the main translation request into individual translation tasks.

3. **Tasks (Right of Manager):**
    - Three dashed boxes labeled "Task" represent task assignments.
    - Each task is sent to a specific "agent":
      - Spanish agent
      - French agent
      - Italian agent

4. **Agents (Far Right):**
    - Each agent (Spanish, French, Italian) handles the specific task.
    - The tasks and results are sent back and forth between the manager and the agents.

**Purpose:**  
The diagram visualizes how a manager (or orchestrator) can distribute complex requests into subtasks and assign them to specialized agents, then collect their results to respond to the original request. In this case, it's used for translating "hello" into multiple languages via specialized language agents.
```

Specify image input detail level

The `detail` parameter tells the model what level of detail to use when processing and understanding the image (`low`, `high`, or `auto` to let the model decide). If you skip the parameter, the model will use auto.

Output:
```bash
{
    "type": "input_image",
    "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
    "detail": "high"
}
```

You can save tokens and speed up responses by using `"detail": "low"`. This lets the model process the image with a budget of 85 tokens. The model receives a low-resolution 512px x 512px version of the image. This is fine if your use case doesn't require the model to see with high-resolution detail (for example, if you're asking about the dominant shape or color in the image).

On the other hand, you can use `"detail": "high"` if you want the model to have a better understanding of the image.

#### Image Input Requirements

Input images must meet the following requirements to be used in the API.

##### Supported File Types
- PNG (.png)
- JPEG (.jpeg and .jpg)
- WEBP (.webp)
- Non-animated GIF (.gif)

##### Size Limits
- Up to 50 MB total payload size per request
- Up to 500 individual image inputs per request

##### Other Requirements
- No watermarks or logos
- No NSFW content
- Clear enough for a human to understand


### Limitations
While models with vision capabilities are powerful and can be used in many situations, it's important to understand the limitations of these models. Here are some known limitations:

- Medical images: The model is not suitable for interpreting specialized medical images like CT scans and shouldn't be used for medical advice.
- Non-English: The model may not perform optimally when handling images with text of non-Latin alphabets, such as Japanese or Korean.
- Small text: Enlarge text within the image to improve readability, but avoid cropping important details.
- Rotation: The model may misinterpret rotated or upside-down text and images.
- Visual elements: The model may struggle to understand graphs or text where colors or styles—like solid, dashed, or dotted lines—vary.
- Spatial reasoning: The model struggles with tasks requiring precise spatial localization, such as identifying chess positions.
- Accuracy: The model may generate incorrect descriptions or captions in certain scenarios.
- Image shape: The model struggles with panoramic and fisheye images.
- Metadata and resizing: The model doesn't process original file names or metadata, and images are resized before analysis, affecting their original dimensions.
- Counting: The model may give approximate counts for objects in images.
- CAPTCHAS: For safety reasons, our system blocks the submission of CAPTCHAs.

## Extend the model with tools

Give the model access to new data and capabilities using tools. You can either call your own custom code, or use one of OpenAI's powerful built-in tools. This example uses web search to give the model access to the latest information on the Internet.

```python
response = client.responses.create(
    model="gpt-4.1",
    tools=[{"type": "web_search_preview"}],
    input="What was a positive news story from today?"
)

print(response.output_text)
````

Output:
```bash
As of June 23, 2025, one notable positive news story is the successful reintroduction of helmeted honeyeaters to Cardinia in Victoria, Australia. These critically endangered birds have returned to the area for the first time since the Ash Wednesday bushfires in 1983, marking a significant milestone in conservation efforts. ([globalgoodnews.com](https://globalgoodnews.com/?utm_source=openai))

Additionally, a 14-year-old from Dallas, Siddharth Nandyala, has developed an AI-powered app capable of detecting heart disease in just seven seconds using only a smartphone's microphone. This innovation has the potential to revolutionize early detection and treatment of heart conditions. ([globalgoodnews.com](https://globalgoodnews.com/?utm_source=openai))

Furthermore, the Yurok Tribe in the United States is celebrating the return of ancestral homelands, following historic dam removals. This restoration supports the tribe's cultural and environmental initiatives. ([goodnewsnetwork.org](https://www.goodnewsnetwork.org/?utm_source=openai))

These stories highlight significant advancements in environmental conservation, technological innovation, and cultural restoration.
```

## Deliver blazing fast AI experiences

Using either the new Realtime API or server-sent streaming events, you can build high performance, low-latency experiences for your users.

```python
stream = client.responses.create(
    model="gpt-4.1",
    input=[
        {
            "role": "user",
            "content": "Say 'double bubble bath'.",
        },
    ],
    stream=True,
)
```

## Build agents

Use the OpenAI platform to build agents capable of taking action—like controlling computers—on behalf of your users. Use the Agents SDK for Python or TypeScript to create orchestration logic on the backend.

```python
import asyncio
from agents import Agent, Runner

spanish_agent = Agent(
    name="Spanish agent",
    instructions="You only speak Spanish.",
)

english_agent = Agent(
    name="English agent",
    instructions="You only speak English",
)

triage_agent = Agent(
    name="Triage agent",
    instructions="Handoff to the appropriate agent based on the language of the request.",
    handoffs=[spanish_agent, english_agent],
)

# Define your async function
async def main():
    result = await Runner.run(triage_agent, input="Hola, ¿cómo estás?")
    return result.final_output

# In Jupyter, use await directly
result = await main()
print(result)
```

Output:
```bash
Hola, estoy bien, gracias. ¿Y tú, cómo estás?
```