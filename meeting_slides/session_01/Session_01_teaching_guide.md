# Session 1 teaching guide

180 minutes, including a 15-minute break. The slides use synthetic examples.

## Preparation

- Confirm current 2026 assessment, deadlines, and software expectations separately. The old grading slide was omitted because it conflicts with the 2025 syllabus.
- Ask students to install R, RStudio, and igraph before class.
- Share code/SNA_Practical_01_02.Rmd and its rendered HTML. Students without working R can work in pairs.
- Use the LaTeX presenter notes for timing, answers, and references. Activity answers follow the prompts.
- The directed advice convention is seeker → source. Keep this convention throughout.

## Scope

The class covers the relational perspective, network design, representations, degree, and density. Advanced centrality, degree distributions, graph-generating models, layout algorithms, and bipartite projections are deferred. Paths and components are discussed intuitively through reachability, without formal algorithms.

## Slide notes

### 1. Social Network Analysis

0–2 min. Welcome. This deck is designed for a 180-minute meeting including a 15-minute break. The advice networks are synthetic teaching examples.

### 2. Today’s learning goals

2–5 min. Explain that interpretation matters as much as calculation. Ask which outcome is least familiar.

### 3. Introductions

5–15 min. Keep introductions brief. With a large class, use pairs and collect a few examples.

### 4. The course ahead

15–18 min. Explain the progression. Do not present the 2025 assessment as confirmed 2026 policy. Confirm current assessment and deadlines separately before class.

### 5. Our three-hour session

18–20 min. Orient students to the break and practical work.

### 6. Who can reach a new opportunity?

20–23 min. Ask students to predict what individual-level data could miss. This is a hypothetical example, not an empirical causal claim.

### 7. Same actors, different relationships

23–28 min. Compare two graphs with six nodes and five edges each. Left has an isolate and a bridge; right is a connected path. Ask who could receive a message if it travels only along observed ties. Equal size and density do not imply equal reachability.

### 8. The relational perspective

28–32 min. A conventional table can store relational data too. The distinction is the substantive unit and dependence structure, not the file format. Mention that ties sharing actors may be dependent; independent-observation assumptions need care.

### 9. A network is a set of actors and ties

32–35 min. Use nodes/vertices and edges/ties as synonyms, then stick with nodes and ties. E is a set; m = |E| is its size.

### 10. Our running example: an advice network

35–40 min. Synthetic six-person research group. Initially treat a tie as a confirmed advice relationship without direction. A–B, A–C, B–C, C–D, D–E; F has no observed ties. Later introduce a distinct directed nomination version.

### 11. Weak ties and access to new information

40–45 min. Use C–D as a structural bridge in our undirected example. Tie strength has not yet been measured, so do not call it weak based on its position alone. Source: Granovetter (1973), The Strength of Weak Ties, https://doi.org/10.1086/225469. Avoid a universal claim that weak ties spread all information better.

### 12. The research question defines the network

45–49 min. This introduces the directed nomination version, not a claim that earlier undirected data encoded direction. Make clear that arrow direction must be stated.

### 13. Directed, undirected, and weighted ties

49–53 min. Friendship survey nominations may be directed, even if everyday friendship is described as mutual. Weighted ties can represent frequency, intensity, duration, or distance; meanings differ.

### 14. Arrow direction changes the interpretation

53–57 min. Directed version has A→B, A→C, B→C, C→D, D→E. Arrow means seeker→source. C is named by two people and names one source. Do not infer frequency from binary degree.

### 15. A network boundary is a research decision

57–61 min. Removing F raises undirected density from 5/15 to 5/10 without changing any observed edge. Explain this now, calculate it later. Distinguish whole-network and ego-network designs briefly.

### 16. No observed tie can mean several things

61–65 min. Missing is not automatically zero. Discuss one example of a missing central respondent. Explain that network data can expose relationships involving people who did not provide data themselves.

### 17. Activity: define a network study

65–75 min. Pairs: 2 min choose question, 5 min specify design, 3 min prepare explanation. Use hypothetical examples rather than collecting classmates’ sensitive nominations.

### 18. Discussion: would your data answer the question?

75–80 min. Invite two pairs. Challenge causal claims gently: a pattern of contact does not establish influence. Ask how they would protect identities and relational information.

### 19. Break

80–95 min. Resume with the six-node example.

### 20. One network, several representations

