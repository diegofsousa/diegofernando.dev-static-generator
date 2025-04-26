title: Erros comuns cometidos em Go - Parte I
date: 2025-04-25 17:44
author: diego
tags: golang, backend, programação
slug: erros-comuns-cometidos-em-go
og_image: assets/images/common-errors.jpeg


**Go** é uma linguagem marcada pela sua excentricidade, seja pelo foco em performance ou pela experiência única de desenvolvimento. Esse perfil faz com que muitos desenvolvedores, cometam alguns deslizes. Equívocos podem acontecer tanto com iniciantes quanto com profissionais mais experientes. Inclusive, por experiência própria, já me peguei utilizando traços de outra linguagem ao programar em Go.

Neste artigo, apresento **5 erros comuns** cometidos por quem está se aventurando na linguagem. Alguns dos pontos listados refletem situações que presencio no dia a dia. Além disso, fiz uma pesquisa para identificar outros cenários recorrentes. Essa é uma lista curada que pode fazer sentido principalmente para *gophers* de primeira viagem. Então vamos à lista:

# #1: Passando valores em vez de ponteiros

Neste caso, não se trata necessariamente de um erro. Na verdade, não há qualquer problema em passar valores diretamente, especialmente para tipos pequenos como `int`, `string` e `bool`. Porém, essa escolha faz diferença quando lidamos com tipos maiores, como uma struct que contém vários arrays.

Sempre que criamos uma função ou método que recebe um argumento por valor, o Go **cria uma cópia** do elemento dentro do escopo da função. Para ilustrar isso, vamos fazer um experimento: criaremos uma variável chamada `name` e uma função `showName`, na qual essa variável será passada por valor:

```
package main

import "fmt"

func main() {
	name := "test"

	showName(name)
}

func showName(name string) {
	fmt.Println(name)
}
```

Apesar de ser uma prática bastante comum, é importante entender exatamente o que está acontecendo. A execução do método `showName` implica na reserva de um novo espaço de memória para armazenar a cópia de `name`. Podemos fazer um pequena modificação no código para ilustrar:

```
package main

import "fmt"

func main() {
	name := "test"
	fmt.Println(&name)

	showName(name)
}

func showName(name string) {
	fmt.Println(&name)
	fmt.Println(name)
}
```

Nesta nova versão, imprimimos tanto o valor de `name` quanto seu endereço de memória no método `main` e dentro de `showName`. A saída será:

```
0xc000120040
0xc000120050
test

Program exited.
```

Os endereços `0xc000120040` e `0xc000120050` representam locais diferentes na memória. Isso evidencia que `name` foi copiado, ou seja: dentro de `showName` estamos trabalhando com uma nova instância, independente da original.

## Passando o valor de `name` x Passando o ponteiro de `name`

Em Go, geralmente sempre passamos valores. Porém, quando queremos manipular o mesmo espaço de memória, enviamos um como valor um ponteiro, que aponta para o dado original.

Com esse conceito em mente, conseguimos entender como funciona a passagem de parâmetros como **valor** e como **ponteiro**. Quando usamos a passagem por **valor**, a função `showName` recebe apenas o conteúdo de `name`. Agora, vejamos um exemplo de passagem por **ponteiro**:

```
package main

import "fmt"

func main() {
	name := "test"
	fmt.Println(&name)

	showName(&name)
}

func showName(name *string) {
	fmt.Println(name)
	fmt.Println(*name)
}
```

Modificamos o código anterior. Ao invés de passar o conteúdo de `name` para `showName`, enviamos seu endereço de memória. Com isso, também alteramos a definição da função: agora ela recebe um ponteiro de `string` (`*string`), em vez de uma `string` simples.

A forma de exibir o valor e o endereço de memória muda: para acessar o conteúdo, precisamos **desreferenciar** (ou *dereferenciar*) o ponteiro usando `*name`. A saída será:

```
0xc0000a8040
0xc0000a8040
test

Program exited.
```

Agora estamos manipulando `name` diretamente no mesmo endereço de memória. Um ponto interessante é que, se alterarmos o valor de `name` dentro da função `showName`, a variável original, definida no método `main`, também será alterada  (justamente porque ambas compartilham o mesmo espaço de memória).

# #2: Acreditar cegamente em ponteiros

Vamos a um caso clássico: declaração de um ponteiro e uso imediato. Quando trabalhamos com ponteiros, o ideal é **verificar se eles não estão nulos** antes de acessá-los. Uma situação de erro seria:

```
package main

import "fmt"

func main() {
	var test *int

	fmt.Println(*test)
}
```

A saída para este código é:

```
panic: runtime error: invalid memory address or nil pointer dereference
[signal SIGSEGV: segmentation violation code=0x1 addr=0x0 pc=0x491476]

goroutine 1 [running]:
main.main()
	/tmp/sandbox2767359061/prog.go:8 +0x16
```

Ao tentarmos imprimir o valor de `test` por meio da desreferenciação, ocorre um erro. Isso acontece porque o ponteiro não foi inicializado e, por padrão, é `nil`. A minha dica aqui é: **por padrão, nunca acredite em ponteiros**. Para este caso, uma verificação básica já evita o erro:

```
package main

import "fmt"

func main() {
	var test *int

    if test != nil {
        fmt.Println(*test)
    }
}
```

# #3: Ignorar erros

Quando lidamos com métodos e funções, normalmente nos deparamos com o seguinte cenário:

```
package main

import "fmt"

func main() {
	test, _ := doSomething()
	fmt.Println(*test)
}

func doSomething() (*int, error) {
	// do sometring
	return nil, fmt.Errorf("some error")
}
```

É muito tentador ignorar o tratamento de erros em Go, especialmente devido à sua verbosidade. Porém, não fazer o tratamento adequado é, de longe, a **pior** coisa que podemos fazer. No código acima, por consequência, iremos esbarrar no mesmo erro já visto anteriormente:

```
panic: runtime error: invalid memory address or nil pointer dereference
[signal SIGSEGV: segmentation violation code=0x1 addr=0x0 pc=0x49438f]

goroutine 1 [running]:
main.main()
	/tmp/sandbox2271710943/prog.go:8 +0x2f

Program exited.
```

Em Go, é comum que funções e métodos retornem um erro para sinalizar situações inesperadas. Por isso, sempre devemos considerar a possibilidade de falhas e tratar esses erros adequadamente para manter o fluxo da aplicação seguro. No caso acima, podemos evitar a falha criando um tratamento simples:

```
package main

import "fmt"

func main() {
	test, err := doSomething()

	if err != nil {
		fmt.Println("error")

		// add handling error
		return
	}

	fmt.Println(*test)
}

func doSomething() (*int, error) {
	// do sometring
	return nil, fmt.Errorf("some error")
}
```

Assim, garantimos que o programa não sofra interrupções inesperadas.

