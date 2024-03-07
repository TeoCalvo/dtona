# Maratona de Data Science (DTona!)

## Aprendendo Data Science na vida real!

Vamos fazer lives com projetos reais, mostrando como é realmente o dia a dia de um cientista de dados. Você entenderá todo o ciclo analítico, bem como as tecnologias adotadas em cada etapa e as boas práticas para que tudo funcione.

Nossas lives acontecem sempre na [Twitch](https://www.twitch.tv/teomewhy), às 20hrs. Você pode conferir nosso calendário com toda a programação. Caso você perca alguma live, a mesma fica gravada por 14 dias na própria Twitch. Vamos fazer um esforço para colocá-las no nosso canal do [YouTube](https://www.youtube.com/channel/UC-Xa9J9-B4jBOoBNIHkMMKA), mas lembre-se que é muito mais divertido estar conosco ao vivo!

## Calendário

Episódio | Dia | Conteúdo |
|:------------:|:------------:|:--------------------------------:|
| 1 | 30-04-2020 | Machine Learning Getting Started |
| 2 | 05-05-2020 | Criação de book de variáveis I |
| 3 | 07-05-2020 | Criação de book de variáveis II |
| 4 | 12-05-2020 | Nossa primeira safra |
| 5 | 14-05-2020 | ABT (Analytical Base Table) |
| 6 | 19-05-2020 | O que é base Out Of Time? |
| 7 | 21-05-2020 | Primeiro Classificador Treinado! |
| 8 | 26-05-2020 | Comparando modelos |
| 9 | 28-05-2020 | Fazendo predições / deploy |
| 10 | 02-06-2020 | Convidado especial: PyCaret |
| 11 | 04-06-2020 | Primeiros passos em Cluster |
| 12 | 09-06-2020 | Segundos passos em Cluster |
| 13 | 11-06-2020 | Fazendo score para Cluster? |

#### Episódio 1
Demos o primeiro passo no mundo de ciência de dados, apresentando os conceitos de Machine Learning e como a máquina gera suas próprias regras a partir de exemplos. Nos próximos episódios, vamos descobrir como criar essa tabela de exemplos.

#### Episódio 2 e 3
Para cada problema de negócio enfrentando é necessário criar característas do evento de interesse, ou seja, criar um ETL para agregar e cruzar informações de diferentes fontes de dados. Não seria o máximo ter algumas dessas características já criadas e poderem ser aproveitadas em vários modelos distintos? Damos o nome de "Book de Variáveis" para essa prateleira de variáveis. Neste episódio, antes de começar a colocar a mão no código, vamos configurar todo nosso ambiente! Muito **SQL** envolvido, do básico ao avançado.

#### Episódio 4
Com todas variáveis criadas, podemos finalmente dar um próximo passo rumo à ABT (Analytical Base Table). Vamos construir nossa primeira safra, entendendo o que é este conceito e qual a importância de ter várias safras. Queremos deixar claro a real importância dessa etapa em um problema de Machine Learning.

#### Episódio 5
Chegou a hora de consolidar todas as safras em uma única tabela, fornecendo tudo o que é necessário para 'ensinar' a máquina. Finalmente temos nossa ABT pronta para alimentar a máquina com informações! Podemos dar início à algumas estatísticas descritivas e entender essa base de dados, usaremos **Pandas**!

#### Episódio 6
Treinar a máquina é uma coisa, mas como avaliar seu comportamento no futuro? Há uma base especial para fazer este tipo de teste: Out of Time. Algumas pessoas também chamam de base "Exposted" ou "Backtest".

#### Episódio 7
Chegou a hora da verdade!! Vamos treinar nosso primeiro classificador. O que será ele? Random Forest? Nãoooo. XGBoost? Nãoooo. Regressão logística? Talvez... Mas o que é necessário fazer antes de treinar o modelo? Transformar dados? Combinar variáveis?

#### Episódio 8
Vamos brincar com outros algoritmos? Qual sua técnica predileta? Vamos conhecer mais o que **scikit-learn** tem a nos oferecer! 

#### Episódio 9
Modelo treinado e validado! Mas e agora? Fazer o que com ele? Quem vai usá-lo? Quem vai gerar valor a partir dele?

## Códigos e dados
Todo material necessário para acompanhar o que será desenvolvido ficará disponível neste repositório. Os dados foram adquitido no [Kaggle](https://www.kaggle.com/olistbr/brazilian-ecommerce), fornecidos pela empresa [Olist](https://olist.com/).

Para baixar os dados originais, clique [aqui](https://drive.google.com/file/d/1YEohXFk7zSajy3Nitzi_svDnu9x4ZFn8/view). Após o download, mantenha o arquivo **olist.db** dentro da pasta ***/data***.

## Links úteis:

|Tema|Link|
|:--------------:|:------------------:|
| Ambiente Python | [Anaconda](https://anaconda.org/) |
| Lib p/ Matrizes | [NumpPy](https://numpy.org/) |
| Lib p/ DataFrames | [Pandas](https://pandas.pydata.org/) |
| Lib p/ Machine Learning | [Scikit-Learn](https://scikit-learn.org/stable/) |
| Editor de código | [VS Code](https://code.visualstudio.com/) |
| Editor de código | [Sublime3](https://www.sublimetext.com/3) |
| Distribuição GNU/Linux | [Manjaro](https://manjaro.org/) |
| Distribuição GNU/Linux | [Ubuntu](https://ubuntu.com/) |
| Material | [Livros](https://github.com/TeoCalvo/twitch/blob/master/mateiral_apoio/livros.md)
| Comunidade | [Discord](https://discord.gg/EUMCn7z) |
