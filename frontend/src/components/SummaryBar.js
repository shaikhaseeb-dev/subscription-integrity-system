import React, { useState } from "react";

export function MetricsRow({ summary }) {
  if (!summary) {
    // Skeleton state
    return (
      <div className="metrics-row">
        {[0, 1, 2].map((i) => (
          <div className="metric-card" key={i}>
            <div className="skel" style={{ width: 80, marginBottom: 10 }} />
            <div className="skel" style={{ width: 120, height: 28 }} />
          </div>
        ))}
      </div>
    );
  }

  const annual = (summary.total_monthly_cost * 12).toFixed(2);
  const perDay = (summary.total_monthly_cost / 30).toFixed(2);

  return (
    <div className="metrics-row">
      {/* Primary metric */}
      <div className="metric-card is-primary">
        <div className="metric-label">
          <span className="metric-icon">💳</span>
          Monthly spend
        </div>
        <div className="metric-value">
          ${summary.total_monthly_cost.toFixed(2)}
        </div>
        <div className="metric-sub">
          ${perDay}/day · ${annual}/yr
        </div>
      </div>

      {/* Secondary */}
      <div className="metric-card">
        <div className="metric-label">Active subscriptions</div>
        <div className="metric-value">{summary.subscription_count}</div>
        <div className="metric-sub">
          {summary.subscription_count === 1
            ? "service tracked"
            : "services tracked"}
        </div>
      </div>

      <div className="metric-card">
        <div className="metric-label">Annual equivalent</div>
        <div className="metric-value">${annual}</div>
        <div className="metric-sub">at current spend</div>
      </div>
    </div>
  );
}

export function BillingEnginePanel({ summary, onRunBilling }) {
  const [running, setRunning] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleRun = async () => {
    setRunning(true);
    setResult(null);
    setError(null);
    try {
      const res = await onRunBilling();
      setResult(res);
    } catch (e) {
      setError(e.message);
    } finally {
      setRunning(false);
    }
  };

  const active = summary?.subscription_count ?? 0;

  return (
    <div className="panel">
      <div className="panel-head">
        <span className="panel-head-title">Billing engine</span>
      </div>

      <div className="billing-body">
        <p className="billing-desc">
          Process all subscriptions due today or earlier. Each run creates a
          permanent billing record.
        </p>

        <div className="billing-counters">
          <div className="bc-item">
            <div className="bc-num">{active}</div>
            <div className="bc-label">Active</div>
          </div>
          {result && (
            <>
              <div className="bc-item">
                <div className="bc-num" style={{ color: "var(--green)" }}>
                  {result.processed_count}
                </div>
                <div className="bc-label">Processed</div>
              </div>
              <div className="bc-item">
                <div className="bc-num" style={{ color: "var(--gray-400)" }}>
                  {result.skipped_count}
                </div>
                <div className="bc-label">Skipped</div>
              </div>
            </>
          )}
        </div>

        {result && (
          <div className="billing-result">
            <span className="billing-result-icon">✓</span>
            <span>
              Run complete on <strong>{result.run_date}</strong>.{" "}
              {result.processed_count} subscription
              {result.processed_count !== 1 ? "s" : ""} billed.
            </span>
          </div>
        )}

        {error && (
          <div className="alert alert-error">
            <span>⚠</span> {error}
          </div>
        )}

        <button
          className="btn btn-primary btn-full"
          onClick={handleRun}
          disabled={running || active === 0}
        >
          {running ? (
            <>
              <span className="spinner" /> Running…
            </>
          ) : (
            "Run billing"
          )}
        </button>
      </div>
    </div>
  );
}
