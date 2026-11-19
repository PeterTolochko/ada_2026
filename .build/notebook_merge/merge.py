from pathlib import Path
import re
base=Path('code')
a=(base/'Lecture1_SNA.Rmd').read_text()
b=(base/'Lecture2_SNA.Rmd').read_text()
def cut(src,start,end=None):
    i=src.index(start)
    return src[i:src.index(end,i+len(start))] if end else src[i:]
def rename_heading(src,old,new):
    return src.replace(old,new,1)
parts=[]
parts.append('''---
title: "Social Network Analysis: Practical Workbook"
subtitle: "Network foundations, igraph, connectivity, and centrality"
author: "Petro Tolochko"
output:
  html_document:
    toc: true
    toc_float: true
    toc_depth: 2
    number_sections: true
    code_folding: show
    theme: readable
---

```{r setup, include=FALSE}
knitr::opts_chunk$set(fig.width = 8, fig.height = 4.5,
                      fig.align = "center", collapse = TRUE, comment = "#>")
```

# Getting started

This workbook brings together the practical material for the first two lectures. It starts with defining a network and using igraph, then moves to degree, density, connectivity, and centrality. The final sections contain optional mathematical extensions.

Run the code from top to bottom: later examples use objects created earlier. Predict the output before running a calculation, and expand the answer boxes after trying each question.

We use **igraph** and base R. Install igraph once, if needed:

```{r install, eval=FALSE}
install.packages("igraph")
```

Load the package whenever you start a new R session:

```{r packages}
library(igraph)
```

The examples are synthetic. Our main example is an undirected network with six actors and five ties. Separate examples introduce directed nominations, weights, and other data structures.

''')
# Keep the original substantive question and one baseline graph.
intro=cut(a,'# A research question becomes network data','```{r plot}')
intro=intro.replace('`from` and `to` are column names required for this edge-list convention.', 'The first two columns contain the endpoints; we call them `from` and `to`.')
intro += '\nWe keep `g` as the original graph. Give edited graphs different names so that the examples can be compared.\n\n'
parts.append(intro)
# igraph object intro, using basic column assignments rather than transform().
obj=cut(b,'## Build from node and edge tables','## Build from a square adjacency matrix')
obj=obj.replace('## Build from node and edge tables','# Get to know an igraph object\n\n## Actor and tie attributes',1)
obj=obj.replace('roster <- transform(nodes, team = c("Red", "Red", "Red", "Blue", "Blue", "Blue"))\nties <- transform(edges, contacts = c(3, 2, 4, 1, 2))','roster <- nodes\nroster$team <- c("Red", "Red", "Red", "Blue", "Blue", "Blue")\nties <- edges\nties$contacts <- c(3, 2, 4, 1, 2)')
parts.append(obj)
# Explain adjacency once and keep the second notebook's reverse import and count example.
adj=cut(a,'# Task 1: connect the graph to its matrix','## Degree is a row sum')
adj=adj.replace('# Task 1: connect the graph to its matrix','# Represent a network as a matrix')
adj=adj.replace('isSymmetric(A)\nall(diag(A) == 0)\nsum(A)', 'A\nt(A)\nsum(A)')
parts.append(adj)
parts.append(cut(b,'## Build from a square adjacency matrix','## Edit without losing the original').replace('## Build from a square adjacency matrix','## Create a graph from the matrix',1))
# Graph manipulation.
parts.append(cut(b,'## Edit without losing the original','## Plot and compare').replace('## Edit without losing the original','# Manipulate graphs',1))
# One plotting helper that supports the retained layout exercise.
parts.append('''# Visualise the network

Start with a simple plot:

```{r plot-basic}
plot(g, vertex.color = "lavender", vertex.label.color = "black",
     main = "Six-person advice network")
```

**Discuss:** what does this picture tell us about F? What would we need to know before interpreting F as socially isolated outside this research group?

## Layouts position the actors

A layout is a table of coordinates, with one row for each actor in the graph's order. We will reuse these coordinates to make our comparisons easier to read.

```{r fixed-layout}
fixed_layout <- rbind(c(0, 1), c(2, 1), c(1, 0),
                      c(3.8, 0), c(3.8, 1), c(5.6, 0))
plot(g, layout = fixed_layout, vertex.size = 28,
     vertex.color = "lavender", vertex.label.color = "black")
```

The short function below stores these plotting choices so we do not need to repeat them in every example. Its arguments are the graph, a title, and a layout.

```{r plotting-helper}
plot_advice <- function(network, main = "", layout = fixed_layout) {
  plot(network, layout = layout, main = main,
       vertex.size = 28, vertex.color = "lavender",
       vertex.label.color = "black", vertex.label.cex = 1.2,
       edge.color = "slategray", edge.arrow.size = 0.5)
}
```

''')
plots=cut(b,'## Plot and compare','## Other inputs and cleaning decisions')
plots=plots.replace('## Plot and compare','## Colours, widths, and consistent comparisons',1)
plots=plots.replace('main = "After adding B–D"','main = "After adding B-D"')
parts.append(plots)
layouts=cut(a,'# Extension: layouts change the picture','# Your own network question').replace('# Extension: layouts change the picture','## Same graph, different layouts',1)
parts.append(layouts)
# Other formats and cleaning examples remain reference content without timing labels.
other=cut(b,'## Other inputs and cleaning decisions','# First metric comparison')
other=other.replace('## Other inputs and cleaning decisions','# Other data structures and cleaning decisions',1)
x=other.index('**Direction changes meaning:**')
y=other.index('**Save for reuse:**',x)
other=other[:x]+other[y:]
parts.append(other)
# Degree and density, with the missing-isolate exercise directly after density.
parts.append(cut(a,'## Degree is a row sum','# Task 2: calculate density').replace('## Degree is a row sum','# Degree and average degree',1)+'''\n## Degree as a share of possible neighbours

An actor can have at most $n-1$ neighbours when self-ties are excluded. Normalised degree is the share of those possible neighbours that are connected:

$$C_D(i)=\\frac{k_i}{n-1}.$$

```{r normalised-degree}
data.frame(node = V(g)$name, degree = degree(g),
           share_of_possible_neighbours = degree(g) / (vcount(g) - 1))
```

C has three neighbours out of five possible, so its normalised degree is 0.6. This rescales degree; it does not measure the quality of the advice C gives.

''')
parts.append(cut(a,'# Task 2: calculate density','# Task 3: direction changes interpretation').replace('# Task 2: calculate density','# Density and adding a relationship',1))
parts.append(cut(a,'# Task 4: the missing isolate','# Extension: interaction counts and weighted ties').replace('# Task 4: the missing isolate','# What happens when an isolate is omitted?',1).replace('**Exit question:**','**Explain:**'))
# Avoid an unnecessary lapply abstraction for the basic-R audience.
parts.append('''## Density and network size

For simple undirected networks,

$$D=\\frac{2m}{n(n-1)}=\\frac{\\bar{k}}{n-1}.$$

A cycle connects each actor to two neighbours. Create cycles of different sizes and compare their mean degrees and densities:

```{r density-size}
cycle_6 <- make_ring(6, directed = FALSE)
cycle_20 <- make_ring(20, directed = FALSE)
cycle_100 <- make_ring(100, directed = FALSE)
data.frame(
  nodes = c(6, 20, 100),
  mean_degree = c(mean(degree(cycle_6)), mean(degree(cycle_20)),
                  mean(degree(cycle_100))),
  density = c(edge_density(cycle_6), edge_density(cycle_20),
              edge_density(cycle_100))
)
```

**Discuss:** each actor has two contacts in every graph. Why does density fall? What would be misleading about describing the largest group as having fewer contacts per person?

''')
# One directed graph definition; all future calculations reuse it.
direct=cut(a,'# Task 3: direction changes interpretation','# Task 4: the missing isolate').replace('# Task 3: direction changes interpretation','# Directed nominations: who names whom?',1)
direct=direct.replace('A_dir\n```','A_dir\nneighbors(g_dir, "C", mode = "in")\nneighbors(g_dir, "C", mode = "out")\n```',1)
parts.append(direct)
parts.append(cut(a,'# Extension: interaction counts and weighted ties','# Extension: density depends on network size').replace('# Extension: interaction counts and weighted ties','# Weighted ties: partners versus interactions',1))
# Matrix-vector and matrix-matrix examples after students can construct/inspect graphs.
walks=cut(b,'# Task 1: matrix multiplication and walks','# Task 2: distances and components').replace('# Task 1: matrix multiplication and walks','# Matrix multiplication and indirect connections',1)
walks=walks.replace('## Two-step walks','''## Combine two tables: students, courses, and instructors

Suppose students A and B take courses X, Y, and Z. Matrix `M` records enrolment; matrix `N` counts the teaching sessions that instructors U and V give in each course.

```{r composition-data}
M <- matrix(c(1, 1, 0,
              0, 1, 1), nrow = 2, byrow = TRUE,
            dimnames = list(c("A", "B"), c("X", "Y", "Z")))
N <- matrix(c(2, 0,
              1, 3,
              0, 1), nrow = 3, byrow = TRUE,
            dimnames = list(c("X", "Y", "Z"), c("U", "V")))
M
N
```

To find A's scheduled exposure to U, take A's row from `M` and U's column from `N`. Match entries course by course, multiply, and add:

- A and U: $1\\times2+1\\times1+0\\times0=3$.
- A and V: $1\\times0+1\\times3+0\\times1=3$.
- B and U: $0\\times2+1\\times1+1\\times0=1$.
- B and V: $0\\times0+1\\times3+1\\times1=4$.

```{r composition-product}
M %*% N
```

The result is a student-by-instructor table. The course columns in `M` must match the course rows in `N`, including their order. This describes scheduled exposure, not actual attendance or learning.

## Two-step walks''',1)
parts.append(walks)
parts.append(cut(b,'# Task 2: distances and components','# Task 3: compare centrality measures').replace('# Task 2: distances and components','# Distances, components, and bridges',1))
# Unique deletion example complements the route-adding task.
bridge=cut(a,'## Coordination and bottlenecks','## Political discussion across groups')
bridge=bridge.replace('## Coordination and bottlenecks','## Remove a tie: which deletion splits the group?',1)
bridge=bridge.replace('```{r bridges}','```{r bridge-deletions}')
parts.append(bridge)
# Directed connectivity should be adjacent to undirected components, not hidden after PageRank.
parts.append(cut(b,'## Directed connectivity','## A weighted shortest-path example'))
# Centrality from intuitive descriptions, with explanation before metric table.
central=cut(b,'# Task 3: compare centrality measures','# Task 4: add an alternative route').replace('# Task 3: compare centrality measures','# Compare centrality measures',1)
i=central.index('## Why we avoid full-graph conventional closeness here')
close=central[i:].replace('## Why we avoid full-graph conventional closeness here','## Closeness: fewer steps to everyone else',1)
central=central[:i]
central=central.replace('## Harmonic centrality from the distance matrix','''## Harmonic centrality: give more credit to nearby actors

A direct neighbour contributes 1, an actor two steps away contributes 1/2, and an unreachable actor contributes zero. Add these contributions and divide by the number of other actors.''',1)
central=central.replace('Betweenness counts participation in shortest paths, splitting credit if several equally short paths exist:', 'Betweenness asks who sits on shortest routes between other actors. On the route A–C–D–E, C and D each receive credit for connecting A to E. Endpoints do not receive credit for that pair. If there are two equally short routes, actors on each route share the credit. The formula adds these contributions:')
central=central.replace('```{r centrality-table}', '''### Eigenvector centrality: whom are you connected to?

A and D each have two contacts. A knows B and C, who both have several contacts. D knows C and E, and E has only one contact. Eigenvector centrality gives more credit for being connected to actors who themselves score highly.

The table below puts these different ideas side by side.

```{r centrality-table}''')
central=central.replace('## Betweenness and eigenvector scores','## Betweenness: participation in shortest routes',1)
# Put closeness before harmonic; keep formulas and calculations in their own logical order.
central=central.replace('# Compare centrality measures\n\n','# Compare centrality measures\n\n'+close+'\n',1)
parts.append(central)
pert=cut(b,'# Task 4: add an alternative route','# Worked extension: eigenvectors and recursive scores').replace('# Task 4: add an alternative route','# Add an alternative route: what changes?',1)
pert=pert.replace('comparison <- data.frame(', 'route_comparison <- data.frame(').replace('knitr::kable(comparison,', 'knitr::kable(route_comparison,')
parts.append(pert)
# Political example retained without conflating nominations and discussion.
parts.append(cut(a,'## Political discussion across groups','# Extension: layouts change the picture').replace('## Political discussion across groups','# Apply the ideas: discussion across groups',1))
# PageRank use first, derivation after it.
parts.append('''# PageRank: following nominations

In-degree counts how many people name an actor as an advice source. PageRank also considers where the nominations come from and how attention is shared across outgoing ties.

Imagine moving through `g_dir` by following nomination arrows. At each actor, choose one of their outgoing nominations. Occasionally jump to a random actor. PageRank describes where this process spends its time.

```{r pagerank-interpretation}
page_scores <- page_rank(g_dir, damping = 0.85, weights = NA)$vector
data.frame(node = V(g_dir)$name,
           incoming_nominations = degree(g_dir, mode = "in"),
           PageRank = round(page_scores, 3))
```

**Interpret:** C has the highest in-degree, but E has the highest PageRank. Following the arrows can take you from A or B through C, then D, then E. Why does this let E receive attention despite having only one incoming nomination? Does this prove that E controls communication?

''')
parts.append(cut(b,'# Worked extension: eigenvectors and recursive scores','# Worked extension: directed prestige and PageRank').replace('# Worked extension: eigenvectors and recursive scores','# Optional mathematics: recursive scores and eigenvectors',1))
pr=cut(b,'# Worked extension: directed prestige and PageRank','# Optional exercises').replace('# Worked extension: directed prestige and PageRank','# Optional mathematics: transpose and PageRank',1)
pr=pr.replace('g_dir <- graph_from_data_frame(edges, directed = TRUE, vertices = nodes)\nA_dir <- as_adjacency_matrix(g_dir, sparse = FALSE)\n','')
parts.append(pr)
weighted=cut(b,'## A weighted shortest-path example','## The Laplacian and connected components')
weighted=weighted.replace('## A weighted shortest-path example','# Optional example: weights as distances',1).replace('weighted_edges','cost_edges').replace('g_weighted','g_costs')
parts.append(weighted)
lap=cut(b,'## The Laplacian and connected components')
lap=lap.replace('## The Laplacian and connected components','# Optional mathematics: the Laplacian',1)
parts.append(lap)
parts.append(cut(a,'# Your own network question'))
# Prefix each chunk to ensure no collisions across original sources.
text='\n'.join(parts)
seen=set()
def chunk(match):
    name=match.group(1)
    if name in seen:
        n=2
        while f'{name}-{n}' in seen:n+=1
        name=f'{name}-{n}'
    seen.add(name)
    return '```{r '+name
text=re.sub(r'```\{r ([A-Za-z0-9_-]+)',chunk,text)
# The audience needs readable output, not boolean assertions or formal tests.
assert 'stopifnot' not in text
assert not re.search(r'(?i)in class|after class|\d+ minutes|https?://',text)
(base/'SNA_Practical_01_02.Rmd').write_text(text)
print('Merged source:',len(text.splitlines()),'lines;',len(seen),'unique chunks')
