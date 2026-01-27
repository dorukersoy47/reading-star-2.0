export function formatDate(dateString) {
  const date = new Date(dateString);
  const day = String(date.getDate());
  const month = String(date.getMonth() + 1);
  const year = date.getFullYear();
  return `${day}.${month}.${year}`;
};