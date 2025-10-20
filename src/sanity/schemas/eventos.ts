import { defineField, defineType } from "sanity";

export default defineType({
  name: "evento",
  title: "Evento",
  type: "document",
  fields: [
    defineField({ name: "titulo", title: "Título", type: "string" }),
    defineField({ name: "descricao", title: "Descrição", type: "text" }),
    defineField({ name: "local", title: "Local", type: "string" }),
    defineField({ name: "inicio", title: "Início", type: "datetime" }),
    defineField({ name: "fim", title: "Fim", type: "datetime" }),
    defineField({ name: "banner", title: "Banner", type: "image", options: { hotspot: true } }),
    defineField({
      name: "recorrencia",
      title: "Recorrência",
      type: "object",
      fields: [
        { name: "tipo", title: "Tipo", type: "string", options: { list: [
          { title: "Nenhuma", value: "none" },
          { title: "Semanal", value: "weekly" },
          { title: "Mensal", value: "monthly" },
        ] } },
        { name: "intervalo", title: "Intervalo", type: "number", description: "Ex.: a cada 1 semana" },
        { name: "diasDaSemana", title: "Dias da semana", type: "array", of: [{ type: "string" }], options: { list: [
          { title: "Domingo", value: "sun" },
          { title: "Segunda", value: "mon" },
          { title: "Terça", value: "tue" },
          { title: "Quarta", value: "wed" },
          { title: "Quinta", value: "thu" },
          { title: "Sexta", value: "fri" },
          { title: "Sábado", value: "sat" },
        ], layout: "tags" } },
        { name: "terminoRecorrencia", title: "Término da recorrência", type: "datetime" },
      ],
    }),
  ],
});
