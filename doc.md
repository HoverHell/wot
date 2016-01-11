
## Web of Trust system <a name="Web_of_Trust_system" href="#Web_of_Trust_system">§</a> ##

### Use cases <a name="Use_cases" href="#Use_cases">§</a> ###

Querying of graph-determined tagged-trust of identified users.


### System Design <a name="System_Design" href="#System_Design">§</a> ###

#### User identifier <a name="User_identifier" href="#User_identifier">§</a> ####

Multiple methods, each can have multiple identifiers
per user.

Technically, multiple identifiers are equivalent to a clique with
full-trust edges. Practically, not all identities can assign trust
(e.g. non-cryptographic ones might not be able to), and querying can
be optimised for those cliques.

<ol manual=1>
 <li value="1"><a name="Web_of_Trust_system__System_Design__User_identifier__1"></a>
 email
 </li>
 <li value="2"><a name="Web_of_Trust_system__System_Design__User_identifier__2"></a>
 email md5
   <ol manual=1>
   <li value="2.1"><a name="Web_of_Trust_system__System_Design__User_identifier__2_1"></a>
   Use case: comments. See: gravatar.
   </li>
   </ol>
 </li>
 <li value="3"><a name="Web_of_Trust_system__System_Design__User_identifier__3"></a>
 pgp
 </li>
 <li value="4"><a name="Web_of_Trust_system__System_Design__User_identifier__4"></a>
 pluggable anything
   <ol manual=1>
   <li value="4.1"><a name="Web_of_Trust_system__System_Design__User_identifier__4_1"></a>
   e.g. social network identifiers.
   </li>
   </ol>
 </li>
 </ol>

Each user is considered to be a single node un the graph.


#### Tagging <a name="Tagging" href="#Tagging">§</a> ####

Query tags. Examples:

<ol manual=1>
 <li value="1"><a name="Web_of_Trust_system__System_Design__Tagging__1"></a>
 “general”
   <ol manual=1>
   <li value="1.1"><a name="Web_of_Trust_system__System_Design__Tagging__1_1"></a>
   A special case, e.g. for mixing into trust with other tags and/or
        where no trust per other tags are available.
     <ol manual=1>
     <li value="1.1.1"><a name="Web_of_Trust_system__System_Design__Tagging__1_1_1"></a>
     Design decision TODO.
     </li>
     <li value="1.1.2"><a name="Web_of_Trust_system__System_Design__Tagging__1_1_2"></a>
     Possibly, allow users to include a <code>f(trusts) -&gt; float</code> in a query.
       <ol manual=1>
       <li value="1.1.2.1"><a name="Web_of_Trust_system__System_Design__Tagging__1_1_2_1"></a>
       ...
       </li>
       </ol>
     </li>
     </ol>
   </li>
   </ol>
 </li>
 <li value="2"><a name="Web_of_Trust_system__System_Design__Tagging__2"></a>
 “service”
 </li>
 <li value="3"><a name="Web_of_Trust_system__System_Design__Tagging__3"></a>
 “commodity”
 </li>
 <li value="4"><a name="Web_of_Trust_system__System_Design__Tagging__4"></a>
 “ideology”
 </li>
 </ol>


#### Graph assigning <a name="Graph_assigning" href="#Graph_assigning">§</a> ####

User action: set a node in the graph.

<ol manual=1>
 <li value="1"><a name="Web_of_Trust_system__System_Design__Graph_assigning__1"></a>
 Way one: <code>set (self, user_id, tag) = trust</code>
   <ol manual=1>
   <li value="1.1"><a name="Web_of_Trust_system__System_Design__Graph_assigning__1_1"></a>
   Trust is always <code>0 .. 1</code>.
   </li>
   </ol>
 </li>
 <li value="2"><a name="Web_of_Trust_system__System_Design__Graph_assigning__2"></a>
 Way two: log a rated interaction <code>add (self, user_id, tag) &lt;- trust</code>
   <ol manual=1>
   <li value="2.1"><a name="Web_of_Trust_system__System_Design__Graph_assigning__2_1"></a>
   Design TODO: Can possibly use bayesian score to compute the
        resulting trust.
   </li>
   </ol>
 </li>
 </ol>

