import { defineField, defineType } from "sanity";

export default defineType({
  name: "ministerio",
  title: "Ministério",
  type: "document",
  fields: [
    defineField({ name: "titulo", title: "Título", type: "string" }),
    defineField({ name: "descricao", title: "Descrição", type: "text" }),
    defineField({ name: "imagem", title: "Imagem", type: "image", options: { hotspot: true } }),
    defineField({ name: "lideres", title: "Líderes", type: "array", of: [{ type: "string" }] }),
    defineField({ name: "contatos", title: "Contatos", type: "array", of: [{ type: "string" }] }),
  ],
});
