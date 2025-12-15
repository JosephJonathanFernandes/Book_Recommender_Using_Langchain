"""Gradio UI assembly for the book recommender."""

import gradio as gr

from .config import APP_SUBTITLE, APP_TITLE, CSS
from .recommender import BookRecommender


def _render_cards(books: list[dict]) -> str:
    if not books:
        return "<div style='color: var(--muted); font-style: italic; padding: 20px; text-align: center;'>No books found for this query.</div>"
    parts = []
    for book in books:
        thumb = book.get("thumbnail", "")
        link = book.get("link", "") or "#"
        title = book.get("title", "Unknown title")
        authors = book.get("authors", "Unknown author")
        desc = (book.get("description", "") or "")[:180]
        parts.append(
            "<div class='card'>"
            f"<a href='{link}' target='_blank' rel='noopener noreferrer'>"
            + (f"<img src='{thumb}' alt='cover' />" if thumb else "<div style='height:200px;background:var(--border);'></div>")
            + "<div>"
            + f"<h4>{title}</h4>"
            f"<p style='font-weight:600;'>{authors}</p>"
            + (f"<p>{desc}...</p>" if desc else "")
            + "</div>"
            + "</a></div>"
        )
    return "<div class='cards'>" + "".join(parts) + "</div>"


def build_interface(recommender: BookRecommender) -> tuple[gr.Blocks, str]:
    def on_recommend(user_interest, genre, exclude, model, temperature, force_refresh, history):
        # Input validation
        if not user_interest or len(user_interest.strip()) < 3:
            return "⚠️ Please enter at least 3 characters to describe your interests.", "", "", history, gr.Dropdown(choices=[item["label"] for item in (history or [])])
        
        rec, hints, books = recommender.recommend(
            user_interest, genre, exclude, model, temperature, force_refresh=force_refresh
        )
        cards_html = _render_cards(books)

        new_entry = {
            "label": (user_interest or "(empty)")[:60],
            "interest": user_interest,
            "genre": genre,
            "exclude": exclude,
            "model": model,
            "temperature": temperature,
            "rec": rec,
            "hints": hints,
            "cards": cards_html,
        }
        history = (history or [])[-7:] + [new_entry]
        labels = [item["label"] for item in history]
        return rec, hints, cards_html, history, gr.Dropdown(choices=labels, value=labels[-1] if labels else None)

    def on_load_session(selection, history):
        if not history:
            return None, None, None, None, None, None, None, None
        if selection is None:
            return None, None, None, None, None, None, None, None
        # find by label
        entry = next((h for h in history if h["label"] == selection), None)
        if not entry:
            return None, None, None, None, None, None, None, None
        return (
            entry["interest"],
            entry["genre"],
            entry["exclude"],
            entry["model"],
            entry["temperature"],
            entry["rec"],
            entry["hints"],
            entry["cards"],
        )

    with gr.Blocks() as demo:
        history_state = gr.State([])
        gr.Markdown("<div class='pill'>📚 AI-Powered</div>", elem_id="pill-top")
        gr.Markdown(
            f"<div class='headline'>{APP_TITLE}</div>"
            f"<div class='subhead'>{APP_SUBTITLE}</div>"
        )

        with gr.Row():
            with gr.Column(scale=1, elem_classes=["panel"]):
                theme_toggle = gr.Radio(
                    ["Dark", "Light"],
                    label="Theme",
                    value="Dark",
                    elem_id="theme-toggle",
                )
                gr.Markdown(
                    "<div class='label'>Quick guide</div>\n"
                    "<ul>\n"
                    "  <li>Describe vibe, pace, themes, or comps.</li>\n"
                    "  <li>Pick a genre or exclude some.</li>\n"
                    "  <li>Press <kbd>Enter</kbd> or click ✨ to submit.</li>\n"
                    "  <li>Use 🔄 to bypass cache for fresh results.</li>\n"
                    "  <li>Spoiler-averse, NSFW-filtered, cached.</li>\n"
                    "</ul>"
                )

            with gr.Column(scale=2, elem_classes=["panel"]):
                user_input = gr.Textbox(
                    label="Your interests (min 3 chars)",
                    placeholder="e.g., hopeful solarpunk with found family and science-forward detail",
                    lines=4,
                    info="💡 Tip: Press Enter to submit!",
                )
                genre_dropdown = gr.Dropdown(
                    label="Preferred genre (optional)",
                    choices=["", "Fantasy", "Science Fiction", "Mystery", "Romance", "Thriller", "Nonfiction", "Historical"],
                    value="",
                )
                exclude_genres = gr.Textbox(
                    label="Exclude genres (comma separated)",
                    placeholder="e.g., grimdark, horror",
                )
                with gr.Accordion("⚙️ Advanced Options", open=False):
                    with gr.Row():
                        model_dropdown = gr.Dropdown(
                            label="Groq model",
                            choices=recommender.supported_models(),
                            value=recommender.default_model,
                            scale=2,
                            info="Choose AI model (larger = smarter but slower)",
                        )
                        temperature_slider = gr.Slider(
                            minimum=0.0,
                            maximum=1.0,
                            value=recommender.default_temperature,
                            step=0.05,
                            label="Temperature",
                            scale=1,
                            info="Lower = focused, Higher = creative",
                        )

                status_msg = gr.Markdown(value="", elem_classes=["status-msg"])
                
                with gr.Row(elem_classes=["toolbar"]):
                    btn = gr.Button("✨ Get Recommendations", elem_classes=["btn-primary"], scale=2)
                    btn_refresh = gr.Button("🔄 New Spin", elem_classes=["ghost-btn"], scale=1)
                    btn_copy = gr.Button("📋 Copy List", elem_classes=["ghost-btn"], scale=1)
                
                with gr.Row(elem_classes=["toolbar"]):
                    btn_export_json = gr.Button("💾 Export JSON", elem_classes=["ghost-btn"], scale=1)
                    btn_export_pdf = gr.Button("📄 Export PDF", elem_classes=["ghost-btn"], scale=1)
                    btn_save_list = gr.Button("⭐ Save to Reading List", elem_classes=["ghost-btn"], scale=1)
                
                with gr.Row(elem_classes=["toolbar"]):
                    btn_share_twitter = gr.Button("🐦 Share", elem_classes=["ghost-btn"], scale=1)
                    btn_share_facebook = gr.Button("📘 Share", elem_classes=["ghost-btn"], scale=1)
                    btn_share_linkedin = gr.Button("💼 Share", elem_classes=["ghost-btn"], scale=1)

                output = gr.Markdown(label="Recommendations", value="")
                
                with gr.Row():
                    with gr.Column(scale=1):
                        rating_slider = gr.Slider(
                            minimum=1,
                            maximum=5,
                            value=5,
                            step=1,
                            label="⭐ Rate these recommendations",
                            info="Your feedback helps improve results",
                        )
                        btn_submit_rating = gr.Button("Submit Rating", elem_classes=["ghost-btn"])
                        rating_feedback = gr.Markdown(value="", elem_classes=["status-msg"])
                    with gr.Column(scale=1):
                        gr.Markdown("### 📚 Your Reading List")
                        reading_list_display = gr.HTML(value="<div id='reading-list-container'></div>")
                
                external_view = gr.Markdown(label="Google Books hints", value="", elem_classes=["label"])
                cards = gr.HTML(label="Books", value="")

                session_selector = gr.Dropdown(label="Saved sessions", choices=[], value=None)
                btn_load = gr.Button("Load session", elem_classes=["ghost-btn"])

                # Submit on Enter key
                user_input.submit(
                    fn=on_recommend,
                    inputs=[user_input, genre_dropdown, exclude_genres, model_dropdown, temperature_slider, gr.State(False), history_state],
                    outputs=[output, external_view, cards, history_state, session_selector],
                    queue=True,
                )
                
                btn.click(
                    fn=on_recommend,
                    inputs=[user_input, genre_dropdown, exclude_genres, model_dropdown, temperature_slider, gr.State(False), history_state],
                    outputs=[output, external_view, cards, history_state, session_selector],
                    queue=True,
                )
                btn_refresh.click(
                    fn=on_recommend,
                    inputs=[user_input, genre_dropdown, exclude_genres, model_dropdown, temperature_slider, gr.State(True), history_state],
                    outputs=[output, external_view, cards, history_state, session_selector],
                    queue=True,
                )

                btn_copy.click(
                    fn=None,
                    inputs=[output],
                    outputs=None,
                    js="""(text) => {
                        navigator.clipboard.writeText(text).then(() => {
                            const btn = event.target.closest('button');
                            const original = btn.textContent;
                            btn.textContent = '✅ Copied!';
                            btn.style.background = 'var(--success)';
                            setTimeout(() => {
                                btn.textContent = original;
                                btn.style.background = '';
                            }, 2000);
                        });
                    }""",
                )
                
                # Export JSON
                btn_export_json.click(
                    fn=None,
                    inputs=[output, user_input],
                    outputs=None,
                    js="""(recs, query) => {
                        const data = {
                            query: query,
                            recommendations: recs,
                            timestamp: new Date().toISOString()
                        };
                        const blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
                        const url = URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = `book-recommendations-${Date.now()}.json`;
                        a.click();
                        URL.revokeObjectURL(url);
                    }""",
                )
                
                # Export PDF (as formatted text)
                btn_export_pdf.click(
                    fn=None,
                    inputs=[output, user_input],
                    outputs=None,
                    js="""(recs, query) => {
                        const content = `BOOK RECOMMENDATIONS\n\nQuery: ${query}\n\nGenerated: ${new Date().toLocaleString()}\n\n${recs}`;
                        const blob = new Blob([content], {type: 'text/plain'});
                        const url = URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = `book-recommendations-${Date.now()}.txt`;
                        a.click();
                        URL.revokeObjectURL(url);
                    }""",
                )
                
                # Save to Reading List
                btn_save_list.click(
                    fn=None,
                    inputs=[output, user_input],
                    outputs=None,
                    js="""(recs, query) => {
                        const item = {
                            query: query,
                            recommendations: recs,
                            timestamp: new Date().toISOString(),
                            id: Date.now()
                        };
                        let readingList = JSON.parse(localStorage.getItem('readingList') || '[]');
                        readingList.unshift(item);
                        readingList = readingList.slice(0, 20); // Keep last 20
                        localStorage.setItem('readingList', JSON.stringify(readingList));
                        
                        // Update display
                        const container = document.getElementById('reading-list-container');
                        if (container) {
                            container.innerHTML = readingList.map(item => 
                                `<div class='reading-list-item'>
                                    <strong>${item.query.substring(0, 50)}...</strong>
                                    <br/><small>${new Date(item.timestamp).toLocaleDateString()}</small>
                                </div>`
                            ).join('');
                        }
                        
                        const btn = event.target.closest('button');
                        const original = btn.textContent;
                        btn.textContent = '✅ Saved!';
                        setTimeout(() => { btn.textContent = original; }, 2000);
                    }""",
                )
                
                # Social sharing
                btn_share_twitter.click(
                    fn=None,
                    inputs=[output, user_input],
                    outputs=None,
                    js="""(recs, query) => {
                        const text = `Just got amazing book recommendations for: ${query}`;
                        const url = `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}`;
                        window.open(url, '_blank');
                    }""",
                )
                
                btn_share_facebook.click(
                    fn=None,
                    inputs=[user_input],
                    outputs=None,
                    js="""(query) => {
                        const url = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(window.location.href)}&quote=${encodeURIComponent('Check out these book recommendations!')}`;
                        window.open(url, '_blank');
                    }""",
                )
                
                btn_share_linkedin.click(
                    fn=None,
                    inputs=[user_input],
                    outputs=None,
                    js="""(query) => {
                        const url = `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(window.location.href)}`;
                        window.open(url, '_blank');
                    }""",
                )
                
                # Rating submission
                btn_submit_rating.click(
                    fn=None,
                    inputs=[rating_slider, user_input],
                    outputs=None,
                    js="""(rating, query) => {
                        const ratingData = {
                            rating: rating,
                            query: query,
                            timestamp: new Date().toISOString()
                        };
                        let ratings = JSON.parse(localStorage.getItem('ratings') || '[]');
                        ratings.push(ratingData);
                        localStorage.setItem('ratings', JSON.stringify(ratings));
                        
                        // Show feedback
                        const feedbackEl = document.querySelector('[data-testid="rating_feedback"] .prose');
                        if (feedbackEl) {
                            feedbackEl.innerHTML = `✅ Thanks! Rated ${rating}/5 stars`;
                            setTimeout(() => { feedbackEl.innerHTML = ''; }, 3000);
                        }
                        return rating;
                    }""",
                )

                btn_load.click(
                    fn=on_load_session,
                    inputs=[session_selector, history_state],
                    outputs=[user_input, genre_dropdown, exclude_genres, model_dropdown, temperature_slider, output, external_view, cards],
                )

        # Theme toggle via JS
        theme_toggle.change(
            fn=None,
            inputs=theme_toggle,
            outputs=None,
            js="(mode) => { document.documentElement.dataset.theme = mode === 'Light' ? 'light' : 'dark'; }",
        )

        gr.HTML("""
<script>
  // Theme initialization
  const radio = document.getElementById('theme-toggle');
  if (radio) {
    const checked = radio.querySelector('input:checked');
    const mode = checked ? checked.value : 'Dark';
    document.documentElement.dataset.theme = mode === 'Light' ? 'light' : 'dark';
  }
  
  // Load reading list from localStorage
  setTimeout(() => {
    const readingList = JSON.parse(localStorage.getItem('readingList') || '[]');
    const container = document.getElementById('reading-list-container');
    if (container && readingList.length > 0) {
      container.innerHTML = readingList.map(item => 
        `<div class='reading-list-item'>
          <strong>${item.query.substring(0, 50)}...</strong>
          <br/><small>${new Date(item.timestamp).toLocaleDateString()}</small>
        </div>`
      ).join('');
    } else if (container) {
      container.innerHTML = '<p style="color: var(--muted); font-style: italic;">No saved items yet</p>';
    }
  }, 500);
</script>
""")

    return demo, CSS
