title: [PT] Entendendo o package Context em Go
date: 2022-10-09 10:05
author: diego
tags: golang, context, programação
slug: entendendo-o-package-context-em-go
og_image: assets/images/gophers_working.jpg

Nos últimos meses tenho voltado meus esforços para o estudo da linguagem Go. Confesso que não é meu primeiro contato com a linguagem – lá em 2017 tive a oportunidade de apresentar um minicurso introdutório em um simpósio universitário. Apesar de não ser uma novidade, precisei revisitar alguns conceitos. O pacote **context.Context** é um deles. Então, let's go!

![Dwight Schrute mandando um "let's go!"](/assets/images/lets-go-dwight-schrute.gif)

Olhando para a [documentação oficial](https://pkg.go.dev/context), temos o seguinte trecho:
> “***Package context defines the Context type, which carries deadlines, cancellation signals, and other request-scoped values across API boundaries and between processes***”. 


Ou seja, o Context permite a criação de prazos e valores de escopo de execução aos processos em que ele é compartilhado. Essa mágica acontece pelo fato que o Context usa *channels* para enviar sinais aos processos, e esses processos por sua vez, escutam essas instruções controlando ações de parada.

Um exemplo clássico de seu uso é em situações de requisições para API’s externas onde queremos delimitar um tempo de espera pela resposta. Também existem outras situações que podemos nos beneficiar do seu uso, tais como controlar o tempo limite de processamento de instruções e determinar prazo de execução de *query* ao banco de dados, por exemplo. Enfim, são várias as possibilidades.

# Iniciando um Context

Antes de começarmos a detalhar os tipos de Context, é importante entendermos como se dá a sua inicialização. **Todo Context para ser usado, deve ser inicializado vazio em algum momento do ciclo de vida**. A própria documentação do Go desencoraja passar `nil` como parâmetro em situações que o requerem. Existem duas formas de inicializá-lo - **context.Background()** e  **context.TODO()**:

### context.Background()

```
package main

import (
	"context"
	"fmt"
)

func main() {
	ctx := context.Background()
	fmt.Println(ctx)
}
```

O `context.Backgroud()` nos retorna um Context não nulo e vazio. **Normalmente é usado pela função principal ou *entrypoint* do projeto**.

### context.TODO()

```
package main

import (
	"context"
	"fmt"
)

func main() {
	ctx := context.TODO()
	fmt.Println(ctx)
}
```

Assim como seu antecessor, o `context.TODO()` também nos retorna um Context não nulo e vazio. A principal diferença é que o **seu uso se dá quando não estiver claro o contexto que se deve usar ou ele ainda não estiver disponível**.


# Tipos de Context


Existem basicamente **três tipos** de Context:

- Cancellation Signals
- Deadline
- Request-scoped values

### Cancellation Signals

O tipo **Cancellation Signals** define um Context que pode ter sua execução interrompida através de um comando. Neste caso, a instrução segue o fluxo normal  até que em certo ponto do código seja dada a sua parada. A seguir, um exemplo de implementação:

```
package main

import (
	"context"
	"fmt"
	"time"
)

func main() {
	ctx := context.Background()
	ctx, cancel := context.WithCancel(ctx)

	go executeFunction(ctx)
	time.Sleep(3 * time.Second)
	cancel()
	time.Sleep(1 * time.Second)
}

func executeFunction(ctx context.Context) {
	for {
		select {
		case <-ctx.Done():
			fmt.Println("Stopping code execution...")
			return
		default:
			time.Sleep(1 * time.Second)
			fmt.Println("Running at", time.Now())
		}
	}
}
```

Antes de explicar a função `main()`, vamos entender primeiro a função `executeFunction()`, pois ela irá receber instruções do Context. Ao receber um parâmetro do tipo `context.Context` fazemos um *loop* infinito, onde, assim que receber o sinal de parada vindo do contexto, ela irá apresentar o texto “**Stopping code execution...**” e terminará sua execução através de um `return` explícito. Caso contrário, seguirá sua execução apresentando “**Running at [horário]**”. O comando `select` funciona como uma espécie de *switch-case*, porém aplicado ao sinais provenientes de ***channels***, como é o caso de Contexts. Como percebemos, o sinal de parada no código é dado pela instrução `ctx.Done()`.

Retornando para a função `main()`, a primeira coisa que fazemos é definir um Context através do `context.Backgroud()`. Após isso, usamos a função `context.WithCancel()` passando o nosso contexto base. Ele nos devolve um novo contexto e uma segunda instrução que chamamos de `cancel`. Ela é essencial para definir a parada das instruções que estão ligadas a este contexto. Enquanto executamos a função `executeFunction()` de forma assíncrona, esperamos três segundos para forçar seu cancelamento com a instrução `cancel()` - aquela mesmo que recebemos do contexto :) . 

O resultado da execução será semelhante ao *log* abaixo:

```
Running at 2022-10-09 16:15:46.80042576 -0300 -03 m=+1.000598497
Running at 2022-10-09 16:15:47.801454038 -0300 -03 m=+2.001626779
Running at 2022-10-09 16:15:48.801876258 -0300 -03 m=+3.002048999
Stopping code execution...
```

