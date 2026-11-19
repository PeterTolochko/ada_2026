# Session 2: Connectivity, centrality, and social position

Three hours, including a 15-minute break. Uses the six-person synthetic advice network from session 1. Retains the first deck’s Beamer style and pagination-only footer.

## Teaching plan

| Minutes | Focus |
|---|---|
| 0–12 | Recall and running example |
| 12–42 | Vectors, transpose, multiplication, walk counts |
| 42–75 | Reachability, shortest paths, components, bridges |
| 75–90 | Break |
| 90–130 | Degree, distance-based centrality, betweenness, interpretation |
| 130–150 | Eigenvectors and PageRank |
| 150–167 | Build, inspect, edit, and plot graphs in igraph |
| 167–175 | First metric comparison and interpretation |
| 175–180 | Exit question and recap |

The reference slide and five appendix slides are outside the timed core. The PageRank linear system, Laplacian, structural equivalence, and shifted iteration are optional, not additional material to squeeze into the three hours.

## Preparation

- Students need igraph and the notebook `code/SNA_Practical_01_02.Rmd`. The HTML version supports reading without running R.
- Review row-source adjacency, summation notation, row/column vectors, and degree from session 1. No previous eigenvalue course is assumed.
- Use the construction, inspection, graph manipulation, and plotting sections before the measures. The “Add an alternative route: what changes?” section provides the B–D comparison. The complete combined workbook contains more material than one practical block.
- Leave the original graph visible during hand exercises. Student activities have separate answer slides.
- Arrow convention: row actor nominates column actor as advice source. This is not necessarily the direction in which advice or information travels.
- Check every interpretation against the tie definition. Centrality is not direct evidence of influence or causal power.

## Mathematical conventions

- Matrix powers count walks, not simple paths. R `%*%` is matrix multiplication; `^` is elementwise exponentiation.
- Distances are unweighted unless a separate positive cost is specified. `weights = NA` disables an accidental weight attribute in igraph.
- Full-graph harmonic normalisation uses n−1 = 5. Closeness examples explicitly use the connected five-person component.
- Betweenness is raw unless labelled normalised. Unordered endpoint pairs exclude the focal actor; unreachable pairs contribute zero.
- Eigenvector examples use the undirected graph, maximum score 1. Directed incoming prestige uses the transpose; it is not meaningful as positive-eigenvalue adjacency centrality on the acyclic nomination graph.
- PageRank uses a row-stochastic transition matrix, uniform rows for dangling nodes, a column probability vector, alpha = .85, and uniform teleportation.

## Slide notes

### 1. Social Network Analysis

0--2 min. Welcome. Build directly on the first class. All small networks are synthetic. The core session is 180 minutes including a 15-minute break. Appendix slides are optional.

### 2. What we will explain today

2--4 min. Explain that students need sums and matrix multiplication, not prior eigenvalue theory. Eigenvectors will be introduced through a repeated calculation.

### 3. Recall: the adjacency matrix

4--8 min. Ask what A times a column of ones does. Matrix-vector multiplication is a set of row sums here. Reintroduce transpose explicitly.

### 4. Our six-person network

8--12 min. Return to the advice graph from class 1. F is a member with no observed ties. Ask whether C and D play the same role. The graph has six nodes and five edges.

### 5. Vectors attach values to actors

12--15 min. Compute the B row by hand. This sum is not yet a probability or a diffusion model: it aggregates neighbour values. An actual process needs assumptions about timing and transmission.

### 6. Matrix-vector multiplication: a weighted sum

15--18 min. Use M for this separate three-node directed example to avoid confusing it with the main six-by-six A. M represents A to B, A to C, B to C. Explain dimensions: 3 by 3 times 3 by 1 gives 3 by 1.

### 7. Direction: receiving values versus sending values

18--21 min. Do not label Ax as forward transmission with row-source adjacency. For an undirected graph the operations coincide. Values are copied along ties in this example; mass is not conserved unless rows are normalised.

### 8. Exercise: follow the indices

21--25 min. Pairs, four minutes. Ask students to write one sum with explicit indices before calculating the whole vector.

### 9. Answer: values arriving along directed ties

25--27 min. Keep the vector values distinct from degrees. This is an algebraic aggregation, not observed information flow.

### 10. From students to instructors through courses

27--28 min. Adapted from the 2025 Session 2 student-course-professor and numerical examples. These counts describe scheduled exposure, not actual attendance or learning. The shared order X, Y, Z matters.

### 11. A complete matrix product, entry by entry

28--30 min. Ask why B gets none of the two sessions with U in X. The product has two student rows and two instructor columns. The three courses are the matching dimension. This is the 2025 numerical product with a concrete interpretation.

### 12. Matrix multiplication links two steps

30--31 min. When both steps use the same adjacency matrix, the product is A squared. Use a binary unweighted graph. Matrix powers with weighted entries sum products of weights, not unweighted walk counts.

### 13. Two steps in a three-person network

31--32 min. Adapted from the three-node chain in the 2025 deck. Point to the top-right entry and centre diagonal entry. In the six-person graph the same operation counts A--C--D.

