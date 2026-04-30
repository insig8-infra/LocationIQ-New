"use client";

import { useEffect, useMemo, useState } from "react";
import { getReport, getReportStatus } from "@/lib/api";
import type { ReportResponse, ReportStatusResponse } from "@/types/locationiq";
import { ReportView } from "@/components/ReportView";

export function ReportTokenPage({ token }: { token: string }) {
  const [status, setStatus] = useState<ReportStatusResponse | null>(null);
  const [report, setReport] = useState<ReportResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const progress = useMemo(() => status?.progress_percent ?? 18, [status]);

  useEffect(() => {
    let cancelled = false;
    let timer: ReturnType<typeof setTimeout> | null = null;

    async function load() {
      try {
        const nextStatus = await getReportStatus(token);
        if (cancelled) return;
        setStatus(nextStatus);

        if (nextStatus.status === "completed" || nextStatus.status === "completed_with_data_gaps") {
          const nextReport = await getReport(token);
          if (!cancelled) setReport(nextReport);
          return;
        }

        if (nextStatus.status === "failed") return;
        timer = setTimeout(load, 3000);
      } catch (caught) {
        if (!cancelled) {
          setError(caught instanceof Error ? caught.message : "Report could not be opened.");
        }
      }
    }

    load();

    return () => {
      cancelled = true;
      if (timer) clearTimeout(timer);
    };
  }, [token]);

  return (
    <main className="app-shell">
      <section className="workspace">
        <header className="topbar">
          <div>
            <p className="eyebrow">LocationIQ</p>
            <h1>Location report</h1>
          </div>
          <div className="stage-meter" aria-label="Report progress">
            <span style={{ width: `${progress}%` }} />
          </div>
        </header>

        {error ? <div className="error-panel">{error}</div> : null}

        {!error && !report ? (
          <section className="action-band">
            <div>
              <p className="eyebrow">Report status</p>
              <h2>{status?.message ?? "Opening report"}</h2>
              <p>{status?.eta_note ?? "Checking the report status."}</p>
            </div>
            <div className="status-number">{progress}%</div>
          </section>
        ) : null}

        {report ? <ReportView report={report} /> : null}
      </section>
    </main>
  );
}