Possible action: unset a node in the graph (set to `NaN`). TODO:
results of it are unclear.


#### Federation <a name="Federation" href="#Federation">§</a> ####

<ol manual=1>
 <li value="1"><a name="Web_of_Trust_system__System_Design__Federation__1"></a>
 Useful for personal servers and clustered servers.
 </li>
 <li value="2"><a name="Web_of_Trust_system__System_Design__Federation__2"></a>
 Requires identities to be somehow associated with addresses
   <ol manual=1>
   <li value="2.1"><a name="Web_of_Trust_system__System_Design__Federation__2_1"></a>
   Possibly by setting metainformation for the user_id
     <ol manual=1>
     <li value="2.1.1"><a name="Web_of_Trust_system__System_Design__Federation__2_1_1"></a>
     Might require the messages to be somehow signed for security.
            E.g. a query-signing key associated with the user with
            the secret part present on the server that answers the queries
            directed to that user.
     </li>
     </ol>
   </li>
   </ol>
 </li>
 <li value="3"><a name="Web_of_Trust_system__System_Design__Federation__3"></a>
 Inter-server traffic encryption is recommended but not particularly required.
 </li>
 <li value="4"><a name="Web_of_Trust_system__System_Design__Federation__4"></a>
 It should be possible to group inter-server queries (<code>Packet</code>s)
    and responses (for optimisation).
 </li>
 <li value="5"><a name="Web_of_Trust_system__System_Design__Federation__5"></a>
 TODO: Whether a <code>Packet</code>'s actual return address can be different
    from the address of the server that sends the query is
    uncertain. Probably shouldn't be.
 </li>
 </ol>


TODO: further design.


#### Graph hiding <a name="Graph_hiding" href="#Graph_hiding">§</a> ####

Currently it is considered near-impossible to hide the relations graph
from someone who can control the user's traffic.

At most it can be made noisier (bitcoin-transactions-like).

The particular weights might be hidden, however it might still be
possible to mine them out.

<ol manual=1>
 <li value="1"><a name="Web_of_Trust_system__System_Design__Graph_hiding__1"></a>
 Simple problem-case is that user A sends a Packet to user B with
    target_user_id `A`, therefore possibly finding out the precise trust
    assigned at `B->A`. Whether that trust is direct or derived can be
    determined by timing and ttl.
   <ol manual=1>
   <li value="1.1"><a name="Web_of_Trust_system__System_Design__Graph_hiding__1_1"></a>
   Possibly, each user should recurse over edges regardless of
        having a direct trust.
   </li>
   </ol>
 </li>
 </ol>

TODO: Further research.


#### Querying <a name="Querying" href="#Querying">§</a> ####

User action: find out the practical reputation of another user.

