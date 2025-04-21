title: O Go não foi feito pra ser bonito... e isso não deveria ser um problema.
date: 2025-04-20 10:05
author: diego
tags: golang, backend, programação
slug: o-go-nao-foi-feito-pra-ser-bonito
og_image: assets/images/gopher-misc-3.jpg

# É isso mesmo que você leu: o Go não foi feito para ser bonito

Essa frase, apesar de forte, não soa tão impactante para quem já utiliza essa linguagem. Ou, pelo menos, não deveria. Assim como grande parte das linguagens populares atualmente, Go é uma linguagem *C-like*, ou seja, baseada em C. Por isso, muito do código escrito em Go é, de fato, inspirado em C.

Go surgiu em 2009, após Rob Pike e Ken Thompson liderarem o projeto inicial dentro do Google. A motivação era uma frustração com o cenário das linguagens existentes, devido a um dilema clássico da programação: escolher entre **compilação eficiente**, **execução eficiente** ou **facilidade de programação**. Na época, muitas das linguagens ainda em uso hoje, como Python e JavaScript, já estavam em evidência. Isso se dava pelo fato de que os desenvolvedores vinham migrando aos poucos para linguagens com tipagem dinâmica, em detrimento da tipagem forte, como C++ e Java.

> “***We were not alone in our concerns. After many years with a pretty quiet landscape for programming languages, Go was among the first of several new languages—Rust, Elixir, Swift, and more—that have made programming language development an active, almost mainstream field again. -official doc***”. 

![Memesobre performance em Go](/assets/images/meme-go.png)*O simples funciona.*

A escolha entre uma linguagem eficiente ou fluída em termos de dinâmica tem grande impacto na concepção de um software. Essas são características que, até então, não coexistiam em uma única linguagem ou tecnologia. Rob e Ken insistiram na ideia de que era possível criar um ecossistema que comportasse as duas vertentes. Ainda bem, né? :)

# Go e eficiência: tudo a ver?

Sim, e vai além disso: podemos afirmar que Go **foi projetada com foco em eficiência**. Há diversos fatores que demonstram essa preocupação, aqui nos ateremos a alguns deles, começando pelo fator compilação.

![Usando o "go build"](/assets/images/build-go.gif)*Usando o "go build".*

Diferente de linguagens como Python e Ruby, Go é compilada, o que, por si só, já a torna mais rápida e eficiente. Em relação a outras que utilizam máquina virtual, a exemplo de Java e Kotlin, temos uma grata surpresa: Go compila diretamente para código de máquina. Sem a necessidade da JVM como intermediária, a velocidade de execução é superior.

## Um parêntese importante: Goroutines

Concorrência é um dos pontos em que Go mais se destaca. Enquanto muitas linguagens sobrecarregam recursos ao utilizar *threads*, Go opera com um custo muito menor graças às **Goroutines**, sua abordagem para criação de código concorrente. Go possui um escalonador de tarefas próprio, que não depende de recursos externos para gerenciar processos simultâneos. Esse ponto, isoladamente, já merece um artigo exclusivo 👀.