### 14. Walks, paths, and matrix powers

32--35 min. Use arrows here to show the order of traversal, not directed edges in the undirected graph. In a directed network diagonal A squared counts reciprocal return walks and need not equal degree.

### 15. Exercise: two-step counts

35--39 min. Four minutes, individual then compare with a neighbour. Expected 2, 1, 0. A reaches E in three steps.

### 16. Answer: what a zero does and does not mean

39--42 min. For this graph A cubed at A,E is exactly one. Distinguish no tie, no walk of a particular length, and unreachable.

### 17. Reachability from matrix powers

42--45 min. This is a statement for nonnegative binary adjacency, with reachability between distinct actors. Do not recommend computing huge matrix powers for large sparse networks: counts grow and numerical overflow becomes possible.

### 18. Shortest paths and geodesic distance

45--48 min. A shortest unweighted walk between distinct actors is a path: a repeated cycle could be removed to shorten it.

### 19. The distance matrix

48--51 min. Use Delta to avoid confusing distance matrix with degree diagonal D in the appendix. Ask students to read C,E and E,C, then F,A. Infinity is not a missing-data code.

### 20. Connected components

51--54 min. Maximal means no further node can be added while preserving connection to the set. An isolate is a component of size one. Our node order already groups components, with a five-by-five block and a zero block.

### 21. Connectivity in a directed graph

54--58 min. The graph is a directed acyclic nomination network. F forms its own weak and strong component. Advice-seeker to source arrows are nomination direction, not guaranteed direction of advice transmission.

### 22. Bridges and articulation points

58--62 min. Count all components, including F. Removing C creates AB, DE, and F: three instead of two. Removing D creates ABC, E, and F. E is a leaf, but not an articulation point. Definitions here are for the undirected graph.

### 23. Exercise: alternative routes

62--68 min. Six minutes in pairs, including a quick check with another pair. Ask students to distinguish edge removal from node removal.

### 24. Answer: redundancy changes social position

68--75 min. Debrief for seven minutes, drawing the two routes. This anticipates the fractional counting rule in betweenness. B degree rises from two to three and D from two to three. F remains isolated.

### 25. Break

75--90 min. Resume at minute 90. Ask students to keep the original graph handy for the centrality calculations.

### 26. Degree and its matrix form

90--92 min. Brief retrieval rather than reteaching class 1. These are binary loopless degree formulas; weights require strength.

### 27. Who can reach the group in fewer steps?

92--95 min. Explain the numerator four: four other actors. The score is one divided by the average distance. Ask which actor might reach the connected group with fewer handoffs if each tie allows one handoff.

### 28. What should we do with F?

95--97 min. Use F to motivate an alternative rather than introduce an infinity calculation. Software conventions for closeness differ. The notebook gives the exact formulas.

### 29. Nearby actors count more

97--100 min. Ask students to say the rule in words before applying it. The formula is the mean reciprocal distance to the other actors; unreachable actors contribute zero.

### 30. Exercise: compare distance-based positions

100--104 min. Four minutes. Require the common denominator five. Tie meanings and model of travel still determine whether this structural advantage is relevant.

### 31. Answer: harmonic centrality

104--106 min. Explain that harmonic centrality differs from closeness even in connected graphs: sum of inverses versus inverse sum. Scores should not be numerically interchanged.

### 32. Who is on the route between others?

106--109 min. Ask students to trace the path and identify intermediaries before counting other pairs. Unreachable pairs contribute zero. The notebook includes the formal definition.

### 33. Counting C's betweenness

109--112 min. D lies between A,E; B,E; and C,E. A,B are endpoints for some routes but never internal on a shortest route. Count explicitly rather than equating bridges with scores.

### 34. Equal shortest paths split the contribution

112--114 min. Make clear this separate diamond graph illustrates counting only; node labels differ from the main graph. Avoid reporting U or V total betweenness as one half without including all pairs.

### 35. What does a betweenness score of 4 mean?

114--116 min. The denominator is the number of unordered pairs excluding the focal actor. The exercise keeps F in the population.

### 36. Different measures describe different positions

116--119 min. Values checked in igraph. Different columns have different scales; compare actors within columns, not numerical values across columns.

### 37. Which position matters for your question?

119--122 min. Three-minute discussion. Require students to name a tie definition and a plausible process. Prestige as receiving nominations is not identical to contact volume.

### 38. Exercise: choose the measure before calculating

122--124 min. Ask students to choose based on the actual question before seeing scores. Ask students to apply the measures just introduced and explain why direction matters for nominations.

### 39. Answer: a research question determines a measure

124--125 min. Accept bridge or articulation analysis as a complementary answer to question 2, especially if students interpret connects as indispensability rather than participation.

### 40. Weights can mean strength or distance

125--130 min. Distance-based igraph measures use the weight attribute by default when present. PageRank and eigenvector centrality treat positive weights as strengths instead. Never blindly reuse interaction counts as distances. Sources: igraph betweenness, harmonic centrality, and PageRank documentation.

