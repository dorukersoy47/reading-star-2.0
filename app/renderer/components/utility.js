export function formatDate(dateString) {
  const date = new Date(dateString);
  const day = String(date.getDate());
  const month = String(date.getMonth() + 1);
  const year = date.getFullYear();
  return `${day}.${month}.${year}`;
};

const lengthMap = { short: 1, medium: 2, long: 3 };
const complexityMap = { simple: 6, medium: 8, complex: 10 };

export function lengthToStanzaCount(length) {
    return lengthMap[length]
}

export function complexityToSyllableCount(complexity) {
    return complexityMap[complexity]
}