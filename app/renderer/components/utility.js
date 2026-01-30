export function formatDate(dateString) {
  const date = new Date(dateString);
  const day = String(date.getDate());
  const month = String(date.getMonth() + 1);
  const year = date.getFullYear();
  return `${day}.${month}.${year}`;
};

export function lineFormat(str) {
  return String(str).replace(/~/g, "");
}

export function escapeHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
}