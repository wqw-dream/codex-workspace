const form = document.getElementById("generator-form");
const preview = document.getElementById("preview");
const printBtn = document.getElementById("print-btn");

const bgMap = {
  纯白: "bg-plain",
  米白: "bg-cream",
  网格: "bg-grid",
  横线: "bg-line",
};

const styleMap = {
  简洁: "style-clean",
  商务: "style-business",
  柔和: "style-soft",
};

function updatePreview(data) {
  preview.className = "preview";
  preview.classList.add(data.paper_size === "A5" ? "paper-a5" : "paper-a4");
  preview.classList.add(bgMap[data.background_style] || "bg-plain");
  preview.classList.add(styleMap[data.visual_style] || "style-clean");

  const textHtml = data.text?.trim()
    ? data.text
        .trim()
        .split("\n")
        .map((line) => `<p>${line}</p>`)
        .join("")
    : '<p class="empty">没有文本内容，仍可打印模板。</p>';

  const imageHtml = data.image_data
    ? `<figure><img src="data:image/png;base64,${data.image_data}" alt="上传图片" /></figure>`
    : "";

  preview.innerHTML = `
    <h3>打印文档预览</h3>
    ${textHtml}
    ${imageHtml}
  `;
}

async function generatePreview(event) {
  event.preventDefault();
  const formData = new FormData(form);

  const response = await fetch("/api/generate", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    preview.innerHTML = '<p class="empty">生成失败，请稍后重试。</p>';
    return;
  }

  const data = await response.json();
  updatePreview(data);
}

form.addEventListener("submit", generatePreview);
printBtn.addEventListener("click", () => window.print());
