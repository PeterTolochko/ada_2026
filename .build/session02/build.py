from pathlib import Path
import json
root=Path.cwd()
old=(root/'meeting_slides/ADA_III_Meeting_01.tex').read_text()
preamble=old.split(r'\begin{document}')[0].replace('Session 1: Relationships as data','Session 2: Connectivity, centrality, and social position')
preamble=preamble.replace(r'\usepackage{amsmath,',r'\usepackage{amssymb,amsmath,')
preamble+=r'''
\newcommand{\ones}{\mathbf{1}}
\newcommand{\Atoy}{\begin{pmatrix}0&1&1&0&0&0\\1&0&1&0&0&0\\1&1&0&1&0&0\\0&0&1&0&1&0\\0&0&0&1&0&0\\0&0&0&0&0&0\end{pmatrix}}
\newcommand{\disto}{\begin{pmatrix}0&1&1&2&3&\infty\\1&0&1&2&3&\infty\\1&1&0&1&2&\infty\\2&2&1&0&1&\infty\\3&3&2&1&0&\infty\\\infty&\infty&\infty&\infty&\infty&0\end{pmatrix}}
'''
slides=[]
def add(title,body,note,minutes=None,activity=None,fragile=False,appendix=False):
 slides.append(dict(title=title,body=body,note=note,minutes=minutes,activity=activity,fragile=fragile,appendix=appendix))
