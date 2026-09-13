title: Understanding the Context package in Go
date: 2022-10-09 10:05
author: diego
lang: en
tags: golang, context, programming
slug: entendendo-o-package-context-em-go
og_image: assets/images/gophers_working.jpg

Over the past few months I've been putting more effort into studying Go. I'll admit it's not my first contact with the language — back in 2017 I had the chance to run an introductory workshop at a university symposium. Even though it isn't new to me, I had to revisit a few concepts. The **context.Context** package is one of them. So, let's go!

![Dwight Schrute saying "let's go!"](/assets/images/lets-go-dwight-schrute.gif)

Looking at the [official documentation](https://pkg.go.dev/context), we find the following excerpt:
> “***Package context defines the Context type, which carries deadlines, cancellation signals, and other request-scoped values across API boundaries and between processes***”.

In other words, Context lets you create deadlines and execution-scoped values for the processes it's shared with. That magic happens because Context uses *channels* to send signals to processes, and those processes, in turn, listen for these instructions to control stop actions.

A classic example of its use is when making requests to external APIs, where we want to cap how long we wait for a response. There are other situations where it comes in handy too, such as controlling how long an instruction is allowed to run, or setting a deadline for a database *query*, for example. In short, there are plenty of possibilities.

# Starting a Context

Before detailing the types of Context, it's important to understand how it's initialized. **Every Context has to be initialized empty at some point in its lifecycle before it can be used**. The Go documentation itself discourages passing `nil` as a parameter in situations that require one. There are two ways to initialize it — **context.Background()** and **context.TODO()**:

## context.Background()

```go
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

`context.Background()` returns a non-nil, empty Context. **It's normally used by the project's main function or *entrypoint***.

## context.TODO()

```go
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

Just like its predecessor, `context.TODO()` also returns a non-nil, empty Context. The main difference is that **it's used when it isn't clear yet which context should be used, or when one isn't available yet**.

# Types of Context

There are basically **three types** of Context:

- Cancellation Signals
- Deadline
- Request-scoped values

## Cancellation Signals

The **Cancellation Signals** type defines a Context whose execution can be interrupted through a command. In this case, the instruction follows its normal flow until, at some point in the code, it's told to stop. Here's an example implementation:

```go
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

Before explaining the `main()` function, let's first understand `executeFunction()`, since it's the one that receives instructions from the Context. Once it receives a `context.Context` parameter, it runs an infinite *loop* where, as soon as it receives the stop signal from the context, it prints “**Stopping code execution...**” and ends its execution with an explicit `return`. Otherwise, it keeps running and printing “**Running at [time]**”. The `select` statement works like a kind of *switch-case*, but applied to signals coming from ***channels***, which is the case with Contexts. As we can see, the stop signal in the code is given by the `ctx.Done()` instruction.

Back in the `main()` function, the first thing we do is create a Context with `context.Background()`. After that, we use the `context.WithCancel()` function, passing in our base context. It gives us back a new context and a second value we call `cancel`. That's essential for stopping the instructions tied to this context. While we run `executeFunction()` asynchronously, we wait three seconds and then force its cancellation with the `cancel()` instruction — yes, that same one we got from the context :) .

The result of running this will look something like the *log* below:

```text
Running at 2022-10-09 16:15:46.80042576 -0300 -03 m=+1.000598497
Running at 2022-10-09 16:15:47.801454038 -0300 -03 m=+2.001626779
Running at 2022-10-09 16:15:48.801876258 -0300 -03 m=+3.002048999
Stopping code execution...
```

## Deadline

As the name suggests, a **Deadline** Context caps how long an instruction or process is allowed to run. That lets us tell the application how long a given piece of code is allowed to take. There are two different functions for working with **Deadline**:

- **`context.WithDeadline()`** — sets a **fixed point in time**.
	- Example: the context has until 10 PM on October 9th, 2022 to finish executing.
- **`context.WithTimeout()`** — sets a **duration counted from the moment it's created**.
	- Example: the context has 4 minutes from now to finish executing.

### context.WithDeadline()

Let's take the same code from before and tweak a few parts:

```go
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

We create a new `deadline` variable by adding three seconds to the current time and pass it to `context.WithDeadline()`. This way, the `executeFunction()` call is interrupted once that three-second window has passed.

Running the code above produces output similar to this:

```text
Running at 2022-10-09 17:30:50.492897161 -0300 -03 m=+1.000190057
Running at 2022-10-09 17:30:51.493583512 -0300 -03 m=+2.000876359
Running at 2022-10-09 17:30:52.493694606 -0300 -03 m=+3.000987449
Running at 2022-10-09 17:30:53.493795753 -0300 -03 m=+4.001088530
Stopping code execution…
```

### context.WithTimeout()

We can use `context.WithTimeout()` to produce the same behavior. Just swap lines **11** and **12** for:

```go
deadline := 3 * time.Second
ctx, cancel := context.WithTimeout(ctx, deadline)
```

The difference from the previous code is that now we no longer need to calculate the current instant plus three seconds. The output is the same.

One interesting detail in this structure is that we also call `cancel()`, but with the `defer` keyword to make sure it runs last. Even though we're capping the execution time, **we can also cancel the instruction early at any point, overriding the time-limit rule**, just like explained in the **Cancellation Signals** section.

### Request-scoped value

Besides controlling execution time and stopping, Context can also pass **key-value** values down to child instructions. This concept matters because it **works regardless of whether the call to those instructions is synchronous or asynchronous**. These values are stored inside the context and are immutable. Let's walk through the code below, a synchronous example:

```go
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

We define the initial, empty context with `context.Background()`. After that, we create a new context from that initial one with `context.WithValue()`, adding a couple of sample values along the way. Since those values are stored in the Context, we can read them elsewhere in the program with `ctx.Value()`, passing in the matching key. If that key doesn't exist, the return value is `nil`. It's also possible to add new values to a context by calling `context.WithValue()` again, passing in the previous context and reassigning it to itself.

# Other scenarios

Context's use cases aren't limited to what's covered here. These days, Go libraries — standard or third-party — often require passing a Context into their functions. The goal of this post was to understand its fundamentals and common uses.

See you next time :)

## References

- [https://pkg.go.dev/context](https://pkg.go.dev/context)
- [https://www.digitalocean.com/community/tutorials/how-to-use-contexts-in-go](https://www.digitalocean.com/community/tutorials/how-to-use-contexts-in-go)
- [https://p.agnihotry.com/post/understanding_the_context_package_in_golang/](https://p.agnihotry.com/post/understanding_the_context_package_in_golang/)
- [https://www.youtube.com/watch?v=eGYZPUoH78c](https://www.youtube.com/watch?v=eGYZPUoH78c)
