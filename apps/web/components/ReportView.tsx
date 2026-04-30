import type { ReportResponse } from "@/types/locationiq";

export function ReportView({
  report,
  reportToken,
}: {
  report: ReportResponse;
  reportToken?: string;
}) {
  const reportJson = report.report;
  const summary = reportJson.reader_summary as {
    headline?: string;
    summary?: string;
    what_to_verify?: Array<{ title: string; text: string }>;
  };
  const exactPin = reportJson.exact_pin as { pin_read?: string; nearest_poi_policy?: string };
  const sourceNotes = (reportJson.source_notes ?? []) as Array<{
    id: string;
    name: string;
    user_facing_note: string;
  }>;

  return (
    <section className="report-panel">
      <div className="section-heading">
        <p className="eyebrow">Interactive report</p>
        <h2>{summary.headline}</h2>
        <p>{summary.summary}</p>
      </div>
      {reportToken ? (
        <div className="report-actions">
          <a className="secondary-button" href={`/report/${reportToken}`}>
            Open secure link
          </a>
        </div>
      ) : null}
      <div className="preview-grid">
        <div className="summary-panel">
          <h3>Exact pin</h3>
          <p>{exactPin.pin_read}</p>
          <p>{exactPin.nearest_poi_policy}</p>
        </div>
        <div className="summary-panel">
          <h3>What to verify</h3>
          <ul>
            {summary.what_to_verify?.map((item) => (
              <li key={item.title}>
                <strong>{item.title}.</strong> {item.text}
              </li>
            ))}
          </ul>
        </div>
      </div>
      <div className="source-list">
        {sourceNotes.map((source) => (
          <div key={source.id}>
            <strong>{source.name}</strong>
            <p>{source.user_facing_note}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