95–98 min. These are related representations, but a layout alone is not a complete data model and an edge list alone omits isolates.

### 21. Edge list and node list

98–102 min. Undirected version: store each pair once. A node table may contain attributes; retain all six actors, including F.

### 22. Adjacency matrix: the same undirected network

102–107 min. Rows and columns use the same node order. A_ij=1 if there is a tie. Undirected matrix is symmetric. Diagonal zeros assume no self-loops. Every undirected edge appears twice.

### 23. Activity: change the representation

107–115 min. 6 min work, 2 min compare. Directed answer is on the next slide. Check students preserve the all-zero row and column for F.

### 24. Answer: the directed advice matrix

115–120 min. Convention: row=sender (seeker), column=receiver (advice source). A→B occupies row A, column B. Row sums are out-degree; column sums are in-degree.

### 25. Degree counts incident ties

120–124 min. All examples here are simple binary graphs without loops. Strength sums weights and is a different measure. An isolate has degree zero; low positive degree does not mean isolation.

### 26. Density is the fraction of possible ties

124–128 min. These formulas assume at most one edge per eligible pair, no self-loops, and n≥2. They are not formulas for summing interaction weights. Density is undefined by these formulas for n<2.

### 27. Activity: describe the six-person group

128–135 min. Let students calculate before showing answers. Ask one pair to explain the denominator and another to interpret C’s directed degree.

### 28. Answer: degree, density, and the missing isolate

135–138 min. Undirected degrees sum to 10 = 2m. Directed in-degree and out-degree each sum to m=5. Omitting F raises density without adding a relationship.

### 29. What these measures can and cannot tell us

138–140 min. Return to the two networks at the start. Optional extension: mean degree = 2m/n = density × (n−1) for simple undirected networks. This is a relation between averages, not a claim about the full degree distribution.

### 30. R practical: build and inspect the network

140–143 min. Allow a fallback: students without working R pair with someone who has it. Notebook needs igraph only. Install packages before class where possible.

### 31. A minimal network in R

143–147 min. Explain why vertices=nodes is essential. Do not spend time on advanced visualization packages.

### 32. Practical task 1: check your answers

147–153 min. Six minutes. Expected: n=6, m=5, degree=(2,2,3,2,1,0), density=1/3. See notebook for commands and checks.

### 33. Practical task 2: change one relationship

153–160 min. Seven minutes. Answer: m=6, density=6/15=.4; E changes 1→2, F changes 0→1. Network becomes connected. Density alone does not express this qualitative change.

### 34. Practical task 3: direction and interpretation

160–166 min. Six minutes. C has highest in-degree=2; A highest out-degree=2. Reversing arrows preserves density and swaps in/out degree. Original graph has no E–F addition in this task.

### 35. One graph can have several layouts

166–170 min. Four minutes. Layout changes do not change adjacency, degree, or density. The fixed arrangement was chosen for teaching and does not encode geography.

### 36. Classic results need careful interpretation

170–173 min. Optional brief context rather than a new theory unit. Travers & Milgram (1969): 64 completed chains from 296 starters; mean 5.2 intermediaries in completed chains. This does not establish universal six-step reachability. https://snap.stanford.edu/class/cs224w-readings/travers69smallworld.pdf. Broido & Clauset (2019), Scale-free networks are rare: https://doi.org/10.1038/s41467-019-08746-5. Preferential attachment is one generative model, not established by a hub-shaped plot.

### 37. Exit question

173–177 min. Individual written response. Expected: an isolate may be missing; omitting it changes the denominator from 15 to 10 and raises density from .333 to .5. Five actors is consistent with the running example, but in a real dataset investigate rather than assume.

### 38. What you should now be able to do

177–180 min. Ask students to name one remaining uncertainty. Next class: paths, components, and graph structure.

### 39. Reading and sources

Reference slide, outside timed teaching. Granovetter https://doi.org/10.1086/225469; Travers & Milgram https://snap.stanford.edu/class/cs224w-readings/travers69smallworld.pdf; Broido & Clauset https://doi.org/10.1038/s41467-019-08746-5; Borgatti et al. https://doi.org/10.1126/science.1165821. Reworked from ADAIII_2025/meeting_slides/ADA_III_Meeting_01.pdf and the 2025 first-session notebook. All network data and diagrams in this deck are synthetic instructional examples.
