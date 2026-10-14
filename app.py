import gradio as gr
import os
import time
import matplotlib.pyplot as plt
import numpy as np

# Import services
from services.audio import extract_audio, get_playable_video
from services.asr import transcribe
from services.scoring import evaluate, generate_feedback
from utils.text_cleaner import clean_text

# --- Luminal Insight Design Tokens ---
COLOR_BG = "#0b0d17"
COLOR_CARD = "#1b1d29"
COLOR_ACCENT = "#9d70ff"
COLOR_TEXT_PRIMARY = "#ffffff"
COLOR_TEXT_SECONDARY = "#9ca3af"

# Custom CSS for Premium Dashboard
custom_css = f"""
body {{ 
    background-color: {COLOR_BG}; 
    color: {COLOR_TEXT_PRIMARY}; 
}}
.gradio-container {{ 
    background-color: {COLOR_BG}; 
    max-width: 100% !important;
}}
.sidebar-box {{
    background-color: {COLOR_BG};
    border-right: 1px solid #1f2937;
    padding: 20px;
}}
.metric-card {{
    background: {COLOR_CARD};
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #1f2937;
    text-align: center;
}}
.feedback-card {{
    background: {COLOR_CARD};
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #1f2937;
}}
footer {{ visibility: hidden; }}
"""

# --- Dashboard Helper Functions ---

def generate_chart(scores):
    if not scores:
        return None
    
    labels = [k.replace('_', ' ').title() for k in scores.keys()]
    values = list(scores.values())

    plt.figure(figsize=(10, 5))
    # Using Lavender and Deep Blue for bars
    plt.bar(labels, values, color=[COLOR_ACCENT, '#7c3aed', '#6d28d9', '#5b21b6'], width=0.6)
    plt.ylim(0, 10)
    plt.title("Detailed Performance Analysis", color=COLOR_TEXT_PRIMARY, fontsize=14, pad=20)
    plt.xticks(color=COLOR_TEXT_SECONDARY, fontsize=10)
    plt.yticks(color=COLOR_TEXT_SECONDARY, fontsize=10)
    
    # Theme dark background
    plt.gcf().patch.set_facecolor(COLOR_CARD)
    plt.gca().set_facecolor(COLOR_CARD)
    plt.gca().spines['bottom'].set_color('#374151')
    plt.gca().spines['left'].set_color('#374151')
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().yaxis.grid(True, linestyle='--', alpha=0.1)
    
    plt.tight_layout()
    return plt

def get_match_score_html(scores):
    if not scores:
        return ""
    # Simple average for "AI Composite Score"
    avg_score = sum(scores.values()) / len(scores)
    percentage = int(avg_score * 10)
    
    return f"""
    <div style="background: {COLOR_CARD}; border: 1px solid #1f2937; border-radius: 16px; padding: 40px; text-align: center; margin-bottom: 20px;">
        <div style="color: {COLOR_TEXT_SECONDARY}; font-size: 0.9em; text-transform: uppercase; letter-spacing: 1px;">Match Score</div>
        <div style="color: {COLOR_TEXT_SECONDARY}; font-size: 0.7em; margin-bottom: 10px;">AI COMPOSITE SCORE</div>
        <div style="font-size: 5em; font-weight: 800; color: {COLOR_ACCENT}; line-height: 1;">{percentage}%</div>
        <div style="margin-top: 15px; font-size: 0.9em; color: {COLOR_TEXT_SECONDARY};">Based on Task Completion, Communication, Quality, and Judgement.</div>
    </div>
    """

def format_feedback_card(items, title, icon="💠", color="#3b82f6"):
    content = "\n".join([f"• {item}" for item in items]) if items else "_Pending analysis..._"
    return f"""
    <div style="background: {COLOR_CARD}; border: 1px solid #1f2937; border-radius: 12px; padding: 20px; min-height: 200px;">
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px;">
            <span style="font-size: 1.5em;">{icon}</span>
            <span style="font-weight: 600; color: {COLOR_TEXT_PRIMARY}; font-size: 1.1em;">{title}</span>
        </div>
        <div style="color: {COLOR_TEXT_SECONDARY}; font-size: 0.95em; line-height: 1.6;">
            {content}
        </div>
    </div>
    """