add('Social Network Analysis',r'\titlepage','Welcome. Build directly on the first class. All small networks are synthetic. The core session is 180 minutes including a 15-minute break. Appendix slides are optional.',(0,2))
add('What we will explain today',r'''\begin{itemize}
\item How matrix multiplication describes indirect connections.
\medskip\item How connectivity changes the meaning of centrality.
\medskip\item Why degree, reach, brokerage, and prestige give different rankings.
\medskip\item How to calculate and check these measures in R.
\end{itemize}''','Explain that students need sums and matrix multiplication, not prior eigenvalue theory. Eigenvectors will be introduced through a repeated calculation.',(2,4))
add('Recall: the adjacency matrix',r'''With rows as senders and columns as receivers,
\[A_{ij}=1\text{ if }i\to j,\qquad A_{ij}=0\text{ otherwise.}\]
\[\mathbf{k}^{\mathrm{out}}=A\ones,\qquad
\mathbf{k}^{\mathrm{in}}=A^{\mathsf T}\ones.\]
\begin{itemize}
\item $\ones$ is a column vector of $n$ ones.
\item In an undirected graph, $A=A^{\mathsf T}$.
\item The order of actors must agree in every matrix and vector.
\end{itemize}''','Ask what A times a column of ones does. Matrix-vector multiplication is a set of row sums here. Reintroduce transpose explicitly.',(4,8))
add('Our six-person network',r'''\begin{columns}[c]
\column{.54\textwidth}\centering\network{A/B,A/C,B/C,C/D,D/E}
\column{.43\textwidth}\[A=\Atoy\]
\end{columns}\medskip
Node order: A, B, C, D, E, F. Ties are undirected unless stated otherwise.''','Return to the advice graph from class 1. F is a member with no observed ties. Ask whether C and D play the same role. The graph has six nodes and five edges.',(8,12))
add('Vectors attach values to actors',r'''Let $x_i$ be an attribute of actor $i$, such as an indicator of receiving information.
\[\mathbf{x}=\begin{pmatrix}1\\0\\0\\0\\0\\0\end{pmatrix},\qquad
A\mathbf{x}=\begin{pmatrix}0\\1\\1\\0\\0\\0\end{pmatrix}.\]
\begin{itemize}
\item Only A has value 1 initially.
\item $(A\mathbf{x})_i=\sum_j A_{ij}x_j$: add the values of $i$'s neighbours.
\end{itemize}''','Compute the B row by hand. This sum is not yet a probability or a diffusion model: it aggregates neighbour values. An actual process needs assumptions about timing and transmission.',(12,15))
add('Matrix-vector multiplication: a weighted sum',r'''For three actors, consider
\[M=\begin{pmatrix}0&1&1\\0&0&1\\0&0&0\end{pmatrix},\qquad
\mathbf{x}=\begin{pmatrix}1\\2\\4\end{pmatrix}.\]
\[M\mathbf{x}=\begin{pmatrix}0\times1+1\times2+1\times4\\0\times1+0\times2+1\times4\\0\times1+0\times2+0\times4\end{pmatrix}
=\begin{pmatrix}6\\4\\0\end{pmatrix}.\]
Rows of $M$ select the values to sum. The result is another actor-level vector.''','Use M for this separate three-node directed example to avoid confusing it with the main six-by-six A. M represents A to B, A to C, B to C. Explain dimensions: 3 by 3 times 3 by 1 gives 3 by 1.',(15,18))
add('Direction: receiving values versus sending values',r'''For $A_{ij}=1$ when $i\to j$,
\[(A\mathbf{x})_i=\sum_j A_{ij}x_j
\quad\text{aggregates values of }i\text{'s outgoing neighbours}.\]
If each sender passes its value along every outgoing tie,
\[\mathbf{y}=A^{\mathsf T}\mathbf{x},\qquad
 y_j=\sum_i A_{ij}x_i.\]
\textbf{The transpose matters:} collecting neighbour attributes and sending values through ties are different operations.''','Do not label Ax as forward transmission with row-source adjacency. For an undirected graph the operations coincide. Values are copied along ties in this example; mass is not conserved unless rows are normalised.',(18,21))
add('Exercise: follow the indices',r'''Use the three-actor matrix
\[M=\begin{pmatrix}0&1&1\\0&0&1\\0&0&0\end{pmatrix},\qquad
\mathbf{x}=\begin{pmatrix}1\\2\\4\end{pmatrix}.\]
\begin{enumerate}
\item Calculate $M^{\mathsf T}\mathbf{x}$.
\item Which actor receives values from two senders?
\item Why is the result different from $M\mathbf{x}$?
\end{enumerate}''','Pairs, four minutes. Ask students to write one sum with explicit indices before calculating the whole vector.',(21,25),'PAIRS: 4 MINUTES')
add('Answer: values arriving along directed ties',r'''\[M^{\mathsf T}\mathbf{x}
=\begin{pmatrix}0&0&0\\1&0&0\\1&1&0\end{pmatrix}
\begin{pmatrix}1\\2\\4\end{pmatrix}
=\begin{pmatrix}0\\1\\3\end{pmatrix}.\]
\begin{itemize}
\item A receives nothing; B receives A's value of 1.
\item C receives A's and B's values: $1+2=3$.
\item C's own value is not added: there is no self-loop.
\end{itemize}''','Keep the vector values distinct from degrees. This is an algebraic aggregation, not observed information flow.',(25,27))
add('Matrix multiplication links two steps',r'''\[(A^2)_{ij}=\sum_{k=1}^n A_{ik}A_{kj}.\]
\begin{itemize}
\item Choose an intermediate actor $k$.
\medskip\item The product is 1 when both $i\to k$ and $k\to j$ exist.
\medskip\item Sum over all possible intermediaries.
\end{itemize}
Thus $(A^2)_{ij}$ counts \textbf{walks of length two} from $i$ to $j$.''','Use a binary unweighted graph. Matrix powers with weighted entries sum products of weights, not unweighted walk counts.',(27,30))
add('A worked two-step connection',r'''In the six-person graph, A can reach D through C:
\[(A^2)_{AD}
=\begin{pmatrix}0&1&1&0&0&0\end{pmatrix}
\begin{pmatrix}0\\0\\1\\0\\1\\0\end{pmatrix}=1.\]
\begin{center}\network{A/B,A/C,B/C,C/D,D/E}\end{center}
Only the intermediate actor C contributes a nonzero product.''','The row is row A, the column is column D. Point to A-C-D on the graph. This same formula is a common-neighbour count in an undirected network.',(30,32))
add('Walks, paths, and matrix powers',r'''\begin{itemize}
\item A \textbf{walk} follows adjacent ties and may repeat actors or edges.
\medskip\item A \textbf{path} does not repeat actors.
\medskip\item $(A^\ell)_{ij}$ counts length-$\ell$ walks, not necessarily paths.
\end{itemize}
\[A\!\to\! B\!\to\! A\quad\text{is a two-step walk, not a path.}\]
In our undirected graph, $(A^2)_{ii}=k_i$: one return walk through each neighbour.''','Use arrows here to show the order of traversal, not directed edges in the undirected graph. In a directed network diagonal A squared counts reciprocal return walks and need not equal degree.',(32,35))
add('Exercise: two-step counts',r'''\begin{center}\network{A/B,A/C,B/C,C/D,D/E}\end{center}
Without multiplying the whole matrix, find:
\[(A^2)_{AA},\qquad(A^2)_{AB},\qquad(A^2)_{AE}.\]
List the contributing walks. Can a zero entry in $A^2$ rule out a longer connection?''','Four minutes, individual then compare with a neighbour. Expected 2, 1, 0. A reaches E in three steps.',(35,39),'HAND CALCULATION: 4 MINUTES')
add('Answer: what a zero does and does not mean',r'''\begin{align*}
(A^2)_{AA}&=2&&\text{via A--B--A and A--C--A},\\
(A^2)_{AB}&=1&&\text{via A--C--B},\\
(A^2)_{AE}&=0&&\text{no two-step walk}.
\end{align*}
But A--C--D--E is a three-step path, so $(A^3)_{AE}\geq1$.
\medskip
\textcolor{accent}{A zero in one matrix power rules out one length, not all lengths.}''','For this graph A cubed at A,E is exactly one. Distinguish no tie, no walk of a particular length, and unreachable.',(39,42))
add('Reachability from matrix powers',r'''For distinct actors in a finite graph,
\[j\text{ is reachable from }i
\iff \sum_{\ell=1}^{n-1}(A^\ell)_{ij}>0.\]
\begin{itemize}
\item If any walk exists, a path exists after removing loops in the walk.
\medskip\item A path visits each actor at most once: its length is at most $n-1$.
\medskip\item This explains reachability; software usually uses graph-search algorithms.
\end{itemize}''','This is a statement for nonnegative binary adjacency, with reachability between distinct actors. Do not recommend computing huge matrix powers for large sparse networks: counts grow and numerical overflow becomes possible.',(42,45))
add('Shortest paths and geodesic distance',r'''\[d(i,j)=\min\{\ell\geq1:(A^\ell)_{ij}>0\}\qquad(i\ne j).\]
\begin{itemize}
\item Set $d(i,i)=0$.
\medskip\item If $j$ is unreachable from $i$, set $d(i,j)=\infty$.
\medskip\item Here $d(A,E)=3$ via A--C--D--E, but $d(A,F)=\infty$.
\end{itemize}
Unweighted distance counts ties. It does not measure physical distance or elapsed time.''','A shortest unweighted walk between distinct actors is a path: a repeated cycle could be removed to shorten it.',(45,48))
add('The distance matrix',r'''\[\Delta=\disto\]
\begin{itemize}
\item Symmetric here because the network is undirected.
\item Infinite entries record genuinely unreachable pairs in this graph.
\end{itemize}''','Use Delta to avoid confusing distance matrix with degree diagonal D in the appendix. Ask students to read C,E and E,C, then F,A. Infinity is not a missing-data code.',(48,51))
add('Connected components',r'''A component is a maximal set of actors connected by paths.
\begin{center}\network{A/B,A/C,B/C,C/D,D/E}\end{center}
\[\{A,B,C,D,E\}\qquad\text{and}\qquad\{F\}.\]
Reordering nodes by component makes $A$ block diagonal: no ties, and no walks, cross between blocks.''','Maximal means no further node can be added while preserving connection to the set. An isolate is a component of size one. Our node order already groups components, with a five-by-five block and a zero block.',(51,54))
add('Connectivity in a directed graph',r'''\begin{center}\network[-{Stealth[length=2mm]}]{A/B,A/C,B/C,C/D,D/E}\end{center}
\begin{itemize}
\item \textbf{Weak connectivity:} connected after ignoring directions.
\medskip\item \textbf{Strong connectivity:} each actor can reach every other in the set by following directions.
\end{itemize}
A can reach E; E cannot reach A. A--E form one weak component, but each actor is its own strong component.''','The graph is a directed acyclic nomination network. F forms its own weak and strong component. Advice-seeker to source arrows are nomination direction, not guaranteed direction of advice transmission.',(54,58))
add('Bridges and articulation points',r'''\begin{itemize}
\item A \textbf{bridge} is an edge whose removal increases the number of components.
\medskip\item An \textbf{articulation point} is a node whose removal increases the number of components.
\end{itemize}
\begin{center}\network{A/B,A/C,B/C,C/D,D/E}\end{center}
C--D and D--E are bridges; C and D are articulation points.''','Count all components, including F. Removing C creates AB, DE, and F: three instead of two. Removing D creates ABC, E, and F. E is a leaf, but not an articulation point. Definitions here are for the undirected graph.',(58,62))
add('Exercise: alternative routes',r'''Suppose we add B--D while retaining all original ties.
\begin{center}\network{A/B,A/C,B/C,C/D,D/E,B/D}\end{center}
\begin{enumerate}
\item Is C--D still a bridge?
\item Is C still an articulation point? What about D?
\item Which A-to-E shortest paths now exist?
\end{enumerate}''','Six minutes in pairs, including a quick check with another pair. Ask students to distinguish edge removal from node removal.',(62,68),'PAIRS: 6 MINUTES')
add('Answer: redundancy changes social position',r'''\begin{itemize}
\item C--D is no longer a bridge: C--B--D is an alternative route.
\medskip\item C is no longer an articulation point; D still separates E from the rest.
\medskip\item A--C--D--E and A--B--D--E are both shortest paths of length 3.
\end{itemize}
\medskip
C's degree stays 3, yet its exclusive brokerage disappears.
\textcolor{accent}{A position depends on the surrounding network, not only the actor's own ties.}''','Debrief for seven minutes, drawing the two routes. This anticipates the fractional counting rule in betweenness. B degree rises from two to three and D from two to three. F remains isolated.',(68,75))
add('Break',r'\begin{center}\Large 15 minutes\end{center}','Resume at minute 90. Ask students to keep the original graph handy for the centrality calculations.',(75,90))
add('Centrality depends on the research question',r'''\begin{center}\begin{tabular}{ll}
\toprule
Question & Candidate measure\\\midrule
How many direct partners? & Degree\\
How near are reachable others? & Closeness / harmonic\\
Who lies on shortest routes? & Betweenness\\
Who connects to highly scored actors? & Eigenvector / PageRank\\\bottomrule
\end{tabular}\end{center}
\bigskip
No single measure establishes influence, expertise, or power. Tie meaning and assumptions about the social process come first.''','Frame social position as multiple structural dimensions. A broker, a popular source, and an actor with prestigious contacts may be different people.',(90,93))
add('Degree and its matrix form',r'''\[\mathbf{k}=A\ones,\qquad C_D(i)=\frac{k_i}{n-1}.\]
For the undirected graph:
\[\mathbf{k}=(2,2,3,2,1,0)^{\mathsf T}.\]
\begin{itemize}
\item Normalising divides by the largest possible degree.
\medskip\item C has $C_D(C)=3/5=0.6$.
\medskip\item Degree ignores indirect connections and alternative routes.
\end{itemize}''','Brief retrieval rather than reteaching class 1. These are binary loopless degree formulas; weights require strength.',(93,95))
add('Closeness on a connected undirected network',r'''\[C_C(i)=\frac{n-1}{\sum_{j\ne i}d(i,j)}.\]
Consider only the connected five-person subgraph A--E:
\[C_C(C)=\frac4{1+1+1+2}=0.8,\qquad
C_C(D)=\frac4{2+2+1+1}=\frac23.\]
\begin{itemize}
\item Higher closeness means smaller average distance to others.
\item The calculation assumes finite distances to every other actor.
\end{itemize}''','Explicitly n=5 on this slide, not six. Conventional normalised closeness is reciprocal average distance. It may suit a process where short routes are substantively relevant.',(95,98))
add('What happens when actors are unreachable?',r'''Including F gives $d(C,F)=\infty$.
\[\sum_{j\ne C}d(C,j)=\infty.\]
\begin{itemize}
\item The connected-network closeness formula loses its useful ranking.
\medskip\item Dropping unreachable actors changes the population being compared.
\medskip\item Software conventions differ: always state how unreachable pairs are handled.
\end{itemize}
We will use harmonic centrality for the full six-person graph.''','Under a literal extended-real reciprocal the connected formula gives zero for everyone; some software omits unreachable nodes instead. igraph closeness omits unreachable nodes and returns NaN for isolates, so do not present its output as the all-six formula. Source: https://r.igraph.org/reference/closeness.html.',(98,100))
add('Harmonic centrality handles unreachable actors',r'''\[C_H(i)=\frac{1}{n-1}\sum_{j\ne i}\frac1{d(i,j)},\qquad\frac1\infty=0.\]
\begin{itemize}
\item Direct neighbour: contribution 1; distance two: contribution $1/2$.
\medskip\item Unreachable actor: contribution 0.
\medskip\item An isolate has score 0; all six actors remain in the denominator.
\end{itemize}
This is a sum of reciprocal distances, not the reciprocal of a sum.''','Normalised harmonic centrality lies in zero to one for our unweighted simple graphs. With arbitrary weighted distances its range need not be bounded by one. Source: https://r.igraph.org/reference/harmonic_centrality.html.',(100,103))
add('Exercise: compare distance-based positions',r'''Distances to the other five actors are:
\begin{center}\begin{tabular}{lccccc}
\toprule
Actor & \multicolumn{5}{c}{Distances to the others}\\\midrule
C & 1 & 1 & 1 & 2 & $\infty$\\
D & 2 & 2 & 1 & 1 & $\infty$\\
F & $\infty$ & $\infty$ & $\infty$ & $\infty$ & $\infty$\\\bottomrule
\end{tabular}\end{center}
Calculate normalised harmonic centrality for C, D, and F.
\medskip
Which of C and D has better distance-based access?''','Four minutes. Require the common denominator five. Tie meanings and model of travel still determine whether this structural advantage is relevant.',(103,107),'HAND CALCULATION: 4 MINUTES')
add('Answer: harmonic centrality',r'''\begin{align*}
C_H(C)&=\frac{1+1+1+1/2+0}{5}=0.7,\\[1ex]
C_H(D)&=\frac{1/2+1/2+1+1+0}{5}=0.6,\\[1ex]
C_H(F)&=0.
\end{align*}
C is closer to more actors. The calculation retains the unreachable actor rather than silently removing it.''','Explain that harmonic centrality differs from closeness even in connected graphs: sum of inverses versus inverse sum. Scores should not be numerically interchanged.',(107,109))
add('Betweenness: participation in shortest routes',r'''For an undirected graph,
\[B(i)=\sum_{\substack{s<t\\s,t\ne i}}\frac{\sigma_{st}(i)}{\sigma_{st}}.\]
\begin{itemize}
\item $\sigma_{st}$: number of shortest paths between $s$ and $t$.
\item $\sigma_{st}(i)$: how many pass through $i$ as an internal actor.
\item Unreachable pairs contribute 0; endpoints do not count.
\end{itemize}
Betweenness assumes shortest routes are relevant to the process under study.''','Unordered pairs avoid double counting in an undirected graph. Directed betweenness sums ordered source-target pairs. Brokerage in practice does not necessarily follow shortest paths. Source: https://r.igraph.org/reference/betweenness.html.',(109,112))
add("Counting C's betweenness",r'''\begin{center}\network{A/B,A/C,B/C,C/D,D/E}\end{center}
The pairs whose unique shortest route passes through C are
\[\{A,D\},\quad\{A,E\},\quad\{B,D\},\quad\{B,E\}.\]
Each contributes 1, so $B(C)=4$. Similarly, $B(D)=3$.
\medskip
Pairs involving F are unreachable and add nothing.''','D lies between A,E; B,E; and C,E. A,B are endpoints for some routes but never internal on a shortest route. Count explicitly rather than equating bridges with scores.',(112,115))
add('Equal shortest paths split the contribution',r'''\begin{center}
\begin{tikzpicture}[actor/.style={circle,draw=accent,fill=pale,minimum size=8mm},every path/.style={draw=edge,thick}]
\node[actor](S) at (0,0){S};\node[actor](U) at (2,1){U};\node[actor](V) at (2,-1){V};\node[actor](T) at (4,0){T};
\draw(S)--(U)--(T);\draw(S)--(V)--(T);
\end{tikzpicture}\end{center}
Two shortest S-to-T paths exist: S--U--T and S--V--T.
\[\frac{\sigma_{ST}(U)}{\sigma_{ST}}=\frac12,\qquad
\frac{\sigma_{ST}(V)}{\sigma_{ST}}=\frac12.\]
These are contributions from one pair, not the actors' full betweenness scores.''','Make clear this separate diamond graph illustrates counting only; node labels differ from the main graph. Avoid reporting U or V total betweenness as one half without including all pairs.',(115,117))
add('Normalising betweenness',r'''There are $\binom{n-1}{2}$ unordered pairs excluding actor $i$.
\[C_B(i)=\frac{B(i)}{\binom{n-1}{2}}
=\frac{2B(i)}{(n-1)(n-2)}.\]
For C in the six-person graph:
\[C_B(C)=\frac4{\binom52}=\frac4{10}=0.4.\]
The denominator includes pairs involving F, even though they contribute zero to the numerator.''','Use n=6 consistently. Component-only normalisation would give a different score, 4/6 for C in the five-node component. Directed normalisation uses (n-1)(n-2). Source: igraph betweenness documentation.',(117,119))
add('Different measures describe different positions',r'''\begin{center}\begin{tabular}{lrrrr}
\toprule
Actor & Degree & Harmonic & Betweenness & Eigenvector\\\midrule
A & 2 & .567 & 0 & .824\\
B & 2 & .567 & 0 & .824\\
C & 3 & .700 & 4 & 1.000\\
D & 2 & .600 & 3 & .567\\
E & 1 & .433 & 0 & .256\\
F & 0 & .000 & 0 & .000\\\bottomrule
\end{tabular}\end{center}
A and D have equal degree. D has more brokerage; A has more recursive centrality.
\medskip
{\footnotesize Harmonic normalised by $n-1$; betweenness raw; eigenvector scaled to maximum 1.}''','Values checked in igraph. Explain eigenvector column only intuitively for now: A connects to B and C, both strongly embedded. We derive it after discussing weights. Different columns have different scales; compare actors within columns, not numerical values across columns.',(119,122))
add('Which position matters for your question?',r'''\begin{itemize}
\item Reaching many direct collaborators: consider degree or strength.
\medskip\item Access through short routes: consider harmonic centrality.
\medskip\item Connecting otherwise separated circles: examine brokerage and alternative routes.
\medskip\item Being nominated by highly scored sources: consider recursive prestige measures.
\end{itemize}
What additional evidence would you need before calling an actor ``influential''?''','Three-minute discussion. Require students to name a tie definition and a plausible process. Prestige as receiving nominations is not identical to contact volume.',(122,125))
add('Weights can mean strength or distance',r'''\begin{itemize}
\item For shortest paths, weights must represent \textbf{costs or lengths}: larger means harder or farther.
\medskip\item Interaction frequency usually represents \textbf{strength}: larger means more frequent contact.
\medskip\item If appropriate, define a separate cost $\ell_{ij}=1/w_{ij}$ for $w_{ij}>0$.
\end{itemize}
\medskip
That conversion is a substantive assumption, not an automatic correction.
In igraph, \texttt{weights = NA} explicitly requests unweighted paths.''','Distance-based igraph measures use the weight attribute by default when present. PageRank and eigenvector centrality treat positive weights as strengths instead. Never blindly reuse interaction counts as distances. Sources: igraph betweenness, harmonic centrality, and PageRank documentation.',(125,130))
add("Recursive centrality: neighbours' scores matter",r'''Degree assigns every neighbour the same contribution:
\[k_i=\sum_j A_{ij}\times1.\]
Eigenvector centrality instead uses the neighbours' scores:
\[x_i=\frac1\lambda\sum_j A_{ij}x_j.\]
An actor receives a high score by connecting to other highly scored actors.
\medskip
We need scores that are mutually consistent across the whole network.''','Work with the undirected graph first so the matrix orientation is unambiguous. This is a definition of recursive importance, not independent evidence of influence.',(130,133))
add('An eigenvector keeps its direction under multiplication',r'''Collect the actor scores in $\mathbf{x}$:
\[A\mathbf{x}=\lambda\mathbf{x},\qquad\mathbf{x}\ne\mathbf{0}.\]
\begin{itemize}
\item $\mathbf{x}$ is an \textbf{eigenvector}; $\lambda$ is its \textbf{eigenvalue}.
\medskip\item Multiplication changes the scale of $\mathbf{x}$, not its direction.
\medskip\item For a connected undirected graph with nonnegative ties, use the positive leading eigenvector.
\end{itemize}
Scale is arbitrary: if $\mathbf{x}$ works, so does $c\mathbf{x}$ for $c>0$.''','Leading means the eigenvalue equal to the spectral radius for a nonnegative adjacency. In our graph the isolate has score zero and the five-node component supplies the leading vector. Do not claim all eigenvectors are centrality scores.',(133,136))
add('Repeated multiplication builds recursive scores',r'''Start with $\mathbf{x}^{(0)}=\ones$ and iterate:
\[\widetilde{\mathbf{x}}^{(t+1)}=A\mathbf{x}^{(t)},\qquad
\mathbf{x}^{(t+1)}=\frac{\widetilde{\mathbf{x}}^{(t+1)}}{\max_i\widetilde{x}^{(t+1)}_i}.\]
\begin{itemize}
\item First update: proportional to degree.
\item Further updates count neighbours weighted by their previous scores.
\item Normalisation prevents the values from growing without bound.
\end{itemize}
Our non-bipartite connected component supports convergence. Other graphs can need different numerical treatment.''','The triangle makes the nontrivial component non-bipartite. Plain power iteration can oscillate on bipartite graphs; do not demonstrate it as universally convergent. For this graph the initial isolate score becomes zero after one multiplication. Notebook includes a shifted iteration extension.',(136,139))
add('Checking an eigenvector numerically',r'''For our graph, with maximum score set to 1,
\[\mathbf{x}\approx(.824,.824,1,.567,.256,0)^{\mathsf T},
\qquad\lambda\approx2.214.\]
For actor C,
\[(A\mathbf{x})_C=x_A+x_B+x_D
\approx.824+.824+.567=2.215\approx\lambda x_C.\]
For actor E,
\[(A\mathbf{x})_E=x_D\approx.567\approx2.214\times.256.\]
{\footnotesize Small discrepancies reflect rounding.}''','Show the residual Ax minus lambda x in R. A is symmetric, so ordinary symmetric eigen decomposition applies. A and B have equal values due to their identical surrounding roles under interchange.',(139,141))
add('Directed prestige needs the transpose',r'''With $A_{ij}=1$ for $i\to j$, incoming prestige satisfies
\[x_j\propto\sum_i A_{ij}x_i
\quad\Longrightarrow\quad A^{\mathsf T}\mathbf{x}=\lambda\mathbf{x}.\]
\begin{itemize}
\item A directed acyclic graph has no positive adjacency eigenvalue.
\medskip\item Disconnected graphs may concentrate scores in one component.
\medskip\item Prestige depends on what a nomination represents.
\end{itemize}
Our directed advice graph is acyclic: PageRank is a more useful recursive example here.''','For a DAG adjacency is nilpotent: sufficiently high powers are zero. igraph uses the left adjacency eigenvector for directed eigenvector centrality. Do not run directed eigen_centrality on this DAG as if it returned meaningful prestige. Source: https://r.igraph.org/reference/eigen_centrality.html.',(141,143))
add('PageRank: share attention across outgoing ties',r'''Define a row-stochastic matrix $P$:
\[P_{ij}=\frac{A_{ij}}{k_i^{\mathrm{out}}}\quad\text{if }k_i^{\mathrm{out}}>0.\]
\begin{itemize}
\item An actor divides its attention across outgoing neighbours.
\item At a node with no outgoing ties, use a uniform row: $P_{ij}=1/n$.
\item With probability $1-\alpha$, jump to an actor sampled from $\mathbf{v}$.
\end{itemize}
Here $\mathbf{v}=\ones/n$ and $\alpha=0.85$.''','This is a mathematical random-surfer model following the stated nomination arrows, not a literal account of how advice travels. Uniform dangling rows match the uniform teleportation example used in the notebook. Positive edge weights would normalise by outgoing strength.',(143,146))
add('PageRank as a linear system',r'''For a column vector of probabilities $\mathbf{p}$,
\[\mathbf{p}=\alpha P^{\mathsf T}\mathbf{p}+(1-\alpha)\mathbf{v},
\qquad\sum_i p_i=1.\]
Rearrange:
\[\boxed{(I-\alpha P^{\mathsf T})\mathbf{p}=(1-\alpha)\mathbf{v}.}\]
\begin{itemize}
\item $I$ leaves a vector unchanged: $I\mathbf{p}=\mathbf{p}$.
\item $0<\alpha<1$ and positive uniform teleportation give a unique probability vector.
\end{itemize}''','Show that an n-by-n matrix multiplies an n-by-one vector on both sides. Notebook solves this system and compares with igraph. It is not necessary to compute an explicit matrix inverse. Source: https://r.igraph.org/reference/page_rank.html.',(146,149))
add('Linear algebra connects the measures',r'''\begin{center}\begin{tabular}{ll}
\toprule
Operation & Network interpretation\\\midrule
$A\ones$, $A^{\mathsf T}\ones$ & Out-degree, in-degree\\
$(A^\ell)_{ij}$ & Number of length-$\ell$ walks\\
First nonzero power at $(i,j)$ & Shortest unweighted distance\\
$A\mathbf{x}=\lambda\mathbf{x}$ & Undirected recursive centrality\\
$(I-\alpha P^{\mathsf T})\mathbf{p}=(1-\alpha)\mathbf{v}$ & PageRank\\\bottomrule
\end{tabular}\end{center}
Harmonic centrality and betweenness use shortest-path information derived from the graph.''','One-minute recap. Avoid claiming all measures are simple matrix powers: betweenness also needs counts and participation of shortest routes.',(149,150))
add('R practical: verify, compare, and explain',r'''Open \texttt{code/Lecture2\_SNA.Rmd}.
\begin{enumerate}
\item Verify one matrix product and one two-step walk count.
\medskip\item Calculate distances, components, and centrality scores.
\medskip\item Add B--D and explain which actor's position changes.
\medskip\item Verify $A\mathbf{x}\approx\lambda\mathbf{x}$ or the PageRank linear system.
\end{enumerate}''','150--153: setup and task allocation. Notebook core tasks are sized for the 25-minute practical; PageRank and advanced extensions can be completed after class. Students with slower setup work in pairs.',(150,153))
add('Key R operations',r'''\begin{lstlisting}
A %*% x                 # Matrix-vector multiplication
A %*% A                 # Two-step walk counts
A^2                     # Elementwise square: a different operation

distances(g, weights = NA)
components(g)
harmonic_centrality(g, normalized = TRUE, weights = NA)
betweenness(g, normalized = FALSE, weights = NA)
eigen_centrality(g, weights = NA)$vector
\end{lstlisting}
For binary $A$, \texttt{A\^{}2} equals $A$ and does not count two-step walks.''','153--159: students complete task 1 then compare their distances and scores. Note R uses elementwise powers for matrices; matrix powers must be built with matrix products. Functions were checked against igraph documentation.',(153,159),fragile=True)
add('Perturbation: add one alternative route',r'''\begin{center}\network{A/B,A/C,B/C,C/D,D/E,B/D}\end{center}
\begin{itemize}
\item Predict C's degree and betweenness before recomputing.
\item Compare the changes for B, C, and D.
\item Does a high score identify an indispensable actor?
\end{itemize}''','159--168: nine-minute perturbation task. C degree remains three; raw betweenness falls four to one. B becomes one, D remains three. Bridge and articulation-point status give a separate view of indispensability.',(159,168),'PREDICT, THEN CHECK')
add('Interpret the results as a researcher',r'''Choose one actor and explain its position using two measures.
\begin{itemize}
\item State the tie definition and the population being analysed.
\medskip\item Explain the measures' different assumptions.
\medskip\item Identify one conclusion the scores do not support.
\end{itemize}
\medskip
Optional mathematical check: compare an eigenvector residual or manual PageRank with the package output.''','168--175: pairs write three sentences and discuss two examples as a class. Do not require every pair to finish the PageRank extension within the session.',(168,175))
add('Exit question',r'''An actor's degree stays unchanged after a new tie is added between two other actors. Its betweenness falls sharply.
\begin{enumerate}
\item How can both statements be true?
\medskip\item Which feature of the surrounding network changed?
\medskip\item Why does $A^2$ count walks rather than only paths?
\end{enumerate}''','Three minutes individually. Use answers to assess whether students distinguish direct ties, alternative routes, and repeated actors.',(175,178))
add('What you should take away',r'''\begin{itemize}
\item Matrix products describe indirect routes and neighbour aggregation.
\medskip\item Connectivity determines which actors can reach one another.
\medskip\item Centrality measures capture different structural positions.
\medskip\item A new alternative route can change brokerage without changing degree.
\medskip\item Scores require a tie definition and a plausible social interpretation.
\end{itemize}''','178--180: exit answer: the new edge provides an alternative route bypassing the actor; matrix multiplication permits repeated actors, such as A-B-A. Next class: collecting, preparing, and visualising empirical network data.',(178,180))
add('Reading and references',r'''\small
\begin{itemize}
\item Borgatti et al. (2022). \emph{Analyzing Social Networks Using R}. Mathematical foundations and chapters on node measures and centrality.
\medskip\item Kolaczyk \& Cs\'{a}rdi (2020). \emph{Statistical Analysis of Network Data with R}, 2nd ed. Chapters 2 and 4; selected mathematical-model sections.
\medskip\item Implementation details: \href{https://r.igraph.org/reference/harmonic_centrality.html}{harmonic centrality}, \href{https://r.igraph.org/reference/betweenness.html}{betweenness}, \href{https://r.igraph.org/reference/eigen_centrality.html}{eigenvector centrality}, and \href{https://r.igraph.org/reference/page_rank.html}{PageRank} in the igraph documentation.
\end{itemize}''','Reference slide outside the timed session. All plotted networks and numerical examples are synthetic. The notebook includes reproducible calculations and checks.')
add('Appendix: the graph Laplacian',r'''For an undirected graph, let $D=\operatorname{diag}(k_1,\ldots,k_n)$.
\[L=D-A,\qquad L\ones=\mathbf{0}.\]
For actor $i$,
\[(L\mathbf{x})_i=k_ix_i-\sum_j A_{ij}x_j
=\sum_j A_{ij}(x_i-x_j).\]
The result compares the actor's value with its neighbours' values.
\medskip
The number of zero eigenvalues of $L$ equals the number of connected components.''','Optional extension, not part of the 180 minutes. For the six-node graph there are two zero eigenvalues. Use D for the degree diagonal and Delta for distances. This is for undirected graphs with nonnegative weights.',appendix=True)
add('Appendix: a quadratic form measures disagreement',r'''For the unweighted undirected graph,
\[\mathbf{x}^{\mathsf T}L\mathbf{x}
=\frac12\sum_{i,j}A_{ij}(x_i-x_j)^2
=\sum_{\{i,j\}\in E}(x_i-x_j)^2.\]
\begin{itemize}
\item Each edge contributes the squared difference between its endpoints.
\medskip\item If values are constant within every component, the expression is zero.
\medskip\item This links connectivity to smoothing and spectral methods.
\end{itemize}''','Optional. Binary values x=(0,0,0,1,1,0) give energy one because only C-D crosses between values. This connects later to community detection without deriving a clustering algorithm.',appendix=True)
add('Appendix: structural equivalence',r'''Actors can have similar positions without being adjacent.
For distinct $i$ and $j$, compare ties to all other actors:
\[A_{ik}=A_{jk}\quad\text{for all }k\notin\{i,j\}.\]
For directed data, compare incoming ties as well.
\medskip
In our undirected network, A and B have identical ties to everyone outside their pair. Interchanging A and B leaves the graph unchanged.
\medskip
\textcolor{accent}{Centrality describes a score; equivalence compares patterns of relations.}''','Optional sociological extension. The pair-excluded definition accommodates adjacent actors; strict full-row equality would fail due to the diagonal and mutual edge entries. Distinguish structural equivalence from looser role or regular equivalence.',appendix=True)
add('Appendix: a stable power iteration',r'''On a connected undirected graph with at least one edge, use
\[\widetilde{\mathbf{x}}^{(t+1)}=(A+I)\mathbf{x}^{(t)}\]
followed by normalisation.
\begin{itemize}
\item If $A\mathbf{x}=\lambda\mathbf{x}$, then $(A+I)\mathbf{x}=(\lambda+1)\mathbf{x}$.
\medskip\item Eigenvectors are unchanged; eigenvalues shift by 1.
\medskip\item The positive diagonal prevents the bipartite oscillation of ordinary adjacency power iteration.
\end{itemize}''','Optional extension. This is a numerical device, not a substantive claim that the observed graph has self-ties. With the full disconnected six-node graph, the nontrivial component still dominates the isolate. Notebook uses the shift as an optional robustness check.',appendix=True)
# Export standalone source and a machine-readable record for the teaching guide.
parts=[preamble,r'\begin{document}']
for q in slides:
 if q['appendix'] and not any(x=='\\appendix' for x in parts): parts.append(r'\appendix')
 parts.append(r'\begin{frame}'+('[fragile]' if q['fragile'] else '')+'{'+q['title']+'}')
 if q['activity']:parts.append(r'\activity{'+q['activity']+'}')
 parts.append(q['body'])
 timing=(str(q['minutes'][0])+'--'+str(q['minutes'][1])+' min. ') if q['minutes'] else ''
 parts.append(r'\note{'+timing+q['note']+'}')
 parts.append(r'\end{frame}')
