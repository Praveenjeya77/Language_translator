"""
Gradio Web Interface for Translation
Beautiful and user-friendly web interface
"""

import gradio as gr
import socket
import sys
sys.path.append('..')

from src.api_translator import APITranslator
from src.utils import get_language_name, get_native_name
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def safe_print(message: str):
    """Print helper that degrades gracefully on consoles without Unicode support."""
    try:
        print(message)
    except UnicodeEncodeError:
        fallback = message.encode("ascii", errors="ignore").decode("ascii")
        print(fallback)


def get_available_port(preferred_port: int = 7860) -> int:
    """Return preferred port if free, otherwise pick a random available port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind(("", preferred_port))
            return preferred_port
        except OSError:
            sock.bind(("", 0))
            return sock.getsockname()[1]


class TranslationApp:
    """Web application for translation"""
    
    def __init__(self):
        self.translators = {}
        logger.info("Translation app initialized")
    
    def get_translator(self, source_lang: str, target_lang: str):
        """Get or create translator for language pair"""
        key = f"{source_lang}_{target_lang}"
        if key not in self.translators:
            self.translators[key] = APITranslator(source_lang, target_lang)
        return self.translators[key]
    
    def translate(self, text: str, source_lang: str) -> str:
        """Translate text"""
        if not text or not text.strip():
            return "⚠️ Please enter some text to translate"
        
        try:
            # Extract language code
            lang_map = {
                'Tamil (தமிழ்)': 'ta',
                'Hindi (हिन्दी)': 'hi',
                'Telugu (తెలుగు)': 'te'
            }
            source_code = lang_map.get(source_lang, 'ta')
            
            translator = self.get_translator(source_code, 'en')
            result = translator.translate(text)
            
            return result
        except Exception as e:
            logger.error(f"Translation error: {e}")
            return f"❌ Error: {str(e)}"
    
    def create_interface(self):
        """Create Gradio interface"""
        
        # Custom theme & CSS
        app_theme = gr.themes.Soft(
            primary_hue="indigo",
            secondary_hue="amber",
            neutral_hue="slate"
        ).set(
            button_primary_background_fill="#f97316",
            button_primary_border_color="#f97316",
            button_secondary_border_color="#94a3b8",
            button_secondary_text_color="#0f172a",
            block_background_fill="#0f172a",
            block_border_width="0px"
        )
        
        custom_css = """
        body {
            background: radial-gradient(circle at top, #1d4ed8, #0f172a 55%);
            color: #e2e8f0;
        }
        .app-wrapper {
            max-width: 1200px;
            margin: 0 auto;
            padding: 24px 12px 48px;
        }
        .header {
            text-align: center;
            padding: 32px;
            background: linear-gradient(125deg, rgba(56,189,248,0.95), rgba(129,140,248,0.95));
            color: white;
            border-radius: 24px;
            margin-bottom: 32px;
            box-shadow: 0 20px 45px rgba(14, 165, 233, 0.25);
        }
        .header h1 {
            font-size: 2.4rem;
            margin-bottom: 8px;
        }
        .header p {
            font-size: 1.05rem;
            opacity: 0.95;
        }
        .accent-card {
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid rgba(148, 163, 184, 0.45);
            border-radius: 16px;
            padding: 18px 20px;
            margin-top: 16px;
            color: #f8fafc;
        }
        .accent-card ul {
            margin-top: 12px;
            color: #cbd5f5;
        }
        .action-buttons button {
            width: 100%;
            height: 52px;
            font-size: 17px;
            font-weight: 600;
        }
        .action-buttons .gr-button-primary {
            background: linear-gradient(135deg, #f97316, #fb7185);
            border: none;
            color: #fff;
        }
        .action-buttons .gr-button-primary:hover {
            opacity: 0.95;
        }
        .gradio-container .gr-textbox textarea {
            background: rgba(15, 23, 42, 0.65);
            border: 1px solid rgba(148, 163, 184, 0.35);
            color: #f8fafc;
        }
        .gradio-container .gr-dropdown button {
            background: rgba(15, 23, 42, 0.65);
            border: 1px solid rgba(148, 163, 184, 0.35);
            color: #f8fafc;
        }
        .gr-markdown h3 {
            color: #e2e8f0 !important;
        }
        """
        
        with gr.Blocks(
            title="Indian Language Translator",
            theme=app_theme,
            css=custom_css
        ) as app:
            
            with gr.Column(elem_classes=["app-wrapper"]):
                gr.Markdown("""
                <div class="header">
                    <h1>🈯 Language Translator</h1>
                    <p>Translate seamlessly between Indian languages and English</p>
                </div>
                """)
                
                with gr.Row():
                    with gr.Column(scale=1):
                        gr.Markdown("### 📝 Input")
                        
                        source_lang = gr.Dropdown(
                            choices=['Tamil (தமிழ்)', 'Hindi (हिन्दी)', 'Telugu (తెలుగు)'],
                            value='Tamil (தமிழ்)',
                            label="Source Language",
                            interactive=True
                        )
                        
                        input_text = gr.Textbox(
                            label="Enter Text",
                            placeholder="Type or paste your text here...",
                            lines=8,
                            max_lines=15
                        )
                        
                        with gr.Row(elem_classes=["action-buttons"], equal_height=True):
                            clear_btn = gr.Button("🧹 Clear Text", variant="secondary")
                            translate_btn = gr.Button("⚡ Translate Now", variant="primary")
                    
                    with gr.Column(scale=1):
                        gr.Markdown("### 📄 Translation")
                        
                        output_text = gr.Textbox(
                            label="English Translation",
                            lines=8,
                            max_lines=15,
                            interactive=False
                        )
                
                gr.Markdown("---")
                gr.Markdown("### 💡 Try These Examples")
                
                gr.Examples(
                    examples=[
                        ["உணவு", "Tamil (தமிழ்)"],
                        ["நான் வீட்டுக்கு செல்கிறேன்", "Tamil (தமிழ்)"],
                        ["வணக்கம் நண்பரே", "Tamil (தமிழ்)"],
                        ["नमस्ते", "Hindi (हिन्दी)"],
                        ["मैं खाना खा रहा हूं", "Hindi (हिन्दी)"],
                        ["आप कैसे हैं?", "Hindi (हिन्दी)"],
                        ["హలో", "Telugu (తెలుగు)"],
                        ["నేను భోజనం చేస్తున్నాను", "Telugu (తెలుగు)"],
                        ["మీరు ఎలా ఉన్నారు?", "Telugu (తెలుగు)"],
                    ],
                    inputs=[input_text, source_lang],
                    outputs=output_text,
                    fn=self.translate,
                    cache_examples=False
                )
            
            # Footer removed per request
            
            # Event handlers
            translate_btn.click(
                fn=self.translate,
                inputs=[input_text, source_lang],
                outputs=output_text
            )
            
            input_text.submit(
                fn=self.translate,
                inputs=[input_text, source_lang],
                outputs=output_text
            )
            
            clear_btn.click(
                fn=lambda: ("", ""),
                outputs=[input_text, output_text]
            )
        
        return app


def main():
    """Main function to launch app"""
    safe_print("\n" + "="*60)
    safe_print("🚀 Starting Indian Language Translator Web App")
    safe_print("="*60)
    safe_print("\n📱 The web interface will open in your browser")
    safe_print("🌐 If it doesn't open automatically, copy the URL shown below\n")
    
    app = TranslationApp()
    interface = app.create_interface()
    
    port = get_available_port(7860)
    if port != 7860:
        safe_print(f"ℹ️ Port 7860 in use. Switching to available port {port}.")
    
    interface.launch(
        server_name="0.0.0.0",
        server_port=port,
        share=False,
        inbrowser=True,
        show_error=True
    )


if __name__ == "__main__":
    main()