# #4: Supergeneralizar erros
Existe um [discurso bem famoso feito pelo próprio Rob Pike sobre erros](https://go.dev/blog/errors-are-values), chamado ***"Errors are values"***. Isso endossa bem a filosofia da linguagem e nos convida a refletir sobre visão tradicional deste tema.

> “***Whatever you do, always check your errors!. -Rob Pike***”. 

Vamos entender esse ponto com um caso de uso de um sistema que realiza chamadas a um banco de dados:

```
package main

import (
	"fmt"
	"log"
)

type Person struct {
	name string
}

func (person Person) validate() error {
	if person.name == "" {
		return fmt.Errorf("person with no name")
	}
	return nil
}

func main() {

	p := Person{
		name: "diego",
	}

	err := createPerson(&p)

	if err != nil {
		log.Println(err)
	}

}

func createPerson(person *Person) error {

	// validate person
	err := person.validate()

	if err != nil {
		return fmt.Errorf("db insert error")
	}

	// get db instance
	db, err := GetDB()

	if err != nil {
		return fmt.Errorf("db insert error")
	}

	// db commit data
	err := db.Commit()

	if err != nil {
		return fmt.Errorf("db insert error")
	}

	return nil
}
```

Supondo que todas as camadas estejam bem implementadas, esse código tende a funcionar. Mas o problema excede o fato de funcionar ou não. A dúvida implícita neste código é: *como sabemos o que **de fato** aconteceu em um erro `db insert error`?* Um erro genérico como esse pode ter várias causas diferentes. Podemos melhorar o tratamento assim:

``` 
    // ...
	// validate person
	err := person.validate()

	if err != nil {
		return err
	}

	// get db instance
	db, err := GetDB()

	if err != nil {
		return fmt.Errorf("get instance db error")
	}

	// db commit data
	err := db.Commit()

	if err != nil {
		return fmt.Errorf("db commit error")
	}

	return nil
    // ...
```

Essa pequena mudança já traz um panorama muito mais claro sobre o que de fato ocorreu. Uma sugestão adicional para melhorar ainda mais a tratativa de erros é **implementar a interface de erro do Go**, criando erros personalizados e enriquecendo as mensagens de retorno. Veremos isso no próximo tópico.

## Criando tipos de erros personalizados através da interface `error`

No Go, qualquer tipo que implemente a seguinte interface é considerado um erro:

```
type error interface {
    Error() string
}
```

Quando sobrescrevemos essa interface, temos a possibilidade de criar tipos de erros personalizados. Isso traz muito mais **flexibilidade**, pois não ficamos mais limitados a usar apenas uma string para identificar o erro. Veja o exemplo abaixo:

```
package main

import (
	"fmt"
    "log"
)


type Person struct {
	name string
}

type CreatePersonError struct {
	Op  string // failed operation (ex: "get_db_instance", "db_commit")
	Err error  // original error
}

func (e *CreatePersonError) Error() string {
	return fmt.Sprintf("create person failed at %s: %v", e.Op, e.Err)
}

func (person Person) validate() error {
	if person.name == "" {
		return fmt.Errorf("person with no name")
	}
	return nil
}

func main() {

	p := Person{
		name: "diego",
	}

	err := createPerson(&p)

	if err != nil {
		log.Println(err)
	}

}

func createPerson(person *Person) error {
	err := person.validate()
	if err != nil {
		return err
	}

	// get db instance
	db, err := GetDB()
	if err != nil {
		return &CreatePersonError{
			Op:  "get_db_instance",
			Err: err,
		}
	}

	// db commit data
	err = db.Commit()
	if err != nil {
		return &CreatePersonError{
			Op:  "db_commit",
			Err: err,
		}
	}

	return nil
}

```

Criamos um novo tipo chamado `CreatePersonError` e implementamos o método `Error()` para ele.
Assim, capturamos o erro original e conseguimos adicionar informações importantes, como a operação que falhou. Todas essas melhorias facilitam um possível *troubleshooting* em cenários de falhas.

# #5: Registrar erros com `log.Fatal()`

Quando nosso sistema encontra um erro irrecuperável, registrar o erro com `log.Fatal()` pode parecer uma solução conveniente, já que ele registra a mensagem e encerra o processo imediatamente. Porém, o que muitas vezes passa despercebido é que `log.Fatal()` internamente faz uma chamada a `os.Exit()`.
Isso é **problemático** porque impede a execução de qualquer outra rotina de limpeza ou encerramento, como `defer`'s ou fechamento de conexões.

Por isso, a abordagem recomendada é sempre retornar o erro para o nível superior da aplicação, onde ele possa ser tratado adequadamente. Normalmente, o único local onde o uso de `log.Fatal()` é considerado aceitável é dentro da função `main()`, onde faz sentido finalizar a execução do programa de maneira controlada.

# Considerações finais

Existem muitas outras situações que poderiam ser listadas aqui (**inclusive, me conta nos comentários quais você adicionaria!** 😊).
O Go é uma linguagem que tem padrões bem estabelecidos e formas claras de construir soluções. E é completamente normal a gente tropeçar de vez em quando, às vezes por descuido, por falta de atenção ou simplesmente pela correria do dia a dia (*afinal, todos temos prazos, né?*).

Neste post, quis compartilhar algumas situações que já vi acontecer (algumas vividas na pele) errando, aprendendo e, claro, criando alguns bugs no caminho. A ideia foi trazer um pouco dessas experiências e boas práticas que fazem parte do ecossistema Go.

Minha intenção é transformar esse post em uma série, então fica por aqui e vamos seguir aprendendo juntos.

Até a próxima :)

#### Referências

- [https://www.jetbrains.com/guide/go/tutorials/handle_errors_in_go/common_mistakes/](https://www.jetbrains.com/guide/go/tutorials/handle_errors_in_go/common_mistakes/)
- [https://medium.com/@sebdah/go-best-practices-error-handling-2d15e1f0c5ee](https://medium.com/@sebdah/go-best-practices-error-handling-2d15e1f0c5ee)
- [https://earthly.dev/blog/learning-golang-common-mistakes-to-avoid/](https://earthly.dev/blog/learning-golang-common-mistakes-to-avoid/)
- [https://weilson.medium.com/top-5-most-common-mistakes-in-golang-56be1be9d676](https://weilson.medium.com/top-5-most-common-mistakes-in-golang-56be1be9d676)
- [https://go.dev/blog/errors-are-values](https://go.dev/blog/errors-are-values)