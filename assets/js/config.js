/*
 * Configuração de contato do site Ankor.
 * Preencha pelo menos UMA das opções abaixo para que o formulário envie os leads.
 * Ordem de prioridade no envio: formEndpoint → whatsapp → email.
 */
window.ANKOR_CONFIG = {
  // URL que recebe POST do formulário (ex.: Formspree, RD Station, webhook do CRM, endpoint do WordPress).
  formEndpoint: '',

  // Número do WhatsApp comercial com DDI e DDD, só dígitos. Ex.: '5512999999999'.
  // Quando preenchido, também exibe o botão de WhatsApp na barra fixa do celular.
  whatsapp: '',

  // E-mail comercial (usado como última alternativa, abre o app de e-mail do visitante).
  email: '',

  // Book do empreendimento (link atual do site).
  bookUrl: 'https://drive.google.com/drive/folders/1gLlD9-CLkf38UBASY8s03THVTHAlYLuv?usp=sharing'
};
