# Codex ImageGen para Claude Code

Skill para gerar e editar imagens no Claude Code usando o gerador nativo do Codex CLI e seu login do ChatGPT. Ela entrega um PNG no projeto e usa os limites do Codex da sua conta. [Documentação da geração nativa](https://learn.chatgpt.com/docs/image-generation?surface=cli).

## Instalação

Você precisa do [Claude Code](https://code.claude.com/docs/en/overview), do Python 3 e de uma versão do [Codex CLI](https://learn.chatgpt.com/docs/cli) com geração de imagens. Use `codex login` para entrar com o ChatGPT e confirme com `codex login status`.

```bash
git clone https://github.com/guilhermealvestech/codex-imagegen.git
mkdir -p ~/.claude/skills
cp -R codex-imagegen/skills/codex-imagegen ~/.claude/skills/
```

Para instalar só em um projeto, copie a pasta da skill para `.claude/skills/` na raiz desse projeto. [Documentação das skills do Claude Code](https://code.claude.com/docs/en/skills).

## Uso

Em uma sessão do Claude Code:

```text
/codex-imagegen Gere um metrônomo 3D azul e creme com fundo transparente. Salve em output/metronomo.png.
```

Para editar uma imagem existente, indique o arquivo e o que deve mudar:

```text
/codex-imagegen Edite output/metronomo.png, mude apenas o pêndulo para azul-claro e salve em output/metronomo-v2.png.
```

Também dá para rodar o script direto no terminal:

```bash
python3 ~/.claude/skills/codex-imagegen/scripts/generate.py \
  'Crie um metrônomo 3D azul e creme com fundo transparente.' \
  -o output/metronomo.png
```

`-i caminho.png` anexa uma imagem de referência ou de edição. Pode ser repetido. `--model` seleciona o agente do Codex e `--reasoning` ajusta seu esforço, que começa em `low`. O gerador de imagens é escolhido pelo próprio Codex.

A skill pede uma imagem por execução. O tamanho e a transparência dependem da saída nativa, que o Claude confere após salvar. Se o Codex não gerar um PNG, o script informa o erro. Para repetir a geração, use um caminho de saída novo.