O objetivo deste artigo não é trazer *benchmarks*, provar pontos de performance da linguagem Go ou tentar convencer alguém a usar. O intuito é fazer uma reflexão em cima das características de uma linguagem. Entretanto, caso queira explorar mais a fundo, há um ["monitoramento" de benchmarks](https://go.dev/wiki/Benchmarks) disponível na documentação oficial.

# Ah, não é tão feio assim, vai!

Ok, ainda temos um ponto a discutir. Talvez um dos principais motivos que afastam novos usuários do Go seja sua sintaxe. Mas será que ela é realmente tão ruim quanto dizem? Parafraseando a própria documentação oficial:

> “***Go attempts to reduce the amount of typing in both senses of the word. Throughout its design, we have tried to reduce clutter and complexity. There are no forward declarations and no header files; everything is declared exactly once. Initialization is expressive, automatic, and easy to use.. -official doc***”. 


Para entender melhor, vamos comparar a sintaxe de Go com outras linguagens. Para sermos justos, os exemplos não utilizarão bibliotecas externas, nem o clássico "Hello, World". As linguagens escolhidas para a análise são Python, JavaScript e Java.

### Requisição HTTP e leitura JSON

Neste primeiro exemplo, faremos uma requisição HTTP e o tratamento da resposta em JSON.

#### Go
```
package main

import (
    "encoding/json"
    "fmt"
    "net/http"
)

func main() {
    resp, err := http.Get("https://jsonplaceholder.typicode.com/posts")
    if err != nil {
        panic(err)
    }
    defer resp.Body.Close()

    var data []map[string]interface{}
    if err := json.NewDecoder(resp.Body).Decode(&data); err != nil {
        panic(err)
    }

    fmt.Println("First post title:", data[0]["title"])
}
```

#### Python
```
import urllib.request
import json

with urllib.request.urlopen("https://jsonplaceholder.typicode.com/posts") as response:
    data = json.loads(response.read())

print("First post title:", data[0]["title"])

```

#### JavaScript
```
const https = require('https');

https.get('https://jsonplaceholder.typicode.com/posts', res => {
    let data = '';
    res.on('data', chunk => data += chunk);
    res.on('end', () => {
        const json = JSON.parse(data);
        console.log("First post title:", json[0].title);
    });
}).on('error', err => console.error(err));
```

#### Java
```
import java.io.*;
import java.net.*;
import javax.json.*;

public class Main {
    public static void main(String[] args) throws Exception {
        URL url = new URL("https://jsonplaceholder.typicode.com/posts");
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("GET");

        try (InputStream is = conn.getInputStream();
             JsonReader reader = Json.createReader(is)) {

            JsonArray array = reader.readArray();
            System.out.println("First post title: " + array.getJsonObject(0).getString("title"));
        }
    }
}

```

### Execução paralela

Agora, executaremos três tarefas simultaneamente. Vale lembrar que Go trata tarefas concorrentes (e não paralelas) com Goroutines.

#### Go
```
package main

import (
    "fmt"
    "sync"
    "time"
)

func task(id int, wg *sync.WaitGroup) {
    defer wg.Done()
    time.Sleep(2 * time.Second)
    fmt.Println("Task", id, "completed")
}

func main() {
    var wg sync.WaitGroup
    for i := 1; i <= 3; i++ {
        wg.Add(1)
        go task(i, &wg)
    }
    wg.Wait()
    fmt.Println("All tasks completed")
}

```

#### Python
```
import threading
import time

def task(id):
    time.sleep(2)
    print(f"Task {id} completed")

threads = []
for i in range(1, 4):
    t = threading.Thread(target=task, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("All tasks completed")

```

#### JavaScript

Não se aplica.

#### Java
```

public class Main {
    public static void main(String[] args) throws InterruptedException {
        Thread[] threads = new Thread[3];

        for (int i = 0; i < 3; i++) {
            final int id = i + 1;
            threads[i] = new Thread(() -> {
                try {
                    Thread.sleep(2000);
                    System.out.println("Task " + id + " completed");
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            });
            threads[i].start();
        }

        for (Thread t : threads) {
            t.join();
        }

        System.out.println("All tasks completed");
    }
}

```

### Leitura de arquivo CSV

Por fim, vamos ler um arquivo CSV com os campos `nome,idade` e somar as idades.

#### Go

```
package main

import (
    "encoding/csv"
    "fmt"
    "os"
    "strconv"
)

func main() {
    f, _ := os.Open("data.csv")
    defer f.Close()

    r := csv.NewReader(f)
    records, _ := r.ReadAll()

    sum := 0
    for _, row := range records {
        age, _ := strconv.Atoi(row[1])
        sum += age
    }

    fmt.Println("Sum of ages:", sum)
}

```

#### Python

```
sum_ages = 0
with open("data.csv") as f:
    for line in f:
        _, age = line.strip().split(",")
        sum_ages += int(age)

print("Sum of ages:", sum_ages)
```

#### JavaScript
```
const fs = require('fs');

fs.readFile('data.csv', 'utf8', (err, data) => {
    const lines = data.trim().split('\n');
    let sum = 0;
    for (const line of lines) {
        const [, age] = line.split(',');
        sum += parseInt(age);
    }
    console.log("Sum of ages:", sum);
});

```

#### Java

```
import java.io.*;
import java.nio.file.*;

public class Main {
    public static void main(String[] args) throws IOException {
        int sum = 0;
        for (String line : Files.readAllLines(Paths.get("data.csv"))) {
            String[] parts = line.split(",");
            sum += Integer.parseInt(parts[1]);
        }
        System.out.println("Sum of ages: " + sum);
    }
}

```

Diante dos exemplos apresentados que buscam reproduzir o mesmo comportamento entre as linguagens, é possível perceber que Go, embora verbosa, não apresenta uma diferença significativa. Isso nos leva a uma reflexão importante: **será que sintaxe é realmente o fator mais determinante no desenvolvimento de software**? Ou uma linguagem que une eficiência com simplicidade tem mais valor?

A resposta, como quase sempre em engenharia de software, é: **depende**. Esta análise é simplificada e não cobre todas as nuances envolvidas na escolha de uma linguagem. Todavia, a reflexão é válida. E a partir dela, uma prova de conceito pode muito bem ser aplicada.

Quando afirmo que o fato de Go não ser tão amigável não deveria ser um problema, estou me referindo ao dilema constante de equilibrar prioridades. O que é mais importante dentro de um contexto? Familiaridade com a linguagem? Até que ponto? Um incômodo na hora de tratar exceções? Tempo de inicialização? Qual é o tempo aceitável?

Essas são reflexões que fazem parte do dia a dia de um engenheiro de software. E, complementando o título deste artigo, **Go não foi feito para ser bonito. Foi feito para ser confiável, durável e simples**.

Até a próxima :)

#### Referências

- [https://go.dev/wiki/Benchmarks](https://go.dev/wiki/Benchmarks)
- [https://dev.to/nigelsilonero/how-does-golang-handle-concurrency-better-than-other-languages-2e51?utm_source=chatgpt.com](https://dev.to/nigelsilonero/how-does-golang-handle-concurrency-better-than-other-languages-2e51)
- [https://go.dev/doc/faq](https://go.dev/doc/faq)
- [https://go.dev/talks/2012/splash.article](https://go.dev/talks/2012/splash.article)