parts.append(r'\end{document}')
(root/'meeting_slides/session_02/main.tex').write_text('\n\n'.join(parts)+'\n')
(root/'.build/session02/slides.json').write_text(json.dumps(slides,indent=2))
guide='''# Session 2: Connectivity, centrality, and social position

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
| 150–175 | Guided R practical and interpretation |
| 175–180 | Exit question and recap |

The reference slide and four appendix slides are outside the timed core. The Laplacian, structural equivalence, and shifted iteration are optional, not additional material to squeeze into the three hours.

## Preparation

- Students need igraph and the notebook `code/Lecture2_SNA.Rmd`. The HTML version supports reading without running R.
- Review row-source adjacency, summation notation, row/column vectors, and degree from session 1. No previous eigenvalue course is assumed.
- Notebook tasks 1–4 form the 25-minute practical. The fully worked manual PageRank calculation and sensitivity exercises can be finished after class.
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

'''
for i,q in enumerate(slides,1):
 timing=f"{q['minutes'][0]}–{q['minutes'][1]} min. " if q['minutes'] else ('Optional appendix. ' if q['appendix'] else '')
 guide+=f"### {i}. {q['title']}\n\n{timing}{q['note']}\n\n"
(root/'meeting_slides/Session_02_teaching_guide.md').write_text(guide)
print('Slides:',len(slides),'core including reference:',sum(not q['appendix'] for q in slides))
