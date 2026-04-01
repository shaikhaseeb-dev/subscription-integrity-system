import React from "react";
import { useSubscriptions } from "./hooks/useSubscriptions";
import { MetricsRow, BillingEnginePanel } from "./components/SummaryBar";
import { AddSubscriptionForm } from "./components/AddSubscriptionForm";
import { UpcomingBilling } from "./components/UpcomingBilling";
import { SubscriptionList } from "./components/SubscriptionList";
import "./App.css";

export default function App() {
  const {
    subscriptions,
    upcoming,
    summary,
    loading,
    error,
    createSubscription,
    runBilling,
  } = useSubscriptions();

  return (
    <div className="app">
      {/* ── Topbar ───────────────────────────────────── */}
      <header className="topbar">
        <div className="topbar-brand">
          <div className="topbar-icon">SI</div>
          <span className="topbar-name">SubIntegrity</span>
        </div>
        <span className="topbar-sep">/</span>
        <span className="topbar-section">Subscriptions</span>

        <div className="topbar-right">
          <span className="live-dot" />
          live
        </div>
      </header>

      {/* ── Page Content ─────────────────────────────── */}
      <main className="page">
        {/* Page title */}
        <div className="page-header">
          <h1 className="page-title">Subscription overview</h1>
          <p className="page-subtitle">
            Track recurring costs, catch upcoming charges, prevent billing
            drift.
          </p>
        </div>

        {/* Global error */}
        {error && (
          <div className="alert alert-error" style={{ marginBottom: 20 }}>
            <span>⚠</span> Could not reach the API — {error}
          </div>
        )}

        {/* 1 · Metrics */}
        <MetricsRow summary={summary} />

        {/* 2 · Actions: Add form + Billing engine */}
        <div className="action-layout">
          <AddSubscriptionForm onAdd={createSubscription} />
          <BillingEnginePanel summary={summary} onRunBilling={runBilling} />
        </div>

        {/* 3 · Upcoming billing */}
        <UpcomingBilling upcoming={upcoming} />

        {/* 4 · Full subscription table */}
        <SubscriptionList subscriptions={subscriptions} loading={loading} />
      </main>

      {/* ── Footer ───────────────────────────────────── */}
      <footer className="footer">
        <span className="footer-l">
          SubIntegrity · Subscription Integrity System
        </span>
        <span className="footer-r">v1.0.0</span>
      </footer>
    </div>
  );
}
