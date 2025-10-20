"use client";
import { NextStudio } from "next-sanity/studio";
import config from "@/sanity.config";

export default function AdminStudioPage() {
  if (!config.projectId) {
    return (
      <div style={{ padding: 24 }}>
        <h1 style={{ fontSize: 20, fontWeight: 600 }}>Sanity Studio não configurado</h1>
        <p style={{ marginTop: 12 }}>
          Defina as variáveis <code>NEXT_PUBLIC_SANITY_PROJECT_ID</code> e
          <code> NEXT_PUBLIC_SANITY_DATASET</code> no arquivo <code>.env.local</code> na raiz do projeto
          e recarregue a página.
        </p>
        <pre style={{ marginTop: 12, background: "#111", color: "#eee", padding: 12 }}>
{`NEXT_PUBLIC_SANITY_PROJECT_ID=xxxx
NEXT_PUBLIC_SANITY_DATASET=production`}
        </pre>
      </div>
    );
  }
  return <NextStudio config={config} />;
}
