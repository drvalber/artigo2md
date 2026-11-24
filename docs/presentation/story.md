---
title: artigo2md
subtitle: Seus PDFs viram texto limpo, sem sair do seu computador
project: artigo2md
lang: pt-BR
generated: 2026-11-21
vocabulary: PDF, Markdown
---

<!-- slide: cover -->
# artigo2md
## Seus PDFs viram texto limpo, sem sair do seu computador
Artigos científicos, livros e diretrizes convertidos em texto estruturado, na máquina de quem usa e sem custo por página.
> Nada é enviado para a internet.
@source docs/briefing.md

<!-- slide: manifesto -->
## Por que este projeto existe
Quem converte artigos científicos conhece o problema: a conversão termina, mas a tabela que o texto cita não está lá. Um único conversor não acerta todo tipo de documento.

O artigo2md parte de uma convicção simples: cada PDF merece ser **examinado antes, encaminhado ao conversor mais adequado e conferido depois**. Se o resultado ficou ruim, o próximo conversor é tentado e o melhor resultado é o que fica.
> Nada é enviado para a internet e não há custo por página.
@source docs/briefing.md

<!-- slide: briefing -->
## O ponto de partida
### Visão
Um conversor de PDFs (artigos científicos, livros, diretrizes e capítulos) para Markdown, um formato de texto simples e estruturado, que roda no computador de quem usa.
### Usuários
Pesquisadores e estudantes, profissionais de saúde e desenvolvedores: gente que precisa ler, anotar, consultar ou preparar muitos documentos.
### Escopo
- Exame do documento antes da conversão
- Escolha automática do conversor, com nota de qualidade e nova tentativa
- Uso pelo navegador ou por comandos, sempre na própria máquina
### Restrições
Processamento sempre local, componentes obrigatórios de licença aberta e permissiva, projeto comunitário sem prazo fixo e sem orçamento.
### Prioridades
Qualidade e robustez em primeiro lugar.
@source docs/briefing.md

<!-- slide: constitution -->
## No que acreditamos
### I. Processamento 100% Local
Nenhum documento de quem usa é enviado a serviços externos.
### II. Dependências Obrigatórias com Licença Permissiva
O projeto segue livre para qualquer uso: nada obrigatório carrega licença restritiva.
### III. Mensagens ao Usuário em Português
Quem usa é atendido na própria língua.
### IV. Testes Antes do Commit
O commit é o registro oficial de uma mudança no projeto: nenhuma é registrada sem que a verificação automática passe.
### V. Veracidade de Dados, Zero Fabricação (NON-NEGOTIABLE)
Nenhum documento do projeto contém dado inventado. Sem fonte rastreável, o trabalho para e uma pessoa decide.
@metric Princípios | principles
@metric Versão | constitution-version
@source docs/constitution.md

<!-- slide: chapter -->
## Do retrato à entrega
O produto já existia e funcionava. Cada peça foi documentada a partir do que ele realmente faz, passou por perguntas e decisões e, onde havia lacuna, ganhou um plano. Esses planos foram executados e conferidos contra o combinado, inclusive um item de privacidade que a própria conferência revelou.

<!-- slide: spec key=command-line-interface -->
## Converter pastas inteiras com um comando
Quem tem muitos documentos não precisa abrir um por um: aponta a pasta e recebe tudo convertido.
### O que é
Um comando único para converter arquivos ou pastas inteiras, abrir a página de uso no navegador e conferir se a instalação está saudável. Documentos já convertidos são pulados, o que permite repetir a operação sem retrabalho.
### Como foi pensada
O ponto frágil estava nos documentos de mesmo nome guardados em pastas diferentes: um deles ficava de fora. A escolha foi fazer a saída repetir a organização de pastas da entrada, um resultado que se mantém estável a cada nova execução.
### Como foi enriquecida
As perguntas definiram a prioridade, confirmaram que pular um documento já convertido não é erro e fecharam cuidados novos: avisar quando a página de uso fica visível para outras máquinas e recusar, com orientação, pedidos em que documentos diferentes disputariam o mesmo arquivo de saída.
### Como foi implementada
Entregue e conferida contra o combinado: a saída repete a organização de pastas da entrada, os avisos novos estão em uso e cada comportamento do comando tem a sua verificação automática.
@metric Tarefas entregues | tasks
@metric Dúvidas esclarecidas | clarify-questions
@metric Revisão final | converge
@tag Linha de comando
@source docs/specs/command-line-interface/spec.md
@source docs/specs/command-line-interface/research.md

<!-- slide: spec key=conversion-engines -->
## Vários conversores, um só compromisso
Cada conversor tem um talento, e todos trabalham sob a mesma regra: o documento não sai da máquina.
### O que é
O produto reúne conversores com talentos diferentes: um principal para páginas em colunas, tabelas e páginas digitalizadas, um leve para texto corrido e opcionais para rapidez e para fórmulas. Ele sabe quais estão instalados e mostra a ficha de cada um.
### Como foi pensada
A garantia de privacidade estava declarada para apenas um dos conversores. A decisão foi estendê-la a todos: recursos remotos desligados de forma explícita e coleta de dados de uso desativada sempre que o conversor oferece essa opção.
### Como foi enriquecida
As perguntas transformaram a privacidade em exigência para todos os conversores e mantiveram a política de aceitar, do conversor opcional de fórmulas, apenas a geração que trabalha localmente. Baixar os modelos na primeira conversão continua permitido: isso traz dados para a máquina, não envia o documento. Uma verificação em execução real mostrou, porém, que o conversor principal consultava a central de modelos mesmo com tudo já baixado, e evitar esse contato virou requisito.
### Como foi implementada
Entregue e conferida contra o combinado: os recursos remotos do conversor principal ficam desligados de forma declarada, a coleta de dados de uso é desativada e, com os modelos já baixados, a conversão acontece sem nenhum contato com a central de modelos. A rede só é usada na primeira conversão, para baixá-los. Cada conversor tem a sua verificação automática.
@metric Tarefas entregues | tasks
@metric Dúvidas esclarecidas | clarify-questions
@metric Revisão final | converge
@tag Docling
@tag MarkItDown
@tag MinerU
@source docs/specs/conversion-engines/spec.md
@source docs/specs/conversion-engines/research.md

