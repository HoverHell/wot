
## Web of Trust system ##

### Use cases ###

Tagged querying of trust of various identified users.


### System Design ###

#### User identifier ####

Multiple methods, each can have multiple identifiers
per user.

Technically, multiple identifiers are equivalent to a clique with
full-trust edges. Practically, not all identities can assign trust
(e.g. non-cryptographic ones can't), and querying can be optimised for
those cliques.

<ol manual=1>
 <li value="1">
 email
 </li>
 <li value="2">
 email md5
   <ol manual=1>
   <li value="2.1">
   Use case: comments. See: gravatar.
   </li>
   </ol>
 </li>
 <li value="3">
 pgp
 </li>
 <li value="4">
 pluggable anything
   <ol manual=1>
   <li value="4.1">
   e.g. social network identifiers.
   </li>
   </ol>
 </li>
 </ol>


#### Tagging ####

Query tags. Examples:

<ol manual=1>
 <li value="1">
 “general”
   <ol manual=1>
   <li value="1.1">
   A special case, e.g. for mixing into trust with other tags and/or
        where no trust per other tags are available.
     <ol manual=1>
     <li value="1.1.1">
     Design decision TODO.
     </li>
     <li value="1.1.2">
     Possibly, allow users to include a `f(trusts) -> float` in a query.
       <ol manual=1>
       <li value="1.1.2.1">
       ...
       </li>
       </ol>
     </li>
     </ol>
   </li>
   </ol>
 </li>
 <li value="2">
 “service”
 </li>
 <li value="3">
 “commodity”
 </li>
 <li value="4">
 “ideology”
 </li>
 </ol>


#### Graph assigning ####

User action: set a node in the graph.

<ol manual=1>
 <li value="1">
 Way one: `set (self, user_id, tag) = trust`
   <ol manual=1>
   <li value="1.1">
   Trust is always `0 .. 1`.
   </li>
   </ol>
 </li>
 <li value="2">
 Way two: log a rated interaction `add (self, user_id, tag) <- trust`
   <ol manual=1>
   <li value="2.1">
   Design TODO: Can possibly use bayesian score to compute the
        resulting trust.
   </li>
   </ol>
 </li>
 </ol>

Possible action: unset a node in the graph (set to `NaN`). TODO:
results of it are unclear.


#### Implementations ####

A *reference* implementation, in e.g. python 3; asynchronous; possibly
with Cython (if performance becomes a concern).

Skipping possibly useful dependencies is not recommended.

Recommendations:

<ol manual=1>
 <li value="1">
 Separate parseable logging of all user-actions (up to ability to
    re-apply the actions).
 </li>
 <li value="2">
 Include all the useful dependencies; stripping them down if needed
    is doable.
 </li>
 </ol>


#### Extensibility ####

A controversial point: some extending might be useful; however, it
becomes useful when most reference implementations use it. See: XMPP
(XEP) successes-and-failures-case. Possibly, discourage
reimplementations and skip plugins until a sufficient system is
implemented, and recommend implementation in the reference code of any
plugin. Plugin-like structure in the reference code might be useful
for that.