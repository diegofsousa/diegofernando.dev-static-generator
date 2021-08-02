# Gerador do site diegofernando.dev

Tecnologias usadas:
 - Pelican


Dependências necessárias para geração do site:

- Criar um diretório "pelican-plugins" com o conteúdo do repositório https://github.com/getpelican/pelican-plugins

- Rodar em ambiente de desenvolvimento
   - `pelican content -s pelicanconf.py  -o output`
   - `pelican -l`
- Gerar output para produção:
   - `make publish`

Créditos:
 - Attila theme
    - https://github.com/arulrajnet/attila