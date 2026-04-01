/**
 * Format an ISO date string as "Apr 3, 2026"
 */
export function formatDate(isoString) {
  if (!isoString) return "—";
  // Parse as UTC to avoid timezone shift on date-only strings
  const [y, m, d] = isoString.split("-").map(Number);
  const date = new Date(y, m - 1, d);
  return date.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

/**
 * Return integer days from today until a target ISO date string.
 * Negative means past.
 */
export function daysUntil(isoString) {
  const [y, m, d] = isoString.split("-").map(Number);
  const target = new Date(y, m - 1, d);
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  return Math.round((target - today) / 86_400_000);
}

/**
 * Format a number as USD currency string
 */
export function formatCurrency(amount) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 2,
  }).format(amount);
}
