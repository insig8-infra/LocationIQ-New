import { ReportTokenPage } from "@/components/ReportTokenPage";

export default async function Page({ params }: { params: Promise<{ token: string }> }) {
  const { token } = await params;
  return <ReportTokenPage token={token} />;
}
