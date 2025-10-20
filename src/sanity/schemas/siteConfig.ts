import { defineField, defineType } from "sanity";

export default defineType({
  name: "siteConfig",
  title: "Configurações do Site",
  type: "document",
  fields: [
    defineField({ name: "nomeIgreja", title: "Nome da Igreja", type: "string" }),
    defineField({ name: "descricaoBreve", title: "Descrição breve", type: "text" }),
    defineField({ name: "logo", title: "Logo", type: "image", options: { hotspot: true } }),
    defineField({
      name: "cores",
      title: "Cores",
      type: "object",
      fields: [
        { name: "primaria", title: "Primária", type: "string", description: "Ex.: #0ea5e9" },
        { name: "secundaria", title: "Secundária", type: "string" },
      ],
    }),
    defineField({
      name: "contatos",
      title: "Contatos e Redes",
      type: "object",
      fields: [
        { name: "telefoneWhatsApp1", title: "WhatsApp 1", type: "string" },
        { name: "telefoneWhatsApp2", title: "WhatsApp 2", type: "string" },
        { name: "email", title: "E-mail", type: "string" },
        { name: "facebook", title: "Facebook", type: "url" },
        { name: "instagram", title: "Instagram", type: "url" },
      ],
    }),
    defineField({ name: "endereco", title: "Endereço", type: "string" }),
    defineField({
      name: "horariosCulto",
      title: "Horários de Culto",
      type: "array",
      of: [{ type: "string" }],
    }),
    defineField({
      name: "doacoes",
      title: "Doações",
      type: "object",
      fields: [
        { name: "pixChave", title: "PIX (chave)", type: "string" },
        { name: "pixQr", title: "PIX (QR)", type: "image" },
        { name: "banco", title: "Banco", type: "string" },
        { name: "agencia", title: "Agência", type: "string" },
        { name: "conta", title: "Conta", type: "string" },
        { name: "titular", title: "Titular", type: "string" },
      ],
    }),
  ],
});
