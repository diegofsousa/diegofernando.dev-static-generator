title: [PT] Padrão Abstract Factory aplicado à diferentes implementações de redimensionamento de imagens
date: 2020-09-20 18:42
author: diego
tags: design pattern, java, gof, padrão, abstract fatory
slug: padrao-abstract-factory-aplicado-a-redimensionamento-de-imagens
og_image: assets/images/factory.webp

O **Abstract Factory** é um importante padrão de projeto do tipo criacional que permite criar famílias de objetos relacionados sem precisar especificar as classes concretas. Este padrão é o primeiro descrito no livro Design Patterns do **GoF**. Conhecer a intuito por trás da criação desses padrões é bastante válido para entender os designs de software mais atuais.

Os objetos ou produtos do problema de design que iremos abordar neste estudo, são três tipos de redimensionamento de imagens. Nas duas primeiras, usaremos a biblioteca nativa **AWT** com sua implementação mais comum. Já na última, usaremos uma abordagem com `getScaledInstance`, da mesma biblioteca. A seguir, um resumo:

- **ImageGraphics2D**: Uma implementação mais comum usando recursos do AWT. Coletamos uma imagem de entrada, e geramos uma imagem de saída.
- **ImageGraphics2DWithRendering**: A mesma estratégia da implementação anterior, porém usamos uma abordagem de renderização com interpolação bilinear.
- **ImageScaledInstance**: Usando o método `getScaledInstance` ao invés da implementação tradicional da biblioteca.

Dessa forma, temos como atributos variáveis entre a família de objetos: a imagem, a largura alvo e a altura alvo. Esses valores podem ser passados onde toda estrutura é chamada. Nesse caso, como é um exemplo, podemos interagir com a fábrica pelo método main. Não especificarei os detalhes de construção de todas as classes, mas deixarei o link da implementação no GitHub. O diagrama de classes aplicado à temática proposta fica assim:

![Banner de divulgação](/assets/images/abstract-factory-diagram.jpeg)*Diagrama de Classe do padrão Abstract Factory aplicado.*

As chamadas do método main para a implementação podem ser desenvolvidas da seguinte maneira:

```java

package dev.diegofernando.imagetest;

import dev.diegofernando.imagetest.factory.ConcreteImageFactory;
import dev.diegofernando.imagetest.factory.Image;
import dev.diegofernando.imagetest.factory.ImageFactory;
import dev.diegofernando.imagetest.util.ImageResourceUtil;

import java.awt.image.BufferedImage;

/**
 * @author Diego Fernando
 * @since 07/09/2020
 */

public class Main {
    public static void main(String[] args){
        BufferedImage image = ImageResourceUtil.getImageFromPath("image.jpg");

        ImageFactory imageFactory = new ConcreteImageFactory();

        Image graphics2dImage = imageFactory.resizeWithGraphics2D(image, 200, 200);
        Image scaledInstanceImage = imageFactory.resizeWithScaledInstance(image, 200, 200);
        Image graphics2dRenderedImage = imageFactory.resizeWithGraphics2DRendered(image, 200, 200);

        graphics2dImage.resize();
        scaledInstanceImage.resize();
        graphics2dRenderedImage.resize();
    }
}
```

Essa abordagem tem alguns prós e contras. O benefício de implementar essa estrutura é a certeza que todos os produtos que vêm da fábrica estão relacionados e são compatíveis entre si. Com o baixo acoplamento, fica fácil introduzir novas variações no produto sem interferir no código do cliente tornando a manutenção facilitada. O ponto ruim da abordagem é a quantidade de código incluindo novas classes e interfaces, o que pode confundir o desenvolvedor no início.