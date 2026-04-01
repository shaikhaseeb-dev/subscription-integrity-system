import { useState, useEffect, useCallback } from "react";
import { api } from "../api/client";

export function useSubscriptions() {
  const [subscriptions, setSubscriptions] = useState([]);
  const [upcoming, setUpcoming] = useState([]);
  const [summary, setSummary] = useState(null);
  const [billingEvents, setBillingEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchAll = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [subs, up, sum, events] = await Promise.all([
        api.getSubscriptions(),
        api.getUpcoming(),
        api.getMonthlySummary(),
        api.getBillingEvents(),
      ]);
      setSubscriptions(subs);
      setUpcoming(up);
      setSummary(sum);
      setBillingEvents(events);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchAll();
  }, [fetchAll]);

  const createSubscription = async (formData) => {
    const sub = await api.createSubscription(formData);
    await fetchAll();
    return sub;
  };

  const runBilling = async () => {
    const result = await api.runBilling();
    await fetchAll();
    return result;
  };

  return {
    subscriptions,
    upcoming,
    summary,
    billingEvents,
    loading,
    error,
    createSubscription,
    runBilling,
    refresh: fetchAll,
  };
}