### Deadline

Como o próprio termo sugere, um Context do tipo **Deadline** delimita o tempo de execução de uma instrução ou processo. Podemos então informar para a aplicação até quando determinado código pode demorar. Temos duas funções diferentes para trabalhar com **Deadline**:

- **`context.WithDeadline()`** - É definido um **valor de tempo fixo**.
	- Exemplo: o contexto tem até as 22h do dia 09 de outubro de 2022 para ser executado.
- **`context.WithTimeout()`** - É definido um **valor de tempo a partir do instante que foi instanciado**.
	- Exemplo: o contexto tem 4 minutos a partir de agora para ser executado.

#### context.WithDeadline()

Vamos então pegar o mesmo código anterior e alterar alguns trechos:

```
package main

import (
	"context"
	"fmt"
	"time"
)

func main() {
	ctx := context.Background()
	deadline := time.Now().Add(3 * time.Second)
	ctx, cancel := context.WithDeadline(ctx, deadline)

	defer cancel()

	executeFunction(ctx)
}

func executeFunction(ctx context.Context) {
	for {
		select {
		case <-ctx.Done():
			fmt.Println("Stopping code execution...")
			return
		default:
			time.Sleep(1 * time.Second)
			fmt.Println("Running at", time.Now())
		}
	}
}
```

Instanciamos uma nova variável `deadline` somando três segundos ao tempo de agora e passamos ela para a função `context.WithDeadLine()`. Dessa forma a instrução da função `executeFunction()` será interrompida após o intervalo de três segundos.

O resultado da execução do código acima será semelhante a seguinte saída:

```
Running at 2022-10-09 17:30:50.492897161 -0300 -03 m=+1.000190057
Running at 2022-10-09 17:30:51.493583512 -0300 -03 m=+2.000876359
Running at 2022-10-09 17:30:52.493694606 -0300 -03 m=+3.000987449
Running at 2022-10-09 17:30:53.493795753 -0300 -03 m=+4.001088530
Stopping code execution…
```

#### context.WithTimeout()

Podemos usar a função `context.WithTimeout()` para produzir o mesmo comportamento. Basta alterarmos as linhas **11** e **12** por:

```
deadline := 3 * time.Second
ctx, cancel := context.WithTimeout(ctx, deadline)
```


A diferença, para o código anterior é que, agora, não precisamos mais fazer o cálculo do instante atual somado com os três segundos. A saída será a mesma.


Um ponto curioso nessa estrutura é que executamos também o `cancel()`, porém com a palavra-chave `defer` para assegurar que ele será a última coisa a ser executada. Apesar de estarmos delimitando o tempo de execução, **podemos também antecipar o cancelamento da instrução a qualquer momento se sobrepondo a regra do limite de tempo**, assim como explicado na seção **Cancellation Signals**.


#### Request-scoped value

Além de controlar tempo de execução e parada, com Context também é possível passar valores no estilo **chave-valor** para instruções filhas. Esse conceito é importante pois ele **funciona independente se a chamada para as instruções é síncrona ou assíncrona**. Esses valores ficam salvos dentro do contexto e são imutáveis. Vamos detalhar o código abaixo um modelo síncrono:

```
package main

import (
	"context"
	"fmt"
)

func main() {
	ctx := context.Background()
	ctx = context.WithValue(ctx, "sessionId", "Session123")
	showValue(ctx)
}

func showValue(ctx context.Context) {
	fmt.Println(ctx.Value("sessionId"))
	addKeyValue(&ctx, "typeError", "ErrorType123")
	fmt.Println(ctx.Value("typeError"))
}

func addKeyValue(ctx *context.Context, key interface{}, value interface{}) {
	*ctx = context.WithValue(*ctx, key, value)
}
```

Definimos o contexto inicial vazio com `context.Background()`. Após isso, criamos um novo contexto a partir do inicial com `context.WithValue()` e já também adicionamos valores fictícios ao contexto. Como esses valores ficam guardados no Context, podemos acessá-los em outra parte no programa com a função `ctx.Value()` passando a chave correspondente. Caso essa chave não exista o retorno é `nil`. Também é possível adicionar novos valores a um contexto criando um `context.WithValues()` passando o contexto anterior e atualizando ele próprio.


# Demais cenários

Os casos de uso do Context não se limitam aos aqui apresentados. Atualmente, as bibliotecas em Go, sejam nativas ou não requerem passar Context em suas instruções. O objetivo desse post foi entender a sua base e seus usos comuns.

Até a próxima :)

#### Referências

- [https://pkg.go.dev/context](https://pkg.go.dev/context)
- [https://www.digitalocean.com/community/tutorials/how-to-use-contexts-in-go](https://www.digitalocean.com/community/tutorials/how-to-use-contexts-in-go)
- [https://p.agnihotry.com/post/understanding_the_context_package_in_golang/](https://p.agnihotry.com/post/understanding_the_context_package_in_golang/)
- [https://www.youtube.com/watch?v=eGYZPUoH78c](https://www.youtube.com/watch?v=eGYZPUoH78c)