### 41. Same number of contacts, different contacts

130--133 min. Contrast this with betweenness: D can be a broker even though A has more highly scored contacts. Ask which actor might score higher and why.

### 42. Eigenvectors: multiplication preserves a line

133--134 min. Define the equation, then immediately use the visual on the next slide. Negative eigenvalues reverse direction but preserve the eigenvector line. Centrality uses the nonnegative leading scores rather than an arbitrary eigenvector. In our graph the isolate has score zero.

### 43. A geometric example of an eigenvector

134--136 min. M is an illustrative coordinate transformation, not the observed network adjacency. For v, the slope changes from 1 to one half. For u, the horizontal direction is preserved and the length doubles. In an n-actor network the vector has n coordinates; the same equation applies.

### 44. Give everyone a score, then look at their neighbours

136--139 min. Show the unscaled second round before discussing rescaling. This follows the 2025 repeated-neighbour-update example. Ordinary iteration can oscillate on some graphs; see the appendix.

### 45. How do we know the scores have settled?

139--141 min. The notebook checks the numerical equation. Emphasise relative scores; 0.82 is not a probability or a share of all ties.

### 46. Who is nominating whom?

141--143 min. Recall the earlier transpose example. Directed adjacency eigenvector centrality does not give a useful positive-eigenvalue ranking on this acyclic network; that detail is optional.

### 47. PageRank: follow the nominations

143--144 min. Make clear that this is a model of following nominations, not a claim that advice itself flows from seeker to source.

### 48. A worked PageRank transition row

144--146 min. Read columns in actor order A--F. Ask where one unit at A goes before introducing teleportation: one half to B and one half to C. Uniform dangling redistribution is built into P; teleportation is a separate operation applied to every row. With teleportation, A's final transition probabilities are .45 each to B and C and .025 each to A, D, E, F. They sum to one.

### 49. Why PageRank can disagree with in-degree

146--149 min. Use the diagram from directed connectivity. The notebook gives the scores and exact calculation. Explain that a different network or random-jump rule can change the rankings.

### 50. Linear algebra connects the measures

149--150 min. One-minute recap. Avoid claiming all measures are simple matrix powers: betweenness also needs counts and participation of shortest routes.

### 51. igraph practical: start with the data

150--152 min. Load igraph and run the running example. Keep g as the baseline. Work through the notebook's in-class blocks; extra import formats and cleaning examples are for reference afterward.

### 52. From tables and matrices to graphs

152--159 min. Use the notebook to inspect node and edge attributes. Point out that V and E select vertices and edges. Match row and column order before importing a matrix. Compare the two graphs by their named adjacency matrices.

### 53. Edit a copy and keep the layout fixed

159--167 min. Show adding and deleting an edge, selecting an induced subgraph, and retaining the baseline graph. Use the notebook's team colours and contact widths to distinguish attributes from layout. Reuse coordinates only when the vertex order and set match.

### 54. Perturbation: add one alternative route

167--172 min. Use the notebook’s “Add an alternative route: what changes?” section. C degree remains three; raw betweenness falls four to one. B becomes one, D remains three. Bridge and articulation-point status give a separate view of indispensability.

### 55. Interpret the results as a researcher

172--175 min. Pairs compare interpretations; discuss one example as a class. Do not require every pair to finish the PageRank extension within the session.

### 56. Exit question

175--178 min. Three minutes individually. Use answers to assess whether students distinguish direct ties, alternative routes, and repeated actors.

### 57. What you should take away

178--180 min. 178--180: exit answer: the new edge provides an alternative route bypassing the actor; matrix multiplication permits repeated actors, such as A-B-A. Next class: collecting, preparing, and visualising empirical network data.

### 58. Reading and references

Reference slide outside the timed session. All plotted networks and numerical examples are synthetic. The notebook includes reproducible calculations and checks.

### 59. Appendix: PageRank as a linear system

Optional. Show that an n-by-n matrix multiplies an n-by-one vector on both sides. Notebook solves this system and compares with igraph. It is not necessary to compute an explicit matrix inverse. Source: https://r.igraph.org/reference/page_rank.html.

### 60. Appendix: the graph Laplacian

Optional extension, not part of the 180 minutes. For the six-node graph there are two zero eigenvalues. Use D for the degree diagonal and Delta for distances. This is for undirected graphs with nonnegative weights.

### 61. Appendix: a quadratic form measures disagreement

Optional. Binary values x=(0,0,0,1,1,0) give energy one because only C-D crosses between values. This connects later to community detection without deriving a clustering algorithm.

### 62. Appendix: structural equivalence

Optional sociological extension. The pair-excluded definition accommodates adjacent actors; strict full-row equality would fail due to the diagonal and mutual edge entries. Distinguish structural equivalence from looser role or regular equivalence.

### 63. Appendix: a stable power iteration

Optional extension. This is a numerical device, not a substantive claim that the observed graph has self-ties. With the full disconnected six-node graph, the nontrivial component still dominates the isolate. Notebook uses the shift as an optional robustness check.
