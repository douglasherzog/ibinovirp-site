import { client } from "@/sanity/lib/client";

type SiteConfig = {
  nomeIgreja?: string;
  descricaoBreve?: string;
};

type SimpleDoc = { _id: string; titulo?: string; pregador?: string; data?: string };

async function getData() {
  const [site, eventos, ministerios, mensagens] = await Promise.all([
    client.fetch<SiteConfig>(`*[_type == "siteConfig"][0]`),
    client.fetch<SimpleDoc[]>(
      `*[_type == "evento"]|order(inicio asc)[0..5]{ _id, titulo, "data": coalesce(inicio, fim) }`
    ),
    client.fetch<SimpleDoc[]>(`*[_type == "ministerio"]|order(_updatedAt desc)[0..5]{ _id, titulo }`),
    client.fetch<SimpleDoc[]>(
      `*[_type == "mensagem"]|order(coalesce(data, _updatedAt) desc)[0..5]{ _id, titulo, pregador, data }`
    ),
  ]);
  return { site, eventos, ministerios, mensagens };
}

export default async function Home() {
  const { site, eventos, ministerios, mensagens } = await getData();

  return (
    <main className="mx-auto max-w-3xl p-6 space-y-8">
      <header className="space-y-2">
        <h1 className="text-2xl font-bold">
          {site?.nomeIgreja || "IBINOVIRP"}
        </h1>
        {site?.descricaoBreve && (
          <p className="text-muted-foreground">{site.descricaoBreve}</p>
        )}
      </header>

      <section>
        <h2 className="text-xl font-semibold mb-2">Próximos eventos</h2>
        {eventos?.length ? (
          <ul className="list-disc pl-5 space-y-1">
            {eventos.map((e) => (
              <li key={e._id}>{e.titulo}</li>
            ))}
          </ul>
        ) : (
          <p className="text-sm text-muted-foreground">Nenhum evento cadastrado.</p>
        )}
      </section>

      <section>
        <h2 className="text-xl font-semibold mb-2">Ministérios</h2>
        {ministerios?.length ? (
          <ul className="list-disc pl-5 space-y-1">
            {ministerios.map((m) => (
              <li key={m._id}>{m.titulo}</li>
            ))}
          </ul>
        ) : (
          <p className="text-sm text-muted-foreground">Nenhum ministério cadastrado.</p>
        )}
      </section>

      <section>
        <h2 className="text-xl font-semibold mb-2">Mensagens/Sermões</h2>
        {mensagens?.length ? (
          <ul className="list-disc pl-5 space-y-1">
            {mensagens.map((s) => (
              <li key={s._id}>
                {s.titulo}
                {s.pregador ? ` — ${s.pregador}` : ""}
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-sm text-muted-foreground">Nenhuma mensagem cadastrada.</p>
        )}
      </section>
    </main>
  );
}
