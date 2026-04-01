import React from "react";
import { formatDate, daysUntil } from "../utils/format";

function StatusBadge({ sub }) {
  const days = daysUntil(sub.next_billing_date);

  if (sub.status !== "active") {
    return (
      <span className="badge badge-gray">
        <span className="badge-dot" />
        Cancelled
      </span>
    );
  }
  if (days < 0)
    return (
      <span className="badge badge-red">
        <span className="badge-dot" />
        Overdue
      </span>
    );
  if (days === 0)
    return (
      <span className="badge badge-amber">
        <span className="badge-dot" />
        Due today
      </span>
    );
  if (days <= 7)
    return (
      <span className="badge badge-blue">
        <span className="badge-dot" />
        Due soon
      </span>
    );
  return (
    <span className="badge badge-green">
      <span className="badge-dot" />
      Active
    </span>
  );
}

export function SubscriptionList({ subscriptions, loading }) {
  return (
    <div className="table-section">
      <div className="table-section-header">
        <span className="table-section-title">All subscriptions</span>
        <span className="table-section-meta">
          {subscriptions.length}{" "}
          {subscriptions.length === 1 ? "record" : "records"}
        </span>
      </div>

      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Service</th>
              <th>Cycle</th>
              <th>Next billing</th>
              <th>Status</th>
              <th>Cost</th>
            </tr>
          </thead>
          <tbody>
            {loading && subscriptions.length === 0 ? (
              // Skeleton rows
              [1, 2, 3].map((i) => (
                <tr key={i}>
                  {[180, 70, 100, 80, 60].map((w, j) => (
                    <td key={j}>
                      <div className="skel" style={{ width: w }} />
                    </td>
                  ))}
                </tr>
              ))
            ) : subscriptions.length === 0 ? (
              <tr>
                <td colSpan={5}>
                  <div className="table-empty">
                    <div className="table-empty-icon">📭</div>
                    <div className="table-empty-title">
                      No subscriptions yet
                    </div>
                    <div className="table-empty-sub">
                      Add your first subscription using the form above.
                    </div>
                  </div>
                </td>
              </tr>
            ) : (
              subscriptions.map((s) => (
                <tr key={s.id}>
                  <td>
                    <div className="td-name-primary">{s.name}</div>
                    <div className="td-name-sub">
                      ID #{s.id} · added {formatDate(s.created_at)}
                    </div>
                  </td>
                  <td>
                    <span className={`tag tag-${s.billing_cycle}`}>
                      {s.billing_cycle}
                    </span>
                  </td>
                  <td style={{ color: "var(--gray-700)" }}>
                    {formatDate(s.next_billing_date)}
                  </td>
                  <td>
                    <StatusBadge sub={s} />
                  </td>
                  <td>
                    <span className="td-cost">${s.cost.toFixed(2)}</span>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
