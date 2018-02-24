# encoding=utf8  
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

import os
import json

# Criar um diretório louvor se ele não existir
directory = "./louvor"
if not os.path.exists(directory):
    os.makedirs(directory)

# Carrega um json e mostra os dados
# data = json.load(open('teste.json'))
data = json.load(open('louvores2018.json'))

#ajuste de identação
try:
    import textwrap
    textwrap.indent
except AttributeError:  # undefined function (wasn't added until Python 3.3)
    def indent(text, amount, ch=' '):
        padding = amount * ch
        return ''.join(padding+line for line in text.splitlines(True))
else:
    def indent(text, amount, ch=' '):
        return textwrap.indent(text, amount * ch)

for louvor in data:  
    titulo = louvor['title'].upper().strip()
    # Criar um diretório com o nome do louvor se ele não existir
    if not os.path.exists(directory+'/'+titulo):
        os.makedirs(directory+'/'+titulo)  
        print('Criado: '+titulo)

    # conta quantos arquivos serão criados verificando as estrofes
    arquivos = louvor['content'].split('\n\n')
    for index, conteudo in enumerate(arquivos, start=1):
        nome = titulo
        f = open(directory+'/'+titulo+'/'+titulo+'_{0}.html'.format(index),'w')
        #ajusta conteudo
        ajustado = conteudo.replace("\n","<br>\n")
        ajustado = indent(ajustado,12)
        codigohtml = """<html>
    <head>    
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">    
    <link href="../../css/style.css" rel="stylesheet" />"""

        if index == 1 and len(titulo) > 32:
            nome = titulo.replace(titulo.split()[len(titulo.split()) / 2],titulo.split()[len(titulo.split()) / 2]+'<br>')
            codigohtml+="""
    <style type="text/css">
      /* Estilo para colocar o Título em duas linhas centralizado */
      #titulo{{
        font-size: 2.7vw; 
        height: none; 
        line-height: 90%;  
      }}     
    </style>"""

        codigohtml+="""    
    </head>
    <body id="principal">"""      

        # Ajuste de estrutura
        if index == len(arquivos):
            codigohtml+="""
    <div id="estrutura-final">"""
        else:
            codigohtml+="""
    <div id="estrutura">"""

        # Ajuste de titulo e logo
        if index == 1:
            codigohtml+="""
      <!-- Chamada do título -->
      <div id="titulo"><span class="cell-middle">{0}</span></div>
      
      <!-- Chamada da logo com título (vinho) -->
      <div id="logo"><span class="icon-logo_bold"></span></div>
        <div id="louvor">
          <div>
"""
        else:
            codigohtml+="""
      <!-- Camada logo sem título (branca) -->
      <div id="logo-branca"><span class="cell-middle icon-logo_bold_white"></span></div>
        <div id="louvor">
          <div>
"""         

        codigohtml+=ajustado#conteudo.replace("\n","<br>\n")

        codigohtml+="""
          </div>
        </div>
    </div>"""

        if index == len(arquivos):
            codigohtml+="""
    <!-- Chamada do rodapé com as formatações necessárias-->
    <div id="rodape">Fim</div>"""

        codigohtml+="""
    </body>
</html>"""

        print('Arquivo criado: '+louvor['title']+'_{0}.html'.format(index))
        f.write(codigohtml.format(nome))
        f.close()