<!-- slide: spec key=engine-routing -->
## O conversor certo para cada documento
O produto escolhe o melhor caminho para cada PDF e não se contenta com um resultado ruim.
### O que é
Depois de examinar o documento, o produto monta a ordem de conversores a tentar, dá uma nota de qualidade ao resultado e, se a nota não basta ou algo falha, tenta o próximo. Fica o melhor resultado.
### Como foi pensada
A nota cai quando o documento cita tabelas e nenhuma aparece no resultado, quando o texto sai curto demais ou quando boa parte do conteúdo original se perde. É a resposta direta ao problema que deu origem ao projeto.
### Como foi enriquecida
As perguntas ratificaram os critérios da nota como a definição de conversão aceitável e fixaram o que acontece quando alguém pede um conversor que não está instalado: o produto explica como instalar, sem trocar a escolha da pessoa. Uma verificação prática mostrou que essa orientação só aparecia para um dos conversores, e a lacuna foi fechada. Ficou decidido também não impor limite de tempo além do que já existe.
### Como foi implementada
Entregue e conferida contra o combinado: quem pede um conversor ausente recebe, em português, a orientação de instalação de qualquer conversor, e cada regra de escolha e de nota tem a sua verificação automática.
@metric Tarefas entregues | tasks
@metric Dúvidas esclarecidas | clarify-questions
@metric Revisão final | converge
@source docs/specs/engine-routing/spec.md
@source docs/specs/engine-routing/research.md

<!-- slide: spec key=pdf-inspection -->
## Entender o documento antes de converter
Antes de qualquer conversão, o produto lê o documento e descobre do que ele precisa.
### O que é
Um exame rápido que identifica páginas com texto, páginas digitalizadas que exigem reconhecimento de caracteres, citações de tabelas e sinais de fórmulas. Esse retrato orienta a escolha do conversor.
### Como foi pensada
Arquivos danificados ou protegidos por senha produziam um aviso técnico em inglês. A decisão foi interromper cedo, com uma mensagem clara em português, antes de acionar conversores pesados. O comportamento foi observado em execução real antes da escolha.
### Como foi enriquecida
As perguntas transformaram lacunas em garantias: a falha clara para arquivo inválido ou protegido e a exigência de que o exame aconteça sem acesso à rede. Também registraram que não há meta de tempo para o exame e que decidir por palavras do texto é um risco aceito, já que um resultado fraco aciona nova tentativa.
### Como foi implementada
Entregue e conferida contra o combinado: arquivos danificados ou protegidos por senha recebem uma mensagem clara em português antes de qualquer conversor ser acionado, e cada comportamento do exame tem a sua verificação automática.
@metric Tarefas entregues | tasks
@metric Dúvidas esclarecidas | clarify-questions
@metric Revisão final | converge
@source docs/specs/pdf-inspection/spec.md
@source docs/specs/pdf-inspection/research.md

<!-- slide: spec key=web-interface -->
## Arrastar, acompanhar e baixar
Converter documentos fica tão simples quanto usar uma página no navegador, sem que nada saia do computador.
### O que é
Uma página local onde a pessoa envia um ou mais PDFs, acompanha a fila de conversão, lê o resultado e baixa um arquivo ou todos de uma vez. O que não interessa mais pode ser apagado.
### Como foi pensada
As conversões acontecem uma por vez, porque os conversores são pesados, e o conversor fica num processo à parte que se encerra quando está ocioso, devolvendo a memória ao computador. Cada pedido guarda o documento original, o andamento e o resultado, e um pedido interrompido por reinício fica sinalizado em vez de sumir.
### Como foi enriquecida
As perguntas fecharam decisões de uso: a página não pede senha e atende só o próprio computador por padrão, não há limite de envio nem de fila e os arquivos ficam guardados até a pessoa apagar.
### Como foi implementada
Conferida contra o combinado: os casos de erro ganharam verificação automática, inclusive a queda inesperada do conversor, e um teste confirma que a página e o serviço local usam os mesmos nomes para cada informação.
@metric Tarefas entregues | tasks
@metric Dúvidas esclarecidas | clarify-questions
@metric Revisão final | converge
@source docs/specs/web-interface/spec.md
@source docs/specs/web-interface/research.md
@source docs/specs/web-interface/data-model.md

<!-- slide: timeline -->
## A jornada
O produto veio primeiro. A documentação de cada peça chegou depois e, logo em seguida, as melhorias planejadas foram entregues e conferidas, peça por peça.
@timeline

<!-- slide: numbers -->
## O projeto em números
@metric Capacidades documentadas | specs
@metric Tarefas entregues | tasks
@metric Dúvidas esclarecidas | clarify-questions
@metric Princípios | principles

<!-- slide: closing -->
## O que vem a seguir
O horizonte é crescer em capacidades: novos formatos, novos conversores e mais recursos de qualidade. A base para isso está pronta: o que foi planejado está entregue e conferido, e, com os modelos já baixados, o conversor principal trabalha sem contatar a central de modelos.
> Qualidade e robustez em primeiro lugar.
@source docs/briefing.md
@source docs/specs/conversion-engines/spec.md

<!-- slide: sources -->
## Fontes
@sources
