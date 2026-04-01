import React from "react";
import { formatDate, daysUntil } from "../utils/format";

function urgencyClass(days) {
  if (days < 0) return "uc-overdue";
  if (days === 0) return "uc-today";
  if (days <= 3) return "uc-soon";
  return "uc-ok";
}

function UrgencyBadge({ days }) {
  if (days < 0)
    return (
      <span className="badge badge-red">
        <span className="badge-dot" />
        {Math.abs(days)}d overdue
      </span>
    );
  if (days === 0)
    return (
      <span className="badge badge-amber">
        <span className="badge-dot" />
        Due today
      </span>
    );
  if (days <= 3)
    return (
      <span className="badge badge-blue">
        <span className="badge-dot" />
        In {days}d
      </span>
    );
  return (
    <span className="badge badge-gray">
      <span className="badge-dot" />
      In {days}d
    </span>
  );
}

export function UpcomingBilling({ upcoming }) {
  return (
    <div className="upcoming-wrap">
      <div className="section-row">
        <span className="section-title">Upcoming billing</span>
        <span className="section-meta">
          next 7 days · {upcoming.length} due
        </span>
      </div>

      {upcoming.length === 0 ? (
        <div className="upcoming-empty">
          <span>✓</span>
          Nothing due in the next 7 days.
        </div>
      ) : (
        <div className="upcoming-cards">
          {upcoming.map((s) => {
            const days = daysUntil(s.next_billing_date);
            return (
              <div key={s.id} className={`uc ${urgencyClass(days)}`}>
                <div>
                  <div className="uc-name">{s.name}</div>
                  <div className="uc-date">
                    {formatDate(s.next_billing_date)}
                  </div>
                </div>
                <div className="uc-right">
                  <div className="uc-amount">${s.cost.toFixed(2)}</div>
                  <div style={{ marginTop: 4 }}>
                    <UrgencyBadge days={days} />
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
