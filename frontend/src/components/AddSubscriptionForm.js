import React, { useState } from "react";

const todayISO = new Date().toISOString().split("T")[0];

const EMPTY = {
  name: "",
  cost: "",
  billing_cycle: "monthly",
  next_billing_date: todayISO,
};

export function AddSubscriptionForm({ onAdd }) {
  const [form, setForm] = useState(EMPTY);
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);
  const [success, setSuccess] = useState(false);

  const set = (key) => (e) => {
    setForm((f) => ({ ...f, [key]: e.target.value }));
    setError(null);
    setSuccess(false);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError(null);
    setSuccess(false);

    try {
      await onAdd({ ...form, cost: parseFloat(form.cost) });
      setForm(EMPTY);
      setSuccess(true);
      setTimeout(() => setSuccess(false), 4000);
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="panel">
      <div className="panel-head">
        <span className="panel-head-title">Add subscription</span>
      </div>

      <div className="panel-body">
        <form onSubmit={handleSubmit} autoComplete="off">
          {/* Row 1: Name + Cost */}
          <div className="form-grid" style={{ marginBottom: 10 }}>
            <div className="field">
              <label className="field-label">Service name</label>
              <input
                className="field-input"
                value={form.name}
                onChange={set("name")}
                placeholder="e.g. GitHub, Figma…"
                required
                autoFocus
              />
            </div>
            <div className="field">
              <label className="field-label">Cost (USD)</label>
              <input
                className="field-input"
                type="number"
                step="0.01"
                min="0.01"
                value={form.cost}
                onChange={set("cost")}
                placeholder="0.00"
                required
              />
            </div>
          </div>

          {/* Row 2: Cycle + Date */}
          <div className="form-grid" style={{ marginBottom: 14 }}>
            <div className="field">
              <label className="field-label">Billing cycle</label>
              <select
                className="field-select"
                value={form.billing_cycle}
                onChange={set("billing_cycle")}
              >
                <option value="monthly">Monthly</option>
                <option value="yearly">Yearly</option>
              </select>
            </div>
            <div className="field">
              <label className="field-label">Next billing date</label>
              <input
                className="field-input"
                type="date"
                min={todayISO}
                value={form.next_billing_date}
                onChange={set("next_billing_date")}
                required
              />
            </div>
          </div>

          {/* Feedback */}
          {error && (
            <div className="alert alert-error" style={{ marginBottom: 12 }}>
              <span>⚠</span> {error}
            </div>
          )}
          {success && (
            <div className="alert alert-success" style={{ marginBottom: 12 }}>
              <span>✓</span> Subscription added successfully.
            </div>
          )}

          <button
            type="submit"
            className="btn btn-primary btn-full"
            disabled={saving}
          >
            {saving ? (
              <>
                <span className="spinner" /> Saving…
              </>
            ) : (
              "Add subscription"
            )}
          </button>
        </form>
      </div>
    </div>
  );
}
