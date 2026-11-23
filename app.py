
import gradio as gr
from google import genai

def generate_plan(goal, level, minutes, equipment, api_key):

    if not api_key:
        return "Please enter your Gemini API key."

    client = genai.Client(api_key=api_key)

    prompt = f"""
    You are a fitness routine planner.

    Create a simple weekly home workout plan using these details:

    Fitness goal: {goal}
    Fitness level: {level}
    Available time per day: {minutes} minutes
    Equipment available: {equipment}

    Include:
    1. A Monday to Sunday workout schedule
    2. Exercises for each workout day
    3. Sets and repetitions or duration
    4. Rest days
    5. Warm-up and cool-down
    6. Rest time between sets
    7. Simple safety instructions

    Keep the plan realistic and easy to understand.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"Error generating plan: {str(e)}"


with gr.Blocks(title="Fitness Routine Planner") as demo:

    gr.Markdown("# Fitness Routine Planner")

    gr.Markdown(
        "Generate a personalized weekly home workout plan."
    )

    api_key = gr.Textbox(
        label="Gemini API Key",
        placeholder="Enter your Gemini API key",
        type="password"
    )

    goal = gr.Dropdown(
        choices=[
            "Weight loss",
            "Build strength",
            "Improve flexibility",
            "General fitness"
        ],
        label="Fitness Goal",
        value="General fitness"
    )

    level = gr.Dropdown(
        choices=[
            "Beginner",
            "Intermediate",
            "Advanced"
        ],
        label="Fitness Level",
        value="Beginner"
    )

    minutes = gr.Slider(
        minimum=10,
        maximum=60,
        value=30,
        step=5,
        label="Minutes available per day"
    )

    equipment = gr.Dropdown(
        choices=[
            "None",
            "Yoga mat",
            "Resistance bands",
            "Dumbbells",
            "Basic home equipment"
        ],
        label="Available Equipment",
        value="None"
    )

    generate_button = gr.Button(
        "Generate Weekly Plan",
        variant="primary"
    )

    output = gr.Markdown()

    generate_button.click(
        fn=generate_plan,
        inputs=[
            goal,
            level,
            minutes,
            equipment,
            api_key
        ],
        outputs=output
    )

demo.launch(share=True)
