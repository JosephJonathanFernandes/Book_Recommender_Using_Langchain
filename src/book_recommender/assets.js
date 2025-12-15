// Theme initialization for Gradio Blocks
export function initTheme(mode) {
  const theme = mode === "Light" ? "light" : "dark";
  document.documentElement.dataset.theme = theme;
}