<ol manual=1>
 <li value="1"><a name="Web_of_Trust_system__System_Design__Querying__1"></a>
 <code>Query</code>: <code>{uuid, target_user_id, reputation_func}</code>
   <ol manual=1>
   <li value="1.1"><a name="Web_of_Trust_system__System_Design__Querying__1_1"></a>
   <code>uuid</code> is the unique identifier of the Query (used later).
   </li>
   <li value="1.2"><a name="Web_of_Trust_system__System_Design__Querying__1_2"></a>
   <code>target_user_id</code> is the User identifier of the user whose
         reputation is queried.
   </li>
   <li value="1.3"><a name="Web_of_Trust_system__System_Design__Querying__1_3"></a>
   <code>reputation_func</code> is the pure-functional low-computation
         function (represented as a string) that converts per-tag
         reputation to a single value, i.e.
         `reputation_func({(string)tag_name: (float)rep, …}) -> (float)resulting_reputation`.
     <ol manual=1>
     <li value="1.3.1"><a name="Web_of_Trust_system__System_Design__Querying__1_3_1"></a>
     At first only few specific constants should be allowed in
            `reputation_func` that have corresponding implementations
            in the codebase, such as `reps.get("some_tag", reps["general"])`.
     </li>
     </ol>
   </li>
   </ol>
 </li>
 <li value="2"><a name="Web_of_Trust_system__System_Design__Querying__2"></a>
 <code>Packet</code>: <code>{(Query)query, requested_user_id, return_address, ttl, rep_cutoff}</code>
   <ol manual=1>
   <li value="2.1"><a name="Web_of_Trust_system__System_Design__Querying__2_1"></a>
   <code>requested_user_id</code> is the user identifier of the user who is
        asked for reputation evaluation (i.e. packet target).
   </li>
   <li value="2.2"><a name="Web_of_Trust_system__System_Design__Querying__2_2"></a>
   <code>return_address</code> is the user identifier which should receive the
        evaluation result.
   </li>
   <li value="2.3"><a name="Web_of_Trust_system__System_Design__Querying__2_3"></a>
   <code>ttl</code> is IP-like time-to-live of the packet.
   </li>
   <li value="2.4"><a name="Web_of_Trust_system__System_Design__Querying__2_4"></a>
   <code>rep_cutoff</code> is minimal interesting reputation, for
        optimisational purposes.
     <ol manual=1>
     <li value="2.4.1"><a name="Web_of_Trust_system__System_Design__Querying__2_4_1"></a>
     TODO: needs further design and research.
     </li>
     </ol>
   </li>
   </ol>
 </li>
 <li value="3"><a name="Web_of_Trust_system__System_Design__Querying__3"></a>
 Query is “sent” from the source_user over all graph edges going
    from that user.
 </li>
 <li value="4"><a name="Web_of_Trust_system__System_Design__Querying__4"></a>
 When a Node with id <code>current_node_id</code> receives a Packet, it is
    expected to return the evaluation result.
   <ol manual=1>
   <li value="4.1"><a name="Web_of_Trust_system__System_Design__Querying__4_1"></a>
   The evaluation result is to be sent to <code>return_address</code>.
   </li>
   <li value="4.2"><a name="Web_of_Trust_system__System_Design__Querying__4_2"></a>
   Optimisations:
     <ol manual=1>
     <li value="4.2.1"><a name="Web_of_Trust_system__System_Design__Querying__4_2_1"></a>
     If the node has recently <em>started</em> answering a query with
          the same `uuid`, it can return the cached result avoiding
          further recursion.
       <ol manual=1>
       <li value="4.2.1.1"><a name="Web_of_Trust_system__System_Design__Querying__4_2_1_1"></a>
       TODO: The caching time is an uncertain parameter; might be
              configurable (in seconds or in max cache memory usage).
       </li>
       <li value="4.2.1.2"><a name="Web_of_Trust_system__System_Design__Querying__4_2_1_2"></a>
       If the node started answering that query but did not
                finish yet, it should return `NaN`. That way, loops are cut.
       </li>
       </ol>
     </li>
     <li value="4.2.2"><a name="Web_of_Trust_system__System_Design__Querying__4_2_2"></a>
     If <code>ttl</code> &lt;= 0, respond with <code>NaN</code> without further recursion.
     </li>
     </ol>
   </li>
   <li value="4.3"><a name="Web_of_Trust_system__System_Design__Querying__4_3"></a>
   If the node has a direct link to User <code>target_user_id</code>, it
        computes the reputation and responds.
     <ol manual=1>
     <li value="4.3.1"><a name="Web_of_Trust_system__System_Design__Querying__4_3_1"></a>
     <em>problematic</em>. See <a href="#Web_of_Trust_system__System_Design__Graph_hiding__1_1">gh_1.1</a>.
     </li>
     </ol>
   </li>
   <li value="4.4"><a name="Web_of_Trust_system__System_Design__Querying__4_4"></a>
   Otherwise it recurses the querying by sending a Packet with
        `return_address` set to `current_node_id` node's own id and
        decremented `ttl` to each of the node's edges.
     <ol manual=1>
     <li value="4.4.1"><a name="Web_of_Trust_system__System_Design__Querying__4_4_1"></a>
     Nodes with weights lower than <code>rep_cutoff</code> can be skipped (see <code>2.4.</code>)
       <ol manual=1>
       <li value="4.4.2"><a name="Web_of_Trust_system__System_Design__Querying__4_4_2"></a>
       Correspondingly, each packet's rep_cutoff should be set to a multiple of
       </li>
       </ol>
     </li>
     <li value="4.4.2"><a name="Web_of_Trust_system__System_Design__Querying__4_4_2"></a>
     The <code>return_address</code> replacement is for two reasons:
       <ol manual=1>
       <li value="4.4.2.1"><a name="Web_of_Trust_system__System_Design__Querying__4_4_2_1"></a>
       The results will be sent to that node so that it can
                multiply each result by own weight for the responding
                edge, and when all the results are obtained respond
                with own result.
       </li>
       <li value="4.4.2.2"><a name="Web_of_Trust_system__System_Design__Querying__4_4_2_2"></a>
       The quering might (or might not) be plausibly-deniable
                as there is no method to discern user's own queries from
                recursed queries.
         <ol manual=1>
         <li value="4.4.2.2.1"><a name="Web_of_Trust_system__System_Design__Querying__4_4_2_2_1"></a>
         For that reason the initial <code>ttl</code> needs to be
                    randomised (or removed in favor of
                    rep_cutoff). However, any randomisation can be
                    evened out statistically.
         </li>
         </ol>
       </li>
       </ol>
     </li>
     <li value="4.4.3"><a name="Web_of_Trust_system__System_Design__Querying__4_4_3"></a>
     Results are considered complete when either:
       <ol manual=1>
       <li value="4.4.3.1"><a name="Web_of_Trust_system__System_Design__Querying__4_4_3_1"></a>
       All nodes respond.
       </li>
       <li value="4.4.3.2"><a name="Web_of_Trust_system__System_Design__Querying__4_4_3_2"></a>
       Timeout is reached.
       </li>
       </ol>
     </li>
     <li value="4.4.4"><a name="Web_of_Trust_system__System_Design__Querying__4_4_4"></a>
     The results list (that might include <code>NaN</code>) are <em>somehow</em>
            combined into a single result.
       <ol manual=1>
       <li value="4.4.4.1"><a name="Web_of_Trust_system__System_Design__Querying__4_4_4_1"></a>
       TODO: probably by <code>max(results, default=NaN)</code>, but it is to be decided.
         <ol manual=1>
         <li value="4.4.4.1.1"><a name="Web_of_Trust_system__System_Design__Querying__4_4_4_1_1"></a>
         Should it be customisable, same as <code>reputation_func</code>?
         </li>
         </ol>
       </li>
       </ol>
     </li>
     </ol>
   </li>
   </ol>
 </li>
 </ol>


#### Implementations <a name="Implementations" href="#Implementations">§</a> ####

TODO.

A *reference* implementation, in e.g. python 3; asynchronous; possibly
with Cython (if performance becomes a concern).

Skipping possibly useful dependencies is not recommended.

Recommendations:

<ol manual=1>
 <li value="1"><a name="Web_of_Trust_system__System_Design__Implementations__1"></a>
 Separate parseable logging of all user-actions (up to ability to
    re-apply the actions).
 </li>
 <li value="2"><a name="Web_of_Trust_system__System_Design__Implementations__2"></a>
 Include all the useful dependencies; stripping them down if needed
    is doable.
 </li>
 </ol>


#### Extensibility <a name="Extensibility" href="#Extensibility">§</a> ####

A controversial point: some extending might be useful; however, it
becomes useful when most reference implementations use it. See: XMPP
(XEP) successes-and-failures-case. Possibly, discourage
reimplementations and skip plugins until a sufficient system is
implemented, and recommend implementation in the reference code of any
plugin. Plugin-like structure in the reference code might be useful
for that.