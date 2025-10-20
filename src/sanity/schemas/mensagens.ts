import { defineField, defineType } from "sanity";

export default defineType({
  name: "mensagem",
  title: "Mensagem/Sermão",
  type: "document",
  fields: [
    defineField({ name: "titulo", title: "Título", type: "string" }),
    defineField({ name: "pregador", title: "Pregador", type: "string" }),
    defineField({ name: "data", title: "Data", type: "date" }),
    defineField({ name: "videoUrl", title: "URL do Vídeo (YouTube/Vimeo)", type: "url" }),
    defineField({ name: "audioFile", title: "Áudio (arquivo)", type: "file" }),
    defineField({ name: "audioUrl", title: "Áudio (URL externa)", type: "url" }),
    defineField({ name: "passagemBiblica", title: "Passagem Bíblica", type: "string" }),
    defineField({ name: "resumo", title: "Resumo", type: "text" }),
    defineField({ name: "capa", title: "Capa", type: "image", options: { hotspot: true } }),
  ],
});
