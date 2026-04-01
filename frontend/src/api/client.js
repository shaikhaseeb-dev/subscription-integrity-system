const BASE_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:5000";

async function request(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  let data;
  try {
    data = await res.json();
  } catch {
    data = {};
  }

  if (!res.ok) {
    const err = new Error(data.error || "Request failed");
    err.status = res.status;
    err.code = data.code;
    err.path = path;
    throw err;
  }

  return data;
}

export const api = {
  getSubscriptions: () => request("/subscriptions"),
  createSubscription: (body) =>
    request("/subscriptions", {
      method: "POST",
      body: JSON.stringify(body),
    }),
  getUpcoming: () => request("/subscriptions/upcoming"),
  getMonthlySummary: () => request("/summary/monthly-cost"),
  runBilling: () => request("/billing/run", { method: "POST" }),
  getBillingEvents: () => request("/billing/events"),
};