# --- Main Processing Wrapper ---

def process_interview(file):
    if file is None:
        return "", None, "", "", "", "⏱ Processing Time: --", None

    start_time = time.time()
    try:
        file_path = file.name if hasattr(file, "name") else file
        
        # Original Pipeline
        audio_path = extract_audio(file_path)
        if not audio_path: raise Exception("Audio extraction failed")
        
        text = transcribe(audio_path)
        if not text: raise Exception("Transcription failed")
        
        cleaned_text = clean_text(text)
        scores = evaluate(cleaned_text)
        feedback = generate_feedback(cleaned_text, scores)
        playable_video_path = get_playable_video(file_path)

        proc_time = f"{time.time() - start_time:.2f}s"
        
        # "Luminal Insight" Refined Outputs
        match_score_html = get_match_score_html(scores)
        chart_plot = generate_chart(scores)
        strengths_html = format_feedback_card(feedback.get("strengths", []), "Strengths", "💠", COLOR_ACCENT)
        improvements_html = format_feedback_card(feedback.get("improvements", []), "Areas for Improvement", "⚠️", "#ef4444")
        time_footer = f"⏱ Processing Time: **{proc_time}**"

        return cleaned_text, chart_plot, match_score_html, strengths_html, improvements_html, time_footer, playable_video_path

    except Exception as e:
        return f"Error: {str(e)}", None, "<div>Error during analysis</div>", "", "", "⏱ Processing Time: Error", None

# --- UI Layout ---

with gr.Blocks(theme=gr.themes.Base(), css=custom_css, title="Luminal Insight | Interview Assist") as demo:
    with gr.Row():
        # --- Left Branding / Nav Column (Static for now) ---
        with gr.Column(scale=1, elem_classes="sidebar-box", min_width=250):
            
            # Action Area
            input_file = gr.File(label="Upload Interview Recording", file_types=["video", "audio"])
            submit_btn = gr.Button("Analyze Interview", variant="primary")
            clear_btn = gr.Button("Reset", variant="secondary")

        # --- Main Analysis Dashboard ---
        with gr.Column(scale=4):
            gr.Markdown("# Interview Assist Dashboard")
            gr.Markdown("Unlock deep behavioral insights using generative AI analysis.")
            
            with gr.Tabs():
                with gr.TabItem("📊 Analysis & Scores"):
                    with gr.Row():
                        with gr.Column(scale=1):
                            # Big Match Score
                            match_score_display = gr.HTML(label="Composite Match Score")
                            
                            with gr.Accordion("Original Transcript", open=False):
                                output_text = gr.Textbox(label="Transcript", lines=10)
                        
                        with gr.Column(scale=2):
                            # Performance Chart Panel
                            score_plot = gr.Plot(label="Performance Metrics")
                            
                            with gr.Row():
                                strengths_display = gr.HTML(label="Strengths")
                                improvements_display = gr.HTML(label="Improvements")
                    
                    footer_time = gr.Markdown("⏱ Processing Time: --")

                with gr.TabItem("🎬 Playable Preview"):
                    output_video = gr.Video(label="Playable Interview Video")
            
            # Subtle Footer Branding
            gr.Markdown("---")
            gr.Markdown("❖ USE VIA API   ⚡ BUILT WITH GRADIO   © 2024 Luminal Insight. All intelligence reserved.")

    # Event handlers
    submit_btn.click(
        fn=process_interview,
        inputs=input_file,
        outputs=[output_text, score_plot, match_score_display, strengths_display, improvements_display, footer_time, output_video]
    )
    
    clear_btn.click(
        fn=lambda: ["", None, "<div></div>", "", "", "⏱ Processing Time: --", None],
        outputs=[output_text, score_plot, match_score_display, strengths_display, improvements_display, footer_time, output_video]
    )

if __name__ == "__main__":
    demo.launch()